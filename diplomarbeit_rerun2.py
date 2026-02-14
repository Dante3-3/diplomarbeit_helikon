#!/usr/bin/env python3
"""
Re-run remaining problematic outputs after removing Final Activation Instruction
from system prompts. Replaces bad entries in results.jsonl.
"""

import json
import os
import time
import subprocess
import tempfile

CONFIG_PATH = "/Users/dstoilovski/Documents/Helikon/diplomarbeit_config.json"
OUTPUT_DIR = "/Users/dstoilovski/Documents/Helikon/diplomarbeit_output"
RESULTS_FILE = os.path.join(OUTPUT_DIR, "results.jsonl")
OLLAMA_URL = "http://localhost:11434/api/chat"

# Remaining failures from first rerun + not-reached deepseek calls
RERUN_LIST = [
    # teil3: gemma2:9b - 6 still failing
    ("teil3", "gemma2:9b", "MC1", 1),
    ("teil3", "gemma2:9b", "MC1", 2),
    ("teil3", "gemma2:9b", "MC1", 3),
    ("teil3", "gemma2:9b", "MC2", 3),
    ("teil3", "gemma2:9b", "MC3", 1),
    ("teil3", "gemma2:9b", "MC3", 3),
    # teil4: gemma2:9b - all 9 still failing
    ("teil4", "gemma2:9b", "SC1", 1),
    ("teil4", "gemma2:9b", "SC1", 2),
    ("teil4", "gemma2:9b", "SC1", 3),
    ("teil4", "gemma2:9b", "SC2", 1),
    ("teil4", "gemma2:9b", "SC2", 2),
    ("teil4", "gemma2:9b", "SC2", 3),
    ("teil4", "gemma2:9b", "SC3", 1),
    ("teil4", "gemma2:9b", "SC3", 2),
    ("teil4", "gemma2:9b", "SC3", 3),
    # teil6: gemma2:9b - all 9 still failing
    ("teil6", "gemma2:9b", "TF1", 1),
    ("teil6", "gemma2:9b", "TF1", 2),
    ("teil6", "gemma2:9b", "TF1", 3),
    ("teil6", "gemma2:9b", "TF2", 1),
    ("teil6", "gemma2:9b", "TF2", 2),
    ("teil6", "gemma2:9b", "TF2", 3),
    ("teil6", "gemma2:9b", "TF3", 1),
    ("teil6", "gemma2:9b", "TF3", 2),
    ("teil6", "gemma2:9b", "TF3", 3),
    # teil7: deepseek-r1:8b - 3 not reached in first run
    ("teil7", "deepseek-r1:8b", "GF2", 1),
    ("teil7", "deepseek-r1:8b", "GF3", 2),
    ("teil7", "deepseek-r1:8b", "GF3", 3),
]


def call_ollama(model, system_prompt, user_prompt):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {"num_ctx": 16384}
    }

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


def is_problematic(response):
    lower = response.lower()[:500]
    indicators = [
        "i am ready to create",
        "please provide",
        "awaiting the user",
        "please share",
        "i'm ready to create",
        "provide the topic",
        "provide me with",
        "i need the following",
        "could you please provide",
        "please give me",
    ]
    return any(ind in lower for ind in indicators)


def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        all_results = [json.loads(line) for line in f if line.strip()]

    print(f"Loaded {len(all_results)} existing results")
    print(f"Re-running {len(RERUN_LIST)} remaining problematic outputs (with cleaned system prompts)...\n")

    replaced = 0
    still_bad = 0

    for idx, (teil_key, model, test_id, rep) in enumerate(RERUN_LIST, 1):
        teil = config["teile"][teil_key]
        system_prompt = teil["system_prompt"]

        user_prompt_data = None
        for up in teil["user_prompts"]:
            if up["id"] == test_id:
                user_prompt_data = up
                break

        if not user_prompt_data:
            print(f"[{idx}/{len(RERUN_LIST)}] WARNING: Could not find prompt {test_id} in {teil_key}")
            continue

        user_prompt = user_prompt_data["prompt"]
        test_title = user_prompt_data["title"]

        print(f"[{idx}/{len(RERUN_LIST)}] {model} | {teil_key}/{test_id} Rep {rep} ... ", end="", flush=True)

        start_time = time.time()
        response = call_ollama(model, system_prompt, user_prompt)
        elapsed = time.time() - start_time

        if is_problematic(response):
            print(f"STILL BAD ({elapsed:.1f}s) - retrying...", end="", flush=True)
            start_time = time.time()
            response = call_ollama(model, system_prompt, user_prompt)
            elapsed = time.time() - start_time
            if is_problematic(response):
                print(f"STILL BAD after retry ({elapsed:.1f}s)")
                still_bad += 1
                continue

        print(f"OK ({elapsed:.1f}s, {len(response)} chars)")

        found = False
        for i, r in enumerate(all_results):
            if (r["teil"] == teil_key and r["model"] == model and
                    r["test_id"] == test_id and r["rep"] == rep):
                all_results[i]["response"] = response
                all_results[i]["elapsed_seconds"] = round(elapsed, 1)
                all_results[i]["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
                found = True
                replaced += 1
                break

        if not found:
            print(f"  WARNING: Could not find matching entry to replace!")

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        for r in all_results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n=== RERUN 2 COMPLETE ===")
    print(f"Replaced: {replaced}/{len(RERUN_LIST)}")
    if still_bad > 0:
        print(f"Still problematic after retry: {still_bad}")
    print(f"Updated: {RESULTS_FILE}")


if __name__ == "__main__":
    main()
