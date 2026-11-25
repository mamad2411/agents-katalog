---
name: updating-robe-skills
description: Create or update AI skills in the RISC OS build environment without modifying the installed /etc copies directly. Use when a user wants to revise an existing build-environment skill, create a local working copy of a skill, derive a new skill from an existing one, create a brand new local skill for this environment, or use the `ai skill new` and `ai skill show` workflow. Prefer this skill over generic skill-creation guidance when the request is specifically about skills for this RISC OS build environment or local skill directories such as `/user/.config/ai/skills`. Always ask the user which route they want before making any skill changes.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(ai:*)
---
# Updating build-environment skills

Use this skill when working on AI skills for the RISC OS build environment and the goal is to edit skills safely in a project or user-controlled location, not to modify `/etc/agentskills` in place.

This includes requests such as:

* "Create a new skill called ..."
* "Add a local skill under `/user/.config/ai/skills`"
* "Update that RISC OS environment skill"
* "Make me a variant of an installed skill"

If the request is specifically about a skill for this environment, use this skill before falling back to a generic skill-creation skill.
The generic skill-creation skill may still be useful in providing testing and verification of the skill which has been updated or created.

The `ai skill ...` and `ai skills ...` command forms are aliases. Treat them as
equivalent, and focus on the order of operations instead.

## Start by asking

Before making any skill changes, ask the user which workflow they want:

1. Create a local shadow copy of an existing installed skill with `ai skill new <name>` and edit that copy.
2. Create a brand new skill with `ai skill new <name>`, and `ai skill show <name>` to display where this skill has been created.
3. A new skill structure in the local directory.

Do not silently choose one of these paths if the user has not already made it clear.

If the user has already made the route clear, proceed without asking again. For example:

* "Create a new skill called X" means workflow 2.
* "Update this installed skill" means confirm whether they want a local shadow copy or an explicit in-place edit.
* "Put it in `/user/.config/ai/skills`" means workflow 2 in that location.

## Rules

* Never edit files under `/etc/agentskills/` directly unless the user explicitly asks for that. Do not offer the user an option - they must request it.
* Prefer creating or updating skills in the working directory when the user is experimenting, drafting, or reviewing changes.
* Never delete an existing local skill directory in order to refresh it from `/etc/`. Local skills may already contain important changes that must be preserved.
* If a local shadow skill already exists, update that local skill in place. Do not overwrite it with a fresh copy from `/etc/`.
* Do not copy files from `/etc/agentskills/<skill-name>/` into an existing local shadow skill unless the user explicitly asks for a manual merge of a specific file. Files may have been intentionally removed from the local skill during a refactor.
* If you are creating the first local shadow of an installed skill, create it with `ai skill new <skill-name>` rather than manually copying files from `/etc/agentskills/`.
* After creating the first local shadow with `ai skill new <skill-name>`, inspect the generated shadow and ensure it contains everything needed to shadow the installed one completely.
* Preserve the original skill name and frontmatter only when the user is making a local copy of the same skill. If they are deriving a new skill, give it a new name and description.
* Keep the copy close to the original unless the user asked for a rewrite.
* The skill will be read by agents who do not have access to the sources that you are working from, so references to code or documentation in local files must not be used.
* If URLs are given, check with the user whether these are public URLs to include, or private ones for information.
* Unless a skill is intentionally repository-specific, keep it generic.
    * Do not add wording such as "in this repository", references to the current checkout, or paths that only make sense in one source tree.
    * Do not use references to files which may not be accessible to other users. Core RISC OS Build Environment files (like help, skills and headers) are fine.
    * Public URL references are ok, but URLs that might be on intranets should be avoided unless explicitly advised to record them.
* If the useful guidance is specific to one project or test layout, either:
  * put it in a deliberately repository-specific skill, or
  * generalise the rule so that it applies outside the current checkout.
