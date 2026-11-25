---
name: social-snippet
description: Generate LinkedIn, Twitter/X, and Threads post snippets from ArtStroy article frontmatter. Produces UTM-tagged copy ready for human review and posting.
---

# Social Snippet Generator

Each published article needs ready-to-paste social copy for the Distribution Manager to post or hand off for human posting.

## When to Run

- After `post-publish-check` passes and the `live` label is applied
- Invoked by the Distribution Manager as part of the syndication workflow
- Re-run only if frontmatter changes post-publication (rare)

## Input: What to Read

From the article's frontmatter (located at `src/content/articles/{slug}/index.mdx`):

| Field | Used for |
|---|---|
| `title` | Headline in all snippets |
| `description` | Supporting copy (Twitter extended, LinkedIn body) |
| `category` | Hashtag set selection |
| `authors` | Attribution line (LinkedIn only) |
| `publishedTime` | Not used in copy; for Distribution Manager's records |

Also read the article's first H2 or first 2 sentences of body for a "hook" — the sharpest insight or surprising claim.

## Platform Output Specifications

### Twitter/X

**Format:**
```
{hook — max 200 chars}

Full article 👉 https://artstroy.net/{slug}?utm_source=twitter&utm_medium=social

{hashtags — max 4}
```

**Rules:**
- Total tweet ≤ 280 characters including URL
- Hook must be the article's sharpest claim, not the title
- No filler phrases: "Great new article", "Check this out", "Just published"
- URL always has UTM: `utm_source=twitter&utm_medium=social`

**Hashtag sets by category:**
- `pentesting`: `#Pentesting #OWASP #WebSecurity #InfoSec`
- `programming`: `#Programming #TypeScript #WebDev #JavaScript`
- `technology` / `qa`: `#QualityAssurance #TestAutomation #QA #SoftwareTesting`

---

### LinkedIn

**Format:**
```
{title}

{2–3 sentence adapted summary — professional tone, first-person plural ("we", "teams", "developers")}

{key takeaway as a bullet or bold line}

Full article: https://artstroy.net/{slug}?utm_source=linkedin&utm_medium=social

{hashtags — max 5, mix broad and niche}
```

**Rules:**
- 150–400 characters ideal (LinkedIn algorithm rewards mid-length)
- Avoid em-dashes in bulk; LinkedIn renders them oddly on mobile
- No clickbait ("You won't believe..."); lean professional and specific
- End with the link, not mid-post (reduces algorithmic suppression)
- Hashtags at bottom, not inline

**Hashtag sets by category:**
- `pentesting`: `#Pentesting #WebSecurity #OWASP #CyberSecurity #AppSec`
- `programming`: `#Programming #JavaScript #TypeScript #WebDevelopment #SoftwareEngineering`
- `technology` / `qa`: `#QualityAssurance #TestAutomation #SoftwareTesting #QA #DevOps`

---

### Threads

Same content as Twitter/X variant — Threads is character-equivalent but allows slightly longer threads.

If article content warrants it (e.g., a listicle or step-by-step guide), split into a 2-post thread:
- Post 1: hook + URL
- Post 2: top 3 points as bullets (no URL repeat)

---

## Output Format

Post all three snippets as a comment on the current syndication issue:

```markdown
## Social Snippets — /{slug}

### Twitter/X
```
{tweet text}
```

### LinkedIn
```
{linkedin post text}
```

### Threads
```
{threads text}
```

---
*Snippets generated {date}. Review before posting — adjust hook if the article changed after initial draft.*
```

## Quality Checks Before Posting

- [ ] Twitter snippet ≤ 280 characters
- [ ] All links contain UTM parameters
- [ ] Hook is specific — could only describe THIS article, not a generic tech post
- [ ] No platform-specific formatting leaking across platforms (e.g., LinkedIn hashtags in tweet)
- [ ] Category hashtag set matches the article's `category` frontmatter field

## What to Avoid

- Rephrasing the title as the hook ("This article covers X" when the title is already X)
- Hashtag stuffing beyond platform limits
- Posting UTM-tagged links on Hashnode (canonical must stay clean — this is a Distribution-Manager-level distinction, but snippets for social are always UTM-tagged)
