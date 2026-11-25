---
name: ekran
description: Tek bir frontend ekranını docs/sayfa-tasarim-brifi.md + docs/arsiv/tasarimlar/stitch/ mockup'ına göre yeni görsel dile (kâğıt/mürekkep/mühür) geçirir. Yalnız sunum katmanı; veri/iş mantığı değişmez. Argümansız çağrılırsa kuyruktaki sıradaki ekranı seçer. Kullanıcı /ekran yazdığında çalışır.
disable-model-invocation: true
argument-hint: "(boş = kuyruktaki sıradaki) | <kuyruk kodu: ui, 2, shell, 3, 10, 10b, 10c, auth, 13, 11, 9, 14, 21, 16, 12, 18, 19, 20>"
---

# Ekran dönüştür

Amaç: bir ekranı **görünüm olarak** brife uydurmak. Davranış aynı kalır.
Kullanıcıyla **Türkçe** konuş. Kod, yorum, tanımlayıcı İngilizce. UI metni `frontend/messages/tr.json`'da.
**Bir oturum = bir kuyruk kodu = bir commit.** Bitince dur; sıradakine kendiliğinden geçme.

## 0. Hangi ekran? (kuyruk)

Argüman verildiyse onu al. **Argüman boşsa:** `docs/arsiv/planfrontend.md`'yi oku ve aşağıdaki sırada FE satırı `[ ]` olan **ilk** kodu seç. `[x]` ve `[~]` olanları atla. `[~]`, başka biri ya da yarım bırakılmış iş demektir. Seçtiğini tek cümleyle söyle ve başla. Soru sorma.

| Sıra | Kod | Ekran | FE | Model | Dosya(lar) | Mockup (`docs/arsiv/tasarimlar/stitch/proje1-tum-sayfalar/`) |
|---|---|---|---|---|---|---|
| 0 | `ui` | Ortak ilkeller + paylaşılan bileşenler (birincil buton bugün siyah, brifte çam) | FE-05 | Sonnet | `components/ui/button.tsx`, `input.tsx`, `label.tsx`, `components/email-verification-banner.tsx`, `components/skill-picker.tsx` | — (brif §2.1, §2.2, §5.3) |
| 1 | `2` | `/v/[token]` sertifika | FE-13 | Sonnet | `app/v/[token]/page.tsx` | `19-…`, `04-…` |
| 2 | `shell` | AppShell: giriş sonrası tüm sayfaları saran sol menü + mobil çekmece (brif §5) | FE-09 | **Opus** | `components/app-shell.tsx` | `06-…` (sol kısım) |
| 3 | `3` | `/p/[slug]` public profil | FE-14 | Sonnet | `app/p/[slug]/page.tsx` | `15-…`, `05-…` |
| 4 | `10` | `/calismalar/[id]` sayfa iskeleti + zincir + durum butonları | FE-17 | **Opus** | `app/calismalar/[id]/page.tsx`, `transition-actions.tsx` | `06-…` |
| 5 | `10b` | `/calismalar/[id]` görev/çıktı/kanıt formları | FE-17 | **Opus** | `task-form.tsx`, `deliverable-form.tsx`, `evidence-upload-form.tsx` | `06-…` |
| 6 | `10c` | `/calismalar/[id]` tanıklık formları | FE-17 | **Opus** | `attestation-form.tsx`, `attestation-revoke.tsx` | `06-…` |
| 6b | `auth` | Giriş/kayıt/şifre/e-posta formlarının içi (AuthLayout zaten yeni) | FE-15 | Sonnet | `app/giris/*`, `app/kayit/*`, `app/sifre-unuttum/*`, `app/sifre-sifirla/*`, `app/e-posta-dogrula/*` | `proje2-brifi-v2/07-giris-v2.png` |
| 7 | `13` | `/profil` | FE-18 | Sonnet | `app/profil/*` (5 bileşen) | `07-…` |
| 8 | `11` | değerlendirme formu | FE-22 | Sonnet | `app/calismalar/[id]/degerlendirme/*` | `12-…`, `14-…` |
| 9 | `9` | `/calismalar` liste | FE-16 | Sonnet | `app/calismalar/page.tsx` | `09-…` |
| 10 | `14` | kuruluş paneli | FE-20 | Sonnet | `app/kurulus/[id]/panel/page.tsx` | `10-…` |
| 11 | `21` | 404 / hata | FE-11 | Sonnet | `app/not-found.tsx`, `app/error.tsx` | `18-…` |
| 12 | `16` | kurum paneli | FE-21 | Sonnet | `app/kurum/[id]/panel/page.tsx` | `16-…` |
| 13 | `12` | yeni çalışma | FE-19 | Sonnet | `app/calismalar/olustur/page.tsx` | `11-…` |
| 14 | `18` | kurum/kuruluş oluştur + kuruma bağlan | FE-23 | Sonnet | `app/kurum/[id]/baglan/`, `app/kurum/olustur/`, `app/kurulus/olustur/` | `13-…`, `01-…`, `03-…` |
| 15 | `19` | admin doğrulama kuyruğu | FE-24 | Sonnet | `app/admin/dogrulama-kuyrugu/page.tsx` | `02-…` |
| 16 | `20` | admin yetkinlik yönetimi (P2, vakit kalırsa) | FE-25 | Sonnet | `app/admin/skiller/page.tsx` | `08-…` |

