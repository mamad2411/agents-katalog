# Skill: Clean Architecture

## Metadata

- Owner: Engineering Team
- Stability: Stable
- Last reviewed: 2026-02-26

## Related skills

- `data-modeling-persistence.skill.md` (modellvalg, persistence-grenser og mapping)
- `database-and-migrations.skill.md` (operativ migrasjonsdrift, deployrekkefølge, backup/restore)

## Terminologi (standard)

- `schema` og `skjema` brukes synonymt; i ny tekst foretrekkes `skjema`.
- `forward-only` brukes som standard term for migrasjonsretning i docs som omhandler databasedrift.
- `rollback` brukes kun om eksplisitt rollback-strategi; ellers foretrekkes korrigerende migrasjon.

## Mål

Designe og implementere kode der domenet er stabilt, testbart og uavhengig av rammeverk, database og transportlag.

Bygge systemer som er:

- enkle å endre
- uavhengige av rammeverk
- testbare uten infrastruktur
- motstandsdyktige mot teknologibytte
- strukturert rundt forretningsregler

Clean Architecture handler primært om avhengighetsretning og ansvar, ikke om mappe-navn alene.

## Når den brukes

- Når nye moduler eller features designes
- Når eksisterende kode refaktoreres mellom lag
- Når avhengigheter legges til eller endres

## Kjerneprinsipper

- Avhengigheter peker innover mot domene (må aldri brytes)
- Forretningsregler er rammeverksuavhengige (må aldri brytes)
- Sideeffekter isoleres i ytterlag (må aldri brytes)

## Kjerneprinsipper (må aldri brytes)

1. Avhengigheter peker innover
   - Kode i indre lag skal ikke importere fra ytre lag.
   - `domain` kjenner verken `application`, `infrastructure` eller web-rammeverk.
   - Gyldig retning: UI/API/DB -> Application -> Domain.
   - Ugyldig retning: Domain -> DB, Domain -> React, Domain -> WordPress.

2. Domene er kjernen
   - Forretningsregler og modeller skal ligge i `domain`.
   - Domenet skal være rent, deterministisk og lett å teste isolert.
   - Domenet skal kunne kjøre i test uten nettverk, database eller UI.

3. Rammeverk er detaljer
   - React, Next.js, WordPress, PostgreSQL og lignende er detaljer i ytterlag.
   - Valg av rammeverk skal ikke styre forretningsmodellen.

4. Use-cases orkestrerer
   - `application` styrer flyt mellom domene og porter.
   - Use-cases inneholder ikke tekniske detaljer om DB, HTTP, filer eller UI.
   - Use-case beskriver hva som skjer ved en forretningshandling, ikke hvordan HTTP/rammeverk fungerer.

5. Infrastruktur implementerer porter
   - `infrastructure` implementerer grensesnitt definert innover.
   - Bytte av database, API-klient eller framework skal ikke kreve domenerewrite.

## Standard lagdeling (pragmatisk)

For de fleste webprosjekter holder fire lag:

- `domain`
- `application` (use-cases)
- `infrastructure`
- `interface` (UI/API)

Ikke introduser flere lag uten konkret smerte.

## Ansvarsfordeling per lag

Domain:

- entities
- value objects
- domain services
- forretningsregler
- ingen IO og ideelt ingen sideeffekter

Application:

- use-cases
- orkestrering
- transaksjonsgrenser
- definerer porter (interfaces)

Infrastructure:

- database-implementasjoner
- API-klienter
- filsystem
- WordPress-integrasjon og andre eksterne adaptere

Interface:

- React-komponenter
- controllers
- API-routes
- HTTP-mapping mellom request/response og use-case input/output

## Domain vs Application (kritisk avgrensning)

Domain:

- inneholder forretningsregler som alltid gjelder
- inneholder invariants
- beskytter konsistens
- kan brukes av flere use-cases

Application:

- beskriver én konkret forretningshandling
- koordinerer steg
- kaller domeneobjekter
- skal ikke eie forretningsregler som hører hjemme i domain

Hvis en regel gjelder uansett use-case, hører den hjemme i `domain`, ikke i `application`.

## Aggregate boundary-regel

- Aggregate root er konsistensgrense i domenet.
- Én repository per aggregate root er default.
- Kryss-aggregate referanser skal skje via ID, ikke via direkte objektgraf.
- Kryss-aggregate regler orkestreres i `application`, ikke ved å bryte domenegrenser.

## Invariants-regel

- Domenemodeller skal beskytte sine egne invariants.
- Ugyldige tilstander skal ikke være mulig å representere.
- Validering som beskytter forretningskonsistens skal ligge i `domain`.

Eksempel:

- Feil: use-case sjekker om `Order` kan fullføres.
- Riktig: `Order.complete()` validerer reglene selv.

## Operativ arbeidsflyt

1. STEP 1: Definer use-case og domeneansvar
2. STEP 2: Plasser ansvar i riktig lag
3. STEP 3: Definer port-kontrakter innover
4. STEP 4: Implementer use-case + domene logikk
5. STEP 5: Implementer adapter i infrastructure/interface
6. STEP 6: Verifiser avhengighetsretning og tester

