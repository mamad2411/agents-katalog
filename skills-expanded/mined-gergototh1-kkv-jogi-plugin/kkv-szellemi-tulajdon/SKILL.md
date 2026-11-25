---
name: kkv-szellemi-tulajdon
description: "KKV szellemi tulajdon tanácsadó: védjegy, szerzői jog, szabadalom, domain vita, szoftver IP — Szt. + Vt. + szerzői jogi tv. alapján"
mcp_tools:
  - search_legislation
  - get_provision
  - check_currency
  - get_eu_basis
  - build_legal_stance
  - validate_citation
---

# KKV Szellemi Tulajdon Tanácsadó

### ⚠️ MCP-first elv
- A pontos jogszabályszöveget MINDIG az MCP tool-okból kérd le
- **SZTNH/EUIPO díjak** tájékoztató jellegűek — az aktuális díjakat az SZTNH (sztnh.gov.hu) és EUIPO (euipo.europa.eu) honlapjáról ellenőrizd
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`

A szerzői jogról szóló 1999. évi LXXVI. törvény (Szjt.), a védjegyek és a földrajzi árujelzők oltalmáról szóló 1997. évi XI. törvény (Vt.), a találmányok szabadalmi oltalmáról szóló 1995. évi XXXIII. törvény (Szt.), és a szoftver szerzői jogi védelméről ad cselekvőképes válaszokat.

## Mikor használd ezt a skill-t

- Védjegybejelentés (SZTNH, EUIPO)
- Szerzői jog — digitális tartalom, fotó, design, szoftver
- Szoftver szellemi tulajdon kérdései
- Domain viták és regisztráció
- Licencelés (felhasználási szerződés)
- Üzleti titok védelme
- Know-how és védelem
- Formatervezési minta oltalom
- Jogsértés (másik cég másolja a termékem/márkám)

---

## Workflow

### 1. Kérdés értelmezése

| Kulcsszavak | Terület | Jogalap |
|---|---|---|
| védjegy, márkanév, logó, brand | Védjegy | 1997. évi XI. tv. (Vt.) |
| szerzői jog, copyright, mű | Szerzői jog | 1999. évi LXXVI. tv. (Szjt.) |
| szoftver, forráskód, program | Szoftver szerzői jog | Szjt. 58-60. § |
| szabadalom, találmány, patent | Szabadalom | 1995. évi XXXIII. tv. (Szt.) |
| domain, honlap cím, .hu | Domain vita | ISZT Regisztrációs Szabályzat |
| licenc, felhasználás, jogdíj | Licencelés | Szjt. 42-52. § |
| üzleti titok, know-how | Üzleti titok | 2018. évi LIV. tv. |
| formatervezés, design, minta | Formatervezési minta | 2001. évi XLVIII. tv. |
| másolás, jogsértés, bitorlás | Jogsértés | Vt. 27. §, Szjt. 94. § |

### 2. Jogszabály keresés

```
search_legislation(
  query: "[IP kulcsszavak]",
  limit: 8
)

// Szjt. (szerzői jog):
get_provision(document_id: "hu-law-1999-76-00-00", section: "[szakaszszám]")

// Vt. (védjegy):
get_provision(document_id: "hu-law-1997-11-00-00", section: "[szakaszszám]")

get_eu_basis(
  document_id: "hu-law-1999-76-00-00",  // Szjt.
  include_articles: true
)

