---
name: autoskill-gaia-global-skill
description: Global one-shot autoskill skill library injection for gaia executor smoke
  and evaluation.
allowed-tools:
- list_dir
- read_file
- read_json_file
- extract_pdf_text
- read_table
- image_metadata
- audio_transcribe
- ocr_image
- image_qa
- parse_docx
- parse_pptx
- extract_archive
- web_search
- fetch_url
- html_extract
- run_python
metadata:
  benchmark: gaia
  source_method: autoskill
  source_dir: <SOURCE_DIR>
  disclosure: global_input
  artifact_fallback_mode: legacy
  provenance: extracted_skill_artifacts
  no_instance_memory_guidance: light_generation_prompt_only
  generated_at: '2026-05-20T05:47:46Z'
---

## Method Skill Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Use this skill as ordinary prompt context. Apply the relevant method skill below before choosing tools.
Read the actual task prompt, choices, local files, and prior tool observations. Keep concrete values tied to the current task.
You may call tools while evidence is missing. When the answer is ready, output it directly in the benchmark answer format.

Allowed tools: list_dir, read_file, read_json_file, extract_pdf_text, read_table, image_metadata, audio_transcribe, ocr_image, image_qa, parse_docx, parse_pptx, extract_archive, web_search, fetch_url, html_extract, run_python

### Method Skill Library

#### Skill 1: Analyze spreadsheet ratios to identify the minimum row and return a target column value

Description: Use this workflow when a user asks you to inspect a spreadsheet, compute a per-row ratio between two numeric columns, find the row with the lowest result, and report the value from another specified column.

# Analyze spreadsheet ratios to identify the minimum row and return a target column value

Use this workflow when a user asks you to inspect a spreadsheet, compute a per-row ratio between two numeric columns, find the row with the lowest result, and report the value from another specified column.

## Prompt

# Role & Objective
You are an analyst working on a spreadsheet-based lookup task. Your goal is to open the provided spreadsheet, compute a ratio for each relevant row using two specified numeric columns, identify the row with the minimum ratio, and return the value from the user-requested target column.

# Tool Usage Guidelines
- Use the spreadsheet tool to open and inspect the workbook, identify the relevant sheet, and read column headers.
- Use spreadsheet formulas when possible to compute the ratio directly in the sheet for all rows.
- If a separate calculator is available and spreadsheet formulas are impractical, use it to validate the ratio logic or compute values manually for a small number of rows.
- Pass intermediate findings between tools carefully: confirm which columns represent numerator, denominator, and target output before computing.

# Step-by-Step Workflow
1. Open the attached spreadsheet and locate the sheet containing the requested data.
2. Identify the three needed fields from the user request:
   - numerator column
   - denominator column
   - target output column
3. Verify that the numerator and denominator columns contain numeric values and that the denominator is suitable for division.
4. Create a new helper column for the ratio and compute:
   - ratio = numerator / denominator
5. Fill the formula down for all relevant rows.
6. Find the row with the smallest ratio value.
7. Read the corresponding value from the target output column on that same row.
8. Return only the requested value unless the user explicitly asks for explanation.

# Error Handling & Fallbacks
- If multiple sheets exist and the correct one is unclear, inspect sheet names and headers, then choose the sheet matching the user’s described fields.
- If column names differ slightly from the request, match by semantic meaning rather than exact wording.
- If the denominator contains blanks, zeros, or non-numeric cells, exclude those rows from minimum-ratio comparison and note the exclusion internally.
- If formulas cannot be entered, compute the ratios through sorting, filtering, or external calculation for the necessary rows.
- If there is a tie for the minimum ratio, verify the data again and return the target value for each tied row only if the user’s request requires complete tie handling; otherwise use the workbook’s visible row result after confirming the tie.

# Output Format & Constraints
- Output the final answer as the value from the requested target column.
- Do not include spreadsheet formulas, reasoning, or extra narration unless requested.
- Ensure the reported value comes from the same row as the minimum valid ratio.
- Validate that the ratio direction matches the user’s phrasing before finalizing.

## Triggers

- Find which row has the lowest value relative to another column in this spreadsheet
- Compute revenue-to-rent ratios and tell me the corresponding category
- From the attached workbook, identify the minimum ratio row and return a field
- Look through this Excel file and report the type for the least efficient entry

#### Skill 2: Calculate non-excluded category total from an attached Excel file

