# CMAPSS Engine Health — Final Questions

**Owner lens:** 18 years HAL (aero engines, airworthiness, module shop) and ONGC (rotating equipment, reliability, shutdown planning).

**Data:** NASA C-MAPSS turbofan run-to-failure (`CMAPSSData.zip`).  
**v1 fleet:** FD001 (sea level, HPC degradation, 100 train / 100 test).  
**v2 fleets:** FD002–FD004 (multi-regime and HPC+fan).

These are not academic EDA prompts. Each question ends in a decision a Chief Engineer / Reliability Manager would sign.

Decision language used throughout:

| Band | Meaning on this project | HAL analogue | ONGC analogue |
|---|---|---|---|
| Continue | RUL > 100 cycles | Clear for next flying programme | Run to next planned window |
| Restrict / Watch | 31–100 | Monitor, limit role, plan bay | Condition-based watch, avoid unplanned trip |
| Withdraw | RUL ≤ 30 | Ground / raise shop-visit demand | Isolate / advance shutdown |

---

## 0. Questions this workbook exists to answer

Q0.1 Which assets are no longer fit to continue, and on what evidence?
Q0.2 If the bay / workshop can take only *N* units this week, which *N* go first?
Q0.3 Is the indication a real HPC-path degradation, or noise / regime shift / bad import?
Q0.4 What brief does the duty engineer send at 06:00 without opening twenty sheets?

If a chart or macro does not help Q0.1–Q0.4, it does not ship in v1.

---

## 1. Continue / restrict / withdraw  (airworthiness + production)

Q1.1 For each test engine at last recorded cycle, is the call **Continue**, **Watch**, or **Withdraw**?
Q1.2 How many engines are in each band right now?
Q1.3 Which engines have RUL ≤ 30 (Withdraw) and must be listed on the alert sheet today?
Q1.4 Engine *X* is asked to do 40 more cycles. Is that inside remaining life with margin, or is it a no-go?
Q1.5 Which engines look healthy on the score but have true RUL < 30 (**false-safe** — the airworthiness miss)?
Q1.6 Which engines look critical but have true RUL > 100 (**false-alarm** — wasted bay time / deferred production)?
Q1.7 For engine *X*, write one sentence a certifying review would accept: *why* it is flagged (sensor, slope, RUL, band).

HAL reading: dispatch vs ground.  
ONGC reading: keep online vs advance outage.

---

## 2. Shop visit / shutdown planning

Q2.1 Rank the fleet for the next shop / shutdown window: lowest RUL, then steepest 20-cycle health drop.
Q2.2 If bay capacity is 5 this week and 8 next week, who is This Week / Next Week / Monitor?
Q2.3 If Watch engines run another 20 cycles, how many will cross into Withdraw?
Q2.4 What is cycles-to-bay for the current Withdraw list?
Q2.5 Which training engines were short-life (< 150 cycles) despite the same sea-level condition — early-wear / build variation cases?
Q2.6 Does capping RUL at 125 cycles (piecewise life, ignore very healthy tail) change the bay queue?

HAL reading: engine-change and module-bay loading.  
ONGC reading: platform shutdown slot and workshop loading.

---

## 3. What is failing  (module / path)

Q3.1 Which sensors actually move as HPC degradation grows on FD001, and which are dead (constant) and must not be shown as gauges?
Q3.2 For engine *X*, which one sensor has the fastest drift over the last 30 cycles versus its own first-30-cycle baseline?
Q3.3 Build one Health Index 0–100 from the live sensors. When does the fleet typically cross 70 / 50 / 30 before failure?
Q3.4 Do short-life and long-life engines degrade on the same sensors, or are there two wear signatures?
Q3.5 On FD003 (HPC + fan), does the HPC temperature/pressure path move earlier than fan-speed path? Can the dashboard tell the fault family?
Q3.6 Which sensor pairs are collinear so we do not put two gauges on the same physical effect?

HAL reading: fan / LPC / HPC / HPT / LPT path, not anonymous `s4`.  
ONGC reading: gas-generator path vs power-turbine / compressor path.

Sensor names used on the dashboard (not only s-numbers):

