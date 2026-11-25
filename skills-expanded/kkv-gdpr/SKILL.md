---
name: kkv-gdpr
description: "KKV GDPR/adatvédelmi tanácsadó: adatkezelési tájékoztató, DPIA, incidens, DPA, cookie — Infotv. + GDPR alapján"
mcp_tools:
  - search_legislation
  - get_provision
  - check_currency
  - get_eu_basis
  - build_legal_stance
  - validate_eu_compliance
  - validate_citation
  - get_provision_eu_basis
---

# KKV GDPR és Adatvédelmi Tanácsadó

### ⚠️ MCP-first elv
- A pontos jogszabályszöveget MINDIG az MCP tool-okból kérd le — soha ne idézz jogszabályt a skill tartalma alapján
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`
- **Infotv. document_id:** `act-cxii-2011-info-self-determination`
- **GDPR EU azonosító:** `regulation:2016/679`

A 2011. évi CXII. törvény (Infotv.) és az EU 2016/679 rendelet (GDPR) alapján ad cselekvőképes válaszokat KKV-k adatvédelmi kérdéseire.

## Mikor használd ezt a skill-t

- Adatkezelési tájékoztató szükséges-e és mit kell tartalmaznia
- DPIA (adatvédelmi hatásvizsgálat) szükségességi check
- Adatvédelmi incidens bejelentési kötelezettség és folyamat
- Hozzájárulási nyilatkozat formai követelményei
- Adatfeldolgozói szerződés (DPA) alapstruktúrája
- Cookie policy kötelezettségek
- Adatkezelési nyilvántartás (ROPA)

---

## Workflow

### 1. Kérdés értelmezése

| Kulcsszavak | Terület | Jogalap |
|---|---|---|
| tájékoztató, privacy policy | Adatkezelési tájékoztató | GDPR 13-14. cikk, Infotv. 20. § |
| hozzájárulás, beleegyezés | Hozzájárulás | GDPR 7. cikk, Infotv. 5. § |
| incidens, adatszivárgás, hack | Adatvédelmi incidens | GDPR 33-34. cikk |
| adatfeldolgozó, DPA, szerződés | Adatfeldolgozói szerz. | GDPR 28. cikk |
| cookie, süti, tracking | Cookie | ePrivacy irányelv, Infotv. |
| DPIA, hatásvizsgálat | Kockázatelemzés | GDPR 35. cikk |
| NAIH, hatóság, bejelentés | Hatósági bejelentés | GDPR 33. cikk |
| nyilvántartás, ROPA | Adatkezelési nyilvántartás | GDPR 30. cikk |

### 2. EU alap lekérdezése

```
get_eu_basis(
  document_id: "act-cxii-2011-info-self-determination",
  include_articles: true
)
```

```
validate_eu_compliance(
  document_id: "act-cxii-2011-info-self-determination"
)
```

```
build_legal_stance(
  query: "[konkrét kérdés angolul/magyarul]",
  limit: 5
)
```

### 3. Területspecifikus logika

#### Adatkezelési tájékoztató kötelező tartalma (GDPR 13. cikk)
1. Adatkezelő neve, elérhetősége
2. DPO elérhetősége (ha kötelező)
3. Az adatkezelés célja és jogalapja
4. Az adatok tárolási ideje
5. Érintett jogai (hozzáférés, törlés, hordozhatóság stb.)
6. Panasz benyújtásának joga (NAIH)
7. Ha profilalkotás történik: erre vonatkozó tájékoztatás

**NAIH kontakt:** ugyfelszolgalat@naih.hu, 1055 Budapest, Falk Miksa utca 9-11.

#### DPIA szükségességi teszt (GDPR 35. cikk)
Kötelező DPIA, ha:
- Szisztematikus és kiterjedt profilalkotás (pl. hitelminősítés)
- Nagy léptékű különleges adatkezelés (egészségügyi, vallási stb.)
- Nyilvánosan hozzáférhető terület szisztematikus megfigyelése

#### Adatvédelmi incidens folyamat (GDPR 33-34. cikk)
1. Incidens észlelése → belső dokumentálás (azonnal)
2. Kockázatértékelés: magas kockázat-e az érintettekre?
3. **Ha igen: NAIH bejelentés 72 órán belül** (incidents.naih.hu)
4. Ha magas kockázat az érintettekre: érintetteket is értesíteni kell
5. Dokumentálás az adatkezelési nyilvántartásban

#### Cookie jogalapok
- Technikai szükséges cookie: hozzájárulás NEM kell
- Analitikai, marketing cookie: **opt-in hozzájárulás kötelező**
- Hozzájárulás előtt ezek nem aktiválhatók

### 4. Kockázatszint meghatározása

- **⛔ Kritikus:** NAIH vizsgálat alatt, incidens bejelentési határidő lejárt, érintett panasza
- **🔴 Magas:** Aktív incidens (72 óra fut), jogosulatlan adatátadás harmadik félnek
- **🟡 Közepes:** Hiányzó vagy elavult tájékoztató, hiányzó DPA szerződés
- **🟢 Alacsony:** Tájékoztató frissítése, ROPA karbantartása

### 5. Output generálása

Használd a `kkv-jogi-router/references/output-template.md` sablont.

**GDPR specifikus kiegészítések a részletes nézethez:**
- GDPR cikk + Infotv. párhuzamos hivatkozás
- NAIH bírságolási precedensek (ha releváns)
- Határidők (72 óra incidens, 1 hónap érintetti kérelem)
- Sablon dokumentumok listája (mit kell elkészíteni)

---

## Sablon kimenetek

### Adatkezelési tájékoztató checklist
```
KÖTELEZŐ ELEMEK:
☐ Adatkezelő neve, székhelye, elérhetősége
☐ Adatkezelési cél(ok) és jogalap(ok)
☐ Érintett kategóriák és adatkategóriák
☐ Adattárolás időtartama (vagy meghatározás szempontjai)
☐ Adatfeldolgozók listája (ha van)
☐ Harmadik országba való adattovábbítás (ha van)
☐ Érintetti jogok és gyakorlásuk módja
☐ NAIH panasztételi jog
☐ Profilalkotásra vonatkozó tájékoztatás (ha van)
```

### DPA szerződés kötelező elemei (GDPR 28. cikk)
```
☐ Az adatkezelés tárgya és időtartama
☐ Az adatkezelés jellege és célja
☐ A személyes adatok típusa és az érintettek kategóriái
☐ Adatkezelő kötelezettségei és jogai
☐ Titoktartás, biztonsági intézkedések
☐ Albeszállítók igénybevételének feltételei
☐ Törlési/visszaszolgáltatási kötelezettség
☐ Auditálási jog
```

---

## Kapcsolódó skillek

- Webshop adatvédelem → **kkv-fogyasztovedelmi** (ÁSZF, elállási jog, cookie + GDPR)
- Munkavállalói adatkezelés → **kkv-munkajog** (munkaviszony, home office adatvédelem)
- DPA szerződés → **kkv-szerzodes** (szerződéskötés, felelősségkorlátozás)
- Szoftver adatvédelem → **kkv-szellemi-tulajdon** (szoftver IP + GDPR)

---

## Fontos korlátok

- Ez tájékoztatás, NEM jogi tanácsadás
- NAIH határozatai és iránymutatásai felülírhatják az általános szabályokat
- Ügyvéd kötelező: NAIH eljárás, bírság, peres ügy esetén
- A GDPR 2018 óta közvetlenül alkalmazandó, az Infotv. kiegészíti
