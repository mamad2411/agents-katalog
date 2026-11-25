---
name: oss-discovery
description: Use when finding OSS on GitHub that fits a purpose and judging whether to adopt it. Always use for requests like "is there a library that does X?", "find me a tool for X", "should we adopt this library?", or "what are the alternatives to X". Runs four stages - check for a domain registry, narrow with gh search, evaluate real usage and health, then read the internals.
---

# Find OSS and judge whether to adopt it

## First: never send natural language straight to search

GitHub search is an AND search over keywords. A sentence returns nothing.

```bash
gh search repos "a tool that autocompletes SQL when you write in the terminal"   # 0 results
gh search repos --topic=sql --topic=cli --stars=">500" --archived=false          # hits
```

Always translate the request into topics, languages and numeric qualifiers before searching.

---

## Stage 1. Find

### Check for a domain registry first

If what you are looking for belongs to a specific domain (MCP servers, editor extensions, packages in a
particular ecosystem), that domain's registry beats GitHub search. **When you find a registry, treat it not
as a shortcut within stage 1 but as the output of a full pass through the workflow.**

```
Pass 1: target = "the means of searching this domain"
    Stages 1-3 identify the registry.
    Stage 4 clarifies its API and constraints.
    The output is the search mechanism itself.

Pass 2: target = what you actually wanted
    Stage 1 searches using the registry's API, then stages 2-4 as usual.
```

**Do not skip stage 4 and infer capabilities.** If an OpenAPI spec exists, read it. Writing "it should be
able to" is how you get it wrong.

### Package ecosystems are enumerable - never hardcode them

```bash
curl -s "https://packages.ecosyste.ms/api/v1/registries" \
  | jq -r '.[] | "\(.name)\t\(.ecosystem)\t\(.packages_count)"' | sort -t$'\t' -k3 -rn
# 100 registries: npmjs.org, proxy.golang.org, hub.docker.com, pypi.org, nuget.org,
# repo1.maven.org, packagist.org, crates.io, rubygems.org, nixpkgs, cocoapods.org, ...
```

Pick by `ecosystem`, then look the package up at `/api/v1/registries/<name>/packages/<pkg>`.

Known registries, measured 2026-09-19:

| Target | Registry |
|---|---|
| MCP servers | `registry.modelcontextprotocol.io/v0.1/servers` (official, publishes OpenAPI), `registry.smithery.ai/servers` (15,579), `api.mcp.github.com/v0/servers` (252, curated) - all keyless. **Glama and PulseMCP now need API keys; PulseMCP's keyless API returns 410** |
| Claude Code plugins and skills | `.claude-plugin/marketplace.json` in `anthropics/claude-plugins-official` (**310 entries** - the `plugins/` and `external_plugins/` directories hold only 53 of them), and `anthropics/skills` |
| Any package | the listing above, then ecosyste.ms (see stage 3) |

**Everything else: [references/registries.md](./references/registries.md)** - Kubernetes/Helm, CLI install
counts, ML models, IaC, editor extensions, containers, vulnerabilities, with endpoints and gotchas.
Check an endpoint is alive before building on it; `scripts/check-sources.sh` re-checks the whole set.

### Topic search alone misses a third of the field

GitHub Topics is opt-in, and the biggest repositories often skip it. Measured with
`gh api search/repositories` (`topics:0` against the same range):

| Range | No topics at all |
|---|---|
| `stars:>500` | **38.8%** (47,739 / 123,029) |
| `stars:>1000` | 34.3% |
| `stars:>10000` | 20.0% |
| `stars:>50000` | 14.6% |

Repositories with no topics include `anthropics/claude-code` (146k), `modelcontextprotocol/servers` (90k),
`openai/codex` (125k), `cline/cline` (69k), `torvalds/linux` and `python/cpython`. Worse are the ones with
the *wrong* topics: `jqlang/jq` is tagged `[jq]` alone - no `cli`, no `json`.

**So always union three queries.** Measured on MCP: 100 hits from topic search alone, **236 unique** from
all three, and only the second one returns `modelcontextprotocol/servers`.

```bash
gh search repos --topic=<t> --stars=">500" --archived=false --limit=100 --json fullName,stargazersCount
gh search repos "<phrase>" --match=name,description --stars=">500" --limit=100 --json fullName,stargazersCount
gh search repos "<kw>" --match=name,description --number-topics=0 --stars=">1000" --limit=50 --json fullName,stargazersCount
```

The third (`--number-topics=0`, the `topics:0` qualifier) deliberately fetches the set topic search
can never reach.