Hvis et steg hoppes over, regnes det som brudd på skill-regelverket.

## Hard Stop-regel

Hvis du må importere et ytre lag inn i et indre lag, skal du:

- Stoppe
- Forklare hvorfor designet bryter dependency rule
- Trekke ut port/kontrakt i riktig lag
- Implementere adapter i ytterlaget

Stopp også hvis:

- aggregate boundary er uklar og krever krysslag-kobling for å fungere
- transaksjonsgrense blir implisitt eller skaper risiko for partial commit

## Kompleksitetsindikatorer

Designet skal forenkles eller refaktoreres når:

- en use-case kjenner til både domene- og infrastrukturdetaljer
- samme forretningsregel finnes i flere lag
- data må oversettes mange ganger uten tydelig grense
- en endring i DB/API krever endring i `domain`

## Kognitiv belastning

Arkitekturen skal være lett å forstå sekvensielt:

- leseren skal raskt se hvor domene, use-case og adapter hører hjemme
- grunnforståelse av en feature skal ikke kreve hopping gjennom mange lag
- filnavn og mapper skal uttrykke ansvar tydelig
- lagstrukturen skal ikke være dypere enn nødvendig
- en enkel feature skal normalt ikke kreve mer enn 3-4 filer for grunnforståelse

Hvis det er uklart hvor kode hører hjemme, er designet for komplekst.

## DTO-regel

- Transportobjekter (HTTP request/response) skal aldri brukes direkte i `domain`.
- Domenemodeller skal ikke eksponeres direkte som API-respons.
- Mapping skjer ved laggrensene.

## Hva "bekreftelse" betyr

- Gyldig: tester passerer, og importretning følger dependency rule.
- Ugyldig: funksjonalitet virker, men indre lag avhenger av ytre lag.
- Bekreftelse skal inkludere minst én test på use-case-nivå.

## Regler (må/skal)

- Må: `domain` skal ikke ha framework-, DB- eller HTTP-avhengigheter.
- Må: `application` skal avhenge av porter, ikke konkrete adaptere.
- Må: sideeffekter skal ligge i `infrastructure`/`interface`.
- Må: én use-case skal representere én konsistent forretningsoperasjon.
- Skal: bruk konsistente mapper/navn per lag.
- Skal: hold use-cases små og fokuserte på én forretningshensikt.

## Import-regel (operativ dependency rule)

- `domain` skal ikke ha imports utenfor eget lag.
- `application` kan importere `domain`.
- `infrastructure` kan importere `application` og `domain`.
- `interface` kan importere `application` (streng variant: ikke `domain` direkte).

## Transaksjonsregel

- Én use-case = én konsistent forretningsoperasjon.
- Transaksjonsgrenser defineres i `application`-laget.
- `domain` skal ikke håndtere transaksjonsstyring.
- Kryss-aggregate operasjoner skal ha eksplisitt konsistensstrategi.
- Partial commits er forbudt.

## Query vs Command (CQRS-light)

- Skrivemodell i `domain`/`application` optimaliseres for invariants og korrekthet.
- Lesemodell kan optimaliseres separat i `infrastructure` for spørringsbehov.
- CQRS-light skal ikke brukes som unnskyldning for lagbrudd eller dupliserte forretningsregler.

## Feilhåndtering skal være konsistent

- Definer ett feilmønster per lag (exceptions eller result-type).
- Ikke bland tekniske feil direkte inn i domenets språk.
- Oversett infrastrukturfeil ved grensen før de når use-case/domene.

## Forskjell på "ny" og "endre"

Eksisterende arkitekturkode kan endres når:

- avhengighetsretning brytes
- ansvar ligger i feil lag
- krav krever ny grense/port

Eksisterende struktur skal ikke endres kun for stil uten verdi.

## Forbudte handlinger

- Importere `infrastructure` fra `domain`.
- Legge forretningsregler i controllere/adapters.
- Koble use-cases direkte til konkrete databaseklasser.
- Blande DTO-er fra transportlaget med domenemodeller uten grense.
- Kalle HTTP-klient direkte fra domene.
- Blande use-case-logikk inn i React-komponenter.
- Legge forretningsregler i API-routes.
- Lage "service"-lag som kun videresender kall uten tydelig ansvar.

## Service-navn-regel

- "Service"-klasser må ha presist ansvar.
- Generiske navn som `Manager` eller vag `Service` er ikke tillatt uten tydelig rolle.

## Anti-overengineering-regel

Følgende er ikke tillatt uten dokumentert behov:

- unødvendige lag og mapper
- porter/interfaces uten reell variabilitet
- kompleks mapping for enkle domeneobjekter
- abstrakte basisklasser som skjuler enkel flyt
- generiske repository-mønstre uten konkret behov
- CRUD-sentrisk standardarkitektur uten forretningsbehov

