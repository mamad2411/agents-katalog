---
name: kkv-ado
description: "KKV adójogi tanácsadó: ÁFA, TAO, KIVA, KATA, számlázás, adóellenőrzés, NAV online számla — Art. + ÁFA tv. + TAO tv. alapján"
mcp_tools:
  - search_legislation
  - get_provision
  - check_currency
  - get_eu_basis
  - build_legal_stance
  - validate_citation
  - format_citation
---

# KKV Adójogi Tanácsadó

### ⚠️ MCP-first elv
- **Adókulcsok, értékhatárok, mentességi küszöbök évente változhatnak** — a skill-ben lévő számok (27%, 12M Ft, 9% stb.) csak tájékoztató jellegű routing hintek
- A pontos, aktuális értékeket MINDIG `get_provision()` hívással ellenőrizd
- A jegybanki alapkamat aktuális értékét az MNB honlapjáról ellenőrizd (nem az MCP-ből)
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`

Az adózás rendjéről szóló 2017. évi CL. törvény (Art.), az általános forgalmi adóról szóló 2007. évi CXXVII. törvény (ÁFA tv.), a társasági adóról szóló 1996. évi LXXXI. törvény (TAO tv.), a kisadózó vállalkozások tételes adójáról szóló 2022. évi XIII. törvény (KATA), és a kisvállalati adóról szóló 2012. évi CXLVII. törvény (KIVA) alapján ad cselekvőképes válaszokat KKV-k adókérdéseire.

## Mikor használd ezt a skill-t

- ÁFA szabályok (alanyi mentesség, fordított adózás, EU-s ÁFA)
- Adónem választás (KATA, KIVA, TAO, átalányadó)
- NAV online számla kötelezettségek
- Számla alaki és tartalmi követelmények
- Adóellenőrzés — jogok és kötelezettségek
- Adóbevallási határidők
- Áfa-visszaigénylés feltételei
- Közösségen belüli értékesítés / beszerzés ÁFA szabályai

---

## Workflow

### 1. Kérdés értelmezése

| Kulcsszavak | Terület | Jogalap |
|---|---|---|
| ÁFA, áfa kulcs, 27%, 18%, 5%, mentes | ÁFA általános | ÁFA tv. 82-84. § |
| alanyi mentesség, 12 millió | Alanyi mentesség | ÁFA tv. 187-196. § |
| fordított adózás, reverse charge | Fordított ÁFA | ÁFA tv. 142. § |
| EU, közösségi, Közösségen belüli | EU ÁFA | ÁFA tv. 89-91. §, 49-51. § |
| számla, e-számla, NAV online | Számlázás | ÁFA tv. 169. §, Art. 10. melléklet |
| TAO, társasági adó, 9% | Társasági adó | TAO tv. 19. § |
| KATA, kisadózó, tételes | KATA | 2022. évi XIII. tv. |
| KIVA, kisvállalati adó | KIVA | 2012. évi CXLVII. tv. |
| átalányadó, átalány | Átalányadó | Szja tv. 50-56. § |
| adóellenőrzés, NAV, revízió | Ellenőrzés | Art. 93-130. § |
| bevallás, határidő, adóbevallás | Bevallás | Art. 44-50. § |
| iparűzési adó, HIPA, helyi adó | Helyi adók | 1990. évi C. tv. |

### 2. Jogszabály keresés

```
search_legislation(
  query: "[adójogi kulcsszavak]",
  limit: 8
)

// ÁFA tv.:
get_provision(document_id: "hu-law-2007-127-00-00", section: "[szakaszszám]")

// Art. (adózás rendje):
get_provision(document_id: "hu-law-2017-150-00-00", section: "[szakaszszám]")

// TAO tv.:
get_provision(document_id: "hu-law-1996-81-00-00", section: "[szakaszszám]")

// Szja tv. (átalányadó):
get_provision(document_id: "hu-law-1995-117-00-00", section: "[szakaszszám]")

