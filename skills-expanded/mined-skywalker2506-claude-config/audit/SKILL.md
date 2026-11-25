---
name: audit
description: Proje kodu taraması — güvenlik, maliyet, performans, gereksiz dosya, API tehlikeleri. Genel veya odaklı.
argument-hint: "[security|cost|performance|cleanup|all]"
---

## /audit

> Model yonlendirmesi: global/model-routing.md

Proje kodunu tarayıp sorunları raporla — bu bir **kod** taramasidir.

### Odak seçenekleri

| Arg | Ne tarar |
|-----|----------|
| *(boş)* veya `all` | Hepsini tarar (genel audit) |
| `security` | Hardcoded key/secret, .env sızıntısı, SQL injection, XSS, güvensiz storage, Firebase rules, API key exposure |
| `cost` | Ücretli servis kullanımı (Firebase, AdMob, RevenueCat, API call), gereksiz network call, büyük asset |
| `performance` | Büyük widget rebuild, gereksiz setState, Hive box leak, memory leak, büyük import, cold start |
| `cleanup` | Gereksiz dosya, kullanılmayan import/dependency, dead code, TODO/FIXME, boş test, .gitignore eksikleri |

### Örnekler

```
/audit                 → genel tarama (hepsi)
/audit security        → sadece güvenlik
/audit cost            → maliyet/ücretli servis odaklı
/audit performance     → performans odaklı
/audit cleanup         → temizlik odaklı
```

---

## Uygulama

Agent tool ile arka planda çalıştır:

```bash
~/Projects/ClaudeHQ/scripts/hq agy --file <şablon-dosyası> --dir <proje> \
  --slug audit-<odak> --json &
```

Tarama mekanik iştir, `agy` üzerinden Gemini'ye gider. Claude'un `Agent` tool'u
Gemini kabul etmediği için model parametresiyle değil, Bash'ten çağrılır.

### Agent prompt şablonu

```
Sen bir kod guvenlik ve kalite uzmanisin. Mevcut projeyi tara.

Proje koku: mevcut calisma dizini
ODAK: [kullanıcının verdiği odak, yoksa "all"]

## TARAMA KURALLARI

- Sadece oku ve raporla — dosya DÜZENLEME, kod YAZMA
- Max 25 tool call — verimli çalış
- Grep/Glob ile pattern ara, şüpheli bulursan Read ile doğrula
- False positive verme — emin olmadığın şeyi raporlama

## TARAMA KONTROL LİSTESİ

### SECURITY (odak: security veya all)

1. **Hardcoded secrets:** Grep ile tara:
   - `apiKey`, `api_key`, `secret`, `password`, `token`, `credential` pattern'ları `.dart`, `.json`, `.xml`, `.plist` dosyalarında
   - `.env` dosyası .gitignore'da mı? `.env` repo'da mı?
   - `google-services.json` ve `GoogleService-Info.plist` içinde prod key var mı?

2. **Firebase güvenliği:**
   - `firebase_options.dart` içinde hassas bilgi var mı?
   - Firestore/RTDB security rules tanımlı mı?

3. **Güvensiz storage:**
   - `SharedPreferences` ile hassas veri saklanan yer var mı? (token, password, userId)
   - `flutter_secure_storage` kullanılıyor mu?

4. **Network güvenliği:**
   - HTTP (HTTPS değil) endpoint var mı?
   - SSL pinning var mı?
   - User input doğrudan URL/query'ye ekleniyor mu? (injection)

5. **Platform güvenliği:**
   - Android: `android:debuggable`, `android:allowBackup="true"`, `usesCleartextTraffic`
   - iOS: `NSAllowsArbitraryLoads`

### COST (odak: cost veya all)

1. **Ücretli servis kullanımı:**
   - Firebase hangi servisler aktif? (Firestore, RTDB, Auth, Storage, Analytics, Crashlytics, AdMob)
   - Her birinin free tier limiti nedir, aşma riski var mı?
   - RevenueCat / IAP konfigürasyonu var mı?
   - Gereksiz Firebase çağrısı (her build'de read/write) var mı?

2. **Asset boyutu:**
   - `assets/` klasörü toplam boyut
   - Büyük resim/font dosyaları (>500KB)
   - Kullanılmayan asset

3. **Dependency maliyeti:**
   - `pubspec.yaml`'daki paketlerden ücretli olan var mı?
   - Gereksiz büyük dependency (toplam app size etkisi)

### PERFORMANCE (odak: performance veya all)

1. **Widget rebuild:**
   - `setState` kullanım sayısı ve yeri (büyük widget'ta gereksiz rebuild)
   - `const` constructor eksikleri
   - Provider/Riverpod doğru kullanım (select, watch vs read)

2. **Memory:**
   - Dispose edilmeyen controller (TextEditingController, AnimationController, StreamSubscription)
   - Hive box açılıp kapatılmayan yer
   - Büyük liste (ListView.builder yerine ListView kullanımı)

3. **Startup:**
   - `main.dart` initialization sırası ve süresi
   - Lazy loading var mı?

4. **Build size:**
   - Kullanılmayan import
   - Tree-shaking'i bozan pattern

### CLEANUP (odak: cleanup veya all)

1. **Gereksiz dosyalar:**
   - `.gitignore`'da olması gerekip olmayan dosyalar
   - Build artifact, cache, generated file repo'da mı?
   - Kullanılmayan test fixture, mock, script

2. **Dead code:**
   - Kullanılmayan Dart dosyası (hiçbir yerde import edilmeyen)
   - Kullanılmayan public class/function
   - Commented-out code blokları (>5 satır)

3. **Dependency hygiene:**
   - `pubspec.yaml`'da kullanılmayan paket
   - `pubspec.lock` ile `pubspec.yaml` tutarlılığı

4. **Code hygiene:**
   - TODO/FIXME/HACK/XXX yorumları (listele)
   - Boş test dosyası (test body'si olmayan)
   - `print()` statement'lar (debug kalıntısı)

## RAPOR FORMATI

Her bulgu için:

```
### [SEVİYE] Başlık
- **Dosya:** path:satır
- **Sorun:** Ne yanlış
- **Risk:** Ne olabilir
- **Çözüm:** Ne yapılmalı
```

Seviyeler:
- 🔴 **KRİTİK** — hemen düzeltilmeli (secret sızıntısı, güvenlik açığı)
- 🟠 **YÜKSEK** — yakında düzeltilmeli (maliyet riski, performans sorunu)
- 🟡 **ORTA** — planlı düzeltilmeli
- 🔵 **BİLGİ** — iyileştirme önerisi

Rapor sonunda özet tablo:

| # | Seviye | Kategori | Dosya | Başlık |
|---|--------|----------|-------|--------|

Ve genel skor (1-10): 10 = temiz, 1 = acil müdahale.
```

## Çıktı

Agent tamamlandığında raporu kullanıcıya göster. Kritik bulgular varsa vurgula.

## Kurallar

- Kod YAZMA, sadece oku ve raporla
- Her bulguyu dosya:satır ile referansla
- Gerçek bulgu ver, spekülatif uyarı verme

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