**Model kontrolü:** Seçilen ekran **Opus** ise ve sen Opus değilsen, işe başlamadan tek satır yaz ve dur: "Bu ekran (`<kod>`) Opus önerilir: `/model opus` yazıp `/ekran <kod>` ile yeniden başlat, ya da 'devam' de." Kullanıcı "devam" derse sen yap. Opus ekranları riskli olanlar: çok testli (shell 29 test), durum makinesine bağlı butonlar, dosya yükleme akışı. Sonnet ekranlarını Opus da yapabilir, uyarı gerekmez.

**Kuyruk bittiyse** (tablodaki tüm kodlar `[x]`): ekran dönüştürme yapma. Kullanıcıya şunu söyle ve dur: "Ekran kuyruğu bitti. Kalan cila işleri (`docs/arsiv/planfrontend.md` Faz 4): FE-26 durumlar turu, FE-27 responsive turu, FE-28 erişilebilirlik turu, FE-31 tam doğrulama, FE-32 demo provası. Hangisiyle devam edelim?"

Dosya yolları `frontend/` altında. Brif bölümü = kodun numarası (`shell` → §5; `auth` → brif 4–8; `10/10b/10c` → "10. Çalışma detayı"; `18` → brif 17+18 ve 15).
Mockup tam adı: `ls docs/arsiv/tasarimlar/stitch/proje1-tum-sayfalar/ | grep '^19-'`. Ek referans: `docs/arsiv/tasarimlar/stitch/proje2-brifi-v2/`.
Mockup **ilham**dir, kaynak değil. Stitch HTML'ini kopyalama: CDN Tailwind, sahte veri ve farklı sınıf adları içerir. Brif ile mockup çelişirse **brif**, brif ile `docs/arsiv/planfrontend.md` çelişirse yine **brif** kazanır.

**Paralel mod:** `git rev-parse --git-dir` çıktısında `worktrees` geçiyorsa bir worktree'desin; başka oturumlar da çalışıyor demektir. Bu durumda:
- Argüman boşsa seçme; kullanıcıdan kod iste.
- `components/ui/` altına yeni dosya ekleme; gerekirse kendi ekran dosyanın içinde küçük yerel bir parça yaz.
- `tr.json`'da yalnız kendi ekranının bölümüne anahtar ekle.
- Commit'ten sonra kullanıcıya `git pull --rebase origin main && git push origin HEAD:main` öner.

Ayrıntı: `docs/arsiv/gece-plani.md` "Paralel oturumlar".

**Başlarken:** `git status --short` temiz değilse DUR ve kullanıcıya göster. Önceki oturumdan commit'lenmemiş iş kalmış olabilir. Temizse `docs/arsiv/planfrontend.md`'de ilgili FE satırını `[~]` yap.

## 1. Kapsam kilidi

