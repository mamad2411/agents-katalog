---
name: kkv-ingatlan
description: "KKV ingatlan és bérlet tanácsadó: székhelyszolgáltatás, üzlethelyiség bérlet, telephely, felmondás — Ptk. + Lakás tv. alapján"
mcp_tools:
  - search_legislation
  - get_provision
  - check_currency
  - build_legal_stance
  - validate_citation
---

# KKV Ingatlan és Bérleti Tanácsadó

### ⚠️ MCP-first elv
- A pontos jogszabályszöveget MINDIG az MCP tool-okból kérd le
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`
- **Ptk. document_id:** `hu-law-2013-5-00-00`

A Ptk. bérleti szerződésre vonatkozó rendelkezései (6:331-6:342. §), a lakások és helyiségek bérletéről szóló 1993. évi LXXVIII. törvény (Ltv.), és a cégjogi szabályok (Ctv.) székhely-vonatkozásai alapján ad cselekvőképes válaszokat.

## Mikor használd ezt a skill-t

- Székhelyszolgáltatás szabályai és kötelezettségei
- Üzlethelyiség bérleti szerződés (irodabérlet, üzlet, raktár)
- Telephely bejelentés
- Bérleti szerződés felmondása (bérbeadó / bérlő oldalról)
- Közös költség, rezsi, üzemeltetés megosztás
- Bérleti díj emelés szabályai
- Óvadék (kaució) szabályok
- Albérlet és továbbadás

---

## Workflow

### 1. Kérdés értelmezése

| Kulcsszavak | Terület | Jogalap |
|---|---|---|
| székhely, székhelyszolgáltatás | Székhely | Ctv. 7. §, 7/2017. IM rendelet |
| telephely, fióktelep | Telephely | Ctv. 7/A. § |
| bérlet, bérleti szerződés, iroda | Bérleti szerz. | Ptk. 6:331-6:342. § |
| felmondás, kiürítés, kilépés | Felmondás | Ptk. 6:339-6:340. §, Ltv. |
| kaució, óvadék, letét | Óvadék | Ptk. 6:336. § |
| bérleti díj, emelés, indexálás | Díjemelés | Ptk. 6:335. § |
| közös költség, rezsi, üzemeltetés | Költségek | Bérleti szerz. + társasházi tv. |
| albérlet, továbbadás, allbérlet | Albérlet | Ptk. 6:338. § |
| építés, átalakítás, felújítás | Bérlői beruházás | Ptk. 6:337. § |

### 2. Jogszabály keresés

```
search_legislation(
  query: "[ingatlan/bérlet kulcsszavak]",
  limit: 8
)

// Ptk. (bérleti szerződés):
get_provision(document_id: "hu-law-2013-5-00-00", section: "[szakaszszám]")

// Ctv. (székhely, telephely):
get_provision(document_id: "hu-law-2006-5-00-00", section: "[szakaszszám]")

