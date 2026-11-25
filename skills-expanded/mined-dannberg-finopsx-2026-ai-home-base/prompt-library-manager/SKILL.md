---
name: prompt-library-manager
description: Save and manage prompts that worked well. Triggers on phrases like "save this prompt", "add to prompt library", "this is a keeper", "remember this prompt". Captures the prompt with metadata (use case, model version, what it's good at, what to watch for) so it can be retrieved and reused later.
---

# Prompt Library Manager

When the user says "save this," capture the prompt that just worked. Most prompt libraries fail because saving is annoying — this skill makes it a one-line operation. The metadata gets generated for the user; they only need to confirm.

## Inputs to confirm before starting

- The prompt to save (default: the most recent one the user ran)
- A short name for it (default: generate a slug from the use case)
- Anything specific the user wants noted (e.g., "this version of the prompt only works with extended thinking on")

## Steps

1. **Identify the prompt.** Pull the most recent prompt the user ran, unless they specify a different one. Confirm with the user before proceeding.

2. **Generate metadata.** Auto-fill these fields based on context:
   - **Name**: kebab-case slug from the use case
   - **Use case**: one sentence describing what the prompt is for
   - **Inputs needed**: the specific values the prompt template requires
   - **Model used**: which AI model the user was running when this worked
   - **Model version date**: today's date, since model behavior shifts
   - **Output format**: what the prompt produces
   - **Watch for**: known failure modes — what does this prompt get wrong sometimes

3. **Suggest tags.** Based on the use case, suggest 2–4 tags from the existing taxonomy. If the existing tags don't fit, propose a new tag.

4. **Confirm with user.** Show the full entry to the user, ask to confirm or edit.

5. **Save to the library.** Write to `Prompts/<name>.md` with the metadata frontmatter and the prompt body. If a file with that name exists, suggest a versioned name (`<name>-v2.md`) and ask which to use.

## Saved prompt format

```markdown
---
name: <slug>
use_case: <one-sentence description>
tags: [tag1, tag2]
inputs_needed:
  - <input 1>
  - <input 2>
model_tested: <model name and version date>
last_validated: <date>
watch_for:
  - <known failure mode 1>
  - <known failure mode 2>
---

# <Use case as a heading>

<The prompt itself, exactly as it was written>
```

## House rules

- Don't save a prompt without "watch for" notes. Every prompt has failure modes; if the user says it has none, push back and ask when it's ever produced unexpected output.
- Don't save a prompt without a model and date. Model behavior shifts; a prompt that worked great in a previous version may degrade or improve. The library needs to track this.
- Update `last_validated` whenever the user reuses a saved prompt and confirms it still works. This keeps the library honest about what's actually in use vs. theoretically saved.
- If the user is saving a prompt they iterated on (3 turns of refinement), save the final version as the prompt and note the iteration history in `watch_for` — what made earlier versions fail.

## Library hygiene

Run a check every quarter (or when the user runs this skill with the `--audit` flag): for each prompt in the library, ask the user:

- Have you used this in the last 90 days?
- Is it still producing good output?
- Has the model changed since `last_validated`?

Archive anything that hasn't been used in 6 months to a `Prompts/archive/` subfolder. The library should reflect what the user actually uses, not what they once thought they'd use.

## Why this skill exists

The single biggest difference between a practitioner who's good at AI and one who isn't is whether they have a prompt library. Most don't, because saving prompts feels like overhead. This skill makes the saving frictionless and the metadata automatic, which is the only way the library actually grows.

Treat the library as a real asset — it's the part of your AI workflow that compounds.