- Kuyruk kodundaki dosyalar + onların `.test.tsx` dosyaları + `tr.json` + gerekirse `components/ui/` altında yeni küçük ilkel. Başka dosyaya dokunma.
- **Yalnız sunum:** JSX yapısı, Tailwind sınıfları, `tr.json` metinleri, `components/ui/` ilkelleri. `fetch`/TanStack Query çağrıları, Zod şemaları, yönlendirme, prop sözleşmeleri, "hangi buton kime görünür" mantığı **değişmez**.
- **Backend'e dokunma.** Veri eksikse uydurma, raporda not düş.
- **Yeni bağımlılık yok** (ikon kütüphanesi, Radix dahil). İkon gerekiyorsa küçük inline SVG ya da ikonsuz.
- **Olmayan veriyi çizme:** istatistik, yüzde, puan, fotoğraf, sayaç yok. Mockup'ta olsa bile.
- **Yeni özellik yok:** brifte "*(Öneri)*" yazan şeyleri (linki kopyala, filtre, GitHub linki vb.) yapma.
- `dangerouslySetInnerHTML`, `localStorage` yasak. Mor/indigo, gradyan, emoji, kalın gölge yasak.

## 2. Hedefli oku (bu kadar, fazlası değil)

1. Brifte o sayfanın bölümü: `grep -n '^### ' docs/sayfa-tasarim-brifi.md` ile satırı bul, yalnız o bölümü oku. Ayrıca §1 (Temel, ~satır 25–110), §3 (hizalama, ~282–300) ve §2'de kullanacağın bileşen alt başlıklarını oku.
2. Mockup PNG'sine bak (Read ile görsel).
3. Hedef dosya(lar) + aynı adlı `.test.tsx` dosyaları.
4. İlkeller (`frontend/components/ui/`): `Button` (variant: primary/secondary/destructive/ghost · size: sm/md/lg), `Card`, `Badge` (default/success/error/warning), `Alert` (error/success/warning/info), `Input`, `Label`, `ChainProgress` (`steps: {label, completed}[]`), `VerifiedSeal`, `AuthLayout`. Önce var olanı kullan. Gerekirse `components/ui/` altına küçük ve testli yeni ilkel ekle (ör. `Skeleton`, `EmptyState`). Başka biri eklediyse yeniden yazma, onu kullan.

## 3. Renk ve yazı — yalnız token

`bg-background` (kâğıt) · `bg-card` · `bg-sand` (navbar/vurgu) · `bg-muted` · `border-border` · `text-foreground` (mürekkep) · `text-muted-foreground` (ikincil) · `bg-success`/`text-success` (çam: birincil buton, mühür, odak) · `text-warning` (aşı) · `text-destructive` (tuğla) · `font-serif` (başlık) · `font-sans` (gövde) · `font-mono` (kayıt no, slogan, tarih damgası). Saydamlık gerekiyorsa `bg-success/10` gibi.

Bitişte hedef dosyalarda şu sayı **0** olmalı:

```bash
grep -cE '(slate|gray|zinc|red|green|blue|indigo|amber|emerald|yellow)-[0-9]{2,3}|bg-white|text-white|text-black' <dosyalar>
```

## 4. Uygula

- Brif tablosundaki sırayla ilerle: düzen → butonlar tablosu → **durumlar** → mobil (375px).
  Durumlar üç tane: yükleniyor (iskelet; "Yükleniyor…" yazısı yok), boş (ne yapılacağını söyleyen metin + varsa aksiyon), hata (+ "Tekrar dene"). Üçü olmadan ekran bitmez.
- **Sayfa kapsayıcısı (AppShell içindeki sayfalar):** sola yaslı, `mx-auto` yok. Kalıp: `max-w-[1120px] px-4 py-8 md:px-6 lg:px-10` (liste/panel), `max-w-[960px] …` (detay/form), `max-w-[640px] …` (dar form). Brifteki 1040/880/560 yan boşluk hariç genişliktir. Kart iç boşluğu `p-4 md:p-6`. Örnek: `app/calismalar/page.tsx`, `app/kurulus/[id]/panel/page.tsx`.
- Ham enum ekranda görünmez (`ACTIVE`, `T1`, `PENDING_APPROVAL`). Yerine `tr.json` etiketi kullan.
- Yeni metin = `tr.json`'a yeni anahtar. **Var olan anahtarların adını değiştirme** (testler anahtara bağlı); metnini brife göre düzeltebilirsin.
- Erişilebilirlik:
  - her form alanında `<label>`
  - görünür focus (`focus-visible:ring-2 focus-visible:ring-success`)
  - hatalar `aria-live` ile duyurulur
  - ikon butonda `aria-label`
  - başlık sırası h1→h2→h3

