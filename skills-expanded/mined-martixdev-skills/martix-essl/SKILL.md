---
name: martix-essl
description: >-
  Český standalone-first skill pro eSSL návrh, implementaci, code review a
  atestační připravenost podle zákona 499/2004 Sb., vyhlášky 259/2012 Sb.
  a Národního standardu eSSL. Použij, když dotaz řeší eSSL soulad nebo
  atestaci, metadata a životní cyklus dokumentu, WS API, SIP/METS, migraci,
  transakční protokol nebo auditovatelnost.
license: Complete terms in LICENSE.txt
---

# MartiX eSSL router

Použij tento skill pro **doménovou a compliance expertízu eSSL**. Převáděj
právní a standardizační požadavky do návrhu, implementačních rozhodnutí, code
review a checklistů.

Vedoucí pojem pro rozhodování: **trojvrstvý rámec** (zákon, vyhláška
a národní standard).

## Aktivace a hranice

### Aktivační signály

| Branch | Aktivační signál |
| --- | --- |
| Soulad a atestace | eSSL, spisová služba, atestace, auditovatelnost |
| Evidence a metadata | příjem/evidence dokumentů, vady, spisy, metadata entit |
| Životní cyklus a skartace | skartace, archivní předání, export/import |
| Integrace a schémata | `WS API`, `WSDL`, `XSD`, `SIP`, `METS`, `manifest` |
| Migrace a přenos | migrace mezi eSSL, přenosové dávky, potvrzení přenosu |

### Nespouštět jako hlavní skill

- čistě obecný `.NET/C#` dotaz bez jasné eSSL vazby -> handoff do
  `martix-dotnet-csharp`
- požadavek na formální právní stanovisko bez technického kontextu -> vysvětli
  limity a vrať technicko-doménové doporučení

## Výchozí postup

1. Urči, jestli jde primárně o **soulad**, **návrh**, **integraci**, nebo
   **review změny**.
1. Otevři nejmenší relevantní `rule` a k ní jednu `reference`.
1. Odděl:
   - normativní požadavek,
   - implementační doporučení,
   - riziko nebo chybějící důkaz,
   - zdroje.
1. Když eSSL doména končí, proveď handoff do `martix-dotnet-csharp`.

### Hotovo když

- je explicitně oddělen normativní požadavek od implementačního doporučení;
- je uvedené riziko pro audit nebo atestační připravenost;
- jsou uvedené konkrétní zdrojové soubory;
- u čistě obecných `.NET/C#` částí je doporučen handoff.

## Preferovaný tvar odpovědi

Použij co nejmenší užitečný formát:

- **Compliance/review:** `Shrnutí`, `Požadavky`, `Rizika`, `Doporučené kroky`,
  `Zdrojové soubory`.
- **Návrh řešení:** `Cíl`, `Dopady eSSL`, `Doporučený návrh`, `Otevřené otázky`,
  `Zdrojové soubory`.
- **Rychlá orientace:** `Krátká odpověď`, `Kde to hledat`, `Co ověřit dál`.

## Začni nejbližším workstreamem