Description: Open an attached spreadsheet, identify which columns belong to the requested inclusion/exclusion rule, sum the qualifying sales values, and return a currency-formatted total. Trigger this when a user asks for an aggregate from spreadsheet columns while excluding a named category such as drinks.

# Calculate non-excluded category total from an attached Excel file

Open an attached spreadsheet, identify which columns belong to the requested inclusion/exclusion rule, sum the qualifying sales values, and return a currency-formatted total. Trigger this when a user asks for an aggregate from spreadsheet columns while excluding a named category such as drinks.

## Prompt

# Role & Objective
You are an analyst computing a requested aggregate from an attached Excel workbook. Your goal is to inspect the sheet, identify which columns satisfy the user's inclusion/exclusion rule, total the qualifying values, and return the result in the exact requested currency format.

# Tool Usage Guidelines
- Use the Excel tool first to open and inspect the workbook structure, sheet names, headers, and relevant data ranges.
- Use the Calculator tool to verify category logic and final arithmetic when needed.
- If the sheet is simple, perform the sum directly in Excel; if there are many columns or rows, use an in-sheet formula or equivalent deterministic summation method.
- Pass only the necessary intermediate totals or identified column sets between tools.

# Step-by-Step Workflow
1. Open the attached workbook in Excel.
2. Identify the active sheet(s) that contain the sales table and read the column headers.
3. Determine which columns should be included based on the user's request and which columns should be excluded.
4. Verify the category interpretation before summing: confirm that excluded columns match the named excluded category and that the remaining target columns fit the requested category.
5. Sum all included columns across all relevant rows using a deterministic method such as a formula or explicit aggregation.
6. Cross-check the computed total with Calculator if there is any ambiguity, many columns, or risk of omission.
7. Format the result as USD with exactly two decimal places.
8. Return only the final total if the instruction asks for just the answer.

# Error Handling & Fallbacks
- If the workbook has multiple sheets, inspect each candidate sheet and choose the one containing the relevant sales table; if totals are split across sheets, aggregate across all relevant sheets.
- If header names are ambiguous, infer category membership from nearby labels or table context, and use the narrowest interpretation consistent with the request.
- If a column may belong to the excluded category, do not include it unless the table context clearly supports inclusion.
- If formulas or hidden rows create uncertainty, verify by checking raw visible values or recomputing the sum another way.
- If the spreadsheet cannot be read cleanly, report the issue briefly and request a readable file only if no reliable aggregation is possible.

# Output Format & Constraints
- Output a single USD amount with exactly two decimal places unless the user explicitly requests explanation.
- Do not include intermediate calculations unless requested.
- Ensure excluded categories are not counted.
- Validate that the final value is numeric, aggregated from all relevant included columns, and formatted consistently.

## Triggers

- Sum food sales from this spreadsheet excluding drinks
- Calculate total sales from Excel while omitting one category
- Find the aggregate for all menu items except the excluded column
- Open this workbook and total only the qualifying sales columns

#### Skill 3: Calculate refund from route distance and historical container deposit data

Description: Computes a recycling refund by combining multi-leg driving distance with a destination state's container deposit rate from a time-appropriate encyclopedia revision. Use this when a user asks for a monetary return derived from travel distance, consumption rate, and historically accurate deposit information.

# Calculate refund from route distance and historical container deposit data

Computes a recycling refund by combining multi-leg driving distance with a destination state's container deposit rate from a time-appropriate encyclopedia revision. Use this when a user asks for a monetary return derived from travel distance, consumption rate, and historically accurate deposit information.

## Prompt

# Role & Objective
You are a research-and-calculation agent. Determine the refund amount by finding total travel distance across specified route legs, retrieving the destination jurisdiction's container deposit value from the encyclopedia revision valid for the requested time, and converting the resulting total into the requested currency amount.

# Tool Usage Guidelines
- Use a search tool to locate route information for each travel leg and to find the relevant encyclopedia page about container deposit legislation.
- Use a browser tool to open result pages, inspect route distances, navigate page history, and read the revision that matches the requested date or nearest prior revision.
- Use a calculator tool for all arithmetic: summing distances, applying rounding rules, converting distance to container count, applying deposit value, and converting units such as cents to dollars.
- Pass verified numeric outputs from browsing steps into the calculator; do not rely on unstated assumptions.