## 5. Ekrana özel notlar

**`ui` — ortak ilkeller**
- `Button` primary: `bg-slate-900` yerine `bg-success text-card hover:bg-success/90`. Diğer varyantlar brif §2.1'e göre (secondary = nötr/soluk, ghost, destructive = tuğla). Tümüne `focus-visible:ring-2 focus-visible:ring-success focus-visible:ring-offset-2` ve `disabled:opacity-50 disabled:cursor-not-allowed`.
- `Input`: `border-border bg-card`, focus halkası çam. `Label`: `text-foreground` 14px 500.
- `email-verification-banner.tsx`: brif §5.3 (uyarı şeridi, aşı tonları: `bg-warning/10 border-warning/30 text-warning`, hata metni `text-destructive`).
- `skill-picker.tsx`: token renkleri; davranış aynı.
- **Prop API'si değişmez** (variant/size adları aynı; yeni prop ekleme). Bu bileşenler 25+ dosyada kullanılıyor.
- `button.test.tsx` ve diğer ilkel testleri sınıf adı doğruluyor. Görünüm değiştiği için bunlar **bilerek** güncellenir (planfrontend K-5). Her değişen assertion'ı raporda listele.
- Bitince **tüm** frontend testlerini çalıştır (`npx vitest run`), yalnız ilkel testlerini değil. Sayfa testleri sınıfa bağlıysa onlar da kırılabilir.
- Diğer ekranlar butona `className` ile kendi rengini vermiş olabilir. Onlara dokunma, rapora yaz.

**`auth` — giriş/kayıt formları**
- `AuthLayout` ve sayfa iskeleti zaten yeni; yalnız form içleri (`form.tsx`, sayfa içi hata/başarı kutuları) token'a geçer. Hata kutusu → `Alert variant="error"`, başarı → `Alert variant="success"`.
- Form doğrulama (Zod), yönlendirme ve API çağrısı değişmez.

**`2` — `/v/[token]`**
- Brif tablosunu satır satır uygula:
  - çift çerçeveli kart, sağ üstte `VerifiedSeal` lg (−4°)
  - kişi adı Serif 32px; bilgi ızgarası 2 kolon (mobilde 1)
  - T1 uyarısı
  - 4 adımı tamamlanmış `ChainProgress`
  - yetkinlik çipleri
  - Mono damga satırı ("Kayıt no: {token ilk 8}…")
- 404: aynı kart + mühür yerinde kesik çizgili boş daire + "Ana sayfaya dön".
- Telefonda açılır: 375px'de mühür üstte ortalı.
- Yalnız brifin "Veri (yalnız bunlar)" listesindeki alanları kullan.

**`shell` — AppShell**
- Bugün kodda yatay üst bar var. Yerine sol navbar gelecek: 248px, `bg-sand`, sağda 1px çizgi, sabit, tam yükseklik.
- Gruplar: Çalışma / Kuruluşlarım / Kurumlarım / Yönetim. **Hangi link kime görünüyor değişmez**; mevcut koşulları aynen taşı.
- Aktif öğe: `bg-card` + 1px border + solda 2px×20px çam çizgi. `/calismalar/*` alt sayfaları "Çalışmalarım"ı aktif yapar (`usePathname`).
- Alt kısımda kullanıcı kartı ve yukarı açılan menü (Profil, Çıkış).
  - Radix yok: buton + koşullu liste.
  - Esc ve dışarı tıklama menüyü kapatır.
  - `aria-expanded` ve `aria-haspopup` doğru olmalı.
- Mobil (<1024px): 56px yapışkan üst bar + soldan açılan 280px çekmece. Esc, arka plana tıklama veya bir öğeye tıklama çekmeceyi kapatır.
- Tam e-posta gösterilmez, kısaltılır ("meyr…@gmail.com").
- `email-verification-banner.tsx` içeriğin üstüne yerleşir; bileşenin kendisine dokunma.
- `app-shell.test.tsx` (29 test): davranış testleri değişmez (görünür linkler, çıkış çağrısı, hata durumları).