* Before changing an existing generic skill, check whether the new note is really domain guidance or only a lesson from the current repository. If it is only repository-local, it does not belong in the generic skill.
* Put documentation and explanatory material in `references/`. Put concrete reusable files such as templates, source examples, headers, test scripts, and other non-documentation resources in `assets/`.
* Progressive disclosure within the skills is vital to ensure that the agents are not overwhelmed by irrelevant (and expensive) detail.
* If bundled example files only make sense when restored to a specific tree layout, preserve that layout inside `assets/`. For example, if a file must end up as `testcode/s/foo` or `testcode/hdr/bar`, prefer `assets/testcode/s/foo` and `assets/testcode/hdr/bar` over renamed stand-alone files.
* When a skill bundles such assets, say explicitly in `SKILL.md` where those files must be copied in the destination tree. Do not make the next agent infer the mapping from renamed files.
* Skills have restrictions set by https://agentskills.io/specification :
    * name must be lower case, 1-64 characters (try to use names like 'writing-foo', 'creating-foo', 'deploying-foo', etc), and must match the directory name.
    * description must by 1-1024 charaters and should describe what it does, and have triggers for when to use it.
    * metadata.author should be set to the author's name.
    * reference files (markdown which will be followed by the agent) should go in the `references` directory.
    * reference filenames should be all lowercase.
    * reference files should only be one level deep from `SKILL.md`.
    * assets (templates, examples files and snippets) should go in the `assets` directory
    * scripts (things that the skill might run) should go in `scripts`.
    * `SKILL.md` should be under 5000 tokens; under 500 lines. This is advisory, not a hard limit.
    * name and description metadata should be around 100 tokens, as they are loaded at startup.
* Skills should use progressive disclosure where possible - split into references and assets as necessary.
* If there is a common workflow, place the workflow itself towards the top of the document, as an ordered list.
* If there are prerequisites that must be know, place them at the top of the document.

## Workflow 1: Create a local shadow of an installed skill

Use this when the user wants a proposed update, review copy, or local variant of an existing skill.

1. Read the installed skill and related resources which will be changed from `/etc/agentskills/<skill-name>/*`.
2. Check whether a local shadow skill already exists.
3. If no local shadow exists, run `ai skill new <skill-name>` to create the shadow, then use `ai skill show <skill-name>` to locate it.
4. Inspect the generated shadow before editing it.
5. If a local shadow already exists, update that local skill in place and do not recopy the `/etc/` files over it.
6. Apply only the requested changes to the local copy.
7. Tell the user that the installed skill was left unchanged.

Do not run `show` before `new` when creating a skill for the first time. A
failed `show` in that situation means the skill does not exist yet, not that
the command form is wrong.

This route is the safest default for suggested skill improvements.

## Workflow 2: Create a brand new skill with `ai skill new`

Use this when the user wants a genuinely new skill rather than a variant of an existing one, or when they want an updated version which replaces the system skill.

1. Confirm the skill name.
2. Run `ai skill new <skill-name>` and then use `ai skill show <skill-name>` to find where the skill is stored.
3. Read the generated skeleton.
4. Fill in the frontmatter and body with concise instructions.
5. If the generated skill includes extra placeholder content, remove what is not needed.

If you are unsure what `ai skill new` generated, inspect the created files before editing them.
If the skill has not been created yet, do not expect `ai skill show <skill-name>`
to succeed beforehand.

Do not keep the old skill name if the new skill has a different purpose.

## Editing guidance

* Keep `description` explicit about what the skill does and when to use it. Any SWI and Service names may help to identify the skill's use.
* Add only information that would help another agent perform the task.
* Prefer local copies and small changes over rewriting long skills from scratch.
* If the change is just a few notes, patch the local shadow skill rather than regenerating everything.
* When updating an existing local shadow skill, treat the local files as the source of truth. Merge carefully; do not replace them wholesale from the installed skill.
* Be especially careful when updating an existing generic skill from a project task. It is easy to accidentally leak repository-specific assumptions into guidance that should stay broadly reusable.
* When revising bundled resources, check whether they are documentation or concrete artefacts and place them under `references/` or `assets/` accordingly.

## Validation

After editing a working-tree skill:

1. Re-read the frontmatter for accuracy.
2. Check that the copied skill still matches the intended workflow.
3. State clearly whether the result is:
   * a local copy of an installed skill, or
   * a newly created skill.

Use the relevant skill validation or display commands to confirm the file has valid metadata.
