---
name: kkv-engedelyek
description: "KKV hatósági engedélyek tanácsadó: működési engedély, tevékenység bejelentés, telepengedély, szakhatósági feltételek — ágazati jogszabályok alapján"
mcp_tools:
  - search_legislation
  - get_provision
  - check_currency
  - build_legal_stance
  - validate_citation
---

# KKV Hatósági Engedélyek és Bejelentések Tanácsadó

### ⚠️ MCP-first elv
- A pontos jogszabályszöveget MINDIG az MCP tool-okból kérd le
- Az engedélyezési feltételek ágazatonként és önkormányzatonként eltérhetnek — az MCP a törvényi kereteket adja
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`

A szolgáltatási tevékenység megkezdésének és folytatásának általános szabályairól szóló 2009. évi LXXVI. törvény, a kereskedelemről szóló 2005. évi CLXIV. törvény (Kertv.), a telepengedélyről szóló 57/2013. (II.27.) Korm. rendelet, és az ágazati jogszabályok alapján ad cselekvőképes válaszokat.

## Mikor használd ezt a skill-t

- Milyen engedély kell a tevékenységemhez
- Kereskedelmi tevékenység bejelentése
- Telepengedély szükségessége
- Vendéglátás indítása (NÉBIH, ÁNTSZ, tűzvédelem)
- Szálláshely-szolgáltatás (NTAK bejelentés)
- Online kereskedelem indítása
- Építési engedély (alapszintű tájékoztatás)
- Hatósági ellenőrzés — mire kell felkészülni

---

## Workflow

### 1. Kérdés értelmezése

| Kulcsszavak | Terület | Jogalap |
|---|---|---|
| engedély, működési engedély | Működési engedély | 2009. évi LXXVI. tv. |
| kereskedelem, bolt, üzlet | Kereskedelmi bejelentés | 2005. évi CLXIV. tv. (Kertv.) |
| telep, műhely, gyár, üzem | Telepengedély | 57/2013. Korm. r. |
| vendéglátás, étterem, kávézó, büfé | Vendéglátás | 2005. évi CLXIV. tv. + NÉBIH |
| szálláshely, apartman, vendégház, Airbnb | Szálláshely | 239/2009. Korm. r. + NTAK |
| webshop, online bolt, e-kereskedelem | Online kereskedelem | 2001. évi CVIII. tv. |
| építés, felújítás, átalakítás | Építési engedély | 1997. évi LXXVIII. tv. (Étv.) |
| HACCP, élelmiszer, higiénia | Élelmiszer-biztonság | 852/2004/EK rendelet |
| tűzvédelem, tűzoltó, tűzriadó | Tűzvédelem | 1996. évi XXXI. tv. |
| ellenőrzés, hatóság, bírság | Hatósági ellenőrzés | 2016. évi CL. tv. (Ákr.) |

### 2. Jogszabály keresés

```
search_legislation(
  query: "[engedélytípus kulcsszavak]",
  limit: 8
)

// Kertv. (kereskedelem):
get_provision(document_id: "hu-law-2005-164-00-00", section: "[szakaszszám]")

