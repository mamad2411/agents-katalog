---
name: kkv-cegjog
description: "KKV cégjogi tanácsadó: Kft. taggyűlés, törzstőke, ügyvezető felelőssége, cégjegyzés, alapítás — Ctv. + Ptk. alapján"
mcp_tools:
  - search_legislation
  - get_provision
  - check_currency
  - build_legal_stance
  - validate_citation
---

# KKV Cégjogi Tanácsadó

### ⚠️ MCP-first elv
- A pontos jogszabályszöveget, törzstőke minimumokat és egyéb értékhatárokat MINDIG az MCP tool-okból kérd le — a skill-ben lévő számok csak tájékoztató jellegűek
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`
- **Ctv. document_id:** `hu-law-2006-5-00-00`
- **Ptk. document_id:** `hu-law-2013-5-00-00`

A cégeljárásról szóló 2006. évi V. törvény (Ctv.) és a Ptk. társasági jogi rendelkezései (3:1-3:177. §) alapján ad cselekvőképes válaszokat KKV-k cégjogi kérdéseire.

## Mikor használd ezt a skill-t

- Kft. taggyűlés összehívásának szabályai
- Törzstőke emelés vagy csökkentés lépései
- Ügyvezető jogai, kötelezettségei, felelőssége
- Cégjegyzés módja, aláírási jog
- Cégalapítás dokumentum checklist
- Tag ki- és belépése
- Osztalék fizetés feltételei

---

## Workflow

### 1. Kérdés értelmezése

| Kulcsszavak | Terület | Jogalap |
|---|---|---|
| taggyűlés, közgyűlés, összehívás | Taggyűlés | Ptk. 3:107-3:116. § |
| törzstőke, alaptőke, emelés, csökkentés | Tőkeváltozás | Ptk. 3:161-3:167. § |
| ügyvezető, vezető tisztségviselő, felelősség | Ügyvezető | Ptk. 3:112-3:116. § |
| cégjegyzés, aláírás, képviselet | Cégjegyzés | Ctv. 7-9. § |
| alapítás, létesítő okirat, társasági szerz. | Alapítás | Ptk. 3:95-3:106. § |
| tag, üzletrész, átruházás | Tagság | Ptk. 3:168-3:177. § |
| osztalék, nyereségfelosztás | Osztalék | Ptk. 3:154-3:158. § |
| felszámolás, végelszámolás, törlés | Megszűnés | Ctv. + Cstv. |

### 2. Jogszabály keresés

```
search_legislation(
  query: "[cégjogi kulcsszavak]",
  limit: 8
)

get_provision(
  document_id: "hu-law-2006-5-00-00",  // Ctv.
  section: "[szakaszszám]"
)

