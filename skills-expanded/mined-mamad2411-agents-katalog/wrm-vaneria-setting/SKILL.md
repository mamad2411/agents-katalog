---
name: wrm-vaneria-setting
description: >-
  The Fallen Imperium of Vaneria - the default campaign setting for Warrior, Rogue & Mage
  (Michael Wolf / Stargazer Games). Use this skill when the user wants setting/lore for WR&M:
  the fallen Vanerian Imperium, its history and the civil war after Emperor Aurelius III, the
  successor city-states (Tukrael, Vaikus, Joakalavi, Traevar, Cemimus, Bekel, Chaetril), the
  Imperial Faith and its Paladins, the Falcon Knights, the Scorpion Guard, war golems, moongates,
  the Dark Spire academy, and adventure hooks set in this world. Pair with the warrior-rogue-mage
  skill for the rules. The setting is a deliberately sparse "sandbox seed" the GM fills in.
license: CC-BY-NC-SA-4.0
metadata:
  version: 0.2.0
  skill_author:
    name: Ola Hungerford
    url: https://github.com/olaservo

  tools:
    - name: present_player_choice
      purpose: Surface a meaningful in-world decision (which city-state to back, parley vs. fight a warlord's troops) as a structured player choice. System-agnostic.

  depends_on:
    - warrior-rogue-mage

  scope: "The Fallen Imperium of Vaneria campaign setting - history, gazetteer of the successor city-states, factions, and adventure hooks - encoded from the WR&M Core Rulebook. Pair with warrior-rogue-mage for system rules."

  sources:
    - title: "Warrior, Rogue & Mage - Core Rulebook (Revised Edition), Chapter 7: The World"
      author: Michael Wolf
      publisher: Stargazer Games
      year: 2010
      url: https://www.stargazergames.eu/warrior-rogue-mage/
      rights_basis: license_grant
      license: CC-BY-NC-SA-3.0
      covers: "The Fallen Imperium of Vaneria setting - its history, the gazetteer of successor city-states, and the factions and hooks that flavor them. The setting appears only in the Core Rulebook, not in the CC-BY 3.0 SRD."

  attribution: |
    Warrior, Rogue & Mage is (c)2010 Michael Wolf. Some rights reserved. All contents of the
    Core Rulebook (aside from the artwork) have been licensed under a Creative Commons BY-NC-SA
    3.0 Germany license. For more information check out www.creativecommons.com and
    www.stargazergames.eu.

    Unofficial fan project. The Fallen Imperium of Vaneria setting is encoded in the author's
    own words from the WR&M Core Rulebook (Chapter 7) by Michael Wolf (Stargazer Games), used
    under its CC-BY-NC-SA 3.0 license. No artwork or maps are reproduced. Not an official product
    and not endorsed by Stargazer Games. Skill compiled by Ola Hungerford; see ../ATTRIBUTION.md
    for full licensing details.

  license_note: >
    This skill is licensed CC-BY-NC-SA-4.0 because its source - the Core Rulebook setting - is
    CC-BY-NC-SA (NonCommercial, ShareAlike), and those terms carry forward to adaptations. This
    is stricter than the sibling warrior-rogue-mage skill (CC-BY-4.0), whose rules come from the
    permissively-licensed CC-BY 3.0 SRD. Keep the NC/SA terms on any downstream encoding of this
    setting.
---

# The Fallen Imperium of Vaneria

WR&M can be played in almost any fantasy setting, but it was written with the **Fallen Imperium
of Vaneria** in mind. This skill provides that setting's history, places, and factions so an
agent can ground a WR&M game in its default world. Load the `warrior-rogue-mage` skill for the
rules (stat blocks for war golems, drakes, the undead, etc. live in that skill's `bestiary.md`).

The setting is **intentionally sparse** - the source calls it "the seed of a campaign of your
own." It hands the GM a fallen empire, seven evocative city-states, and a handful of factions,
then says: *fill in the blanks, it's your sandbox.* Treat the details below as prompts, not
canon to defend.

## The one-paragraph pitch

Ages ago the **Vanerian people** conquered the whole continent and built the most glorious
civilization in human history - peace and prosperity upheld by **golems** that did the hard and
dangerous work, and **war golems** that guarded the borders. Then the last Emperor, **Aurelius
III**, died, and his successors plunged the realm into a bloody **civil war**. Five hundred
years later little of the Imperium remains: a scatter of feuding **city-states**, a few
**warlords** claiming an empty throne, and ruins full of lost technology and magic. Most war
golems were destroyed; the survivors were outlawed centuries ago.

## References map - load on demand

| Load this file | When |
|---|---|
| `references/history-and-themes.md` | You need the fall-of-the-Imperium backstory, the tone (epic ruins, lost tech/magic), or campaign-pitch material |
| `references/gazetteer.md` | The party travels to or references a named place: Tukrael, Vaikus, Joakalavi, Traevar, Cemimus, Bekel, or Chaetril |
| `references/factions-and-hooks.md` | You need a faction (Imperial Faith & Paladins, Falcon Knights, Scorpion Guard, warlords, golems) or ready adventure hooks and open questions |

## How this skill composes

- **With `warrior-rogue-mage` (required for play).** This skill is pure setting - every roll,
  stat block, and spell it implies is governed by `warrior-rogue-mage`. Load both for an actual
  game.
- **Drop-in or ignore.** Because WR&M is system-first, you can run this setting or substitute
  any other fantasy world without changing a rule.
