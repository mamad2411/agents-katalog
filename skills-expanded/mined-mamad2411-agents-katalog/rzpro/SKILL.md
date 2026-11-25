---
uuid: 9a4c1f72-6b8e-4d03-a5f1-2c7b0e9d6a48
name: rzpro
icon: icon.svg
description: Registr zdravotnických prostředků (RZPRO, KSRZIS). Use for Czech medical device lookups by device name or evidence number - manufacturer, device kind, risk class, intended purpose, notified body, variants/catalogue numbers, and registered persons and their activities. Triggers on "zdravotnický prostředek", "RZPRO", "evidenční číslo", "notifikovaný prostředek", "výrobce zdravotnických prostředků", "registr ZP", "najdi prostředek", "diagnostický prostředek", "IVD".
version: 1.2.0
jurisdictions: [CZ]
i18n:
  cs:
    displayName: "RZPRO - registr zdravotnických prostředků"
    summary: "Vyhledávání zdravotnických prostředků v registru RZPRO - podle názvu nebo evidenčního čísla, výrobce, varianty, osoby."
    examplePrompts:
      - "Najdi v registru zdravotnických prostředků katetry a vypiš výrobce a rizikovou třídu."
      - "K jakému zdravotnickému prostředku patří katalogové číslo 4157744?"
      - "Jaké zdravotnické prostředky má v registru ohlášené firma B. Braun?"
  en:
    displayName: "RZPRO - Medical Devices Registry"
    summary: "Look up medical devices in the RZPRO registry - by name or evidence number, manufacturer, variants, persons."
    examplePrompts:
      - "Find catheters in the medical device register and list manufacturer and risk class."
      - "Which medical device does catalogue number 4157744 belong to?"
      - "Which medical devices has B. Braun notified in the register?"
  sk:
    displayName: "RZPRO - register zdravotníckych pomôcok"
    summary: "Vyhľadávanie zdravotníckych pomôcok v registri RZPRO - podľa názvu alebo evidenčného čísla, výrobca, varianty, osoby."
    examplePrompts:
      - "Nájdi v registri zdravotníckych pomôcok katétre a vypíš výrobcu a rizikovú triedu."
      - "Ku ktorej zdravotníckej pomôcke patrí katalógové číslo 4157744?"
      - "Aké zdravotnícke pomôcky má v registri ohlásené firma B. Braun?"
---

# RZPRO - registr zdravotnických prostředků

Structured access to the Czech Register of Medical Devices (**RZPRO**, KSRZIS).
A single tool - **`rzpro-cli`** - wraps the ai-scraper search API. There is no
local database; every command is an API call.

**IMPORTANT:** The only tool in this skill is `rzpro-cli`. Do NOT call `curl` or
any other tool. Assume `rzpro-cli` is installed and available in `PATH`.

**IMPORTANT:** When `rzpro-cli` prints an `error:` line, stop and report it. Do
NOT guess workarounds and do NOT blindly retry. When looking up several items,
run each independently.

## Commands

### search
- Devices: `rzpro-cli search CZRZP [OPTIONS]`
- Persons/companies: `rzpro-cli search CZRZP-OS [OPTIONS]`

See `rzpro-cli search CZRZP --help` / `CZRZP-OS --help` or
`references/search-rzpro.md` for the filter lists. Output is JSON on stdout:
`{ "results": [...], "total": N, "offset": N, "limit": N }`.

**Always pipe it through `jq`** and select only the fields you need. A bare call puts
every field of every result into the context window; with a pipe, only the `jq` output
does. This matters most at `--limit 100`.

### get
`rzpro-cli get <rzpro://…> [--dry-run]`:

| Resource | Returns |
|---|---|
| `rzpro://doc/<DOC_ID>/meta` | full device record - kind, risk class, intended purpose, manufacturer, variants/catalogue numbers, validity |
| `rzpro://osoba/<KEY>` | a registered person/company by IČO or Registrační číslo, with the devices it notified |
| `rzpro://doc/values/<FIELD>` | distinct values + counts - `FIELD` ∈ `druh\|riziko\|stat` |

## Workflow

1. Device by name - words match device name, trade name and manufacturer together.
   Keep `docId` for the follow-up `get`:
   ```
   rzpro-cli search CZRZP --query "katetr" \
     | jq '.total, (.results[] | {docId, nazev, druh, miraRizika, vyrobce})'
   ```
2. Device by evidence number → take the `docId` → `get …/doc/<docId>/meta`:
   ```
   rzpro-cli search CZRZP --evidencni-cislo 01-0000019-19 \
     | jq '.results[] | {docId, nazev, obchodniNazev, stav}'
   ```
3. Which device a catalogue number belongs to:
   ```
   rzpro-cli search CZRZP --katalogove-cislo 4157744 \
     | jq '.results[] | {docId, nazev, vyrobce}'
   ```
4. A company (activities + notified devices) - `osoba` returns
   `{person, devices}`, so select from each branch. To search companies by name,
   use the `CZRZP-OS` source:
   ```
   rzpro-cli get rzpro://osoba/27082440 | jq '{person: .person, pocetProstredku: (.devices | length)}'
   rzpro-cli search CZRZP-OS --query "Braun" | jq '.results[] | {nazev, regCislo, evidencniCislo}'
   ```
5. Variants and linked persons of a device live inside the `/meta` record, which
   wraps it as `{docId, device}` - the raw columns are under `.device`. List the keys
   once, then select:
   ```
   rzpro-cli get rzpro://doc/CZRZP00000019/meta | jq '.device | keys'
   rzpro-cli get rzpro://doc/CZRZP00000019/meta | jq '.device | {nazev, miraRizika}'
   ```

When a filter yields `null`, inspect the keys with `jq 'keys'` (or `.device | keys`)
rather than guessing the field name.

## Result fields (device search)

Each item in `results[]`: `docId` (internal id - for `get`, never shown to the
user), `evidencniCislo`, `nazev`, `obchodniNazev`, `stav`, `isActive`, `druh`,
`miraRizika`, `vyrobce` (manufacturer-of-record, incl. foreign makers),
`platnostDo`.

## Presenting results

Present readably - device name, kind, risk class, manufacturer, validity. Do NOT
dump raw JSON; pull only what you need with `jq`. Never
show a raw `docId` (`CZRZP…`), a `CZRZP` / `CZRZP-OS` source code, a `rzpro://`
address, or an env-var name to the user.

## Pagination & truncation

`search` returns `total` but only `limit` results (**default 20, max 100**).

**Pick the page size before the call, from what you need.** Re-running the same search
with a bigger `--limit` costs a whole extra round trip and leaves both outputs in
context - the first page is paid for twice.

| What you need | Call |
|---|---|
| One device / one evidence number (targeted) | default `--limit 20` |
| Completeness - every device of a manufacturer, every variant | `--limit 100` straight away |
| Just a count | `--limit 1`, read `total`, stop |

When `total` still exceeds what you received, page with `--offset`. **Do NOT draw a
global conclusion** from a truncated page. Deep paging is capped:
`offset + limit <= 10000`.

## Notes

- Risk classes are tied to the device kind (general `I`-`III`; active implantable
  `AI`; IVD `IVD*` / `IVDR *`) - "implantable class III" yields 0; use `AI`. See
  `references/search-rzpro.md`.
- `vyrobce` is the manufacturer-of-record and is always present, including foreign
  makers. The linked Czech-registered persons (with notifier/edit rights) are in
  the `/meta` record; that list is empty for foreign manufacturers.

## Reference Files

- **`references/search-rzpro.md`** - full device + person filter lists.
