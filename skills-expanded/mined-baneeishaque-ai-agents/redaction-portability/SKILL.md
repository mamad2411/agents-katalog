---
name: redaction-portability
description: Industrial protocol for addressing, redacting, and relativizing sensitive/absolute information in workspace artifacts — covers paths, identities, network topology, organizational identifiers, file-naming hygiene, and a canonical placeholder vocabulary so every produced artifact is safe to publish and portable across machines.
category: Security-Standards
---

# Redaction & Portability Skill (v2)

> ## ⛔ BLOCKING — Run This 3-Question Test Before Writing ANY of the Following
>
> - A markdown link with `../` that escapes the current file's enclosing repo (`[label](../../../../<other-repo>/...)`)
> - A literal organization name, internal codename, internal product name, or internal hostname in prose
> - A cross-repo "(see related skill in `<other-repo>`)" parenthetical
>
> **Test (all three MUST be YES):**
>
> 1. Are BOTH link endpoints in the SAME Git repository — OR in a parent + `.gitmodules`-registered-submodule pair (per §0.1 carve-out)?
> 2. Would the link still resolve if a stranger cloned ONLY the host repo into a fresh empty directory? (Multi-root VS Code workspaces, sibling folders on the author's disk, and "I have both repos checked out" do NOT count — see §0.1 Independence rules.)
> 3. Does the link text + surrounding prose reveal NOTHING about an org-private repo's existence, name, codename, or internal toolchain that a public reader wouldn't already know?
>
> Any NO → the link/mention is FORBIDDEN. The repair: drop the link in the public→private direction (use generic prose "consult your organization's internal skill library, if one exists"); use name-only references in the private→public direction (``the `<skill-name>` skill in the public `ai-agents` repo``).

This skill is the **single source of truth (SSOT)** for sanitising any
workspace artifact before it leaves the author's machine — be it a
committed skill `SKILL.md`, a conversation log under `docs/conversations/`,
a case study under `docs/cases/`, a commit message body, a generated
report, or a pull-request description.

It exists because:

1. AI-agent sessions naturally capture **machine-specific, identity-bearing,
   and organization-specific** strings (paths, usernames, proxy hosts,
   internal repository URLs, vendor product codenames, license keys,
   email addresses, ticket IDs, AI-agent session IDs).
2. Those strings have a strong bias toward leaking into committed
   artifacts because agents are trained to be *faithful* to the
   transcript — fidelity is a virtue inside the working session but a
   liability once the artifact is published.
3. Manual redaction is error-prone; this skill provides a **mechanical,
   audit-friendly** procedure that any agent can re-apply to any
   artifact at any time.

---

## 0. Scope

This skill applies to:

- Every file under `.agents/skills/**/SKILL.md`, `AGENTS.md`, `docs/`
- Every file under `ai-agent-rules/**/*.md`
- Every commit message body (subject, body, trailers)
- Every PR / issue description authored by the agent
- Every generated report (markdown, JSON, CSV) intended for publication

It does NOT apply to:

- Per-developer local config (`~/.m2/settings.xml`,
  `~/.ssh/config`, IDE preferences) — these are intentionally
  machine-specific and never committed.
- Files explicitly gitignored.
- Build outputs / logs that are not committed.

### 0.1 Repository Scope Tiers — Public vs Organization-Private

Redaction is **not** a single-axis decision (placeholder vs literal). It is a **product**
of two axes: the *string sensitivity tier* (§1) and the *repository publication scope*.
This sub-section defines the second axis. Every workspace folder lives in exactly one
of the following scope tiers, and the tier dictates what is allowed in committed
artifacts of THAT folder:

| Scope tier        | Examples                                          | Allowed string content                                                                                       |
| :---------------- | :------------------------------------------------ | :----------------------------------------------------------------------------------------------------------- |
| **Public**        | `ai-agents` (general skill library, GitHub public) | Tier C only (universal open-source identifiers). Tier A + B MUST be redacted to placeholders.                |
| **Org-private**   | `<corp>_ai_agents` (e.g., `acme_ai_agents`)        | Tier A still redacted; **Tier B literals scoped to that organization ARE PERMITTED** (e.g., `<toolbase>`).   |
| **Personal**      | `personal/sandbox` branch, `~/scratch/`           | Anything the author chooses; never published.                                                                |

**The two cardinal rules** that follow from this matrix:

1. **Public-scope artifacts MUST be self-contained.** They may not import, link to, or
   functionally depend on any org-private or personal-scope artifact. A public consumer
   who clones only the public repo must be able to use every skill without ever
   discovering that an org-private sibling exists. Concretely:

   - **Forbidden in a public-scope file:** `[label](../../../../<org>_ai_agents/.agents/skills/<skill>/SKILL.md)` — the target file is not in the public consumer's clone, so the link is broken, AND the link text leaks the org name + the existence of an internal skill library.
   - **Forbidden in a public-scope file:** the literal name of an organization (`<corp>`, e.g. "Acme Corp") even in prose, unless it is the genuine subject of a Tier C open-source attribution (e.g., "the BSD license" → keep; "on a `<corp>` workstation" → use `<corp>` rather than the literal name).
   - **Allowed in a public-scope file:** *generic* fallback prose that says "if your organization provides a shared tool root, consult your organization's internal skill library" — no name, no link.

2. **Org-private-scope artifacts MAY reference public-scope artifacts — by name, not by
   relative path.** The two repositories are independent Git repositories with separate
   existences; a relative link from one to the other (`../../../../<public-repo>/...`)
   resolves only inside one specific multi-root workspace layout and is broken for any
   developer who clones the org-private repo standalone. Reference public-scope skills
   and rules by canonical inline-code name only — e.g., write
   ``the general `system-wide-tool-management` skill (in the public `ai-agents` repo)``
   rather than a relative-path link. (An absolute URL to the public repo's hosted form
   is acceptable only when the public repo's hosting location is stable and the
   commit-pinning is acceptable for the use case; prefer name-only references.)

   Org-private files MAY use literal Tier B values that are universally true *within
   that organization* (the organization's shared tool root such as `<toolbase>`, the
   corporate proxy host, the internal VCS URL). The org-private repo itself is the
   de-facto namespace boundary; re-redacting `<toolbase>` everywhere adds noise without
   adding protection. The **one** preservation: use the `<placeholder>` form **once**
   beside the literal as a teaching aid (per §5.1), so a reader writing a future
   companion skill knows the canonical placeholder name to use if/when the snippet
   gets ported to public scope.

**Submodule sub-case (a deterministic intra-distribution carve-out).** A parent repo
MAY embed another repo as a Git submodule registered in the parent's `.gitmodules`
(e.g., the `ai-agents` parent registers `ai-agent-rules` at `<parent>/ai-agent-rules/`).
The registered mount path is deterministic because `.gitmodules` is itself a tracked,
versioned file in the parent — every commit of the parent pins both the submodule's
clone URL and its mount path. Together the parent + its registered submodules form a
single **Distribution Unit**: the project's documented clone recipe is
`git clone --recurse-submodules <parent-url>`, and a developer following that recipe
obtains the full unit at the deterministic layout.

Consequently:

- **Parent ↔ registered-submodule relative paths are ALLOWED** (in either direction)
  when they traverse the `.gitmodules`-pinned mount point. They are intra-distribution
  paths, not inter-repo escapes. Example (legal): a parent skill at
  `.agents/skills/<skill>/SKILL.md` linking to `../../../ai-agent-rules/<rule>.md`.
- **The Standalone-Clone Test is evaluated against the Distribution Unit**, not the
  enclosing worktree alone. The reference clone is
  `git clone --recurse-submodules <parent-url>`, which is the project's documented
  recipe. Links that resolve in that recipe pass the test.
- **Standalone-clone of the submodule by itself remains supported** (the submodule
  has its own clone URL), but in that mode the submodule is consumed *outside* its
  Distribution Unit. A developer who deliberately clones only the submodule accepts
  that links pointing into the parent will not resolve — same way partial consumption
  of any multi-repo project has limits. The submodule's own README SHOULD note its
  primary consumption is via the parent.

What remains **categorically forbidden** even after this carve-out:

- Links between two **independent repos that are NOT in a parent/submodule
  relationship** registered in either's `.gitmodules` — e.g.,
  `ai-agents` ↔ `<corp>_ai_agents` (sibling distributions, no `.gitmodules`
  registration linking them). These have NO defined relative position; the
  categorical-meaninglessness argument applies in full.
- Links from a parent into an **unregistered** sibling folder that just happens to
  live next to it on the author's disk (the "multi-root VS Code workspace" trap).
  Without `.gitmodules` registration there is no Distribution Unit, no deterministic
  mount, no project-recipe clone — just the author's local accident.
- All Tier-leak prohibitions (link text leaking org names, etc.) apply unchanged
  regardless of repo topology.

The agent's audit therefore distinguishes two cases for any `../` that escapes the
enclosing worktree's root: (a) does it land inside a sibling registered in the
nearest enclosing `.gitmodules`? → ALLOWED (intra-distribution); (b) anywhere else?
→ FORBIDDEN (inter-distribution escape).

**Asymmetric linking summary:**

```text
<public-repo>      ──X──────────────────────▶ <org-private-repo>    (FORBIDDEN: unregistered sibling + leaked name)
<public-repo>      ───▶ <public-repo>                                 (ALLOWED, relative path, intra-repo)
<org-private-repo> ───▶ <org-private-repo>                            (ALLOWED, relative path, intra-repo)
<org-private-repo> ───▶ `<public-skill-name>` (no link, by name only)  (ALLOWED, name-only reference)
<org-private-repo> ──X──────────────────────▶ <public-repo> (via relative path) (FORBIDDEN: unregistered sibling, layout-dependent)
<parent-repo>      ───▶ <registered-submodule>/<file> (via `.gitmodules` mount)  (ALLOWED, intra-distribution-unit)
<registered-submodule> ───▶ <parent-repo>/<file> (via `../` to mount root)        (ALLOWED, intra-distribution-unit)
<parent-repo>      ──X──▶ <unregistered-sibling-folder>/<file>                    (FORBIDDEN: no `.gitmodules` entry → local accident)
```

> The last three rows are the submodule carve-out above. A submodule **registered**
> in the parent's `.gitmodules` has a deterministic mount path that ships with every
> parent commit; the project's clone recipe is `git clone --recurse-submodules
> <parent-url>`, and links across the registered mount resolve under that recipe.
> Anything not in `.gitmodules` (an unregistered sibling folder that just happens to
> sit next to the parent on the author's disk) gets no such guarantee and is treated
> as an inter-repo escape.

*Intra-repo* means both link endpoints live inside the same Git repository (the `../`
chain never crosses that repo's root) — always allowed. *Intra-distribution-unit*
means both endpoints live inside the same Distribution Unit (the enclosing repo plus
its registered submodules) but cross a `.gitmodules`-pinned mount — also allowed.
*Inter-distribution* (two independent repos with no parent/submodule relationship via
`.gitmodules`) is what the FORBIDDEN rows prohibit.

**The unifying principle:** no relative-path link may escape its enclosing
Distribution Unit. The Distribution Unit is the enclosing repo PLUS every submodule
registered in its `.gitmodules` (recursively). Within the unit, relative paths are
first-class; across units they fail the Standalone-Clone Test.

**Detection heuristic.** Before adding any inter-skill link from a public-scope file,
resolve the link's target relative path against the public repo root — if the target
escapes the public repo (`../../../../some-other-repo/...`), the link is illegal
regardless of redaction of its display text.

### 0.2 Submodule→Parent URL References — The Standalone-Clone Gap

The §0.1 carve-out says that parent↔registered-submodule relative paths are
ALLOWED because they are intra-distribution-unit. This is correct for the
primary clone recipe (`git clone --recurse-submodules <parent-url>`).

However, there is a gap: when a file INSIDE a registered submodule references
a file in the parent, a relative path (`../../../<parent>/<path>`) works in the
`--recurse-submodules` clone but is BROKEN when someone clones the submodule
standalone. The §0.1 carve-out explicitly acknowledges this limitation.

The author has three options for such a reference, each with different
portability and stability characteristics:

| Option | Example (concrete) | Standalone clone | Stable over time |
|---|---|---|---|
| **A — Relative path** | `../../../../ai-agent-rules/../foo.md` | ❌ Broken | ✅ (tracks HEAD of parent) |
| **B — SHA-pinned URL** | `https://github.com/<OWNER>/<REPO>/blob/<SHA>/<path>#<anchor>` | ✅ Resolves | ✅ (pinned to specific content) |
| **C — Branch-pinned URL** | `https://github.com/<OWNER>/<REPO>/blob/main/<path>#<anchor>` | ✅ Resolves | ❌ (content shifts under the link) |

**Recommendation:** use Option A (relative path) when the reference is
pedagogical or administrative and the standalone-clone experience is not a
concern. Use Option B (SHA-pinned URL) when the reference is operational —
a reader who clones only the submodule MUST be able to follow the link —
AND the parent repo's hosting location is stable and public (or
org-private with predictable access). **Never use Option C** — a
branch-pinned URL silently becomes stale or misleading when the target
file is modified on that branch.

