# JS Analyze

Run JavaScript and frontend attack-surface analysis for a target, completed scan, or supplied JS bundle set.

**Usage**: `/js-analyze <target_url|scan_id|js_path>`

## Instructions

1. Use the `js-analysis-agent` subagent for the deep dive.
2. Load and follow `skills/js-analyze/SKILL.md`.
3. Prefer a completed ShakerScan scan first:
   - if the argument is a scan ID, use it directly
   - otherwise look for the latest completed scan for the target
4. If no useful scan exists, ask whether to queue the canonical Scan with a `balanced` or
   `thorough` budget. Keep active testing off unless the user separately confirms authorization and
   asks for active probes.
5. Return:
   - a concise markdown report
   - a `custom_endpoints` block
   - one ready `curl` example for `/scans`
   - a small `custom_list` block if the JS produces useful path seeds for content discovery
6. Keep the markdown checklist from the skill updated. Do not move on until every checklist item is complete.
