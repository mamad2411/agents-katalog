---
name: kkv-szerzodes
description: "KKV szerződési tanácsadó: Ptk. alapján ÁSZF audit, szavatosság, késedelmi kamat, NDA, vállalkozási vs. megbízási szerződés"
mcp_tools:
  - search_legislation
  - get_provision
  - validate_citation
  - format_citation
  - check_currency
  - build_legal_stance
---

# KKV Szerződési Tanácsadó

### ⚠️ MCP-first elv
- A pontos jogszabályszöveget MINDIG az MCP tool-okból kérd le
- Kötelező hívási sorrend és document_id-k: `kkv-jogi-router/references/mcp-usage-guide.md`
- **Ptk. document_id:** `hu-law-2013-5-00-00`

A 2013. évi V. törvény (Ptk.) alapján ad cselekvőképes válaszokat KKV-k szerződéses kérdéseire.

## Mikor használd ezt a skill-t

- Szerződés kockázati pontjainak azonosítása (Ptk. alapján)
- ÁSZF (Általános Szerződési Feltételek) audit
- Szavatosság vs. jótállás különbség tisztázása
- Teljesítési határidő + késedelmi kamat számítás
- NDA (titoktartási megállapodás) tervezet
- Vállalkozási vs. megbízási szerződés elhatárolása
- Kártérítés, felelősségkorlátozás kérdések

---

## Workflow

### 1. Kérdés értelmezése

| Kulcsszavak | Terület | Kulcs Ptk. szakaszok |
|---|---|---|
| szerződés, érvényesség, semmis, megtámadható | Szerz. érvényessége | Ptk. 6:86-6:110. § |
| ÁSZF, általános feltétel, tisztességtelen | ÁSZF | Ptk. 6:77-6:81. § |
| szavatosság, hibás teljesítés, kellékszavatosság | Szavatosság | Ptk. 6:157-6:175. § |
| jótállás, garancia | Jótállás | Ptk. 6:171. § |
| késedelem, késedelmi kamat, teljesítési határidő | Késedelem | Ptk. 6:154-6:156. § |
| kártérítés, kár, felelősség, kizárás | Kártérítés | Ptk. 6:142-6:152. § |
| titoktartás, NDA, üzleti titok | Titoktartás | 2018. évi LIV. tv. |
| vállalkozás, megbízás, különbség | Vállalkozás vs megbízás | Ptk. 6:238. §, 6:272. § |
| előleg, foglaló, kötbér | Biztosítékok | Ptk. 6:185-6:186. § |

### 2. Jogszabály keresés

```
search_legislation(
  query: "[keresési terminusok]",
  limit: 8
)
```

```
get_provision(
  document_id: "hu-law-2013-5-00-00",
  section: "[szakaszszám]"
)
```

```
validate_citation(citation: "[hivatkozás]")
```

### 3. Területspecifikus logika

#### ÁSZF érvényességi vizsgálat (Ptk. 6:77-6:81. §)
Tisztességtelen feltétel (automatikusan semmis), ha:
- Egyoldalúan, indokolás nélkül módosítható
- Ellenbizonyítási lehetőséget kizárja
- A másik fél lényeges jogát korlátozza aránytalanul
- Kizárja a bíróság joghatóságát

KKV-k közötti ÁSZF kevésbé szigorú (B2B) vs. fogyasztói ÁSZF (B2C).

#### Szavatosság vs. jótállás
| | Kellékszavatosság | Jótállás (garancia) |
|---|---|---|
| Alapja | Törvény (kötelező) | Törvény (kötelező tartós fogyasztási cikkeknél) vagy önkéntes vállalás |
| Ki élhet vele | Minden vevő | Fogyasztó (B2C) |
| Határidő | 1 év (általános), 2 év (új fogyasztási cikk) | 1 év (kötelező) + önkéntes |
| Bizonyítás | 6 hónapon belül: vélelem a hibára | Vélelem a hibára |

#### Késedelmi kamat számítás
- **B2B (vállalkozások között):** jegybanki alapkamat + 8% (2013. évi IX. tv. alapján)
- **B2C (fogyasztóval):** jegybanki alapkamat + 5%
- Fizetési határidő: B2B esetén max. 60 nap (kivételek: 30+30 nap)

#### Vállalkozási vs. megbízási szerződés
| | Vállalkozási | Megbízási |
|---|---|---|
| Kötelezettség | Eredmény (mű elkészítése) | Gondos eljárás (nem eredmény) |
| Kockázat | Vállalkozónál | Megbízónál |
| Felmondás | Korlátozott | Bármikor felmondható |
| Típuspéldák | Építés, szoftver fejlesztés | Ügyvéd, könyvelő, tanácsadó |