**Redaction treatment for SHA-pinned URLs in public-scope files:**

A SHA-pinned URL contains three Tier-B elements (repo owner, repo name,
commit SHA) plus one Tier-C element (`github.com`). In a **public-scope**
skill artifact, all Tier-B elements MUST be redacted to placeholders:

```markdown
<!-- Forbidden in a public-scope skill: -->
See [Phase 1g](https://github.com/<PARENT-REPO-OWNER>/<PARENT-REPO>/blob/<SHA>/.agents/skills/...)

<!-- Allowed — Tier-B elements replaced: -->
See Phase 1g in the parent repo
(`<PARENT-REPO-OWNER>/<PARENT-REPO>` at
`<PARENT-FILE-PATH>` commit `<SHA>`).
```

In an **operational** file (a real commit message, a real submodule
`rules.md` that ships with a real repo), the literal URL is appropriate
because the file IS the actual workflow artifact — it is not a portable
recipe. The skill teaches the pattern; the concrete usage carries the
real values.

**Detection heuristic for branch-pinned URLs.**

Before adding a URL-based cross-reference from a submodule artifact to a
parent, audit for branch-pinned (unstable) URLs:

```bash
# Search for /blob/main/ or /blob/master/ in staged files
git diff --cached | grep -E '/blob/(main|master)/'
```

