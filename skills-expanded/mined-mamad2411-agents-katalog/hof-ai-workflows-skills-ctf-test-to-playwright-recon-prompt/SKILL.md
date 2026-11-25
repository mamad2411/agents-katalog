# CTF Test To Playwright Recon Prompt

You are running recon for a test-only Java Selenium to Playwright BDD migration.

## Objective

From hof-e2e-auto-tests, discover and report all source assets needed to run the ctf-test-to-playwright skill for one service.

Recon must produce strict traceability for like-for-like migration:
- scenario -> step phrase -> step definition -> StepLib method -> page object method -> test data reference
- include all in-use items; do not report only high-level candidates.

This recon step is discovery-only.
Do not edit target repositories.
Do not propose CI, CD, Drone, secrets, auth, or infrastructure changes.

## Inputs

Required:
- UI_SERVICE_FOLDER (example: hff, lmr, eta)

Optional:
- UI_FEATURE_FILE (example: hff.feature)
- SOURCE_FEATURE_GLOB_OVERRIDE

## Path Resolution

Resolve HOF_REPO_ROOT from current working directory:
- If ./ai/ctf-migration exists, use .
- Else if ../ai/ctf-migration exists, use ..
- Else stop and report: Unable to resolve HOF_REPO_ROOT from current working directory

Set:
- SOURCE_E2E_REPO_ROOT=${HOF_REPO_ROOT}/hof-e2e-auto-tests
- SOURCE_FEATURES_ROOT=${SOURCE_E2E_REPO_ROOT}/Function/src/main/resources/features/ui
- SOURCE_STEP_LIB_ROOT=${SOURCE_E2E_REPO_ROOT}/Function/src/main/java/uk/gov/ho/domain/component/ui/stepLib
- SOURCE_PAGE_OBJECTS_ROOT=${SOURCE_E2E_REPO_ROOT}/Function/src/main/java/uk/gov/ho/domain/component/ui/pages
- SOURCE_TEST_DATA_ROOT=${SOURCE_E2E_REPO_ROOT}/Function/src/main/resources/test-data/applicant-data

Feature selection precedence:
1. If SOURCE_FEATURE_GLOB_OVERRIDE is set, use it.
2. Else if UI_FEATURE_FILE is set, use ${SOURCE_FEATURES_ROOT}/${UI_SERVICE_FOLDER}/${UI_FEATURE_FILE}
3. Else use ${SOURCE_FEATURES_ROOT}/${UI_SERVICE_FOLDER}/**/*.feature

## Recon Steps

1. Feature inventory
- Enumerate selected feature files.
- Parse tags, Background, Scenarios, Scenario Outlines, and Examples.
- Capture scenario names and key step phrases.

2. StepLib inventory
- Enumerate candidate StepLib files in SOURCE_STEP_LIB_ROOT.
- Identify step definition files/classes that implement selected feature step phrases.
- Identify StepLib methods actually invoked by those step definitions.
- Record method signatures and a short behavior summary.

3. Page object inventory
- Enumerate service page objects under ${SOURCE_PAGE_OBJECTS_ROOT}/${UI_SERVICE_FOLDER}.
- If shared/common page objects are referenced by selected StepLib methods, include them.
- Record class names, key methods, and usage hints.

4. Test data inventory
- Locate service test data files under SOURCE_TEST_DATA_ROOT.
- Record CSV or other data files referenced by selected StepLib or scenario flows.
- Treat test data as source reference only.

5. Initial mapping seed
- Create a mapping from source scenario steps to step definitions, StepLib methods, and page object methods.
- Group implementation into deterministic migration batches.
- Flag ambiguous or unresolved mappings.

## Output Format

Return sections in this strict order:

1. RECON_SUMMARY
- service_name
- resolved_source_repo_root
- resolved_feature_glob
- feature_file_count
- scenario_count
- step_phrase_count
- step_definition_class_count
- step_definition_method_count
- candidate_steplib_class_count
- candidate_steplib_method_count
- candidate_page_object_count
- candidate_test_data_file_count

2. FEATURE_INVENTORY_TABLE
- file
- scenario
- type (scenario or outline)
- tags
- key_steps

3. STEP_LIB_INVENTORY_TABLE
- file
- class
- method
- signature
- behavior_summary
- mapping_confidence (high, medium, low)

4. STEP_DEFINITION_INVENTORY_TABLE
- file
- class
- method
- step_phrase
- calls_steplib_methods

5. PAGE_OBJECT_INVENTORY_TABLE
- file
- class
- method
- behavior_summary
- referenced_by_steplib

6. TEST_DATA_INVENTORY_TABLE
- file
- format
- likely_used_by
- notes

7. INITIAL_SOURCE_TO_IMPLEMENTATION_MAPPING_TABLE
- scenario
- source_step_phrase
- source_step_definition_method
- candidate_steplib_method
- candidate_page_object_method
- status (mapped, ambiguous, unresolved)
- notes

8. RISKS_AND_AMBIGUITIES

9. RECOMMENDED_MIGRATION_BATCH_ORDER
- Batch each group by coherent behavior slices.

10. STRICT_PARITY_INPUT_CHECK
- unmapped_scenarios
- unmapped_step_phrases
- unmapped_step_definition_methods
- unmapped_steplib_methods
- unmapped_page_object_methods
- decision: PASS or FAIL
- remediation

## Handoff Contract To Migration Skill

The recon output is the required input pack for ctf-test-to-playwright.
At minimum, the migration skill must receive:
- feature file inventory
- step definition inventory
- associated StepLib methods
- associated page objects
- associated test data references
- initial mapping table with ambiguity notes

If required source inputs are missing, stop and list missing inputs explicitly.
