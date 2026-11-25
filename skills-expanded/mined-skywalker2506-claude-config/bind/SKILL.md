---
name: bind
description: claude-config baglantisi kur — global ve projects CLAUDE.md'yi yonlendiriciye cevir, mevcut icerigi tasit
user_invocable: true
trigger_phrases:
  - /bind
  - bind
  - bagla
  - baglanti kur
  - connect config
---

# /bind — claude-config Baglanti Kurulumu

Bu skill, `~/.claude/CLAUDE.md` (global) ve `~/Projects/CLAUDE.md` (projects) dosyalarini `~/Projects/claude-config` reposuna baglar. Tum kurallar ve konfigürasyon claude-config'den yonetilir hale gelir.

## Adim adim akis

Asagidaki adimlari **sirayla ve kullaniciya sorarak** uygula.

### Adim 1: Durum kontrolu

Su dosyalari kontrol et:

| Dosya | Kontrol |
|-------|---------|
| `~/.claude/CLAUDE.md` | Var mi? "claude-config/CLAUDE.md dosyasini oku" iceriyor mu? |
| `~/Projects/CLAUDE.md` | Var mi? "claude-config/CLAUDE.md dosyasini oku" iceriyor mu? |
| `~/Projects/claude-config/CLAUDE.md` | Var mi? (master dosya) |

Duruma gore rapor ver:
- Her ikisi de baglanmis → "Baglanti zaten aktif. Islem gerekmiyor." → dur.
- Sadece biri baglanmis → hangisinin eksik oldugunu bildir, Adim 2'ye gec.
- Hicbiri baglanmamis → her ikisini de baglanacagini bildir, Adim 2'ye gec.

### Adim 2: Baglanti onayi

Kullaniciya sor:

> claude-config baglantisi kurulsun mu? Bu islem:
> - [baglanmamis dosyalari listele] yonlendirici yapacak
> - Tum kurallar ~/Projects/claude-config/CLAUDE.md'den okunacak
> - Config degisiklikleri sadece claude-config reposu uzerinden yapilacak
>
> Devam edeyim mi?

Hayir derse → dur.

### Adim 3: Mevcut icerik analizi

Baglanmamis her dosya icin:
1. Dosyayi oku
2. Icerigini `~/Projects/claude-config/CLAUDE.md` ile karsilastir
3. Kullaniciya rapor ver:

> [dosya adi]'de su icerikler var:
> - [bolum listesi]
>
> claude-config/CLAUDE.md'de zaten mevcut olanlar: [liste]
> Eksik olup tasinmasi gerekenler: [liste]
> Tasiyayim mi?

Tasinacak icerik yoksa → "Tum icerik zaten claude-config'de." de, Adim 5'e atla.

### Adim 4: Icerik tasima

1. Eksik icerikleri `~/Projects/claude-config/CLAUDE.md` dosyasina ekle (uygun bolume)
2. Kullaniciya ne eklendigini 1-2 satirda ozetle

### Adim 5: Yonlendiricileri yaz

**Global CLAUDE.md** (`~/Projects/claude-config/global/CLAUDE.md`):

```markdown
# Global Claude — Yonlendirici

> **Bu dosya sadece yonlendiricidir.** Tum kurallar, skill tanimlari ve konfigürasyon detaylari `~/Projects/claude-config/CLAUDE.md` dosyasindadir.

---

## Her oturum basinda

1. **`~/Projects/claude-config/CLAUDE.md` dosyasini oku** ve talimatlarini uygula — bu okuma yapilmadan hicbir kural uygulanmaz ve hicbir kod yazilmaz
2. Yanit basinda model etiketi: `(Model Adi)`
3. Dil: kullaniciya Turkce; kod/commit Ingilizce

## Config degisikligi

Degisiklik yapmak icin `~/Projects/claude-config/` reposunda duzenle → `./install.sh` calistir.
**`~/.claude/` altindaki dosyalari dogrudan duzenleme** — `install.sh` ile ezilir.

## Migration sinyalleri

| Sinyal | Aksiyon |
|--------|---------|
| `INSTALL_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` |
| `MCP_SETUP_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` |
| `MIGRATION_NEEDED` | `/migration` calistir |
| `MIGRATION_UPDATE` | Delta uygula, versiyon guncelle |
| `SECRETS_MISSING` | `~/.claude/secrets/secrets.env` duzenle |
| `SECRETS_NONE` | `install.sh` calistir veya secrets.env olustur |
| `CONFIG_UPDATE` | Kullaniciya sor: git pull + install.sh |
| `BIND_NEEDED` | `/bind` calistir — claude-config baglantisi kur |

## Secrets

- Secret degerleri **ASLA** konusma ciktisina, commit'e, public dosyaya veya log'a yazilmaz
- Secret'lar yalnizca `~/.claude/secrets/` altinda
```

**Projects CLAUDE.md** (`~/Projects/claude-config/projects/CLAUDE.md`):

```markdown
# Projects — Yonlendirici

> **Bu dosya sadece yonlendiricidir.** Tum kurallar `~/Projects/claude-config/CLAUDE.md` dosyasindadir.

---

## Her oturum basinda

1. **`~/Projects/claude-config/CLAUDE.md` dosyasini oku** ve talimatlarini uygula
2. Yanit basinda model etiketi: `(Model Adi)`
3. Dil: kullaniciya Turkce; kod/commit Ingilizce

## Degisiklik

Proje kurallarini degistirmek icin `~/Projects/claude-config/` reposunda duzenle → `./install.sh` calistir.
```

Sonra `install.sh` calistir → her iki yonlendirici yerine kopyalanir.

### Adim 6: Dogrulama

1. `~/.claude/CLAUDE.md` oku → yonlendirici mi?
2. `~/Projects/CLAUDE.md` oku → yonlendirici mi?
3. Kullaniciya bildir: "Baglanti kuruldu. Artik tum kurallar ~/Projects/claude-config/CLAUDE.md'den okunuyor."

## Onemli

- **Her adimda kullanici onayi al**
- Mevcut icerikte kullanicinin elle ekledigi ozel kurallar olabilir — bunlari kaybetme
- `install.sh` calistirmadan once degisiklikleri claude-config reposunda commit et

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
