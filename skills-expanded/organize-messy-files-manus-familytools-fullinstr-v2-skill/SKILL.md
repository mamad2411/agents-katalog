---
name: organize-messy-files-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for organize-messy-files using latest full-instruction v2 family injection.
allowed-tools:
  - document_batch_summary
  - document_keyword_score
  - document_text_extract
  - file_inventory
  - list_dir
  - make_dir
  - move_file
  - read_file
  - run_python
  - run_shell
  - search_text
  - write_file
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: Organize Messy Files

## When to use this skill
Use this skill for `organize-messy-files` tasks to sort and organize unstructured files (PDFs, PPTXs, DOCXs) into a specific folder taxonomy based on content. It is required when instructions demand reading document contents to determine categories and moving files without altering names or contents.

## Visible input and artifact inventory
Inputs include the instruction file and a directory of messy files. Expected artifacts are newly created folders corresponding to specified subjects, containing all original files moved based on content. No files should be left unorganized, and original names and contents must remain intact.

## Execution procedure for the current task
1. **Inventory Files**: Use `file_inventory` or `list_dir` to identify files to organize.
2. **Extract Taxonomy**: Read instructions to extract required folder names and categorization criteria.
3. **Create Folders**: Use `make_dir` to create the specified folders.
4. **Analyze Content**: Use `document_text_extract`, `document_batch_summary`, or `document_keyword_score` to determine each file's subject.
5. **Move Files**: Use `move_file` to relocate files to corresponding folders without dropping or altering data.
6. **Handle Edge Cases**: Place files that do not clearly fit primary categories into the designated fallback folder.

## Family tool routing and useful placeholder snippets
- **File Discovery**: `file_inventory` for a comprehensive list.
- **Folder Creation**: `make_dir` for taxonomy setup.
- **Content Analysis**: `document_text_extract` for text reading. Use `document_batch_summary` or `document_keyword_score` for bulk identification.
- **File Movement**: `move_file` for transferring files.
- **Automation**: Use `run_python` or `run_shell` to automate reading, scoring, and moving in bulk.

## Validation checks before final submission
- Verify all required folders exist with exact names.
- Ensure all original files are moved; confirm the original directory is empty of target files.
- Check a sample in each folder for correct categorization.
- Confirm no file names or contents were altered.

## Common failure modes and repair actions
- **Missing Folders**: Review instructions and use `make_dir`.
- **Uncategorized Files**: Re-evaluate content and move to appropriate or fallback folders.
- **Incorrect Categorization**: Use `move_file` to correct locations if scoring was inaccurate.
- **Altered Files**: Restore original files if possible and repeat moving carefully.

## Finalizer capsule
To ensure the minimum required artifact shape near the maximum step limit, verify all files are moved to designated folders. If unorganized files remain, move them to the fallback folder to ensure none are left out. Confirm the folder structure exactly matches the requested taxonomy.
