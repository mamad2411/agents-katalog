---
name: debug-helper
description: Hata mesajı veya stack trace alır, kök nedeni bulur ve düzeltir
argument-hint: <error-message-or-description>
user-invocable: true
allowed-tools: Read Grep Glob Bash(git log *) Edit
effort: medium
---

## Hata Analizi

Hata / Sorun: **$ARGUMENTS**

## Adım 1: Hatayı Anla

Hata mesajını veya açıklamasını parse et:
- Hata türü nedir? (TypeError, SyntaxError, ReferenceError, runtime hatası vb.)
- Stack trace'de gösterilen dosya ve satır numaraları
- Hangi koşulda tetikleniyor?

## Adım 2: İlgili Kodu Bul

Stack trace'deki veya açıklamada belirtilen dosyaları oku.
Şunları ara:
- Hatanın doğrudan kaynağı
- Bu kodu son değiştiren commit: `git log --oneline -10 -- <dosya>`
- Benzer hataların başka yerlerde de olup olmadığı

## Adım 3: Kök Neden

Şu kategorilerden birini tespit et:
- **Tip uyuşmazlığı** - beklenmedik null/undefined, yanlış tip
- **Mantık hatası** - yanlış koşul, off-by-one
- **Async sorun** - race condition, eksik await
- **Bağımlılık** - import hatası, versiyon uyumsuzluğu
- **Ortam** - env değişkeni eksik, path sorunu
- **Veri** - beklenmedik format, eksik alan

## Adım 4: Düzeltme

Düzeltmeyi açıkla ve kodu göster.  
Kullanıcının onayını al, ardından uygula.

## Adım 5: Doğrulama

Düzeltme sonrası ne test edileceğini belirt.
