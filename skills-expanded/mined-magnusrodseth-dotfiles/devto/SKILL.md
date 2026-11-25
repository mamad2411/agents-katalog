---
name: devto
description: Publish and manage articles on Dev.to (Forem API) from local markdown, using the API key stored in 1Password. Use when the user wants to post, draft, update, publish, unpublish, or list their Dev.to articles, cross-post a blog post or vault note to Dev.to, or mentions dev.to, DEV Community, or the Forem API.
---

# Dev.to

Publish markdown to Dev.to through the Forem API. Authenticated as `magnusrodseth` (user id `3803258`).

The key lives in 1Password at `op://Private/Dev.to API Key/credential` on the personal account (`my.1password.eu`). **Never read it into a variable that gets printed, never paste it into a URL, never echo it.** `scripts/devto.sh` resolves it per call and keeps it out of stdout.

## The two rules that matter

**Draft first, always.** `published` defaults to `false`. Create the draft, hand the user the edit URL, let them read it rendered in Dev.to's own editor. Publishing is a separate command.

**Publishing is close to irreversible.** The Forem API has **no DELETE endpoint**. Once published, an article mints a public URL that gets crawled, cached and syndicated within minutes. `unpublish` hides it from the site but does not undo distribution. Treat `publish` as outward-facing: confirm explicitly with the user before running it, every time, even if they authorized a publish earlier in the session.

## Commands

```bash
S=~/.claude/skills/devto/scripts/devto.sh

bash $S whoami                              # verify auth
bash $S list [published|unpublished|all]    # your articles, id + title + state
bash $S get <id>                            # one article as JSON

bash $S draft <file.md> [--title T] [--tags "a,b,c"] [--description D] [--canonical URL]
bash $S update <id> <file.md> [same flags]
bash $S publish <id>                        # GATED: confirm with the user first
bash $S unpublish <id>                      # hide a published article
```

`draft` and `update` read the markdown file, strip any YAML frontmatter (see below), and send it as `body_markdown`. Both print the article id and both URLs on success.

## The frontmatter trap

Forem parses YAML frontmatter **inside `body_markdown`** and lets it override the JSON fields. Vault notes and blog posts almost always carry frontmatter with `type:`, `created:`, `tags:`, `related:` and other keys Forem does not understand, which produces a mangled post or a 422.

`scripts/devto.sh` strips a leading `---` block before sending. That is the correct default. If the user genuinely wants Forem-style frontmatter to drive the metadata, pass `--keep-frontmatter` and make sure the block contains only keys Forem accepts (`title`, `published`, `tags`, `series`, `cover_image`, `canonical_url`, `description`).

When publishing a vault note, the publishable text is usually only the part below a `---` separator partway down the file. Read the file and confirm what the article actually starts at rather than assuming the whole file is the post.

## Field rules

- `tags` on **write** is a comma-separated **string**, max **4** tags, lowercase alphanumeric only. On **read** the same data comes back as `tag_list`, an array. Do not send an array.
- `title` is required on create unless frontmatter supplies it.
- `description` is the social and SEO snippet. Keep it under about 150 characters.
- `canonical_url` points at the original when cross-posting, so the source keeps the SEO credit.
- `series` groups posts; a new string starts a new series.
- `main_image` is the cover image URL.

## Responses

`201` created, `200` updated, `401` bad or missing key, `422` unprocessable (usually a bad tag, a duplicate title, or frontmatter Forem could not parse). On `422` the body names the field, so print it rather than guessing.

Full schema, error shapes and less common fields: [REFERENCE.md](REFERENCE.md)

## Sponsored or client work

Dev.to requires disclosure on paid or sponsored posts. If the article is sponsored, confirm the disclosure is in the body before creating the draft, not after. An undisclosed sponsored post risks the account.
