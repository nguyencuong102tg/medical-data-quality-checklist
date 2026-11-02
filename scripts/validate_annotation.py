#!/usr/bin/env python3
"""Validate a small medical annotation review CSV.

This public demo script checks structure and basic review hygiene.
It does not access patient data or private datasets.

Usage:
    python validate_annotation.py examples/annotation_sample.csv
"""
import argparse
import csv
import sys
from collections import Counter

REQUIRED_COLUMNS = [
    "id",
    "status",
    "note",
    "issue_type",
    "severity",
]

ALLOWED_STATUS = {
    "Accept",
    "Accept with minor note",
    "Reject",
    "Escalate",
}

ALLOWED_SEVERITY = {
    "",
    "Low",
    "Medium",
    "High",
}

ALLOWED_ISSUE_TYPE = {
    "",
    "none",
    "format",
    "language_quality",
    "terminology",
    "factual_accuracy",
    "ambiguity",
    "duplicate",
    "safety",
    "units",
    "missing_context",
}


def normalize(value):
    return (value or "").strip()


def validate(rows, line_start=2):
    errors = []
    ids = Counter()

    for line_no, row in enumerate(rows, start=line_start):
        row_id = normalize(row.get("id"))
        status = normalize(row.get("status"))
        note = normalize(row.get("note"))
        issue_type = normalize(row.get("issue_type"))
        severity = normalize(row.get("severity"))

        if not row_id:
            errors.append(f"Line {line_no}: `id` must not be empty.")
        else:
            ids[row_id] += 1

        if status not in ALLOWED_STATUS:
            errors.append(f"Line {line_no}: invalid status {status!r}.")

        if severity not in ALLOWED_SEVERITY:
            errors.append(f"Line {line_no}: invalid severity {severity!r}.")

        if issue_type and issue_type not in ALLOWED_ISSUE_TYPE:
            errors.append(f"Line {line_no}: invalid issue_type {issue_type!r}.")

        if status and status != "Accept" and not note:
            errors.append(f"Line {line_no}: non-Accept rows must have a note.")

    for row_id, count in ids.items():
        if row_id and count > 1:
            errors.append(f"Duplicate id {row_id!r}: found {count} times.")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--max-errors", type=int, default=30)
    args = parser.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [col for col in REQUIRED_COLUMNS if col not in (reader.fieldnames or [])]
        if missing:
            print("ERROR: missing required columns: " + ", ".join(missing))
            return 2
        rows = list(reader)

    errors = validate(rows)
    print(f"Checked {len(rows)} rows.")
    if errors:
        for err in errors[:args.max_errors]:
            print("ERROR:", err)
        return 1

    print("PASS: no issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
