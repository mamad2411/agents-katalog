---
name: aangifte
description: Stel de kwartaal-BTW-aangifte samen uit de facturen en bonnen — berekent de rubrieken voor een dienstverlenende zzp'er (1a, 1b, 1e, 3b, 4a, 4b, 5a, 5b, 5g) en de ICP-opgaaf, genereert een PDF-overzicht en schrijft een regel weg naar aangiftes.csv. Ter voorbereiding van de aangifte op Mijn Belastingdienst Zakelijk.
allowed-tools:
  - Bash(node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" *)
  - Bash(open aangiftes/*)
  - Read
  - Write
---

# BTW-aangifte samenstellen

Maak een kwartaaloverzicht voor de BTW-aangifte uit alle verkoopfacturen en bonnen. De
gebruiker geeft een kwartaal op (bv. "Q1 2026", "dit kwartaal", "vorig kwartaal").

## Stappen

### 1. Bepaal het kwartaal
Reken om naar `YYYY-QN`. "Dit kwartaal" / "vorig kwartaal" → leid af van vandaag
(Q1=jan–mrt, Q2=apr–jun, Q3=jul–sep, Q4=okt–dec). Bij twijfel: vraag het kwartaal.

### 2. Bereken de rubrieken (deterministisch)
```
node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" aangifte 2026-Q2
```
Dit leest `invoices.csv` (alleen `status` sent/paid in het kwartaal) + `receipts.csv`
(`vat_period` = kwartaal) + `clients.csv`, en geeft JSON terug met:
- `rubrieken[]` — 1a (21%), 1b (9%), 1e (0% of niet bij jou belast, o.a. binnenlands verlegd),
  3a (uitvoer van goederen — altijd € 0, zie hieronder), 3b (diensten aan EU-ondernemers, verlegd),
  4a (inkoop buiten EU, verlegd), 4b (inkoop binnen EU, verlegd), 5a (verschuldigd),
  5b (voorbelasting), 5g (saldo).
- `omzet_buiten_eu` — verlegde omzet aan afnemers **buiten de EU**. Die staat bewust in géén rubriek:
  diensten die in het land van de afnemer belast zijn geef je niet aan in de btw-aangifte, en 3a is
  alleen voor uitvoer van goederen. Er komt een waarschuwing bij met bedrag en klantnamen — meld die.
- `icpEntries[]` + `icp_total` — intracommunautaire prestaties per EU-klant.
- `summary` (verschuldigd / voorbelasting / saldo), `saldo_richting`, `deadline`, `warnings`, `counts`.
- `exact` — omzet, verschuldigd, voorbelasting en saldo op centen, vóór afronding. Alleen ter
  verklaring als de gebruiker vraagt waarom een bedrag afwijkt van de facturen; niet om in te vullen.

**Alle rubrieken zijn hele euro's**, zoals het aangifteformulier vraagt. Btw-bedragen zijn in het
voordeel van de ondernemer afgerond (verschuldigd per rubriek naar beneden, voorbelasting naar boven),
omzet rekenkundig. Toon de bedragen ook zonder centen. Zie
`${CLAUDE_PLUGIN_ROOT}/rules/btw-tarieven.md` (sectie "Afronden op hele euro's").

De rekenregels (port van Vink `calculateBtw`): 5a = BTW van 1a+1b+4a+4b (de afgeronde rubrieken
opgeteld); 5b = voorbelasting + 4a-BTW + 4b-BTW, elk voor het zakelijke deel (`business_pct`), als
totaal afgerond; 5g = 5a − 5b. Door de afronding kan verlegde btw netto € 1 schelen. Niets zelf narekenen — gebruik deze output.

### 3. Toon het overzicht + waarschuwingen
Presenteer de rubrieken beknopt, het saldo (te betalen of terug te vragen) en de deadline.
Loop de `warnings` na en meld ze (concept-facturen niet meegeteld, ontbrekend `business_pct`,
geen data, geen bonnen). Als iets oogt alsof er data mist (bv. wel facturen maar 0 bonnen),
wijs daarop voordat je een PDF maakt.

### 4. Genereer PDF + leg vast (één deterministische stap)
Bouw `/tmp/aangifte.json`:
```json
{ "business": { …uit business.json… }, "aangifte": <de volledige JSON uit stap 2> }
```
Draai dan:
```
node "${CLAUDE_PLUGIN_ROOT}/lib/admin.mjs" record-aangifte /tmp/aangifte.json aangiftes/2026-Q2-btw-aangifte.pdf
```
Dit rendert de PDF **en** schrijft de `aangiftes.csv`-rij weg, rechtstreeks uit de berekende JSON —
**je tikt geen enkele rubriekwaarde over** (alle 18 kolommen mapt de code zelf). Het commando print
kwartaal, saldo, richting en deadline terug; gebruik die in je melding.
Open de PDF: `open aangiftes/2026-Q2-btw-aangifte.pdf`.

Meld kort: kwartaal, saldo (te betalen/terug), deadline, pad naar de PDF. Als er ICP-regels zijn,
herinner de gebruiker dat er naast de BTW-aangifte ook een **ICP-opgaaf** moet (zie
`${CLAUDE_PLUGIN_ROOT}/rules/icp-opgaaf.md`).

## Belangrijk
- Dit is een **voorbereidend overzicht**, geen ingediende aangifte. De gebruiker neemt de
  rubrieken over op Mijn Belastingdienst Zakelijk.
- Alleen facturen met `status` sent/paid tellen mee; concepten niet.
- **Niet ondersteund** — vult de gebruiker zo nodig zelf in: 1c (overige tarieven), 1d (privégebruik,
  bv. auto), 2a (binnenlands verlegde inkoop), 3a (uitvoer van goederen), 3c en 5d (KOR). Speelt een
  daarvan, zeg het erbij.
- Bonnen tellen mee op hun `vat_period`, niet op datum — zo kun je een vergeten bon in een al
  betaald kwartaal alsnog in het eerstvolgende kwartaal meenemen (geen suppletie nodig).
- Een al ingediend kwartaal opnieuw draaien geeft simpelweg een nieuwe PDF + extra CSV-regel; dat
  overschrijft niets. Corrigeren doet de gebruiker met de hand.
