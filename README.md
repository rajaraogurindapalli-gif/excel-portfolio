# Excel Portfolio

Professional Excel analytics projects by **RR** (Hyderabad).

[![Excel CI](https://github.com/rajaraogurindapalli-gif/excel-portfolio/actions/workflows/excel-ci.yml/badge.svg)](https://github.com/rajaraogurindapalli-gif/excel-portfolio/actions/workflows/excel-ci.yml)

## Project 01 — CMAPSS Engine Health — COMPLETE

NASA C-MAPSS FD001. Decision dashboard, gated validation, VBA, and a 12-prompt agent.

It supports the engineer. It does not replace an airworthiness or reliability stamp.

| Deliverable | Where |
|---|---|
| Story (data → questions → transform → functions → agent → automation) | [`projects/01-cmapss-engine-health/PROJECT_DOCUMENTATION.md`](projects/01-cmapss-engine-health/PROJECT_DOCUMENTATION.md) |
| Question catalogue | [`projects/01-cmapss-engine-health/QUESTIONS.md`](projects/01-cmapss-engine-health/QUESTIONS.md) |
| Build gates | [`projects/01-cmapss-engine-health/BUILD_GUIDE.md`](projects/01-cmapss-engine-health/BUILD_GUIDE.md) |
| Workbook | Local `CMAPSS_Engine_Health.xlsm` (macros stay on the PC; not required in git) |

Source: [NASA C-MAPSS](https://data.nasa.gov/docs/legacy/CMAPSSData.zip) — Saxena, Goebel, Simon, Eklund, PHM08.

Checked on FD001: trust PASS, 25 / 42 / 33 bands, This Week 34-81-31-68-82, engine 34 NO-GO at RUL 7, engine 1 GO at RUL 112.

## Project 02 — Iowa Liquor Sales (next)

Official 2024 wholesale lines from [data.iowa.gov](https://data.iowa.gov/catalog/dataset/1261). One Board + four interconnected exhibits (describe / diagnose / predict / prescribe). DEV 10% / TEST 50% / PROD 100% stores. Power Query + Power Pivot DAX.

## Layout

```text
excel-portfolio/
├── .github/workflows/excel-ci.yml
├── scripts/validate_workbooks.py
├── projects/01-cmapss-engine-health/
└── README.md
```
