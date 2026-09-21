# Excel Portfolio

Professional Excel analytics projects by **RR** (Hyderabad).

Current focus: NASA C-MAPSS turbofan engine degradation — analytics dashboard, VBA automation, and a natural-language query agent. Every workbook is version-controlled and checked by GitHub Actions.

[![Excel CI](https://github.com/rajaraogurindapalli-gif/excel-portfolio/actions/workflows/excel-ci.yml/badge.svg)](https://github.com/rajaraogurindapalli-gif/excel-portfolio/actions/workflows/excel-ci.yml)

## Project 01 — CMAPSS Engine Health

Source: [CMAPSS Jet Engine Simulated Data](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data) (`CMAPSSData.zip`).

Four fleets (FD001–FD004) of run-to-failure and truncated test trajectories, 26 columns per cycle (unit, cycle, 3 operating settings, 21 sensors), plus true Remaining Useful Life (RUL) for test engines.

| Layer | What we will build |
|---|---|
| Analytics dashboard | Fleet KPIs, degradation trends, RUL risk, sensor heatmaps |
| VBA automation | Import/clean NASA txt files, refresh pivots, flag critical engines, export reports |
| NL agent | Ask questions in English against the workbook (engine status, RUL, sensors) |

Question catalogue: `projects/01-cmapss-engine-health/QUESTIONS.md`

## Repository layout

```text
excel-portfolio/
├── .github/workflows/excel-ci.yml
├── scripts/validate_workbooks.py
├── projects/01-cmapss-engine-health/
├── requirements.txt
└── README.md
```