build_legal_stance(
  query: "[IP kérdés angolul]",
  limit: 5
)
```

### 3. Területspecifikus logika

#### Védjegy (Vt.)

**Mi védhető védjegyként:**
- Szó, szóösszetétel (cégnév, terméknév)
- Ábra, logó
- Szó + ábra kombináció
- Szín, hang, hologram (ritkább)

**Bejelentés menete:**
1. Előzetes kutatás (SZTNH adatbázis + EUIPO TMview)
2. Bejelentés az SZTNH-hoz (magyar) vagy EUIPO-hoz (EU-s)
3. Alaki vizsgálat (~1 hónap)
4. Érdemi vizsgálat + közzététel (~3-6 hónap)
5. Lajstromozás

**Költségek (tájékoztató):**
- SZTNH (magyar védjegy): ~67 000 Ft (1 osztály) + 20 000 Ft/további osztály
- EUIPO (EU védjegy): 850 EUR (1 osztály online) + 50 EUR (2. osztály) + 150 EUR (3.+)
- Védjegyoltalmi idő: 10 év, korlátlanul megújítható

**Nizzai osztályok:** 45 áru/szolgáltatás osztály — meg kell határozni, melyikbe tartozik

#### Szerzői jog (Szjt.)

**Automatikusan véd:**
- Irodalmi mű (cikk, blog, könyv)
- Fotó, grafika, illusztráció
- Zene, film, videó
- Szoftver forráskód
- Adatbázis (ha egyéni/eredeti)
- Webdesign (ha egyéni/eredeti jellegű)

**NEM védi:**
- Ötlet, koncepció, módszer
- Jogszabály szövege
- Közismert adat, tény
- Név, cím (de védjegyként védhető)

**Védelmi idő:** szerző élete + 70 év

**Fontos KKV-knak:**
- A szerzői jog regisztráció NÉLKÜL automatikusan keletkezik
- Munkaviszonyban készült mű: a munkáltató szerzi meg a vagyoni jogokat (Szjt. 30. §)
- Megbízási szerződéssel készült mű: a szerzőé marad, hacsak a szerződés nem rendelkezik másként!

#### Szoftver szerzői jog (Szjt. 58-60. §)

**Védett:** forráskód, tárgykód, felhasználói felület (ha eredeti)
**NEM védett:** algoritmus, programnyelv, funkcionális specifikáció

**Munkaviszonyban készült szoftver:**
- Vagyoni jogok automatikusan a munkáltatóé
- Személyhez fűződő jogok a szerzőnél maradnak

**Megbízásban készült szoftver:**
- A vagyoni jogok a szerzőnél maradnak (!)
- Külön szerződésben kell átruházni → **IP átruházási záradék kötelező**

**Open source felhasználás:**
- Licenc típusa meghatározza a felhasználási kereteket (MIT, GPL, Apache stb.)
- GPL: ha beépíted → a te kódod is GPL kell legyen (copyleft)
- MIT/Apache: szabadabban felhasználható

#### Domain viták

**Regisztráció:**
- .hu domain: ISZT (Internet Szolgáltatók Tanácsa) szabályzata
- Regisztráció: akkreditált regisztrátoroknál
- Elv: "first come, first served" — DE védjegyjogosult felülírhatja

**Domain vita eljárás:**
- Alternatív vitarendezés (AVR) az ISZT-nél
- Ha a domain sérti védjegyjogot vagy névjogot → visszavonható
- EU domainnél: UDRP eljárás (WIPO)

#### Licencelés / Felhasználási szerződés (Szjt. 42-52. §)

**Kötelező tartalmi elemek:**
```
☐ Felhasználás módja (többszörözés, terjesztés, nyilvánosság)
☐ Területi hatály (Magyarország, EU, világ)
☐ Időtartam (határozott/határozatlan)
☐ Kizárólagos vagy nem kizárólagos
☐ Díjazás (egyösszegű, jogdíj %, royalty)
☐ Allicencia adásának joga (van/nincs)
☐ A mű módosításának joga
```

**Kizárólagos felhasználás:** írásban kell, különben nem kizárólagos!

#### Üzleti titok védelme (2018. évi LIV. tv.)

**Üzleti titok feltételei:**
1. Titkos (nem általánosan ismert)
2. Gazdasági értékkel bír (éppen azért, mert titkos)
3. A jogosult megtette az ésszerű titokvédelmi intézkedéseket

**Védelmi intézkedések:**
- NDA (titoktartási megállapodás) — lásd `kkv-szerzodes`
- Hozzáférés korlátozás (fizikai és digitális)
- Belső szabályzat (munkavállalóknak)
- Jelölés ("BIZALMAS" / "CONFIDENTIAL")

### 4. Kockázatszint

- **⛔ Kritikus:** Védjegybitorlási per, szerzői jogi per, szoftver IP vita bíróság előtt
- **🔴 Magas:** Védjegy bejelentés nélküli használat, IP átruházás hiánya megbízásos szoftvernél
- **🟡 Közepes:** Licencszerződés hiányosságai, domain vita, open source licenc kérdések
- **🟢 Alacsony:** Védjegy kutatás, szerzői jogi tájékozódás, NDA készítés

### 5. Output

Használd a `kkv-jogi-router/references/output-template.md` sablont.

**IP specifikus kiegészítések:**
- SZTNH / EUIPO eljárási díjak és időkeretek
- Oltalmi idők (védjegy: 10 év, szerzői jog: élet+70 év, szabadalom: 20 év)
- Regisztrációs vs. automatikus védelem különbsége
- Gyakorlati lépések (bejelentés, kutatás, szerződés)

---

## Fontos korlátok

- Ez tájékoztatás, NEM jogi tanácsadás
- Szabadalmi ügyvivő kötelező: szabadalmi bejelentésnél
- Ügyvéd ajánlott: védjegybejelentésnél, IP átruházásnál, jogsértésnél
- A szerzői jogi védelem nem helyettesíti a védjegyoltalmat (és fordítva)
- Nemzetközi IP kérdéseknél országspecifikus szabályok vonatkoznak