### With no registry, translate into vocabulary

| Element of the request | Translates to |
|---|---|
| The function in "a tool that does X" | Several `--topic=` values (GitHub Topics is a normalized vocabulary) |
| "in the terminal", "as a CLI" | `--topic=cli`, `--topic=terminal` |
| A stated or inferred language | `--language=` |
| "something solid", "the standard one" | `--stars=">500"` plus `--archived=false` |
| "something still usable" | `--updated=">(six months ago)"` |
| "something recent" | `--created=">(start of this year)"` |

**Split the vocabulary candidates across several queries and merge the results.** Do not try to land it in one.

When no names are known at all, search the web first to pick names out of blog posts and comparisons,
then confirm them on GitHub.

---

## Stage 2. Narrow

```bash
gh search repos --language=<lang> --topic=<topic> \
  --stars=">1000" --updated=">(six months ago)" --archived=false \
  --sort=stars --limit=20 \
  --json fullName,stargazersCount,license,pushedAt,description
```

**Always pass `--archived=false`.** Without it, repositories that stopped years ago dominate the top.

### Snowball the owners out of the results

Do not carry a list of well-known organizations; derive it from the search you just ran. Owners cluster,
and the cluster is exactly what topic search drops.

```bash
# 1. Which owner keeps coming up?
gh search repos "<phrase>" --match=name,description --stars=">500" --limit=50 --json fullName \
  | jq -r '.[].fullName' | cut -d/ -f1 | sort | uniq -c | sort -rn | head
#   14 modelcontextprotocol   <- far ahead of the rest

# 2. Search that owner directly
gh search repos --owner=modelcontextprotocol --stars=">100" --limit=30 --json fullName,stargazersCount
#   90455 servers   24340 python-sdk   13428 typescript-sdk   10913 inspector   7264 registry
```

Measured: step 2 added 10 repositories that none of the three stage-1 queries had found, `inspector`
(10,913 stars) among them. Works in any domain because the owner comes from the data, not from a list.

Only when no name at all is known, ask GitHub for the organizations:

```bash
gh api -X GET search/users -f q='type:org followers:>30000' -f sort=followers -f order=desc \
  --jq '.items[].login'   # openai microsoft deepseek-ai anthropics github google huggingface ...
```

Do not paste that output into a document - it goes stale. `anthropics/anthropic-quickstarts` has already
been renamed to `claude-quickstarts`.

### Confirm development is ongoing, with GraphQL

The Search API cannot return recent commit counts. This is what keeps star counts from fooling you.

```bash
gh api graphql -f query='{ search(query:"<query>", type:REPOSITORY, first:20){ nodes{ ... on Repository {
  nameWithOwner stargazerCount
  licenseInfo{spdxId}
  defaultBranchRef{target{... on Commit{history(since:"(six months ago)T00:00:00Z"){totalCount}}}}
  issues(states:OPEN){totalCount} pullRequests(states:OPEN){totalCount}
}}}}'
```

### Search API limits

- **1,000 results** maximum per query; paging cannot exceed it. Split with ranges like `stars:1000..2000`.
  Page 11 returns **HTTP 422** ("Only the first 1000 search results are available")
- Rate limit **30 req/min** (10 req/min for code search). Put a `sleep` in any loop
- Query length 256 characters; at most five `AND` / `OR` / `NOT` operators combined

### gh CLI traps

- **Several `org:` qualifiers must be separate shell arguments.** `gh search repos "org:a org:b kw"` fails
  with `Invalid search query`; `gh search repos kw org:a org:b` works. Or use `--owner=a,b`
- `--match` only accepts `name|description|readme`. **`in:topics` has no flag** - write the raw qualifier
- `--number-topics=N` is the `topics:N` qualifier
- Negation goes after `--`: `gh search repos --topic=mcp -- -topic:awesome`
- `gh search repos` cannot report a total. Use `gh api -X GET search/repositories -f q='...' --jq .total_count`

---

## Stage 3. Evaluate

### Start with one call per candidate

```bash
curl -s "https://summary.ecosyste.ms/api/v1/projects/lookup?url=https://github.com/<owner>/<repo>" \
  | jq '{stars:.repository.stargazers_count, archived:.repository.archived, license:.repository.license,
         dds:.commits.dds, committers:.commits.total_committers,
         past_year_commits:.commits.past_year_total_commits,
         packages:[.packages[].name], security_md:(.repository.metadata.files.security != null)}'
```

**`commits.dds` is the Development Distribution Score - the bus factor.** Low means one person writes
everything. Measured: ripgrep 0.32, vitest 0.68. Neither GitHub search nor the GitHub API gives you this.

