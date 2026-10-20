# Content Discovery

Build a high-signal route and file discovery plan for a target using ShakerScan evidence, JS outputs, and framework clues.

**Usage**: `/content-discovery <target_url|scan_id>`

## Instructions

1. Use the `content-discovery-agent` subagent for the deep dive.
2. Load and follow `skills/content-discovery/SKILL.md`.
3. Prefer a completed ShakerScan scan first:
   - if the argument is a scan ID, use it directly
   - otherwise look for the latest completed scan for the target
4. If `js-analyze` output exists for the same target, use it as phase-two input.
5. Return:
   - a concise markdown report
   - a `custom_list` block for ffuf or similar tooling
   - a `custom_endpoints` block for deterministic Scan route seeding when applicable
   - one ready `ffuf` example and one ready ShakerScan `curl`
6. Keep the markdown checklist from the skill updated. Do not move on until every checklist item is complete.