check_currency(document_id: "hu-law-2007-127-00-00")  // ÁFA tv.
```

### 3. Területspecifikus logika

#### ÁFA kulcsok (ÁFA tv. 82-84. §)
- **27%** — általános kulcs
- **18%** — egyes élelmiszerek, vendéglátás helyben fogyasztás
- **5%** — alapvető élelmiszerek, könyvek, gyógyszerek, új lakóingatlan, internet
- **Mentes** — pénzügyi szolgáltatás, biztosítás, oktatás, egészségügy

#### Alanyi mentesség (ÁFA tv. 187-196. §)
- **Értékhatár:** évi 12 000 000 Ft bevétel (2025-től)
- Nem számít be: tárgyi eszköz értékesítés, mentes tevékenység
- **Előny:** nem kell ÁFA-t felszámítani, nem kell ÁFA bevallás
- **Hátrány:** beszerzés ÁFA-ját nem lehet levonni
- **Elvesztés:** ha túllépi a határt → a túllépés napjától ÁFA-köteles
- **Választás:** előző év dec. 31-ig kell bejelenteni a NAV-nak

#### Fordított adózás (ÁFA tv. 142. §)
Mikor alkalmazandó (belföldön, B2B):
- Építőipari szolgáltatás (2008-as TEÁOR-os)
- Hulladékkereskedelem
- Munkaerő kölcsönzés (építőipari)
- Ingatlan értékesítés (ha az eladó választotta)
- Gabona és acélipari termékek

**Feltételek:** mindkét fél ÁFA-alany + belföldi ügylet + B2B

#### Számlázási kötelezettségek (ÁFA tv. 159-178. §)
```
SZÁMLA KÖTELEZŐ TARTALMI ELEMEK:
☐ Számla sorszám (egyedi, folyamatos)
☐ Kibocsátó neve, címe, adószáma
☐ Vevő neve, címe, adószáma (100 000 Ft+ ÁFA esetén kötelező)
☐ Teljesítés időpontja
☐ Számla kibocsátásának kelte
☐ Termék/szolgáltatás megnevezése, mennyisége
☐ Nettó egységár és nettó összeg
☐ ÁFA mérték (%) és ÁFA összeg
☐ Bruttó összeg
☐ Fizetési mód és határidő
```

#### NAV Online Számla rendszer
- **Kötelező:** minden belföldi B2B számla adatszolgáltatása valós időben
- **Technikai:** NAV Online Számla 3.0 XML séma
- **Határidő:** kiállítástól számított azonnal (valós idejű adatszolgáltatás)
- **Mentesség:** alanyi mentes nem kötelezett (de választhatja)
- **Szankció:** adatszolgáltatás elmulasztása → mulasztási bírság (500 000 Ft-ig / számla)

#### Adónem összehasonlítás (KKV szempontból)

| | KATA | KIVA | TAO + Szja | Átalányadó |
|---|---|---|---|---|
| Ki választhatja | Egyéni vállalkozó (kizárólag) | Kft./Bt. (max 50 fő) | Bárki | EV (max 36M Ft) |
| Adó mértéke | 50 000 Ft/hó | 10% pénzforgalmi eredmény | 9% TAO + 15% Szja osztalék | Szja 40-80%-os ktsg.hányad |
| Bevételi korlát | 18M Ft/év | 3Mrd Ft/év | Nincs | 36M Ft/év (egyes tevékenységeknél) |
| ÁFA | Alanyi mentes lehet | Normál ÁFA | Normál ÁFA | Alanyi mentes lehet |
| Mikor éri meg | Alacsony bevétel, kevés költség | Bérköltség-intenzív cég | Nagy cégek, beruházások | Szolgáltató EV, kevés költség |

#### Adóellenőrzés — jogok és teendők (Art. 93-130. §)

**NAV ellenőrzés típusai:**
- Bevallás utólagos vizsgálata
- Egyes adókötelezettségek ellenőrzése
- Adatgyűjtésre irányuló ellenőrzés

**Adózó jogai ellenőrzéskor:**
1. Képviselő (könyvelő, ügyvéd) bevonása
2. A megállapításokkal szembeni észrevétel (15 nap)
3. Fellebbezés a határozat ellen (30 nap)
4. Bírósági felülvizsgálat kérése

**Kötelezettségek:**
1. Iratok rendelkezésre bocsátása
2. Együttműködés
3. Nyilatkozattétel

**Ellenőrzés időkorlátja:** az elévülési időn belül (5 év)

#### Helyi iparűzési adó (HIPA) — 1990. évi C. tv.
- Adóalap: nettó árbevétel – eladott áruk beszerzési értéke – alvállalkozói teljesítmények
- Mérték: max. 2% (önkormányzat állapítja meg)
- Bevallás: május 31. (éves)
- Előleg: március 15. és szeptember 15.

### 4. Kockázatszint

- **⛔ Kritikus:** NAV határozat elleni jogorvoslat, adócsalás gyanúja, nagy összegű adóhiány
- **🔴 Magas:** Ellenőrzés alatt, ÁFA visszaigénylés elutasítva, adónem-váltás határidő
- **🟡 Közepes:** Bevallási határidő közeledik, alanyi mentesség határ közelében, számla formai hibák
- **🟢 Alacsony:** Adónem összehasonlítás, tájékozódás, számla tartalmi ellenőrzés

### 5. Output

Használd a `kkv-jogi-router/references/output-template.md` sablont.

**Adójogi specifikus kiegészítések:**
- NAV határidők (bevallás, bejelentés, fizetés)
- Szankció mértékek (adóbírság: max 50%, mulasztási bírság: max 500 000 Ft, késedelmi pótlék: jegybanki alapkamat + 5%)
- Számítási példák (ÁFA, késedelmi pótlék, adóalap)
- Adónem-váltási határidők és feltételek

---

## Fontos korlátok

- Ez tájékoztatás, NEM adótanácsadás
- Könyvelő és/vagy adótanácsadó bevonása ajánlott minden döntésnél
- Adóellenőrzésnél ügyvéd/adószakértő kötelező
- Az adószabályok évente változhatnak — mindig ellenőrizd az aktuális szöveget
- Egyedi elbírálású kérdéseknél NAV felvilágosítás kérhető (Art. 174. §)