Ikke introduser nytt lag før det finnes konkret smerte.

## Abstraksjonstest (før ny abstraksjon)

Før ny port/abstraksjon legges til, sjekk:

- Finnes minst to realistiske implementasjoner?
- Reduserer dette kobling og gjør testing enklere?
- Forenkler dette lesing av use-case-flyt?

Hvis nei, vent med abstraksjonen.

## Repository-regel

- Ikke lag repository-interface før du faktisk trenger variasjon.
- Ikke lag ett generisk repository for alle entiteter som default.
- Design repository per use-case-behov, ikke per CRUD-mal.
- Hold repository-kontrakter aggregate-orienterte, ikke ORM-orienterte.

## Teststrategi per lag

Domain:

- skal være 100% testbar isolert
- tester forretningsregler uten IO

Application:

- test use-cases med mockede porter
- verifiser orkestrering og feilflyt

Infrastructure:

- integrasjonstester mot faktiske adaptere

Interface:

- UI-tester eller API-tester for mapping og kontrakt

## Kvalitetskriterier

- Kriterium 1: Domene kan testes isolert uten IO.
- Kriterium 2: Use-case bruker porter, ikke konkrete adaptere.
- Kriterium 3: Infrastruktur kan byttes uten endring i domene.
- Kriterium 4: Avhengighetsretning er konsekvent innover.
- Kriterium 5: Kodeplassering er intuitiv for nye utviklere.

## Granularitetsregel

Arkitekturendringer skal gjøres i små steg:

- flytt én ansvarsenhet om gangen
- verifiser tester og importretning etter hvert steg
- unngå store omskrivninger uten plan/ADR

## Tillatt vs ikke tillatt forbedring

Tillatt:

- flytte kode til riktig lag
- innføre port for å bryte konkret kobling
- isolere sideeffekter i adapters

Ikke tillatt:

- skjult feature-utvikling under arkitekturrefaktorering
- endre domenekontrakter uten krav
- introdusere nye lag uten dokumentert problem

## Definisjon av ferdig

Skillen er fulgt riktig når:

- forretningsregler ligger i domene
- use-case orkestrerer flyten
- infrastruktur implementerer porter
- UI/API-laget er tynt
- ansvar er plassert i riktig lag
- dependency rule er oppfylt
- tester verifiserer domene/use-case uten infrastrukturavhengighet
- sideeffekter er isolert i ytterlag

## Operativ kontrakt for AI-agenter

Agenten skal:

- alltid spørre: "Hvilket lag tilhører dette?"
- alltid starte med domene/use-case før adapterdetaljer
- stoppe ved lagbrudd og korrigere importretning
- foretrekke minste arkitektoniske grep som løser problemet
- dokumentere større arkitekturvalg i ADR
- flytte logikk innover når den kan være rammeverksuavhengig
- forklare lagplassering eksplisitt i endringer

For React/Next/WordPress-kontekst:

- WordPress behandles som adapter, ikke sannhetskilde for forretningsregler
- React-komponenter holdes tynne
- Domain er systemets sannhetskilde for regler

## Direktehet-prinsippet

Foretrekk:

- eksplisitt flyt: input -> use-case -> domene -> output
- tydelige porter mellom lag
- konkrete adaptere i ytterlag

Unngå:

- indirekte kontrollflyt som skjuler laggrenser
- rammeverksdetaljer i domene/use-case
- abstraksjoner som gjør flyten vanskelig å følge

Ekstra streng variant:

- Agenten skal aldri introdusere lagbrudd for å "få ting til å virke raskt".
- Agenten skal behandle dependency rule som absolutt.

## Eksempel

Dårlig:

- `domain/order.ts` importerer `databaseClient` direkte.
- `loginUseCase` kjenner HTTP-request/response-objekter.

Bedre:

- `domain` inneholder regler og entiteter uten IO.
- `application/login-user.ts` bruker `UserRepository`-port.
- `infrastructure/http/login-controller.ts` oversetter HTTP til use-case input/output.

## Vanlige feil

- Anemisk domene med all logikk i controller/service.
- Use-cases som bygger SQL eller kjenner ORM-detaljer.
- Lagdeling på papiret, men importretning brytes i praksis.
- For mange abstraheringer før behov er bevist.

## Viktig realitet

Clean Architecture er ikke:

- lag for lag for lag uten behov
- enterprise patterns for sin egen del
- overdreven abstraksjon

Clean Architecture er:

- avhengighetskontroll som beskytter forretningsreglene.

## Endringslogg

- 2026-02-24: Opprettet
- 2026-02-24: Utvidet med pragmatisk lagmodell, ansvarsfordeling, teststrategi og AI-guardrails mot overengineering
- 2026-02-26: Justert med aggregate boundary-regel, tydeligere transaksjonspolicy og CQRS-light-presisering
- 2026-02-26: Lagt til Related skills for symmetrisk kryssnavigasjon
- 2026-02-26: Lagt til Terminologi (standard) for konsistent språk på tvers av skills
