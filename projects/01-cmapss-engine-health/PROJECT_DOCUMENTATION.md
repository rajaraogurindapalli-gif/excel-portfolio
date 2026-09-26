# CMAPSS Engine Health — Project Documentation

**Workbook:** `CMAPSS_Engine_Health.xlsm`  
**Set:** NASA C-MAPSS FD001  
**Owner lens:** HAL airworthiness + ONGC rotating-equipment reliability  
**Status:** Phase 1–5 complete (dashboard, VBA, bounded agent)  
**Rule:** This file supports the engineer. It does not replace an airworthiness or reliability stamp.

---

## 1. What the data is

NASA C-MAPSS (Commercial Modular Aero-Propulsion System Simulation) is a public turbofan degradation set from Saxena, Goebel, Simon and Eklund (PHM08, 2008).

Official archive: https://data.nasa.gov/docs/legacy/CMAPSSData.zip

We locked **v1 to FD001 only**:

| File | Role | Size we validated |
|---|---|---|
| `train_FD001.txt` | 100 engines run **to failure** | 20,631 cycle rows |
| `test_FD001.txt` | 100 engines **stopped before failure** | 13,096 cycle rows |
| `RUL_FD001.txt` | True remaining useful life at the last test snapshot | 100 rows (one per test engine) |
| `readme.txt` | Column and experiment description | reference |

Each cycle row has:

- `unit` — engine id 1–100  
- `cycle` — running cycle, starts at 1, no gaps  
- `os1, os2, os3` — operating settings (FD001 is one condition; almost constant)  
- `s1`–`s21` — sensors (gas-path temperatures, pressures, spool speeds, bleeds)

**HAL reading:** serial / tail asset, flight cycles, HPC / LPT temperatures, delivery pressure, spool speeds.  
**ONGC reading:** tag number of a GT / compressor train, discrete fired-hour analogue, TTX / CDP / speed / bleed.

FD001 is one fault mode (HPC degradation) and one operating condition. It is a **controlled laboratory fleet**, not a shop-floor download. We treat it as a decision exercise, not as a certificate.

Sensors that do not move on FD001 (held off the gauges): `s1, s5, s10, s16, s18, s19`, and `os3`. Live sensors used in the health index: `s2, s3, s4, s7, s8, s9, s11, s12, s13, s14, s15, s17, s20, s21` (T24, T30, T50, P30, Nf, Nc, Ps30, phi, NRf, NRc, BPR, htBleed, W31, W32).

---

## 2. Questions to be answered

The file is built to answer **decision questions**, not chart decoration.

### Duty call

- Which test engines are **Withdraw / Watch / Continue** at the last snapshot?  
- Can engine *N* be cleared for **40 more cycles**?  
- Who occupies the **This Week** bay (capacity 5) and **Next Week** bay (capacity 8)?

### Trust

- Did we import the official FD001 counts (20,631 / 13,096 / 100)?  
- Does every engine run cycles 1, 2, 3… with no skip?  
- Are false-safe and false-alarm on the health index zero on this snapshot?

### Degradation

- What is the fleet healthy band (train, cycles 1–30)?  
- Which live sensor is furthest from that band at the last cycle?  
- How far did health fall over the last 20 cycles?

### Brief

- What does the planner need at 06:00: counts, worst RUL, This Week list, disclaimer?

Default band cuts (yellow cells on `90_Params`):

- **Withdraw:** true RUL ≤ 30  
- **Watch:** 31–100  
- **Continue:** > 100  

On the FD001 test labels that split is **25 / 42 / 33**. Worst test RUL is **7** (engine **34**). Train median run-to-failure life is **199** cycles.

---

## 3. How we handled raw data

1. Downloaded the NASA zip. Used only FD001.  
2. Confirmed four files and sizes before any chart.  
3. Loaded space-separated text with a fixed header:

   `split, unit, cycle, os1, os2, os3, s1 … s21`

4. Landed full tables on `10_Train`, `11_Test`, `12_RUL`. No sampling, no silent row drop.  
5. **Phase 1 gate** (`91_Validate`) compares Excel counts to NASA spec using formulas, not pasted numbers:

   - `COUNTA` of cycle rows vs 20,631 and 13,096  
   - `MAX` / `MIN` of unit id vs 100 and 1  
   - `MIN` of cycle vs 1  
   - cycle-gap pre-check = 0  

6. Work stops if `91_Validate!C20` is not **PASS**.

We did not “clean” NASA values. Outliers are degradation. Dead sensors are documented on `99_Notes` and excluded from the index, not deleted from the raw sheets.

---

## 4. How raw data became the dashboard

Pipeline (one way, left to right):

```
raw .txt
    → 10_Train / 11_Test / 12_RUL          (Phase 1 land + validate)
    → 21_HealthyBand                       (train cycles 1–30 mean and std)
    → 20_Fleet                             (one row per engine)
    → 02_BayQueue                          (test fleet ranked by RUL, then health)
    → 01_Dashboard / 03_Engine / 05_Brief  (decision views)
    → 04_Agent + VBA                       (questions + buttons)
```