#### NDA kötelező elemek
```
☐ Titoktartás tárgya (mit tekintünk üzleti titoknak)
☐ Kötelezetti kör (munkavállalók, alvállalkozók?)
☐ Felhasználás tilalma (csak adott célra)
☐ Időtartam (általában 2-5 év, egyes esetekben határozatlan)
☐ Kötbér (megszegés esetén fizetendő összeg)
☐ Visszaszolgáltatási/megsemmisítési kötelezettség
☐ Kivételek (közhirré vált info, hatósági kötelezés)
```

#### Felelősségkorlátozás határai (Ptk. 6:152. §)
- Szándékos vagy súlyos gondatlanságból eredő kár: NEM korlátozható
- Testi sérülés, halál: NEM korlátozható
- Fogyasztóval szemben: erősen korlátozott lehetőség
- B2B: felek megállapodhatnak ésszerű korlátozásban

### 4. Kockázatszint

- **⛔ Kritikus:** Semmis szerz. teljesítése, jogosulatlan alvállalkozás, bírósági eljárás
- **🔴 Magas:** Érvénytelen ÁSZF kikötés, felelősségkorlátozás jogellenes
- **🟡 Közepes:** Hiányzó kötelező elemek, késedelmi kamat kérdések
- **🟢 Alacsony:** Szerz. típus meghatározása, szavatossági határidők

### 5. Output

Használd a `kkv-jogi-router/references/output-template.md` sablont.

**Szerződéses specifikus kiegészítések:**
- Ptk. szakaszszámok pontos hivatkozással
- Érvényesítési határidők (elévülés)
- Kötelező és ajánlott dokumentumok

---

## Kiegészítő területek

### Freelancer / alvállalkozói szerződés

**Megbízási szerződés digitális szolgáltatásra (Ptk. 6:272. §):**

**Kötelező/ajánlott elemek:**
```
☐ Felek adatai (megbízó + megbízott: név, cím, adószám)
☐ Megbízás tárgya (pontos feladatleírás)
☐ Teljesítési határidő(k) / mérföldkövek
☐ Díjazás (összeg, fizetési ütemezés, valuta)
☐ Számlázási feltételek (fizetési határidő, számla típusa)
☐ Elfogadási folyamat (ki és hogyan fogadja el a munkát)
☐ Módosítási kérelmek kezelése (change request)
☐ IP / szellemi tulajdon átruházás → lásd kkv-szellemi-tulajdon
☐ Titoktartás (NDA záradék vagy külön NDA)
☐ Felmondás feltételei
☐ Felelősségkorlátozás
☐ Versenytilalom (ha szükséges, időben korlátozott)
```

**KATA/alvállalkozói kockázat:** lásd `kkv-munkajog` (KATA-s alvállalkozó vs. munkavállaló elhatárolás)

### Szoftver fejlesztési szerződés

**Speciális elemek a standard megbízásin felül:**
```
☐ Specifikáció / követelményrendszer (mellékletben)
☐ Fejlesztési módszertan (agile/waterfall/hybrid)
☐ Forráskód tulajdonjoga (ki az IP tulajdonos?)
☐ Forráskód átadás feltételei (escrow megállapodás?)
☐ Technológiai stack meghatározása
☐ Tesztelés és elfogadás (UAT) folyamata
☐ Hibakategóriák és javítási SLA
☐ Garanciális időszak (jellemzően 3-12 hónap)
☐ Karbantartás és support feltételek (külön szerz. vagy záradék)
☐ Harmadik fél komponensek (open source licencek!)
☐ Adatvédelem (ha személyes adatot kezel) → lásd kkv-gdpr
☐ Hosting és üzemeltetési felelősség
```

**Kritikus pont:** Ha a szerződés nem rendelkezik az IP-ről → a vagyoni jogok a fejlesztőnél maradnak (Szjt. 58. §, megbízási jogviszony)!

### SaaS / előfizetéses szerződés (mint szolgáltató)

**Ha a KKV SaaS szolgáltatást nyújt:**
```
☐ Szolgáltatás leírás (SLA: rendelkezésre állás, pl. 99.9%)
☐ Előfizetési feltételek (havi/éves, megújulás)
☐ Felmondási jog és folyamat
☐ Adathordozhatóság (export lehetőség)
☐ Adattörlés a szerződés végén
☐ Felelősségkorlátozás (kártérítési plafon)
☐ Árváltoztatás joga és értesítési kötelezettség
☐ Force majeure záradék
```

---

## Fontos korlátok

- Ez tájékoztatás, NEM jogi tanácsadás
- Ügyvéd kötelező: peres eljárás, nagy értékű szerz., ingatlan, céges tranzakciók
- A Ptk. diszpozitív szabályait a felek eltérő megállapodása felülírhatja
- Fogyasztói szerz. esetén a `kkv-fogyasztovedelmi` skill is releváns
- Szoftver fejlesztési szerződéseknél az IP kérdés rendezése kritikus → lásd `kkv-szellemi-tulajdon`