Any match MUST be replaced with a SHA-pinned URL. To obtain the current
SHA of the parent's default branch:

```bash
git -C <parent-repo> rev-parse HEAD
```

### 0.3 Commit Messages as Committed Artifacts

Commit messages are committed artifacts. They pass through the same
standalone-clone test as any file under `.agents/skills/` or
`ai-agent-rules/`. This is especially consequential for **submodule
commit messages** — a submodule has its own clone URL, and someone
cloning only the submodule reads its log without the parent repo.

**Three allowed patterns** for referencing parent-repo content in a
submodule commit message, in order of preference:

1. **SHA-pinned GitHub URL** — best when the reference targets a
   specific document or heading. Resolves in any clone, points to
   immutable content.

   ```
   docs(rules): cross-reference stash-apply failure fallback with resolvable URLs

   - Link to selective file extraction recovery path via GitHub URL that
     resolves in standalone clone
   - Link to redaction-portability skill for the URL decision framework
     used here
   ```

2. **Full repo-name + descriptive path** — when a URL is impractical
   (e.g., the message references a whole skill, not a specific line).
   Acts as a navigation hint the reader can search for:

   ```
   feat(skill): add Phase 1g selective file extraction from stash

   Backport the selective-file-extraction recovery path from the
   `baneeishaque/ai-suite` parent repo's
   `git-pre-execution-safety-stash` skill.
   ```

3. **Generic prose** — when the reference is conceptual and the
   specific location is not load-bearing:

   ```
   docs(rules): add blockquote for interactive hunk staging safety

   References the stash-apply failure fallback documented in the parent
   repo's safety-stash skill for handling live editor conflicts.
   ```

**Forbidden in a submodule commit message:**

- Parent-repo jargon (internal section labels, heading titles, local
  acronyms that only make sense inside the Distribution Unit).
