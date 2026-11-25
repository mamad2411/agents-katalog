---
name: ajan
description: Gemini alt ajanı (`baton`, eski adı `ajan`, `agy` CLI). Uygulama işini Gemini'ye devretmek, izlemek, düzeltmek ve doğrulamak için. Kullanıcı "geminiye ver", "neon'a ver", "hydrogen'e ver", "flash'a ver", "alt ajana ver", "delege et", "delegate to Gemini", "give this to Gemini", "hand off to a sub-agent", "use neon", "use hydrogen", "use Gemini for implementation" dediğinde veya büyük/tekrarlı uygulama işinde.
---

# ajan — Gemini alt ajanı

`baton` CLI'si `PATH`'te olmalı. `command -v baton` boşsa kendin kurmaya çalışma; kullanıcıya https://github.com/HSGunes/gemini-baton-for-claude-code#quick-start adresini göster ve dur. **Claude planlar, görev/ölçüt yazar, doğrular; Gemini (`agy` `stream-json`) uygular.**

Ana bağlamı korumak için `gemini-baton:ajan-yonetici` (veya `/gemini-baton:devret <iş>`) kullan; aşağısı elle akış içindir.

## Modeller
- Varsayılan otomatik (kullanıcı istemedikçe `--model` verme); mevcut liste için `baton modeller`.
- Kullanıcı yeni/belirli model isterse `--model <aile|tam-kimlik>`; basit/mekanik işler için `--model flash-orta`.
- Varsayılan model kotada veya geçersizse `baton modeller` ile başka bir aile seç.
- Büyük, çok parçalı işte kullanıcı isterse `--orkestra` kullan (varsayılan değildir).

## Akış
1. **Görev** (`GOREV_X.md`, kısa/kesin): okunacak/değişecek dosyalar (adıyla), imzalar, davranış, kabul ölçütleri, test beklentisi, "başka dosyaya dokunma", varsa teşhis. Ortak bağlam: `-g ORTAK.md -g GOREV_X.md` (ör. `examples/GOREV_ORNEK.md`).
2. **Başlat** (arka plan): `baton baslat ETIKET -g GOREV_X.md --yaz DIZIN1 --yaz DIZIN2 [--oku DIZIN] [--model ...]`
   - `ETIKET`: `[A-Za-z0-9._-]`, 1–64 karakter; çalışıyorsa çıkış 3.
   - Çıkış 2 (izin eksik): eksik kuralı bildirip dur; `--izin-ekle` asla otomatik kullanılmaz (yalnız kullanıcı açıkça onaylarsa dar dizinle).
   - `--komut "python3 -m pytest"`: yalnız gerekirse dar önekle; yoksa terminal kapalı (göreve "komut çalıştırma" yaz).
3. **Bekle**: Bash `run_in_background: true` ile `baton bekle ETIKET [ETIKET...]` (ön planda uzun bekleme yok). Durum: `baton durum`.
4. **Denetle**: `baton rapor ETIKET` → diff oku → test/derlemeyi KENDİN çalıştır (rapor kanıt değil).
5. **Düzelt**: `baton devam ETIKET -m "<özet>. Testleri gevşetme; kök nedeni düzelt."` + `baton bekle ETIKET` (arka planda), veya `baton dogrula ETIKET --test "<komut>" --tur 2` (`--tur N`: en fazla N düzeltme, N+1 test; varsayılan 3).
6. **İptal / temizlik**: `baton iptal ETIKET` (yalnız çalışan görevde, yoksa çıkış 1), `baton temizle --gun 7`.

## Kurallar ve token
- Kodu Gemini yazar (Claude kotasını korur); `ajan-yonetici` `sonnet`'te kalır (Opus yalnız kullanıcı isterse).
- `baton izle` kullanma, tam `yanit.md` okuma; `baton rapor` kullan.
- Her `devam` tüm konuşmayı yeniden işler; `--tur` düşük tut, uzadıysa teşhisle yeni görev aç.
- Farklı dosyalara dokunan görevler paralel çalışabilir; aynı dosyaya dokunanlar paralel çalışmaz.
- Etkileşimli `agy` oturumuna dokunma; `--dangerously-skip-permissions` yasak (dar dizin/önek kullan).
- Test gevşetme (silinen assert, büyütülen eşik, skip) kontrolü yap.
