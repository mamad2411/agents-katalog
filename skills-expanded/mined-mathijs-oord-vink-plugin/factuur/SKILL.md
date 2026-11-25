---
name: factuur
description: Maak een verkoopfactuur voor een klant — vult uurprijs/omschrijving/aantal aan op basis van eerdere facturen, kent het juiste oplopende factuurnummer toe (YYYY-NNNN), genereert een PDF in het vaste Vink-format en schrijft alles weg naar de CSV's voor de BTW-aangifte.
allowed-tools:
  - Bash(node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" *)
  - Bash(open facturen/*)
  - Read
  - Write
---

# Factuur maken

Maak een verkoopfactuur. De gebruiker geeft een **klant** op en optioneel een **omschrijving**
van wat gefactureerd moet worden. Vul ontbrekende details zoveel mogelijk zelf aan op basis van
eerdere facturen voor dezelfde klant.

## Stappen

### 1. Lees de basis
- `data/business.json` (afzender).
- `data/clients.csv` — zoek de klant (fuzzy op naam). Meerdere matches → vraag welke.
- **Klant niet gevonden?** Vraag de ontbrekende gegevens (naam, t.a.v., adres, postcode, plaats,
  land, evt. BTW-nummer) en voeg een rij toe aan `clients.csv` met een nieuw `id` (`c_002`, …,
  hoogste bestaande +1). Zonder adres/postcode/plaats kan er geen geldige factuur (Art. 35a).

### 2. Smart defaults uit eerdere facturen
- Filter `data/invoices.csv` op deze `client_id`; pak de **meest recente** factuur.
- Haal de bijbehorende regels uit `data/invoice_items.csv` (`invoice_number` match).
- Gebruik die als default voor **uurprijs (`rate`), eenheid (`unit`) en omschrijving** waar de
  gebruiker niets opgeeft. Aantal (`quantity`) vraag je als het niet gegeven is — dat verschilt
  meestal per maand. Pas omschrijvingen met een maand/periode erin aan naar de juiste periode
  (bv. "Product consultancy mar 2026" → "… apr 2026").
- Geen eerdere factuur én geen input → vraag de gebruiker om regels (omschrijving, aantal,
  eenheid, tarief).

### 3. Bepaal BTW — **per regel**
- Bepaal voor **elke regel afzonderlijk** het juiste tarief (`vat_percentage`); regels op één
  factuur mogen verschillen. Voor de meeste diensten (consultancy/development/design) is dat
  **21%**, maar classificeer naar de aard van de regel: **voedsel, boeken, medicijnen, kapper,
  fietsenmaker → 9%** (zie `${CLAUDE_PLUGIN_ROOT}/rules/btw-tarieven.md`). Twijfel je over een
  regel, of valt 'n product mogelijk onder het verlaagde tarief? Lees de regels en/of leg het
  kort aan de gebruiker voor in de preview — gok niet stilzwijgend op 21%.
- De code splitst gemengde facturen automatisch: de PDF toont dan een **BTW-kolom per regel** +
  een totaalregel per tarief, en de aangifte boekt elke regel in de juiste rubriek (1a/1b/1e).
  Bij één uniform tarief blijft de BTW-kolom weg (tarief staat dan onderaan).
- **Uitzondering — verlegd** (`vat_reverse_charged: true`): alléén als je een **buitenlandse
  zakelijke klant** factureert (BTW-nummer begint niet met `NL`). Dan geen BTW op de factuur +
  automatische verleggings-zin op de PDF. Een EU-ondernemer (met btw-nummer in `clients.csv`) telt
  in rubriek 3b + ICP; omzet aan een afnemer buiten de EU komt niet in de aangifte. Zeldzaam — bij
  NL-klanten nooit. Twijfel? Lees `${CLAUDE_PLUGIN_ROOT}/rules/nultarief-verlegd-vrijgesteld.md`.

### 4. Nummer, datum, betaaltermijn & kwartaal
- Factuurnummer: `node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" next-invoice-number` → `YYYY-NNNN`. **Nooit zelf verzinnen.**
- Datum: vandaag, tenzij anders opgegeven.
- Betaaltermijn (`payment_term_days`): `client.payment_terms` (kolom in clients.csv) als die gevuld
  is, anders `business.payment_terms_days` (14). **De vervaldatum reken je niet zelf uit** — die
  berekent `record-invoice` deterministisch uit datum + termijn.
- **Kwartaal** uit de factuurdatum: `YYYY-QN` (Q1=jan–mrt, Q2=apr–jun, Q3=jul–sep, Q4=okt–dec).
  De PDF gaat in het kwartaalmapje `facturen/<YYYY-QN>/` (bv. datum 2026-05-08 → `facturen/2026-Q2/`).
  Het mapje wordt automatisch aangemaakt door `record-invoice` als het nog niet bestaat.

### 5. Preview (compact) → bevestiging
Bouw de invoice-JSON en draai `node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" compute-invoice <pad.json>` om subtotaal/BTW/
totaal deterministisch te krijgen. Toon een **compacte** preview met alleen beslis-relevante data:

```
Factuur 2026-0005 — Voorbeeld Klant B.V. — datum 05-06-2026, vervalt 19-06-2026
  24    Uren   Consultancy apr 2026        € 100,00   (21%)  € 2.400,00
  5,5   Uren   AI-consultancy apr 2026     € 100,00   (21%)  €   550,00
  Subtotaal € 2.950,00   BTW 21% € 619,50   Totaal € 3.569,50
```
Bij gemengde tarieven toon je het tarief per regel en de BTW per tarief, bv.:
`Subtotaal € 625,00   BTW 21% € 89,25 + BTW 9% € 18,00   Totaal € 732,25`.

Vraag expliciet om bevestiging vóór je iets wegschrijft. Pas aan op feedback en toon opnieuw.

### 6. Na bevestiging: vastleggen (één deterministische stap)
Bouw `/tmp/factuur.json` — alléén de **WAT**. Alle bedragen én de vervaldatum berekent de code zelf;
neem dus géén `subtotal`/`vat`/`total`/`due_date`/`amount` op in de JSON:
```json
{
  "business": { …uit business.json… },
  "client":   { "id": "c_001", …name, attention, address, postal_code, city, country, vat_number… },
  "invoice": {
    "number": "2026-0005", "date": "2026-06-05",
    "vat_reverse_charged": false, "reference": "", "notes": "",
    "line_items": [
      {"description":"…","quantity":24,"unit":"hours","rate":100,"vat_percentage":21}
    ]
  },
  "payment_term_days": 14
}
```

> **Factuurtaal.** De PDF wordt gerenderd in `business.language` (default `nl`). Wil je een **Engelse
> factuur** — bv. voor een buitenlandse klant, of als de gebruiker daarom vraagt — zet dan
> `"language": "en"` in het `invoice`-object. Dat vertaalt alle labels (INVOICE, Description, VAT,
> betaalzin, …), de bedragen (`€1,234.56`) en de datums (`15 Mar 2026`); de bedragen/BTW zelf
> veranderen niet. Bij een verlegde factuur aan een EU-klant ligt Engels voor de hand. Laat je het
> veld weg, dan volgt de factuur de bedrijfs-default.
>
> **Buitenlandse klant.** Geef `country` mee in `client` (zoals in `clients.csv`). Is dat niet
> Nederland, dan zet de code het land onder het klantadres én onder je eigen adres.

Draai dan (vervang `<YYYY-QN>` door het kwartaal uit stap 4):
```
node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" record-invoice /tmp/factuur.json facturen/<YYYY-QN>/2026-0005.pdf
```
Dit berekent regels/subtotaal/BTW/totaal **en** de vervaldatum, rendert de PDF, en schrijft in één
keer `invoices.csv` + `invoice_items.csv` weg (kwartaalmapje wordt automatisch aangemaakt). **Je tikt
zelf geen enkel bedrag of datum over.** Het commando print de weggeschreven waarden terug (nummer,
vervaldatum, subtotaal, BTW, totaal, pad) — gebruik die in je melding. Bestaat het factuurnummer al,
dan stopt het commando en schrijft het niets (duplicaat-guard); kies dan een nieuw nummer. Het stopt
ook bij een ongeldige datum (geen `YYYY-MM-DD`), een factuur zonder regels of een aantal/tarief dat
geen getal is (punt als decimaalteken) — corrigeer de JSON en draai opnieuw.

Open daarna de PDF: `open facturen/<YYYY-QN>/2026-0005.pdf`. Meld kort: nummer, klant, totaal, pad.

> Concept i.p.v. verzonden? Zet `"status": "draft"` in `invoice` — concepten tellen niet mee in de
> aangifte. Default (zonder `status`) is `sent`.

## Factuureisen (Art. 35a Wet OB) — afgedwongen
Afzender naam/adres/BTW-nr/KvK/IBAN, klantnaam + adres, oplopend factuurnummer, factuurdatum,
≥1 regel met omschrijving/aantal/tarief, BTW-bedrag (of verleggings-vermelding). Ontbreekt er
iets bij afzender of klant → vul aan vóór je genereert. Details: `${CLAUDE_PLUGIN_ROOT}/rules/factuureisen.md`.

## Belangrijk
- `status` van een nieuwe factuur = `sent` (hij telt dan mee in de BTW-aangifte). Gebruik
  `draft` alleen als de gebruiker een concept wil — concepten tellen niet mee in de aangifte.
- Status later op `paid` zetten (+ betaaldatum): met `/betaald`. Een factuur
  corrigeren/verwijderen: met de hand in `invoices.csv`. De skill heeft geen verwijder-actie
  (bewuste keuze).
