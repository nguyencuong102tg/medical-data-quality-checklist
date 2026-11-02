# Medical Data Quality Checklist

This repository contains **clean, public templates** for reviewing medical data, MCQs, annotations, and health-related content quality.

These examples are for portfolio demonstration and workflow improvement. They do not contain patient data, proprietary datasets, or confidential project information.

## Contents
- `checklists/annotation_qa_checklist.md`
- `checklists/mcq_review_checklist.md`
- `templates/mcq_review_template.md`
- `templates/data_issue_report_template.md`
- `examples/synthetic_review_example.md`

## Runnable validator demo

A small Python script validates annotation review CSV rows for required status, duplicate IDs, missing notes, and allowed issue labels.

```bash
python scripts/validate_annotation.py examples/annotation_sample_valid.csv
python scripts/validate_annotation.py examples/annotation_sample_with_issues.csv
```

The first command should pass; the second intentionally shows validation errors.

## Suggested use
- Standardize review language.
- Catch common medical data issues: ambiguous answers, wrong units, unsupported claims, duplicated questions, unsafe advice.
- Produce short written justifications for evaluation work.
