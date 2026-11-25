---
name: opencode
description: "OpenCode — Zen (web) ve Ollama (lokal) birlikte; sablon her ikisini acar. Triggers: opencode, zen, ollama, kota bitti."
user-invocable: true
---

# OpenCode — Zen (web) + Ollama (lokal)

[OpenCode](https://opencode.ai/) terminal/IDE/desktop icin acik kaynak kod asistani. Claude kotasi bitince veya ek model yolu olarak kullan.

Bu repodaki sablon **her iki yolu da acik tutar:** **`opencode`** (Zen, bulut) + **`ollama`** (lokal). `enabled_providers: ["opencode", "ollama"]`. Ayrinti: [Zen](https://open-code.ai/docs/en/zen), [Providers](https://open-code.ai/docs/en/providers).

## Claude Code model menusu vs baska modeller

**Secici (picker) listesi:** Claude Code’daki “Select model” ekranindaki satirlar (Default / Sonnet / Haiku / Opus) urun icinde **hazir listelenir**; buraya kendi basina **yeni bir satir** (or. Zen’deki `opencode/gpt-5-nano`) **eklenmez** — bu menunun tasarimi boyle.

**Baska modeller yine kullanilabilir** — sadece o liste degil, genelde:

- **`claude --model <model-id>`** ile (ve uygun hesap / kota),
- Ileri kurulumda **yonlendirme** (or. `ANTHROPIC_BASE_URL` + uyumlu API) ile; bu tur modeller **o grafik menude gorunmeden** calisir.

**Zen / OpenCode modelleri** Claude Code menusunun parcasi degil; onlar icin **`opencode`** + **`/models`** veya `~/.config/opencode/opencode.json`.

**OpenCode’da model eklemek:** Zen’de `/connect` + `/models`; Ollama’da `provider.ollama.models` + `ollama pull ...`; `model` anahtarini `saglayici/model` yap — **burada ekleme normaldir**.

## GPT-5 Nano — ekle / kur (ucretsiz bulut)

**Indirilecek bir model dosyasi yok** — `ollama pull gpt-5-nano` calismaz. Zen bulutundan API ile kullanilir.

| Adim | Ne yap |
|------|--------|
| 1 | OpenCode CLI: `npm install -g opencode-ai` veya `cd ~/Projects/claude-config && ./install.sh --opencode` |
| 2 | Varsayilan model zaten `opencode/gpt-5-nano`: `~/.config/opencode/opencode.json` (`model`, `small_model`). Yoksa: `./install.sh --refresh-opencode-config` |
| 3 | Zen anahtari (bir yol yeter): **A)** `opencode` → `/connect` → **opencode** → yapistir — veya **B)** asagiya bak |
| 4 | TUI’de `/models` ile `opencode/gpt-5-nano` secili oldugunu dogrula |

### Zen API anahtarini elle (`~/.config/opencode/opencode.json`)

- Repoda **gercek anahtar yok**; sablonda `provider.opencode.options.apiKey` icin `{env:OPENCODE_ZEN_API_KEY}` kullanilir.
- **Elle degistir:** Ayni dosyada `apiKey` degerini dogrudan `"sk-..."` yapabilirsin (yalnizca bu dosya makinede kalsin — git’e atma).
- **Ortam degiskeni:** `export OPENCODE_ZEN_API_KEY='sk-...'` (orn. `~/.zshrc`) — anahtari dosyada tutmazsin.
- **`./install.sh --refresh-opencode-config`** bu dosyayi sablonla **ez**er; elle yazdigin anahtari kaybedersin — once yedek veya env yolu kullan.

## Durum (claude-config)

- Sablon: `claude-config/templates/opencode.json` → `install.sh` ilk calistirmada `~/.config/opencode/opencode.json` **yoksa** kopyalar (mevcut dosyayi ezmez).
- Eski tek-saglayici config varsa sablonu zorla yaz: `./install.sh --refresh-opencode-config` (once `opencode.json.bak.<tarih>` yedegi alinir).
- CLI: `npm install -g opencode-ai` veya `./install.sh --opencode`
- Kimlik bilgisi: Zen icin `/connect` → `opencode` → [opencode.ai/auth](https://opencode.ai/auth) uzerinden API anahtari (OpenCode’un sakladigi yer: `~/.local/share/opencode/auth.json`).

## 1) OpenCode Zen — ucretsiz (sinirli sure / kosullu) web modelleri

Zen, OpenCode ekibinin [test ettigi modeller](https://open-code.ai/docs/en/zen) listesi; **ucretsiz** olanlara ornekler (fiyatlandirma tablosuna gore; promosyonlar degisebilir):

| Model ID (Zen) | Not |
|----------------|-----|
| `opencode/gpt-5-nano` | Ucretsiz (tablo) |
| `opencode/minimax-m2.1-free` | Ucretsiz, sinirli sure |
| `opencode/glm-4.7-free` | Ucretsiz, sinirli sure |
| `opencode/kimi-k2.5-free` | Ucretsiz, sinirli sure |
| `opencode/big-pickle` | Ucretsiz, sinirli sure |

**Uyari:** Ucretsiz Zen modellerinin bir kisminda gizlilik notu: gelistirme icin veri toplanabilir. Tam liste ve guncel fiyat: [Zen — Pricing & Privacy](https://open-code.ai/docs/en/zen).

### Akis

1. `opencode` ac
2. `/connect` → **opencode** sec → [opencode.ai/auth](https://opencode.ai/auth) ile anahtar yapistir
3. `/models` ile model sec (ornek: `opencode/gpt-5-nano`)

Varsayilan sablon `model` / `small_model`: `opencode/gpt-5-nano`. Anahtar yoksa once `/connect` yap veya `/models` ile `ollama/...` sec.

## 2) Ollama — tamamen lokal, API anahtari yok

```bash
ollama pull qwen2.5-coder:7b
cd ~/Projects/SeninProje && opencode
```

TUI: `/models` → `ollama/qwen2.5-coder:7b`

## Yapilandirma dosyalari

- Global: `~/.config/opencode/opencode.json`
- Kaynak sablon: `~/Projects/claude-config/templates/opencode.json`
- `enabled_providers`: `["opencode","ollama"]` — sadece lokal istiyorsan `["ollama"]` yap

## Hizli komutlar (install.sh → `~/.zshrc`)

| Komut | Ne acar |
|-------|---------|
| `claude-free` | OpenCode TUI, model `opencode/gpt-5-nano` (Zen; TUI icinde /connect ile anahtar) |
| `claude-local` | OpenCode TUI, model `ollama/qwen2.5-coder:7b` (once `ollama pull qwen2.5-coder:7b`) |

Arguman vermezsen mevcut dizin (`.`) kullanilir ornek: `cd ~/Projects/Foo && claude-local`.

## claude-config senkron

```bash
cd ~/Projects/claude-config && ./install.sh
```

- CLI: `./install.sh --opencode`
- `opencode.json` sablonla esitle (ikisi birden): `./install.sh --refresh-opencode-config`

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