check_currency(document_id: "[törvény azonosítója]")
```

### 3. Területspecifikus logika

#### Taggyűlés összehívása (Ptk. 3:107-3:109. §)
**Kötelező taggyűlés:**
- Évente legalább egyszer (éves beszámoló elfogadásához)
- Ha a saját tőke a törzstőke felére csökkent
- Ha fizetésképtelenség fenyeget
- Ha a tagok 10%-a kéri

**Összehívás menete:**
1. Írásbeli meghívó (legalább 15 nappal előtte)
2. Tartalmazza: időpont, helyszín, napirendi pontok
3. Napirendre nem vett kérdésben csak ha minden tag jelen van és hozzájárul

**Határozatképesség:** a törzstőke több mint fele képviselve van

**Szavazati arányok:**
- Egyszerű többség (50%+1): általános ügyek
- 3/4-es többség: létesítő okirat módosítása, törzstőke változás, átalakulás
- Egyhangú: tag kizárása, kötelezés megszüntetése

#### Törzstőke emelés (Ptk. 3:161. §)
**Lépések:**
1. Taggyűlési határozat (3/4-es többség)
2. Társasági szerződés módosítása
3. Befizetés/nem pénzbeli apport teljesítése
4. Cégbírósági bejelentés (30 napon belül)
5. Közzététel (Cégközlöny)

**Minimális törzstőke Kft.-nél:** 3 000 000 Ft (vagy 1 Ft — ha az egyszerűsített alapítást választják, de ekkor osztalék korlátok vannak)

#### Törzstőke csökkentés (Ptk. 3:164. §)
- Hitelezői védelem: közzétételre van szükség, hitelezők kifogásolhatják
- 2 körös közzététel (Cégközlöny), összesen ~3 hónap
- Hitelezők kielégítése vagy biztosítéka szükséges

#### Ügyvezető felelőssége (Ptk. 3:24. §, 3:117-3:119. §)
**Általános felelősség:**
- A gazdasági társaság irányában: ügyvezetői gondosság — ha szándékos vagy gondatlan károkozás → saját vagyonával felel
- Harmadik személyek irányában: a társaság felel (nem az ügyvezető személyesen), kivéve ha:
  - Visszaélésszerű magatartás
  - A társaság fizetésképtelensége esetén a hitelezőkkel szembeni felelősség (Cstv.)

**Kizárt ügyvezetők:**
- Aki ellen a bűnügyi nyilvántartásban bejegyzés van (bizonyos bűncselekmények)
- Aki más cégnél felszámolás miatt kizárt

#### Cégjegyzés (Ctv. 7-9. §)
- **Önálló cégjegyzés:** bármely ügyvezető egyedül jogosult
- **Együttes cégjegyzés:** két ügyvezető/prokurista együtt
- **Banki aláírás:** a bankszámlához külön aláírásiminta szükséges (nem azonos a cégaláírással)
- Cégjegyzési mód a társasági szerz.-ben rögzítve, Cégbíróságon bejegyezve

#### Cégalapítás dokumentum checklist (Kft.)
```
☐ Társasági szerződés (közokirat vagy ügyvéd által ellenjegyzett)
☐ Tagok személyi igazolványa / cég esetén aláírási jogosultság igazolása
☐ Ügyvezető(k) elfogadó nyilatkozata
☐ Törzstőke befizetési igazolás (banki igazolás vagy apport-értékbecslés)
☐ Székhelyhasználat igazolása (tulajdoni lap, bérleti szerz., hozzájárulás)
☐ Adóhatósági bejelentkezési lap (NAV 'T201T)
☐ Cégbírósági bejegyzési kérelem (e-cégeljárás)
☐ Közzétételi díj befizetése
```

#### Osztalékfizetés feltételei (Ptk. 3:154-3:158. §)
- Éves beszámoló elfogadása után
- Csak a tárgyévi adózott nyereségből + szabad tartalékból
- **NEM fizethető osztalék, ha:**
  - A saját tőke a törzstőke alá csökkenne
  - A lekötött tartalék csökkenne

### 4. Kockázatszint

- **⛔ Kritikus:** Felszámolás, csőd, vezető tisztségviselői felelősség peres úton
- **🔴 Magas:** Érvénytelen taggyűlési határozat, törzstőke szabályok megsértése
- **🟡 Közepes:** Taggyűlés formai hibái, cégjegyzési jogosultság kérdések
- **🟢 Alacsony:** Dokumentum checklist, alapítás előkészítése

### 5. Output

Használd a `kkv-jogi-router/references/output-template.md` sablont.

**Cégjogi specifikus kiegészítések:**
- Cégbírósági határidők (bejegyzési kötelezettségek)
- Cégközlöny közzétételek (kötelező és díjköteles)
- Adóhatósági párhuzamos kötelezettségek (NAV bejelentések)

---

## Kiegészítő területek

### Bt. (Betéti Társaság) specifikus szabályok (Ptk. 3:154-3:158. §)

**Bt. jellemzők:**
- Legalább 1 beltag (korlátlan felelősség) + 1 kültag (betétje erejéig felel)
- Nincs törzstőke minimum (de betétek összege a vagyoni hozzájárulás)
- Beltag: személyes közreműködés + üzletvezetés
- Kültag: nem vehet részt az üzletvezetésben (ha igen → beltagi felelősség!)

**Bt. vs. Kft. összehasonlítás:**

| | Bt. | Kft. |
|---|---|---|
| Tőke minimum | Nincs | 3 000 000 Ft |
| Felelősség | Beltag: korlátlan | Tagok: törzsbetét erejéig |
| Alapítási költség | Alacsonyabb (~100-150 000 Ft) | Magasabb (~150-250 000 Ft) |
| Adózás | TAO vagy KIVA | TAO vagy KIVA |
| Mikor éri meg | Kis kockázatú, családi vállalkozás | Nagyobb kockázat, befektető, komolyabb üzlet |

**Bt. megszűnése:**
- Ha a beltag vagy kültag kilép és nem lép be új → 6 hónapon belül pótolni kell
- Ha nem pótolják → EV-vé alakul vagy megszűnik

### Egyéni vállalkozó → Kft. átmenet

**Mikor érdemes váltani:**
- Bevétel meghaladja a 30-50M Ft-ot
- Személyes felelősség kockázata nő
- Befektetőt/társat keres
- Komolyabb szerződéses partneri kör

**Átmenet lépései:**
```
1. Kft. megalapítása (ügyvéd kötelező)
2. Tevékenység átszervezése az EV-ről a Kft.-re
   - Szerződések átírása / újrakötése
   - NAV bejelentés (új adószám)
   - Bankszámla nyitás
   - Engedélyek átírása (ha van)
3. EV megszüntetése (vagy szüneteltetése)
   - NAV bejelentés
   - Záró bevallások
4. NAV online számla átállítás
5. Partnerek értesítése
```

**Adózási átmenet:**
- EV záró bevallás (Szja)
- Kft. nyitó bevallás (TAO)
- ÁFA: az alanyi mentesség újra választható, de a Kft.-nek külön kell kérnie
- HIPA: új adóalany → új bejelentés az önkormányzatnál

### Egyszemélyes Kft. sajátosságai

- Taggyűlés helyett: tag írásbeli határozata
- A tag és az ügyvezető ugyanaz a személy lehet
- De: az ügyvezető felelőssége változatlan
- Osztalékkifizetés: saját magának is elfogadó határozat kell
- Könyvvizsgáló: 300M Ft éves nettó árbevétel felett kötelező

---

## Fontos korlátok

- Ez tájékoztatás, NEM jogi tanácsadás
- Társasági szerz. módosítása ügyvéd ellenjegyzéséhez kötött
- Ügyvéd kötelező: átalakulás, összeolvadás, szétválás, felszámolás, EV→Kft. váltás
- Az egyszerűsített cégeljárás esetén az e-cégeljárás szabályai eltérnek
- Bt. beltag korlátlan felelőssége komoly személyes kockázat — döntés előtt ügyvédi konzultáció ajánlott