### Fleet row (`20_Fleet`, 200 rows)

For each engine we keep the **last cycle** and the cycle **20 steps earlier** (or the first cycle if the engine is shorter than 20). Those snapshots are observations. Everything a planner reads is then a **formula**:

| Column | Rule |
|---|---|
| `true_rul` | Train = 0 at failure. Test = `VLOOKUP` into `12_RUL` |
| `rul_capped` | `MIN(true_rul, RULCap)` with cap 125 |
| `truth_band` | `IF` RUL ≤ Withdraw → Withdraw; ≤ Watch → Watch; else Continue |
| `mean_abs_z` | Mean of `ABS((last_s − Mean_s) / Std_s)` over 14 live sensors |
| `health_index` | `MAX(0, MIN(100, 100 − HealthScale × mean_abs_z))` with scale 20 |
| `delta_health_20` | health 20 cycles ago − health now (drop is positive) |
| `model_band` | health ≤ 50 Withdraw; < 70 Watch; else Continue |
| `rul_rank_test` | Test engines only: lower RUL first, then lower health |
| `shop_week` | Rank ≤ 5 This Week; ≤ 13 Next Week; else Monitor |
| `false_safe` | Model Continue **and** true RUL ≤ 30 |
| `false_alarm` | Model Withdraw **and** true RUL > 100 |
| `why_flagged` | One sentence: engine, band, RUL, model, health, primary sensor |

Primary sensor is the live channel with the largest |z| at last cycle.

### Dashboard

`01_Dashboard` does not store a second copy of the fleet. It **points** at the queue and the gates:

- Trust strip = `91_Validate!C20` and `22_Phase2Gate!C16`  
- Withdraw / Watch / Continue = `COUNTIF` on `02_BayQueue`  
- Selected engine = `INDEX/MATCH` on the queue using `SelectedEngine` (`90_Params` C14)  
- 40-cycle GO / NO-GO = `IF(true_rul >= 40, GO, NO-GO)`  
- Top 10 = first ten rows of the queue  

Change a yellow parameter (Withdraw cut, capacity, selected engine) and the calls move. That is the point of the model.

---

## 5. Logical and math functions we used

### Excel — math and aggregation

| Function | Where | Why |
|---|---|---|
| `COUNTA` | Validate | Row counts vs NASA spec |
| `MAX`, `MIN` | Validate, helpers | Unit range, first cycle, worst RUL |
| `MEDIAN` | Helpers / dashboard | Train life 199 |
| `SUMIFS` | Engine drill, train life helper | Last-cycle sensor for one test engine |
| `COUNTIF` / `COUNTIFS` | Dashboard, queue, ranks | Band counts, This Week slots, rank |
| `AVERAGE` (via mean |z|) | Fleet | Health index ingredients |
| `ABS` | Fleet, engine drill | Distance from healthy band |
| `MIN` (cap) | Fleet | Piecewise RUL cap 125 |
| `MAX` / `MIN` clip | Fleet | Health bounded 0–100 |
| `PERCENTILE` | Helper | Optional tail of test RUL |

Health index, written out:

    z_s = (x_s_last - mu_s_healthy) / sigma_s_healthy
    mean_abs_z = average of |z_s| over 14 live sensors
    H = clip(100 - 20 * mean_abs_z, 0, 100)

Healthy mean and std come from **train cycles 1–30**, fleet-wide (`21_HealthyBand`).

### Excel — logic and lookup

| Function | Where | Why |
|---|---|---|
| `IF` / nested `IF` | Bands, shop week, GO/NO-GO, validate PASS/FAIL | Decision tree |
| `AND` | False-safe / false-alarm | Two conditions at once |
| `IFERROR` | Dashboard lookups | Missing engine id fails soft |
| `VLOOKUP` | Test RUL onto fleet | One key, exact match |
| `INDEX` + `MATCH` | Queue → dashboard / agent views | Rank-k engine, selected engine |
| `ISNUMBER` | Phase 3 gate | Selected RUL must be numeric |
| Named ranges | `Band_Withdraw`, `HealthScale`, `SelectedEngine`, `Mean_s4`, … | Parameters stay visible and blue |

### Conditional format (not calculation, but part of the call)

Withdraw / This Week = red wash. Watch / Next Week = amber. Continue / Monitor = green. PASS / FAIL on the gate sheets.

### VBA — automation functions

| Routine | Job |
|---|---|
| `RunGates` | Recalculate; read P1/P2/P3; message PASS or hold |
| `RefreshDashboard` | Calculate decision sheets; jump to `01_Dashboard!B2` |
| `ExportBrief` | Write `CMAPSS_Brief_yyyymmdd_hhnn.txt` next to the workbook |
| `GoSelectedEngine` | Open `03_Engine` for `SelectedEngine` |
| `SetupAgent` | Create `04_Agent` and the 12-prompt list |
| `AnswerAgent` | Parse C5; write C7; show the same text in a box |

VBA does **not** invent RUL. It reads cells the formulas already computed.

---

## 6. Why an agent is required

A duty engineer will not filter `20_Fleet` at 06:00. They will ask:

- Which engines must not run tomorrow?  
- Can 34 do 40 more cycles?  
- What is trust?

Without an agent those answers exist, but they are scattered across Validate, Queue, Dashboard, and Params. The agent is a **narrow window onto the same numbers**.

It is required because:

1. The questions are known and finite (we froze 12).  
2. The answers must be **traceable** to a cell, not to a chat model.  
3. A general LLM can hallucinate an RUL. This agent cannot: if the queue says 7, it says 7.  
4. HAL / ONGC reviews need a sentence that still carries the disclaimer.

It is **not** a replacement for the dashboard, the bay list, or the stamp.

---

## 7. How we built the agent

Bounded pattern matcher in VBA. No API, no internet, no weights.

1. Sheet `04_Agent`: question in **C5**, answer in **C7**, catalogue of 12 prompts on the left.  
2. Button **ANSWER** calls `AnswerAgent`.  
3. The text is lower-cased. If the line contains `engine`, the number **after that word** is the asset id (so a leading `3.` in “3. Can engine 34…” is ignored after the parser fix).  
4. Keywords pick a branch:

| Prompt idea | Branch |
|---|---|
| must not run / This Week | List queue rows where shop week = This Week |
| Next Week | Same for Next Week |
| 40 more cycles + engine N | RUL ≥ 40 → GO, else NO-GO |
| false-safe | `22_Phase2Gate!C13` |
| median train life | Dashboard D8 |
| worst RUL | Dashboard L8 + queue C6 |
| why flagged / primary sensor | Queue columns for that engine |
| how many Continue Watch Withdraw | Dashboard F8 / H8 / J8 |
| capacity | Params C12 / C13 |
| trust | Validate C20, Phase 2 C16, Phase 3 C14 |
| anything else | “Not in the frozen list” |

5. Every answer appends: *This is a planning aid, not a release stamp.*

Worked checks on FD001:

| Question | Answer |
|---|---|
| Which engines must not run tomorrow? | 34 (7), 81 (8), 31 (8), 68 (8), 82 (9) |
| Can engine 34 do 40 more cycles? | NO-GO, 7 cycles |
| Can engine 1 do 40 more cycles? | GO, 112 cycles |
| What is trust status? | PASS / PASS / PASS |

---

## 8. How automation was completed

Automation here means **repeatable operations on a trusted workbook**, not a black-box pipeline.

### What is automated

- Recalculate all decision sheets  
- Jump back to the dashboard title (avoids scrolling into empty columns)  
- Export the 06:00 brief to a timestamped text file  
- Read the three gates in one box  
- Answer the 12 prompts  

Cover buttons:

| Button | Macro |
|---|---|
| RUN GATES | `RunGates` |
| REFRESH DASHBOARD | `RefreshDashboard` |
| EXPORT 06:00 BRIEF | `ExportBrief` |

Agent button: **ANSWER** → `AnswerAgent`.

### What is not automated (on purpose)

- Re-import of NASA text (v1 data is landed and gated once)  
- Changing Withdraw / Watch cuts (the engineer edits yellow cells)  
- Signing an engine as airworthy  

### How to run the finished file

1. Open `CMAPSS_Engine_Health.xlsm` in desktop Excel.  
2. Enable Content.  
3. Cover → **RUN GATES**. All three must PASS.  
4. Open `01_Dashboard`. Change `90_Params` C14 to walk engines.  
5. Cover → **EXPORT 06:00 BRIEF** if a text copy is needed.  
6. `04_Agent` C5 → **ANSWER**.

Trust Center may stay on **Disable VBA macros with notification**. This workbook is local.

---

## 9. Limits (write these on any resume line)

- FD001 only: one condition, one fault mode.  
- Truth band uses NASA **true RUL**. The health index is an independent check, not a certified remaining-life model.  
- Healthy band is fleet-wide first-30, not each engine’s own baseline.  
- Agent understands 12 phrasings, not free English.  
- False-safe / false-alarm were 0 on this snapshot; that is a result, not a guarantee.

---

## 10. Sheet map

| Sheet | Phase | Role |
|---|---|---|
| 00_Cover | 0–5 | Title, disclaimer, buttons |
| 91_Validate | 1 | Import gate |
| 10_Train / 11_Test / 12_RUL | 1 | Raw land |
| 21_HealthyBand | 2 | μ, σ for 14 sensors |
| 20_Fleet | 2 | 200-row model |
| 02_BayQueue | 2 | Ranked test list |
| 22 / 24 gates | 2–3 | Model and dashboard gates |
| 01_Dashboard | 3 | Decision view |
| 03_Engine | 3 | Sensor drill |
| 05_Brief | 3 | 06:00 page |
| 04_Agent | 5 | Frozen prompts |
| 90_Params | all | Spec + yellow inputs |
| 99_Notes | all | HAL / ONGC dictionary |

---

## 11. Source

A. Saxena, K. Goebel, D. Simon, N. Eklund, *Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation*, PHM08, 2008.  
Data: NASA C-MAPSS, https://data.nasa.gov/docs/legacy/CMAPSSData.zip
