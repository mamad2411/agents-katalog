---
name: api-gif-generator
description: Prepare and execute authorized short GIF generation requests with the public GIF Cinema adapter, and report actual output and account/model limitations.
---
# API GIF Generator

Read the root gif-cinema skill's `references/generation.md` for the actual runtime
contract. Prefer `render` with a single-shot JSON when using still-image references.
Check currently available account/model support; a historical model label is not a
promise of access. Plan offline first, then use only the user's authorized bounded
call cap and start with `--retries 0`. Read OPENAI_API_KEY from the environment without
printing or saving it. Preserve unknown-outcome safety and do not create a new output
folder to bypass a pending request. Inspect the returned GIF before claiming success.
The story compiler prepares request inputs only; it never calls a provider itself.
