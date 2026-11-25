---
name: goal
description: "Hedefi calistirilabilir kabul kriterine cevir, kriter yesillenene kadar dur-durak bilmeden calis. Her turda olc, kirmiziyi teshis et, duzelt, tekrar olc. Triggers: goal, hedef, hedefe kadar devam, bitene kadar calis, kriter yesillenene kadar, goal loop."
user-invocable: true
argument-hint: "[hedef cumlesi] veya [check|status|stop]"
---

# /goal — Hedef kilidi: kriter yesillenene kadar durma

"Bitene kadar devam et" tek basina calistirilamaz bir emirdir, cunku **bitti**nin ne oldugunu
soylemez. Bu skill once onu soyletir: hedefi **calistirilabilir kabul kriterlerine** cevirir,
sonra o kriterler yesillenene kadar dongu doner.

Kriter yoksa dongu iki sekilde bozulur: ya ilk makul cikti gorulunce erken durur, ya da
hicbir zaman durmaz. Ikisi de ayni koktenlik: olculemeyen hedef.

## Argumanlar

| Arg | Ne yapar |
|-----|----------|
| *(hedef cumlesi)* | Kriterleri cikar → onaya sunmadan calistir → yesillenene kadar dongu |
| `check` | Sadece kriterleri calistir, rapor et, is yapma |
| `status` | Hangi kriter yesil, kac tur donuldu, son turda ne degisti |
| `stop` | Donguyu bitir, kalan kirmizilari acikca listele |

---

## Faz 1 — Hedefi kritere cevir

Hedef cumlesinden **3-8 kabul kriteri** cikar. Her kriter su testi gecmeli:

> Bir baskasi bu kriteri, benim ne yaptigimi bilmeden, tek komutla calistirip
> yesil/kirmizi diyebilir mi?

| Kotu kriter | Neden kotu | Iyi karsiligi |
|---|---|---|
| "Kart UI'i duzgun gorunuyor" | "Duzgun" olculemez | `sample sahnede 5 kart render ediliyor, screenshot'ta 5 ayri kart bbox'i var` |
| "Testler yaziliyor" | Faaliyet, sonuc degil | `dotnet test → 0 exit, >= 12 test` |
| "Performans iyi" | Esik yok | `1000 kartlik ListView'da frame time < 16ms` |
| "Derleniyor" | Neyin? | `Unity -batchmode -quit → log'da 0 adet "error CS"` |

`.goal/criteria.json` yaz:

```json
{
  "goal": "Sample sahne gercek Guildbound sanatiyla oynanabilir",
  "criteria": [
    {"id":"C1","check":"unity -batchmode -quit ... && ! grep -q 'error CS' log","why":"derlenmeyen sahne oynanmaz"},
    {"id":"C2","check":"ls Assets/Art/Sliced/**/*.png | wc -l → >= 44","why":"sanat gercekten dilimlenmis olmali"}
  ],
  "blocked_by_human": []
}
```

**Kriteri sonradan gevsetme.** Kirmizi kriteri yesillendirmek icin esigi dusurmek, hedefi
degistirmektir; yapilacaksa kullaniciya **acikca** soylenir, sessizce degil.

## Faz 2 — Dongu

Her tur ayni dort adim:

```
OLC → TEshis → DUZELT → TEKRAR OLC
```

1. **Olc.** Butun kriterleri calistir. Kismi degil, hepsini — cunku bir duzeltme baska bir
   kriteri kirabilir ve bunu ancak hepsini kosarak gorursun.
2. **Teshis.** Kirmizi kriterlerden **birini** sec: en cok digerini acan hangisiyse o.
   Kirmizinin sebebini yaz. Sebep yazilmadan yapilan duzeltme tahmindir.
3. **Duzelt.** Sadece o sebebe yonelik. Yoldayken gordugun ilgisiz seyi duzeltme — kaydet,
   gec.
4. **Tekrar olc.** Ayni turda. Yesillendiyse sonraki tura, yesillenmediyse teshis yanlisti;
   yeni teshis yaz, eskisini tekrarlama.

Her tur sonunda `.goal/log.jsonl`'e bir satir: tur no, kriter durumlari, ne degisti, hangi
dosyalar.

## Faz 3 — Ne zaman durur

Ucu de mesru duruş, biri basari:

| Durum | Kosul | Ne yapilir |
|---|---|---|
| **Basari** | Tum kriterler ayni turda yesil | Commit + push, ozet yaz, dur |
| **Ilerleme yok** | 3 ardisik turda hicbir kriter durum degistirmedi **ve** yeni bilgi cikmadi | DUR. Kullaniciya: hangi kriter, uc teshisin neydi, neden tutmadi |
| **Insan kilidi** | Kriter, senin uretemeyecegin bir girdiye bagli (sanat varligi, kimlik bilgisi, urun karari) | O kriteri `blocked_by_human`'a tasi, **kalan kriterlerle devam et**, sonda acikca listele |

"Ilerleme yok" kurali `durmasin` emrinin karsiti degil, kosuludur: ayni duvara dorduncu kez
kosmak devam etmek degil, donmektir. Uc farkli teshis tutmadiysa problem senin
gormedigin bir yerde.

## Faz 4 — Yesil taklidi yasak

Bir kriteri yesillendirmenin sahte yollari — hepsi yasak, hepsi yasanmis:

- Testi `skip`/`ignore` isaretlemek
- Assertion'i gevsetip yesil almak
- Kriter komutunu daha kolay bir komutla degistirmek
- "Manuel dogruladim" deyip komutu hic calistirmamak
- Derleme hatasini kodu yorum satirina alarak susturmak

Bir kriter gercekten yanlis yazilmissa (olcmesi gerekeni olcmuyorsa) duzeltilebilir — ama
duzeltme **ayri ve gorunur** olur: neyin neden degistigi log'a ve ozete yazilir.

## /plan-build ile birlikte

`plan-build` bir **artis** teslim eder; `goal` o artisin hedefe vardigini **dogrular ve
varmadiysa donduru surdurur.** Birlesik akis:

```
plan-build: recon → Fable plan → kapi → Opus dalgalari → entegrasyon
                                                              ↓
goal:                                    OLC → kirmizi varsa TEshis → DUZELT → OLC
                                                              ↓
                                    hala kirmizi ve yapisal ise → Fable'a KALAN plani yazdir
                                                              ↓
                                                     yeni dalga → tekrar OLC
```

Kural: kirmizi **noktasal** ise (tek dosya, tek hata) dogrudan duzelt — yeni plan turu acma,
o pahali. Kirmizi **yapisal** ise (paketler arasi sozlesme yanlis, eksik modul) Fable'a
sadece kalan isi yazdir; plani bastan yazdirma.

## Yapma

- **Kriteri hedefe gore degil, ulasabildigine gore yazma.** Kriter hedefi tarif eder, kapasiteni degil.
- **Tek turda her kirmiziya saldirma.** Paralel duzeltmeler birbirinin olcumunu kirletir.
- **Kismi olcumle tur kapatma.** Bir kriteri duzeltirken digerini kirdigini ancak hepsini kosarak gorursun.
- **Insan kilidini beklerken donguyu durdurma.** O kriteri isaretle, digerleriyle devam et.
