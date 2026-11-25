---
name: betaald
description: Zet een verkoopfactuur op betaald — werkt voor zowel zelf-gemaakte facturen (/factuur) als geïmporteerde zelffacturen (/zelffactuur). Zet status op `paid` en legt de betaaldatum vast in `paid_at`. Verandert niets aan de BTW-aangifte (sent én paid tellen al mee).
allowed-tools:
  - Bash(node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" *)
  - Read
---

# Factuur op betaald zetten

De gebruiker meldt dat een verkoopfactuur betaald is. Zet de status op `paid` en leg de
**betaaldatum** vast in de kolom `paid_at`. Geldt voor **alle** rijen in `data/invoices.csv` —
zowel `source=created` (zelf gemaakt) als `source=imported` / self-billing.

Het rekenwerk en de veilige rij-herschrijving doet `admin.mjs` (principe: AI bepaalt WAT, code
bepaalt HOE). **Nooit zelf de CSV bewerken** — altijd via het commando hieronder.

## Stappen

### 1. Bepaal welke factuur
- De gebruiker geeft meestal een **factuurnummer** (bv. `2026-0006` of `IRB172600063`).
- **Geen of onduidelijk nummer?** Lees `data/invoices.csv` en toon de **openstaande** facturen
  (`status` = `sent`, dus nog niet `paid`): nummer, klant, totaal, datum. Vraag welke. Match
  desnoods fuzzy op klantnaam/bedrag/maand als de gebruiker dat noemt.
- Controleer dat het nummer bestaat in `data/invoices.csv`. Niet gevonden → meld het en stop
  (geef de dichtstbijzijnde matches als hint).
- Staat de factuur al op `paid`? Meld de bestaande `paid_at` en vraag of die overschreven moet
  worden voordat je doorgaat.

### 2. Bepaal de betaaldatum
- Gebruiker geeft een datum → gebruik die (formaat `YYYY-MM-DD`; reken een vorm als
  "10 juni" / "10-06-2026" om naar `2026-06-10`).
- **Geen datum opgegeven → vandaag** (dat is de default van het commando).

### 3. Zet op betaald
```bash
node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" mark-paid <factuurnummer> [YYYY-MM-DD]
```
- Zonder datum-argument → `paid_at` wordt vandaag.
- Het commando voegt de `paid_at`-kolom toe als die nog niet bestaat, zet `status=paid` en
  herschrijft `invoices.csv` atomisch. Het print het resultaat terug (incl. `was_already_paid`).

### 4. Meld kort
Nummer, klant, totaal en de vastgelegde `paid_at`. Bij meerdere facturen: per stuk een regel.

## Belangrijk
- **Alleen status + betaaldatum** — bedragen, BTW, regels of paden raak je niet aan.
- Geen effect op `/aangifte`: zowel `sent` als `paid` tellen al mee in de BTW-aangifte; `paid_at`
  is puur administratief (cashflow/debiteurenbewaking).
- Een betaling terugdraaien (`paid` → `sent`) of een verkeerde `paid_at` corrigeren: met de hand
  in `invoices.csv` (bewuste keuze — de skill zet alleen op betaald).
