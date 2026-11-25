---
name: alibaba-product-publishing
description: Prepare, create, copy, edit, repair, validate, and—only with explicit authorization—save or submit Alibaba.com seller product listings through an authenticated browser or another user-requested supported publishing channel. Use when an agent must map Excel, CSV, structured records, product-material folders, templates, or existing products into Alibaba.com listing fields; handle titles, models, attributes, SKUs, prices, packaging, logistics, after-sales settings, customs codes, or description templates; prevent cross-product value leakage; resume interrupted batches; or hand off verified edit pages. Apply merchant-specific behavior only from current-task instructions or an explicit merchant configuration.
---

# Alibaba.com Product Publishing

Prepare and verify Alibaba.com product listings without assuming any merchant, brand, category, template, shipping method, or submission policy.

## 1. Apply instruction precedence

Resolve behavior in this order:

1. Follow the user's explicit instructions for the current task.
2. Follow an explicitly supplied merchant or batch configuration.
3. Preserve valid values already present on the target product or source template.
4. Apply the safe defaults in this skill.

Do not carry settings from another merchant, task, browser session, or prior conversation unless the user explicitly supplies them as current context.

Read [references/merchant-config.example.yaml](references/merchant-config.example.yaml) when configuring a merchant or batch. Treat it as a schema and example, not as active values.

## 2. Enforce safe defaults

Use these defaults when the user and merchant configuration are silent:

- Preserve existing images, selling points, box specifications, templates, logistics settings, and after-sales settings.
- Do not invent a brand, model prefix, template name, customs code, SKU, price, unit, dimension, weight, certification, or delivery promise.
- Leave optional empty fields unchanged and record `skipped_empty`.
- Mark missing or ambiguous required values `needs_attention`.
- Keep edit pages open for review.
- Do not click the product-level Save, Submit, Publish, or equivalent final action.

Treat a request to prepare, fill, continue, process, or upload products as authorization to edit applicable fields, not as authorization to save or submit. Require explicit current-task authorization whose scope identifies the products and the requested final action.

Use this default endpoint:

```text
read sources → bind product identity → fill real controls → verify page state → hand off
```

## 3. Check channel capabilities

Before writing, verify that the selected channel can:

- reuse or establish the intended authenticated seller session;
- inspect current URLs, visible labels, controls, dialogs, and validation messages;
- perform genuine user-facing click, type, select, check, and upload actions as needed;
- read authoritative post-action state;
- distinguish multiple product pages or tabs;
- pause safely for user-only steps such as CAPTCHA.

Read [references/browser-capability-contract.md](references/browser-capability-contract.md) before adapting this workflow to a new browser-control agent or tool.

If the channel cannot meet the requirements, stop browser writes. Continue only with source normalization, mapping, validation planning, or a handoff report.

Prefer an official import, API, or merchant-workbench channel when the user explicitly requests it and it supports the required fields. Otherwise reuse the authenticated browser session selected by the user or already in scope. Do not switch accounts, profiles, browsers, or publishing channels without permission.

## 4. Load merchant and batch policy

Build an effective configuration before writing. Resolve at least:

```yaml
brand_name:
model_prefix:
images_policy: preserve
selling_points_policy: preserve
box_specs_policy: preserve
shipping_mode_policy: preserve
customs_code_policy: source_only
template_policy: preserve
approximation_policy: disallow
save_policy: explicit_authorization
submit_policy: explicit_authorization
```

Use `null` or omission for unset merchant values. Never interpret an example placeholder as a real setting.

If the requested operation conflicts with a merchant policy, explain the conflict and follow the user's current explicit instruction unless doing so would exceed tool permissions or safety boundaries.

## 5. Normalize source data

Create one canonical record per product:

```yaml
product_key:
target_action: create | copy | edit | repair
target_item_id:
template_item_id:
category_path:
brand:
source_model:
publish_model:
title:
attributes: {}
custom_attributes: {}
sku_dimensions: []
sku_rows: []
price_tiers: []
shipping_periods: []
product_dimensions:
net_weight:
package_dimensions:
gross_weight:
logistics:
customs_code:
after_sales:
description_templates: {}
expected_unchanged: []
source_locations: {}
tab_identity: {}
variant_fingerprint:
status: pending
```

