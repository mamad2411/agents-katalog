---
name: pipeline-knowledge
description: "Bir pipeline'in knowledge paketini kurma ve genisletme. Arastirma -> madde -> kaynak -> kapi dongusu; ADR-002 kurallari, kaynak siniflari, celiski kaydi. Triggers: knowledge paketi, knowledge yaz, bilgi biriktir, pipeline egit, arastir ve kaydet, knowledge pack, madde yaz, kaynak ekle, zanaat bilgisi."
---

# pipeline-knowledge — bir hattin bilgisini kurmak

`docs/AI/` bir ajana **"bu repo nasil calisir"** der. `knowledge/` **"bu is nasil iyi
yapilir"** der. Ikisi ayridir ve birlestirilmez.

Bu skill ikincisini kurma islemidir. Kurallar `bm-contracts/docs/AI/ADR-002-knowledge-layer.md`
ve `AGENT_PROTOCOL.md` icinde; burada **uygulama** ve **yasanmis hatalar** var.

## 1) Bir maddenin zorunlu sekli

```markdown
---
topicId: kebab-case-benzersiz
title: Tek cumlelik iddia
appliesTo: [hangi sema, hangi asama, hangi karar]
confidence: high | medium | low
sourceRefs: [kaynak-kimligi, ...]
---

# Baslik

... govde: gercek degil KARAR. "Bu bilgi tasarimda neyi degistirir."

## Sinirlar
Nerede gecerliligini kaybediyor. **ZORUNLU.**
```

**"Sinirlar" bolumu olmayan madde reddedilir.** En cok atlanan ve en pahaliya patlayan
parca budur: siniri yazilmamis bir madde, uygun olmayan baglamda guvenle uygulanir ve
sessizce yanlis sonuc uretir.

**Kaynaksiz madde kabul edilmez.** `sourceRefs` bos olamaz.

## 2) Kaynak siniflari ve hiyerarsi

| kind | Ne | Guvenilirlik |
|---|---|---|
| `measured` | **Bu platformun kendi olcumu** | en yuksek |
| `docs` / `paper` | Resmi dokumantasyon, lisans metni, akademik | yuksek |
| `talk` | Konferans/video anlatimi, adim adim rehber | orta |
| `practice` | Studyo pratigi, aktarilan deneyim | orta |

**Celiski kurali:** `measured` bir madde `talk` bir maddeyle celisirse **olcum kazanir** —
ve madde dosyasi celiskiyi **saklamaz**, ikisini de yazar ve hangisinin neden kazandigini
soyler.

Sebebi: dis kaynaklar genelde **insanli** akislari anlatir (sanatci gorur, begenmezse
tekrarlar). Otomatik hatta o insan yok; ayni teknik farkli davranir, ve farki yalniz olcum
gosterir.

### `measured` kelimesini korumak

**`measured` yalniz kendi olctugumuz sey icindir.** Baskasinin makinesinde cikmis bir rakami
`measured` isaretlemek, ona sahip olmadigi bir tekrarlanabilirlik yukler — ve `measured`
celiskide her sinifi yendigi icin o iddia **haksiz yere** kazanir.

Basliklara dikkat: "## Olculmus parametreler" diye bir baslik altina video rakami yazmak,
dipnotta "bizde olculmedi" yazsa bile yaniltir. **Basliklar okunur, dipnotlar atlanir.**
Dogru ifade: "Kaynakta bildirilen parametreler — bizde olculmedi".

### Ani ile olcumu ayirmak

Kendi projelerimizde **yasanmis** ama burada tekrarlanamayan olaylar icin ayri bir kimlik
kullan (ornegin `bm-observed`, `kind: practice`). Ikisi de bize aittir; biri **olcum**,
digeri **ani**. Karistirmak yukaridaki ayni hatadir.

## 3) URL zorunlu — ve bu bir formalite degil

`talk` bir kaynagin **URL'i yoksa madde denetlenemez.** Bagimsiz bir denetci "bu rakim
gercekten o videoda mi var, yoksa baglama uyarlanmis mi" sorusunu **ayirt edemez**.

Bu bir kez yasandi: dort `talk` kaynagi URL'siz kaydedildi ve en yuk tasiyan rakam —
"su kartta 28 dakika", kullanicinin kartiyla ayni donanim — dogrulanamaz kaldi.

