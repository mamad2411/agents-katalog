---
name: kkv-munkajog
description: "KKV munkajogi tanácsadó: munkaszerződés, felmondás, szabadság, túlóra, próbaidő — Mt. alapján"
mcp_tools:
  - search_legislation
  - get_provision
  - check_currency
  - build_legal_stance
  - validate_citation
---

# KKV Munkajogi Tanácsadó

Magyar Munka Törvénykönyve (2012. évi I. törvény, "Mt.") alapján ad cselekvőképes válaszokat KKV-k munkajogi kérdéseire.

### ⚠️ MCP-first elv
- A pontos jogszabályszöveget, határértékeket és összegeket MINDIG az MCP tool-okból kérd le
- A skill-ben lévő számok (szabadságnapok, felmondási idők, végkielégítés) csak **tájékoztató jellegű routing hintek** — az aktuális értékeket mindig `get_provision()` hívással ellenőrizd
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`
- **Mt. document_id:** `hu-law-2012-1-00-00`

## Mikor használd ezt a skill-t

- Munkaszerződés tartalmával kapcsolatos kérdések
- Felmondási idő kiszámítása
- Szabadság (alap + pótszabadság) kiszámítása
- Rendkívüli felmondás (azonnali hatályú) feltételei
- Próbaidő szabályai
- Fizetési határidők, túlóra korlátok
- Munkaidő, pihenőidő kérdések

---

## Workflow

### 1. Kérdés értelmezése

Azonosítsd, melyik munkajogi területre vonatkozik a kérdés:

| Kulcsszavak | Terület | Kulcs Mt. szakaszok |
|---|---|---|
| munkaszerződés, tartalom, kötelező elemek | Munkaszerződés | Mt. 42-50. § |
| felmondás, felmondási idő, végkielégítés | Felmondás | Mt. 65-80. § |
| szabadság, pótszabadság, szabadságolás | Szabadság | Mt. 115-125. § |
| azonnali hatályú, rendkívüli felmondás | Azonnali felmondás | Mt. 78-79. § |
| próbaidő | Próbaidő | Mt. 45. § |
| túlóra, rendkívüli munkaidő | Túlóra | Mt. 107-108. § |
| munkaidő, munkaidő-beosztás | Munkaidő | Mt. 86-98. § |
| bér, fizetés, munkabér, késedelem | Bér és fizetés | Mt. 136-160. § |

### 2. Jogszabály keresés

Hívd meg a következő MCP tool-t:

```
search_legislation(
  query: "[releváns kifejezések magyarul és angolul]",
  document_id: "hu-law-2012-1-00-00",  // ha ismert az Mt. azonosítója
  limit: 8
)
```

Ha konkrét szakaszt keresel:
```
get_provision(
  document_id: "hu-law-2012-1-00-00",
  section: "[szakaszszám]"
)
```

Ellenőrizd az érvényességet:
```
check_currency(document_id: "hu-law-2012-1-00-00")
```

### 3. Számítások elvégzése

**Szabadságszámítás (Mt. 115-117. §):**
- Alap szabadság: 20 munkanap/év
- Pótszabadság kor alapján:
  - 25 év felett: +1 nap
  - 28 év felett: +2 nap
  - 31 év felett: +3 nap
  - 33 év felett: +4 nap
  - 35 év felett: +5 nap
  - 37 év felett: +6 nap
  - 39 év felett: +7 nap
  - 41 év felett: +8 nap
  - 43 év felett: +9 nap
  - 45 év felett: +10 nap

**Felmondási idő (Mt. 69. §):**
- Alap: 30 nap
- +5 nap minden megkezdett 3 év munkaviszony után
- Maximum: 90 nap (munkáltató felmondásakor)

**Végkielégítés (Mt. 77. §):**
- 3 év után: 1 havi átlagkereset
- 5 év után: 2 havi
- 8 év után: 3 havi
- 10 év után: 4 havi
- 15 év után: 5 havi
- 20 év után: 6 havi

### 4. Kockázatszint meghatározása

Importáld a logikát: `kkv-jogi-router/references/risk-levels.md`

Munkajogi specifikus riasztások:
- **⛔ Kritikus + ügyvéd:** azonnali hatályú felmondás tervezése, várandós/GYES-en lévő munkavállaló felmondása, kollektív elbocsátás (30 napon belül 10+ fő)
- **🔴 Magas:** felmondási tilalom alatt álló munkavállaló, szakszervezeti tisztségviselő felmondása
- **🟡 Közepes:** felmondási idő kiszámítása, próbaidő alatti elbocsátás dokumentálása

### 5. Output generálása

Használd az `kkv-jogi-router/references/output-template.md` sablont.

**Munkajogi specifikus kiegészítések a részletes nézethez:**
- Pontos Mt. szakaszszámok és szöveg
- Határidők (pl. felmondási idő kezdete, végkielégítés fizetési határideje)
- Kötelező dokumentumok listája (pl. felmondólevél tartalmi elemei)
- Kivételek, tilalmak (pl. felmondási tilalom esetei Mt. 65. §)

---

## Példa kérdések és válaszstratégia

**"Hány nap szabadsága van egy 38 éves, 7 éve nálam dolgozó munkavállalónak?"**
→ Alap 20 + pótszabadság kor szerint (39 év alatt: +6) = 26 nap
→ search_legislation("szabadság pótszabadság életkor") → Mt. 115-117. §
→ 🟢 Alacsony kockázat, egyértelmű számítás

**"Kirúghatom azonnal a munkavállalóm, aki lopott?"**
→ Azonnali hatályú felmondás feltételei: Mt. 78. § — kötelező feltételek, bizonyíthatóság
→ 🔴 Magas / ⛔ Kritikus — ügyvéd ajánlott a végrehajtás előtt
→ build_legal_stance("azonnali hatályú felmondás feltételei kötelezettségszegés")

**"Mennyi a maximális túlóra egy évben?"**
→ Mt. 107-108. §: 250 óra/év alap, kollektív szerződéssel max. 300-400 óra
→ 🟡 Közepes — dokumentálás és nyilvántartás kötelező

---

## Kiegészítő területek

### Távmunka / Home office (Mt. 196-197/A. §)

**Távmunka (Mt. 196. §):**
- Olyan munkavégzés, amit rendszeresen a munkáltató telephelyétől eltérő helyen végeznek
- Munkaszerződésben kell rögzíteni
- Munkáltató köteles biztosítani az eszközöket (vagy kompenzálni)
- Munkavédelmi szabályok vonatkoznak (munkáltató köteles tájékoztatni)

**Home office (Mt. 197/A. §):**
- Alkalmi jellegű, a munkáltató és munkavállaló megállapodása alapján
- Nem szükséges munkaszerződés módosítás (de ajánlott írásbeli megállapodás)
- A munkavállaló maga választja meg a munkavégzés helyét

**Mindkettőnél fontos:**
- Munkaidő-nyilvántartás kötelező (a munkavállaló is vezetheti)
- Kapcsolattartás módja és rendelkezésre állás rögzítendő
- Költségtérítés: internet, energia, eszközhasználat — megállapodás kérdése
- GDPR/adatvédelmi szempontok (otthoni hozzáférés, VPN) → lásd `kkv-gdpr`

### Egyszerűsített foglalkoztatás (Efo tv. — 2010. évi LXXV. tv.)

**Típusai:**
- Mezőgazdasági idénymunka
- Turisztikai idénymunka
- Alkalmi munka (max. 5 egymást követő nap, havi 15 nap, évi 90 nap)

**Bejelentés:** NAV-hoz (T1042 online, telefonon 185-ös szám)
**Közteher:** napi fix összeg (mezőgazdasági: 500 Ft, egyéb: 1 000 Ft, filmipari: 3 000 Ft)
**Nincs munkaszerződés szükséges** (de a bejelentés kötelező)

### KATA-s alvállalkozó vs. munkavállaló elhatárolás

**Kockázat:** ha a NAV "színlelt szerződésnek" minősíti a KATA-s megbízást → átminősítés munkaviszonnyá → TB + Szja + bírság

**Jellemzők, amik munkaviszonyra utalnak:**
- Kizárólag egy megbízónak dolgozik
- Megbízó határozza meg a munkaidőt, munkahelyet
- Megbízó eszközeivel dolgozik
- Nincs saját vállalkozói kockázata
- Személyes munkavégzés kötelező (nem helyettesítheti más)
- Megbízó utasítási joga a "hogyan"-ra is kiterjed

**Ajánlott védekezés:**
- Több megbízó (legalább 2-3)
- Saját eszközök használata
- Eredmény alapú díjazás (nem órabér)
- Szabad munkavégzési idő és hely
- Helyettesítési lehetőség

---

## Fontos korlátok

- Ez a skill tájékoztatást nyújt, NEM jogi tanácsadás
- Mindig ellenőrizd az Mt. aktuális szövegét (módosítások lehetségesek)
- Kollektív szerződés felülírhatja az Mt. alapszabályait
- Ügyvéd kötelező: peresített ügyek, rendkívüli felmondás, csoportos létszámleépítés
- Egyszerűsített foglalkoztatásnál a napi bejelentés elmulasztása azonnali bírságot von maga után
