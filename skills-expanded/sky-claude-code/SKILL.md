---
name: sky-claude-code
description: >-
  Claude Code'u verimli kullanma (iş akışı rehberi): iyi istek yazma, plan modu ve onaylı
  planlar, CLAUDE.md ve bellek, izin modları ve izin kuralları, alt agent'lar ve paralel iş,
  slash komutları ve skill'ler, hook'lar ile otomasyon, MCP sunucuları bağlama, git worktree
  ile paralel oturumlar, bağlam yönetimi (/compact, /clear), başsız mod (claude -p) ve CI/GitHub
  entegrasyonu, maliyet ve hız ipuçları. "Claude Code'u nasıl daha iyi kullanırım", "workflow",
  "hook nasıl yazılır" dendiğinde kullan. Güncel ayrıntılar için resmi dokümana/claude-code-guide'a bak.
disable-model-invocation: true
---

# Sky · Claude Code İş Akışı

Özellikler hızlı değişir: kesin bayrak/ayar adı gerektiğinde güncel dokümana bak (veya `claude-code-guide` agent'ına sor). Bu skill kalıcı **alışkanlıkları** anlatır.

## İyi istek

- **Hedef + bağlam + kısıt + bitti ölçütü**: "Randevu formuna telefon doğrulaması ekle (`src/features/booking/`). Zod şeması paylaşılsın, mevcut hata stiline uy. Bitti: test + 375px'te kontrol."
- İlgili dosyaları/hata çıktısını ver; "neden" bilgisini ekle (Claude doğru ödünleşimi seçer).
- Büyük iş → önce plan iste (plan modu), onayla, sonra uygula.
- Bir seferde bir konu; konu değişince yeni oturum veya `/clear`.

## CLAUDE.md

Proje kuralları, komutlar, tuzaklar — kısa ve güncel (bkz. `sky-claude-md`). Aynı hatayı iki kez gördüysen bir satır ekle.

## İzinler

- Okuma ve güvenli komutlar (test, lint, typecheck) için izin kuralları → onay yorgunluğu azalır; yıkıcı komutlar her zaman onaylı kalsın.
- Sky'ın `pre-bash` hook'u tehlikeli komutlarda ve şüpheli paketlerde ayrıca onay ister.

## Alt agent'lar

- Geniş arama/okuma, bağımsız inceleme (güvenlik, erişilebilirlik), paralel araştırma → alt agent; ana bağlam temiz kalır.
- Sky agent'ları: `sky-architect`, `sky-builder`, `sky-tester`, `sky-debugger`, `sky-*-reviewer`, `sky-critic`…
- Agent'a net görev + bitti ölçütü ver; sonucunu doğrula (rapor ≠ kanıt).

## Komutlar, skill'ler, hook'lar

- **Slash komutu**: tekrar eden iş akışı (`/sky-check`, `/sky-review`) — `commands/*.md`.
- **Skill**: alan bilgisi ve kurallar, gerektiğinde yüklenir — `skills/*/SKILL.md`.
- **Hook**: her seferinde **mutlaka** olması gereken otomatik davranış (format, güvenlik kapısı, bildirim) — Claude'un hatırlamasına bırakılmaz.
Kendi skill/komut/hook'unu yazmak için `sky-skill-authoring`.

## MCP

Dış araçlar (veritabanı, tarayıcı, Figma, issue takip, dokümantasyon) MCP sunucularıyla bağlanır; yalnızca gerekenleri ekle (her sunucu bağlam ve risk ekler),
en az yetkiyle (salt okunur DB kullanıcısı). Kendi MCP sunucun: `sky-mcp-server`.

## Paralel çalışma

Git **worktree** ile aynı repoda birden çok bağımsız oturum (her biri kendi dalında) — biri özellik yazarken diğeri hata düzeltir; çakışmayan dosyalar.

## Bağlam yönetimi

- Uzun oturumda bağlam dolar: mantıklı bir noktada özetleyip devam et (`/compact`) veya yeni konuya `/clear`.
- Büyük dosyaları tamamen okutmak yerine ilgili bölümü göster; log çıktılarını kırp.
- Önemli kararları dosyaya yaz (plan, ADR) — bağlam sıfırlansa da kalır.

## Başsız mod ve CI

`claude -p "…"` ile betiklerden/CI'dan çalıştırma (ör. PR'da otomatik inceleme, changelog taslağı, hata triyajı); çıktıyı JSON olarak alıp işleme.
GitHub entegrasyonu ile issue/PR'da etiketleyerek görev verme. CI'da izinleri dar tut.

## Kalite döngüsü

İste → plan → uygula → **doğrula** (test, tarayıcı, `/sky-check`) → incele (`/sky-review`) → commit. "Çalışıyor" iddiasını kanıtla iste; ekran görüntüsü, test çıktısı.

## Maliyet ve hız

Doğru modeli seç (karmaşık mimari/hata ayıklama için güçlü model, mekanik işler için hızlı model), gereksiz büyük bağlamdan kaçın, tekrar eden işleri komutlaştır,
alt agent'lara daha hızlı model yeterli olabilir.