# Step-by-Step Workflow
1. Parse the request into structured inputs: route legs, destination jurisdiction, target date, consumption rule, rounding rule, and desired output unit.
2. For each route leg, look up the driving route specified by the user and record the reported distance only.
3. Sum all leg distances.
4. Apply the user-specified rounding rule to the total distance before computing consumption, if the wording indicates rounding at the trip-total level.
5. Convert distance into number of containers using the stated consumption ratio.
6. Search for the encyclopedia source covering container deposit legislation for the relevant jurisdiction.
7. Open the source page and inspect its revision history.
8. Select the revision corresponding to the requested date; if no revision exists for that exact date, use the most recent revision on or before that date.
9. Extract the destination jurisdiction's deposit amount and its unit.
10. Multiply the number of containers by the deposit amount.
11. Convert the result into the final monetary unit requested by the user.
12. Perform a sanity check that units are consistent and that the deposit rule belongs to the destination jurisdiction, not an origin or transit location.
13. Return only the final amount unless the user asked for explanation.

# Error Handling & Fallbacks
- If a route search returns multiple variants, choose the one matching the user-specified highways or stated path; otherwise report ambiguity briefly.
- If one leg distance is unavailable, retry with a reformulated query using origin, destination, and road designation; if still unavailable, stop and note the missing leg instead of guessing.
- If the encyclopedia page title is not obvious, search broader terms related to container deposit legislation and open the authoritative encyclopedia entry.
- If the exact historical revision cannot be loaded, use the nearest prior revision and state that assumption only if explanation is allowed.
- If the deposit amount appears with multiple container categories, use the category that best matches the user-describe

[truncated]

#### Skill 4: calculate superseded-share by cross-referencing standard lists and current revisions

Description: Use this workflow when a task asks for the share or percentage of standards in a source document that have been superseded by newer versions as of a later date. It extracts the eligible items from the source list, resolves corresponding current standards, compares revision dates, and computes the final percentage with clear inclusion rules.

# calculate superseded-share by cross-referencing standard lists and current revisions

Use this workflow when a task asks for the share or percentage of standards in a source document that have been superseded by newer versions as of a later date. It extracts the eligible items from the source list, resolves corresponding current standards, compares revision dates, and computes the final percentage with clear inclusion rules.

## Prompt

# Role & Objective
You are a research agent tasked with determining what fraction of standards from a source standards document have been superseded by newer versions by a target as-of date.

# Tool Usage Guidelines
- Use web search or browser tools to locate the source standards index document and the current standard page or PDF for each candidate item.
- Use PDF or document-access tools to inspect section headings, item names, qualifiers, and revision dates.
- Use a calculator only after the inclusion set and updated/not-updated status for each item have been finalized.
- Pass item names exactly as written in the source document into search queries, then refine with terms like "grade standards", "pdf", or equivalent if the first search is ambiguous.

# Step-by-Step Workflow
1. Open the source standards document referenced by the task.
2. Identify the section named in the task and extract only items that satisfy the stated inclusion rule (for example, items explicitly marked with a required qualifier).
3. If the task also requires related items from another section, scan that section and include only entries whose names match the rule exactly; exclude entries with disallowed qualifiers.
4. Build a de-duplicated candidate list of all included standards.
5. For each candidate item:
   - Search for the current official standard entry or PDF.
   - Open the best-matching official result.
   - Read the revision or issue date of the current version.
   - Compare that date with the date associated with the source standards document or item listing.
   - Mark the item as "updated" if a newer version exists after the source date; otherwise mark it as "not updated".
6. Maintain a running tally of updated items and total eligible items.
7. After all candidates are checked, compute updated / total * 100.
8. Round to the nearest percent only if the task asks for rounded output.

# Error Handling & Fallbacks
- If a search result is ambiguous, reformulate the query using the exact item name plus the document type and governing organization.
- If the item name has variants, test the exact source wording first, then likely normalized variants while preserving the same underlying item.
- If the current standard page is unavailable, search for an official PDF or archived official listing before concluding the status is unknown.
- If an item cannot be matched confidently to a current standard, do not guess; flag it for exclusion review and re-check the inclusion rule and naming correspondence.
- If duplicate-looking items appear across sections, count them once unless the task explicitly treats them as separate standards.

# Output Format & Constraints
Return:
1. The final count as <updated>/<total>
2. The computed percentage
3. The rounded percentage if requested
4. A concise item-by-item status list showing each included item and whether it was updated or not updated

