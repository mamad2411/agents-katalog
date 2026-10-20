---
name: cedar
description: "Cedar policy language 4.5: write, validate and evaluate authorization policies with entities, schemas, templates and PARC requests. Targets Cedar 4.x (language 4.5, SDK 4.13.0) and upgrades policies and schemas from Cedar 3.x and 2.x. Use when adding fine-grained authorization to an application, modelling RBAC or ABAC as permit and forbid policies, designing a Cedar schema, writing entity and context JSON, linking policy templates for sharing features, debugging an unexpected Allow or Deny, upgrading to Cedar 4, or reviewing policies for safety. Triggers: Cedar, cedar-policy, Cedar policy, cedarschema, permit, forbid, when, unless, principal action resource context, PARC, policy template, ?principal, ?resource, template-linked policy, entity hierarchy, Cedar validator, default deny, forbid overrides permit, Amazon Verified Permissions."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.1"
  kind: standard
---

# Cedar

Cedar is an open-source policy language for authorization, maintained in the `cedar-policy` project. Policies `permit` or `forbid` a principal taking an action on a resource in a context, an authorizer combines them into `Allow` or `Deny`, and a validator checks policies against a schema. With this skill the agent writes Cedar policies, schemas and entity data that validate and that decide requests as intended.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: policy author, application integrating the authorizer, or reviewer.
- Model: the principals, actions, resources and hierarchies of the application, and which decisions need attributes or context.
- Target version: Cedar 4.x (current, the default): language version 4.5, implemented by SDK versions 4.10.0 to 4.13.0, pinned to SDK v4.13.0 (Released, 2026-09-15). Cedar 3.x and Cedar 2.x are legacy: read their policies and schemas and upgrade them, never author them. No preview exists. See [`references/versions.md`](references/versions.md).
- Sources: when refreshing, re-read every URL in [Sources](#sources), check the document history for a new language version and the releases page for a new SDK, and update the pins.

## Invariants

1. **Default deny, forbid overrides permit, skip on error.** Any satisfied `forbid` gives `Deny`; else any satisfied `permit` gives `Allow`; else `Deny`. A policy whose evaluation errors is ignored (authorization, Algorithm and Discussion).
2. **Every policy has an effect and a full scope.** `permit` or `forbid`, then `principal`, `action` and `resource`, each unconstrained or constrained with `==`, `in` or `is`; optional `when` and `unless`; a closing `;` (policy syntax).
3. **A request is PARC**: principal, action and resource are entity references and context is a record (authorization, Request creation).
4. **Entity IDs are unique, immutable and never reused**, such as UUIDs, so that a recycled name never inherits old grants (policy syntax; security best practices).
5. **Validate policies against a schema before use.** The authorizer does not validate; requests and entities must follow the schema, or a valid policy may error at run time and be skipped (validation, Request validation expectations).
6. **Guard optional attributes and tags** with `has` or `.hasTag()` before access; access to a missing attribute is an error (operators, `has`).
7. **Template placeholders are `?principal` and `?resource` only**, on the right of `==` or `in` in the scope (templates).
8. **Build dynamic policies from templates, never string concatenation**, to prevent Cedar code injection (security best practices).
9. **Annotations do not affect evaluation**; `@id` is not special in the language (policy syntax, Annotations).

## Workflow

1. **Pick the version.** Target Cedar 4.x at language 4.5 unless the deployment pins an older language version; then use only features at or below it.
   -> [`references/versions.md`](references/versions.md)
   ✓ The language and SDK versions are recorded, and neither is from a legacy line.
2. **Model entities and actions.** Choose entity types, parent relations and attributes, and the actions with the principal and resource types they apply to.
   -> [`references/schema-entities.md`](references/schema-entities.md)
   ✓ A Cedar schema declares every entity type and action, with `appliesTo` for each action.
3. **Write the policies.** Start from least privilege, use `in` for groups and hierarchies, and use `forbid` for guardrails.
   -> [`references/policies.md`](references/policies.md)
   ✓ Each policy has a reason in an annotation and uses only schema names.
4. **Use templates where grants are per user or per resource.** Link templates rather than generating policy text.
   -> [`references/policies.md`](references/policies.md)
   ✓ No policy text is built by concatenating input.
5. **Validate.** Run the validator against the schema and fix every error; review warnings.
   -> [`references/validation-evaluation.md`](references/validation-evaluation.md)
   ✓ Validation reports no errors.
6. **Build requests and entity data.** Produce PARC requests and entity JSON that follow the schema, with schema-based parsing where available.
   -> [`references/schema-entities.md`](references/schema-entities.md)
   ✓ Test requests cover allow, deny and forbid-override cases, and the expected determining policies.
7. **Integrate and review.** Authenticate before authorizing, bound input sizes, log decisions with determining policies and errors, and re-validate on schema change.
   -> [`references/validation-evaluation.md`](references/validation-evaluation.md)
   ✓ Errors in the response are monitored, not silently dropped.
8. **Upgrade** (only when asked). Follow the 2.x to 3.x and 3.x to 4.x checklists in order.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded policies validate under language 4.5 and the test requests return the same decisions.

## Verify before done

- [ ] Every policy validates against the schema with no errors.
- [ ] Optional attributes and tags are guarded with `has` or `.hasTag()`.
- [ ] Entity IDs are UUIDs or other non-reusable IDs, not names.
- [ ] Tests include a request where a `forbid` overrides a matching `permit`.
- [ ] Policies created at run time are template-linked, not concatenated.
- [ ] Authorization responses' errors are logged.

## Reference index

- **`references/versions.md`**: Cedar 4.x, 3.x and 2.x, the language and SDK versions in each, what changed, the upgrade checklists, and why no preview is listed. Load for steps 1 and 8.
- **`references/policies.md`**: policy structure, scope forms, conditions, annotations, operators, templates and patterns. Load for steps 3 and 4.
- **`references/schema-entities.md`**: the Cedar schema format, the JSON schema form, entity and context JSON, and requests. Load for steps 2 and 6.
- **`references/validation-evaluation.md`**: the authorization algorithm, policy evaluation, validation checks and their limits, the 4.13.0 warning change, and security practices. Load for steps 5 and 7.

## Related skills

- `openfeature` when authorization and feature flags share targeting attributes: `npx skills add ScaleDockHQ/scaledock-skills --skill openfeature`.
- `ocsf` to log authorization decisions as audit events: `npx skills add ScaleDockHQ/scaledock-skills --skill ocsf`.
- `rego` for writing the policy in Rego for Open Policy Agent instead: `npx skills add ScaleDockHQ/scaledock-skills --skill rego`.
- `openfga` for relationship-based (Zanzibar-style) authorization models: `npx skills add ScaleDockHQ/scaledock-skills --skill openfga`.
- `cel` for policy conditions written as Common Expression Language expressions: `npx skills add ScaleDockHQ/scaledock-skills --skill cel`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Cedar Policy Language Reference Guide](https://docs.cedarpolicy.com/): reference for Version 4.5, docs commit 3a37098 (2026-09-25), checked 2026-10-02.
- [Cedar document history](https://docs.cedarpolicy.com/other/doc-history.html): language version table, language versions 2.0 to 4.5 (4.5: SDK 4.10.0 to 4.13.0; April 23, 2026), checked 2026-10-05.
- [Cedar v4.13.0 release](https://github.com/cedar-policy/cedar/releases/tag/v4.13.0): Released, v4.13.0 (2026-09-15), checked 2026-10-02.
- [cedar-policy SDK changelog](https://github.com/cedar-policy/cedar/blob/main/cedar-policy/CHANGELOG.md): Released (changelog), main branch; entries 2.0.0 (2023-05-10) to 4.13.0 (2026-09-15), Unreleased language version TBD, checked 2026-10-05.
- [Cedar repository](https://github.com/cedar-policy/cedar): Apache-2.0, main branch, checked 2026-10-02.
- [Basic policy construction](https://docs.cedarpolicy.com/policies/syntax-policy.html): reference, language 4.5, checked 2026-10-02.
- [Operators and functions](https://docs.cedarpolicy.com/policies/syntax-operators.html): reference, language 4.5, checked 2026-10-02.
- [Policy templates](https://docs.cedarpolicy.com/policies/templates.html): reference, language 4.5, checked 2026-10-02.
- [JSON policy format](https://docs.cedarpolicy.com/policies/json-format.html): reference, language 4.5, checked 2026-10-02.
- [How Cedar authorization works](https://docs.cedarpolicy.com/auth/authorization.html): reference, language 4.5, checked 2026-10-02.
- [Entities and context syntax](https://docs.cedarpolicy.com/auth/entities-syntax.html): reference, language 4.5, checked 2026-10-02.
- [Cedar schema](https://docs.cedarpolicy.com/schema/schema.html): reference, language 4.5, checked 2026-10-02.
- [Cedar schema format](https://docs.cedarpolicy.com/schema/human-readable-schema.html): reference, language 4.5, checked 2026-10-02.
- [JSON schema format](https://docs.cedarpolicy.com/schema/json-schema.html): reference, language 4.5, checked 2026-10-02.
- [Policy validation against schema](https://docs.cedarpolicy.com/policies/validation.html): reference, language 4.5, checked 2026-10-02.
- [Cedar security](https://docs.cedarpolicy.com/other/security.html): reference, language 4.5, checked 2026-10-02.
