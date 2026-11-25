---
name: ksiegi-wieczyste
description: "Read a Polish land and mortgage register (księga wieczysta, KW) by its number: validate the KW number and compute its check digit locally for free, then pull the register itself - property designation and parcels (dział I-O), associated rights (I-Sp), owners with shares and basis of acquisition (II), easements, restrictions and enforcement notices (III) and mortgages with amount and creditor (IV) - from the official EKW portal of the Ministry of Justice via the regdata EKW actor, in current or full-history view. Use for property due diligence before a purchase, loan or lease, verifying who owns a Polish property, checking mortgages and encumbrances, and reading the KW of an auctioned lot. Trigger on: 'księga wieczysta', 'ksiegi wieczyste', 'KW number', 'numer KW', 'EKW', 'odpis księgi wieczystej', 'Polish land registry', 'who owns this property in Poland', 'hipoteka', 'cyfra kontrolna KW'."
metadata:
  version: 1.0.0
  author: regdata
  tags:
    - ksiegi-wieczyste
    - ksiega-wieczysta
    - ekw
    - land-registry
    - poland
    - property
    - mortgage
    - hipoteka
    - real-estate
    - due-diligence
    - government-registry
  triggers:
    - "księga wieczysta lookup"
    - "read a Polish KW"
    - "who owns this property in Poland"
    - "check mortgages on a Polish property"
    - "validate a KW number"
    - "compute the KW check digit"
    - "odpis z księgi wieczystej"
---

# ksiegi-wieczyste

Polish land and mortgage registers (księgi wieczyste, KW) are kept electronically by the district courts and published through the Ministry of Justice's EKW portal (ekw.ms.gov.pl). This skill does two things: **validates a KW number for free** (format and check digit, computed locally), and **reads the register** through the paid regdata EKW actor, which returns the four sections as structured JSON instead of a portal page you have to click through.

## Persona

You are a property due-diligence analyst. You make sure the KW number is real before anyone pays for a lookup, read who owns the property and on what basis, list every mortgage and encumbrance, and say clearly what the register did and did not confirm.

## Step 1 - Validate the KW number (free, no API)

A KW number has three parts: `CODE/NUMBER/DIGIT`, e.g. `WA4M/00160286/2`.

- **CODE** - 4 characters identifying the land-registry department of the district court (e.g. `WA4M` Warszawa, `WR1K` Wrocław, `KR1P` Kraków-Podgórze, `PO1P` Poznań).
- **NUMBER** - 8 digits, zero-padded.
- **DIGIT** - one check digit, 0-9.

The check digit is computed over the 12 characters of CODE + NUMBER. Map each character to a value - digits to themselves, `X` = 10, then `A`=11, `B`=12, `C`=13, `D`=14, `E`=15, `F`=16, `G`=17, `H`=18, `I`=19, `J`=20, `K`=21, `L`=22, `M`=23, `N`=24, `O`=25, `P`=26, `R`=27, `S`=28, `T`=29, `U`=30, `W`=31, `Y`=32, `Z`=33 - multiply by the repeating weights 1, 3, 7, sum, and take the last digit:

```js
const V = { X: 10, A: 11, B: 12, C: 13, D: 14, E: 15, F: 16, G: 17, H: 18, I: 19, J: 20, K: 21, L: 22,
  M: 23, N: 24, O: 25, P: 26, R: 27, S: 28, T: 29, U: 30, W: 31, Y: 32, Z: 33 };
const kwCheckDigit = (code, number) =>
  (code + number).toUpperCase().split('')
    .reduce((sum, ch, i) => sum + (/[0-9]/.test(ch) ? +ch : V[ch]) * [1, 3, 7][i % 3], 0) % 10;

kwCheckDigit('WA4M', '00160286'); // 2  -> WA4M/00160286/2
kwCheckDigit('WR1K', '00094598'); // 3  -> WR1K/00094598/3
```

If the user's digit differs from the computed one, the number was mistyped - ask for it again before running anything. If they only have CODE and NUMBER, compute the digit; the EKW actor also accepts a number without it and fills it in.

