---
name: setup-vink
description: Eenmalige onboarding — stelt de bedrijfsgegevens (afzender) en standaard betaaltermijn in door interactief data/business.json te vullen, en legt kort uit wat elke skill (/factuur, /zelffactuur, /bon, /betaald, /aangifte, /dashboard, /jaaropgave) doet. Roep aan bij eerste gebruik of als business.json nog ontbreekt.
allowed-tools:
  - Bash(mkdir -p *)
  - Bash(cp -n *)
  - Bash(cp -Rn *)
  - Bash(diff -q *)
  - Read
  - Write
---

# Setup / onboarding

Help een nieuwe gebruiker zijn administratie-map in gebruik te nemen: initialiseer de map met lege
templates, vul de **afzendergegevens** (`data/business.json`) en de **standaard betaaltermijn** in,
en geef een korte uitleg van de beschikbare skills. Dit is een eenmalige stap; daarna gebruikt de
gebruiker `/factuur`, `/bon`, enz.

De **code/skills/regels/templates** komen uit de plugin (`${CLAUDE_PLUGIN_ROOT}/...`); de **data**
komt in de huidige map (waar Claude Code draait) — die blijft van de gebruiker en overleeft
plugin-updates.

## Stappen

### 0. Initialiseer de map (alleen wat ontbreekt)
Zet bij eerste gebruik de lege template-bestanden klaar. `-n`/`-Rn` overschrijft niets wat er al
staat, dus dit is veilig om altijd te draaien (`|| true`: `cp -n` meldt een fout-status als een
bestand al bestaat — dat is hier juist de bedoeling):

```bash
mkdir -p data facturen bonnen aangiftes jaaropgaven
cp -Rn "${CLAUDE_PLUGIN_ROOT}/seed/data/." data/ || true
cp -n  "${CLAUDE_PLUGIN_ROOT}/seed/business.example.json" data/business.example.json || true
cp -n  "${CLAUDE_PLUGIN_ROOT}/seed/CLAUDE.md" CLAUDE.md || true
```

Dit maakt (indien nog niet aanwezig): de lege CSV-templates in `data/`, een voorbeeld
`business.example.json`, een project-`CLAUDE.md` met de mapconventies, en de uitvoer-mappen.
Bestaat alles al → er verandert niets en je gaat door naar stap 1.

**Bestond `CLAUDE.md` al?** Vergelijk 'm met de versie uit de plugin:
`diff -q "${CLAUDE_PLUGIN_ROOT}/seed/CLAUDE.md" CLAUDE.md`. Verschilt hij, dan is de plugin sindsdien
bijgewerkt (bv. nieuwe map-conventies) of heeft de gebruiker 'm zelf aangepast. Meld dat en vraag of je 'm
mag vervangen; zo ja, bewaar eerst de oude als `CLAUDE.md.bak`. Nooit ongevraagd overschrijven.

### 1. Check of er al een setup is
Lees `data/business.json`.
- **Bestaat het al** met een echte naam (niet "Jouw Bedrijfsnaam")? Meld dat de setup al gedaan
  is, toon de huidige kerngegevens (naam, BTW-nr, IBAN, betaaltermijn) en vraag of de gebruiker
  iets wil **wijzigen**. Zo nee → klaar. Zo ja → ga naar stap 3 voor de te wijzigen velden.
- **Bestaat het niet** (alleen `data/business.example.json`)? Ga door naar stap 2.

### 2. Korte introductie
Leg in 3-4 zinnen uit wat dit is: een lichtgewicht ZZP-administratie op platte bestanden, waar de
AI redeneert en `lib/admin.mjs` deterministisch rekent en schrijft. Noem dat je nu eerst zijn
bedrijfsgegevens nodig hebt om geldige facturen te kunnen maken (factuureisen Art. 35a Wet OB).

### 3. Vraag de bedrijfsgegevens
Vraag de velden hieronder. Vraag ze **gegroepeerd** (niet per stuk een aparte vraag) zodat de
gebruiker ze in één keer kan plakken, maar maak duidelijk welke verplicht zijn. Lees
`data/business.example.json` voor de exacte veldnamen/structuur.

