# Excel Portfolio

Professional Excel analytics projects by **RR** (Hyderabad).

This repository is the home for portfolio-ready Excel work: data cleaning, KPI design, dashboards, and business reporting. Every workbook is version-controlled and checked automatically by GitHub Actions.

[![Excel CI](https://github.com/rajaraogurindapalli-gif/excel-portfolio/actions/workflows/excel-ci.yml/badge.svg)](https://github.com/rajaraogurindapalli-gif/excel-portfolio/actions/workflows/excel-ci.yml)

## Why CI/CD on Excel?

Excel files are binary. Without automation they silently break, grow stale, or become hard to review. This repo treats workbooks like products:

- **Validate** every `.xlsx` on push and pull request (openable, has sheets, has data).
- **Inventory** sheets, row counts, and column headers as a CI artifact.
- **Fail fast** if a workbook is corrupt or empty.
- **Ready to extend** with dashboard export, data-quality rules, and GitHub Pages later.

## Repository layout

```text
excel-portfolio/
├── .github/workflows/excel-ci.yml   # GitHub Actions pipeline
├── scripts/validate_workbooks.py    # CI validation script
├── projects/                       # One folder per Excel project
├── requirements.txt
├── .gitattributes                  # Treat Excel as binary
└── README.md
```

## Projects

| # | Project | Status | Skills |
|---|---------|--------|--------|
| 01 | *Coming next* | Planned | Power Query, PivotTables, KPIs, dashboards |

Each project folder will contain:

- the workbook (`.xlsx`)
- a short `README.md` (objective, dataset, insights, screenshots)
- optional raw/sample data

## CI pipeline

Workflow: `.github/workflows/excel-ci.yml`

**Triggers:** push to `main`, pull requests, and manual `workflow_dispatch`.

**Job:** `validate-excel`

1. Check out the repo
2. Set up Python 3.12
3. Install `openpyxl` and `pandas`
4. Run `scripts/validate_workbooks.py`
5. Upload `workbook-inventory.json` as an artifact

The validator currently checks:

- file is a readable Excel workbook
- at least one visible worksheet exists
- at least one sheet has a header row and data (or the project is still empty — that is allowed until the first workbook lands)

## Local validation

```bash
python -m pip install -r requirements.txt
python scripts/validate_workbooks.py
```

## Git notes for Excel

- `.xlsx` / `.xlsm` are marked **binary** in `.gitattributes` so Git does not try to merge them.
- Prefer one project per folder and descriptive commit messages (`feat: add sales KPI dashboard`).
- Large source dumps belong in `projects/<name>/data/`, not the repo root.

## About

Built as a public portfolio track: Excel first, then SQL, Python, and Power BI projects in the same professional pattern (clean repo + CI + write-up).
