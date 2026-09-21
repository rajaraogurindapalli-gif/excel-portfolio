#!/usr/bin/env python3
"""Validate Excel workbooks in this portfolio repository.

Checks every .xlsx / .xlsm under projects/ (and repo root as a fallback):
- file opens with openpyxl
- at least one visible sheet
- reports sheet names, dimensions, and header row

Exits 0 when there are no workbooks yet (scaffold mode).
Exits 1 if any workbook is corrupt or completely empty.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
SEARCH_DIRS = [ROOT / "projects", ROOT]
EXTS = {".xlsx", ".xlsm"}
SKIP_PREFIX = "~$"


def find_workbooks() -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()
    for folder in SEARCH_DIRS:
        if not folder.exists():
            continue
        for path in folder.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in EXTS:
                continue
            if path.name.startswith(SKIP_PREFIX):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            found.append(path)
    return sorted(found)


def inspect_workbook(path: Path) -> dict:
    wb = load_workbook(path, read_only=True, data_only=True)
    sheets = []
    visible_with_data = 0
    try:
        for ws in wb.worksheets:
            state = getattr(ws, "sheet_state", "visible")
            max_row = ws.max_row or 0
            max_col = ws.max_column or 0
            headers: list[str] = []
            if max_row >= 1 and max_col >= 1:
                first = next(ws.iter_rows(min_row=1, max_row=1, values_only=True), ())
                headers = [str(c) if c is not None else "" for c in first]
            has_data = max_row >= 2 and max_col >= 1
            if state == "visible" and has_data:
                visible_with_data += 1
            sheets.append(
                {
                    "name": ws.title,
                    "state": state,
                    "max_row": max_row,
                    "max_col": max_col,
                    "headers": headers[:20],
                    "has_data": has_data,
                }
            )
    finally:
        wb.close()

    rel = path.relative_to(ROOT).as_posix()
    return {
        "path": rel,
        "sheets": sheets,
        "sheet_count": len(sheets),
        "visible_sheets_with_data": visible_with_data,
        "ok": len(sheets) > 0,
    }


def main() -> int:
    workbooks = find_workbooks()
    inventory = {
        "workbook_count": len(workbooks),
        "workbooks": [],
        "errors": [],
    }

    if not workbooks:
        print("No Excel workbooks found yet. CI scaffold is healthy.")
        Path("workbook-inventory.json").write_text(
            json.dumps(inventory, indent=2), encoding="utf-8"
        )
        return 0

    failed = False
    for path in workbooks:
        print(f"Checking {path.relative_to(ROOT).as_posix()} ...")
        try:
            info = inspect_workbook(path)
        except Exception as exc:  # noqa: BLE001 — surface any openpyxl failure
            failed = True
            msg = f"{path.relative_to(ROOT).as_posix()}: failed to open ({exc})"
            print(f"  ERROR {msg}")
            inventory["errors"].append(msg)
            continue

        inventory["workbooks"].append(info)
        if not info["ok"]:
            failed = True
            msg = f"{info['path']}: no worksheets"
            print(f"  ERROR {msg}")
            inventory["errors"].append(msg)
            continue

        print(
            f"  OK  {info['sheet_count']} sheet(s), "
            f"{info['visible_sheets_with_data']} with data"
        )
        for sheet in info["sheets"]:
            print(
                f"      - {sheet['name']} "
                f"({sheet['state']}, {sheet['max_row']}x{sheet['max_col']})"
            )

        if info["visible_sheets_with_data"] == 0:
            failed = True
            msg = f"{info['path']}: workbook has no visible sheet with data rows"
            print(f"  ERROR {msg}")
            inventory["errors"].append(msg)

    Path("workbook-inventory.json").write_text(
        json.dumps(inventory, indent=2), encoding="utf-8"
    )

    if failed:
        print("\nValidation failed.")
        return 1

    print(f"\nValidation passed for {len(workbooks)} workbook(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
