---
name: zelffactuur
description: Importeer een verkoopfactuur die je opdrachtgever namens jou heeft gemaakt (self-billing / "factuur uitgereikt door afnemer"). Telt als omzet — net als /factuur — maar je maakt 'm niet zelf en genereert geen PDF; je neemt het bestaande document over met zijn eigen factuurnummer.
allowed-tools:
  - Bash(node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" *)
  - Bash(mkdir -p facturen/*)
  - Bash(cp * facturen/*)
  - Read
  - Write
---

# Zelffactuur / self-billing importeren

De gebruiker geeft een **verkoopfactuur** op die hij **niet zelf heeft gemaakt** — een
opdrachtgever of intermediair (bv. een detacheerder/bemiddelaar zoals Yacht, Hays, Tentoo)
heeft die namens hem uitgereikt op basis van goedgekeurde uren. Dit is **omzet**
(verkoopfactuur), géén kost.

Belangrijk onderscheid (zie `${CLAUDE_PLUGIN_ROOT}/rules/self-billing.md`):
| | Verkoopfactuur (`/factuur`) | Self-billing (`/zelffactuur`) | Inkoopfactuur (`/bon`) |
|--|--|--|--|
| Richting | uitgaand, ik maak 'm | inkomend, afnemer maakt 'm | inkomend |
| Wat | omzet | **omzet** | kosten |
| BTW | verschuldigd 1a/1b | **verschuldigd 1a/1b** | voorbelasting 5b |

## Stappen

### 1. Lees het document
Lees de PDF/afbeelding en extraheer:
- **Factuurnummer** = dat van de opdrachtgever/intermediair (bv. `IRB172600055`). **Niet** jouw
  eigen `YYYY-NNNN`-reeks en **niet** `next-invoice-number` gebruiken.
- **Factuurdatum**, **vervaldatum**.
- **Opdrachtgever** (de afnemer die de factuur uitreikt — bv. Voorbeeld Opdrachtgever B.V.) +
  adres + diens **BTW-nummer** (staat meestal onderaan, bv. "Btw-nummer … NL000000000B01").
- **Regels**: omschrijving, aantal, tarief, bedrag (bv. "Normale uren 32,00 × 95,00 = 3.040,00").
- **Subtotaal (excl. BTW)**, **BTW-tarief + bedrag**, **totaal**.

### 2. Bevestig dat het self-billing is
Self-billing als het document tekst bevat als **"factuur uitgereikt door (de) afnemer"**,
"self-billing", "zelffacturering" of "invoice issued by the recipient". Dan `self_billing=true`.
Een gewone verkoopfactuur die je elders maakte en alleen wilt importeren: `self_billing=false`,
`source=imported`. Beide tellen als omzet.

> Let op (wettelijk): bij self-billing mag je **niet** óók zelf een `/factuur` sturen voor dezelfde
> levering. Importeer 'm hier; maak 'm niet met `/factuur`.

### 3. BTW
Vrijwel altijd NL-omzet met verschuldigde BTW: `vat_percentage` van het document (meestal 21,
soms 9), `vat_reverse_charged=false`. Alleen verlegd als het document dat expliciet vermeldt.

### 4. Match/maak de opdrachtgever als klant
Zoek de opdrachtgever in `data/clients.csv` (fuzzy). Niet gevonden → voeg een rij toe met nieuw
`id` (`c_002`, … hoogste +1): naam, adres, postcode, plaats, land, `country_type=nl`, het
BTW-nummer van het document, evt. `attention`.

### 5. Preview (compact) → bevestiging
Bouw `/tmp/zelffactuur.json` — alléén de **WAT**, met de bedragen **zoals ze op het document staan**:
```json
{
  "client": { "id": "c_002", "name": "Voorbeeld Opdrachtgever B.V." },
  "invoice": {
    "number": "IRB172600055", "date": "2026-05-31", "due_date": "2026-06-30",
    "self_billing": true, "vat_reverse_charged": false,
    "subtotal": 3040.00, "vat_amount": 638.40, "total": 3678.40,
    "reference": "", "notes": "",
    "pdf_path": "facturen/2026-Q2/IRB172600055.pdf",
    "line_items": [
      {"description":"Normale uren","quantity":32,"unit":"hours","rate":95,"amount":3040.00,"vat_percentage":21}
    ]
  }
}
```
- `number` = het factuurnummer van de opdrachtgever; `subtotal` / `vat_amount` / `total` = de totalen van
  het document; per regel `amount` = het regelbedrag van het document.
- Eenheid: "uren"/"normale uren" → `hours`; anders de passende `unit` (`days`, `pieces`, `months`, `times`).
- `pdf_path` = waar het origineel komt te staan (stap 6): `facturen/<YYYY-QN>/<factuurnummer>.pdf`, met
  `<YYYY-QN>` = kwartaal uit de factuurdatum (Q1=jan–mrt, … Q4=okt–dec).

Draai dan:
```
node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" compute-imported-invoice /tmp/zelffactuur.json
```
Dit rekent de regels na tegen het subtotaal, de btw en het totaal van het document, zonder iets weg te
schrijven. **Sluit het niet aan, dan stopt het commando en zegt het wat afwijkt.** Lees het document dan
opnieuw (verkeerd overgenomen bedrag, gemiste regel) — pas nooit een bedrag aan om het kloppend te maken.

Toon: factuurnummer (van opdrachtgever), opdrachtgever, datum, regels, subtotaal/BTW/totaal,
en "self-billing: ja/nee". Vraag bevestiging.

### 6. Na bevestiging: bewaar origineel + leg vast
1. **Bewaar het originele bestand** in het kwartaalmapje `facturen/<YYYY-QN>/` (bewaarplicht). Maak
   het mapje eerst aan: `mkdir -p facturen/<YYYY-QN>`, en kopieer het bronbestand van de gebruiker naar
   het pad dat je als `pdf_path` opgaf (bv. `facturen/2026-Q2/IRB172600055.pdf`). Geen PDF genereren —
   die bestaat al.
2. **Leg vast:**
   ```
   node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" record-imported-invoice /tmp/zelffactuur.json
   ```
   Dit rekent opnieuw na en schrijft `invoices.csv` (`source=imported`, `status=sent`) en
   `invoice_items.csv` in één keer weg. **Je tikt zelf geen rij over.** Het commando stopt zonder iets te
   schrijven als het factuurnummer al in `invoices.csv` staat (niet dubbel importeren) of als het
   origineel niet op `pdf_path` staat. Het print de weggeschreven waarden terug — gebruik die in je melding.

Meld kort: factuurnummer, opdrachtgever, totaal, dat het als omzet is geboekt (rubriek 1a/1b),
en dat het origineel in `facturen/<YYYY-QN>/` staat. Het telt automatisch mee in `/aangifte`.

## Belangrijk
- `status="sent"` (telt mee in de BTW-aangifte). Markeer 'm later op `paid` met `/betaald`
  (zet ook de betaaldatum `paid_at`) als hij betaald is.
- De urenspecificatie (vaak pagina 2) hoeft niet als losse regels — neem de factuurregel(s) van
  pagina 1 over. Bewaar de volledige PDF (incl. specificatie) voor de bewaarplicht.
- Geen verwijder-actie via de skill — corrigeren doet de gebruiker met de hand in de CSV.
