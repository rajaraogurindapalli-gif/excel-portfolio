# Iowa Liquor Sales — Questions to be answered

**Case:** Prairie Grain & Power Trading (disguised commercial head)  
**Exhibit:** State of Iowa Liquor Sales, calendar 2024  
**Source:** https://data.iowa.gov/catalog/dataset/1261  
**Rule:** Wholesale to the store is not consumer sell-out. Blue cells are assumptions, not Iowa facts.

The board meets in 14 days. The file must answer the questions below. Charts that do not serve a question are out of scope.

---

## Fact vs assumption

| Iowa fact (do not invent) | Blue / yellow on `90_Params` |
|---|---|
| Date, store, city, county | FY 2025 revenue target and quarterly weights |
| Vendor name | Festival lift %, slack cut %, competitor Q4 price-cut % |
| Item, category | Store-type map when the name is ambiguous |
| Cost, state retail, bottles, sale dollars, liters | 90-day pace factor (default 1.00 until 2025 actuals exist) |

If a number is not on data.iowa.gov, it is labeled assumption.

---

## A — Descriptive (what 2024 was)

**A1.** What was 2024 net sales, liters, and realized price per liter?  
**A2.** Does 80% of sales sit in ≤20% of SKUs? Of brands? Of retailers? Give three Lorenz points, not a slogan.  
**A3.** Which SKUs are A / B / C on dollars, and which A-SKUs are C on margin (state cost vs state retail)?  
**A4.** Who are the top 10 retailers by dollars, and what share of *their* book is a single vendor?  
**A5.** Who are the top 8 vendors by category, and what is implied share inside whiskey and inside vodka?  
**A6.** What is mix by category, by county, and by month?  
**A7.** What is the retailer book by store type (grocery / liquor / convenience — mapped and labeled)?

---

## G — Diagnostic (why it looked like that)

**G1.** Waterfall versus a flat year: volume vs $/liter vs mix vs new items. Which one built the dollar?  
**G2.** Why do peak months spike — more bottles, higher price, or a different SKU mix?  
**G3.** Why is retailer *R* large — breadth of SKUs or one vendor’s bottle? (hostage risk)  
**G4.** Why is vendor *V* large — many stores or a few large doors?  
**G5.** Which A-SKUs have high dollars and worsening $/liter through the year? (price leak)

---

## D — Predictive (what if we do not intervene)

**D1.** Month actual vs target vs forecast. YTD. Implied full year = actual YTD ÷ seasonal weight used so far. RAG.  
**D2.** Which 10 A-SKUs are more than 15% behind their own seasonal path?  
**D3.** Next 90 days by category = last-year same months × YTD pace vs last year. Pace defaults to 1.00.  
**D5.** Base-case 2025 = 2024 × seasonal index, no lift. Gap to the board target.  
**D6.** The forecast is an index, not a causal model. State that on the tracker.

---

## B / C / E — Prescriptive (what we sign)

**B2.** Base case vs target.  
**B3.** Festival case: peak months +15% on A-SKUs only. Slack case: trough months −10% on the whole book.  
**B4.** Competitor case: #1 vendor cuts realized price 8% in Q4; 30% of overlapping SKUs lose 12% volume.  
**B5.** Combined festival + competitor cut. Plan or wish?  
**C2.** Twenty retailers to fund in the peak (dollar × growth × not hostage).  
**C3.** Vendors to deepen vs dual-source vs narrow.  
**C4.** If capital funds only A-SKUs, what 2024 dollar coverage remains, and which counties go dark?  
**D4.** One lever to close the gap: +2% price on A-SKUs, peak volume, or drop C-SKUs.  
**E1.** Binding 2025 list: SKUs to fund, retailers to keep, vendors to dual-source, target you would sign.  
**E2.** What would have to be true to keep the original target?  
**E3.** What must not be claimed (no sell-out; wholesale only; DEV is not the plan).

---

## How the four analytics types sit on the boards

| Type | Sheet | Questions |
|---|---|---|
| All four summarized | `01_Board` | A1, A2, D1, B5, D4, E3 |
| Descriptive | `11_Describe` | A1–A7 |
| Diagnostic | `12_Diagnose` | G1–G5 |
| Predictive | `13_Predict` | D1–D3, D5–D6 |
| Prescriptive | `14_Prescribe` + `05_Decision` | B2–B5, C2–C4, D4, E1–E3 |

One control strip on `90_Params` (target, lifts, selected category / retailer / vendor / SKU). Every board reads the same drivers.

---

## Agent — 12 frozen prompts

1. What was 2024 sales and $/liter?  
2. Do we have 80/20 on SKUs?  
3. Which SKUs are A on dollars and C on margin?  
4. Which retailers are hostage to one vendor?  
5. Why did the peak months move?  
6. Does base-case 2025 hit the target?  
7. What is the combined festival + competitor-cut gap?  
8. Which 20 retailers do we fund?  
9. If we fund only A-SKUs, what coverage remains?  
10. Implied full-year vs target (RAG).  
11. Which lever closes the gap?  
12. What must we not claim?

Answers must come from the model. The agent does not invent dollars.

---

## Environment stamp (every answer)

DEV = 10% of stores. TEST = 50%. PROD = 100%.  
Cover and Board show the stamp. A DEV number is not the signed plan.

---

## Out of scope

- Consumer sell-out or household demand  
- Extra years treated as if they were Iowa 2024  
- A second home dashboard that copies dollars instead of pointing at the model  
- Free-text LLM answers that cannot be traced to a measure