Add category-specific fields only when the source or target category requires them.

Before writing:

- Reject `undefined`, `null`, `NaN`, unparsed objects, or those literal strings as page values.
- Reject unparseable required numbers and unclear units.
- Preserve identifiers such as model numbers and SKU codes as text.
- Keep source values and page-standardized values separately when mapping is necessary.
- Record the source location for each material value so discrepancies are auditable.
- Do not let one invalid product block independent products whose identities and data are valid.

## 6. Map source values without losing precision

Read the target page's actual enumerations before mapping source values.

Use this structure when source and page vocabularies differ:

```yaml
source_value:
page_standard_value:
exact_custom_value:
mapping_basis:
approximation_used: false
```

- Select an exact page value when one exists.
- If the page only provides a broader valid value, select it and preserve the precise source value in an appropriate custom field when permitted.
- Approximate only when the effective configuration permits it; record the basis.
- Otherwise leave the field unresolved and mark `needs_attention`.
- Never replace precise source capacity, power, voltage, chemistry, dimensions, or certifications with an unsupported guess.

## 7. Bind each page to the correct product

Never bind products by tab order alone. Use the strongest available evidence:

1. Product `itemId` or another unique platform identifier.
2. Existing model or unique product code.
3. Unique title combined with category or product state.
4. A task-local page binding already verified in the current browser session.
5. Source folder or filename.
6. User confirmation.

Record:

```yaml
tab_identity:
  browser_tab_id:
  url:
  item_id:
  model:
  title:
  evidence: []
```

Treat tab identifiers as session-local evidence. After a browser restart or navigation reset, verify identity again using URL, item ID, model, and title. Mark uncertain pages `failed_identity` and do not modify them.

Compare images for identity only when the user permits image inspection. Never change image fields merely because images were used as evidence.

## 8. Write only through real controls

Use genuine interactions with the unique visible control representing the target field.

Do not:

- set `value`, `checked`, `innerHTML`, DOM attributes, or framework state through page evaluation;
- call native setters and synthesize events to imitate user input;
- address controls by a global numeric index;
- inject values into hidden inputs, mirrors, or cloned controls;
- claim success based only on a mutated DOM snapshot.

Use page evaluation only for read-only discovery and verification.

For each field:

1. Refresh the page structure when the form or dialog changed.
2. Locate the field by a stable attribute, exact visible label, accessible name, or uniquely scoped container.
3. Narrow multiple matches until one intended visible control remains.
4. Perform the real interaction.
5. Read the smallest authoritative signal proving the new state.
6. Compare the result with the normalized target value.

Do not hide ambiguity with a generic first-match operation.

For controlled or autocomplete inputs:

```text
locate unique visible input
→ enter the exact value
→ read back while focused
→ allow component processing
→ blur through a stable unrelated control
→ read back again
```

Correct unexpected expansion, truncation, replacement, or clearing immediately. Use Tab only after confirming that the specific component treats Tab as the intended commit action.

## 9. Apply field-specific rules conditionally

Read [references/field-playbook.md](references/field-playbook.md) before editing any applicable complex field such as custom attributes, SKUs, tiered prices, shipping periods, packaging, logistics, templates, or customs codes.

Apply only fields present in the target category and required by the source or effective configuration. Record absent conditional fields as `not_applicable`; do not fail a product because another category supports a field that this category does not.

Separate:

- `common_fields`: values proven safe for every product in the batch;
- `variant_fields`: title, model, power, voltage, capacity, attributes, SKUs, prices, dimensions, packaging, and other product-specific values.

Compare every variant field per product. Never infer that a field is common merely because most products share it.

## 10. Process batches conservatively

Allow parallel work only for source reading, read-only page discovery, opening tabs, and identity mapping. Write product forms serially unless the channel provides isolated transactional operations with independent verification.

For a new category, copied-template workflow, complex SKU design, high-risk logistics setup, or authorized submission batch, complete one representative product first. Verify it before continuing the batch.

