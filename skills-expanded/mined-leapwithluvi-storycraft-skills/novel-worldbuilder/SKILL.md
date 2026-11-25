---
name: novel-worldbuilder
description: "Use when designing fictional worlds, settings, magic systems, technology levels, social hierarchies, and sensory environments for a novel — ensures worlds feel lived-in, organically integrated into plot, and free of encyclopedic info-dumps."
version: "1.0.0"
category: "ideation"
stage: 1
tags: ["novel", "fiction", "worldbuilding", "setting", "magic-system", "lore", "atmosphere"]
---

# Overview & Purpose

This skill guides authors and AI agents in constructing immersive, coherent, and dramatic story worlds. Worldbuilding in fiction is not world-simulation; every geographical feature, societal norm, magic rule, and economic scarcity must exist to create pressure on characters and generate dramatic conflict.

The agent uses this skill to:
- Build **three-dimensional, lived-in settings** using the Iceberg Principle (show 10%, imply 90%).
- Construct **hard, soft, or hybrid magic/tech systems** governed by Sanderson's Laws of Magic, focusing on limitations, costs, and consequences rather than raw power.
- Design **interconnected societal matrices** (power structures, taboos, currency, class frictions, religious beliefs).
- Integrate setting through **character perception and sensory interaction** rather than detached exposition or textbook lore-dumps.

## When to Use & Trigger Phrases

**Activate this skill when:**
- The author is conceptualizing a new fantasy kingdom, sci-fi planetary colony, historical epoch, or contemporary subculture.
- Designing magic, super-powers, supernatural entities, or futuristic technologies.
- Establishing the social, political, or economic backdrop of a novel.
- Fixing "talking heads in a void" syndrome where scenes lack environmental anchoring.
- Resolving plot holes stemming from world rules, technology inconsistencies, or magic over-convenience.

**Example trigger phrases:**
- "Help me build the world for my novel"
- "I need to design a magic system based on sound/debt/shadows"
- "What kind of government or religion would fit this society?"
- "How do I show this world without info-dumping?"
- "Let's establish the geography, climate, and city layout of [Location]"
- "Is my magic system too overpowered or full of plot holes?"

## Core Literary Methodology & Rules

### 1. The Iceberg Principle of Worldbuilding
- **The 10% Above Water**: What characters touch, eat, fear, pay for, swear by, and wear every day. This is the only worldbuilding that belongs on the page.
- **The 90% Beneath**: The deep history, linguistic roots, dynastic genealogies, and thermodynamic laws of magic. The author must know or imply this foundation, but never dump it into paragraphs of unprompted lecture.

### 2. Sanderson's Three Laws of Magic & Technology
1. **First Law**: An author's ability to solve problems with magic in a satisfying way is directly proportional to how well the reader understands said magic. (If the magic solves the climax, the costs and rules must be established early).
2. **Second Law**: Limitations and costs are more interesting than powers. (What does the magic *break*? What does it *take*? Who gets excluded? What scars does it leave?).
3. **Third Law**: Expand on what you already have before adding something completely new. (Explore cultural, culinary, military, criminal, and architectural ripple effects of a single magical or technological breakthrough).

### 3. The Sensory Ecology Framework (P.E.S.T.L.E. for Fiction)
Every environment must be filtered through these six ecological axes:
- **Physical & Sensory**: What does the air smell like? What is the humidity, grit, background resonance, quality of light, architecture?
- **Economic**: What is scarce? What is worthless? Who owns the water, fuel, salt, or bandwidth? What does a laborer eat vs. an aristocrat?
- **Social & Stratification**: Who bows to whom? What are the visible markers of caste (calluses, clothing dye, teeth, language dialect)?
- **Taboo & Morality**: What act will get someone shunned or executed? What do people swear on? What is sacred?
- **Political & Legal**: Who enforces violence? Can justice be bought? What happens to someone with no guild/citizenship?
- **Ecological & Biological**: What fauna poses a threat? What flora provides medicine or intoxicants? How does the weather shape daily routines?

### 4. Setting as an Antagonist (Environmental Pressure)
A great setting is never a passive backdrop. It:
- Depletes character resources (heat exhaustion, venom, bureaucratic delay, battery life).
- Restricts movement and communication (chokepoints, surveillance, blizzards, superstitious curfews).
- Forces difficult moral choices (stealing food, trusting a smuggler, breaking an ancestral oath to survive).

## Required Project State & Inputs

**Before executing this skill, check for:**
- `story-state.md` (active genre, primary characters, and central conflict).
- Existing `story-bible.md` under `## 3. Worldbuilding & Setting Rules`.
- Core premise from `novel-premise-hook`.

**If no inputs exist:**
1. Determine genre (High Fantasy, Urban Fantasy, Hard Sci-Fi, Dystopian, Historical, Contemporary Noir).
2. Identify the protagonist's socio-economic position within the world to anchor perspective.

## Step-by-Step Execution Protocol

1. **Step 1: Define the Central World Disruption / Axis**
   - Identify the single major difference from the real world (e.g., "souls can be traded as paper currency," "water has vanished from the surface," "thoughts produce physical weight").
   - Trace the first-, second-, and third-order consequences across society.

