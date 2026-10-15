---
name: flight-report
description: >
  Search Google Flights and generate a structured price comparison report.
  Triggers on: 便宜機票, 機票比價, 查機票, 航班搜尋, 直飛, 找機票, 機票報告,
  cheap flights, flight search, nonstop flights, flight comparison, airfare,
  flight report, compare flights, best flights, flight deals
user_invocable: true
---

# Flight Report Skill

You are a flight search assistant. When the user asks about flights, airfare, or ticket prices, follow these steps to produce a comprehensive price comparison report.

## Step 1: Parse the User Query

Extract the following from the user's natural language query (Chinese or English):
- **Origin**: departure city or airport
- **Destination**: arrival city or airport
- **Date range**: start and end dates (if the user says "三月到五月", interpret as the full months)
- **Trip type**: one-way, round-trip, or flexible-roundtrip
  - 來回 = round-trip; default to one-way if not specified
  - If the user specifies a **day range** (e.g. 「玩4~7天」「4到5天」), use **flexible-roundtrip**
- **Return offset**: if round-trip (fixed), how many days for the return (default: 7 days)
- **Flexible day range**: if flexible-roundtrip, extract min_days and max_days
  - 天數定義：含頭含尾（出發日 + 回程日都算）。「玩4天」= 出發日算第1天，回程日算第4天，住3晚
  - 例：「4~7天」→ min_days=4, max_days=7
- **Nonstop**: whether direct flights only (直飛 = nonstop)
- **Outbound arrival time limit**: e.g. 「中午前到」→ arrival_before=12:00
- **Baggage needs**: LCC routes typically need checked baggage (default round-trip: NT$2,000)
- **Seat class**: economy (default), business, first
- **Number of adults**: default 1

If any critical info is missing (origin or destination), ask the user before proceeding.

## Step 2: Map City Names to IATA Codes

Use the reference file at `~/.claude/skills/flight-report/references/airport-codes.md` to convert Chinese city names to IATA airport codes.

Common mappings:
- 桃園/台北 → TPE
- 東京成田 → NRT, 東京羽田 → HND
- 大阪/關西 → KIX
- 福岡 → FUK
- 首爾/仁川 → ICN
- 曼谷 → BKK
- 新加坡 → SIN

If the city is ambiguous (e.g. "東京" could be NRT or HND), default to the main international airport (NRT for 東京) and mention the assumption.

## Step 3: Run Flight Search

Execute the search script using the Bash tool:

```bash
python ~/.claude/skills/flight-report/scripts/search_flights.py \
  --origin {ORIGIN} \
  --destination {DEST} \
  --start-date {YYYY-MM-DD} \
  --end-date {YYYY-MM-DD} \
  --trip-type {one-way|round-trip} \
  --seat {economy|business|first} \
  --adults {N} \
  --currency TWD \
  --sample-mode 3 \
  --delay 2 \
  --output /tmp/flight_results.json \
  {--nonstop if requested} \
  {--return-offset N if round-trip}
```

**Important notes:**
- The script samples every 3 days by default. For short ranges (< 14 days), use `--sample-mode 1`.
- For large date ranges (> 3 months), use `--sample-mode 7` to reduce requests.
- The script outputs progress to stderr and results to the JSON file.
- If the script fails or returns errors, check if the IATA codes are correct and try with `--sample-mode 7` for a smaller sample.

### Step 3b: Flexible Round-Trip Search (Independent One-Way Combination)

When the user specifies a flexible day range (trip_type = flexible-roundtrip), use the following flow instead of Step 3:

1. **Search outbound (one-way)**: origin → destination, across the user's date range
2. **Search return (one-way)**: destination → origin, date range = outbound_start + (min_days-1) ~ outbound_end + (max_days-1)
3. **Run both searches concurrently** (use `run_in_background` for at least one):

```bash
# Outbound search
python ~/.claude/skills/flight-report/scripts/search_flights.py \
  --origin {ORIGIN} --destination {DEST} \
  --start-date {OUT_START} --end-date {OUT_END} \
  --trip-type one-way --sample-mode 1 --delay 2 \
  --currency TWD --output /tmp/out_daily.json \
  {--nonstop if requested}

# Return search
python ~/.claude/skills/flight-report/scripts/search_flights.py \
  --origin {DEST} --destination {ORIGIN} \
  --start-date {RET_START} --end-date {RET_END} \
  --trip-type one-way --sample-mode 1 --delay 2 \
  --currency TWD --output /tmp/ret_daily.json \
  {--nonstop if requested}
```

4. **Combine results** using the combination script:

```bash
python ~/.claude/skills/flight-report/scripts/combine_flights.py \
  --outbound-json /tmp/out_daily.json \
  --return-json /tmp/ret_daily.json \
  --min-days {MIN_DAYS} --max-days {MAX_DAYS} \
  --filter-complete \
  --baggage-cost {BAGGAGE_COST} \
  {--arrival-before HH:MM if specified} \
  --output /tmp/combo_results.json
```

**⚠️ Sample-mode caveat for flexible round-trip:**
When both outbound and return use `--sample-mode 3`, the possible day counts are limited to `offset + 3n` values, so some trip lengths will have zero combinations. For flexible round-trip searches, **always use `--sample-mode 1`** and limit the date range to one month or less. For larger ranges, split into monthly batches.

## Step 4: Read and Analyze Results

Read the output JSON file:
```bash
cat /tmp/flight_results.json
# or for flexible round-trip:
cat /tmp/combo_results.json
```

### Data Quality Filtering

The scraper sometimes returns entries with a price but no flight details (airline, departure, and arrival are empty). These incomplete entries must be filtered out before analysis to avoid recommending flights with no actionable information.

- For flexible round-trip: use `--filter-complete` in `combine_flights.py` (handles this automatically)
- For one-way / fixed round-trip: manually skip any flight where `airline`, `departure`, or `arrival` is null/empty

### Analysis

Analyze the data:
- Sort flights by price to find the cheapest options
- Group by month for monthly summaries
- Identify which day of the week tends to be cheapest
- Note any "is_best" flights (Google's recommended picks)

## Step 5: Supplement with Web Search (Optional)

Use WebSearch to find additional context:
- Current airline baggage policies for the route
- Any seasonal travel advisories
- Alternative airport options

Keep this brief — the main value is in the flight data.

## Step 6: Generate the Report

Follow the template at `~/.claude/skills/flight-report/references/report-template.md` to produce the final report in **Traditional Chinese (繁體中文)**.

- For **one-way / fixed round-trip**: use the standard report template (single-direction table)
- For **flexible round-trip**: use the **來回組合報告模板** (round-trip combination template) in the same file

Key formatting rules:
- Use a Markdown table for the price comparison
- Show TOP 10 cheapest flights (or combinations for flexible round-trip)
- For flexible round-trip, include: 天（含頭含尾）/夜、請假天數、行李費、總成本
- **請假天數算法**：去程當天一律算請假（除非出發時間在晚上 22:00 之後），回程當天不算請假。中間的平日全部算請假
- Include "各天數最便宜" and "依請假天數推薦" sections for flexible round-trip
- Include monthly price summaries (for one-way/fixed round-trip)
- Add actionable booking advice
- Include Google Flights and Skyscanner quick links
- All prices in TWD unless the user specifies otherwise

## Error Handling

- If `fast-flights` fails on a particular date, the script logs the error and continues with other dates
- If ALL dates fail, suggest the user try:
  1. Different date range
  2. Removing the nonstop filter
  3. Checking if the route exists on Google Flights
- If the IATA code mapping is unclear, ask the user to confirm the airport