- Relative paths to parent files.
- Branch-pinned URLs (`/blob/main/...`).

**The principle:** a submodule commit message must be self-contained.
A reader who clones only the submodule must be able to understand the
message. If the message references parent content it cannot explain
itself, the reference must be a navigable URL (pattern 1) or a
descriptive enough search hint (pattern 2) that the reader can locate
the source independently.

**Don't redefine SSOT.** When a commit message describes the rationale
for a cross-reference that the `redaction-portability` skill already
covers, reference the skill by name — do not restate the decision
framework inline.

---

## 1. The Three Sensitivity Tiers

Every string the agent emits falls into one of three tiers. The required
treatment differs per tier.

### Tier A — Identity & Credentials (always redact)

| Class | Examples | Replacement |
|---|---|---|
| Personal name (human author) | real human names | `<author>` or `[REDACTED_NAME]` |
| Username on a developer machine | OS account names | `<user>` |
| Email address | `firstname.lastname@example.com` | `<author-email>` |
| Auth token, API key, password | any opaque secret string | `<redacted-secret>` (NEVER leave plaintext) |
| Personal IP address / MAC | `10.x.y.z`, `aa:bb:cc:dd:ee:ff` | `<host-ip>`, `<mac>` |
| Personal SSH public-key fingerprint | `SHA256:…` | `<ssh-fingerprint>` |
| Cloud account / subscription ID | UUIDs in URLs / tooling output | `<account-id>` |

### Tier B — Machine & Organization Topology (redact unless universally true)

| Class | Examples | Replacement |
|---|---|---|
| Absolute filesystem path on author's machine | `C:\Users\<user>\…`, `/home/<user>/…` | `<workspace-root>`, `<user-home>`, `~/…` |
| Drive letter or mount point | `C:\<shared-tool-root>\…`, `/mnt/build/…` | `<toolbase>`, `<build-mount>` |
| Corporate proxy host & port | internal proxy FQDN + port | `<corp-proxy-host>:<corp-proxy-port>` |
| Corporate domain / TLD | `*.<corp>.com`, `*.<corp-cloud>.com` | `<corp-domain>`, `<corp-cloud-domain>` |
| Internal repository URL | `https://<internal-vcs>/<team>/<repo>` | `<internal-vcs>/<team>/<repo>` |
| Internal artifact repository | `https://<internal-nexus>/…` | `<internal-artifact-repo>` |
| Internal CI/CD endpoint | `https://<internal-ci>/job/…` | `<internal-ci>` |
| Internal ticketing | `https://<ticket-system>/browse/PROJ-1234` | `<ticket-system>/<TICKET-ID>` |
| VPN / network zone names | `corp-vpn-east`, `dmz-build-net` | `<vpn>`, `<network-zone>` |
| Internal SMTP / chat hosts | internal mail/chat FQDNs | `<internal-mail>`, `<internal-chat>` |
| Vendor product codename (internal) | unreleased project names, NDA codenames | `<product-codename>` |
| Customer / client name | external customer names | `<customer>` |
| License key / dongle ID | opaque license strings | `<license-key>` |
| **Public-but-not-universal identifier** — a real GitHub owner / repo / submodule / branch / SHA that *is* publicly visible but is **specific to one user's workflow trace**, not the skill's general subject matter | `baneeishaque/ai-suite`, submodule `ai-agent-rules`, branch `master`, `<sha>` in a Source Recipe / case study / example | `<ORG-USER>/<REPO>`, `<SUBMODULE>`, `<DEFAULT-BRANCH>`, `<SHA-...>` (see §2) |

### Tier C — Public / Universal (keep verbatim)

These are universally true; redacting them harms reproducibility:

- Public domain names: `repo.maven.apache.org`, `github.com`,
  `central.sonatype.com`
- Open-source project / artifact names: `commons-io`, `Eclipse Orbit`,
  `Apache Tycho`, `Adoptium Temurin`
- Open-source bundle symbolic names: `org.apache.commons.commons-io`
- Standard tool flags, JVM options, OSGi headers
- Standard local-machine reserved names: `127.0.0.1`, `localhost`,
  `0.0.0.0`
- Standard env var names: `HTTP_PROXY`, `JAVA_HOME`, `USERPROFILE`
- Standard CLI commands

The rule of thumb: **if a competent reader on a different machine /
different organization would benefit from the literal string, keep it.
Otherwise, redact.**

### Tier B Rationale — Redaction Is for Portability, Not Secrecy

A frequent objection: *"Both the repo and the submodule are public on
GitHub — anyone can `git clone` them. Why redact the names?"*

Redaction in Tier B is **not** a confidentiality control. The repo names,
owner handles, submodule names, branch names, and SHAs may all be world-
readable on GitHub. They are redacted for two **portability** reasons:

1. **A skill is a reusable recipe, not a trip report.** When §6 (Source
   Recipe) reads *"Clone `<ORG-USER>/<REPO>`, init submodule `<SUBMODULE>`,
   observe `<SHA-URL-SWAP>` …"*, a different author with
   `acme-corp/their-monorepo` containing a `vendor-libs` submodule can
   map every placeholder to their situation in one pass. With literal
   names baked in (`baneeishaque/ai-suite` + `ai-agent-rules`), every
   reader must mentally translate before they can apply the skill — and
   readers who don't notice the literal-vs-template distinction will
   wrongly conclude the skill only applies to that specific repo.