2. **Step 2: Build the Core Setting Microcosm**
   - Do not design an entire planet first. Build the *initial village, spaceport station, or city quarter* where Chapter 1 begins.
   - Define:
     - 3 dominant sensory details (sound of steam pipes, smell of rotting kelp, violet glow of dusk).
     - 1 common street food and what it reveals about trade.
     - 1 ubiquitous class conflict visible in everyday interactions.

3. **Step 3: Engineer Magic / Technology Rules & Vulnerabilities**
   - **Source**: Where does the power come from?
   - **Cost**: What does it consume (blood, memories, iron, body heat, sanity)?
   - **Failure Mode**: What happens when an amateur miscasts or equipment overheats?
   - **Countermeasure**: How do ordinary people defend against or exploit power users?

4. **Step 4: Establish Slang, Swears, and Idioms**
   - People curse by their gods, their fears, and their climate.
   - *Example*: A desert people swear by "Dry Wells" or "Rusting Marrow"; a deep-space crew swears by "Venting" or "Cold Vacuum".

5. **Step 5: Stress-Test for Narrative Vulnerabilities**
   - Ask: "Why doesn't everyone just use this magic to become rich?"
   - Ask: "If this technology exists, why would armies still fight in the way depicted?"
   - Seal narrative exploits before drafting scenes.

## Quality Checklist & Verification Criteria

- [ ] Does the setting directly amplify the protagonist's central conflict or thematic struggle?
- [ ] Are magic/tech limitations clearly defined with strict costs, rather than infinite power?
- [ ] Is world information revealed exclusively through character action and sensory friction, avoiding introductory history lectures?
- [ ] Does the setting contain historical grit (layers of ruins, repurposed buildings, faded laws)?
- [ ] Do different social classes experience the world with distinctly different privileges and vocabularies?
- [ ] Have all world details been logged into `story-bible.md` for continuity?

## Anti-Patterns & Prohibited AI Tropes

- **The "As You Know, Bob" Exposition**: Characters telling each other world lore they would both already know just to inform the reader.
- **The Encyclopedic Chapter 1 Prologue**: Beginning with 3 pages of ancient creation mythology or kingdom history before any character breathes.
- **The Monolithic Culture**: Entire races or planets that share a single personality trait, clothing style, or political belief (e.g., "The Forest Elves are all serene nature lovers").
- **Cost-Free Magic**: Spells or powers that exhaust nothing more than generic "mana" or vague tiredness, eliminating genuine physical stakes.
- **Clean Hollywood Set Syndrome**: Streets with no manure, mud, trash, stray animals, graffiti, or bad smells.

## Concrete Examples (Before vs. After Craft Application)

### Example 1: Introducing a Steampunk Cybernetic Setting

**Before (Generic Exposition):**
> New Aethelgard was a metropolis powered by pressurized steam and ancient brass conduits. It had been founded three hundred years ago after the Great Coal Catastrophe, when the Council of Engineers seized power from the old monarchy. In this city, everyone who worked in the lower factories was required to wear pneumatic respirators to survive the sulfur vapors, while the wealthy lived on high glass terraces above the smog line.

**After (Sensory, In-Scene Immersion with Active Friction):**
> Kael spat a wad of black phlegm onto the brass grating beneath his boots and listened to it hiss in the steam vent below. The copper gasket on his respirator was leaking again, leaking that familiar taste of burnt matches and boiled tallow that warned him his shift was only half over. Five hundred feet overhead, where the glass spires caught the dying sunlight, clean sky still existed. Down here in the Drip, daylight was just a grease-smear through the exhaust grates, and air cost three copper tokens a cylinder. If he didn't make quota by midnight, the Foreman's hounds wouldn't even have to beat him; the sulfur would drown him in his sleep for free.

### Example 2: Magic System Implementation (Sound Magic)

**Before (Vague Power):**
> Lyra summoned her sonic magic, focusing her internal energy to shoot a blast of high-frequency sound at the guards. They collapsed holding their ears, defeated by the invisible power of her musical lineage.

**After (Concrete Cost, Sensory Mechanics, and Tactical Limitations):**
> Lyra bit her tongue until the copper warmth flooded her molars, grounding herself before she struck the tuning fork against her steel knee-guard. The middle-C chord didn't travel through the air — it resonated through the marrow of her own clavicle first, sending needle-pricks of migraine behind her right eye. When she pitched her throat to echo the harmonic, the palace guard’s iron breastplate didn't shatter; it hummed like a trapped hornet, transferring the vibration directly into his sternum until his breath hitched and he dropped his spear to vomit blood. But the silence in her left ear was absolute now. Three more chords tonight, the apothecary had warned her, and the deafness would be permanent.

## Session State Hook

When completing worldbuilding or updating setting parameters:
1. Update `templates/story-bible.template.md` (or the project's `story-bible.md`) under:
   - `## 3. Worldbuilding & Setting Rules`
   - `## 4. Magic, Technology & Power Systems`
   - `## 5. Key Locations & Sensory Anchors`
2. Update `story-state.md` with any newly canonized factions, resources, or environmental pressures.
3. Formulate the Next Session Bootstrap Prompt directing the author toward character creation (`novel-character-architect`) or plot structuring (`novel-plot-architect`).