- T24, T30, T50 — temperatures  
- P15, P30, Ps30 — pressures  
- Nf, Nc, NRf, NRc — speeds  
- phi, BPR, W31, W32 — flow / bleed  
- Dead on FD001 and hidden: T2, P2, epr, farB, Nf_dmd, PCNfR_dmd, os3

---

## 4. Trust the data before you trust the call

Q4.1 Did import land 26 numeric columns with official names, and do row counts match NASA spec (FD001 train 20,631 / test 13,096)?
Q4.2 Are cycles complete and monotonic per engine (start at 1, step +1, no duplicates)?
Q4.3 Train and test both use unit 1…100. Is every row stamped Train/Test so we never mix them in a pivot?
Q4.4 What is the healthy-band noise (first 30 cycles) so a later deviation is judged against real scatter, not a single point?
Q4.5 On FD002/FD004, do operating settings move the sensors more than damage does? If yes, raw thresholds from FD001 are not airworthy on those fleets.

No dashboard number is published until Q4.1–Q4.3 are green.

---

## 5. Fleet picture  (one screen)

Q5.1 How many engines and cycles are under watch in the active FD set?
Q5.2 What is min / median / max run-to-failure life in training? (FD001: 128 / 199 / 362.)
Q5.3 What is P10 / median / mean remaining life on the test snapshot?
Q5.4 How do FD001 vs FD003 median lives and late-life slopes differ (one fault vs two)?
Q5.5 What is the single-page 06:00 brief: band counts, top 10, worst RUL, dominant drifting sensor, import status?

---

## 6. What the three tools must answer

### Dashboard tiles (v1)

Each tile maps to one final question.

| Tile | Answers |
|---|---|
| Band KPIs | Q1.2, Q5.1, Q5.3 |
| Withdraw / Watch / Continue donut | Q1.1, Q1.2 |
| Bay queue (top 10) | Q2.1, Q2.2 |
| Life histogram (training) | Q5.2, Q2.5 |
| Selected-engine health + sensors | Q1.4, Q1.7, Q3.2, Q3.3 |
| Import / data-trust strip | Q4.1–Q4.3 |

### VBA (the engineer does not re-type NASA files)

Q6.1 One button imports train, test, and RUL text files onto named sheets with official headers.
Q6.2 One button builds `RUL`, `health_index`, `risk_band`, `split`, and drops dead sensors.
Q6.3 One button refreshes pivots, queue, colours, and alerts.
Q6.4 One button exports the 06:00 brief (PDF + CSV) with timestamp.
Q6.5 Validate Import writes pass/fail against NASA row counts before any KPI is shown.
Q6.6 (v2) Switch Fleet FD001–FD004 and rebuild.

### NL agent  — frozen prompt list

The agent answers only these. Anything else gets one clarifying question.

1. How many engines are Withdraw / Watch / Continue right now?
2. Show the bay queue for this week. Capacity is *N*.
3. What is the remaining life of engine *X* in FD001 test?
4. Can engine *X* do *C* more cycles?
5. Why is engine *X* flagged?
6. Which sensor is drifting on engine *X*?
7. What is the health index of engine *X* at cycle *C*?
8. Which engines are false-safe?
9. What is median time-to-failure on the training fleet?
10. Give me the 06:00 brief.
11. Compare FD001 and FD003 median life.
12. Did the last import pass validation?

---

## 7. Out of scope for v1  (parked, not deleted)

- Deep learning RUL models  
- FD002/FD004 as the primary dashboard  
- Cost / AOG / production-deferment money model  
- Mapping CMAPSS sensors 1:1 onto a specific HAL engine type or ONGC GT frame  
- Automatic airworthiness release  — this tool supports the engineer; it does not replace the stamp

---

## 8. Acceptance

v1 is done when:

1. Q1.1–Q1.7 and Q2.1–Q2.4 have numbers on the dashboard.  
2. Q4.1–Q4.3 are a visible green/red strip.  
3. VBA Q6.1–Q6.5 run from buttons.  
4. Agent prompts 1–6 and 10 return the same numbers as the tiles.  
5. A HAL/ONGC colleague can use the workbook without reading this file.
