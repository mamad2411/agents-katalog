---
name: agent-browser
description: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction.
allowed-tools: Bash(npx agent-browser:*), Bash(agent-browser:*)
---

# Browser Automation — agent-browser

Install: `npm i -g agent-browser` → `agent-browser install` (Chrome indir).

## Core Workflow

Her otomasyon bu 4 adımı izler:

1. **Navigate** → `agent-browser open <url>`
2. **Snapshot** → `agent-browser snapshot -i` (ref'leri al: `@e1`, `@e2`, ...)
3. **Interact** → ref kullanarak tıkla/doldur
4. **Re-snapshot** → sayfa değiştikten sonra MUTLAKA yeni snapshot

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "pass" && agent-browser click @e3
agent-browser wait --load networkidle && agent-browser snapshot -i
```

**Önemli:** Ref'ler (`@e1`) sayfa değişince geçersiz olur. Navigasyon / form submit / modal sonrası her zaman re-snapshot.

## Zincirleme

Ara çıktıya ihtiyaç yoksa `&&` ile zincirle (daha hızlı):

```bash
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i
```

## Kimlik Doğrulama

**Tercih edilen — auth vault (şifreli, tekrar kullanılabilir):**
```bash
echo "$PASS" | agent-browser auth save myapp --url https://app.com/login --username user --password-stdin
agent-browser auth login myapp
```

**Profil ile kalıcı oturum:**
```bash
agent-browser --profile ~/.myapp open https://app.com/login
# ... ilk giriş ...
# Sonraki çalıştırmalarda direkt dashboard'a git
agent-browser --profile ~/.myapp open https://app.com/dashboard
```

Detay: `references/authentication.md`

## Temel Komutlar

```bash
# Navigasyon
agent-browser open <url>                    # Sayfaya git
agent-browser close                         # Tarayıcıyı kapat

# Snapshot & Etkileşim
agent-browser snapshot -i                   # Ref'li snapshot (interaktif)
agent-browser snapshot -s "#selector"       # Kapsam sınırlı snapshot
agent-browser click @e1                     # Tıkla
agent-browser fill @e2 "text"               # Temizle + yaz
agent-browser type @e2 "text"               # Temizlemeden yaz
agent-browser select @e1 "option"           # Dropdown seç
agent-browser check @e1                     # Checkbox işaretle
agent-browser press Enter                   # Tuşa bas
agent-browser scroll down 500              # Kaydır

# Bilgi al
agent-browser get text @e1                  # Element metni
agent-browser get url                       # Mevcut URL
agent-browser get title                     # Sayfa başlığı

# Bekleme
agent-browser wait @e1                      # Element çıkana dek bekle
agent-browser wait --load networkidle       # Ağ durulana dek
agent-browser wait --url "**/dashboard"     # URL eşleşene dek
agent-browser wait --text "Welcome"         # Metin görünene dek
agent-browser wait 2000                     # Milisaniye bekle

# Yakalama
agent-browser screenshot                    # Ekran görüntüsü
agent-browser screenshot --full             # Tam sayfa
agent-browser screenshot --annotate         # Numaralı element etiketleri
agent-browser pdf output.pdf               # PDF kaydet

# İndirme
agent-browser download @e1 ./file.pdf      # Element tıklayarak indir
agent-browser wait --download ./output.zip # İndirme tamamlanana dek bekle

# JS
agent-browser eval 'document.title'        # Basit JS
agent-browser eval --stdin <<'EOF'          # Karmaşık JS (önerilen)
JSON.stringify(Array.from(document.querySelectorAll("a")).map(a=>a.href))
EOF
```

## Cihaz & Görünüm

```bash
agent-browser set viewport 375 812         # Mobil boyut
agent-browser set device "iPhone 14"       # Cihaz emülasyonu
agent-browser --headed open <url>          # Görsel mod (debug)
```

## Güvenlik (AI agent'lar için)

```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1  # Sayfa içeriğini işaretle
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"  # Domain kısıtı
export AGENT_BROWSER_MAX_OUTPUT=50000      # Büyük sayfa sınırı
```

## Derinlemesine Referanslar

| Referans | Ne zaman |
|----------|----------|
| `references/commands.md` | Tam komut listesi, tüm seçenekler |
| `references/authentication.md` | OAuth, 2FA, cookie, token yenileme |
| `references/session-management.md` | Paralel oturumlar, state kalıcılığı |
| `references/snapshot-refs.md` | Ref yaşam döngüsü, sorun giderme |
| `references/video-recording.md` | Kayıt, debug |
| `references/proxy-support.md` | Proxy, geo-test |

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
