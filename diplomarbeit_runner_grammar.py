#!/usr/bin/env python3
"""
Grammar-Split Runner: Re-runs only the split grammar teile (5a, 5b, 5c)
based on Sprague's feedback to separate exercise types into individual prompts.
Results go to diplomarbeit_output/results_grammar_split.jsonl
"""

import json
import subprocess
import tempfile
import os
import time
from datetime import datetime

CONFIG_FILE = "diplomarbeit_config_grammar.json"
RESULTS_FILE = "diplomarbeit_output/results_grammar_split.jsonl"
OLLAMA_URL = "http://localhost:11434/api/chat"
TIMEOUT = 900

def call_ollama(model, system_prompt, user_prompt):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ],
        "stream": False,
        "options": {"num_ctx": 16384}
    }
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
        json.dump(payload, tmp, ensure_ascii=False)
        tmp_path = tmp.name

    try:
        start = time.time()
        proc = subprocess.run(
            ["curl", "-s", "--max-time", str(TIMEOUT),
             "-H", "Content-Type: application/json",
             "-d", f"@{tmp_path}", OLLAMA_URL],
            capture_output=True, text=True, timeout=TIMEOUT + 20
        )
        elapsed = time.time() - start

        if proc.returncode != 0:
            return None, elapsed, f"[ERROR] curl failed (exit {proc.returncode})"

        result = json.loads(proc.stdout)
        content = result.get("message", {}).get("content", "")
        return content, elapsed, None
    except subprocess.TimeoutExpired:
        return None, TIMEOUT, "[ERROR] timeout"
    except Exception as e:
        return None, 0, f"[ERROR] {e}"
    finally:
        os.unlink(tmp_path)

def is_problematic(response):
    if not response:
        return True
    lower = response.lower()[:500]
    indicators = [
        "i am ready to create", "please provide", "awaiting the user",
        "please share", "i'm ready to create", "provide the topic",
        "provide me with", "i need the following",
    ]
    return any(ind in lower for ind in indicators)

def load_existing(path):
    existing = set()
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                try:
                    r = json.loads(line)
                    existing.add((r['teil'], r['model'], r['test_id'], r['rep']))
                except:
                    pass
    return existing

def main():
    with open(CONFIG_FILE, encoding='utf-8') as f:
        config = json.load(f)

    os.makedirs("diplomarbeit_output", exist_ok=True)
    existing = load_existing(RESULTS_FILE)

    models = config["models"]
    reps   = config["repetitions"]
    teile  = config["teile"]

    total = sum(len(t["user_prompts"]) for t in teile.values()) * len(models) * reps
    done = 0
    skipped = 0

    print(f"Grammar-Split Run: {total} total calls ({len(teile)} teile × {len(models)} models × 3 prompts × {reps} reps)")
    print(f"Already completed: {len(existing)}\n")

    with open(RESULTS_FILE, "a", encoding='utf-8') as out:
        for teil_key, teil in teile.items():
            sys_prompt = teil["system_prompt"]
            for model in models:
                for prompt in teil["user_prompts"]:
                    for rep in range(1, reps + 1):
                        key = (teil_key, model, prompt["id"], rep)
                        if key in existing:
                            skipped += 1
                            continue

                        done += 1
                        total_done = done + skipped
                        print(f"[{total_done}/{total}] {teil_key} | {model} | {prompt['id']} | rep {rep}")

                        response, elapsed, error = call_ollama(model, sys_prompt, prompt["prompt"])

                        if error or is_problematic(response):
                            status = error or "PROBLEMATIC"
                            response = response or status
                            print(f"  !! {status} ({elapsed:.1f}s)")
                        else:
                            print(f"  OK {elapsed:.1f}s | {len(response)} chars")

                        record = {
                            "teil": teil_key,
                            "teil_name": teil["name"],
                            "kategorie": teil["kategorie"],
                            "model": model,
                            "test_id": prompt["id"],
                            "test_title": prompt["title"],
                            "rep": rep,
                            "response": response,
                            "elapsed_seconds": round(elapsed, 2),
                            "timestamp": datetime.now().isoformat()
                        }
                        out.write(json.dumps(record, ensure_ascii=False) + "\n")
                        out.flush()

    total_written = done
    print(f"\nDone. {total_written} new results written to {RESULTS_FILE}")
    print(f"Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
