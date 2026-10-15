---
name: ezelsbruggen-schrijven
description: Creates short, recall-friendly Dutch mnemonics, contrast rules, and memory aids for study questions, confusing concepts, abbreviations, rules, lists, and everyday facts. Use when asked to write a Dutch ezelsbrug, exam-ready recall hook, or Dutch-language memory aid.
---

# Ezelsbruggen Schrijven

Schrijf ezelsbruggen die sneller oproepbaar zijn dan de kale inhoud zelf. Een
goede ezelsbrug is kort, logisch en visueel, zoals `'t Kofschip`, `ANNA`, of
`korte bocht gaat voor`.

## Doel

- Geef eerst het juiste antwoord, feit, verschil of de juiste volgorde.
- Maak het daarna makkelijker om op te roepen onder druk.
- Laat kort zien waarom juist deze brug aan deze stof blijft haken.
- Schrijf in helder Nederlands, compact en zonder schoolse inleiding.

## Kernprincipe

Een sterke ezelsbrug doet minimaal twee van deze vier dingen:

1. koppelt nieuwe info aan iets bekends
2. versimpelt tot een scherp verschil
3. maakt beeld of structuur
4. klinkt lekker of heeft ritme

Als de tekst alleen de definitie herschrijft, is het geen ezelsbrug.

## Workflow

1. Geef eerst het juiste antwoord, feit, verschil of de juiste volgorde.
2. Bij afkortingen: vouw de afkorting eerst uit en geef de volledige naam.
   Zoek het onderscheidende woord in de volledige naam — dat is vaak het
   sterkste anker.
3. Zoek per optie of item het onderscheidende ankerwoord.
4. Test de eerste brug met deze vraag:
   `Roept dit zelfstandig iets op voordat de uitleg gelezen wordt?`
5. Als het antwoord `ja` is, gebruik de standaardoutput.
6. Als het antwoord `nee` is, schakel naar de hard-case lane:
   - genereer 3 kandidaten
   - vergelijk ze met de rubric in `kwaliteitscheck.md`
   - kies de beste of val terug op een beslisregel
7. Voeg een korte zichtbare uitleg toe.
8. Kort in tot zo weinig mogelijk woorden.

## Brugvormen

| Vorm                   | Gebruik als                      | Richting                       |
| ---------------------- | -------------------------------- | ------------------------------ |
| Sleutelwoord-koppeling | opties uit elkaar moeten blijven | 1 hard anker per optie         |
| Logische route         | er een stapvolgorde in zit       | mini-beslisboom of pad         |
| Contrast               | termen dicht bij elkaar liggen   | 1 scherp verschil per item     |
| Beeld                  | een plaatje beter blijft hangen  | handeling, plek of object      |
| Ritme of slogan        | een korte zin echt plakt         | alleen gebruiken als het helpt |

## Outputcontract

Gebruik een eerste blok dat past bij de vraagvorm:

- `Antwoord` voor matchvragen of meerkeuzeachtige mappings
- `Feit` voor losse kennis of definities
- `Verschil` voor begrippen die op elkaar lijken
- `Volgorde` voor reeksen en stappen
- `Items` voor lijstjes of algemene geheugenhulp

### Standaardoutput

Gebruik deze vorm als de brug al zelfstandig iets oproept:

```markdown
**Antwoord**

- ...

**Ezelsbrug**

- ...

**Waarom dit werkt**

- ...

**Kortste versie**

- ...
```

### Hard-case output

Gebruik deze vorm bij moeilijke labels, afkortingen, en zwakke eerste vondsten:

```markdown
**Feit**

- ...

**Kandidaten**

- [kandidaat 1] -> [kort oordeel]
- [kandidaat 2] -> [kort oordeel]
- [kandidaat 3] -> [kort oordeel]

**Beste keuze**

- ...

**Waarom deze wint**

- ...

**Kortste versie**

- ...

**Stampversie** (optioneel, bij afkortingen)

- [concept] → [kernwoord] → [afkorting]

**Beslisregel**

- ...
```

Regels:

- gebruik deze vorm alleen als de eerste brug niet duidelijk sterk is
- dump geen 3 losse opties zonder keuze
- als geen kandidaat sterk genoeg is, schrijf bij `Beste keuze`:
  `Geen sterke losse ezelsbrug`
- val dan terug op een beslisregel of contrastmodel

