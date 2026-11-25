---
name: localization-manager
description: Localization setup en review - String Catalogs, pluralization, region formats. Gebruik bij nieuwe features en pre-launch.
---

# Localization Manager

## String Catalogs (iOS 17+)
Gebruik `.xcstrings` format — veel beter dan `.strings` + `Localizable.stringsdict`.

Setup:
1. File → New → File → String Catalog
2. Naam: `Localizable`
3. Click "+ Language" om languages toe te voegen
4. Xcode auto-extract: build triggert extraction uit code

## In code
```swift
// Auto-localizable
Text("Welkom")
Text("Hallo \(name)")
Text("Je hebt \(count) taken", comment: "Main screen - task count")

// Voor non-Text strings
String(localized: "error.network")
```

## Nederland-specifieke gotchas
- Datum: `d MMMM yyyy` niet `MMMM d, yyyy`
- Tijd: 24-uur (17:30) niet 12-uur (5:30 PM)
- Getal: `1.234,56` niet `1,234.56`
- Valuta: `€ 19,99` met spatie
- Telefoon: `+31 6 12345678`

Altijd gebruiken:
```swift
// Datum
Date().formatted(date: .long, time: .omitted)
// "21 april 2026" in NL, "April 21, 2026" in US

// Valuta
price.formatted(.currency(code: "EUR"))
// "€ 19,99" in NL, "€19.99" in US

// Getal
1234.56.formatted()
// "1.234,56" in NL, "1,234.56" in US
```

## Pluralization
In String Catalog, click bij key → "Vary by Plural"
Voor Nederlands: `zero`, `one`, `other` zijn meestal genoeg.


## Length variations
Sommige UI zones kort houden. Voor button labels: gebruik max 15 chars in alle locales.
String Catalog ondersteunt length variations via substitutions.

## RTL support (voor toekomst)
Gebruik `.leading`/`.trailing` niet `.left`/`.right`.
Test met Scheme → Options → Application Language → Arabic (RTL Pseudo).

## Scheme voor testing
Maak extra scheme "App-NL" en "App-PseudoLang":
- Product → Scheme → Edit Scheme
- Run → Options → Application Language
- Pseudolanguage (RTL) of specifieke taal

## Accessibility labels ook localiseren
```swift
Button("Kies") { ... }
  .accessibilityLabel("Kies een optie")
// Beide in String Catalog
```

## Context comments — verplicht
```swift
Text("Save", comment: "Button on edit screen to save changes")
```
Vertalers hebben dit nodig.

## Output
- Checklist van te localiseren strings gevonden zonder `comment:`
- Date/number/currency formatters die hardcoded zijn
- `.left`/`.right` instances (moet `.leading`/`.trailing` zijn)
- Ontbrekende pluralization rules
