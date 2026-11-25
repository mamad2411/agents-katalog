---
name: evoskill-gaia-global-skill
description: Global one-shot evoskill skill library injection for gaia executor smoke
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
  source_method: evoskill
  source_dir: <SOURCE_DIR>
  disclosure: global_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  no_instance_memory_guidance: light_generation_prompt_only
  generated_at: '2026-05-20T06:22:00Z'
---

## Method Skill Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Use this skill as ordinary prompt context. Apply the relevant method skill below before choosing tools.
Read the actual task prompt, choices, local files, and prior tool observations. Keep concrete values tied to the current task.
You may call tools while evidence is missing. When the answer is ready, output it directly in the benchmark answer format.

Allowed tools: list_dir, read_file, read_json_file, extract_pdf_text, read_table, image_metadata, audio_transcribe, ocr_image, image_qa, parse_docx, parse_pptx, extract_archive, web_search, fetch_url, html_extract, run_python

### Method Skill Library

#### Skill 1: analyze-chess-diagram-for-best-move

Description: Use this skill when a task shows a chess position as an image and asks for the best, winning, or next move, requiring reconstruction of the board and conversion of the chosen move into correct standard algebraic notation.

## When to use
- The task includes a chessboard image and asks for the best move, winning move, or next move.
- The side to move must be inferred from the prompt or verified from the position.
- Success depends on reading piece locations from the diagram rather than from text.
- The answer must be given in standard algebraic notation.

## Procedure
1. Inspect the image and determine board orientation. Identify which corner squares correspond to light and dark colors, and map ranks/files from the correct perspective.
2. Read every visible piece onto a mental or written board using `<square>` coordinates. Confirm kings, major pieces, pawns, and any promoted or ambiguous pieces.
3. Verify the side to move from the prompt. If unclear, infer cautiously from the position and state any uncertainty internally before proceeding.
4. Generate legal candidate moves for the moving side. Reject any move that leaves its king in check or depends on a misread square.
5. Evaluate forcing ideas first: mate threats, direct checks, winning captures, promotions, skewers, pins, forks, and unavoidable material gain.
6. Select the strongest legal move that satisfies the task goal, preferring a forced win over a merely good move.
7. Convert the move to SAN: use piece letter or pawn notation, include capture markers, destination square, promotion, check/checkmate, and disambiguation when required.
8. Perform a final legality and notation check against the reconstructed position before answering with only `<best move>`.

## Notes / caveats
- Do not assume the board is shown from one side's perspective; verify coordinates from the square colors and layout.
- Distinguish visually similar pieces carefully, especially bishops vs pawns and queens vs kings in small images.
- SAN must match the move type exactly; include `x`, `+`, `#`, `=` and disambiguation only when justified.
- If image quality is poor, re-check critical squares involved in the final tactic before committing.

#### Skill 2: applicant-qualification-gap-check

Description: Use this skill when a task includes a requirements document and a structured applicant table and asks you to map qualifications to fields, evaluate each applicant, and identify rows that miss exactly a specified number of criteria.

## When to use
- You have a requirements document plus a spreadsheet or table of applicants.
- The task asks for a count or list of applicants who fail exactly <threshold> qualification(s).
- Qualifications must be extracted from prose and matched to differently named table columns.
- You need a repeatable audit trail showing which criterion each applicant fails.

## Procedure
1. Read the requirements document and rewrite each qualification as a checklist item with a clear pass/fail rule. Split only genuinely distinct subconditions.
2. Inspect the applicant table and map each checklist item to the relevant column or combination of columns using a qualification-to-column mapping.
3. Normalize wording and coding differences. Translate categorical values, abbreviations, blanks, and implicit encodings into comparable values.
4. Evaluate each applicant row against every checklist item. Record pass/fail per criterion in helper columns or an equivalent matrix.
5. Compute an unmet-criteria count for each row by summing failures across checklist items.
6. Filter or count rows where unmet-criteria count equals <threshold>.
7. Visually verify the result with conditional formatting, filters, or spot checks on flagged rows.
8. Recheck borderline cases where the requirement wording or table encoding is ambiguous before reporting the final count or list.

