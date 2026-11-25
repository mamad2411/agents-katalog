---
name: get_doc
version: 1.0.0
license: MIT
---

# get_doc

Fetch the full markdown of one of the 4 published documents via
`host.fetchOrigin("/docs/<name>.md")`.

## Arguments

- `name` (string, required): one of `rfc-skills-in-llms-txt`,
  `ext-executable-skills`, `ext-skill-attestations`, `mcpwasm-readme`.

## Returns

`{ name, length, truncated, content }`.

- `content`: the markdown body, truncated to 4000 chars.
- `length`: the size of the **document**, as declared by the origin. It is not
  the length of `content`, and it is not the length of what the sandbox
  received — the host caps every `fetchOrigin` response, so measuring the body
  would report the cap (4096) for every document above it.
- `truncated`: whether `content` is partial. When it is, read the rest with
  `search_spec`, or fetch the document directly if you can.

## Example

```json
{ "name": "ext-executable-skills" }
```