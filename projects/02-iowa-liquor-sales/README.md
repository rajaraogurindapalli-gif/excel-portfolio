# 02 — Iowa Liquor Sales

HBS-style commercial case on official 2024 wholesale lines.
One Board + four interconnected exhibits (describe / diagnose / predict / prescribe).
Power Query environments: DEV 10% stores / TEST 50% / PROD 100%.
Measures in Excel Power Pivot (DAX). VBA later.

## Source (fact table only)

- Portal: https://data.iowa.gov/catalog/dataset/1261
- CSV: https://idh-be.iowa.gov/api/v1/datasets/1261/rows.csv
- Publisher: State of Iowa, Alcohol Operations Bureau
- Coverage: 1 Jan 2024 – 31 Dec 2024 (~2,590,975 rows)
- License: CC BY

Raw CSV and PROD workbook stay on the PC. Do not commit them.

Classification of store-level extracts: INTERNAL.
Wholesale to the store is not consumer sell-out.

## Local layout

```text
02-iowa-liquor-sales/
  data/raw/          iowa_liquor_sales_2024.csv
  data/lists/        store_dev / store_test (Phase 1)
  data/notes/        SOURCE.txt, CLASSIFICATION.txt
  workbooks/         Iowa_Liquor_DEV.xlsm / TEST / PROD
  exports/
```