Two things this response does **not** contain, despite looking like it should:

- **`score` is ecosyste.ms's own number, not Scorecard.** ripgrep scores 37.3 here and 4.7 on Scorecard
- `.issues` comes back as an empty `{table: ...}` stub. Fetch it separately when you need it:
  `issues.ecosyste.ms/api/v1/hosts/GitHub/repositories/<owner>%2F<repo>` gives
  `avg_time_to_close_pull_request` (vitest: 1,160,654s = 13.4 days)

### Is it actually used? (more reliable than star count)

```bash
curl -s "https://packages.ecosyste.ms/api/v1/registries/<registry>/packages/<pkg>" \
  | jq '{dependent_packages_count, dependent_repos_count, downloads, rankings}'
```

`rankings` gives the **percentile across all packages (lower is better)**. No authentication required.
Registry names come from the listing in stage 1.

deps.dev also reports dependents, but **per version**, so it answers a different question - "has this
release been picked up yet", not "is this package widely used":

```bash
curl -s "https://api.deps.dev/v3alpha/systems/npm/packages/<pkg>/versions/<ver>:dependents"
# react 18.2.0 -> 13,438   vitest 5.0.1 (just released) -> 91
```

### Security health

```bash
curl -s "https://api.deps.dev/v3/projects/github.com%2F<owner>%2F<repo>" \
  | jq '{license, scorecard: .scorecard.overallScore, checks: [.scorecard.checks[]?|{name,score}]}'
```

deps.dev embeds Scorecard and returns 200 with the rest of the metadata even when there is no Scorecard,
whereas `api.scorecard.dev/projects/github.com/<owner>/<repo>` 404s outright. **Coverage is identical
either way** - `tconbeer/harlequin` and `sxyazi/yazi` have no Scorecard on either. When one exists,
`api.scorecard.dev` is fresher (measured 2026-09-14 against deps.dev's 2026-08-24).

**Do not cut on the aggregate score.** Excellent single-maintainer projects lose points on review-related
checks (ripgrep scores 4.7 out of 10). Read the individual checks: `Vulnerabilities`, `Dangerous-Workflow`,
`Maintained`, `Signed-Releases`.

Known vulnerabilities in the exact version, keyless, and `querybatch` judges a whole shortlist at once:

```bash
curl -s -X POST https://api.osv.dev/v1/query \
  -d '{"package":{"name":"<pkg>","ecosystem":"npm"},"version":"<ver>"}' | jq '[.vulns[]?.id]'
```

### Order of judgement

1. **Is it maintained?** Commits in the last three months above zero, `archived: false`
2. **Is it actually used?** The `dependent_repos_count` percentile
3. **Is one person carrying it?** `commits.dds`
4. **License.** `licenseInfo.spdxId`. `NOASSERTION` needs a closer look
5. **Security.** The individual Scorecard checks, plus OSV for the version you would pin
6. Star count. **Look at this last.** Marketing moves it easily

---

## Stage 4. Read

Once the field is narrowed, look inside.

- **An OpenAPI spec or official specification comes first.** Machine-readable, exhaustive, no inference
- **DeepWiki MCP.** Ask questions about any public repository in natural language.
  `claude mcp add -s user -t http deepwiki https://mcp.deepwiki.com/mcp` (no authentication)
- **Context7 MCP.** Once adoption is decided, pull version-specific API references

---

## What not to do

- **Judge on star count alone.** It is the last signal. Do not skip stages 1-3
- **Treat presence in a registry as a quality guarantee.** Listings are self-reported, and excellent
  implementations go unlisted
- **Skip stage 4 and infer what a registry or API can do.** Do not guess at what a spec would tell you
- **Send natural language straight to search.** It returns nothing
- **Omit `--archived=false`.** Dead repositories rise to the top
- **Search by topic only.** 38.8% of repositories above 500 stars carry no topics at all. Union the three
  queries in stage 1, then snowball the owners in stage 2
- **Assume a registry is still up.** PulseMCP's keyless API answers 410 and Glama's answers 401.
  Check the status before building on one

---

## Evidence

The reasoning behind each choice, the measurements, and the full list of tools considered and rejected
live in
[oss-discovery-tools.md](https://github.com/shoei03/oss-discovery/blob/main/docs/oss-discovery-tools.md).

Trend tracking (which repositories are growing right now) is out of scope for this skill.
For the state of the event data, see
[github-trend-data.md](https://github.com/shoei03/oss-discovery/blob/main/docs/github-trend-data.md).
