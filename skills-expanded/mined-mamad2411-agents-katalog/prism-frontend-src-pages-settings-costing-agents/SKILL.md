# Costing save and migration protocol

- `costingForm.ts` owns defaults/normalization; normalize before dirty comparison and save. `useCostingSettingsBootstrap.ts` owns reads, `useCostingDerivedState.ts` owns derived state, and `useCostingSettingsSave.ts` owns ordinary saves.
- Reporting-currency symbol and timezone are one `PUT /api/settings/costing`, with the saved `expected_updated_at` baseline. Preserve that combined write so either field cannot overwrite the other from stale state. Currency code changes use migration rather than this ordinary save.
- Successful writes clear timezone preference cache, prime shared reporting-currency state, update the saved form from the response, and bump reference revision. `../useCostingSettingsData.ts` owns post-migration authoritative refresh; do not establish another currency cache.
- `currencyMigrationProtocol.ts` owns bounded inventory/template paging, draft create/chunk/seal, preview, and commit. Preserve inventory identity/generation, settings/epoch CAS, operation IDs, and preview/draft hashes; stale evidence requires a new preview.
- Dialog input/steps and repair edits remain in `../sections/billing-currency/`. Migration drafts retain complete role-keyed cards and missing/pending prices; do not project multi-card templates to a scalar.
- Archive-only unused-FX cleanup is a separate migration operation and preserves the active epoch/template prices. It does not restore FX mapping authoring.
