---
name: kkv-koveteleskezeles
description: "KKV követeléskezelési tanácsadó: fizetési felszólítás, fizetési meghagyás (FMH), végrehajtás, késedelmi kamat — Pp. + Vht. alapján"
mcp_tools:
  - search_legislation
  - get_provision
  - check_currency
  - build_legal_stance
  - validate_citation
---

# KKV Követeléskezelési Tanácsadó

### ⚠️ MCP-first elv
- A pontos jogszabályszöveget MINDIG az MCP tool-okból kérd le
- **Illetékek, díjak, összeghatárok** (FMH illeték, felszámolási illeték) változhatnak — mindig ellenőrizd
- A **jegybanki alapkamat** aktuális értékét az MNB honlapjáról ellenőrizd (a késedelmi kamat számításhoz)
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`

A polgári perrendtartásról szóló 2016. évi CXXX. törvény (Pp.), a fizetési meghagyásos eljárásról szóló 2009. évi L. törvény (Fmhtv.), a bírósági végrehajtásról szóló 1994. évi LIII. törvény (Vht.), és a Ptk. késedelmi kamat szabályai alapján ad cselekvőképes válaszokat.

## Mikor használd ezt a skill-t

- Nem fizető partner — mit tegyen a KKV
- Fizetési felszólítás elkészítése
- Fizetési meghagyásos eljárás (FMH) indítása
- Végrehajtás megindítása
- Késedelmi kamat számítása és érvényesítése
- Tartozás elengedés, részletfizetés
- Követelés engedményezés (factoring)
- Elévülési kérdések

---

## Workflow

### 1. Kérdés értelmezése

| Kulcsszavak | Terület | Jogalap |
|---|---|---|
| nem fizet, tartozás, hátralék | Követeléskezelés indítás | Ptk. 6:47-6:48. § |
| felszólítás, figyelmeztetés | Fizetési felszólítás | Ptk. 6:154. § |
| fizetési meghagyás, FMH, MOKK | FMH eljárás | 2009. évi L. tv. |
| végrehajtás, foglalás, inkasszó | Végrehajtás | 1994. évi LIII. tv. |
| kamat, késedelmi kamat | Késedelmi kamat | Ptk. 6:48. § |
| elévülés, elévült, határidő | Elévülés | Ptk. 6:22-6:25. § |
| engedményezés, factoring, faktor | Követelés átruházás | Ptk. 6:193-6:200. § |
| csőd, felszámolás, fizetésképtelen | Felszámolási eljárás | 1991. évi XLIX. tv. (Cstv.) |
| részletfizetés, egyezség | Megállapodás | Ptk. 6:191. § |

### 2. Jogszabály keresés

```
search_legislation(
  query: "[követeléskezelési kulcsszavak]",
  limit: 8
)

// Ptk. (késedelmi kamat, elévülés):
get_provision(document_id: "hu-law-2013-5-00-00", section: "[szakaszszám]")

// Fmhtv. (fizetési meghagyás):
get_provision(document_id: "hu-law-2009-50-00-00", section: "[szakaszszám]")

// Vht. (végrehajtás):
get_provision(document_id: "hu-law-1994-53-00-00", section: "[szakaszszám]")

