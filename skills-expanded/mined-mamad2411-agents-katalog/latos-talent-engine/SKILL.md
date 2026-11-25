---
name: latos-talent-engine
description: Yetenek taksonomisi ve EXPERTS_TALENT motoru — kültür/sanat/spor ~100 yetenek. Faz 6. (Agency expert-engine ile çakışmaz.)
---

# LATOS Talent Engine

## Instructions
1. `SKILLS_TALENT/TALENT_TAXONOMY.md` oku/güncelle
2. Yetenek başına `EXPERTS_TALENT/{yetenek}/top100_YYYY-MM-DD.md`
3. URL + timestamp zorunlu; doğrulanamayan `unverified`
4. `SKILLS_TALENT/TITLE_TO_TALENT_MAP.md` eşlemesi
5. Aylık READ→DELTA→DIFF→WRITE→DIGEST

**Hibrit:** Skill yoksa `/yetenek-guncelle` inline.

## Examples
- Satranç yeteneği → FIDE kaynaklı isimler (unverified until human review)
- Hitabet → Toastmasters WC referansı

## Performance Notes
- Tam 100 yetenek × 100 uzman fazlı üretim
- İnsan onay kapısı zorunlu

## Troubleshooting
- Hallüsinasyon riski → unverified default
