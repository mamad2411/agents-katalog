---
name: commit
description: Staged değişiklikleri analiz edip Conventional Commits formatında commit mesajı oluşturur
user-invocable: true
allowed-tools: Bash(git *)
effort: low
---

## Değişiklikleri İncele

```bash
git diff --staged
git status
git log --oneline -5
```

## Commit Mesajı Oluştur

Conventional Commits formatını kullan:

```
<type>(<scope>): <kısa açıklama>

[isteğe bağlı gövde]

[isteğe bağlı footer]
```

### Type Seçimi
- `feat` - yeni özellik
- `fix` - hata düzeltmesi
- `refactor` - davranış değişikliği olmayan yeniden yapılandırma
- `test` - test ekleme veya düzeltme
- `docs` - yalnızca dokümantasyon
- `style` - biçimlendirme (logic yok)
- `chore` - build, bağımlılık güncellemesi
- `perf` - performans iyileştirmesi
- `ci` - CI/CD değişikliği

### Kurallar
- Başlık satırı 72 karakteri geçmemeli
- Türkçe veya İngilizce - repo'daki mevcut dili kullan
- "ne yaptı" değil "ne yapar" odaklı: "Ekle" değil "Ekledi"
- Breaking change varsa footer'a `BREAKING CHANGE:` ekle

## Uygula

Onaylanan mesajla commit oluştur:
```bash
git commit -m "..."
```