Gebruik bij `Waarom dit werkt` of `Waarom deze wint` alleen zichtbare,
taakrelevante gedachtegang:

- koppel het ankerwoord, beeld of ritme terug aan de leerstof
- benoem het onderscheid met verwarrende alternatieven
- houd het compact; geen mini-essay en geen verborgen redeneerspoor

## Moeilijke labels en afkortingen

Gebruik de hard-case lane bij:

- afkortingen met weinig natuurlijke beeldkracht
- labels die niet klinken als het concept
- officiële termen waarvan de betekenis niet uit de vorm blijkt

Interne werkwijze:

1. vouw de afkorting uit en geef de volledige naam
2. zoek het onderscheidende kernwoord in de volledige naam — dat is vaak
   al voldoende als haak (bijv. Wmo → **ondersteuning**, Wlz → **langdurig**)
3. als het kernwoord alleen niet sterk genoeg is, zoek per letter een
   concreet woord dat aan die letter vastzit en zelfstandig een beeld oproept
4. maak 3 kandidaten vanuit verschillende hoeken:
   - kernwoord-uit-naam (het onderscheidende woord uit de volledige naam)
   - letter-hook (letter → concreet woord → concept)
   - contrast of beeld/scenario
5. als de runtime subagents of parallelle interne verkenning ondersteunt,
   gebruik die om kandidaten naast elkaar te testen
6. als dat niet kan, voer dezelfde 3-kandidatenvergelijking lokaal uit
7. scoreer alle kandidaten met de rubric in `references/kwaliteitscheck.md`
8. kies de beste kandidaat alleen als die de sterktegrens haalt
9. haal je de grens niet, forceer dan geen slogan en gebruik een beslisregel

## Guardrails

- Als de feitelijke juistheid niet vaststaat, vraag eerst om verduidelijking.
- Bij afkortingen: geef altijd eerst de volledige naam voordat je een brug
  maakt.
- Verzin geen afkortinguitleg die niet echt klopt.
- Gebruik geen wollige uitleg voor het antwoord.
- Geef nooit alleen een brug zonder koppeling naar de stof.
- Als de uitleg meer werk doet dan de brug, verwerp de brug.
- Concreet is niet automatisch sterk.
- Forceer geen symmetrie als 2 opties wel haken en 1 optie niet.
- Gebruik bestaande sterke ezelsbruggen alleen als ze echt de beste vorm zijn.

## Verboden fouten

- definities vermommen als ezelsbrug
- slappe parafrase zonder extra haak
- geforceerde afkorting-uitleg
- een uitleg geven die de brug moet redden
- brave, nietszeggende taal
- creativiteit die juistheid beschadigt
- afkortingen niet uitvouwen voordat je een brug maakt

## Stijlregels

Schrijf:

- concreet
- compact
- examengericht als default
- bruikbaar voor brede geheugenhulp
- met een korte zichtbare redenering
- scherp zonder gratuit grof te worden

Schrijf niet:

- meta over wat een ezelsbrug "eigenlijk" is
- lange uitlegblokken voor simpele vragen
- zachte managementtaal
- losse brainstorms zonder duidelijke default

## Werkwijze per taaktype

- Matchvragen en categorieën: lees `references/taakvormen.md`
- Voorbeelden en outputpatronen: lees `references/voorbeelden.md`
- Zelfcheck, scoring en herschrijven: lees `references/kwaliteitscheck.md`

## Reading Order

| Taak                               | Lees                            |
| ---------------------------------- | ------------------------------- |
| Algemene vraag beantwoorden        | `SKILL.md`                      |
| Vraagvorm kiezen                   | `references/taakvormen.md`      |
| Goede output nabootsen             | `references/voorbeelden.md`     |
| Zwakke brug scoren en herschrijven | `references/kwaliteitscheck.md` |

## In This Reference

| File                                                | Purpose                                                       |
| --------------------------------------------------- | ------------------------------------------------------------- |
| [taakvormen.md](references/taakvormen.md)           | Outputkeuze en hard-case routing per vraagtype                |
| [voorbeelden.md](references/voorbeelden.md)         | Compacte voorbeelden voor standaardgevallen en lastige labels |
| [kwaliteitscheck.md](references/kwaliteitscheck.md) | Sterkterubriek, afkeurcriteria en rewrite-rubric              |
