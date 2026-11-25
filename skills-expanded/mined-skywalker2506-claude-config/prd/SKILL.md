---
name: prd
description: "Generate a Product Requirements Document (PRD) for a new feature. Triggers: create a prd, write prd, plan feature, requirements for, spec out."
user-invocable: true
---

# PRD Generator

## The Job

1. Receive feature description
2. Ask 3-5 clarifying questions (with lettered options for quick "1A, 2C" answers)
3. Generate structured PRD
4. Save to `tasks/prd-[feature-name].md`

Do NOT implement. Just create the PRD.

## Questions Format

```
1. Primary goal?
   A. Option one
   B. Option two
   C. Other: [specify]
```

## PRD Structure

### 1. Introduction/Overview
Brief description + problem it solves.

### 2. Goals
Specific, measurable objectives.

### 3. User Stories
Each story small enough for one focused session:

```markdown
### US-001: [Title]
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] Specific verifiable criterion
- [ ] Typecheck/lint passes
- [ ] [UI stories] Verify in browser
```

Criteria must be verifiable. "Works correctly" = bad. "Button shows confirmation dialog" = good.

### 4. Functional Requirements
`FR-1: The system must...` — explicit, numbered.

### 5. Non-Goals (Out of Scope)

### 6. Technical Considerations (Optional)

### 7. Success Metrics

### 8. Open Questions

## Output

- Format: Markdown
- Location: `tasks/prd-[feature-name].md`

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
