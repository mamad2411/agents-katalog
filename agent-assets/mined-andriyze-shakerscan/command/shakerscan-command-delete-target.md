# Archive or Delete a Target

Archive a target (hide it, pause its schedules, keep its history) or permanently delete it with
everything it owns (scans, findings, endpoints, evidence, schedules).

**Usage**: `/delete-target <target-id-or-url> [--archive]`

## Rules

- Only on the user's explicit request for that exact target. Never delete as a side effect of
  cleanup, triage, or an audit.
- Deletion is a three-step lifecycle flow, not a plain `DELETE`: a bounded preview, a
  dangerous-tier approval bound to that exact preview, then execution. Show the preview to the
  user and get their confirmation before approving. Do not schedule or batch deletions.
- Prefer archive when the user wants the target out of the way but may want its history: it is
  reversible, deletion is not.
- There is no MCP tool for this; use `shakerscan api`.

## Instructions

1. Resolve the target and show what it is:
   ```bash
   shakerscan api GET "/targets?limit=200&include_inactive=true"
   shakerscan api GET /targets/{id}
   ```

2. Archive (reversible):
   ```bash
   shakerscan api POST /targets/{id}/archive
   ```
   An archived target leaves the default inventory; `GET /targets?include_inactive=true` and the
   Targets page's "Show archived" toggle still list it. Restore it with
   `shakerscan api PATCH /targets/{id} '{"is_active": true}'`.

3. Delete (permanent). Preview first and show the user the counts and any blockers:
   ```bash
   shakerscan api POST /data-deletion/preview '{"kind":"target","target_id":"{id}"}'
   ```
   To delete a whole domain with all its subdomains and linked services, preview
   `{"kind":"domain","domain":"example.com"}` instead; show the user every target in `root_ids`.
   The preview returns `preview_id`, `preview_hash`, `scope_receipt_id`, `expires_at`, cascade
   counts, `blockers` and what is retained. A preview with blockers cannot be executed; report
   them. Stop here and ask the user to confirm the exact preview.

4. After the user confirms, approve that exact preview and execute it:
   ```bash
   shakerscan api POST /arsenal/approvals '{"scope_receipt_id":"{scope_receipt_id}","risk_tier":"dangerous","confirmations":["confirm_authorized","confirm_scope_reviewed","confirm_delete_records"],"approved_by":"{user name}","action_name":"data.records.delete","action_context":{"preview_id":"{preview_id}","preview_hash":"{preview_hash}"},"expires_at":"{expires_at}"}'
   shakerscan api POST /data-deletion/execute '{"preview_id":"{preview_id}","preview_hash":"{preview_hash}","approval_receipt_id":"{approval_receipt.id}"}'
   ```
   Use the user's name in `approved_by`. The approval is one-use and bound to the preview hash;
   a changed selection needs a new preview. A retry of `execute` returns the same durable receipt.

5. Report the result: what was deleted (counts from the receipt), the `files` outcome (erased,
   missing, failed, unproven result files), what was retained, and the receipt id. On a `428`, the preview or approval was missing or stale: start again from step 3.
