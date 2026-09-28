import argparse
import json
from pathlib import Path
from extract import run, FIELDS, normalize


def evaluate(split="dev", mode="mock"):
    totals = {name: {"correct": 0, "count": 0} for name in FIELDS}
    rows = []
    for case in json.loads(Path("data/gold.json").read_text()):
        if case["split"] != split:
            continue
        record = run(case["file"], mode)
        wrong = []
        for name in FIELDS:
            expected = normalize(name, case["expected"][name])
            correct = record["values"][name] == expected
            totals[name]["count"] += 1
            totals[name]["correct"] += int(correct)
            if not correct:
                wrong.append(name)
        rows.append(
            {
                "file": case["file"],
                "wrong_fields": wrong,
                "needs_review": record["needs_review"],
            }
        )
    for item in totals.values():
        item["accuracy"] = item["correct"] / item["count"]
    return {"mode": mode, "split": split, "fields": totals, "rows": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["dev", "holdout"], default="dev")
    parser.add_argument("--mode", choices=["mock", "live"], default="mock")
    args = parser.parse_args()
    result = evaluate(args.split, args.mode)
    Path("output").mkdir(exist_ok=True)
    Path(f"output/eval-{args.split}-{args.mode}.json").write_text(
        json.dumps(result, indent=2)
    )
    print(json.dumps(result, indent=2))
