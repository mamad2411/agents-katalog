---
name: persona
description: "Kisilik yonetimi — listele, degistir, olustur, duzenle. Triggers: persona, kisilik, personality, karakter degistir."
argument-hint: "[list | switch <name> | create <name> | edit <name>]"
---

# /persona — Kisilik Yonetimi

Aktif kisiligi degistir, yeni kisilik olustur veya mevcut kisiligi duzenle.

## Komutlar

### /persona (argumansiz) veya /persona list
Mevcut kisilikleri listele:
1. `~/Projects/claude-config/config/personas/` altindaki tum `.md` dosyalari oku
2. Her birinin frontmatter'indan `name` ve `description` al
3. `config/active-persona.txt` oku → aktif olani isaretle
4. Tablo olarak goster:

```
| Kisilik | Aciklama | Aktif |
|---------|----------|-------|
| Jarvis  | J.A.R.V.I.S. — sadik AI asistani | * |
| ...     | ...      |       |
```

### /persona switch <name>
1. `config/personas/<name>.md` var mi kontrol et
2. Varsa → `config/active-persona.txt`'e yaz
3. Persona dosyasini oku, kisiligi hemen uygula
4. "Kisilik degistirildi: <name>" bildir
5. Yoksa → mevcut kisilikleri listele, onerilerden birini sec

### /persona create <name>
1. `config/personas/example.md` sablonunu kopyala → `config/personas/<name>.md`
2. Kullaniciya sor: "Bu kisilik nasil olmali? Ton, hitap, tarz, ornek cumleler?"
3. Cevaba gore dosyayi doldur
4. "Kisilik olusturuldu: <name>. Gecis yapmak icin: /persona switch <name>"

### /persona edit <name>
1. `config/personas/<name>.md` dosyasini oku
2. Kullaniciya mevcut icerigi goster
3. "Neyi degistirmek istiyorsunuz?" diye sor
4. Degisikligi uygula

## Kurallar
- `jarvis.md` her zaman kalir — silinemez (varsayilan)
- Aktif kisilik degistiginde CLAUDE.md'deki kisilik blogu degismez — persona dosyasi runtime'da okunur
- Yeni session'da `active-persona.txt` okunur ve o kisilik uygulanir

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