check_currency(document_id: "hu-law-2009-50-00-00")  // Fmhtv.
```

### 3. Területspecifikus logika

#### Követeléskezelés lépésről lépésre

```
AJÁNLOTT SORREND:
1. lépés → Fizetési felszólítás (0-30 nap késedelem)
2. lépés → Második felszólítás + kamat közlés (30-60 nap)
3. lépés → Ügyvédi felszólítás (60-90 nap)
4. lépés → Fizetési meghagyás (FMH) benyújtása (90+ nap)
5. lépés → Végrehajtás megindítása (ha jogerős FMH + nem fizet)
```

#### Fizetési felszólítás tartalma
```
KÖTELEZŐ/AJÁNLOTT ELEMEK:
☐ Jogosult (hitelező) adatai
☐ Kötelezett (adós) adatai
☐ Tartozás jogcíme (számla szám, szerződés)
☐ Tartozás összege (tőke + kamat külön)
☐ Eredeti fizetési határidő
☐ Póthatáridő (általában 8-15 nap)
☐ Következmény (FMH, végrehajtás, üzleti kapcsolat felfüggesztése)
☐ Bankszámlaszám a fizetéshez
☐ Dátum, aláírás
```

**Tipp:** Tértivevényes levélben VAGY elektronikusan igazolhatóan (olvasási visszaigazolás) küldeni — bizonyíthatóság!

#### Fizetési meghagyásos eljárás — FMH (2009. évi L. tv.)

**Mi ez:** Gyorsított, online indítható közjegyzői eljárás pénzkövetelésre.

**Feltételek:**
- Lejárt pénzkövetelés (nem más teljesítés)
- Összeg: max. 30 000 000 Ft (e felett peres eljárás kötelező)
- 3 000 000 Ft alatt FMH kötelező (nem indítható per előtte)
- Belföldi kézbesítési cím szükséges (külföldi adósnál EU FMH vagy per)

**Indítás:**
- Online: MOKK (Magyar Országos Közjegyzői Kamara) rendszere
- Ügyvéd/jogi képviselő javasolt, de nem kötelező
- Illeték: a követelés 3%-a, minimum 5 000 Ft, maximum 300 000 Ft

**Folyamat:**
1. Kérelem benyújtása (MOKK online)
2. Közjegyző kibocsátja az FMH-t (3 munkanapon belül)
3. Adósnak kézbesítik
4. Adós ellentmondhat 15 napon belül
   - Ha NEM mond ellent → jogerőre emelkedik → végrehajtható
   - Ha ellentmond → perré alakul (bíróságra kerül)

**Időtartam:** ellentmondás nélkül ~4-6 hét

#### Végrehajtás (Vht.)

**Végrehajtási lap kiadása:** jogerős FMH vagy bírósági ítélet alapján

**Végrehajtás módjai:**
- Bankszámla inkasszó (leggyorsabb)
- Munkabér letiltás (max. 33%, kivételes: 50%)
- Ingóságok foglalása és árverése
- Ingatlan végrehajtás (csak nagyobb összeg esetén arányos)
- Gépjármű foglalás

**Végrehajtás költsége:** végrehajtói díj (a behajtott összeg %-a) + eljárási illeték

#### Késedelmi kamat számítás (Ptk. 6:48. §)

**B2B (vállalkozások között):**
- Mérték: jegybanki alapkamat + 8 százalékpont
- Automatikusan jár, külön felszólítás nélkül
- Behajtási költségátalány: 40 EUR egyenérték (egyszeri, automatikus)

**B2C (fogyasztóval szemben):**
- Mérték: jegybanki alapkamat (Ptk. 6:47. §)

**Kamat számítás képlet:**
```
Késedelmi kamat = Tőke × (jegybanki alapkamat + 8%) × késedelmes napok / 365
```

**MNB jegybanki alapkamat:** ellenőrizd a mindenkori aktuális értéket (mnb.hu)

#### Elévülés (Ptk. 6:22-6:25. §)

- **Általános elévülési idő:** 5 év
- **Elévülés megszakítása:**
  - Írásbeli felszólítás (igazolhatóan)
  - Bírósági/hatósági eljárás megindítása
  - Tartozáselismerés az adós által
- Megszakítás után újraindul az 5 év
- **Elévülés nyugvása:** ha a jogosult menthető okból nem tud érvényesíteni

#### Felszámolás kezdeményezése (Cstv.)

**Mikor:** ha az adós fizetésképtelen (nem eseti nemfizetés, hanem tartós)
- 200 000 Ft feletti lejárt tartozás
- 20 napos írásbeli fizetési felszólítás eredménytelen
- Bíróságnál kérelem benyújtása
- **Illeték:** 80 000 Ft
- **Ügyvéd kötelező!**

### 4. Kockázatszint

- **⛔ Kritikus:** Saját cég felszámolás-közeli helyzete, ellentmondással perré alakult ügy
- **🔴 Magas:** Elévülés közelében lévő követelés, végrehajtás eredménytelen
- **🟡 Közepes:** FMH indítás, felszólítás küldés, kamatszámítás
- **🟢 Alacsony:** Felszólítás szöveg, tájékozódás, folyamat megértése

### 5. Output

Használd a `kkv-jogi-router/references/output-template.md` sablont.

**Követeléskezelési specifikus kiegészítések:**
- Pontos összegszámítás (tőke + kamat + behajtási ktsg.átalány)
- Határidők (15 nap ellentmondás, 5 év elévülés)
- Illetékek és díjak
- Következő lépés javaslat (milyen lépésnél tart a folyamat)

---

## Fontos korlátok

- Ez tájékoztatás, NEM jogi tanácsadás
- Ügyvéd kötelező: peres eljárás, felszámolás, 30M Ft feletti követelés
- A végrehajtás során végrehajtó jár el, nem az ügyvéd közvetlenül
- Csődeljárásnál más szabályok vonatkoznak (Cstv.)
- A jegybanki alapkamat változik — mindig az aktuálist kell alkalmazni