**Verplicht** (anders kan er geen geldige factuur):
- `name` — bedrijfs-/handelsnaam (afzender op de factuur)
- `address` — straat + huisnummer
- `postal_code` — postcode
- `city` — plaats
- `coc_number` — KvK-nummer
- `vat_number` — BTW-id (formaat `NL........B..`)
- `iban` — rekeningnummer voor betaling

**Optioneel / met default:**
- `account_holder` — tenaamstelling rekening (default = `name`)
- `country` — default `Nederland`
- `phone`, `email`, `website` — komen op de factuur als ze ingevuld zijn (mogen leeg)
- `payment_terms_days` — standaard betaaltermijn in dagen (zie stap 4)
- `language` — standaardtaal voor factuur-PDF's én het dashboard: `nl` (default) of `en`. Vraag dit
  kort: schrijft de gebruiker vooral aan Nederlandse klanten (`nl`) of ook aan buitenlandse (`en`)?
  Dit is alléén de standaard — per factuur kan `/factuur` er alsnog een Engelse van maken (bv. voor
  een buitenlandse klant). De **aangifte** blijft altijd Nederlands (officiële Belastingdienst-rubrieken).
- `telemetry` — anonieme gebruiksping: `true` (default) of `false`. Stel hier geen vraag over, maar
  **meld het altijd** in één zin: Vink stuurt één keer per maand een anonieme ping naar vinkapp.nl
  (geen ID, geen administratiedata), zodat de maker ziet hoeveel mensen Vink gebruiken. Wil de
  gebruiker dat niet, zet dan `false`.

Wat de gebruiker leeg laat van de optionele velden: laat leeg ("") of gebruik de default. Vul
**nooit** zelf een KvK-/BTW-nummer of IBAN in — dat moet de gebruiker aanleveren. Ontbreekt een
verplicht veld, vraag er gericht naar voor je wegschrijft.

### 4. Betaaltermijn
Vraag de standaard betaaltermijn in dagen (`payment_terms_days`). Gangbaar bij ZZP: **14, 21 of
30 dagen**; default **14**. Dit is de standaard voor álle facturen; per klant kun je later een
afwijkende termijn zetten in de kolom `payment_terms` van `data/clients.csv`. `0` = direct
betalen.

### 5. Toon preview → bevestiging
Toon de samengestelde `business.json` compact (alle velden) en vraag bevestiging. Pas aan op
feedback en toon opnieuw.

### 6. Schrijf weg
Schrijf het JSON-object naar `data/business.json` (met de Write-tool, nette indentatie). Het
bestand blijft in de map van de gebruiker; de plugin zelf bevat alleen het lege voorbeeld.

### 7. Korte uitleg van de skills
Sluit af met een compacte uitleg (één regel per skill) zodat de gebruiker weet wat hij heeft:

- **/factuur** — verkoopfactuur maken (omzet). Genereert een PDF en boekt in de CSV's.
- **/zelffactuur** — factuur die je opdrachtgever namens jou maakte (self-billing) importeren; telt óók als omzet.
- **/bon** — bon/inkoopfactuur als kosten verwerken; classificeert de BTW en converteert vreemde valuta.
- **/betaald** — een verkoopfactuur op betaald zetten (status + betaaldatum).
- **/aangifte** — kwartaal-BTW-overzicht samenstellen ter voorbereiding van je aangifte.
- **/dashboard** — stand van zaken: openstaande facturen, omzet/kosten, eerstvolgende aangifte-deadline.
- **/jaaropgave** — jaarcijfers (omzet → belastbare winst) ter voorbereiding van je aangifte inkomstenbelasting.

Noem ook even: de map `${CLAUDE_PLUGIN_ROOT}/rules/` bevat de Nederlandse fiscale regels die de skills raadplegen, en dat
dit een **voorbereidend** hulpmiddel is — de feitelijke aangiftes (BTW en inkomstenbelasting) doet de
gebruiker zelf bij de Belastingdienst. Stel voor om als eerste een `/factuur` of `/bon` te proberen.

## Belangrijk
- Vul nooit zelf fiscale identifiers (KvK, BTW-nummer, IBAN) in — alleen de gebruiker levert die.
- Overschrijf een bestaande, ingevulde `business.json` niet zonder expliciete bevestiging.
- Dit raakt alleen `data/business.json`; klanten/facturen/bonnen komen via de andere skills.