2. **Skills get copied / forked across repositories.** The whole point of
   a shared skill library (public `ai-agents`, org-private
   `<corp>_ai_agents`) is that a useful skill migrates outward. A literal
   `baneeishaque/ai-suite` in a skill that ends up cloned into another
   user's repo reads as confusing noise — *"why is this skill talking
   about a repo I've never heard of?"* — and obscures the skill's
   actual subject matter.

**Where the literals legitimately live** (and MUST NOT be scrubbed from):

- **Session checkpoints** (`~/.copilot/session-state/<id>/checkpoints/*.md`,
  `plan.md`, `scratch/*`) — private to the author's machine; full literal
  trace is needed to resume the original work.
- **Git commit messages and PR descriptions** on the actual workflow —
  these naturally carry real SHAs, branch names, and ticket IDs because
  they ARE the trip report.
- **Bug reports / support tickets** that reference the literal occurrence.

The skill file itself stays portable; the literal trace lives in the
private workspace artifacts that document *this one application* of the
skill.

**Test the redaction.** Before declaring a skill done, read its §6 (or
any case-study section) and ask: *"Could a developer at a different
organization, working on a different repo with a different submodule,
follow this recipe step-by-step by substituting their own values for the
placeholders?"* If any literal name forces the reader to think *"this
recipe is really about that other repo, not mine"* — redact it.

---

## 2. Canonical Placeholder Vocabulary

A controlled vocabulary makes redaction *predictable* and *searchable*
(future agents can grep for `<workspace-root>` to find every site that
needs a per-machine substitution).

### 2.1 Path placeholders

| Placeholder | Meaning |
|---|---|
| `<workspace-root>` | Root of the workspace this agent is inspecting |
| `<workspace-root-21>`, `<workspace-root-N>` | Disambiguate when multiple workspaces appear in one document |
| `<user-home>` | The author's home directory (`~`) |
| `<toolbase>` | Organization-shared tool installation root |
| `<product-host>` | Vendor product directory inside `<toolbase>` (codenamed) |
| `<eclipse-install>` | Eclipse installation directory |
| `<jdk-install>` | JDK installation directory |
| `<m2-repo>` | `~/.m2/repository` |
| `<dir-1>`, `<dir-N>` | Disambiguated directory placeholders inside scripts |

### 2.2 Identity placeholders

| Placeholder | Meaning |
|---|---|
| `<author>` | The human author of a commit / session |
| `<user>` | OS username on a specific machine |
| `<author-email>` | Email of a commit author |
| `<reviewer>` | Reviewer of a PR / commit |
| `<session-id>` | An AI-agent session identifier (machine-local; never include in published artifacts) |
| `[REDACTED_NAME]` | Legacy form, kept for backwards compatibility — prefer `<author>` |
| `[REDACTED]` | Generic redaction, last resort when no specific placeholder fits |

### 2.3 Network & organization placeholders

| Placeholder | Meaning |
|---|---|
| `<corp-proxy-host>` | Corporate HTTP/HTTPS proxy hostname |
| `<corp-proxy-port>` | Corporate proxy port |
| `<corp-domain>` | Corporate primary domain (`*.example.com`) |
| `<corp-cloud-domain>` | Corporate cloud-hosted secondary domain |
| `<internal-vcs>` | Internal Git/VCS server base URL |
| `<internal-artifact-repo>` | Internal Maven/Nexus/Artifactory |
| `<internal-ci>` | Internal CI/CD endpoint |
| `<ticket-system>` | Jira / Azure DevOps / similar |
| `<TICKET-ID>` | Single ticket reference (`PROJ-1234`) |
| `<customer>` | External customer / client name |
| `<product-codename>` | Internal / unreleased product codename |

### 2.4 Generic disambiguation suffixes

When the same placeholder type appears multiple times in one document
with **different** values, suffix with letters: `<consumer-plugin-A>`,
`<consumer-plugin-B>`. When the count exceeds the alphabet, switch to
numeric: `<consumer-plugin-1>`, `<consumer-plugin-N>`.

### 2.5 Publication-scope placeholders (for URL references)

