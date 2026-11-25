---
name: upgrade-closure
description: >-
  Use when the user asks what a direct dependency upgrade changes in the
  resolved closure, which transitives appear or disappear, or whether the
  candidate brings new vulnerabilities or license categories. Gradle when a
  wrapper exists; otherwise one deps.dev upgrade. Not a safety verdict.
disable-model-invocation: true
---

# Upgrade closure

Call **`compare_upgrade_closure`**. Do not diff graphs yourself.

`graphSource` defaults to `auto`:

- `auto` — Gradle when the project is a Gradle build and `gradlew` exists,
  otherwise deps.dev.
- `gradle` — two sequential wrapper resolves. No deps.dev fallback if that fails.
- `depsdev` — one isolated public graph pair. Exactly one upgrade.

Gradle accepts up to 20 substitutions (`substitution` `exact` or `module`,
default `exact`). The server does not retry `exact` as `module`. deps.dev
rejects more than one upgrade. `includeLicenses` defaults to true.

## Steps

1. Pass the library upgrades the user named (`groupId`, `artifactId`,
   `fromVersion`, `toVersion`) and `projectPath` when the project is not the
   working directory. Leave `graphSource` unset unless the user asked for
   `gradle` or `depsdev`. Do not call the tool once per coordinate.

2. If the selection would be deps.dev and the user named more than one upgrade,
   say "a batch closure needs a Gradle wrapper" and do not call. Do not loop one
   call per coordinate. The confirm-step split lives in `/check-deps`: markers; the
   `runtimeClasspath` predicate only for Gradle configuration names; without a
   wrapper, Maven `implementation` and `runtimeOnly` stay (drop test scopes and
   `compileOnly` / `provided`); the 20-upgrade cap; no call when nothing remains.
   Do not invent a second split.

3. Render with the same decision row as `/check-deps`. Lead with `advisory`,
   `graphSource`, `diffReliable`, and any `not closure-checked` line you already
   printed. Do not re-rank. Do not paraphrase a CVE `summary`. Skip a field
   only when the payload omitted it.

   The upgraded coordinate is not in `vulnerabilities.introduced` / `remaining` /
   `fixed`. Its introduced, remaining, and fixed rows are
   `targets[].vulnerabilityDelta`; keep that relation. `targets[].vulnerabilities`
   is `relation: target` only. Do not relabel a delta row `target`, and do not use
   the target list to fill introduced, remaining, or fixed. Other coordinates come
   from the closure buckets.

   Render every CVE decision row in those lists, whatever `advisory` is. A `stop`
   result still shows a non-MAL CVE. A `review` result still shows `fixed` and
   `MEDIUM`/`LOW` rows. `advisory` only chooses the action.

   - **`stop`** — do not apply the edit. Also call out each `MAL-` id in `targets[].vulnerabilities`,
     `targets[].vulnerabilityDelta`, and `vulnerabilities.introduced` / `remaining` /
     `uncompared`, including `path` when present. If the same id is in both the
     target list and the delta, one row, and the relation is the delta's. Do not
     apply the edit. Do not call an `uncompared` `MAL-` "introduced".
   - **`review`** — one decision row per introduced id from `vulnerabilityDelta`
     and from `vulnerabilities.introduced` (include an id with no severity), per
     `relation: target` at `CRITICAL`/`HIGH` only when that id is not already in
     `vulnerabilityDelta`, and per remaining `CRITICAL`/`HIGH` from
     `vulnerabilityDelta` and from `vulnerabilities.remaining`, still labeled
     remaining. Then license `violation`s and every matrix reason that is set:
     `diffReliable` false, `fixesIncomplete`, a target not `landed`,
     `rewroteVersionless`, `capabilityUnavailable`. When
     `compare_versions(safeUpgrade.version, toVersion) > 0`, say the confirmed
     direct version does not clear every known CVE and name that candidate. That
     compare is `compare_versions`: numeric segments, then stability class, qualifier
     presence, prerelease ordinals, then a lexical tie-break. Not text order (`1.10`
     is above `1.9`). An RC and a final release that share a numeric core are not equal. Ask
     again before editing. Writing that higher version is a new confirm and a
     new preview.
   - **`info`** — `added` / `changed` / `removed` counts and the first rows, then
     a decision row for each remaining `MEDIUM`/`LOW`, each `fixed` id, and each
     introduced `MEDIUM`/`LOW`, from `vulnerabilityDelta` and from the closure
     buckets. License rows whose `verdict` is `review` or `ok`. Do not call the
     bump safe. Those rows are in addition to the full CVE list above, not instead of it.
   - **`unknown`** — the closure was not compared. Quote `error`. Do not describe
     empty buckets as "no change" and do not fill the gap.
   - **`none` after a compare** (`diffReliable: true`, and the target has a
     `vulnerabilities` list) — no coordinate change outside the target, then that
     target OSV result (`relation: target`). Quote the non-guarantee note from
     `notes`. Do not say safe. If the coordinate is a platform or carries
     `managedBy`, and `graphSource` is `depsdev`, do not use that closure
     sentence: an empty public-graph diff is not "no coordinate change". The
     server has no `isPlatform` input.
   - **`none` when nothing was requested to change** — nothing was requested to
     change and the current coordinate was not re-queried. Do not say the graphs
     were compared. Do not invent an empty OSV result. Do not say safe.
     `targets[].vulnerabilities` is absent on that path; an empty list would mean
     it was queried.

   Compared `none`, all-identity `none`, and `unknown` are not "safe" and are not
   "no vulnerabilities".

   `targets[].safeUpgrade` is one extra line on the direct coordinate, labeled
   advisory: `fixesAllKnown` and `version`, or `fixesAllKnown: false` plus
   `reason`. It is not a row per CVE. Do not present it as the version to write.