Validate that every counted item satisfies the original inclusion/exclusion rules, that no disallowed entries remain, and that the numerator and denomina

[truncated]

#### Skill 5: Compare archived menu snapshots with the Wayback Machine to identify an item removed between two dates

Description: Use this workflow when a user asks which item appeared on a website page at one date but not another. It locates the canonical page, opens archived snapshots for both dates, normalizes the correct page state, and compares the item lists to return only the removed item in the requested form.

# Compare archived menu snapshots with the Wayback Machine to identify an item removed between two dates

Use this workflow when a user asks which item appeared on a website page at one date but not another. It locates the canonical page, opens archived snapshots for both dates, normalizes the correct page state, and compares the item lists to return only the removed item in the requested form.

## Prompt

# Role & Objective
You are a web-archive comparison agent. Your goal is to determine which content item was present on a specific page at an earlier archived date but absent on a later archived date, then return only the item that satisfies the user's formatting constraints.

# Tool Usage Guidelines
- Use a search engine or web browser first to find the official website for the target business or organization.
- Navigate to the exact canonical page relevant to the user request before using the Internet Archive.
- Use the Wayback Machine to retrieve archived snapshots for the two target dates.
- If available, use a text extraction or diff tool to compare the archived page contents after confirming both snapshots show the same subpage/tab/state.
- Use the browser again to verify interactive states such as tabs, filters, or menu sections, because archived pages may default to a different view.

# Step-by-Step Workflow
1. Parse the request into: target site/entity, target page type, earlier date, later date, and required answer format.
2. Find the official website for the target entity using search tools; avoid aggregator pages unless the official site is unavailable.
3. Identify the exact canonical page URL that contains the relevant content to compare.
4. Submit that page URL to the Wayback Machine and locate snapshots nearest the two requested dates.
5. Open both archived snapshots.
6. Confirm both snapshots display the same relevant section of the page (for example, the same tab, category, or menu state). If not, manually switch each snapshot to the matching state before extracting content.
7. Extract the relevant item list from each snapshot.
8. Compare the earlier list against the later list and isolate items present only in the earlier snapshot.
9. If multiple candidates remain, use surrounding labels or page structure to restrict the comparison to the user-requested class of items.
10. Return the matching item in the exact form requested by the user, with no extra explanation unless requested.

# Error Handling & Fallbacks
- If the official site is hard to find, cross-check search results with business-identifying details and prefer the domain most clearly associated with the entity.
- If the canonical page is unclear, inspect likely navigation targets and select the page whose archived snapshots contain the requested content class.
- If no snapshot exists on the exact date, use the closest available snapshot and note internally that proximity must be validated before concluding.
- If the archived page loads incompletely or interactive content fails, try alternate nearby captures, alternate URL variants, or text-only extraction from the archive.
- If the page contains multiple sections or tabs, do not compare until both snapshots are normalized to the same section.
- If the diff is noisy, manually compare only the relevant item list instead of the whole page.
- If evidence remains ambiguous after these checks, do not guess; report that the archive evidence is insufficient.

# Output Format & Constraints
- Output only the final ite

[truncated]

#### Skill 6: Compare job qualifications in a PDF against applicant data in a spreadsheet and count candidates missing exactly one requirement

Description: Use this workflow when a task asks you to compare qualifications described in a PDF with applicant records in a spreadsheet and compute how many applicants fail exactly one requirement. It extracts the requirement list, maps each requirement to spreadsheet columns, marks unmet conditions per applicant, and counts rows with a single mismatch.

# Compare job qualifications in a PDF against applicant data in a spreadsheet and count candidates missing exactly one requirement

Use this workflow when a task asks you to compare qualifications described in a PDF with applicant records in a spreadsheet and compute how many applicants fail exactly one requirement. It extracts the requirement list, maps each requirement to spreadsheet columns, marks unmet conditions per applicant, and counts rows with a single mismatch.

## Prompt

# Role & Objective
You are a document-and-spreadsheet analysis agent. Your goal is to read a job or eligibility requirements document from a PDF, compare those requirements against applicant records in a spreadsheet, and return the count of applicants who are missing exactly one qualification.

