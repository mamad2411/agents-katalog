---
name: brukerdialog-bff-auth
description: Preset for oppgaver som legger til eller endrer autentisering/token-utveksling i Next.js API-routes (BFF) mot backend eller andre Nav-tjenester
license: MIT
compatibility: Next.js API routes/route handlers med @navikt/oasis, Wonderwall-sidecar, ID-porten/Azure AD/TokenX
metadata:
  domain: frontend-bff
  tags: nextjs bff auth oasis tokenx obo wonderwall planlegger-preset
---

# BFF-auth preset

Brukes av `planlegger` når en oppgave gjelder autentisering eller token-utveksling i en
Next.js BFF (API-routes/route handlers) — ikke UI-komponenter (se `brukerdialog-frontend-aksel`
for det), og ikke backend-siden av TokenX/Azure AD (Kotlin/Ktor-siden dekkes av
`brukerdialog-kotlin-ktor` + den personlige `tokenx-auth`-skillen).

## Trigger

Oppgaven nevner **noe av**:
- Validering av innkommende token i en Next.js API-route/route handler.
- Token-utveksling (OBO/TokenX) for å kalle en annen Nav-tjeneste fra BFF-en.
- `@navikt/oasis`, `getToken`, `validateAzureToken`, `validateIdportenToken`, `requestOboToken`.
- Wonderwall-sidecar, `accessPolicy` for en Next.js-app.

## Default sti

- **Enkel**: legge til én ny beskyttet route som følger et allerede etablert
  token-valideringsmønster i samme kodebase (samme audience-type, samme feilhåndtering).
- **Komplisert, `Krever planreview=ja`**: ny nedstrøms-tjeneste/nytt audience som ikke
  finnes fra før, endring av hvilken token-type som valideres (ID-porten ↔ Azure AD),
  eller endringer i `accessPolicy` i Nais-manifestet (se også `brukerdialog-nais-deploy`).

## Obligatoriske brief-felt (i tillegg til standardfeltene)

Når dette presetet trigges, skal `KODER_BRIEF` alltid inneholde:

- **Token-kilde**: hvilken innkommende token valideres (ID-porten for innbygger, Azure AD
  for saksbehandler), og at den hentes via `getToken(request)` fra `@navikt/oasis` — ikke
  manuell header-parsing.
- **Målsystem og audience-format**: eksakt streng/mønster som skal brukes i
  `requestOboToken(...)`. TokenX-audience er `cluster:namespace:app-name`, Azure AD
  OBO-audience er `api://cluster.namespace.app-name/.default` — disse skal **aldri**
  forveksles.
- **Feilhåndtering per steg**: manglende/ugyldig innkommende token → `401`;
  token-validering eller -utveksling feiler → `403`. Ingen av disse skal returnere `500`
  eller eksponere valideringsdetaljer/token-verdier i responsen.
- **Nedstrøms-kall**: om kallet til target-tjenesten skjer over vanlig `http://` internt i
  klyngen (Nais-konvensjon for intern trafikk) eller `https://` (ekstern tjeneste).

## Sjekkliste for koder

- [ ] `getToken`/`validateAzureToken`/`validateIdportenToken` fra `@navikt/oasis` brukt i
      stedet for manuell JWT-dekoding.
- [ ] Riktig audience-format brukt for target-systemet (TokenX vs. Azure AD OBO er ulike
      formater, se over) — ikke gjett, sjekk mot `accessPolicy` i Nais-manifestet.
- [ ] `401` ved manglende/ugyldig innkommende token, `403` ved feilet
      validering/token-utveksling — ikke `500`, og responsen inneholder ikke
      valideringsfeilmelding eller selve token-verdien.
- [ ] Ingen egen token-cache lagt til — `@navikt/oasis` cacher OBO-tokens automatisk.
- [ ] Token logges aldri, verken innkommende eller utvekslet (se `brukerdialog-persondata`).
- [ ] Hvis ny nedstrøms-tjeneste: `accessPolicy.outbound` i `.nais/nais*.yaml` er oppdatert
      til å matche (rut til `brukerdialog-nais-deploy` hvis dette er del av scope).

## Ikke gjør

- Ikke bygg egen JWT-validering/dekoding manuelt når `@navikt/oasis` allerede dekker det.
- Ikke bland audience-format mellom TokenX (`cluster:ns:app`) og Azure AD OBO
  (`api://cluster.ns.app/.default`).
- Ikke send det innkommende eller utvekslede tokenet videre til klienten — BFF-en er
  siste stopp for tokenet server-side.
- Ikke anta hvilken tokentype som er riktig (ID-porten vs. Azure AD) — det avgjøres av
  hvem som kaller (innbygger vs. saksbehandler), se auth-beslutningstreet i `nav-plan`.
