---
name: skillx-gaia-global-skill
description: Global one-shot skillx skill library injection for gaia executor smoke
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
  source_method: skillx
  source_dir: <SOURCE_DIR>
  disclosure: global_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  no_instance_memory_guidance: light_generation_prompt_only
  generated_at: '2026-05-20T12:38:39Z'
---

## Method Skill Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Use this skill as ordinary prompt context. Apply the relevant method skill below before choosing tools.
Read the actual task prompt, choices, local files, and prior tool observations. Keep concrete values tied to the current task.
You may call tools while evidence is missing. When the answer is ready, output it directly in the benchmark answer format.

Allowed tools: list_dir, read_file, read_json_file, extract_pdf_text, read_table, image_metadata, audio_transcribe, ocr_image, image_qa, parse_docx, parse_pptx, extract_archive, web_search, fetch_url, html_extract, run_python

### Method Skill Library

#### Skill 1: plan-if-we-assume-all-articles-published-by-nature-in-2020-articles-only-not-book-rev

Description: If we assume all articles published by Nature in 2020 (articles, only, not book reviews/columns, etc) relied on statistical significance to justify their findings and they on average came to a p-value of 0.04, how many papers would be incorrect as to their claims of statistical significance? Round the value up to the next integer.

# step 1: Identify the target publication set from the question: the venue, time window, and which publication types count. This defines exactly what must be counted.
# step 2: Use the publication’s official archive or search interface to filter to the requested year and include only the allowed publication type. Record the total count of qualifying papers.
# step 3: Translate the assumed average p-value into the error-rate fraction requested by the problem, then multiply that fraction by the paper count. This gives the estimated number of papers treated as incorrect under the task’s assumption.
# step 4: Round the result upward to the next integer and return that value. This matches the required output format.

#### Skill 2: plan-in-unlambda-what-exact-charcter-or-text-needs-to-be-added-to-correct-the-followi

Description: In Unlambda, what exact charcter or text needs to be added to correct the following code to output "For penguins"? If what is needed is a character, answer with the name of the character. If there are different names for the character, use the shortest. The text location is not needed. Code:

`r```````````.F.o.r. .p.e.n.g.u.i.n.si

# step 1: Look up a concise reference for the esoteric language’s syntax so you can identify how output strings are encoded.
# step 2: Find a canonical example program that prints text, because matching against a known-valid pattern is the fastest way to spot structural mistakes.
# step 3: Read the example closely to infer the role of the repeated syntax markers that precede each output character.
# step 4: Compare the given program against that pattern by counting the repeated output literals and the required structural markers.
# step 5: Identify any mismatch between those counts to determine the single missing token needed to make the program well formed.
# step 6: Return the missing token in the format requested, using the shortest standard name if it is a character.

#### Skill 3: plan-the-attached-spreadsheet-shows-the-inventory-for-a-movie-and-video-game-rental-s

Description: The attached spreadsheet shows the inventory for a movie and video game rental store in Seattle, Washington. What is the title of the oldest Blu-Ray recorded in this spreadsheet? Return it as appearing in the spreadsheet.

# step 1: Open the attached spreadsheet and locate the rows for the requested media format so the search is limited to the relevant inventory subset.
# step 2: Inspect the release-year field within that subset and identify the earliest year to determine which entry is oldest.
# step 3: Match that earliest year back to its corresponding title row so the correct item is selected.
# step 4: Return the title exactly as written in the spreadsheet to preserve the source formatting.

#### Skill 4: plan-how-many-studio-albums-were-published-by-mercedes-sosa-between-2000-and-2009-inc

Description: How many studio albums were published by Mercedes Sosa between 2000 and 2009 (included)? You can use the latest 2022 version of english wikipedia.

# step 1: Identify the subject entity and open the authoritative reference page specified by the task so you work from the intended source.
# step 2: Navigate to the discography section and locate the subsection that lists the relevant release type so you exclude unrelated works.
# step 3: Scan the release years in that subsection and keep only entries whose dates fall within the requested interval.
# step 4: Count the filtered entries and report the total so the answer matches the requested category and time range.

#### Skill 5: plan-the-object-in-the-british-museum-s-collection-with-a-museum-number-of-2012-5015-

Description: The object in the British Museum's collection with a museum number of 2012,5015.17 is the shell of a particular mollusk species. According to the abstract of a research article published in Science Advances in 2021, beads made from the shells of this species were found that are at least how many thousands of years old?

