---
name: ralph
description: "Convert PRD to prd.json for Ralph autonomous agent loop. Triggers: convert prd, ralph json, create prd.json, start ralph."
user-invocable: true
---

# Ralph PRD Converter

Converts PRD markdown to `prd.json` for autonomous execution.

## Output Format

```json
{
  "project": "[Project Name]",
  "branchName": "ralph/[feature-kebab-case]",
  "description": "[Feature description]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": ["Criterion 1", "Typecheck passes"],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

## Story Size Rule

Each story must be completable in ONE iteration (one context window).

Right-sized: add a DB column, add a UI component, update server action.
Too big: "build entire dashboard" — split into schema, queries, UI, filters.

## Story Order: Dependencies First

1. Schema/database (migrations)
2. Backend logic
3. UI components
4. Dashboard/summary views

## Acceptance Criteria

Must be verifiable. Always include `"Typecheck passes"`. UI stories add `"Verify in browser"`.

Bad: "Works correctly". Good: "Filter dropdown has options: All, Active, Completed".

## Conversion Rules

1. Each user story → one JSON entry
2. IDs: sequential US-001, US-002...
3. Priority: dependency order
4. All stories: `passes: false`, empty `notes`
5. branchName: `ralph/[feature-kebab-case]`

## Running Ralph

After creating prd.json, run from project directory:
```bash
~/Projects/claude-config/projects/scripts/ralph.sh [max_iterations]
```

Default: 10 iterations. Each iteration spawns fresh Claude Code instance.

## Archive

If prd.json exists with different branchName, archive first:
- Copy current prd.json + progress.txt to `archive/YYYY-MM-DD-feature/`
- ralph.sh handles this automatically

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
