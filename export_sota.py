import pandas as pd
import json
import argparse

"""
SOTA Interoperability Tool: Jailbreak Taxonomy -> HarmBench/JailbreakBench
Version: 1.0.0 (Interoperability Module)

This script exports our proprietary 10-category data into standardized 
JSON formats used by industrial evaluation engines.
"""

def export_to_harmbench(input_file, output_file):
    print(f"[*] Reading taxonomy data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"[!] Error: {e}")
        return

    # Transformation to HarmBench-style Behavior Mapping
    harmbench_data = []
    for _, row in df.iterrows():
        harmbench_data.append({
            "BehaviorID": f"TAX-{row['category']}-{_}",
            "Behavior": row['prompt_pattern'],
            "Category": row['category'],
            "Context": "Adversarial Robustness Testing",
            "ModelContext": row['model_id']
        })

    with open(output_file, 'w') as f:
        json.dump(harmbench_data, f, indent=4)
    
    print(f"[+] SOTA Export Complete: {len(harmbench_data)} patterns exported to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Taxonomy to SOTA Benchmarking Formats")
    parser.add_argument("--input", default="data/prompt_patterns.csv", help="Dataset input file")
    parser.add_argument("--output", default="data/results/harmbench_compatible.json", help="Output JSON path")
    
    # Using the prompt patterns for the real export
    export_to_harmbench("data/prompt_patterns.csv", "data/results/harmbench_compatible.json")
