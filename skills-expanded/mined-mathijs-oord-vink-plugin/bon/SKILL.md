---
name: bon
description: Verwerk een bon of inkoopfactuur als kostenpost — leest het document, classificeert de BTW (aftrekbaar / verlegd EU / verlegd niet-EU / niet-aftrekbaar), converteert vreemde valuta naar euro op de ECB-dagkoers, en schrijft alles weg naar receipts.csv voor de BTW-aangifte.
allowed-tools:
  - Bash(node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" *)
  - Bash(mkdir -p bonnen/*)
  - Bash(cp * bonnen/*)
  - Read
  - Write
---

# Bon / kosten verwerken

De gebruiker geeft een bon of inkoopfactuur op (pad naar PDF/afbeelding, of een omschrijving).
Verwerk het als kostenpost zó dat het correct meetelt in de BTW-aangifte.

## Stappen

### 1. Lees het document
Lees de PDF/afbeelding en extraheer:
- **leverancier** (naam), **leveranciers-BTW-nummer** (indien vermeld), **factuurnummer**, **datum**.
- **bedrag(en)** en **BTW-bedrag(en) + tarief(en)**, **valuta**.
- Signalen voor verlegging: staat er "BTW verlegd", "reverse charge", "VAT reverse charged",
  "Art. 44/194", of staat **jouw eigen** BTW-nummer (uit `data/business.json`) op de factuur
  terwijl er géén BTW is gerekend?

Vraag de gebruiker alleen wat je écht niet uit het document haalt (bv. categorie, of het
zakelijk percentage bij telefoon/internet).

### 2. Valuta
Noteer de **valuta van de bon** en neem de bedragen over zoals ze erop staan. **Reken zelf niets
om** — de omrekening naar euro (ECB-dagkoers op de bon-datum; in het weekend de vorige beursdag)
doet de code in stap 7–8.

### 3. Categorie
Kies één: `office, travel, software, phone_internet, insurance, marketing, education,
food_drinks, equipment, other`. Bij telefoon/internet: vraag het **zakelijk percentage**
(`business_pct`, bv. 70) — dat schaalt de aftrekbare voorbelasting.

### 4. BTW-classificatie (`vat_status`) — deterministische beslisboom
Eerste match wint (port van Vink `vat-classification.ts`):

1. **Categorie `food_drinks` of `insurance`** → `non_deductible`
   (horeca-BTW uitgesloten, Art. 1 BUA; verzekering vrijgesteld, Art. 11).
2. **NL-leverancier (BTW-nr begint met NL) + BTW > 0** → `deductible` (rubriek 5b). Ook als het een
   buitenlands concern is dat via een Nederlands filiaal met NL-btw factureert (bv. AWS).
3. **Buitenlandse leverancier die btw van zijn eigen land rekent** (bv. een Duits hotel met Duitse
   btw) → `non_deductible`. Buitenlandse btw trek je niet af in de Nederlandse aangifte; terugvragen
   kan apart, met een teruggaafverzoek voor btw uit andere EU-landen.
4. **EU-leverancier (niet-NL EU-prefix) + geen BTW óf verleggingstekst** → `reverse_charge_eu`
   (rubriek 4b + 5b, netto €0).
5. **Niet-EU leverancier + geen BTW óf verleggingstekst** → `reverse_charge_non_eu`
   (rubriek 4a + 5b, netto €0).
6. **Jouw eigen BTW-nr op de factuur + geen BTW geheven** → verlegd. Kijk naar het vestigingsland van
   de **entiteit op de factuur** (adres, btw-nummer), niet naar de merknaam: EU-land →
   `reverse_charge_eu`, daarbuiten → `reverse_charge_non_eu`. Veel Amerikaanse SaaS-leveranciers
   factureren EU-klanten vanuit Ierland of Luxemburg. Geen land te vinden → `reverse_charge_non_eu`
   en meld dat het een aanname is.
7. **Geen BTW op het document, geen andere signalen** → `non_deductible`
   (waarschijnlijk KOR-leverancier of vrijgesteld — geen aftrek).
8. **Nederlandse BTW geheven (21%/9%), maar geen leveranciers-BTW-nr** → `deductible`
   (vereenvoudigde factuur ≤€100, Art. 35b — een Nederlandse kassabon).

**Bij `reverse_charge_*`:** `vat_amount` = 0 (er staat geen btw op de bon) en `vat_percentage` = 21 —
het Nederlandse tarief dat je zelf aangeeft in 4a/4b, niet de 0% van de bon. Alleen 9 als de dienst
onder het verlaagde tarief valt. De code weigert een verlegde bon met een btw-bedrag: staat er wél btw
op, dan is het regel 3 (`non_deductible`).

Twijfel? Lees `${CLAUDE_PLUGIN_ROOT}/rules/kosten-voorbelasting.md` en `${CLAUDE_PLUGIN_ROOT}/rules/nultarief-verlegd-vrijgesteld.md`.
Bij echte ambiguïteit kies de **fiscaal veilige** optie (`non_deductible`) en meld het.

### 5. Meerdere BTW-tarieven op één bon (bv. horeca 9% + 21%)
Geef `vat_breakdown` mee als lijst, in de valuta van de bon:
`[{"percentage":9,"amount":2.10},{"percentage":21,"amount":4.20}]`.
`vat_amount` = som van alle entries; `vat_percentage` = het dominante (hoogste-bedrag) tarief.

### 6. BTW-periode
Het btw-kwartaal (`vat_period`, `YYYY-QN`) leidt de code zelf af uit de bon-datum. Geef `vat_period`
alleen mee als de bon in een **later** kwartaal moet meetellen — een vergeten bon uit een kwartaal
waarvan de aangifte al is ingediend zet je op het lopende kwartaal.

### 7. Preview (compact) → bevestiging
Bouw `/tmp/bon.json` — alléén de **WAT**, met de bedragen zoals ze op de bon staan:
```json
{
  "date": "2026-04-15",
  "supplier_name": "Figma", "supplier_vat_number": "IE3557088SH", "supplier_invoice_number": "INV-1234",
  "description": "Figma Professional april",
  "category": "software",
  "currency": "USD", "amount": 45.00, "vat_amount": 0, "vat_percentage": 21,
  "vat_status": "reverse_charge_eu",
  "business_pct": "", "notes": ""
}
```
`amount` = het **totaalbedrag incl. btw**, `vat_amount` = het btw-bedrag, beide in `currency` (default
`EUR`). Draai dan:
```
node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" compute-receipt /tmp/bon.json
```
Dit rekent om naar euro en bepaalt het kwartaal, zonder iets weg te schrijven. Toon beknopt uit die
output: leverancier, datum, bedrag in euro (en het originele bedrag + koers indien omgerekend),
BTW-bedrag, `vat_status` + één regel waarom, categorie, kwartaal. Vraag bevestiging.

### 8. Na bevestiging: bewaar origineel + leg vast
1. **Kopieer het bronbestand** naar het kwartaalmapje `bonnen/<vat_period>/` (bewaarplicht
   Art. 52 AWR — origineel is het wettelijke bewijs). Maak het mapje eerst aan:
   `mkdir -p bonnen/<vat_period>`. Gebruik de `vat_period` uit stap 7 als mapnaam en een nette
   bestandsnaam: `bonnen/<vat_period>/YYYY-MM-DD-leverancier.pdf` (bv.
   `bonnen/2026-Q2/2026-04-15-apple.pdf`). Zet dat pad als `file_path` in `/tmp/bon.json`.
2. **Leg vast:**
   ```
   node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" record-receipt /tmp/bon.json
   ```
   Dit rekent opnieuw om en schrijft de rij naar `receipts.csv`. **Je tikt zelf geen eurobedrag,
   koers of kwartaal over.** Het commando print de weggeschreven rij terug — gebruik die in je
   melding. Staat dezelfde inkoopfactuur (leverancier + factuurnummer) er al in, dan stopt het
   commando en schrijft het niets.

Meld kort: leverancier, bedrag, classificatie, kwartaal.

## Let hier op (wat vaak misgaat)
- **Bewaarplicht:** altijd het originele bestand kopiëren naar het kwartaalmapje
  `bonnen/<vat_period>/` — de gestructureerde velden zijn gemak, het origineel is het bewijs.
- **Horeca:** BTW niet aftrekbaar (BUA), maar het **bedrag incl. BTW** is wél een zakelijke kost
  voor de IB. We boeken 'm als `non_deductible` (telt niet mee in BTW-aangifte).
- **Gemengd gebruik** (telefoon/internet, soms reiskosten): `business_pct` bepaalt het aftrekbare
  deel van de voorbelasting. Dat geldt ook bij een verlegde bon: de btw in 4a/4b blijft volledig
  verschuldigd, alleen het zakelijke deel komt in 5b.
- **Valuta:** de code converteert op de **bon-datum**, niet op vandaag — geef dus de juiste datum mee.
- **Binnenlands verlegd** (Nederlandse leverancier, "btw verlegd" — bv. onderaanneming in de bouw):
  hoort in rubriek 2a en wordt **niet ondersteund**. Meld het en boek de bon niet als
  `reverse_charge_*`; de gebruiker vult 2a zelf in.
- **Self-billing** (een opdrachtgever maakt een factuur namens jou): dat is **omzet**, geen kost —
  hoort als verkoopfactuur in `invoices.csv`, niet hier. Zie `${CLAUDE_PLUGIN_ROOT}/rules/self-billing.md`.
- **Investering ≥ €450 excl. BTW** (laptop, dure apparatuur): BTW is dit kwartaal volledig
  aftrekbaar (gewoon `deductible`), maar voor de **IB** moet je afschrijven — flag dit even naar
  de gebruiker. Zie `${CLAUDE_PLUGIN_ROOT}/rules/afschrijving-investeringen.md`. Boek het bedrijfsmiddel
  onder categorie `equipment`: `/jaaropgave` herkent `equipment` ≥ €450 als investering en schrijft
  'm af. Eén bon met meerdere losse spullen onder €450 per stuk is géén investering → `office`.
- **KOR-leverancier:** geen BTW op de factuur → niets af te trekken (`non_deductible`).

## Belangrijk
Geen verwijder-actie via de skill — een bon corrigeren/verwijderen doet de gebruiker met de hand
in `receipts.csv` (en het bestand in `bonnen/`).
