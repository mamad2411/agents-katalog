---
name: magzdown
description: Turn markdown the agent produced into a Magzdown link the user can read as a typeset document. Use when the user asks to share, present, publish, or make readable a report, summary, PRD, review, or any document you wrote, or says "open in magzdown".
---

# Open in Magzdown

Magzdown renders markdown as a paginated, typeset document at a URL. The document is encoded in the URL itself, so there is no upload and no account. Use it when a human needs to read what you wrote, instead of pasting raw markdown or pointing at a `.md` file.

## When to use

- The user asks to share, present, or "make readable" a report, summary, PRD, research note, or code review you produced.
- The user says "open in magzdown" or "give me a magzdown link".
- You finished a long markdown document and the user will read it rather than edit it.

Do not use it for code, config, or short answers.

## Before you share

The document travels inside the URL, so the link is the document: anyone holding it can read the content, and it lands in browser history and in whatever chat it is pasted into.

- Ask the user before creating a link. Do not share on your own initiative.
- Refuse if the content carries secrets (keys, tokens, credentials), personal data, or anything the user marked confidential or proprietary. Say what you found and offer a redacted version instead.
- If you are unsure whether the content is shareable, ask rather than encode.

## Encoding

Spec: `shared/encode.md` in this repo, or https://www.magzdown.com/docs.

1. UTF-8 bytes of the markdown.
2. Prepend bytes `0x01 0x00`.
3. Base64, then `+` to `-`, `/` to `_`, strip `=` padding.
4. URL: `https://www.magzdown.com/open?md=<encoded>`

Check: markdown `# Hi` encodes to `AQAjIEhp`.

## Produce the link

Write the markdown to a file first (for example `report.md`), then run one of these.

Bash:

```bash
printf 'https://www.magzdown.com/open?md=%s\n' "$(printf '\x01\x00' | cat - report.md | base64 | tr '+/' '-_' | tr -d '=\n')"
```

Python:

```python
import base64, sys
md = open(sys.argv[1], encoding="utf-8").read()
enc = base64.urlsafe_b64encode(b"\x01\x00" + md.encode()).rstrip(b"=").decode()
print("https://www.magzdown.com/open?md=" + enc)
```

## Size guard

Check the file size before encoding. Over about 100 KB of markdown the URL may get truncated by a browser or proxy. If it is bigger, remove embedded base64 images, split the document into parts, or ask the user which section they want.

```bash
wc -c < report.md
```

## Hand it over

Give the user the URL as a markdown link with the document title as the text, for example `[Q3 infra review](https://www.magzdown.com/open?md=...)`. Say in one line what the link is. Do not also paste the full markdown; the link replaces it.