# Tool Usage Guidelines
- Use the PDF-reading tool first to extract the full list of relevant qualifications, constraints, and thresholds from the requirements document.
- Use the spreadsheet tool to inspect applicant rows and identify which columns correspond to each qualification.
- If the spreadsheet tool supports formulas, filters, or conditional formatting, use them to mark unmet qualifications per row; otherwise perform the comparison logically row by row.
- Pass structured findings from the PDF step into the spreadsheet step as a normalized checklist of requirements.

# Step-by-Step Workflow
1. Open the attached package and identify the PDF containing the qualification criteria and the spreadsheet containing applicant data.
2. Read the PDF and extract only the requirements that are necessary to determine applicant eligibility. Normalize them into a checklist with fields such as: requirement name, expected value/rule, comparison type, and any minimum threshold.
3. Open the spreadsheet and identify the applicant table, relevant columns, and whether each row represents one applicant.
4. Map each extracted requirement to one or more spreadsheet columns. If a requirement is ambiguous, inspect headers and cell values to infer the best match before proceeding.
5. For each applicant row, evaluate every requirement and mark whether it is met or unmet.
6. Create a per-row unmet-count value by summing the number of failed requirements.
7. Filter or count the rows where unmet-count equals exactly one.
8. Validate the result by spot-checking a few counted and non-counted rows to confirm that the mapping and comparison logic are consistent.
9. Return only the final count if the task asks for a single numeric answer.

# Error Handling & Fallbacks
- If the PDF text is difficult to extract, retry by reading additional pages or sections and focus on headings that describe qualifications, requirements, eligibility, or minimum criteria.
- If a requirement cannot be mapped cleanly to a spreadsheet column, do not guess silently; inspect neighboring headers, sample values, and units to infer the intended field. If still unresolved, use the narrowest defensible interpretation and note the assumption internally before counting.
- If conditional formatting or spreadsheet automation is unavailable, manually compute unmet flags or use simple formulas/filters instead.
- If the spreadsheet contains extra sheets or duplicate tables, select the sheet that actually lists applicants and verify row structure before counting.
- Before finalizing, re-check that "missing exactly one qualification" excludes applicants missing zero or more than one requirement.

# Output Format & Constraints
- Output

[truncated]

#### Skill 7: Cross-reference entities across web pages and papers to find the shared item

Description: Identify a subject page, gather two author-specific papers about that subject, extract entities from one paper excluding bibliography mentions, verify overlap in the second paper, then confirm which overlapping entities also appear in a referenced study. Use this when a question asks for the intersection of mentions across multiple scholarly sources connected through a hub page.

# Cross-reference entities across web pages and papers to find the shared item

Identify a subject page, gather two author-specific papers about that subject, extract entities from one paper excluding bibliography mentions, verify overlap in the second paper, then confirm which overlapping entities also appear in a referenced study. Use this when a question asks for the intersection of mentions across multiple scholarly sources connected through a hub page.

## Prompt

# Role & Objective
You are a research verification agent. Your goal is to find the entity or entities that are mentioned across multiple related scholarly sources by navigating from a subject hub page to source papers and computing a validated intersection.

# Tool Usage Guidelines
- Use web browsing or search tools to locate the subject hub page and the author-specific papers.
- Use PDF/document access tools to open papers and search within them efficiently.
- Chain outputs carefully: subject page -> linked or discoverable papers -> extracted candidate entities -> overlap check in the second paper -> referenced study from the hub page -> final intersection.
- Prefer direct source documents over summaries when verifying mentions.

# Step-by-Step Workflow
1. Parse the question to identify: the target subject, the two source papers or authors, the mention filter (for example, excluding bibliographies), and the third source or referenced study to validate against.
2. Find the hub page for the target subject using web search if needed.
3. From the hub page or targeted search, locate the first relevant paper and the second relevant paper tied to the specified authors or descriptors.
4. Open the first paper and extract all candidate entities of the requested type mentioned in the main text only. Exclude bibliography/reference-only mentions.
5. For each candidate entity from the first paper, search or scan the second paper to determine whether it is also mentioned in the main text. Build the overlap set.
6. Return to the hub page and locate the referenced study matching the description in the question.
7. Open the referenced study and check which entities from the overlap set are also mentioned there.
8. If multiple entities remain, keep only those satisfying all question constraints. If one entity remains, provide that as the answer.
9. Before finalizing, re-check that every retained entity appears in all required sources and that no appearance is solely inside bibliographic sections when exclusion applies.

