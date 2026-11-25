---
name: ktl-website
description: 'Build a browsable website for the `.lokf/` knowledge bundle that ktl-sidecar installed in this repository: a Hugo site in `website/`, with a page per concept and its trust label, a health page, a knowledge graph, search by trust and type, and the four `lokf export` files served beside the pages. It finds the README, the docs, the changelog, the figures, a LinkML schema, retellings and a federated workspace by itself, with no setting, and is deployed to GitHub Pages by a workflow. Use when: someone asks to publish, browse, present or deploy the knowledge bundle; wants a website, a docs site or GitHub Pages for it, or one to replace an mkdocs site; or asks to repair or update a site this skill installed. Not for writing or confirming concepts; that is ktl-librarian and ktl-curator. Not for installing the bundle itself; that is ktl-sidecar, which runs first. Keywords: website, GitHub Pages, Hugo, documentation site, knowledge graph, LinkML, gen-doc, Datasette, OKF, LOKF, trust ladder.'
license: Apache-2.0
compatibility: 'Requires a `.lokf/` sidecar from ktl-sidecar 0.30.0 or later (its `knowledge-report.sh`, and a committed `uv.lock`), uv, git, a POSIX shell (bash; Git for Windows on Windows) and python3 or uv for placeholder substitution. No Node.js. Step 5''s workflow is GitHub Actions and GitHub Pages; on another forge the host publishes the site folder''s `dist` itself.'
---

# ktl-website

