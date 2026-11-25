---
name: ui-page-portfolio
description: "A portfolio (a person's or a studio's work: developer, designer, photographer, writer, studio): the job for each kind, the skeleton with a wireframe, selected work as case studies, entries that carry the facts, one built from a GitHub account with real data, about and contact, a CV as a page and a PDF, photography portfolios, image weight, search for a person's name, and the generic developer look to avoid. Read before building or reworking one."
---

# Portfolio

The generated portfolio greets instead of showing: "Hi, I'm X" with a
waving hand, a job title, skill bars, repository cards with a star count on
each, a dark page in monospace. The work is the page. A portfolio is judged
in its first screen by one question: what does this person make, and is it
good? Answer it with the work, not with a greeting. One kind of page: the
measures (container, grid, spacing, type) are in `ui-layout`, and each part
it uses has its own `ui-part-*` skill. Start from this skeleton, then cut
and reorder for the content.

## 1. The job, by kind

| Kind | Judged by | The work shown as | First screen |
|---|---|---|---|
| Developer | what they built, and how well | projects: what each does and for whom, a screenshot or a real command and its output, links to the source and the live thing | the claim, the first projects beginning |
| Designer | how they think, and the craft | three to six case studies (section 3), large images of the real work | the claim and the first case study's image |
| Photographer | the photographs | series, full-bleed and in sequence, words small and few (section 7) | a photograph; the name small in the header |
| Writer | the writing | pieces with the publication, the date and one line, linking to the published text | the claim (subjects, where published) and the latest pieces |
| Studio | its judgement, and results | projects as decisions (`ui-reference-studio`); clients named only with permission | the claim and the first entry |

## 2. Skeleton

1. Header: the name, three links at most, the one contact link
   (`ui-part-header`).
