---
name: nxd-render-static-artifact
description: Render one published NXD data-product release as a self-contained, offline HTML artifact. Use when the user asks to show, document, inspect, share, or create a static page for a published local data product or release. Read only the verified release catalog documents — through native MCP resource operations, or, when the client exposes no resource primitives, through the read-only list_data_product_resources / read_data_product_resource bridge tools. Never start a product, mint credentials, query rows, or substitute a partial catalog response.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  author: nextdata
  version: 0.76.0
---

# nxd-render-static-artifact

Create exactly one release-scoped, self-contained offline HTML file. The file
describes what that release declares; it is not a catalog, a live dashboard, a
query surface, or a conversation widget. It may be previewed, but the
preview is the same completed file written to disk.

## Read and validate before rendering

Use only `nxd://` documents as payload input. Never call an nxd lifecycle,
catalog-action, or query tool to gather artifact content; local file operations
may only construct, validate, and atomically land the HTML output. In
particular, never use `list_data_products`, `describe_models`, `info`, a source
definition, a live endpoint, or a query as a fallback. A failed read is an
artifact failure, not permission to make a partial page.

### Choose one read transport, then keep it

The same `nxd://` documents are reachable two ways. Choose once, before the
first read, and use that one transport for the whole bundle:

1. **Native MCP resource operations** — the default. Use them whenever this
   client exposes resource listing/reading at all.
2. **The `nxd-desktop` bridge tools** `list_data_product_resources` and
   `read_data_product_resource` — only when the client exposes **no** resource
   primitives. Some clients connect to the server and still never surface
   resources to the agent; that is what these exist for. They are read-only
   transports over the identical sealed documents and take a canonical `nxd://`
   uri verbatim.

These two tools are the sole tool exception for artifact input, and only as
transports: they may fetch the `current` / `verified.json` / `outputs` bundle
this skill already requires. Reading `info` or `models` through the bridge is
the same prohibited substitution it is through a resource read — the bundle is
defined by which documents, not by how they arrive. Every other prohibition
above stands unchanged.

Never mix transports inside one bundle: a bundle assembled half from resource
reads and half from tool reads is not a verified release bundle, even when
every document validates.

**Fall back on missing capability, never on a bad answer.** The only trigger is
the client not offering resource operations — a fact about the client, knowable
before the first read. A resource read that *fails* has told you something
true about the release: a malformed uri, an unknown workflow, an integrity
failure, or a supersession redirect. Retrying it through the bridge is not a
fallback, it is asking a second time in the hope of a different answer, and it
will return the same error because both transports run the same reader. Handle
those per [reference/contract.md](reference/contract.md) § Failure boundary.

1. Read the workflow's `current` resource, then read `verified.json` and
   `outputs` at its exact canonical `publish_seq`. Encode the workflow URI
   segment and require canonical decimal sequence text. Require
   `current.release_uri` to equal the canonical encoded `verified.json` URI.
   If the user requested another sequence, state that the requested release was
   superseded, name both sequences, and continue with the current bundle instead
   of returning an error or pretending the historical release was served.
2. Require `schema: nxd-desktop-verified-v1` and
   `trust: artifact_verified` on both `verified.json` and `outputs`; require
   `verified.release.workflow` / `verified.release.publish_seq` and
   `outputs.workflow` / `outputs.publish_seq` to equal `current`.
3. Require `current.definition_id` and `current.artifact_id` to equal
   `verified.release.definition_id` and `verified.release.artifact_id`.
   Require at least `workflow`, `publish_seq`, `run_id`, `definition_id`,
   `artifact_id`, `compiler_id`, and `published_at_unix_ms`. Do not accept or
   emit a `release_id`.
4. Use `data_model.models[].attributes` as the complete ordered display schema,
   then overlay roles from the same model/field in
   `models.models[].fields[].roles`. Validate every local role target and every
   local join endpoint. For a cross-product join with a non-empty
   `to_data_product`, validate the declared target identifiers without
   requiring that remote model in the local `data_model`.
5. Validate every output-level `model_names` / `models[].name` entry, then every
   `ports[].model_names` entry and every `ports[].models[].name` against the
   local display schema. Treat roles as a set
   and require every ordered model and attribute to be usable, including
   unannotated fields and complex `data_type` values.
6. On a superseded-release response, report the requested/current redirect and
   restart the whole bundle from `current`.
   Retry this bounded bundle at most twice. On a missing field, malformed value,
   unsupported schema, mismatch, orphan, read error, or third supersession,
   fail the whole artifact. Do not announce a partial artifact.

Keep artifact status separate from runtime health. A static-artifact failure
does not invalidate a healthy endpoint; a later governed query may still run.

## Render the complete semantic contract

Render this fixed semantic-first order. Do not add catalog, query, results, or
raw-payload screens.

1. **Identity** — name, description, version, and domain.
2. **Model overview** — each model's name, description, and grain/role summary.
3. **Complete schema** — every ordered `data_model` model and attribute;
   show the exact scalar or safely serialized complex type, semantic tags and
   constraints when their keys are present, and every overlaid role/PII marker.
   A `description` key that is present but `null` or `""` is rendered with its
   gloss, not dropped — dropping it is indistinguishable from a field that
   declared one. An unannotated field remains a field.