check_currency(document_id: "hu-law-2013-5-00-00")  // Ptk.
```

### 3. Területspecifikus logika

#### Székhelyszolgáltatás (7/2017. IM rendelet)

**Cég székhelye:** ahol a központi ügyintézés történik (Ctv. 7. §)

**Saját ingatlan mint székhely:**
- Tulajdoni lap másolat szükséges a cégalapításhoz
- Ha más tulajdona → tulajdonosi hozzájáruló nyilatkozat

**Székhelyszolgáltatás (virtuális iroda):**
- 7/2017. (VI.30.) IM rendelet szabályozza
- Kötelező írásbeli szerződés a szolgáltató és a cég között
- Szolgáltató kötelezettségei:
  - A cég iratainak, hatósági küldeményeinek átvétele
  - A cég cégtáblájának kihelyezése
  - Hatóságok számára hozzáférés biztosítása
  - Cégiratok őrzése
- **NAV bejelentési kötelezettség** a székhelyszolgáltatásról

**Telephely vs. fióktelep:**
- **Telephely:** ahol a tevékenységet folytatják (nem szükséges cégbírósági bejegyzés minden esetben)
- **Fióktelep:** a székhelytől különböző helyen lévő szervezeti egység (cégbírósági bejegyzés kötelező)

#### Üzlethelyiség bérleti szerződés (Ptk. 6:331-6:342. §)

**Kötelező/ajánlott tartalmi elemek:**
```
☐ Felek adatai (bérbeadó, bérlő — teljes név, cím, adószám)
☐ Bérlemény pontos megjelölése (cím, helyrajzi szám, alapterület)
☐ Bérleti díj összege és fizetési módja
☐ Fizetési határidő (melyik hónap hányadikáig)
☐ Közös költség, rezsi viselésének módja
☐ Bérleti időtartam (határozott/határozatlan)
☐ Kaució (óvadék) összege és visszafizetési feltételei
☐ Felmondási feltételek és határidők
☐ Bérlemény állapota (átadás-átvételi jegyzőkönyv!)
☐ Átalakítás, felújítás feltételei
☐ Albérlet/továbbadás lehetősége
☐ Rendeltetésszerű használat (milyen tevékenységre)
```

**Határozott idejű bérleti szerződés:**
- Lejáratkor automatikusan megszűnik
- Előtte nem mondható fel egyoldalúan (kivéve súlyos szerződésszegés)
- Ha a bérlő bentmarad és a bérbeadó nem tiltakozik → határozatlanná válik

**Határozatlan idejű bérleti szerződés:**
- Hónap végére felmondható, a hónap 15. napjáig közölt felmondással
- A felek a szerződésben eltérhetnek (pl. 60 napos felmondási idő)

#### Felmondás szabályai

**Bérbeadó felmondhat:**
- Határozatlan idejű: hónap 15-ig a hónap végére (Ptk. 6:339. §)
- Azonnali hatállyal ha: bérlő nem fizet (felszólítás után sem), bérleményt rongálja, rendeltetésellenesen használja
- Határozott idejű: csak súlyos szerződésszegés esetén

**Bérlő felmondhat:**
- Határozatlan idejű: hónap 15-ig a hónap végére
- Határozott idejű: általában nem (csak szerződésszegés vagy közös megegyezés)
- Azonnali hatállyal ha: bérlemény lakhatatlan/használhatatlan, bérbeadó súlyos kötelezettségszegése

**A bérlemény visszaadása:**
- Átadás-átvételi jegyzőkönyv (a kiadáskori állapottal összevetve)
- Normál amortizáció: bérlő nem felel érte
- Szándékos rongálás: kaució levonható + kártérítés

#### Kaució / Óvadék (Ptk. 6:336. §)

- Általában 2-3 havi bérleti díj
- A bérbeadó köteles visszaadni a bérlet végén (levonva a jogos követeléseit)
- Nem használható fel "utolsó havi bérleti díjként" (hacsak a szerződés nem engedi)
- Jogos levonás: bérleti díj hátralék, kártalanítás, nem fizetett közüzemi díj

#### Bérleti díj emelés

- Határozatlan idejű: a bérbeadó egyoldalúan emelheti (de ésszerű mértékben)
- **Indexálás szerződésben:** KSH fogyasztói árindex (CPI) alapú emelés évente — ajánlott szerződésben rögzíteni
- Határozott idejű: csak ha a szerződés tartalmazza az emelés módját

#### Bérlői beruházás (Ptk. 6:337. §)

- A bérlő a bérbeadó hozzájárulása nélkül is elvégezhet szükséges karbantartást
- Értéknövelő beruházás: csak bérbeadó írásbeli hozzájárulásával
- **Ha nincs megállapodás:** a bérlő a bérlet végén köteles az eredeti állapotot visszaállítani (vagy a bérbeadó megtartja kompenzáció nélkül)
- **Ajánlott:** beruházásról külön írásbeli megállapodás (ki fizeti, mi történik a bérlet végén)

### 4. Kockázatszint

- **⛔ Kritikus:** Kilakoltatás/kiürítés folyamatban, székhely nélküli cég (törlési eljárás kockázata)
- **🔴 Magas:** Bérleti szerződés nélküli használat, felmondás formailag hibás, kaució jogellenes visszatartása
- **🟡 Közepes:** Bérleti szerz. hiányos elemei, díjemelési vita, átalakítási kérdés
- **🟢 Alacsony:** Szerződéskötés előtti tájékozódás, kaució visszakövetelés, indexálás kiszámítása

### 5. Output

Használd a `kkv-jogi-router/references/output-template.md` sablont.

**Ingatlan specifikus kiegészítések:**
- NAV bejelentési kötelezettségek (székhely, telephely)
- Cégbírósági kötelezettségek (fióktelep bejegyzés)
- Átadás-átvételi jegyzőkönyv fontossága
- Adójogi vonatkozások (bérleti díj levonhatósága, ÁFA)

---

## Fontos korlátok

- Ez tájékoztatás, NEM jogi tanácsadás
- Ügyvéd ajánlott: kilakoltatás, nagy értékű bérleti szerz., vállalkozási célú ingatlan
- A lakásbérlet külön szabályozás alá esik (Ltv.) — ez a skill elsősorban üzleti célú bérletekre fókuszál
- Ingatlan adásvétel ügyvédi ellenjegyzés kötelező → nem tartozik ide
- Társasházi jogviták külön terület
