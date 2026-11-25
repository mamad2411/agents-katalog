---
name: kkv-fogyasztovedelmi
description: "KKV fogyasztóvédelmi tanácsadó: webshop checklist, elállási jog, jótállás, panaszkezelés — Fgytv. + e-ker. tv. alapján"
mcp_tools:
  - search_legislation
  - get_provision
  - check_currency
  - get_eu_basis
  - build_legal_stance
  - validate_citation
  - get_provision_eu_basis
---

# KKV Fogyasztóvédelmi Tanácsadó

### ⚠️ MCP-first elv
- A pontos jogszabályszöveget MINDIG az MCP tool-okból kérd le
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`

A fogyasztóvédelmi törvény (1997. évi CLV. tv., "Fgytv."), az elektronikus kereskedelmi törvény (2001. évi CVIII. tv.), és a 45/2014. (II.26.) Korm. rendelet (távollevők közötti szerz.) alapján ad cselekvőképes válaszokat.

## Mikor használd ezt a skill-t

- Webshop kötelező jogi tájékoztatók listája
- 14 napos elállási jog feltételei és kivételei
- Jótállási jegy tartalmi követelményei
- Fogyasztói panaszkezelési folyamat (kötelező elemek)
- Tisztességtelen kereskedelmi gyakorlat elkerülése
- Online értékesítés különleges szabályai
- Szállítási feltételek, teljesítési határidő

---

## Workflow

### 1. Kérdés értelmezése

| Kulcsszavak | Terület | Jogalap |
|---|---|---|
| webshop, online áruház, e-shop | Webshop kötelezők | 2001. évi CVIII. tv. 4-5. § |
| elállás, visszaküldés, visszavonás | Elállási jog | 45/2014. Korm. r. 20-27. § |
| jótállás, garancia, hibás termék | Jótállás | 151/2003. Korm. r., Ptk. 6:171. § |
| szavatosság, kellékszavatosság | Szavatosság | Ptk. 6:157-6:175. § |
| panasz, reklamáció, fogyasztói panasz | Panaszkezelés | Fgytv. 17/A. § |
| megtévesztő, félrevezető, reklám | Tisztességtelen práktika | 2008. évi XLVII. tv. |
| ár, áralap, listaár | Árinformáció | 4/2009. (I.30.) NFGM-SZMM rendelet |
| szállítás, teljesítés, határidő | Szállítás | 45/2014. Korm. r. 22. § |

### 2. Jogszabály keresés

```
search_legislation(
  query: "[fogyasztóvédelmi kulcsszavak]",
  limit: 8
)

// Fgytv. (fogyasztóvédelem):
get_provision(document_id: "hu-law-1997-155-00-00", section: "[szakaszszám]")

get_eu_basis(
  document_id: "hu-law-1997-155-00-00",  // Fgytv.
  include_articles: true
)

build_legal_stance(
  query: "consumer rights withdrawal e-commerce Hungary",
  limit: 5
)
```

### 3. Területspecifikus logika

#### Webshop kötelező tájékoztatók (2001. évi CVIII. tv. 4-5. §)
```
KÖTELEZŐ MEGJELENÍTÉS A WEBOLDALON:
☐ Vállalkozás neve, székhelye
☐ Elérhetőség (email, telefon)
☐ Cégbejegyzési szám / egyéni vállalkozói azonosító
☐ Adószám
☐ Felügyeleti hatóság (ha van)
☐ ÁSZF (letölthető formában)
☐ Adatkezelési tájékoztató
☐ Panaszkezelési tájékoztató
☐ Elállási jog tájékoztató (ha alkalmazható)
☐ Szállítási feltételek és díjak
☐ Fizetési módok
☐ A szerz. nem minősül írásbeli szerz.-nek (ha nem archiválják)
☐ Magatartási kódex (ha csatlakoztak)
```

#### Elállási jog (45/2014. Korm. r.) — 14 naptári nap
**Mikor jár:**
- Távollevők között kötött szerz. (online, telefon, katalógus)
- Fogyasztónak minősülő vásárló (magánszemély)
- Fizikai termék: az átvételtől számított 14 nap
- Szolgáltatás: a szerz. megkötésétől számított 14 nap

**Mikor NEM jár (kivételek, 29. §):**
- Egyedi megrendelésre készített termék
- Gyorsan romló termék
- Lepecsételt higiéniai termék (ha felbontották)
- Digitális tartalom (ha a letöltés megkezdődött és fogyasztó beleegyezett)
- Személyre szabott termék
- Újságok, folyóiratok (egyes)
- Szálláshely, étkezés, szórakoztatás (meghatározott dátumra)

**Visszatérítési kötelezettség:**
- 14 napon belül vissza kell fizetni (szállítási díjjal együtt, kivéve a legolcsóbb standard szállítás)
- Termék visszaküldési költsége: alapból a fogyasztót terheli (kivéve ha vállalkozó vállalta)

#### Kötelező jótállás tartós fogyasztási cikkre (151/2003. Korm. r.)
Kötelező, ha a termék ára meghaladja a küszöbértéket (jelenleg 10 000 Ft felett egyes cikkeknél):
- **0-1 év:** teljes jótállás (díjmentes javítás, csere)
- Jótállási jegy kötelező, tartalmazza:
  - Termék megnevezése, típusa
  - Vásárlás dátuma
  - Jótállás időtartama
  - Jótálló neve, elérhetősége
  - Javítóhálózat megjelölése

#### Fogyasztói panaszkezelés (Fgytv. 17/A. §)
```
KÖTELEZŐ FOLYAMAT:
1. Panasz fogadása (szóban vagy írásban)
2. Szóbeli panasz: azonnal megvizsgálni és orvosolni VAGY
   Írásbeli panasz: 30 napon belül írásban válaszolni