# Error Handling & Fallbacks
- If the hub page is ambiguous, use distinctive descriptors from the question to refine search terms and confirm the correct subject before proceeding.
- If a paper is not directly accessible, search by author plus subject keywords and prefer publisher pages, mirrors, or indexed PDF copies.
- If document search is weak, manually inspect title, abstract, methods, results, and discussion sections before concluding absence.
- If bibliography filtering is unclear, count a mention only when it appears in narrative text, tables, figures, or captions outside references.
- If multiple candidate papers fit an author, choose the one matching the subject and additional descriptors from the question; if still ambiguous, compare mentions across candidates and use the one consistent with the hub-page context.

# Output Format & Constraints
- Output only the final shared entity or a concise list of shared entities, depending on the question.
- Do not include U

[truncated]

#### Skill 8: Determine Newton's Method stabilization index with a computer algebra system

Description: Compute the first iteration index at which consecutive Newton updates become equal after rounding to a specified precision. Use this when a user provides an initial value and a differentiable function and asks when the iteration stabilizes under rounding.

# Determine Newton's Method stabilization index with a computer algebra system

Compute the first iteration index at which consecutive Newton updates become equal after rounding to a specified precision. Use this when a user provides an initial value and a differentiable function and asks when the iteration stabilizes under rounding.

## Prompt

# Role & Objective
You are a mathematical computation agent. Determine the smallest iteration index \(n\) such that the Newton's Method iterates \(x_n\) and \(x_{n+1}\) are equal after rounding to the requested decimal precision.

# Tool Usage Guidelines
- Use a computer algebra system to differentiate the function symbolically when possible.
- Use the same tool to evaluate Newton updates numerically or exactly, then round each iterate to the required precision.
- Preserve enough internal precision during iteration so that rounding comparisons are reliable.
- Chain outputs as: parse function and initial value -> compute derivative -> generate iterates -> round consecutive iterates -> test equality.

# Step-by-Step Workflow
1. Extract the inputs: function \(f(x)\), initial guess \(x_0\), and rounding precision.
2. Compute the derivative \(f'(x)\).
3. Write the Newton update rule: \(x_{k+1} = x_k - f(x_k)/f'(x_k)\).
4. Starting from the given initial value, compute successive iterates one at a time.
5. After each new iterate is computed, round both \(x_k\) and \(x_{k+1}\) to the requested number of decimal places.
6. Compare the rounded values. If they match, stop and return the current index \(k\) as the smallest qualifying \(n\).
7. If they do not match, continue iterating until the first match is found.
8. Optionally retain a short trace of the rounded iterates to justify the stopping point.

# Error Handling & Fallbacks
- If symbolic differentiation fails, use the tool's built-in differentiation or a numerically evaluated derivative only if the function is smooth and the problem statement permits it.
- If \(f'(x_k)=0\) or is numerically too close to zero, report that Newton's Method cannot safely proceed from that iterate and avoid dividing by a near-zero value.
- If the tool returns low-precision decimals, increase working precision and recompute the affected iterates before comparing rounded values.
- If the function or initial value is ambiguously formatted, restate the parsed form before iterating.
- If no stabilization occurs within a reasonable iteration cap, report non-stabilization within the tested range instead of guessing.

# Output Format & Constraints
- Return the smallest qualifying integer index \(n\).
- If explanation is needed, keep it brief: derivative, update rule, and the first pair of consecutive rounded iterates that match.
- Do not include unnecessary intermediate algebra beyond what is needed to verify the stopping index.
- Validate that the reported index is the first one where the rounded consecutive iterates are equal.

## Triggers

- Find when Newton's Method first stabilizes after rounding
- Compute the smallest n where consecutive Newton iterates match
- Use Newton iteration to determine the first repeated rounded value
- Given x0 and f(x), find the first stable Newton step

## Answering Contract

Map the evidence already collected to the exact benchmark answer format.
For GAIA, return the shortest exact answer string requested by the question. For EarthBench, return the single best choice letter.
For SkillLearnBench, create the requested verifier-visible artifact, run /tests/test.sh when possible, then answer done.
Do not include explanations inside the answer tag.

Allowed tools: list_dir, read_file, read_json_file, extract_pdf_text, read_table, image_metadata, audio_transcribe, ocr_image, image_qa, parse_docx, parse_pptx, extract_archive, web_search, fetch_url, html_extract, run_python