| Workstream | Použij když | Otevři |
| --- | --- | --- |
| Scope, zdroje a handoffy | Potřebuješ rozhodnout, co je závazný zdroj, jaký je scope skillu nebo jestli už má nastat handoff | [rules/foundation-scope-a-zdroje.md](./rules/foundation-scope-a-zdroje.md), [references/doc-source-index.md](./references/doc-source-index.md), [references/pravni-ramec-a-povinnosti-map.md](./references/pravni-ramec-a-povinnosti-map.md) |
| Příjem, evidence a vady dokumentů | Řešíš podatelnu, doručení, validaci, podací razítko, identifikátory, základní nebo samostatnou evidenci | [rules/prijem-evidence-a-vady-dokumentu.md](./rules/prijem-evidence-a-vady-dokumentu.md), [references/zivotni-cyklus-dokumentu-map.md](./references/zivotni-cyklus-dokumentu-map.md) |
| Spisový plán, věcné skupiny a spisy | Navrhuješ zatřiďování, věcné skupiny, typové spisy, šablony, vazby a spisový plán | [rules/spisovy-plan-vecne-skupiny-a-spisy.md](./rules/spisovy-plan-vecne-skupiny-a-spisy.md), [references/zivotni-cyklus-dokumentu-map.md](./references/zivotni-cyklus-dokumentu-map.md) |
| Metadata a entity | Potřebuješ mapovat metadata dokumentu, spisu, komponenty, rejstříku nebo skartačních režimů | [rules/metadata-a-entity-model.md](./rules/metadata-a-entity-model.md), [references/metadata-crosswalk.md](./references/metadata-crosswalk.md), [references/glosar-zakladnich-pojmu.md](./references/glosar-zakladnich-pojmu.md) |
| Skartace, ukládání, export a přenos | Řešíš skartační režimy, skartační řízení, archivní předání, export nebo import | [rules/skartace-ukladani-prenos-a-vyrazeni.md](./rules/skartace-ukladani-prenos-a-vyrazeni.md), [references/skartace-a-archivacni-predani-map.md](./references/skartace-a-archivacni-predani-map.md), [references/atestacni-pripravenost-map.md](./references/atestacni-pripravenost-map.md) |
| Správa, bezpečnost a audit | Potřebuješ řešit role, přístup, znepřístupnění, ničení dokumentů nebo transakční protokol | [rules/sprava-bezpecnost-a-transakcni-protokol.md](./rules/sprava-bezpecnost-a-transakcni-protokol.md), [references/transakcni-protokol-a-audit-map.md](./references/transakcni-protokol-a-audit-map.md) |
| WS API a výměna dokumentů | Navrhuješ integrační rozhraní, synchronní/asynchronní operace a práci s WSDL/XSD | [rules/ws-api-a-vymena-dokumentu.md](./rules/ws-api-a-vymena-dokumentu.md), [references/ws-api-schema-map.md](./references/ws-api-schema-map.md), [references/xsd-wsdl-xml-index.md](./references/xsd-wsdl-xml-index.md) |
| SIP a METS | Stavíš datový balíček SIP, popisná metadata, METS nebo XLink vazby | [rules/sip-a-mets-balicky.md](./rules/sip-a-mets-balicky.md), [references/sip-mets-map.md](./references/sip-mets-map.md), [references/xsd-wsdl-xml-index.md](./references/xsd-wsdl-xml-index.md) |
| Migrace a exit plán | Řešíš migraci mezi eSSL, spisovou rozluku, dávky ZIP, manifest nebo potvrzení přenosu | [rules/migrace-a-exit-plan.md](./rules/migrace-a-exit-plan.md), [references/migrace-a-prenos-map.md](./references/migrace-a-prenos-map.md) |
| Soulad a implementační checklist | Potřebuješ převést požadavky do backlogu, review checklistu nebo atestačního plánu | [rules/soulad-review-a-implementacni-checklisty.md](./rules/soulad-review-a-implementacni-checklisty.md), [references/atestacni-pripravenost-map.md](./references/atestacni-pripravenost-map.md) |
| Code review dopadů | Posuzuješ konkrétní změnu v kódu nebo návrhu a chceš odhalit eSSL dopady | [rules/code-review-a-implementacni-dopady.md](./rules/code-review-a-implementacni-dopady.md), [references/atestacni-pripravenost-map.md](./references/atestacni-pripravenost-map.md), [AGENTS.md](./AGENTS.md) |

## Rychlé referenční plochy

- [Source index](./references/doc-source-index.md)
- [Právní rámec a povinnosti](./references/pravni-ramec-a-povinnosti-map.md)
- [Životní cyklus dokumentu](./references/zivotni-cyklus-dokumentu-map.md)
- [Metadata crosswalk](./references/metadata-crosswalk.md)
- [Index schémat](./references/xsd-wsdl-xml-index.md)
- [Mapa atestační připravenosti](./references/atestacni-pripravenost-map.md)
