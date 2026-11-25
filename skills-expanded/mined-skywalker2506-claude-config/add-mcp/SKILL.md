---
name: add-mcp
description: "Add optional MCP servers after initial install. Triggers: add mcp, mcp ekle, firebase ekle, flutter ekle, unity ekle."
user-invocable: true
---

# Add MCP — Sonradan MCP Sunucusu Ekle

Kurulum sonrasi ek MCP sunuculari ekler. Mevcut olanlar atlanir.

## Kullanim

```
/add-mcp              → mevcut secenekleri listele, kullanici secsin
/add-mcp flutter      → flutter-dev MCP ekle
/add-mcp firebase     → firebase MCP ekle
/add-mcp unity        → Unity MCP ekle (proje bazli)
/add-mcp flutter,firebase → birden fazla ekle
```

## Mevcut Opsiyonel MCP'ler

| Anahtar | MCP | Komut | Not |
|---------|-----|-------|-----|
| `flutter` | flutter-dev | `claude mcp add -s user flutter-dev -- npx -y flutter-dev-mcp` | 2026-08-04'te default'tan cikarildi (0 cagri) |
| `firebase` | firebase | `claude mcp add -s user firebase -e "SERVICE_ACCOUNT_KEY_PATH=$PATH" -- npx -y @gannonh/firebase-mcp` | `FIREBASE_SERVICE_ACCOUNT_PATH` gerekir (secrets.env) |
| `unity` | unity-mcp | Proje bazli kurulum (asagiya bak) | Unity Editor acik olmali |
| `jcodemunch` | jcodemunch | `claude mcp add -s user jcodemunch -- uvx jcodemunch-mcp` | ~120 tool; `/index` skill'i buna bagli. 2026-08-04'te cikarildi (0 cagri) |
| `context7` | context7 | `claude mcp add -s user context7 -- npx -y @upstash/context7-mcp` | 2026-08-04'te cikarildi (0 cagri) |

## Akis

### 1. Arguman kontrolu

Arguman verilmisse → direkt ekle.
Verilmemisse → listeyi goster, kullanici secsin.

### 2. Zaten kurulu mu?

```bash
claude mcp list 2>/dev/null
```

Secilen MCP zaten listedeyse: "flutter-dev zaten kurulu, atlaniyor" de.

### 3. Gereksinim kontrolu

**firebase** icin:
```bash
grep "^FIREBASE_SERVICE_ACCOUNT_PATH=" ~/.claude/secrets/secrets.env 2>/dev/null
```
Yoksa kullaniciya sor:
> Firebase service account JSON dosyasinin yolu nedir?

Cevabi `secrets.env`'e ekle, sonra MCP'yi kur.

**unity** icin:
1. `unity-mcp-cli` kurulu mu?
```bash
command -v unity-mcp-cli
```
Yoksa: `npm install -g unity-mcp-cli`

2. **SADECE `$(pwd)` dizinini kontrol et** — parent, child veya sibling dizinlere bakma:
```bash
CUR="$(pwd)"
ls -d "$CUR/Assets" "$CUR/ProjectSettings" 2>/dev/null
```
**Her ikisi de** ayni dizinde yoksa → **KURMA**. Kullaniciya de:
> Bu klasor ($CUR) Unity projesi degil. Unity proje kok dizininde (Assets/ ve ProjectSettings/ olan yer) `/add-mcp unity` calistir.

Alt klasorde veya parent'ta Unity projesi olsa bile **o dizine gecmeden kurma**.

3. Her ikisi de varsa → Unity projesi:
```bash
unity-mcp-cli install-plugin "$CUR"
unity-mcp-cli setup-skills claude-code "$CUR"
```

### 4. Kur

**flutter/firebase:** Tablodan ilgili `claude mcp add` komutunu calistir.
**unity:** Adim 3'teki proje bazli komutu calistir.

### 5. Sonuc

Basarili: "[mcp-adi] MCP eklendi. Yeni oturumda aktif olacak."
Unity icin: "Unity MCP kuruldu. Unity Editor'u ac, Tools > MCP Unity > Server Window'dan serveri baslat."
Basarisiz: hatayi goster, yardimci ol.

## Kaldirma

Kullanici "kaldir" / "remove" derse:
```bash
claude mcp remove -s user <mcp-name>
```

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
