+++
date = "2016-08-01"
title = "MONCSKILL (Data: races.lst)"
original_url = "list/data/races.html#moncskill"
categories = [ "all-tag", "races-tag" ]
+++

## Status

None

## Syntax

`MONCSKILL:x|x`

## Parameters

-   x: Text (Skill Name)
-   x: TYPE.Text (Skill Type)



<span id="moncskill"></span> \*\*\* New 5.4

What it does
------------

-   Grants the listed skills as monster class skills.
-   The replacement/substitution symbol (%) may be used at the end of
    the skill name.
-   Monster class skills are only class skills for monster classes such
    as Giant, Outsider, Undead etc.
-   If a monster takes levels in a base class only those skills defined
    as class skills in that class count as class skills for that level,
    the monster class skills will not apply.
-   **.MOD Behavior:** When modifying a race with the `.MOD` tag, given
    an existing `MONCSKILL` tag, the data included in a new `MONCSKILL`
    tag will be appended to the existing tag data.

Examples
--------

`MONCSKILL:Alchemy|Wilderness Lore`

The "Alchemy" and "Wilderness Lore" skills are made monster class
skills.

`MONCSKILL:Alchemy|TYPE.Knowledge`

The "Alchemy" and "Knowledge" type skills are made monster class skills.

**.MOD Example:**

Initial Race: `Ooze Monkey <tab> MONCSKILL:Alchemy|Wilderness Lore`

Modified By: `Ooze Monkey.MOD <tab> MONCSKILL:Acrobatics|Stealth`

Is Equivalent To:
`Ooze Monkey <tab> MONCSKILL:Acrobatics|Alchemy|Stealth|Wilderness Lore`
.

The "Acrobatics", "Alchemy", "Stealth", and "Wilderness Lore" skills are
made monster class skills.

