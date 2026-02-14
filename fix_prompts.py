#!/usr/bin/env python3
"""Remove 'Final Activation Instruction' blocks from system prompts in config."""
import json
import re

CONFIG_PATH = "/Users/dstoilovski/Documents/Helikon/diplomarbeit_config.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

for teil_key, teil in config["teile"].items():
    sp = teil["system_prompt"]
    # Remove everything from "Final Activation Instruction" to the end
    # Pattern: **Final Activation Instruction:**\n... to the end
    patterns = [
        r'\n*---\n\*\*Final Activation Instruction[:\*]*\*?\*?\n.*$',
        r'\n*\*\*Final Activation Instruction[:\*]*\*?\*?\n.*$',
        r'\nFinal Activation Instruction.*$',
    ]

    original_len = len(sp)
    for pat in patterns:
        sp = re.sub(pat, '', sp, flags=re.DOTALL)

    # Also remove trailing "Role assignment confirmed" and "Awaiting the user" if still present
    sp = re.sub(r'\nRole assignment confirmed\.?\n?.*$', '', sp, flags=re.DOTALL)
    sp = re.sub(r'\nAwaiting the user.*$', '', sp, flags=re.DOTALL)

    sp = sp.rstrip()

    if len(sp) != original_len:
        print(f"{teil_key}: trimmed {original_len - len(sp)} chars from system prompt")
        teil["system_prompt"] = sp
    else:
        print(f"{teil_key}: no changes needed")

with open(CONFIG_PATH, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("\nConfig updated!")