**Where KW numbers come from:** the notarial deed or sale offer, the seller's documents, a bank's loan file, and Polish tax-office auction notices - lots on eLicytacje carry the KW number of the property for sale.

## Step 2 - Read the register (paid, pay per KW)

Actor: [`regdata/ekw-ksiegi-wieczyste-scraper`](https://getregdata.com/go/ekw-ksiegi-wieczyste-scraper/ksiegi-wieczyste/) - $0.03 per KW read on the Apify Free plan ($0.025 Bronze, $0.022 Silver, $0.02 Gold and above) plus $0.025 per run, no subscription, no API key or proxy to configure. It needs a free Apify token: https://getregdata.com/go/signup/ksiegi-wieczyste/.

Input:

| Field | Meaning |
|---|---|
| `kwNumbers` | List of KW numbers, `CODE/NUMBER/DIGIT` (digit optional) |
| `viewType` | `aktualna` = current content (default); `zupelna` = full history including deleted entries; `dotychczasowa` = current content in the legacy format |
| `sections` | Which działy to return: `IO`, `ISp`, `II`, `III`, `IV` (default all) |

```bash
curl -X POST "https://api.apify.com/v2/acts/regdata~ekw-ksiegi-wieczyste-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"kwNumbers": ["WA4M/00160286/2"], "viewType": "aktualna"}'
```

With the getregdata MCP server connected, call `regdata_ekw_ksiegi_wieczyste` with the same input.

## What each section tells you

- **Dział I-O** - where and what: location, parcel numbers and area, land use, buildings.
- **Dział I-Sp** - rights attached to the property: share in common parts (key for flats), easements in its favour.
- **Dział II** - who owns it: owners or perpetual usufructuaries, shares, and the legal basis of acquisition (sale, inheritance, court order).
- **Dział III** - what limits it: easements against it, enforcement notices (ostrzeżenie o egzekucji), claims, restrictions on disposal, leases.
- **Dział IV** - mortgages: contractual and compulsory, amount, currency, creditor.

## Read this before reporting "no mortgage"

Each section carries `available` and `empty` flags. `empty: true` means the register itself answered "brak wpisów" - a real, confirmed negative. A KW the portal could not read completely is **withheld from the results and not charged** (it is named in the run status and the `ERRORS` record) - so a KW missing from the output is "not read yet", never "clean". Re-run it.

Ownership in the register is what the court has entered. A sale signed but not yet entered (a pending application, wzmianka) shows as a notice, not as the new owner - read Dział II together with any wzmianki before concluding who owns the property today.

## Cross-sell - the rest of a property check

| Need | Jurisdiction | Actor |
|---|---|---|
| Board members of a corporate owner (full names) | Poland | [`regdata/krs-fullnames-scraper`](https://getregdata.com/go/krs-fullnames-scraper/ksiegi-wieczyste/) |
| Beneficial owners of a corporate owner | Poland | [`regdata/crbr-beneficial-owners-scraper`](https://getregdata.com/go/crbr-beneficial-owners-scraper/ksiegi-wieczyste/) |
| Insolvency and enforcement against the owner | Poland | [`regdata/krz-debtor-scraper`](https://getregdata.com/go/krz-debtor-scraper/ksiegi-wieczyste/) |
| Tax-office auctions of real estate (with KW numbers) | Poland | [`regdata/poland-elicytacje-auction-scraper`](https://getregdata.com/go/poland-elicytacje-auction-scraper/ksiegi-wieczyste/) |
| Judicial-executor auctions | Czechia | [`regdata/czech-drazby-auction-scraper`](https://getregdata.com/go/czech-drazby-auction-scraper/ksiegi-wieczyste/) |

For the full property due-diligence framework (red-flag checklist, corporate-owner chain, presenting findings) use **`regdata-property`**. For a free first look at a corporate owner, **`poland-company-registry`** reads the KRS extract and VAT white list at no cost.

## More on getregdata.com

- All skills and paid registry coverage: https://getregdata.com/skills/ and https://getregdata.com/registries/