4. A plugin-marker upgrade comes back as `advisory: unknown` with
   `error: "plugin marker; closure not compared"`. Do not treat that as `none`.

## Decision row

One CVE, in this order. Same row as `/check-deps`. Do not paraphrase `summary`.

1. `relation` — introduced, remaining, fixed, uncompared, or target.
2. `vulnerableNode` as `groupId:artifactId:version`.
3. `id`, linked with `url`. When `url` is empty, use `https://osv.dev/vulnerability/{id}`.
4. `severity`, or `severity unknown` when hydration left it off.
5. `summary`, or the id alone when `summary` is empty.
6. `fixedVersion`, or `fix unknown` when it was omitted.
7. `clearedBySelection`: `selected version is at or above the fix`, `selected version is still below the fix`, or omit this clause when there is no `fixedVersion`. For `relation: fixed`, say the bump no longer selects the vulnerable version.
8. `path` as an arrow chain (`g:a:v → g:a:v`) when present. When `pathOmitted` is present, say the middle was shortened and the leaf is the vulnerable node.
9. When the node is not the target and `clearedBySelection` is false: this coordinate is not the line being edited; clearing it needs a constraint or a higher root, and this preview does not propose that pin.

## Constraints and non-goals

- Do not loop this tool. One Gradle batch, or one deps.dev upgrade.
- Do not treat a failed Gradle result as a deps.dev graph.
- Do not diff two `get_transitive_graph` results. That wrapper drops `relation`,
  and the server already owns the matrix.
- Do not run `mvn dependency:tree` or `./gradlew dependencies` and present the
  text as if OSV had been queried.
- When `graphSource` is `depsdev`, say the graph is isolated: it does not see
  `dependencyManagement`, `ResolutionStrategy`, strict versions,
  `enforcedPlatform`, exclusions, or private artifacts. Do not say that about
  a Gradle result.
- `landed: false` or `rewroteVersionless: true` is at least `review`. If
  `landed` is false, you may offer one retry with `substitution: "module"`.
  The server does not launch that second pair. Do not send it unless the user
  accepts. An accepted retry is a new preview, not an edit.
- An empty OSV list is not verified-clean. Unchanged transitives were not queried.
- License rows are heuristic signals, not legal advice. Only changed coordinates
  are licensed. On the Gradle path, license metadata is not taken from the
  resolve; a missing deps.dev record is `review`, not a known license.

## Fallback (MCP unavailable only)

Say the closure was not compared. Do not reconstruct the diff by hand and do
not treat a dependency tree printout as an OSV result.
