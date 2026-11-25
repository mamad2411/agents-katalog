# orchestrator-master Skill

De daadwerkelijk loadable skill staat in:

```text
skills/orchestrator-master/SKILL.md
```

Daar staat YAML-frontmatter op bestandsniveau, zodat Pi de metadata kan parsen en de skill automatisch kan ontdekken. Dit document is alleen de ontwerp- en onderhoudsnotitie; kopieer geen fenced YAML uit documentatie naar de runtime.

## Doel

De skill geeft Pi compacte operationele regels voor:

- kiezen tussen single, parallel, crew en swarm;
- thinking-level selectie;
- conflictvrije schrijfpartitionering;
- quota- en circuit-breakerbewust uitvoeren;
- reproduceerbare handoffs;
- evalueren en herplannen na iedere wave.

## Ontwerpregels

- Houd de skill kleiner dan de volledige architectuurdocumentatie.
- Verwijs voor live status altijd naar runtime-tools.
- Beschrijf toekomstige v2-paden niet alsof ze al bestaan.
- Gebruik progressive disclosure: tool schema → skill → gerichte repositorydocs.
- Vraag geen menselijke keuze wanneer topology of thinking level rechtstreeks uit de taak volgt.

## Validatie

1. Start Pi vanuit de repositoryroot.
2. Herlaad de extensie en skillregistry.
3. Controleer dat `orchestrator-master` als skill wordt ontdekt.
4. Test een eenvoudige taak: de skill moet single-agent uitvoering adviseren.
5. Test een complexe taak met onafhankelijke lanes: de skill moet partitionering, limits en acceptatiebewijs opnemen.
6. Test een partial failure: de skill moet gericht herplannen en niet blind extra agents spawnen.

## Onderhoud

Wijzig operationele beslisregels in `skills/orchestrator-master/SKILL.md`. Werk dit document alleen bij wanneer discovery, architectuur of validatieproces verandert.