## Notes / caveats
- Avoid double-counting one qualification just because it appears across multiple fields.
- Treat missing data carefully; do not assume blank means fail unless the task context supports it.
- Distinguish mandatory qualifications from preferences or descriptive text in the source document.
- Review rows near the threshold manually, especially when a criterion depends on interpretation.

## Example
Extract a set of mandatory qualifications from an attached document, map them onto columns in an applicant sheet, create helper indicators for each unmet requirement, then count applicants whose total failure count equals <threshold>.

#### Skill 3: apply-referenced-equation-to-spreadsheet-row

Description: Use this skill when a task asks you to compute a numeric result from a named equation in an external paper or article using values from a specific row in an attached table or spreadsheet.

## When to use
- The task cites a paper, article, or reference source and asks for a value from a specific equation.
- The needed inputs live in one row of an attached spreadsheet or structured table.
- The main challenge is matching equation symbols to the correct columns before calculating.
- The output must include a computed number with specified rounding or formatting.

## Procedure
1. Open the cited source and locate the exact equation requested, including any note that it is the final, revised, or preferred form.
2. Transcribe the equation into working form using placeholders like `<var1>`, `<var2>`, and `<constant>`.
3. Define each symbol from the source itself; if any notation is ambiguous, consult a secondary reference and reconcile the meanings.
4. Open `<current file>`, find the target record `<current row>`, and confirm you have the correct row label or identifier.
5. Map each equation symbol to a specific column in that row, recording `<symbol> -> <column> -> <value>`.
6. Check units, scales, and whether any value is a rate, constant, concentration, or other quantity that could be confused.
7. Substitute the row values into the equation explicitly and compute the result with a calculator or equivalent tool.
8. Format the output exactly as requested, including rounding to `<current precision>` and reporting any applied rounding.
9. Sanity-check the result against the equation structure to catch swapped variables or impossible magnitudes.

## Notes / caveats
- Do not assume symbol meanings from modern conventions; verify them in the cited source.
- Distinguish similar quantities carefully, especially constants versus observed rates or inputs versus outputs.
- Confirm the selected row before calculating; nearby labels are easy to misread.
- If multiple equations appear, use only the one explicitly requested.

## Example
A task cites a historical scientific paper and asks for a derived value for one record in an attached spreadsheet. Read the paper, identify the requested equation, ground each symbol, map those symbols to columns in the target row, substitute the values, compute, and return the rounded result with a brief variable-to-column trace.

#### Skill 4: audit-standards-supersession-from-historical-list

Description: Use this skill when a task asks you to extract standards or item entries from a historical source, apply inclusion/exclusion wording rules, and determine how many were later superseded by official versions as of a target date.

## When to use
- The task provides a historical standards list, citation, or PDF and asks for a count or percentage of items later updated or superseded.
- You must include only entries from specified sections and apply exact wording filters such as including one qualifier but excluding another.
- You need to match historical item names to current official standards pages or documents.
- The output requires both item-level updated/not-updated judgments and an aggregate result.

## Procedure
1. Open the historical source and extract candidate entries from the specified section(s) in <current document>.
2. Apply the prompt’s inclusion and exclusion rules exactly; keep a structured table with <item name>, <historical citation>, and <historical date>.
3. Normalize each retained item name for searching, preserving meaningful qualifiers in a separate note such as <qualifier>.
4. Search official publisher or regulator sources for the best current page or PDF matching each item.
5. For each item, inspect the latest official version date or revision marker available as of <target date>.
6. Compare that official date/version to the historical source date and label the item as <updated> or <not updated>.
7. Record explicit evidence for each determination, including cases where no newer official version is found.
8. Compute the requested count or percentage from the final included set, then round only as instructed.

## Notes / caveats
- Prefer official standards pages or linked official PDFs over summaries or secondary sources.
- Do not merge near-duplicate items if qualifiers change the standard’s identity.
- Do not infer an update from a related item; mark <not updated> unless the exact item has a newer official version.
- Watch for section-specific wording traps, especially when the same base item appears under multiple forms.

