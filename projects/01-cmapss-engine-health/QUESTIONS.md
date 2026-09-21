# CMAPSS Engine Health — Questions to Answer

Dataset: NASA C-MAPSS turbofan degradation (`https://data.nasa.gov/docs/legacy/CMAPSSData.zip`).
Citation: Saxena, Goebel, Simon, Eklund, PHM08 (2008).

Scope for v1: **FD001** (100 train / 100 test engines, 1 operating condition, HPC degradation). FD002–FD004 stay in the model as comparison slices.

These questions drive three deliverables:

1. **Dashboard** — visual answers an MRO / fleet engineer can scan in 30 seconds.
2. **VBA automation** — buttons and macros that recompute answers after a new NASA file drop.
3. **NL agent** — the same questions, asked in plain English against the workbook.

---

## A. Fleet snapshot (executive)

1. How many engines are in the training fleet vs the test fleet for each FD set?
2. What is the total number of recorded operational cycles?
3. What is the shortest, median, and longest run-to-failure life in training (FD001 train lives: 128 / 199 / 362 cycles)?
4. How many test engines have true RUL below 30 / 50 / 100 cycles (critical / watch / healthy bands)?
5. What share of the test fleet is already inside a maintenance window (RUL ≤ 50)?
6. Which 10 engines should be pulled first this week, ranked by lowest RUL then steepest recent sensor drift?
7. How does FD001 life distribution compare with FD002, FD003, and FD004?
8. Does the two-fault fleet (FD003/FD004) fail earlier or later than the HPC-only fleet?

## B. Data quality and readiness

9. Are all 26 columns present and numeric after import?
10. Which sensors are constant in FD001 and should be dropped from KPIs (`s1, s5, s10, s16, s18, s19`, plus `os3`)?
11. How many missing, duplicate, or out-of-order (unit, cycle) rows exist?
12. Do cycle numbers start at 1 and increase by 1 for every unit?
13. Are unit IDs unique across train vs test, or do they collide and need a `split` flag?
14. What is the noise level (std / IQR) of each useful sensor in the first 30 healthy cycles?
15. After a new zip drop, did row counts match the official spec (FD001 train 20,631 rows, test 13,096 rows)?

## C. Degradation and sensors

16. Which sensors show a clear trend as an engine approaches failure?
17. For a given engine, when does the first persistent deviation from its own healthy baseline appear?
18. What is a simple health index (0–100) from the most informative sensors (`s2, s3, s4, s7, s11, s12, s15, s17, s20, s21` and core-speed family `s8, s9, s13, s14`)?
19. How many cycles before failure does the health index typically cross 70 / 50 / 30?
20. Are high-life engines (life > 250) degrading on the same sensors as short-life engines (life < 150)?
21. Which sensor pairs move together (collinearity), so the dashboard does not plot redundant gauges?
22. Does HPC-related temperature / pressure (`T30/T50`, `P30`, `Ps30`) degrade earlier than fan-related speed sensors in FD003 vs FD001?

## D. Remaining useful life

23. For each training engine, what is RUL at every cycle (`max_cycle - cycle`)?
24. For each test engine, what is RUL at the last observed cycle (from `RUL_FDxxx.txt`)?
25. What is the fleet mean / median / P10 RUL on the latest test snapshot?
26. If we cap RUL at 125 cycles (common CMAPSS piecewise target), how do rankings change?
27. Using only last-cycle sensor values, which linear or rule-based score ranks test engines closest to true RUL?
28. What is the absolute error of that baseline vs true RUL (MAE, and % of engines within 10 / 20 cycles)?
29. Which engines are false-safe (model says healthy, true RUL < 30) — the dangerous misses?
30. Which engines are false-alarm (model says critical, true RUL > 100) — wasted shop visits?

## E. Operating conditions and fault modes