| Placeholder | Meaning |
|---|---|
| `<PARENT-REPO-OWNER>` | GitHub owner / org of the parent repo in a parent↔submodule Distribution Unit |
| `<PARENT-REPO>` | Parent repo name in a parent↔submodule Distribution Unit |
| `<SHA>` | A Git commit SHA (full 40-char or abbreviated). Prefer the full SHA in pinned references. |
| `<SUB-SHA>` | A submodule pointer SHA (the SHA recorded in the parent's tree for the submodule commit) |
| `<SHA-URL-SWAP>` | Meta-placeholder for a section that teaches the reader to replace a placeholder SHA with the real one |
| `<PARENT-FILE-PATH>` | Path within the parent repo, relative to its root |
| `<SUBMODULE-MOUNT>` | Mount path of a registered submodule relative to the parent root |

### 2.6 The general rule of placeholder formation

`<lower-case-hyphenated-noun>` — angle-bracketed, lower-case,
hyphen-separated. This visually signals "placeholder, replace with
real value" and is consistent with HTML/XML/markdown convention. Do
not use snake_case (`<work_space_root>`) or PascalCase
(`<WorkspaceRoot>`).

---

## 3. Path Handling Protocol

### 3.1 Absolute → relative

Any `C:\…` or `/Users/…` path in a workspace artifact MUST be
converted to one of:

- A workspace-relative path: `.agents/skills/<skill>/SKILL.md`
- A user-home-relative path with `~`: `~/.m2/settings.xml`
- A placeholder if neither applies: `<workspace-root>/<plugin>/MANIFEST.MF`

**Why placeholders, not real anonymous paths**: a `C:\…\com.example.plugin\…`
still leaks the drive letter and operating system. A placeholder is OS-agnostic.

### 3.2 Cross-workspace references

When a document spans two workspaces (e.g., a session log that started
in one workspace and migrated to another), disambiguate explicitly:

```text
Source:      <workspace-root-source>
Target:      <workspace-root-target>
Skill repo:  <ai-agents-root>
```

Never write two real absolute paths side-by-side.

### 3.3 The fileLinkification carve-out

Links to other files in the **same repository** are NOT redacted — they
are relativized per the markdown-generation rules
([fileLinkification section](../../../ai-agent-rules/markdown-generation-rules.md)).

```markdown
✅ [SKILL.md](../SKILL.md)               # relative, portable
✅ [SKILL.md](.agents/skills/x/SKILL.md) # workspace-relative
❌ [SKILL.md](C:\work\ai-agents\…)        # absolute path — never
❌ [SKILL.md](file:///C:/…)              # file:// scheme — never
```

Also: **angle-bracket placeholders inside `[text](target)` link
targets MUST be replaced with inline-code form** because they produce
non-navigable broken links:

```markdown
❌ [<plugin>/<file>.target](../../../<plugin>/<file>.target)
✅ Workspace file (symbolic): `<plugin>/<file>.target`
```

### 3.4 Path-like strings inside code fences

Code fences are NOT exempt from redaction. A bash snippet showing
`cd C:\Users\<user>\…` is just as leaky as the same path in prose.

Acceptable forms:

```powershell
cd <workspace-root>
git -C <workspace-root> status
Get-ChildItem '<toolbase>\<product>\plugins'
```

If the literal example value is **load-bearing** for understanding
(e.g., demonstrating a proxy URL format), keep it but mark with a
parenthetical: `http://<corp-proxy-host>:<corp-proxy-port>`
*(literal example: `http://proxy.example.com:8080`)*.

---

## 4. Identity Handling Protocol

### 4.1 Commit-author trailers

In documentation that quotes a commit, redact the author line:

```diff
- Author: Full Personal Name <firstname.lastname@example.com>
+ Author: <author> <<author-email>>
```

Keep the commit SHA — SHAs are content-addressed and reveal nothing about identity.

### 4.2 Reported names in transcripts

When a session log says `the user, <Real Name>, asked …`, redact to
`the user asked …`. The author's identity is not load-bearing for the
technical content.

### 4.3 Username paths

Anywhere a developer's OS username appears in a path, redact to
`<user-home>` or `~`.

### 4.4 Reviewer / approver names

PR descriptions citing approvers MUST redact to `<reviewer-1>`,
`<reviewer-2>`, etc.

---

## 5. Network & Organization Handling Protocol

### 5.1 Proxy hosts

If the document explicitly teaches *how to configure* a proxy, keep
**both** the placeholder and one literal anonymized example:

```text
host: <corp-proxy-host>   # e.g., proxy.example.com
port: <corp-proxy-port>   # e.g., 8080
```

This satisfies pedagogy (reader knows what shape of value goes there)
without leaking the actual corporate proxy address.

### 5.2 Internal domain names

Replace organization-specific domains with placeholders:

```diff
- nonProxyHosts>127.0.0.1|localhost|*.<corp>.com|*.<corp-cloud>.com</nonProxyHosts>
+ nonProxyHosts>127.0.0.1|localhost|*.<corp-domain>|*.<corp-cloud-domain></nonProxyHosts>
```

### 5.3 Internal repository URLs

```diff
- https://<internal-vcs-real>/scm/<team>/<repo>.git
+ <internal-vcs>/<team>/<repo>.git
```

### 5.4 Ticket / issue references

```diff
- See <Ticket System> PROJ-12345 for the original report
+ See <ticket-system>/<TICKET-ID> for the original report
```

### 5.5 Customer / project codenames

Internal product codenames and customer names MUST be redacted:

```diff
- The <Internal-Product> customer-specific build for <Customer>
+ The <product-codename> customer-specific build for <customer>
```

### 5.6 IPv4 / IPv6 addresses

- `127.0.0.1`, `::1`, `0.0.0.0` → keep (universally meaningful)
- `192.168.x.x`, `10.x.x.x`, `172.16-31.x.x` (private ranges) → redact (`<host-ip>`)
- Public routable IPs from session output → redact unless it's a
  documented public service IP

---

## 6. File Naming Hygiene

Filenames themselves are artifacts. Apply redaction to the file path
just as to file contents.

### 6.1 Conversation log naming

```text
.agents/skills/<skill>/docs/conversations/YYYY-MM-DD-<topic>.md
```

✅ `2026-05-10-jdk17-to-jdk21-and-ide-fixes.md` — topic only
❌ `2026-05-10-<author>-<corp>-jdk-fix.md` — name + organization leak

### 6.2 Case-study naming

```text
.agents/skills/<skill>/docs/cases/<topic>.md
```

✅ `apache-commons-io-symbolic-name-aliasing.md` — public technology
✅ `m2e-enterprise-proxy-resolution.md` — generic infrastructure
❌ `<corp>-<proxy-product>-fix.md` — organization leak

### 6.3 Path placeholders in filenames

A filename should NOT contain `<placeholder>` syntax — angle brackets
break on many filesystems. Instead, encode the abstraction in words:

- `<corp-proxy>` topic → filename `enterprise-proxy-resolution`
- `<workspace-root-21>` topic → filename `jdk21-workspace-migration`

---

## 7. Code Examples — Special Cases

### 7.1 Diffs

Diffs included for pedagogy MUST be redacted just like prose. The
public technical content (GAV, bundle names, OSGi headers) is
universal (kept verbatim); the surrounding path is redacted:

```diff
- <location path="C:\<shared-tool>\<product>\<version>\eclipse\plugins" .../>
+ <location path="<toolbase>\<product-orbit>\eclipse\plugins" .../>
```

### 7.2 Shell snippets

Replace the user's working directory in prompts:

```diff
- PS C:\Users\<user>\work_2026\<workspace>> git status
+ PS <workspace-root>> git status
```

### 7.3 Log output / stack traces

Stack traces often leak local paths in `at com.example.Foo(Foo.java:42)`
*if* the stack frame format includes file URIs (rare). Frame text
itself is normally safe. The path-revealing lines are usually:

- `Working Directory: …`
- `Configuration file: …`
- `Local repository: …`

Redact these; keep the substantive trace.

### 7.4 PowerShell `$env:USERPROFILE` is safe

`$env:USERPROFILE` is a portable reference — it expands per-machine at
runtime. It is the *recommended* way to write user-home paths in
PowerShell examples:

```powershell
Get-ChildItem "$env:USERPROFILE\.m2\repository"  # ✅ portable
Get-ChildItem 'C:\Users\<user>\.m2\repository'   # ❌ leaky
```

Likewise `~` in POSIX shells.

### 7.5 Pedagogical Carve-Out — Examples That Teach Redaction

A skill (or rationale subsection) whose **subject IS the redaction rule itself** MAY quote literal Tier B values, provided two conditions hold:

1. The literal exists to **teach the reader what to redact** — i.e., it appears as the "before" side of a before/after comparison, inside an example table, or as the concrete instance the surrounding prose is reasoning about. Using a placeholder would be circular ("we replace `<ORG-USER>` with `<ORG-USER>`") and would defeat the explanatory purpose.
2. The surrounding prose **marks the literal as an example-to-be-redacted** — typically via "e.g.", an example column in a table, a `❌ leaky` annotation, or framing such as *"Forbidden in a public-scope file: `<corp>`"*.

Examples of the carve-out applied in this very skill:

- §1 Tier B table: `C:\Users\<user>\…`, `/home/<user>/…` shown literally in the **"Examples"** column.
- §1 Tier B Rationale: `baneeishaque/ai-suite` and `ai-agent-rules` quoted inside a *"Why these would be redacted"* discussion.
- §7.4 above: `'C:\Users\<user>\.m2\repository'  # ❌ leaky` shown to teach the contrast with `$env:USERPROFILE`.

**Boundary**: the carve-out covers **didactic** literals. It does NOT cover Source Recipe sections, case-study walkthroughs, traceability entries, or commit citations — those are operational content, not teaching content, and MUST use placeholders per §1–§5.

**Self-test before invoking the carve-out**: *"If I replaced this literal with `<PLACEHOLDER>`, would the surrounding sentence still make its teaching point?"* If yes → use the placeholder; the carve-out does NOT apply. If no (the sentence becomes circular or vacuous) → the carve-out applies and the literal stays.

---

## 8. Implementation Workflow

When applying this skill to existing artifacts:

### Step 1 — Inventory

```powershell
# Find every absolute Windows path
Select-String -Path '<artifact-glob>' -Pattern '[A-Z]:\\[\w\\]+' -AllMatches

# Find every absolute POSIX path
Select-String -Path '<artifact-glob>' -Pattern '/(?:Users|home|opt|mnt)/[\w\-./]+'

# Find every email address
Select-String -Path '<artifact-glob>' -Pattern '[\w\.\-]+@[\w\.\-]+\.\w+'

# Find every IPv4
Select-String -Path '<artifact-glob>' -Pattern '\b(?:\d{1,3}\.){3}\d{1,3}\b'

# Find every internal-looking hostname (heuristic)
Select-String -Path '<artifact-glob>' -Pattern '[\w\-]+\.(?:<corp1>|<corp2>|example)\.(?:com|net|local)'
```

### Step 2 — Classify

For each match, decide Tier A / B / C per §1.

### Step 3 — Substitute

Apply the canonical placeholder vocabulary per §2. Use bulk
`multi_replace_string_in_file` operations for high-volume substitution.

### Step 4 — Verify (mandatory)

After substitution, re-run the inventory scans. The terminal output
should be empty (or show only Tier-C universally-true matches).

```powershell
# A passing verification looks like this:
Select-String -Path '<artifact>' -Pattern '<real-name>|<real-corp-domain>' -SimpleMatch
# (no output)
```

### Step 5 — Encoding sanity-check

Redaction edits frequently mangle non-ASCII (em-dashes, ellipses,
emoji). After substitution, scan for mojibake markers:

```powershell
Select-String -Path '<artifact>' -Pattern 'Ã|â€|Â|ï¿½'
# (no output expected)
```

If matches appear, fix encoding before considering redaction complete.

The root cause is almost always a non-UTF-8-aware read-modify-write in
Windows PowerShell 5.1; the prevention protocol and the deterministic
mojibake-repair recipe live in
[`ai-agent-rules/shell-execution-rules.md` §2.4](../../../ai-agent-rules/shell-execution-rules.md#24-utf-8-safe-bulk-text-edits-in-powershell-forbidden-patterns)
and MUST be applied before re-running the redaction pass.

### Step 6 — Re-render check

Open the rendered markdown in a previewer. Look for:

- Broken links (placeholders used in `[text](path)` link targets
  produce non-navigable links — see §3.3)
- Broken tables (extra `|` from incomplete substitution)
- Wide tables overflowing (placeholders are often longer than the
  values they replaced; consider line-wrapping cells)

---

## 9. Compositional Use by Other Skills

This skill is invoked passively by many composers:

- [`skill-factory`](../skill-factory/SKILL.md) — applies §1–§8 during
  the final audit of every generated `SKILL.md` and conversation log
- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) —
  applies §4 to commit-message bodies that quote author trailers
- [`code-explanation`](../code-explanation/SKILL.md) — applies §7 to
  code excerpts copied into explanation documents
- [`work-log-processing`](../work-log-processing/SKILL.md) — applies
  §4 to log entries naming individuals

Composers MUST cite this skill explicitly when their output contains
content from §1's redaction targets.

---

## 10. Prohibited Behaviors

- **DO NOT** commit a personal email address to a tracked artifact
  even as a "for-attribution" courtesy. Attribution lives in the
  commit's Git author field, not in the artifact body.
- **DO NOT** invent fake-looking real values to satisfy redaction
  (e.g., replacing `<corp>.com` with `myveryreal.com`). Use canonical
  placeholders. The placeholder *is* the contract.
- **DO NOT** leave half-redacted strings (`<corp-proxy-host>.<corp>.com`)
  — they leak the suffix.
- **DO NOT** redact public open-source identifiers (Apache Commons,
  Eclipse, Maven Central). This is forbidden *over*-redaction —
  removing them harms reproducibility for future readers.
- **DO NOT** create new placeholder forms ad-hoc — extend §2's
  vocabulary first via a separate skill update.
- **DO NOT** rely on Git history to "hide" a redaction — once
  committed unredacted, the value is permanently in the object
  database. Reach for `git-filter-repo` or BFG if a hard scrub is
  required, but prevention is the only reliable strategy.
- **DO NOT** insert a link from a public-scope file to an
  org-private-scope or personal-scope file (per §0.1 rule 1). The
  link target won't exist in the public consumer's clone, and the
  link text itself leaks the existence and name of the private
  artifact.
- **DO NOT** include a composer-table row (or "Related Skills" list
  item) in a base/published skill that references a skill in a different
  repository — even by name only, if the name reveals the other repo's
  contents. The composer table is part of the published artifact;
  cross-repo references fail the Standalone-Clone Test (§0.1 Q2) and
  leak repo topology (§0.1 Q3). **Example of forbidden pattern:** a
  public base skill listing `<project-specific-composer>` (a
  project-specific composer in a separate private repo) in its composer
  table — the row has no valid relative path and reveals the private
  repo's structure. **Repair:** omit the row from the base skill; let
  the project-specific skill's own `AGENTS.md` or composer section
  include the reference instead.
- **DO NOT** name an organization (`<corp>`, customer
  name) in prose in a public-scope file. Use "a corporate
  workstation" / "your organization" / `<corp>` instead.
- **DO NOT** rely on a sibling-folder workspace layout (multi-root
  VS Code workspace) to make a cross-repo link "work" — it works
  only for the original author. External consumers clone the public
  repo standalone and the relative path silently breaks.

---

## 11. Quick-Reference Substitution Recipe

For one-shot bulk edits, the master substitution recipe (apply in
order; do not skip):

1. Absolute filesystem paths → `<workspace-root>` / `<user-home>` / `<toolbase>`
2. Per-machine drive letters → tier-2 placeholder
3. Email addresses → `<author-email>`
4. Personal names → `<author>`
5. OS usernames → `<user>`
6. Internal hostnames → `<corp-proxy-host>` / `<internal-vcs>` / etc.
7. Internal domains → `<corp-domain>` / `<corp-cloud-domain>`
8. Ticket IDs → `<ticket-system>/<TICKET-ID>`
9. Customer / codename strings → `<customer>` / `<product-codename>`

Per-organization concrete patterns (specific FQDNs, specific user
names) belong in **organization-specific extensions** (e.g.,
an org-private `<corp>_ai_agents/.agents/skills/` sibling repo) —
never in this SSOT.

---

## 12. Related Skills & Rules

- [markdown-generation-rules.md](../../../ai-agent-rules/markdown-generation-rules.md) —
  authoritative link syntax; fileLinkification section
- [`skill-factory`](../skill-factory/SKILL.md) — primary consumer
- [`project-structure`](../project-structure/SKILL.md) — where
  redacted artifacts belong on disk
- [`vscode-extension-portability`](../vscode-extension-portability/SKILL.md) —
  analogous portability protocol for VS Code extension paths

---

## 13. Versioning

| Version | Date | Change |
|---|---|---|
| v1 | (initial) | Path relativization + basic name redaction (Tiers A/B not separated) |
| v2 | 2026-05-10 | Introduced three-tier model, canonical placeholder vocabulary, network/organization protocol, file-naming hygiene, encoding sanity-check, quick-reference recipe, prohibited behaviors, broken-link carve-out (§3.3) |
| v2.1 | 2026-06-09 | Added §0.2 (SHA-pinned URL pattern for submodule→parent in standalone-clone gap), §2.5 (publication-scope placeholders), branch-pinned URL detection heuristic, three-option comparison table |
| v2.2 | 2026-06-09 | Added §0.3 (commit messages as committed artifacts — three allowed reference patterns for submodule messages, forbidden parent-repo jargon), updated version table |