# step 1: Search the museum collection database by the provided museum number and open the matching object record to identify the specimen’s species. This anchors the rest of the lookup to the exact collection item.
# step 2: Verify the species’ currently accepted scientific name in an authoritative taxonomy source if the museum record may use an older synonym. This prevents missing later literature indexed under a revised name.
# step 3: Search for a research article from the specified journal and year using the accepted species name plus terms related to shell beads or ornaments. This narrows results to the relevant paper about archaeological finds from that species.
# step 4: Open the matching article and read the abstract for the minimum reported age of the beads. The abstract usually states the age directly in the units needed for the answer.
# step 5: Return only the age value in the requested scale after converting formats if needed. This keeps the final response aligned with the question’s wording.

#### Skill 6: plan-in-july-2-1959-united-states-standards-for-grades-of-processed-fruits-vegetables

Description: In July 2, 1959 United States standards for grades of processed fruits, vegetables, and certain other products listed as dehydrated, consider the items in the "dried and dehydrated section" specifically marked as dehydrated along with any items in the Frozen/Chilled section that contain the whole name of the item, but not if they're marked Chilled. As of August 2023, what is the percentage (to the nearest percent) of those standards that have been superseded by a new version since the date given in the 1959 standards?

# step 1: Open the historical standards document and isolate the subset of entries that match the task’s inclusion rules across the relevant sections, because the final denominator depends on that filtered list.
# step 2: Build a checklist of the qualifying product names exactly as they appear in the document, including any related entries from the secondary section that satisfy the name-match rule and excluding entries barred by the task.
# step 3: For each checklist item, locate the official current standards page or linked standard document for that product, because only the authoritative current record can show whether the standard was revised.
# step 4: Compare the effective or issue date of the current standard with the date shown in the historical document, and mark the item as superseded only if a newer version exists.
# step 5: Repeat the same date check for every qualifying item and keep a running count of total items and superseded items, because the task asks for a percentage over the filtered set.
# step 6: Compute the superseded share from those counts and round to the nearest whole percent before reporting.

#### Skill 7: plan-using-the-biopython-library-in-python-parse-the-pdb-file-of-the-protein-identifi

Description: Using the Biopython library in Python, parse the PDB file of the protein identified by the PDB ID 5wb7 from the RCSB Protein Data Bank. Calculate the distance between the first and second atoms as they are listed in the PDB file. Report the answer in Angstroms, rounded to the nearest picometer.

# step 1: Locate the authoritative structure record or attached data file for the requested identifier so you work from the correct source artifact.
# step 2: Obtain the plain structure file in the expected format so it can be parsed programmatically.
# step 3: Load the file with the requested scientific parsing library so atom records are interpreted reliably rather than by manual text slicing.
# step 4: Iterate through the parsed atoms in file order and capture the first two listed atoms so the calculation matches the task’s ordering requirement.
# step 5: Compute the distance between those two atom coordinates using the library’s atom/coordinate operations so the measurement is taken in the file’s native spatial units.
# step 6: Round the result to the precision requested by the question and report it with the required unit so the final output matches the expected format.

#### Skill 8: plan-use-density-measures-from-the-chemistry-materials-licensed-by-marisa-alviar-agne

Description: Use density measures from the chemistry materials licensed by Marisa Alviar-Agnew & Henry Agnew under the CK-12 license in LibreText's Introductory Chemistry materials as compiled 08/21/2023.

I have a gallon of honey and a gallon of mayonnaise at 25C. I remove one cup of honey at a time from the gallon of honey. How many times will I need to remove a cup to have the honey weigh less than the mayonaise? Assume the containers themselves weigh the same.

# step 1: Find the referenced source table in the specified chemistry material and extract the densities of the two substances at the stated temperature, so the comparison uses the required authority.
# step 2: Convert the initial container volume and the repeated removal amount into the same volume unit, so mass changes can be computed consistently from density.
# step 3: Write the mass of each container’s contents using density times volume, treating only one substance’s volume as decreasing after each removal.
# step 4: Set an inequality where the remaining mass of the repeatedly reduced substance becomes less than the fixed mass of the other substance, then solve for the required number of removals.
# step 5: Round the result up to the next whole removal, because the mass must be strictly below the comparison value after a complete removal step.

## Answering Contract

Map the evidence already collected to the exact benchmark answer format.
For GAIA, return the shortest exact answer string requested by the question. For EarthBench, return the single best choice letter.
For SkillLearnBench, create the requested verifier-visible artifact, run /tests/test.sh when possible, then answer done.
Do not include explanations inside the answer tag.

Allowed tools: list_dir, read_file, read_json_file, extract_pdf_text, read_table, image_metadata, audio_transcribe, ocr_image, image_qa, parse_docx, parse_pptx, extract_archive, web_search, fetch_url, html_extract, run_python