Use these states:

```text
pending → mapped → opened → filled → verified → ready_for_handoff
```

Use additional states as needed:

- `skipped_empty`
- `skipped_by_policy`
- `not_applicable`
- `needs_attention`
- `failed_identity`
- `saved` or `submitted` only after explicit authorization and authoritative confirmation

When an action times out, inspect whether it already took effect before retrying. Do not repeat clicks blindly.

## 11. Verify against the source

Capture the page's authoritative actual values for every applicable target field. Compare:

- strings and template names exactly after intentional whitespace normalization;
- numbers after normalizing display separators and precision;
- units exactly or through an explicit documented conversion;
- enumerations and multiselects as complete sets;
- SKU dimensions, options, combination rows, codes, prices, and inventory;
- price tiers by quantity, price, currency, and unit;
- shipping periods by quantity threshold and delivery days;
- policy-controlled fields against both their intended value and expected unchanged state.

Generate source and page fingerprints from applicable variant fields, including at least:

```text
publish_model + title + custom_attributes + selected_sku_options
+ price_tiers + product_dimensions + package_dimensions + gross_weight
```

Use fingerprints as an exception detector, not as a substitute for field checks:

1. Require the page fingerprint to correspond to the bound source record.
2. Flag different source fingerprints that produce identical page fingerprints.
3. Detect leftover template titles, models, SKUs, dimensions, weights, or prices.
4. Expand any fingerprint anomaly into a field-by-field comparison.

Do not mark products with identity uncertainty, required-field errors, cross-product leakage, or template residue `ready_for_handoff`.

## 12. Resume safely

Maintain a compact task ledger:

| product_key | tab_identity | item_id | publish_model | status | last_stage | error |
|---|---|---|---|---|---|---|

After a browser or control-session reset:

1. Read the current pages or tabs again.
2. Rebind each page using current URL, item ID, model, and title.
3. Never bind identical new-product URLs by tab order.
4. Read current page values to determine whether the previous action succeeded.
5. Resume from verified state and avoid repeating confirmed external actions.

## 13. Hand off clearly

Keep all intended edit pages available when the channel permits. Report:

```text
total products / ready_for_handoff / needs_attention / failed_identity

For each product:
- product_key, item_id, and publish_model
- fields filled and verified
- fields preserved or skipped by policy
- unresolved fields and reasons
- whether the edit page remains available
- whether any save or submission occurred
```

Never imply that a product was saved, submitted, published, or accepted by the server unless an authoritative response proves it.

## 14. Save or submit only with explicit authorization

When the user explicitly authorizes saving or submission for a clear product scope:

1. Reverify identity, required fields, policy-controlled fields, fingerprints, and template residue.
2. Confirm the intended final-action button is unique, visible, enabled, and correctly labeled.
3. Perform one real action and wait for navigation, a structured response, or another authoritative result.
4. Handle confirmation dialogs deliberately.
5. Do not treat a click event or correct-looking DOM as server success.
6. Confirm a success URL, structured success flag, returned product ID, clear server-backed status, or equivalent authoritative signal.
7. When possible, verify the product ID, title, and state in product management.
8. Stop and request user action for CAPTCHA, account verification, or other user-only challenges.

If authorization is missing, ambiguous, expired, or narrower than the current batch, stop at `ready_for_handoff`.

## Completion checklist

- [ ] Resolve current instructions and merchant configuration without importing another merchant's defaults.
- [ ] Confirm channel capabilities and authenticated account scope.
- [ ] Normalize all product records and reject dirty required values.
- [ ] Bind every writable page using product identity evidence.
- [ ] Write only through unique real controls.
- [ ] Verify applicable common and variant fields against source data.
- [ ] Preserve or modify images, selling points, box specifications, logistics, templates, and other policy fields exactly as configured.
- [ ] Detect cross-product leakage and copied-template residue.
- [ ] Record unresolved or inapplicable fields honestly.
- [ ] Leave pages ready for review unless explicitly authorized to save or submit.
- [ ] Confirm any authorized server-side result with authoritative evidence.
