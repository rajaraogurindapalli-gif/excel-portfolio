# Build guide — CMAPSS Engine Health (v1)

Approved question set: `QUESTIONS.md`.
Audience: HAL airworthiness / ONGC reliability desk.
Repo: `rajaraogurindapalli-gif/excel-portfolio`.

Work one phase. Do not skip the gate at the end of a phase.

## Split of work

| Who | Does |
|---|---|
| You (Windows laptop + desktop Excel) | Enable macros, import `.bas`, click buttons, take screenshots, commit |
| Grok | Workbook skeleton, data model, dashboard layout, VBA source, agent rules, GitHub files |
| GitHub Actions | Validates every `.xlsx` / `.xlsm` on push |

Excel Online cannot run this project. Use desktop Excel (Microsoft 365 or 2021+).

---

## Phase 0 — Desk and repo (30 min)

0.1 Open [excel-portfolio](https://github.com/rajaraogurindapalli-gif/excel-portfolio). Confirm Actions is green.
0.2 On the laptop install Git if missing, then:

```bat
cd %USERPROFILE%\Documents
git clone https://github.com/rajaraogurindapalli-gif/excel-portfolio.git
cd excel-portfolio
```

0.3 Create the project folders (if not already present):

```text
projects/01-cmapss-engine-health/
  data/raw/          NASA txt files (not the full zip if > GitHub comfort; FD001 is enough for v1)
  data/work/         csv extracts used by Excel
  vba/               .bas modules
  screenshots/
  CMAPSS_Engine_Health.xlsm
  QUESTIONS.md
  BUILD_GUIDE.md
  README.md
```

0.4 Download [CMAPSSData.zip](https://data.nasa.gov/docs/legacy/CMAPSSData.zip). Copy only these into `data/raw/`:

- `train_FD001.txt`
- `test_FD001.txt`
- `RUL_FD001.txt`
- `readme.txt`

Leave FD002–FD004 out of v1 (size + scope).

0.5 In Excel: File → Options → Trust Center → Macro Settings → *Disable all macros with notification* (you will Enable Content once). File → Options → Customize Ribbon → tick **Developer**.

**Gate:** repo cloned, three FD001 files on disk, Developer tab visible.

---

## Phase 1 — Land the data (trust strip)

Answers Q4.1–Q4.3 before any chart exists.

1.1 Convert space-separated NASA files to CSV with headers:

```text
unit, cycle, os1, os2, os3, s1 … s21
```

Plus `split=Train|Test` and, on test last-cycle rows, `true_rul` from `RUL_FD001.txt` (row i = engine i).

1.2 Excel sheets to create:

| Sheet | Purpose | Visible |
|---|---|---|
| `00_Cover` | Title, source, disclaimer (not a release stamp) | Yes |
| `01_Dashboard` | Decision screen | Yes |
| `02_BayQueue` | Ranked shop list | Yes |
| `03_Engine` | One-engine drill | Yes |
| `04_Agent` | Type a question, get an answer | Yes |
| `05_Brief` | 06:00 export page | Yes |
| `10_Train` | Raw train cycles | Very hidden later |
| `11_Test` | Raw test cycles | Very hidden later |
| `12_RUL` | 100 true RUL values | Very hidden later |
| `20_Fleet` | One row per engine (the model) | Hidden |
| `21_HealthyBand` | First-30-cycle mean/std per sensor | Hidden |
| `90_Params` | Band cuts 30 / 100, capacity N, selected engine | Yes |
| `91_Validate` | Row-count pass/fail | Yes |
| `99_AgentMap` | Prompt → named range / procedure | Hidden |

1.3 Validation numbers that must appear on `91_Validate`:

- Train rows = 20631
- Test rows = 13096
- Train units = 100
- Test units = 100
- RUL rows = 100
- Cycles per unit start at 1 and increase by 1

**Gate:** all six checks green. No dashboard work until this gate.

---

## Phase 2 — Fleet model (one row per engine)

Sheet `20_Fleet` is the only table the dashboard reads.

Columns:

```text
engine_id
split                  Train | Test
last_cycle
life_or_observed       train max cycle | test last cycle
true_rul               train: 0 at last cycle; test: from RUL file
rul_capped             MIN(true_rul, 125)
risk_band              Withdraw | Watch | Continue
health_index           0–100 at last cycle
delta_health_20        drop over last 20 cycles (test: as many as exist)
primary_sensor         sensor with largest |z| vs own healthy baseline
shop_week              This Week | Next Week | Monitor
false_safe             Yes if band=Continue and true_rul<30 (test only)
false_alarm            Yes if band=Withdraw and true_rul>100 (test only)
why_flagged            one sentence
```

Band rules (on `90_Params`, blue input cells):

- Withdraw if `true_rul <= 30`
- Watch if `31–100`
- Continue if `> 100`

Health index (v1, simple and explainable):

1. For each live sensor, z = (last − healthy_mean) / healthy_std using that engine’s first 30 cycles when possible, else fleet first-30.
2. Live FD001 sensors: T24, T30, T50, P30, Ps30, Nf, Nc, phi, BPR, htBleed, W31, W32 (and close cousins that actually vary).
3. Dead sensors stay off the index: T2, P2, epr, farB, Nf_dmd, PCNfR_dmd, os3.
4. Health = 100 − clipped mean |z| scaled so typical end-of-life sits near 20–40.

**Gate:** 200 rows (100 train + 100 test), no blank bands, Withdraw count matches `true_rul<=30` on test.

---

## Phase 3 — Dashboard (the decision screen)

`01_Dashboard` layout, top to bottom:

1. Title: CMAPSS FD001 — Fleet airworthiness / reliability view  
   Subtitle: Supports the engineer. Does not replace the stamp.
2. Data-trust strip (green/red from `91_Validate`).
3. KPI cards: engines, cycles, median train life, Withdraw count, worst test RUL.
4. Donut or stacked bar: Continue / Watch / Withdraw (test fleet).
5. Bay queue preview (top 10 from `02_BayQueue`).
6. Selected engine (value on `90_Params!SelectedEngine`): band, RUL, health, primary sensor, why-flagged sentence.
7. Slicer / cell: capacity N (default 5).

`02_BayQueue`: sort test engines by true_rul ASC, then delta_health_20 DESC. First N = This Week, next 8 = Next Week, rest = Monitor.

`03_Engine`: last 60 cycles of selected engine for 4 sensors (T50, Ps30, Nc, W32) vs healthy band.

Colour:

- Withdraw = dark red fill
- Watch = amber
- Continue = green
- Inputs on `90_Params` = blue font
- Formulas = black font

**Gate:** a colleague can answer Q1.1–Q1.4 and Q2.1–Q2.2 from `01_Dashboard` without opening hidden sheets.

---

## Phase 4 — VBA automation

Modules to keep as text in `vba/` (versioned) and import via Developer → Visual Basic → File → Import:

| Module | Button on Cover/Dashboard |
|---|---|
| `modImport.bas` | 1. Import NASA files |
| `modModel.bas` | 2. Build fleet model |
| `modRefresh.bas` | 3. Refresh dashboard |
| `modAlerts.bas` | 4. Write Withdraw to Alerts |
| `modBrief.bas` | 5. Export 06:00 brief |
| `modValidate.bas` | 6. Validate import |
| `modAgent.bas` | 7. Answer question |

Rules:

- No `Select` / `Activate` except when writing the Agent answer cell.
- Named ranges for every KPI the agent reads.
- Errors go to `91_Validate`, not MsgBox spam (one summary box is enough).
- Save as `.xlsm`. Never commit `~$` lock files.

Button row on `00_Cover` and repeated small on `01_Dashboard`.

**Gate:** after deleting calculated sheets, buttons 1→6 rebuild a correct Withdraw count from the raw txt files alone.

---

## Phase 5 — Natural-language agent

Not Copilot. A bounded agent that only answers the frozen 12 prompts in `QUESTIONS.md` §6.

How it works:

1. User types in `04_Agent!C5`.
2. VBA lowercases the text, extracts engine id / cycle / capacity with regex.
3. `99_AgentMap` maps intent keywords → procedure.
4. Answer is written to `04_Agent!C8` and, if needed, `SelectedEngine` is set so `03_Engine` follows.
5. Unknown question → one clarifying line, no guess.

Examples that must work after Phase 5:

```text
How many engines are Withdraw right now?
Can engine 17 do 40 more cycles?
Why is engine 8 flagged?
Bay queue this week. Capacity is 5.
Give me the 06:00 brief.
Did the last import pass validation?
```

**Gate:** those six sentences return the same numbers as the dashboard tiles.

---

## Phase 6 — GitHub and CI

6.1 Do not commit the full 45 MB zip. Commit FD001 txt + workbook + vba + screenshots.
6.2 `.gitattributes` already marks `xlsx/xlsm` as binary.
6.3 Push:

```bat
git add projects/01-cmapss-engine-health
git commit -m "feat: CMAPSS FD001 dashboard, VBA, and agent v1"
git push origin main
```

6.4 Open Actions. `Excel CI` must open the `.xlsm` and list sheets. If the file is corrupt, the job fails.

6.5 Add three screenshots to `screenshots/`:

- dashboard with trust strip green
- bay queue
- agent answering “why is engine 8 flagged”

**Gate:** green CI run + README link to the workbook.

---

## Phase 7 — Project README (portfolio write-up)

`projects/01-cmapss-engine-health/README.md` must contain:

- Problem in HAL/ONGC language (continue / watch / withdraw)
- Data source and citation (Saxena et al., PHM08)
- What v1 does and what it refuses to do (no release stamp)
- How to open and enable macros
- Button list
- Agent prompt list
- Screenshot trio
- Limits (FD001 only, simple health index)

**Gate:** someone who was not in this chat can run the file from README alone.

---

## Phase 8 — Acceptance against QUESTIONS.md

Tick on `91_Validate` or a printed checklist:

- [ ] Q1.1–Q1.7 visible
- [ ] Q2.1–Q2.4 visible
- [ ] Q4.1–Q4.3 green/red strip
- [ ] VBA 1–6 rebuild from raw files
- [ ] Agent prompts 1–6 and 10 match tiles
- [ ] Disclaimer on Cover: tool supports the engineer; it does not replace the stamp

When all boxes are ticked, v1 is closed. v2 is FD002–FD004 and a better RUL score — not before.

---

## Suggested calendar

| Session | Phase | Output |
|---|---|---|
| 1 | 0–1 | Validated FD001 in Excel |
| 2 | 2–3 | Dashboard + bay queue |
| 3 | 4 | Working buttons |
| 4 | 5 | Agent on 12 prompts |
| 5 | 6–8 | Push, screenshots, README, accept |

Start session 1 by saying: **start Phase 1** — Grok will generate the CSV extracts and the workbook skeleton next.