## Example
Given a historical standards booklet, first isolate entries under one preservation method plus selected entries from another section that match a name rule. Then check each retained item against current official standards documents, classify each as updated or not updated by <target date>, and calculate the final percentage.

#### Skill 5: browse-faceted-library-catalog-for-metadata-outlier

Description: Use this skill when a task requires finding a specific record inside a repository or library discovery interface by browsing classification facets, applying metadata filters, and identifying an outlier record from interface cues before extracting a metadata value.

## When to use
- The target item is inside a repository, catalog, or discovery portal with browse facets or hierarchical classifications.
- The task specifies a taxonomy path, subject code, or browse hierarchy rather than a strong keyword query.
- You must narrow results with filters such as language, year, document type, or availability.
- The correct record is distinguished by an outlier cue such as an icon, source label, affiliation, or country indicator.

## Procedure
1. Open the target site <repository site>; use a search engine only to locate the entry point if needed.
2. Prefer the site’s browse or facet UI over free-text search when the prompt is classification-based.
3. Traverse the requested hierarchy <classification path> until you reach the target category.
4. Apply constraints one at a time, such as <language filter>, <date bound>, and <document type>, confirming each filter remains active.
5. Scan the reduced result set for visual or metadata outliers, including icons, source-country cues, institution names, or unusual labels.
6. Open the most likely record <candidate record> and inspect its detailed metadata.
7. Extract the requested field <target attribute> and normalize it to a concise value.
8. Cross-check that the record satisfies all constraints and is the unique best match before answering.

## Notes / caveats
- Treat icons and flags as hints, not proof; verify what they represent in the metadata.
- Do not rely on current ranking or counts alone; use the stated constraints, especially temporal ones.
- If multiple outliers remain, compare full record pages rather than summary cards.
- Repository pages may show origin indirectly through institution or source information instead of an explicit country field.

## Example
A repository task may require browsing to a specific subject class, filtering to a narrow language subset and time range, then finding the single record whose source cue differs from the rest and extracting the origin from its metadata page.

#### Skill 6: bruteforce-caesar-cipher-with-context

Description: Use this skill when a user mentions a Caesar cipher or provides a short phrase that looks like a simple rotational substitution and you need to brute-force all shifts, then pick the plaintext that best fits the prompt’s context.

## When to use
- The prompt explicitly says the text is a Caesar cipher.
- The user provides a short encrypted phrase with readable word boundaries and punctuation.
- You can enumerate all rotational shifts and need to choose the most plausible natural-language output.
- The prompt includes scenario clues that can help distinguish between several readable candidates.

## Procedure
1. Extract the ciphertext as `<ciphertext>` and note any contextual clues as `<context clues>`.
2. Use a trusted Caesar-decoding method to generate every shift for `<ciphertext>`; if no tool is available, compute all rotations manually or with built-in text processing.
3. Preserve spacing, punctuation, and capitalization as much as possible while reviewing outputs.
4. Scan the full candidate list instead of stopping at the first readable result.
5. Rank candidates by naturalness: prefer outputs that form coherent words, grammatical phrases, and a message consistent with `<context clues>`.
6. If multiple candidates look plausible, compare them against the user’s stated purpose, topic, or constraints and choose the strongest semantic fit.
7. Return the best plaintext and, if available, include the corresponding shift as `<shift>`.

## Notes / caveats
- Do not assume the first plausible decryption is correct; several shifts can look partly meaningful.
- Short ciphertexts are ambiguous, so context may matter more than raw word resemblance.
- Verify that the selected output is a complete coherent message, not just a few recognizable tokens.
- If no candidate is clearly natural language, say the result is uncertain and present the top options.

## Example
A short encrypted note is said to contain meetup instructions. Generate all Caesar shifts, review each candidate, and choose the one that reads like a natural instruction matching the described situation.

#### Skill 7: classify-botanical-vegetables-from-grocery-list

Description: Use this skill when a user asks to separate fruits and vegetables from a mixed food list using strict botanical correctness rather than culinary convention, especially when they want only the botanical vegetables returned in a specific format.