**`3` — `/p/[slug]`**
- 720px ortalı, `/v` ile aynı aile.
- `/v` ile birebir aynı parça varsa (ör. ince üst bar), `components/` altında ortak küçük bir bileşene çıkarabilirsin. Bu durumda `/v` dosyasına da dokunabilirsin, başka refactor yok.
- Doğrulanmış deneyim kartlarında `VerifiedSeal` sm kullan; API token veriyorsa kart `/v/{token}`'a gider.

**`10` / `10b` / `10c` — çalışma detayı (demonun kalbi)**
- Durum makinesi ve izin mantığı değişmez.
- Durum → zincir adımı eşlemesi brif §2.12'de.
- `10`: başlık satırı, meta, `ChainProgress`, "sıradaki adım" kutusu, sekme düzeni ve `transition-actions` butonlarının yerleşimi.
- `10b` ve `10c`: yalnız tablodaki formlar; sayfa iskeletine dokunma.
- FE-17 `[x]` yalnız `10c` bitince olur. `10` ve `10b`'den sonra `[~]` kalır.

**`13` — `/profil`**
- 5 bileşenin her birine aynı kart düzenini uygula: başlık + açıklama + içerik.
- Beyan edilen yetkinlik **gri**, doğrulanmış yetkinlik **çam + mühür** görünür. Bu ayrım demoda gösterilecek, belirgin olmalı.

**`11` — değerlendirme formu**
- Ana mockup `12-…appshell.png`.
- Tanıklık verme anı: gönder butonu birincil (çam), gönderim sonrası başarı mesajı.

**Diğerleri (`9`, `14`, `21`, `16`, `12`, `18`, `19`, `20`):** brif bölümü + genel kurallar yeterli. Büyük dosyalarda (`16`: ~450 satır) bölme yapma, yalnız sınıf ve düzen değiştir.

## 6. Testler — kural

- **Davranış testi değişmez** (metin, rol, tıklama, çağrılan API, yönlendirme). Kırılırsa **kodu** düzelt.
- Yalnız **sınıf adı/DOM yapısı** doğrulayan assertion'lar güncellenebilir; her birini raporda listele.
- Testi geçsin diye silmek, `skip`'lemek ya da beklentiyi gevşetmek **yasak**.
- 3 denemede çözemediğin test olursa dur ve kullanıcıya hatayı göster.

## 7. Doğrula (`frontend/` içinde)

```bash
npx vitest run <hedef klasör veya test dosyaları>
npm run typecheck
npm run lint
```

Ayrıca §3'teki grep = 0 olmalı. Hepsi temiz değilse commit yok.

Sonra kullanıcıya söyle: `npm run dev` açıkken ekranı tarayıcıda **375px ve 1280px** genişlikte kontrol etsin (DevTools → cihaz araç çubuğu).
Seed hesapları: `ayse.yilmaz@posta.test`, `murat.demirci@yelkovanyazilim.test`, `nermin.basaran@cinaralti.edu.test`, `kerem.taskin@cinaralti.edu.test`. Şifre `backend/scripts/seed.py`'de; çıktıya yazma.

## 8. Kapat

1. `docs/arsiv/planfrontend.md`'de FE satırını `[x]` yap (`10`/`10b` için `[~]` kalır).
2. Commit: dosyaları **adıyla** ekle (`git add -A`/`git add .` yasak). Mesaj Türkçe, tek satır + gövdede FE kodu. **Co-Authored-By satırı ekleme.**
   ```
   feat(ui): /v/[token] sertifika sayfası yeni görsel dile geçirildi

   FE-13
   ```
3. Push **yalnız kullanıcı söylerse**.
4. Rapor (kısa):
   ```
   Değişen: <dosyalar> — <ne>
   Doğrulanan: vitest <n geçti> · typecheck · lint · sabit renk 0
   Güncellenen sınıf testleri: <liste veya —>
   Açık not: <eksik veri / brif sapması veya —>
   Sıradaki: <kuyruktaki bir sonraki kod> — devam için /clear, sonra /ekran
   ```
