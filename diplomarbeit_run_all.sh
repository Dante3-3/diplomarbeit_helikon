#!/bin/bash
echo "=========================================="
echo "DIPLOMARBEIT - Full Test Run Started"
echo "$(date)"
echo "=========================================="

cd /Users/dstoilovski/Documents/Helikon

for teil in teil2 teil3 teil4 teil5 teil6 teil7 teil8; do
    echo ""
    echo ">>> Starting $teil at $(date)"
    python3 diplomarbeit_runner.py $teil
    
    echo ">>> Evaluating $teil with Copilot at $(date)"
    python3 diplomarbeit_evaluator.py --teil $teil
    
    echo ">>> $teil COMPLETE at $(date)"
    echo ""
done

echo "=========================================="
echo "ALL DONE at $(date)"
echo "Results: diplomarbeit_output/results.jsonl"
echo "Report: diplomarbeit_output/diplomarbeit_report.md"
lines=$(wc -l < diplomarbeit_output/results.jsonl)
echo "Total outputs: $lines"
echo "=========================================="