2. First screen: a claim that says what this person makes, specifically,
   and the work beginning in the same screen (`ui-part-hero`: "claim and
   proof side by side", "statement over the work" or "index first").
3. The work: the strongest three to eight pieces, led by the best. Each with
   its name, what it is for someone who has not seen it (two plain
   sentences), one concrete detail, and its evidence: a screenshot, a
   photograph, a short real example of it in use. Group them by what they do
   when there are many ("Agents", "Automation", "Game tools"), not by
   language or date (`ui-part-sections`).
4. About: three to five sentences in the first person with specifics: where,
   what they work on, what they care about in the work. A real photo if one
   is given.
5. Contact: the email as a link (or a placeholder), and the profiles that
   exist.
6. Footer: one line (`ui-part-footer`).

The header sticks and stays slim so it does not crop the work, and a page of
projects runs long, so it has a back-to-top control
(`ui-part-back-to-top`).

```
│ [Name]                                    Work   Writing   Contact │ sticky
│ The claim: what this person makes, for whom,                       │
│ its consequence in the muted colour.  [City] · [open to, if given] │
│ Agents (a group's heading)                                         │
│ [screenshot from its README]    Lead project: two plain sentences, │
│ [with a caption            ]    one concrete detail.               │
│                                 Go · 2026 · Source · Live site     │
│ name       one line on what it does                 Rust · Source  │
│ name       one line on what it does                   Go · Source  │
│ All 16 repositories on GitHub                                      │
│ About: three to five sentences            [photo, when given]      │
│ [your email] · GitHub · LinkedIn                      [Name], 2026 │
```

## 3. Selected work as case studies

- For designers, studios and anyone whose work needs its reasoning: a page
  per project (`/work/<slug>`), linked from its entry on the index.
- In order: the title and the outcome in one line; a row of facts (client
  or context, role, when, team, tools or medium, links); the problem and
  its constraints; the decisions, each with its reason and shown (a
  sketch, a before and after, the shipped screen); the result, what
  shipped and what changed, with numbers only when real and permitted; the
  next project. Captions say what each image shows and why it matters.
- Team work says who did what ("I led the research and the booking flow;
  [Name] built the front end"). Work under NDA says so and shows what is
  allowed; never an invented stand-in.

## 4. Entries that carry the facts

- Each entry: the name as the link, what it is and for whom in one or two
  plain sentences, and a meta line with the facts that help a decision (the
  stack or medium, the year, the role); links named for where they go
  ("Live site", "Source", "Case study").
- The lead ones larger with their evidence, the rest compact rows
  (`ui-part-sections` section 5); one image ratio per group, screenshots in
  their own ratio, never cropped through the interface (`ui-part-images`).
- A dead live link or a demo behind a sign-in says so ("Archived, source
  only") rather than leading nowhere.

## 5. Built from a GitHub account

- Read each chosen repository's README, not only its one-line description:
  that is where what it does, how it works and its screenshots are. Use the
  README's own images (screenshots, diagrams) as the evidence, taken from
  the repository; when it has none, a short real usage example from the
  README (the command that installs or runs it) in a code block.
- Choose; do not list everything. Forks, empty repositories, dotfiles,
  configuration and abandoned experiments stay out. Four to eight projects,
  grouped by what they do.
- Rewrite each description for this page in plain words; do not paste the
  repository's tagline.
- The lead projects (one to three) show an image when their README has one:
  a screenshot or a diagram, with a caption. The rest are compact rows.
- Stars, followers and language counts are not content. A star count may sit
  in a project's meta when it would impress a stranger (hundreds); a table of
  how many repositories use each language never.
- The chosen projects are written into the page. The repositories left out
  are one link ("All 16 repositories on GitHub"), not a second list of their
  one-line descriptions fetched at load time.
- Repository creation dates are not a career history: there is no timeline
  unless the user gives one.
- Anything about the person beyond GitHub (email, employer, history, photo)
  is a visible placeholder until the user gives it. The placeholder reads as
  one ("[your email]"); how to fill it in goes in the README, never as a note
  on the page.
- Start from the pinned repositories (the person chose them) and the facts
  the API gives, fetched at build time and written into the page, never
  from the browser on load (60 requests an hour without a token, and a
  token in the page is a leaked secret):

  ```sh
  # Public repositories and their facts, no token (add &page=2 past 100).
  curl -s "https://api.github.com/users/<login>/repos?per_page=100&sort=pushed" |
    jq '.[] | select(.fork | not) | {name, description, language, stargazers_count, pushed_at, homepage, archived}'
  # The pinned ones, through GraphQL (needs a token: gh auth login).
  gh api graphql -f query='query { user(login: "<login>") { pinnedItems(first: 6, types: REPOSITORY) {
    nodes { ... on Repository { name description url homepageUrl stargazerCount primaryLanguage { name } } } } } }'
  ```

- Copy the README's images into the site's own assets and optimise them; a
  relative path in a README resolves to
  `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>`. Check
  that each `homepage` still answers before calling it the live site. No
  invented metrics: downloads or users only from a real source (the npm,
  PyPI or crates.io API), with the date.

## 6. About, contact and the CV

- The about adds where they are and their time zone when given ("Based in
  Bandung, UTC+7") and what they are looking for, in their words; no skill
  bars or list of thirty technologies (the tools show in the projects).
  Availability only when the user states it, as a dated line ("Taking on
  one project from March 2026"), never a pulsing dot.
- Contact: the email as a visible `mailto:` link people can read and copy;
  the profiles that exist, named; a form only when it sends somewhere real
  and says what happens next (`ui-page-form`).
- The CV as a page (`/cv`): roles with dates in one format, education,
  selected work linking to its entries, in headings, lists and `time`
  elements, with a print stylesheet (no header, navigation or footer; one
  column, black on white). The PDF is printed from that same page at build
  time so the two never drift (Playwright's `page.pdf({ format: "A4" })`),
  linked with its type and real size: "CV (PDF, 90 KB)". Employers, dates
  and degrees only from the user.

## 7. Photography

- The photographs are the design: full-bleed or large on a quiet ground,
  near-white or near-black (a mid-grey wall reads dull on screen, and
  `preview` reports it), with the words small and few.
- Series as sequences: a page per series in the photographer's order, each
  photograph whole in the full view, never cropped through its frame; an
  index of series with one cover each. Grids in one ratio, or justified
  rows that keep each photograph's own ratio.
- A lightbox is a modal dialog: arrows, Escape, swipe, a counter ("3 of
  12"), the caption, the photograph in the URL; each thumbnail a link that
  works without script (`ui-part-images` section 6).
- Captions give the place, the year, the client or publication when given;
  alt text says what is seen. Export in sRGB, strip GPS from the metadata,
  and skip right-click blocking: it stops nobody.

## 8. Weight and speed

- The first image is the LCP element: `fetchpriority="high"`, never lazy;
  every other image `loading="lazy"` with its width and height, `srcset`
  and `sizes`, AVIF or WebP from a pipeline (`ui-part-images` section 3).
- Thumbnails under about 40 KB, the lead image under about 200 KB, the
  full-size file only when the lightbox opens it; a video as a poster with
  `preload="none"`, an embed loaded on a click. Long galleries take
  `content-visibility: auto` with `contain-intrinsic-size` per series, so
  rows off screen are not rendered. LCP under 2.5s on a mid-range phone
  (`frontend-performance`).

## 9. Search for a person's name

- The home page's `title` carries the name and what they make, 50 to 60
  characters ("[Name], [what they make] in [city]"); each case study its
  own title and description; one `h1` per page.
- JSON-LD `Person` on the home page, real values only, `image` only for a
  real photo (`frontend-seo`):

  ```html
  <script type="application/ld+json">
  {"@context": "https://schema.org", "@type": "Person", "name": "[Name]",
   "url": "https://[domain]/", "jobTitle": "[Role]", "sameAs": ["https://github.com/[login]"]}
  </script>
  ```

- A domain of their own as the canonical URL; the profiles link back to it
  (GitHub's website field, LinkedIn), with `rel="me"` on links to profiles
  that verify it (Mastodon). An Open Graph image of 1200 by 630 with the
  name and a piece of real work; static HTML and a `sitemap.xml`.

## 10. The default to avoid

The generated developer portfolio: a dark page, monospace for everything
technical, one amber or green accent, a name with a coloured full stop, a
64px avatar, a claim and a "See the projects" button, "Selected work /
About / Contact" as hairline lists with a star count on every row, a
language table, and a "Built with" footer. Dark with monospace can be right
for a developer, but as a decision a concept asks for (a page that reads
like a well-made manual, with real command output as its images), not as the
starting point. The terminal costume goes with it: a fake terminal as the
hero, a typing effect, `>` prompts and `~/about` paths as labels, neon green
on black, glitch text; only when the person's own concept is a terminal.

## Check it

- `preview` at 360, 768 and 1440px: at 360px the claim and the start of the
  work in the first screen; the header sticks and the long page has its
  back-to-top control; no repeated-block report (the lead projects
  have room, the rest are rows); no image without alt; no code past the edge.
- Follow every link: sources, live sites, case studies, the CV's PDF.
- Every star count, language and date matches the API at build time;
  nothing is invented; each placeholder is listed in the report.
- Lighthouse on mobile for the home page and the heaviest gallery; the
  JSON-LD through validator.schema.org.

## Avoid

A greeting as the headline; a job title in its place; skill bars and
percentages; every repository listed, forks included; star counts on every
row and a language table; descriptions pasted from repository taglines; a
timeline made of creation dates; invented clients, metrics or availability;
stock or generated photos of the person; a photograph cropped through its
frame; a lightbox that lets focus escape or ignores Escape; a 4000px
original scaled down in CSS; a contact form that sends nowhere.
