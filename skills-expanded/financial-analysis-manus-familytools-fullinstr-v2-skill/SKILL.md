---
name: financial-analysis-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for financial-analysis using latest full-instruction v2 family injection.
allowed-tools:
  - extract_archive
  - list_dir
  - read_file
  - run_python
  - run_shell
  - search_text
  - sec13f_fund_details
  - sec13f_holdings_compare
  - sec13f_holdings_query
  - sec13f_index_search
  - sec13f_top_holders
  - write_file
  - write_json
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Financial Analysis Skill

## When to use this skill
Use this skill for tasks analyzing hedge fund activities, such as comparing financial data across quarters (e.g., Q2 and Q3). It applies when determining Assets Under Management (AUM), stock counts held by funds, identifying stocks with increased investments, or ranking fund managers by investments in specific stocks using SEC 13F filings.

## Visible input and artifact inventory
The environment typically includes:
- Zipped SEC 13F filings datasets (e.g., `13f-2025-q2.zip`, `13f-2025-q3.zip`).
- An `instruction.md` detailing questions.
- A `task.toml` with metadata.
- A `Dockerfile` for setup.

The expected output is a JSON file named `answers.json` in `/root`, formatted per the instructions' schema.

## Execution procedure for the current task
1. **Initial Setup**: Read `instruction.md` for questions and output format. Inventory visible files to locate datasets.
2. **Data Extraction**: Use `extract_archive` to unzip datasets into directories (e.g., `/root/2025-q2`).
3. **Fund Identification**: For fund-specific data (AUM, stock count), use `sec13f_index_search` to fuzzy search the COVERPAGE for the fund's name to get its `accession_number`.
4. **Data Retrieval**:
   - Use `sec13f_fund_details` with the `accession_number` for AUM and stock count.
   - For comparing holdings, get the `accession_number` for both quarters. Use `sec13f_holdings_compare` to analyze changes and identify top stocks with increased investments.
   - For top fund managers investing in a stock, find the stock's CUSIP, then use `sec13f_top_holders` to rank funds by share value.
5. **Artifact Creation**: Compile answers into a JSON object matching the schema. Use `write_json` to save it to `/root/answers.json`.

## Family tool routing and useful placeholder snippets
- **`extract_archive`**: Unzip datasets.
- **`sec13f_index_search`**: Find `accession_number` by searching COVERPAGE.
  ```python
  accession_number = sec13f_index_search(search_term="fund name", quarter="2025-q3")
  ```
- **`sec13f_fund_details`**: Get AUM and stock count.
  ```python
  details = sec13f_fund_details(accession_number="0001234567-25-000001")
  ```
- **`sec13f_holdings_compare`**: Compare holdings between quarters.
  ```python
  comparison = sec13f_holdings_compare(accession_number_q2="...", accession_number_q3="...")
  ```
- **`sec13f_top_holders`**: Find top investors in a stock.
  ```python
  top_holders = sec13f_top_holders(cusip="123456789", quarter="2025-q3")
  ```
- **`write_json`**: Save final answers.

## Validation checks before final submission
- Verify `answers.json` exists in `/root`.
- Ensure JSON structure exactly matches the schema (e.g., `q1_answer` is a number, `q3_answer` is a list).
- Check all questions are answered with correct data types.

## Common failure modes and repair actions
- **Missing `accession_number`**: Try variations of the fund's name or check for typos.
- **Incorrect JSON Schema**: Review data types and keys used during `write_json` and correct them.
- **Data Extraction Errors**: Ensure `extract_archive` was used correctly and paths match instructions.

## Finalizer capsule
If nearing the maximum step limit and analysis is incomplete, create a minimally compliant `answers.json` in `/root`. It should contain correct keys per the schema, even with default values (e.g., `0` for numbers, `[]` for lists), to ensure correct artifact shape and prevent complete failure.
