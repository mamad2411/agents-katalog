---
name: osv
description: >-
  OSV schema 1.9 (Open Source Vulnerability format): write, validate, publish and consume OSV vulnerability records.
  Use when producing or reviewing an advisory database export, converting advisories to OSV, matching a package
  version or commit against vulnerabilities, or evaluating affected ranges: id prefixes (GHSA, GO, PYSEC, RUSTSEC,
  CVE, x_), modified, withdrawn, aliases, upstream, related, severity (CVSS_V2, CVSS_V3, CVSS_V4, Ubuntu, source),
  affected package (ecosystem, name, purl, wildcard *), SEMVER, ECOSYSTEM and GIT ranges with introduced, fixed,
  last_affected and limit events, versions, references, credits, ecosystem names and suffixes such as Debian:12 or
  Ubuntu:22.04:LTS, the IsVulnerable algorithm, the JSON Schema, and the osv.dev API and data dumps. Targets OSV
  schema 1.9 (1.9.1); 1.7 to 1.8, 1.2 to 1.6 and 1.0 are legacy, upgrade from them; the unreleased main branch is
  tracked as a preview. Triggers: OSV record, OpenSSF vulnerability format, api.osv.dev, schema_version.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# OSV schema

The OSV (Open Source Vulnerability) schema, maintained by the OpenSSF in `ossf/osv-schema`, is a JSON interchange format that describes a vulnerability and maps it precisely to package versions or commit hashes. With this skill the agent writes and validates OSV records, publishes them as a home database, and evaluates them as a consumer to decide whether a package version or commit is affected.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Citations name the heading in the rendered specification (`docs/schema.md`), for example (§ affected[].ranges[].events). When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer (a home database or converter that exports records), aggregator (re-serves other databases' records), or consumer (a scanner or tool that matches packages against records).
- Ecosystems: which package ecosystems the records cover, and whether commit-level (`GIT`) data is available.
- Home database prefix: the registered `id` prefix you publish under, or `x_` for a local database not aggregated by OSV.dev.
- Target version: OSV schema 1.9 (default, release 1.9.1). OSV schema 1.7 to 1.8, OSV schema 1.2 to 1.6 and OSV schema 1.0 are legacy: read them and upgrade from them, never author them. OSV schema main (unreleased) is a preview (posture: track): never emit it. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the `ossf/osv-schema` releases and `CHANGELOG.md` for a newer release, diff `docs/schema.md` and `validation/schema.json` on `main` against the release tag, and update the pins.

## Invariants

1. **`id` and `modified` are required, and `schema_version` too above 1.0.0** (§ id, modified fields). Every other field is optional.
2. **`id` is `<DB>-<ENTRYID>` with a defined prefix.** Use a prefix from the defined database prefix table, or `x_` for a local database (§ id, modified fields). The JSON Schema `prefix` pattern enforces the list.
3. **Timestamps are RFC 3339 in UTC ending in `Z`** for `modified`, `published` and `withdrawn` (§ id, modified fields; § published field; § withdrawn field). Of two records with the same `id`, the later `modified` is authoritative.
4. **`schema_version` is SemVer with no leading `v`; a missing value means `1.0.0`.** Readers process a newer minor or patch version by ignoring unexpected fields (§ schema_version field).
5. **Only the JSON encoding is served**, not YAML, TOML or any other transliteration (§ Format Overview).
6. **`package.ecosystem` is a defined ecosystem and `name` is always present with it**, because the ecosystem defines how the name is read (§ affected[].package field). `purl` has no `@version` part.
7. **Every range has a `type` and at least one `introduced` event; each event object holds exactly one of `introduced`, `fixed`, `last_affected` or `limit`; a range never mixes `fixed` and `last_affected`** (§ affected[].ranges[].type field; § affected[].ranges[].events fields, Requirements).
8. **`GIT` ranges carry `repo` and full-length commit hashes** (§ affected[].ranges[].repo field; `validation/schema.json`, "GIT ranges must use full-length commit hashes").
9. **Top-level and per-package `severity` are exclusive.** If any `affected[].severity` is set, the top-level `severity` must not be (§ affected[].severity field).
10. **A version is affected if it is listed in `versions` or lies in any range**, evaluated with the `IsVulnerable` algorithm (§ affected fields; § Evaluation). `database_specific` never changes the result (§ affected[].ranges[].database_specific field).
11. **`aliases` only for the same vulnerability; `upstream` for supply-chain parents; `related` for the rest.** A distribution record must not list the upstream library's CVE as an alias (§ aliases field; § upstream field; § related field).
12. **`details` is CommonMark; `summary` is plain text.** Display code may strip raw HTML and non-`http(s)` links, and databases are encouraged not to include them (§ summary, details fields).

## Workflow

1. **Pick the version.** Use OSV schema 1.9 and set `schema_version` to `"1.9.1"`. If you are handed older records, plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy or preview line.
2. **Fix the identity.** Choose the `id` from your registered prefix, set `modified` (and `published`), and fill `aliases`, `upstream` and `related` by their definitions.
   -> [`references/ecosystems-and-ids.md`](references/ecosystems-and-ids.md), [`references/fields.md`](references/fields.md)
   ✓ The `id` matches the JSON Schema prefix pattern, and no upstream CVE sits in `aliases` of a downstream record.
3. **Describe the vulnerability.** Write `summary` (one line, about 120 characters at most), `details`, `severity` with a defined type and optional `source`, `references` with defined types, and `credits`.
   -> [`references/fields.md`](references/fields.md)
   ✓ Every CVSS `score` is a vector string that matches its type's pattern; `Ubuntu` scores are lowercase priorities.
4. **Describe what is affected.** One `affected` entry per package, with `package.ecosystem` and `name` (and `purl`), then `ranges` and/or `versions`. Put commit-level data in a separate entry with no `package` and a `GIT` range.
   -> [`references/affected-and-ranges.md`](references/affected-and-ranges.md), [`references/ecosystems-and-ids.md`](references/ecosystems-and-ids.md)
   ✓ Each range has a valid `type`, an `introduced` event, single-key events, and uses `fixed` rather than `last_affected` or `limit` where a fix is known.
5. **Validate.** Check the record against `validation/schema.json` with any JSON Schema 2020-12 validator, then against the prose rules the schema cannot express.
   -> [`references/publishing-and-consuming.md`](references/publishing-and-consuming.md)
   ✓ The record validates, and the Verify list below passes.
6. **Publish** (producer). Serve one JSON file per `id` at a stable URL, bump `modified` on every change, withdraw with `withdrawn` and the reason in `summary`, and register a prefix and ecosystem before contributing to OSV.dev.
   -> [`references/publishing-and-consuming.md`](references/publishing-and-consuming.md)
   ✓ Every published change has a later `modified`, and the prefix is in the defined table.
7. **Consume** (consumer). Match by `ecosystem` and `name` (or purl), evaluate with `IsVulnerable`, ignore unknown fields, and resolve duplicates by `modified`.
   -> [`references/affected-and-ranges.md`](references/affected-and-ranges.md), [`references/publishing-and-consuming.md`](references/publishing-and-consuming.md)
   ✓ `last_affected`, `limit` and `introduced: "0"` are handled, and `ECOSYSTEM` and `GIT` ranges are not compared as SemVer.
8. **Upgrade** (only when asked). Follow the upgrade section for each step from the source line to OSV schema 1.9.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded record validates against the 1.9.1 schema and affects the same versions as before.

## Verify before done

- [ ] `id` and `modified` are present, and `schema_version` is `"1.9.1"` (§ schema_version field; § id, modified fields).
- [ ] The record validates against `validation/schema.json` at tag `v1.9.1`, which rejects unknown top-level fields (`additionalProperties: false`).
- [ ] All timestamps are UTC and end in `Z`.
- [ ] Every `package.ecosystem` is in the defined list, with a suffix only where the ecosystem defines one, and `name` follows that ecosystem's naming rule (§ Defined ecosystems).
- [ ] Every `events` array has an `introduced`, single-key event objects, and no `fixed` together with `last_affected` (§ Requirements).
- [ ] `SEMVER` ranges are used only for real SemVer 2.0 versions and do not overlap; other version schemes use `ECOSYSTEM` with an enumerated `versions` list where possible (§ affected[].ranges[].type field).
- [ ] `GIT` ranges have `repo`, full 40- or 64-character hashes, and a `fixed` event for every cherry-picked fix commit (§ Requirements).
- [ ] Top-level `severity` is absent whenever any `affected[].severity` is set (§ affected[].severity field).
- [ ] `aliases`, `upstream` and `related` follow their definitions (§ aliases field; § upstream field; § related field).
- [ ] Nothing from the main-branch preview is emitted (for example, an `id` validated only against unreleased rules).

## Reference index

- **`references/versions.md`**: every version line with its status, what changed per release, upgrade steps, and the main-branch preview. Load for steps 1 and 8.
- **`references/fields.md`**: every top-level field, `severity` types and sources, `references` types, `credits` types, and the JSON Schema constraints. Load for steps 2, 3 and 5.
- **`references/affected-and-ranges.md`**: `affected`, `package`, `versions`, range types, events, special values, the `IsVulnerable` algorithm and worked examples. Load for steps 4 and 7.
- **`references/ecosystems-and-ids.md`**: the defined ecosystems with their suffix and naming rules, the wildcard name, and the database prefixes. Load for steps 2 and 4.
- **`references/publishing-and-consuming.md`**: validation, publishing as a home database, contributing to OSV.dev, the OSV.dev API and data dumps, consumer rules and common mistakes. Load for steps 5 to 7.

## Related skills

- `purl` for the Package URL in `affected[].package.purl` and OSV.dev purl queries: `npx skills add ScaleDockHQ/scaledock-skills --skill purl`.
- `cyclonedx` for SBOMs and VEX whose components are matched against OSV records: `npx skills add ScaleDockHQ/scaledock-skills --skill cyclonedx`.
- `csaf` for CSAF security advisories, another advisory format: `npx skills add ScaleDockHQ/scaledock-skills --skill csaf`.
- `openvex` for exploitability statements about vulnerabilities found through OSV: `npx skills add ScaleDockHQ/scaledock-skills --skill openvex`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OSV schema specification (rendered)](https://ossf.github.io/osv-schema/): Released (stable), Version 1.9.1 (2026-09-24), checked 2026-10-05.
- [OSV schema docs/schema.md at v1.9.1](https://github.com/ossf/osv-schema/blob/v1.9.1/docs/schema.md): Released, tag v1.9.1 (8e3305d), checked 2026-10-05.
- [OSV JSON Schema validation/schema.json at v1.9.1](https://github.com/ossf/osv-schema/blob/v1.9.1/validation/schema.json): Released, tag v1.9.1, JSON Schema 2020-12, checked 2026-10-05.
- [OSV JSON Schema validation/README.md](https://github.com/ossf/osv-schema/blob/v1.9.1/validation/README.md): Released, tag v1.9.1, checked 2026-10-05.
- [OSV schema CHANGELOG](https://github.com/ossf/osv-schema/blob/v1.9.1/CHANGELOG.md): Released, through 1.9.1, checked 2026-10-05.
- [OSV schema RELEASING.md](https://github.com/ossf/osv-schema/blob/v1.9.1/RELEASING.md): Released, tag v1.9.1, checked 2026-10-05.
- [OSV schema releases](https://github.com/ossf/osv-schema/releases): GitHub releases, latest v1.9.1 (2026-09-24), checked 2026-10-05.
- [OSV schema docs/schema.md on main](https://github.com/ossf/osv-schema/blob/main/docs/schema.md): Unreleased, main at 2780d2a (2026-10-01); Draft posture: track, checked 2026-10-05.
- [OSV schema docs/schema.md at v1.9.0](https://github.com/ossf/osv-schema/blob/v1.9.0/docs/schema.md): Released (superseded), tag v1.9.0 (2026-08-06), checked 2026-10-05.
- [OSV schema docs/schema.md at v1.8.0](https://github.com/ossf/osv-schema/blob/v1.8.0/docs/schema.md): Released (superseded), tag v1.8.0 (2026-07-09), checked 2026-10-05.
- [OSV schema docs/schema.md at v1.7.0](https://github.com/ossf/osv-schema/blob/v1.7.0/docs/schema.md): Released (superseded), tag v1.7.0 (2025-03-05), checked 2026-10-05.
- [OSV schema docs/schema.md at v1.6.7](https://github.com/ossf/osv-schema/blob/v1.6.7/docs/schema.md): Released (superseded), tag v1.6.7 (2024-09-16), checked 2026-10-05.
- [OSV schema docs/schema.md at 1.2.0](https://github.com/ossf/osv-schema/blob/1.2.0/docs/schema.md): Released (superseded), tag 1.2.0 (2022-01-19), checked 2026-10-05.
- [OSV schema docs/schema.md at 1.1.0](https://github.com/ossf/osv-schema/blob/1.1.0/docs/schema.md): Tag (no release or changelog entry), tag 1.1.0 (2021-12-15), checked 2026-10-05.
- [OSV schema docs/schema.md at 1.0.0](https://github.com/ossf/osv-schema/blob/1.0.0/docs/schema.md): Released (superseded), tag 1.0.0 (2021-09-08), checked 2026-10-05.
- [OSV.dev API documentation](https://google.github.io/osv.dev/api/): Documentation, API 1.0, checked 2026-10-05.
- [OSV.dev POST /v1/query](https://google.github.io/osv.dev/post-v1-query/): Documentation, API 1.0, checked 2026-10-05.
- [OSV.dev POST /v1/querybatch](https://google.github.io/osv.dev/post-v1-querybatch/): Documentation, API 1.0, checked 2026-10-05.
- [OSV.dev GET /v1/vulns/{id}](https://google.github.io/osv.dev/get-v1-vulns/): Documentation, API 1.0, checked 2026-10-05.
- [OSV.dev data sources and data dumps](https://google.github.io/osv.dev/data/): Documentation, as published 2026-10-05, checked 2026-10-05.
- [OSV.dev contributing a new data source](https://google.github.io/osv.dev/data/new): Documentation, as published 2026-10-05, checked 2026-10-05.
- [Properties of a High Quality OSV Record](https://google.github.io/osv.dev/data_quality.html): Documentation, 1.0.0, checked 2026-10-05.