4. **Joins** — every declared endpoint and cardinality after validating both
   endpoints. Connect two models — visually or in prose — only for a declared
   join. With `joins: []` and per-model `joins: null`, draw no lines and name no
   shape ("a star", "normalized"); shared column names are not relationships. A
   legend reading "none declared" does not license edges above it.
5. **Output exposure and ports** — render output-level `model_names` / `models`
   as their own declaration, then preserve each port and read its own
   `model_names` / `models`. Never replace either surface with a union. Render
   each port's service name and `promises`. A port whose `promises` is `null`
   still renders the label with `null · not declared`, and one whose
   `models` is `[]` renders `[] · none declared` — never omit the row.
6. **Evidence** — only published artifact evidence. Show `compiler_id` only as
   evidence when non-zero; an all-zero ID is not meaningful provenance.
7. **Release provenance** — a closed-by-default `details` after evidence, with
   only `workflow`, `publish_seq`, `trust`, `definition_id`, `artifact_id`,
   `run_id`, and `published_at_unix_ms`.
8. **Diagnostics** — a closed-by-default `details` after provenance, limited to
   resource URIs, schema, and validation state. Never expose raw payloads.

Every value you render that is present-but-empty carries a gloss — no
exceptions, and check each one as you write it. The fixed glosses are
`null · not declared`, `[] · none declared`, and `"" · empty`.
This applies wherever the value appears: a model or field `description`, a
port's `promises` or `models`, and any optional identity field. These states
co-occur in one release — `identity.description` is `null` while a model
`description` is `""`, and registry `joins` is `[]` while a model's `joins` is
`null` — so gloss each value for what it is and never print one for another.
For every optional value, branch on the **key**, never on the value:

- **Key absent** — render nothing at all: no label, slot, dash, or placeholder.
- **Key present** — always render the label, with the value or its gloss. This
  holds for `null`, `""` and `[]` exactly as it does for a real value. Dropping
  the field because the value looked empty, or leaving its cell blank, both
  tell the reader the same false thing: that nothing was declared.

Before writing the file, walk every `null`, `""` and `[]` in the bundle and
confirm each one appears in the page with its gloss. A missing gloss is a
failed artifact, not a cosmetic gap.
Omit a table column whose value is absent in every row; keep it and gloss each
cell when even one row has a value.
Clamp the page to the viewport and give tables and long values their own
horizontal scroll box — the page itself must never scroll sideways in a narrow
side panel. Never render live-only `external_url`,
`environment`, `full_name`, `glossary`, or per-port `infra_profile_name`, and
never render the semantic registry's intentionally empty `data_product` or
`table`.

## File and safety contract

Build a sibling temporary file, validate it, then atomically rename it to
`<workflow>-release-<publish_seq>.html` in the selected safe directory.

**Validating the temp file includes grepping it for each gloss.** Collect every
`null`, `""` and `[]` the bundle declares — a port's `promises`, a field's or
model's `description`, an empty `models` list — and confirm each appears in the
file with its gloss before the rename. A gloss the bundle needs and the file
lacks means either the render dropped a declared value or the gloss text does
not match exactly — check the spelling first, then fix and re-validate rather
than landing the file. This is the step that most often gets skipped, and
skipping it is how an incomplete page reaches the user looking finished.

Escape
all payload-derived text and attribute values. If embedding JSON, escape
`</script>`, U+2028, and U+2029. Use a restrictive local CSP, system-font
fallbacks, and no remote scripts, fonts, requests, or live tool calls. On
failure remove/leave only the temp file per the host's safe cleanup semantics;
never replace an existing release artifact with partial output.

After a same-workflow rebuild, discard cached resource URIs and the prior
current-file assumption. The old file is historical; render the new sequence
before describing or querying the rebuilt product.

## Reference artifacts

Use [reference/contract.md](reference/contract.md) for the exact validation
matrix and [reference/pitfalls.md](reference/pitfalls.md) for safety failures.
`assets/artifact-example.html` is the complete offline example; `assets/kit.html`
is the component reference. Do not use either as a source of live data.

## Verify before handoff

- [ ] One completed offline HTML file, no remote URL, no Query/Catalog/results UI
- [ ] One read transport for the whole bundle; the bridge tools used only
      because the client exposes no resource operations, never to retry a failed
      resource read
- [ ] All data-model fields, complex types, multi-role fields, joins, output-level models, ports and promises shown
- [ ] No line drawn and no shape named without a declared join
- [ ] Grep the finished file for each gloss: every `null`, `""` and `[]` in the
      bundle — including a port's `null` promises and a field's `null`
      description — appears with its gloss. Zero hits for a gloss whose value
      the bundle contains means the artifact is incomplete, not tidy.
- [ ] Page does not scroll horizontally at side-panel width
- [ ] Evidence precedes closed Release provenance and closed Diagnostics
- [ ] Provenance contains only its allowlist; Diagnostics contains only allowed fields
- [ ] All resource and semantic validation passed as one exact release bundle
- [ ] Handoff separately states artifact status, path, and publish sequence