## When to use
- The user asks for fruits or vegetables from a mixed grocery or food list.
- The prompt emphasizes botanical accuracy, scientific classification, or excluding botanical fruits.
- The list contains mixed items such as produce, processed foods, animal products, seeds, spices, or grains.
- The user requests a formatted subset such as alphabetized, comma-separated output.

## Procedure
1. Read the request and identify the target category: `<botanical fruits>` or `<botanical vegetables>`.
2. Scan `<current list>` and discard items outside the requested produce classification task, such as animal products, processed foods, and other irrelevant pantry items.
3. For each remaining plant item, classify by plant structure, not culinary use: treat mature ovaries and related seed-bearing structures as fruits; treat roots, stems, leaves, and flower parts as vegetables.
4. Exclude seeds, nuts, grains, spices, or ambiguous plant products unless the user explicitly wants them considered within the fruit/vegetable split.
5. If the target is vegetables, remove any item that is botanically a fruit even if commonly called a vegetable.
6. Keep only items matching `<target category>` and format them as requested, such as `<alphabetized comma-separated list>`.

## Notes / caveats
- Do not rely on grocery-store categories or culinary habits.
- Treat common culinary vegetables conservatively; many are botanical fruits and should be excluded from a vegetable list.
- Herbs and leafy plant parts can count as vegetables when they are non-fruit plant tissue relevant to the user’s produce grouping.
- Follow the user’s formatting instructions exactly after classification.

## Example
Given a mixed shopping list, first remove non-produce items, then eliminate all seed-bearing plant structures if the user wants only botanical vegetables, then sort and return the survivors in the requested format.

#### Skill 8: compare-cohort-biographical-metrics-with-date-cutoff

Description: Use this skill when a task asks you to find an extremum among people in a defined cohort using biographical statistics that must be verified as of a historical cutoff date, possibly with eligibility-based exclusions.

## When to use
- The task asks for the least, most, earliest, or latest value among members of a named group.
- The compared value is a biographical statistic drawn from profile pages, infoboxes, or article text.
- The answer must be correct as of a past date rather than the current page state.
- Some cohort members may need exclusion based on rules like no qualifying participation or no recorded value.

## Procedure
1. Identify the target person or entity from the prompt or source material; if needed, infer it from an image or descriptive clue.
2. Find a reliable biography page for that person and extract the cohort or group membership.
3. Enumerate all members of the cohort from a reliable list or linked biographies.
4. For each member, inspect a source state matching <as-of date> when the task is date-sensitive; use revision history if available.
5. Extract the target metric from structured fields first, then verify with article prose if the value is missing, ambiguous, or potentially outdated.
6. Apply each exclusion rule explicitly, documenting why a member is excluded or retained.
7. Normalize all retained values into a common unit or format before comparing.
8. Select the qualifying member with the requested extremum and format the result as <name>; <normalized value>.
9. Record a brief audit trail covering cohort membership, dated metric verification, exclusions, and conversion.

## Notes / caveats
- Do not treat a missing structured field as zero; check the prose or corroborating sources.
- Prefer date-appropriate revisions for living people or frequently edited biographies.
- Normalize units before ranking; mixed formats can reverse the comparison.
- Separate "no qualifying event" from "unknown value" and justify exclusions clearly.

## Example
Start from a person identified in source material, derive their cohort from a biography, review date-appropriate versions of each cohort member's page, exclude members with no qualifying participation, convert the remaining statistics to one unit, and return the member with the minimum value plus the converted amount.

## Answering Contract

Map the evidence already collected to the exact benchmark answer format.
For GAIA, return the shortest exact answer string requested by the question. For EarthBench, return the single best choice letter.
For SkillLearnBench, create the requested verifier-visible artifact, run /tests/test.sh when possible, then answer done.
Do not include explanations inside the answer tag.

Allowed tools: list_dir, read_file, read_json_file, extract_pdf_text, read_table, image_metadata, audio_transcribe, ocr_image, image_qa, parse_docx, parse_pptx, extract_archive, web_search, fetch_url, html_extract, run_python