**Alim aninda yaz.** Sonradan bulunmayan kaynak, kaynak degildir.

## 4) Arastirma — `transcriptr` ile

```bash
curl -s --max-time 2 http://localhost:8080/health || \
  ( cd ~/Projects/transcriptr && nohup dart run tool/caption_server.dart >/tmp/tr.log 2>&1 & )
curl -s "http://localhost:8080/research?q=DAR_SORGU&limit=4&provider=claude"
```

Donen `video_id` → `https://youtu.be/<id>`. **URL'i hemen kaydet.**

**Sorguyu dar tut.** Genis sorgu alakasiz video getirir **ve onlardan kendinden emin bir
digest yazar**. Bu yasandi: "game design what makes it addictive" sorgusu kumar ekonomisi ve
bir Family Guy klibi getirdi, ve digest onlardan otoriter gorunumlu "bulgular" uretti.
Getirdigin sonucun **basliklarina bak**; digest'e sonuclarin ilgili oldugunu dogrulamadan
guvenme.

## 5) Referans varsa tarif etme

Elde bir referans artefakti (gorsel, ornek dosya, mevcut uygulama) varsa **kosullandir,
tarif etme**. Bir stili/deseni kelimelerle tanimlamak cok boyutlu bir seyi sirayla anlatmaya
calismaktir; her duzeltme baska bir ekseni bozar.

Bu yasandi: bir sanat stili dort tur metinle tanimlanmaya calisildi, dordu de **farkli bir
yonden** iskaladi; referans gorselleri dogrudan verilip prompt bosaltilinca **tek turda**
oturdu.

Metin, referansin **tasimadigi** sey icin kalir: ozne, kisit, kadraj.

## 6) Dogru seye baktigindan emin ol

Bir kaynagi "inceledim" demek yetmez — **dogru olcekte** incelemek gerekir.

Bu da yasandi: bir stil tanimi, oyunun Steam sayfasindaki *oyun ici* ekran goruntulerinden
yazildi; karakterler orada kartlar uzerinde minik goruyordu. Karakter sanati **boyutunda hic
gorulmeden** kendinden emin bir tanim yazildi ve uc eksende ters cikti.

## 7) Bosluk birakmak uydurmaktan iyidir

Bir alani dolduracak veri yoksa **bos birak ve gorunur kil** — "makul varsayilan" yazma.

Ve bosluklar **simetrik** raporlanmali. Bir eksigin her kosumda bagirip digerinin sessiz
kalmasi cifte standarttir; sessiz olan, digerinin arkasina saklanir.

## 8) Madde koda terfi eder

Bir madde mekanik olarak olculebilir hale gelirse **knowledge'dan cikar, koda girer**.
Gecis madde icinde isaretlenir:

```
→ kodlasti: ContinuityChecker — scope:scene isik degisimi bayrak uretir
```

Saglikli bir knowledge paketinin belirtisi **buyumesi degil**, maddelerinin koda akiyor
olmasidir. Knowledge yorumun yasadigi yerdir; olculebilenin orada isi yoktur.

## 9) Kayit elle tutulan liste olmasin

Kod bir topic kimligi alintiliyorsa, o kimlik listesi **elle tutulmamalidir**. Bu yasandi:
`knowledge/` on madde buyudu, koddaki liste yedide kaldi, koruma testi yakaladi.

Yapisal cozum: kaydi `knowledge/*.md`'den **uret**. O zaman madde eklemek ikinci bir
duzenleme gerektirmez ve madde silmek **derleme hatasi** verir — test zamani hatasindan
gucludur.

## 10) Teslimde

- `_index.md` guncel mi (gorev→madde tablosu + madde tablosu)
- `_sources.md`'de her `sourceRefs` kimligi tanimli mi, URL'ler yazili mi
- Her maddede "Sinirlar" var mi
- Celiski varsa **kaydedildi mi** (saklanmadi mi)
- Kod degistiyse `docs/AI/STATE.md` **ayni commit'te** guncellendi mi

Son madde ayrica yasandi: bir kusur duzeltildi, `STATE.md` bir sonraki commit'e birakildi, ve
iki dakika boyunca belge ile kod zit sey soyledi. `STATE.md`'nin kendi kurali zaten yaziyor:
*guncel degilse teslim eksiktir.*
