---
name: fix-issue
description: GitHub issue numarasını alır, okur ve otomatik olarak çözer
argument-hint: <issue-number>
user-invocable: true
allowed-tools: Bash(gh *) Read Edit Glob Grep Bash(git *)
effort: medium
---

GitHub issue #$1 için aşağıdaki adımları takip et:

## 1. Issue'yu Oku
```bash
gh issue view $1
```

## 2. Analiz Et
- Issue'nun tam olarak ne istediğini anla
- İlgili dosyaları ve kod bölgelerini tespit et
- Varsa bağlantılı issue'ları veya PR'ları kontrol et: `gh issue view $1 --comments`

## 3. Çözümü Uygula
- Minimal değişiklik yap - sadece issue'nun gerektirdiklerini
- Mevcut kod stiline uy
- Gerekirse test ekle veya güncelle

## 4. Doğrula
- Değişiklikleri gözden geçir
- Testleri çalıştır

## 5. Commit Hazırla
```bash
git add -p
```
Commit mesajı şu formatta olsun:
```
fix: <issue başlığından kısa özet>

Closes #$1
```

Issue'yu kapat ve çözümü özetle.
