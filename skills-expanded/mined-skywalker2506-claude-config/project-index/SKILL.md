---
name: project-index
description: "Proje index'i yönet — init, show, list, update. L1 katman: on-demand proje detayı."
triggers: project-index, proje indexi, index init, proje özeti, proje detay
---

# /project-index

Proje index sistemi. 3 katman:
- **L0 (auto):** SessionStart hook → `.claude/index.md` varsa `PROJECT_INDEX:` sinyali
- **L1 (bu skill):** On-demand detay, init, güncelleme
- **L2:** jCodeMunch / file tree (gerektiğinde)

## Komutlar

### `/project-index init [proje-adi]`
Mevcut dizin veya verilen proje için `.claude/index.md` oluştur.
Template: `$(cat ~/Projects/claude-config/templates/project-index.md.template)`

Adımlar:
1. `projects.json`'dan proje meta verisini oku (varsa)
2. Dizin yapısına bak (mevcut stack'i tahmin et)
3. Template'i doldur, `.claude/index.md` yaz
4. Test: `bash ~/Projects/claude-config/projects/scripts/project_index.sh` çalıştır — `PROJECT_INDEX:` sinyali görünmeli

### `/project-index show [proje-adi]`
Proje index'ini göster. Argüman yoksa mevcut dizin.

### `/project-index list`
Tüm projelerin index durumunu göster.
`$(for p in $(cat ~/Projects/ClaudeHQ/projects.json | python3 -c "import sys,json; [print(p['path'].replace('~', '/Users/musabkara')) for p in json.load(sys.stdin)['projects']]"); do echo "$p: $([ -f "$p/.claude/index.md" ] && echo '✓' || echo '—')"; done)`

### `/project-index update`
Mevcut `.claude/index.md` dosyasını güncelle (focus alanı genellikle değişir).

## INDEX_CREATE sinyali

`CLAUDE.md` veya herhangi bir hook `INDEX_CREATE` sinyali üretirse → mevcut proje için `/project-index init` çalıştır.

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
