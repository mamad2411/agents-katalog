---
name: durum
description: docs/PLAN.md'deki ilerlemeyi okur, nerede kalındığını kısaca söyler ve sıradaki maddeyi uygulamaya başlar. Kullanıcı /durum yazdığında çalışır.
disable-model-invocation: true
argument-hint: "(boş) | <madde-no>"
---

# Durum ve devam

Amaç: kullanıcının prompt yazmasına gerek kalmadan, planda kalınan yerden devam etmek.

## 1. Durumu oku (minimum context)

Şu üçünü oku, fazlasını **okuma**:

- `docs/PLAN.md` — tamamını oku (kısa tutulmuş bir dosyadır)
- `!`git log --oneline -5`` — son 5 commit (tam history okuma)
- `!`git status --short`` — çalışma ağacı durumu

Argüman verilmişse (`$1` bir madde numarasıysa) o maddeyi hedefle; verilmemişse **ilk işaretsiz `- [ ]` maddeyi** hedefle.

## 2. Kısa durum raporu ver

Tam olarak bu formatta, uzatmadan:

```
Tamamlanan: <faz/madde sayısı, ör. "Faz 1 bitti, 2.1-2.2 bitti">
Şu an: <hedeflenen madde numarası ve başlığı>
Çalışma ağacı: <temiz | N dosya değişik>
```

Commit edilmemiş değişiklik varsa ve bunlar önceki maddeye aitse, **önce onu sor** — üstüne yeni iş yapma.

## 3. Sıradaki maddeyi uygula

Rapordan sonra **durma, sorma, doğrudan başla.** Kullanıcı `/durum` yazarak zaten "devam et" demiştir.

Uygularken:

- `CLAUDE.md` içindeki çalışma döngüsüne uy: hedefli oku → uygula → hedefli doğrula
- Maddenin detayı `docs/` veya `docs/yetkin360-final-analiz.md` içindeyse **sadece ilgili bölümü** oku (grep ile bul)
- Doğrulama matrisine göre minimum gerekli testi çalıştır

## 4. İstisna — önce onay al

Madde şunlardan birini içeriyorsa, uygulamadan **önce sor**:

- Migration oluşturma/uygulama
- Dosya veya klasör silme
- 3+ dosyayı etkileyen refactor
- Yetkilendirme, kimlik doğrulama, izin mantığı değişikliği
- Bağımlılık ekleme/yükseltme
- Deploy veya dış servise veri gönderme

Bu durumda raporun sonuna tek satır ekle: `Bu madde onay gerektiriyor: <sebep>. Başlayayım mı?`

## 5. Madde bitince

- `docs/PLAN.md`'de kutuyu `- [x]` yap
- Kısa çıktı formatını kullan (Değişen / Doğrulanan / Kalan)
- Commit **atma** — kullanıcı `/bitir` derse o zaman atılır
- Sıradaki maddeye kendiliğinden geçme; kullanıcı tekrar `/durum` yazsın

## Kural

Bu komutun tamamı **kısa** olmalı. Uzun analiz, seçenek listesi, gerekçe anlatımı yapma. Plan zaten kararlaştırılmış işleri içerir — tartışma değil, uygulama zamanı.
