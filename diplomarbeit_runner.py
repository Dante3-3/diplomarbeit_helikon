#!/usr/bin/env python3
"""
Diplomarbeit LLM Test Runner
Processes one Teil at a time: calls Ollama API for all model/prompt/repetition combinations.
Usage: python3 diplomarbeit_runner.py <teil_key> (e.g. teil2, teil3, ... teil8)
"""

import json
import sys
import os
import time
import subprocess
import tempfile

CONFIG_PATH = "/Users/dstoilovski/Documents/Helikon/diplomarbeit_config.json"
OUTPUT_DIR = "/Users/dstoilovski/Documents/Helikon/diplomarbeit_output"
RESULTS_FILE = os.path.join(OUTPUT_DIR, "results.jsonl")
OLLAMA_URL = "http://localhost:11434/api/chat"

# Models for Teil 2-7 (English categories)
MODELS_STANDARD = ["mistral:latest", "gemma2:9b", "deepseek-r1:8b"]
# Models for Teil 8 (German category) - includes EuroLLM
MODELS_GERMAN = ["mistral:latest", "gemma2:9b", "deepseek-r1:8b", "jobautomation/OpenEuroLLM-German:latest"]

REPETITIONS = 3
MAX_USER_PROMPTS = 3  # Only first 3 user prompts


def call_ollama(model, system_prompt, user_prompt):
    """Call Ollama API via curl (more reliable for large payloads) and return the response text."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {"num_ctx": 16384}
    }

    # Write payload to temp file to avoid shell escaping issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
        json.dump(payload, tmp, ensure_ascii=False)
        tmp_path = tmp.name

    try:
        proc = subprocess.run(
            ["curl", "-s", "--max-time", "900", "-H", "Content-Type: application/json",
             "-d", f"@{tmp_path}", OLLAMA_URL],
            capture_output=True, text=True, timeout=920
        )
        if proc.returncode != 0:
            return f"[ERROR] curl failed (exit {proc.returncode}): {proc.stderr[:500]}"

        result = json.loads(proc.stdout)
        return result.get("message", {}).get("content", "")
    except subprocess.TimeoutExpired:
        return "[ERROR] Request timed out (900s)"
    except json.JSONDecodeError as e:
        return f"[ERROR] Invalid JSON response: {str(e)[:200]}"
    except Exception as e:
        return f"[ERROR] {str(e)}"
    finally:
        os.unlink(tmp_path)


def process_teil(teil_key):
    """Process all tests for one Teil."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    if teil_key not in config["teile"]:
        print(f"ERROR: {teil_key} not found in config. Available: {list(config['teile'].keys())}")
        sys.exit(1)

    teil = config["teile"][teil_key]
    teil_name = teil["name"]
    kategorie = teil["kategorie"]
    system_prompt = teil["system_prompt"]
    user_prompts = teil["user_prompts"][:MAX_USER_PROMPTS]

    models = MODELS_GERMAN if teil_key == "teil8" else MODELS_STANDARD

    total_calls = len(models) * len(user_prompts) * REPETITIONS
    current = 0

    print(f"=== Processing {teil_key}: {teil_name} ===")
    print(f"Models: {models}")
    print(f"User prompts: {len(user_prompts)}, Repetitions: {REPETITIONS}")
    print(f"Total API calls: {total_calls}")
    print()

    for model in models:
        for up in user_prompts:
            for rep in range(1, REPETITIONS + 1):
                current += 1
                test_id = up["id"]
                test_title = up["title"]
                user_prompt = up["prompt"]

                print(f"[{current}/{total_calls}] {model} | {test_id} | Rep {rep} ... ", end="", flush=True)
                start_time = time.time()

                response = call_ollama(model, system_prompt, user_prompt)

                elapsed = time.time() - start_time
                print(f"Done ({elapsed:.1f}s, {len(response)} chars)")

                result = {
                    "teil": teil_key,
                    "teil_name": teil_name,
                    "kategorie": kategorie,
                    "model": model,
                    "test_id": test_id,
                    "test_title": test_title,
                    "rep": rep,
                    "response": response,
                    "elapsed_seconds": round(elapsed, 1),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }

                with open(RESULTS_FILE, "a", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(f"\n=== {teil_key} complete! {total_calls} results saved to {RESULTS_FILE} ===")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 diplomarbeit_runner.py <teil_key>")
        print("Example: python3 diplomarbeit_runner.py teil2")
        sys.exit(1)

    teil_key = sys.argv[1]
    process_teil(teil_key)