3. Elutasítás esetén: tájékoztatni a fogyasztót a békéltető testület lehetőségéről
4. Panasznyilvántartás 5 évig megőrzési kötelezettség
```

**Békéltető testület:** minden vármegye székhelyén működik; online: ODR platform (EU)

#### Tisztességtelen kereskedelmi gyakorlatok (2008. évi XLVII. tv.)
Tilos:
- Hamis áthúzott ár (ha nem volt az valóban az ár)
- Hamis "készlet erejéig" / "utolsó darab" jelzés
- Manipulált vélemények, fake review-k
- Rejtett reklám
- Nyomásgyakorlás (fake countdown timer, mesterséges sürgősség)

### 4. Kockázatszint

- **⛔ Kritikus:** GVH eljárás, fogyasztóvédelmi hatósági bírság, class action
- **🔴 Magas:** Elállási jog megtagadása jogalap nélkül, hiányzó kötelező tájékoztatók
- **🟡 Közepes:** Hiányos jótállási jegy, panasz 30 napon túli megválaszolása
- **🟢 Alacsony:** Webshop tájékoztatók frissítése, ÁSZF elállási fejezet

### 5. Output

Használd a `kkv-jogi-router/references/output-template.md` sablont.

**Fogyasztóvédelmi specifikus kiegészítések:**
- GVH (Gazdasági Versenyhivatal) és NFH (Nemzeti Fogyasztóvédelmi Hatóság) hatáskörök
- Bírságolási keret (akár forgalom %-ában)
- EU irányelv alap (Consumer Rights Directive, Omnibus Directive)

---

## Kiegészítő területek

### Marketplace értékesítés (Amazon, eBay, Etsy, eMAG)

**Ki a kereskedő:** a marketplace-en értékesítő vállalkozás — a platform csak közvetítő!

**KKV kötelezettségei marketplace-en:**
- Saját ÁSZF és adatkezelési tájékoztató (a platform feltételein felül)
- Elállási jog biztosítása (14 nap — a KKV felé, nem a platform felé)
- Jótállási jegy biztosítása (kötelező jótállás esetén)
- Panaszkezelés (a fogyasztó a kereskedőhöz fordulhat, nem csak a platformhoz)
- Számlázás a KKV kötelezettsége
- ÁFA: oda kell figyelni a marketplace ÁFA szabályokra (egyes platformok ÁFA-t vonnak le)

### DSA — Digital Services Act (EU 2022/2065)

**KKV-k érintettsége:**
- Ha a KKV online platformot üzemeltet (webshop, közvetítő, tartalom-megosztó)
- Ha a KKV online hirdet (hirdetői átláthatóság)

**Kötelezettségek (ha a KKV platform):**
- Egyértelmű felhasználási feltételek
- Tartalommoderálási kötelezettség
- Bejelentési és eljárási mechanizmus (notice and action)
- Átláthatósági jelentés

### Influencer marketing jelölési kötelezettség

**Szabályozás:** 2008. évi XLVII. tv. + NMHH/GVH iránymutatás

**Kötelező jelölés ha:**
- A tartalomkészítő ellenszolgáltatást kap (pénz, termék, kedvezmény)
- A jelölésnek egyértelműnek kell lennie: "Fizetett hirdetés" / "Reklám" / "#hirdetés"
- NEM elegendő: apró betűs megjegyzés, rejtett hashtagek, "Köszönöm a [brand]-nek"

**KKV mint megbízó felelőssége:**
- A KKV felelős, hogy az influencer szabályosan jelölje a tartalmat
- Írásbeli megállapodás ajánlott (jelölési kötelezettség rögzítésével)
- GVH bírságolhat: a megbízót ÉS az influencert is

### Omnibus irányelv változások

**Árleszállítás szabályai:**
- Leárazásnál kötelező feltüntetni az akció előtti 30 nap legalacsonyabb árát
- Progresszív leárazásnál: a legelső árleszállítás előtti ár az irányadó

**Fake review tilalom:**
- Tilos: fiktív vélemények közzététele, vélemények vásárlása
- Kötelező: jelezni, ha nem ellenőrzik a vélemények hitelességét

---

## Fontos korlátok

- Ez tájékoztatás, NEM jogi tanácsadás
- A fogyasztóvédelmi szabályok kógensek — a felek nem térhetnek el tőlük a fogyasztó hátrányára
- B2B viszonyban ezek a szabályok nem alkalmazandók (ott `kkv-szerzodes`)
- GVH eljárásnál ügyvéd kötelező
- Marketplace specifikus kérdéseknél az adott platform szabályzata is irányadó