31. How many distinct operating-condition clusters exist in FD002 / FD004 from (`os1, os2, os3`)?
32. Do sensor means shift more because of condition than because of degradation?
33. After conditioning on operating setting, does the health index still trend toward failure?
34. Is six-condition data (FD002/FD004) too noisy for the same KPI thresholds used on FD001?
35. Can the dashboard tell HPC-only failure (FD001/FD002) from HPC+fan failure (FD003/FD004) from late-life sensor shape?

## F. Maintenance and operations (the “so what”)

36. If shop capacity is 8 engines per week, which engines go this week vs next week vs monitor?
37. What is the estimated cycles-to-shop for the current critical list?
38. If we wait 20 more cycles on the watch list, how many engines are predicted to enter RUL ≤ 30?
39. Which engines have unusual early wear (short life despite starting in the same condition)?
40. What single-page brief would a maintenance planner send at 06:00: count by risk band, top 10 list, and sensors that moved overnight?

## G. Dashboard design questions (what each tile must answer)

41. **KPI row:** engines monitored, cycles logged, median life, engines with RUL ≤ 50, worst RUL.
42. **Risk donut:** healthy / watch / critical counts.
43. **Life histogram:** training time-to-failure distribution.
44. **RUL bar:** test engines sorted by true or estimated RUL, colored by band.
45. **Sensor small-multiples:** selected engine vs fleet healthy band over cycles.
46. **Health sparkline:** health index for the engine picked on the slicer.
47. **Leaderboard:** top 10 at-risk units with last cycle, RUL, health index, primary drifting sensor.
48. **Set comparison:** FD001 vs FD003 median life and late-life sensor slope.

## H. VBA automation questions (macros must answer by doing)

49. Can one button ingest `train_FDxxx.txt`, `test_FDxxx.txt`, and `RUL_FDxxx.txt` and land them on named sheets?
50. Can import assign official column names (unit, cycle, os1–os3, s1–s21) instead of blank headers?
51. Can a Clean Data macro drop constant sensors, add `split`, `max_cycle`, `RUL`, `risk_band`?
52. Can Refresh Dashboard rebuild pivots, charts, and the top-10 range without manual clicks?
53. Can Flag Critical write engines with RUL ≤ 30 to a `Alerts` sheet and color the leaderboard?
54. Can Export Brief save a timestamped PDF/CSV of the planner page?
55. Can Validate Import check row counts against the spec and write a pass/fail log for CI-style review?
56. Can Switch Fleet (FD001–FD004) reload the active set and refresh every dependent range?

## I. Natural-language agent questions (exact prompts the agent must handle)

These are the queries the agent should parse and answer from the workbook.

### Status
57. "How many engines are critical right now?"
58. "Show the 10 engines with the lowest remaining life."
59. "What is the RUL of engine 34 in FD001 test?"
60. "Is engine 17 safe to fly another 40 cycles?"
61. "Which engines entered the watch band since the last import?"

### Sensors and health
62. "Which sensor is drifting fastest on engine 5?"
63. "Plot health index for engine 81."
64. "Compare s4 and s11 on the last 30 cycles of engine 20 vs the fleet healthy baseline."
65. "List sensors that do not change in FD001."
66. "What was engine 50's health index at cycle 100?"

### Fleet and comparison
67. "What is median time-to-failure in training?"
68. "Which training engine lived the longest?"
69. "Compare FD001 and FD003 median lives."
70. "How many test engines have RUL under 20 cycles?"
71. "Summarize the fleet in three sentences."

### Planning
72. "If we can shop only 5 engines, which five?"
73. "Give me a morning brief for the maintenance planner."
74. "Which engines look false-safe?"
75. "Explain why engine 8 is flagged."

---

## Priority for build order

**Must answer in the first dashboard (FD001):** 1–6, 10, 16, 18, 23–26, 36, 40–47, 49–55, 57–60, 67, 70, 72–73, 75.

**Second pass (multi-fleet + better model):** 7–8, 22, 27–35, 61–66, 68–69, 74.

**Agent contract:** every NL question maps to a named Excel range or a VBA procedure. If the agent cannot resolve the entity (engine id, FD set, sensor), it asks one clarifying question instead of guessing.