Install a **website** for the knowledge bundle in the repository this skill is invoked from. It is a Hugo site under `website/`, built from the bundle and from whatever else the repository holds, with a workflow that publishes it to GitHub Pages. Every file is copied from `templates/` (paths below are relative to this skill's directory), never retyped. The site shows a page per concept with the trust label `knowledge-report.sh` gives it, a health page, a knowledge graph, and search that filters by trust and type. It serves the four files `lokf export` writes under `/knowledge/`, so the repository becomes a producer node for the bundle's IRIs.

> Model: a small or mid-tier model is enough here: Step 1 copies templates and substitutes placeholders, and Step 0 is structured file lookup. Mistakes are caught by Step 3's grep, Step 4's build and Step 6's hand-off.

## What the site finds by itself

No setting names what the site shows: the build looks for each of these and shows what it finds.

| The repository has | The site shows |
| --- | --- |
| `.lokf/knowledge/` | the bundle's pages, the health page and the graph (required) |
| `README.md` | the home page; without one, the bundle's own introduction |
| `SPEC.md` | the Specification page |
| `docs/**.md` | the Guide part, a page per file |
| `docs/<page>.<language>-simple.md` | a retelling, which `docs/<page>.md` offers above its title |
| `docs/architecture.md` | the home page's Architecture button |
| `src/<name>/schema/<name>.yaml`, at the root or under `.linkml/`, or the file `site.toml`'s `schema` names | the Schema part, written by LinkML's `gen-doc`, and the home page leads with the schema |
| `.lokf/schema/domain.yaml`, else LOKF core: `.lokf/schema/lokf.yaml` or the `lokf` package's copy | with no schema of the repository's own, the Schema part shows the bundle's domain vocabulary or LOKF core, and the home page does not lead with it |
| `CHANGELOG.md` | a page per release |
| `.assets/` | the figures |
| `.lokf/ingest.lock.yaml` | a mirrored source's origin, on its concept's card |
| `.github/workflows/knowledge-federation.yaml` | the workspace, on the graph page |

The home page has five buttons on every site: the schema, the bundle, the architecture page, the glossary and the quick start. One whose page is not there is greyed, never linked. [references/inputs.md](references/inputs.md) gives the rule for each input.

## Scope

- **This skill** runs **once**, to install the site, or again to **repair** or **update** it: copy each template over a copy that is missing or differs. It writes nothing into the bundle, the README, the docs or the changelog.
- **ktl-sidecar** runs first: the site builds from the sidecar's scripts and toolkit. **ktl-librarian** and **ktl-curator** change what the pages say.

> Guardrails: three files are the repository's own once written, and a repair never replaces them: `website/site.toml`, `website/README.md` and `website/assets/css/custom.css`. A `website/` that is not this skill's is never written into: the site goes in `ktl-website/` instead, as *The site's folder* below says. Stop when the sidecar's preflight reports the bundle unhealthy, and send that to ktl-sidecar or ktl-librarian first. Deployment is GitHub Actions and GitHub Pages; elsewhere, [references/deploy.md](references/deploy.md) says what the host does itself.

## The site's folder

The site's folder is `website/`. A folder is this skill's when it holds `site.toml` and `hugo.toml`. The preflight's `website` line settles which folder this run uses, and every step below means that folder where it says `website/`. The first line that holds decides:

- `website/` is this skill's: the site is there. Repair or update it.
- `ktl-website/` is this skill's: the site is there, since `website/` was another site's when the skill first ran. Repair or update it, and leave `website/` alone.
- `website/site.config.mjs` exists: it is this skill's earlier Astro site. Move it to Hugo in place, as Step 1 says.
- `website/` exists: it is another site's. Install into `ktl-website/`.
- Neither folder exists: install into `website/`.

The workflow and the sidecar's sync look in both folders, so neither needs to be told.

## Step 0: gather the facts

**First, the preflight.** Run `bash scripts/website-preflight.sh <repo-root>` from this skill's directory and read its screen. It runs the sidecar's own preflight inside it, then says whether another publisher holds the repository's Pages, the address Pages serves the site at, which folder the site goes in, which of the inputs above the site will find, and whether an mkdocs site is there to replace. Its last line names what is missing and which steps that disables; repeat that line in the Step 6 hand-off. When the person cannot act on a `missing` or `warn` line, write them a request note from [references/prerequisites.md](references/prerequisites.md).

Resolve every placeholder from real sources before writing anything; never leave a `<...>` token behind.

| Placeholder | Meaning | Where to find it |
| --- | --- | --- |
| `<REPO_OWNER>` | the repository's owner on GitHub, as its address spells it | `git remote get-url origin`: the part before the repository name (`noelmcloughlin` in `github.com/noelmcloughlin/ai-linkmo`); the preflight's `git` line prints both |
| `<REPO_NAME>` | the repository's name on GitHub | the same remote, after the owner, without `.git` |
| `<SITE_URL>` | the site's address, ending in `/` | the preflight's `address` line ([references/deploy.md](references/deploy.md#a-custom-domain-a-user-site-or-a-private-site)) |
| `<PROJ_NAME>` | the project's human-readable name, which is the site's title | the bundle's `index.md` `title` without "Knowledge Bundle", the README's `#` title, or a manifest `name` |
| `<PROJ_DESC>` | one sentence, the site's description | the bundle's `index.md` `description`, the quoted `>` line of `llms.txt`, or the README's first sentence |

`<REPO_OWNER>` and `<REPO_NAME>` come from the remote, never from a person's name; the sidecar's `<OWNER_SLUG>` is a different thing. Give `<PROJ_NAME>` and `<PROJ_DESC>` as plain text on one line: Step 1 escapes them for TOML.

**When the site replaces an mkdocs site**, which the `mkdocs` line names, read `mkdocs.yml` once, by eye, for the values [references/deploy.md](references/deploy.md#reading-mkdocsyml) lists.

## Step 1: install the site

```bash
cp -R <this skill>/templates/website website && mv website/gitignore website/.gitignore
```

Only two files carry placeholders: `website/site.toml` and `website/README.md`. Substitute them through Python, never through sed:

```bash
export REPO_OWNER REPO_NAME SITE_URL PROJ_NAME PROJ_DESC
python3 -c '
import json, os, re, sys
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    for token in ("REPO_OWNER", "REPO_NAME", "SITE_URL", "PROJ_NAME", "PROJ_DESC"):
        value = os.environ[token]
        if not value.isprintable():
            sys.exit(token + ": line break or unprintable character")
        if token == "SITE_URL" and not re.fullmatch(r"https?://[^\s\x22\\<>]+/", value):
            sys.exit("SITE_URL: not an http or https address ending with /")
        if path.endswith(".toml"):
            value = json.dumps(value, ensure_ascii=False)[1:-1]
        text = text.replace("<" + token + ">", value)
    open(path, "w", encoding="utf-8").write(text)
' website/site.toml website/README.md
```

Then edit `website/site.toml` only for what the preflight settled: `branch` when the default branch is not `main`, and a logo when the person names one of the repository's own. Set `browse` only when the person asks to publish the data, whose databases become public. When the site replaces an mkdocs site, write the redirects and `docsExclude` entries that Step 0 read. Everything else is found, not set. [references/customising.md](references/customising.md) describes each value.

**Repair or update.** The preflight's `website` line names each file that differs from its template or is missing. Copy those templates over, one file at a time, and never the three files the repository owns.

**From the earlier Astro site.** With the person's agreement, carry the old `site.config.mjs` values into `site.toml` and remove the old files, as [references/customising.md](references/customising.md#from-the-earlier-astro-site) lists.

## Step 2: keep the repository's checks off the generated folders (add only)

The build writes `website/dist/`, `website/generated/`, `website/resources/`, `website/static/pagefind/` and `website/.venv/`, which `website/.gitignore` keeps out of git. A Markdown lint, link check or spell check that runs over `**/*.md` still reaches them locally. The preflight's `lint` line names the configurations. Add an exclusion for `website/(dist|generated|resources|\.venv)/` to each, as the skills repository's `lychee.toml` and `.markdownlint-cli2.jsonc` do, and nothing else at the root. If the repository runs Dependabot, suggest the `uv` entry for the site's folder from [references/deploy.md](references/deploy.md) in one line; do not add it unasked.

## Step 3: verify

```bash
grep -n -e '<REPO_' -e '<SITE_' -e '<PROJ_' website/site.toml website/README.md
```

No match means every placeholder is resolved. The build refuses a `site.toml` that still holds one.

## Step 4: build

```bash
bash website/scripts/build.sh
```

The script runs `scripts/prepare.sh` (`lokf export` and, for a schema, `gen-doc`, both from `.lokf/`'s own environment, and the report script), then Hugo and Pagefind, which uv installs from PyPI at the versions the site's `uv.lock` holds, then the raw-HTML cleaning and a check of every link between the pages. It needs the network once. Where PyPI or the CDN is blocked, [references/deploy.md](references/deploy.md#behind-a-proxy) says what to set.

`bash website/scripts/build.sh serve` serves the site at `http://localhost:1313/`, under `baseURL`'s path, and rebuilds it on each edit. Commit `website/`. With no uv, report the build as skipped: the workflow builds in CI.

## Step 5: install the deploy workflow (optional)

Skip this step when `.lokf/` is gitignored (the workflow builds from the checkout) or the repository is not on GitHub. Copy `templates/github/knowledge-website.yaml` to `.github/workflows/knowledge-website.yaml`. It builds the site on every pull request that touches its inputs and deploys nothing until the repository variable `KNOWLEDGE_WEBSITE_ENABLED` is `true`. Setting it, and the one-time switch of Pages to Actions, are the maintainer's: give the two commands from [references/deploy.md](references/deploy.md), and do not run them. When the preflight's `pages` line warned of another publisher, install the workflow all the same and say that the variable stays unset until that publisher is retired.

## Step 5b: retire mkdocs (the maintainer's)

When the preflight's `mkdocs` line found `mkdocs.yml`, this site replaces it, and the build's link check has followed every redirect Step 1 wrote. Retiring mkdocs changes Pages and deletes a branch, so give the maintainer the list in [references/deploy.md](references/deploy.md#retiring-mkdocs) and run none of its Pages or branch steps. With the maintainer's agreement, put the list's file changes on the site's branch. Say once that the pull request preview is lost.

## Step 6: hand off

Tell the person:

- which folder the site is in, and why when it is `ktl-website/`;
- which Step 0 values were **guessed** rather than found (`<PROJ_DESC>` above all);
- whether Step 4's build ran and passed, or was skipped, and its last line (`check-links: N pages, 0 broken link(s)`);
- which parts the site found (README, docs, retellings, changelog, figures, schema, workspace, mirror records, data), and which home buttons are greyed and what file would light each;
- what was left alone: another site's `website/`, the lint configurations, Pages and the variable;
- when the site replaces an mkdocs site or an Astro one, the values carried over and the steps that are still the maintainer's;
- the preflight's last line, as printed;
- that the site serves the four `lokf export` files at the site's address under `knowledge/`, so that address is a candidate `base_iri` for the bundle when its current one is a placeholder or a code-host URL (ktl-librarian's Rule 2 has the migration);
- that the next ktl-librarian run reads the site folder's `README.md` as the source for a playbook concept.