build_legal_stance(
  query: "[tevékenységtípus + permit/license Hungary]",
  limit: 5
)
```

### 3. Területspecifikus logika

#### Bejelentés vs. engedélyköteles tevékenység

**Bejelentésköteles (egyszerűbb — azonnal megkezdhető):**
- Kereskedelmi tevékenység (bolt, webshop)
- Vendéglátás (alapszintű)
- Szolgáltatások többsége
- **Folyamat:** bejelentés a jegyzőnek → nyilvántartásba vétel → tevékenység megkezdhető

**Engedélyköteles (hatósági döntés szükséges):**
- Telepengedély-köteles tevékenységek (zaj, bűz, veszélyes anyag)
- Egyes élelmiszer-ipari tevékenységek
- Gyógyszertár, orvosi rendelő
- Dohánybolt
- **Folyamat:** kérelem → szakhatósági vélemények → hatósági döntés → engedély

#### Kereskedelmi tevékenység bejelentése (Kertv. + 210/2009. Korm. r.)

**Hol:** a működés helye szerinti jegyzőnél (önkormányzat)

**Bejelentés tartalma:**
```
☐ Kereskedő neve, székhelye, adószáma
☐ Üzlet címe
☐ Kereskedelem formája (üzletben, webshop, mozgóbolt, piaci)
☐ Forgalmazni kívánt termékek köre (TEÁOR)
☐ Üzlet nyitvatartási ideje
☐ Üzlet alapterülete
☐ Tulajdoni lap vagy bérleti szerz. (jogszerű használat igazolása)
```

**Üzletköteles termékek (nem bejelentés, hanem működési engedély kell):**
- Dohánytermékek → dohánybolt koncesszió
- Gyógyszerek → OGYÉI engedély
- Fegyver, lőszer → rendőrségi engedély
- Pirotechnikai termékek

#### Telepengedély (57/2013. Korm. r.)

**Mikor kell:**
- Ipari tevékenység (gyártás, szerelés, javítás)
- Jelentős zajjal, bűzzel, rezgéssel járó tevékenység
- Veszélyes anyagok tárolása

**Két kategória:**
1. **Bejelentésköteles telep:** kisebb zavaró hatás (pl. asztalosműhely)
2. **Telepengedély-köteles telep:** nagyobb környezeti hatás (pl. autófényező, nyomda)

**Eljáró hatóság:** a telep helye szerinti jegyző + szakhatóságok (környezetvédelem, tűzvédelem, közegészségügy)

#### Vendéglátás indítása

**Szükséges lépések:**
```
☐ 1. Vállalkozás megalapítása (EV, Kft., Bt.)
☐ 2. TEÁOR bejelentés (5610 — éttermi vendéglátás stb.)
☐ 3. Kereskedelmi tevékenység bejelentése (jegyző)
☐ 4. NÉBIH regisztráció (élelmiszer-vállalkozás)
☐ 5. HACCP rendszer kiépítése
☐ 6. Közegészségügyi feltételek (NNK — volt ÁNTSZ)
☐ 7. Tűzvédelmi előírások teljesítése
☐ 8. Dohányzási szabályok kihelyezése
☐ 9. Zeneszolgáltatás → ARTISJUS díj (ha zenét játszanak)
☐ 10. Teraszhasználat → közterület-használati engedély (önkormányzat)
```

**HACCP (852/2004/EK rendelet):**
- Élelmiszer-biztonsági rendszer — minden vendéglátóhely kötelező
- Dokumentálni kell: hőmérsékletek, beszállítók, takarítás, kártevő-mentesítés
- NÉBIH bármikor ellenőrizheti

#### Szálláshely-szolgáltatás (239/2009. Korm. r.)

**Típusok:**
- Szálloda, panzió, kemping, üdülőház, közösségi szálláshely, egyéb szálláshely
- Magánszálláshely (Airbnb típusú, max. 8 vendég)

**Kötelezettségek:**
```
☐ NTAK regisztráció (Nemzeti Turisztikai Adatszolgáltató Központ)
☐ Szálláshely bejelentés a jegyzőnek
☐ Vendégnyilvántartás vezetése
☐ Idegenforgalmi adó (IFA) beszedése és befizetése
☐ Tűzvédelmi előírások
☐ Kategóriának megfelelő felszereltség
```

**Magánszálláshely (Airbnb):**
- NTAK regisztráció kötelező
- Max. 8 fő / szálláshely
- Társasházban: SZMSZ és közgyűlési határozat ellenőrzése (tilthatják!)
- IFA: önkormányzatonként eltérő (általában 300-500 Ft/fő/éj)

#### Online kereskedelem (webshop) indítása

**Jogi feltételek:**
```
☐ Vállalkozás (EV, Kft., Bt.)
☐ Kereskedelmi tevékenység bejelentés (jegyző) — webshopra is!
☐ ÁSZF elkészítése → lásd kkv-szerzodes
☐ Adatkezelési tájékoztató → lásd kkv-gdpr
☐ Fogyasztói tájékoztatók → lásd kkv-fogyasztovedelmi
☐ NAV online számla rendszer csatlakozás → lásd kkv-ado
☐ Cookie kezelés (opt-in) → lásd kkv-gdpr
☐ Csomagolási hulladék díj (ha terméket csomagol) — termékdíj kérdés
```

**A webshopra is vonatkozik a kereskedelmi bejelentési kötelezettség!**

#### Hatósági ellenőrzés — mire készüljünk (Ákr.)

**Jogok ellenőrzéskor:**
- Képviselő (ügyvéd) bevonása
- Jegyzőkönyv másolata
- Észrevétel az ellenőrzési megállapításokra
- Fellebbezés (15 nap)

**Általános dokumentumok, amiket kérhetnek:**
```
☐ Vállalkozási okmányok (cégkivonat, egyéni vállalkozói igazolvány)
☐ Működési engedély / bejelentés igazolása
☐ Kereskedelmi bejelentés igazolása
☐ HACCP dokumentáció (vendéglátás)
☐ Tűzvédelmi szabályzat
☐ Munkavédelmi dokumentáció
☐ Munkaszerződések (munkaügyi ellenőrzés)
☐ Számlatömbök / számlázóprogram
```

### 4. Kockázatszint

- **⛔ Kritikus:** Engedély nélküli működés, hatósági bezárás, élelmiszer-biztonsági incidens
- **🔴 Magas:** Hiányzó bejelentés, NÉBIH/NNK megállapítás, tűzvédelmi hiányosság
- **🟡 Közepes:** Hiányos dokumentáció, lejárt engedély megújítása, NTAK regisztráció elmulasztása
- **🟢 Alacsony:** Tevékenység bejelentés tervezése, checklist összeállítás

### 5. Output

Használd a `kkv-jogi-router/references/output-template.md` sablont.

**Engedélyezési specifikus kiegészítések:**
- Eljáró hatóság megjelölése (jegyző, NÉBIH, NNK, katasztrófavédelem)
- Ügyintézési határidők (Ákr.: 60 nap, sommás: 8 nap)
- Illetékek és díjak
- Szükséges dokumentumok checklist
- Szakhatósági közreműködők listája

---

## Fontos korlátok

- Ez tájékoztatás, NEM jogi tanácsadás
- Az engedélyezési feltételek ágazatonként és önkormányzatonként eltérhetnek
- Speciális tevékenységek (orvosi, gyógyszertári, pénzügyi) külön jogszabályi kerettel rendelkeznek
- Építési engedélykérdéseknél építész / építési jogi szakértő szükséges
- Környezetvédelmi engedélyeknél környezetvédelmi szakértő szükséges
