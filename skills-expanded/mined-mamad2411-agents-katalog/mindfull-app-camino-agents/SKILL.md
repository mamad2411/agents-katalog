# AGENTS.md

**Lees eerst [CLAUDE.md](CLAUDE.md). Dat is het volledige contract voor dit project en het geldt voor jou net zo goed.**

Wij werken met **Claude Code**, en die laadt `CLAUDE.md` zelf. Dit bestand is er voor het geval iemand een tool gebruikt die dat niet doet, zoals Cursor of Codex: die lezen `AGENTS.md` en zouden zonder dit bestand zonder enige projectafspraak beginnen. Het staat er dus als vangnet, niet omdat we die tools nodig hebben.

Dit is dus geen tweede regelset. Bij twijfel of tegenspraak wint `CLAUDE.md`.

---

## Stand van zaken

**De app draait, maar er staat nog geen enkel scherm in.** `apps/mobile` is gescaffold (Expo SDK 57, expo-router) en `npm run typecheck`, `npm run lint` en `npm test` zijn groen. De tokens staan in `packages/ui/tokens`, de componenten in `packages/ui/components` nog niet. De twintig routebestanden van de userflow staan er leeg, met per stuk een verwijzing naar hun specificatie.

Sinds 20 augustus 2026 staat de contentbibliotheek van Mind in `content/mind/`: 339 pagina's naslag om in te zoeken. Let op: dat is **nog geen goedgekeurde contentbron voor de app**, zie `content/mind/LEESMIJ.md` voordat je er iets uit overneemt.

Wat nog moet: het concept in `docs/scope.md` bevestigen en de resterende TODO's daar beslissen, door het team en niet door een agent. Zie `CLAUDE.md` sectie 0. Word je gevraagd een productbeslissing te nemen die daar had moeten staan, meld dat dan in plaats van hem zelf te nemen.

---

## De regels die je in geen geval mag missen

Ook als je verder niets leest:

1. **Log nooit inhoudelijke gebruikersinvoer.** Niet naar de console, niet naar een crash reporter, niet naar analytics, ook niet tijdelijk om te debuggen. Dit is een app over mentale gezondheid.
2. **Push nooit naar `main`.** Werk op een branch, ga via een pull request. `main` is technisch beschermd.
3. **Voeg geen dependency toe.** Vraag ernaar.
4. **Geen hardcoded kleuren, spacing, radii, font sizes of shadows.** Altijd via de tokens uit `packages/ui/tokens`.
5. **Raak geen gedeelde bestanden aan** buiten de scope van je taak. De lijst staat in `CLAUDE.md` sectie 5.
6. **Verzin geen tabel, veld, analytics-event of hulptekst.** Staat het niet in `docs/datamodel.md` of `docs/scope.md`, dan bestaat het niet en vraag je ernaar.
7. **Zet geen afbeelding in Supabase Storage die in de app bundle hoort.** Iconen, illustraties en gradients horen in de bundle, alleen content die Mind zelf toevoegt gaat naar Storage. Zie `docs/assets-en-media.md`.
8. **Tel check-ins nooit op de collectieve tabel.** Die heeft geen gebruikerscode, dus dat kan niet, en een poging daartoe breekt de anonimisering. De teller hoort in de persoonlijke stroom. Zie `docs/limieten-en-misbruik.md`.

## Media en caching, kort

Vier regels die egress en laadtijd bepalen. De onderbouwing en de cijfers staan in `docs/assets-en-media.md`.

- **Comprimeer en schaal vooraf**, nooit tijdens het opvragen. Image transformations bestaan niet op ons plan en de grootste winst zit in de afmeting, niet in het formaat.
- **Public bucket, geen signed URLs** voor content die niet per gebruiker afgeschermd hoeft te worden. Elk token in een signed URL is een eigen cache-entry, dus daarmee wordt de cache nooit warm en gaat elke aanvraag naar de origin.
- **Zet `cacheControl` hoog bij upload.** De standaard is één uur, en dat is te laag voor content die zelden wijzigt.
- **Wijzigt een afbeelding, upload naar een nieuw pad.** Overschrijven werkt niet betrouwbaar, want browsers verversen hun eigen cache niet als de CDN invalideert.

Melden dat iets niet kan binnen deze grenzen is een geldig eindresultaat. Een taak half afmaken zonder het te melden is dat niet.

## Eigenaarschap is geen schrijfrecht

In `docs/taakverdeling.md` staat per gebied één eindverantwoordelijke. Dat betekent dat die persoon reviewt en de knopen doorhakt.

Het betekent **niet** dat alleen die persoon daar mag werken, en het betekent niet dat een wijziging van iemand anders geweigerd hoort te worden. We hebben daarom bewust geen verplichte Code Owner-review op de repo staan, zie `docs/setup-github.md`. Iedereen mag overal aan werken, met één review als kwaliteitscheck.

## Waar je de rest vindt

| Vraag | Document |
|---|---|
| Wat bouwen we wel en niet | `docs/scope.md` |
| Hoe de app zich hoort te gedragen | `docs/productprincipes.md` |
| Afspraken rond design: tokens, schermregels, assets, Figma | `docs/design-system.md` |
| Een concrete kleur, maat, component of schermopbouw | `packages/ui/README.md`, of `.claude/skills/mind-design/SKILL.md` |
| Iets opzoeken in de content van Mind: challenges, gidsen, zelftests, ervaringsverhalen | `content/mind/LEESMIJ.md`, of `.claude/skills/mind-content/SKILL.md` |
| Wat er moet gebeuren om het ontwerp in React Native te krijgen | `docs/van-ontwerp-naar-app.md` |
| Welke data we opslaan en hoe lang | `docs/datamodel.md` |
| Hoe de backend in elkaar zit en hoe je er iets aan wijzigt | `docs/backend-draaiboek.md` |
| Waar plaatjes horen, compressie en caching | `docs/assets-en-media.md` |
| Rate limits en misbruik | `docs/limieten-en-misbruik.md` |
| Wat met Mind is afgesproken over privacy | `docs/privacy-besluiten.md` |
| Wie waar eigenaar van is | `docs/taakverdeling.md` |
| De git-workflow | `.claude/skills/werkwijze/SKILL.md` |

## Voor je klaar bent

Rapporteer welke bestanden je hebt aangepast en welke aannames je hebt gedaan. Draai `npm run typecheck`, `npm run lint` en `npm test` als die er zijn. De volledige definition of done staat in `CLAUDE.md` sectie 7.
