---
name: kkv-jogi-router
description: "KKV virtuális jogi csapat orchestrátor: természetes kérdésből meghatározza a területet és a megfelelő skill-t hívja"
mcp_tools:
  - search_legislation
  - build_legal_stance
  - get_provision
  - check_currency
  - validate_eu_compliance
  - get_eu_basis
---

# KKV Jogi Router — Orchestrátor

Ez a skill az összes KKV jogi skill belépési pontja. Természetes magyar kérdésből azonosítja az érintett jogterületet(eket), meghívja a megfelelő specializált skill(eket), és egységes formátumban adja vissza a választ.

## Indítás

Amikor a felhasználó jogi kérdést tesz fel egy KKV-val kapcsolatban, ezt a skill-t kell először futtatni.

---

## Routing logika

### 1. lépés — Terület azonosítása

| Ha a kérdés tartalmaz ilyen kulcsszavakat… | → Hívd ezt a skill-t |
|---|---|
| munkaszerződés, felmondás, szabadság, túlóra, próbaidő, munkaviszony, bér, munkaidő, munkavállaló, home office, távmunka, egyszerűsített foglalkoztatás, KATA-s alvállalkozó | **kkv-munkajog** |
| személyes adat, GDPR, cookie, adatkezelés, NAIH, adatvédelem, hozzájárulás, adatszivárgás, incidens, DPA | **kkv-gdpr** |
| szerződés, ÁSZF, NDA, titoktartás, szavatosság, késedelem, kártérítés, felelősség, vállalkozási, megbízási, freelancer, SaaS, szoftver fejlesztés | **kkv-szerzodes** |
| webshop, fogyasztó, elállás, jótállás, garancia, visszaküldés, online értékesítés, panasz, reklamáció, marketplace, influencer, DSA | **kkv-fogyasztovedelmi** |
| cég, Kft., Bt., taggyűlés, törzstőke, ügyvezető, cégjegyzés, alapítás, osztalék, üzletrész, egyéni vállalkozó, EV átalakulás, egyszemélyes | **kkv-cegjog** |
| ÁFA, adó, TAO, KIVA, KATA, számla, NAV, adóellenőrzés, bevallás, áfa-kulcs, alanyi mentesség, fordított adózás, iparűzési, HIPA, e-számla | **kkv-ado** |
| nem fizet, tartozás, követelés, fizetési meghagyás, FMH, végrehajtás, inkasszó, késedelmi kamat, felszólítás, elévülés, csőd, felszámolás | **kkv-koveteleskezeles** |
| védjegy, szerzői jog, szabadalom, IP, szellemi tulajdon, domain, logó, márka, licenc, bitorlás, copyright, open source | **kkv-szellemi-tulajdon** |
| székhely, telephely, bérlet, iroda, bérleti szerződés, kaució, bérleti díj, kiürítés, székhelyszolgáltatás, fióktelep | **kkv-ingatlan** |
| engedély, működési engedély, bejelentés, telepengedély, NÉBIH, HACCP, vendéglátás, szálláshely, NTAK, Airbnb, kereskedelem bejelentés | **kkv-engedelyek** |

### 2. lépés — Keresztterületek kezelése

Ha a kérdés több területet érint, **mindkét skill-t futtasd**:

Tipikus keresztterületek:
- Webshop + adatvédelem → **kkv-fogyasztovedelmi** + **kkv-gdpr**
- Munkaviszony megszűnés + szerz. → **kkv-munkajog** + **kkv-szerzodes**
- Cégalapítás + munkáltatói kötelezettségek → **kkv-cegjog** + **kkv-munkajog**
- Cégalapítás + adónem választás → **kkv-cegjog** + **kkv-ado**
- Webshop indítás + engedélyek → **kkv-engedelyek** + **kkv-fogyasztovedelmi** + **kkv-gdpr**
- Vendéglátás indítás → **kkv-engedelyek** + **kkv-ado** + **kkv-munkajog**
- Nem fizető partner + szerz. → **kkv-koveteleskezeles** + **kkv-szerzodes**
- Szoftver fejlesztési szerz. + IP → **kkv-szerzodes** + **kkv-szellemi-tulajdon**
- Iroda bérlet + székhely → **kkv-ingatlan** + **kkv-cegjog**
- Freelancer megbízás → **kkv-szerzodes** + **kkv-munkajog** (KATA elhatárolás)
- Márkaépítés + védjegy → **kkv-szellemi-tulajdon** + **kkv-cegjog**
- EV → Kft. átmenet → **kkv-cegjog** + **kkv-ado**

### 3. lépés — Ha a terület nem egyértelmű

Futtasd ezt:
```
build_legal_stance(
  query: "[a felhasználó kérdése angolul/magyarul]",
  limit: 5
)
```
A találatok alapján azonosítható, melyik törvény a releváns.

---

## Output formátum

Minden válasz a `references/output-template.md` alapján épül fel.

**Alap:** rövid válasz (kockázatszint + teendők)
**Opcionális:** ha a felhasználó kéri, vagy a kockázat 🔴/⛔ → részletes jogi háttér automatikusan

Kockázatszint logika: `references/risk-levels.md`

---

## Példa kérdések → routing

| Kérdés | Router döntés |
|---|---|
| "Hány nap szabadság jár egy 38 éves munkavállalónak?" | kkv-munkajog |
| "Kötelező adatkezelési tájékoztató a webshopba?" | kkv-gdpr + kkv-fogyasztovedelmi |
| "Kirúghatom azonnali hatállyal a munkavállalóm?" | kkv-munkajog (⛔ ügyvéd flag) |
| "Mi kötelező egy Kft. alapításához?" | kkv-cegjog |
| "Mi a különbség a szavatosság és jótállás között?" | kkv-szerzodes vagy kkv-fogyasztovedelmi (B2C esetén mindkettő) |
| "Mekkora bírság jár GDPR sértésért?" | kkv-gdpr |
| "ÁSZF-be kell írni az elállási jogot?" | kkv-fogyasztovedelmi + kkv-szerzodes |
| "Melyik adónem éri meg nekem jobban?" | kkv-ado |
| "A partnerem nem fizet 3 hónapja, mit tegyek?" | kkv-koveteleskezeles |
| "Védjegyeztessem a logómat?" | kkv-szellemi-tulajdon |
| "Milyen engedély kell étterem nyitáshoz?" | kkv-engedelyek + kkv-ado |
| "Székhelyszolgáltatást szeretnék igénybe venni" | kkv-ingatlan + kkv-cegjog |
| "EV-ből Kft.-t akarok csinálni" | kkv-cegjog + kkv-ado |
| "Freelancert szerződtetnék szoftverfejlesztésre" | kkv-szerzodes + kkv-szellemi-tulajdon + kkv-munkajog |
| "Airbnb-ztetnék, mi kell hozzá?" | kkv-engedelyek + kkv-ado |
| "Marketplace-en akarok eladni" | kkv-fogyasztovedelmi + kkv-ado |
| "Home office-ban dolgoznak a munkavállalóim" | kkv-munkajog + kkv-gdpr |

---

## Mindig add hozzá a választ végéhez

```
---
⚠️ *Ez a tájékoztatás nem minősül jogi tanácsadásnak. Konkrét jogi döntés előtt kérj ügyvédi véleményt.*
```
