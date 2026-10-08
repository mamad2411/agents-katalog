---
name: garden-capture
description: Capture a thought, decision, learning, or fact into the garden vault inbox. Use ONLY when the user explicitly asks: "capture X", "remember that X", "for the garden Y", "save this", etc. Do not capture proactively — the user wants to approve what lands in the vault. Writes to ~/garden/inbox/: the gardener will file it properly later.
---

# garden-capture

Drops a raw capture into `~/garden/inbox/`. The gardener (scheduled) processes inbox files into properly-filed atomic notes.

## When to use

Only when the user explicitly invokes capture. Triggers: "capture this", "save that", "for the garden", "remember X", or equivalents.

If you notice something in conversation that *seems* noteworthy but the user didn't ask to capture, do **not** write to `inbox/`. Suggest it inline ("worth capturing?") and let the user decide. The vault is the user's, and they want explicit control over what goes in.

## How

1. Compose a short markdown file with this structure:

```markdown
---
type: capture
created: <YYYY-MM-DD>
source: <session | manual | conversation>
---

# <one-line summary>

<the content: keep it raw, gardener will refine>

Context: <project | person | topic if known>
```

2. Filename: `~/garden/inbox/<YYYY-MM-DD>-<slug>.md`. Slug = first 5–7 words of the summary, lowercased, hyphenated.

3. Write the file. Don't edit anything else in the vault: that's the gardener's job.

4. Tell the user one line: "Captured to inbox as `<filename>`."

## Multiple captures

If the user dumps several distinct things at once, write each as a separate inbox file. One concept per file.

## Don't

- Don't file directly into `notes/`, `decisions/`, etc.: that's gardener territory.
- Don't add wiki-links speculatively. Gardener handles linking.
- Don't ask for permission for routine captures. Just write.
