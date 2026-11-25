---
name: shooting-day
version: 1.0.0
description: Plan a production day end to end — order of day, categorised shot list, equipment checklist and a WhatsApp-ready crew briefing so nobody shows up asking where the call sheet is.
author: MarcoZorn
license: MIT
tags: [agency, workflow, operations, production, video]
compatible: claude-code, codex-cli, cursor, gemini-cli, openclaw
---

# Shooting Day

## When to use this skill

**English:** "shooting", "shot list", "call sheet", "filming day", "production day", "plan the shoot".

**Italiano:** "shooting", "riprese", "giorno di ripresa", "ODG", "scaletta set", "piano riprese".

## What this skill does

Turns a shoot into a plan the whole crew can run from a phone. It produces the order of day with times and locations, a shot list categorised the way a social edit actually needs (hook, body, CTA, B-roll, audio), an equipment checklist you tick as you pack, and a crew briefing formatted to paste straight into WhatsApp. It ends the two universal set problems: "where's the shot list" and "who has the call sheet".

## Inputs required

1. **Project / client** and what you are shooting (reels, ad, brand film, product).
2. **Date, city and location(s)** — including call time and wrap target.
3. **Deliverables** — how many pieces, formats and durations come out of the day.
4. **Crew** — who is on set and their role.
5. **Talent** — presenter, model, founder, none.
6. **Key shots or script beats** if they exist. If not, the skill proposes a shot list from the deliverables.

## Output format

1. **ODG (ORDER OF DAY)** — timed schedule with locations.
2. **SHOT LIST** — grouped: Hook / Body / CTA / B-roll / Audio.
3. **EQUIPMENT CHECKLIST** — tick-box, grouped by category.
4. **CREW BRIEFING** — WhatsApp-ready block, copy-paste as-is.
5. **WEATHER NOTE** — placeholder with city + date to check the morning of.

---

## Brand voice

If a `BRAND.md` file exists in this skill's folder (`.claude/skills/shooting-day/BRAND.md`) or in `.claude/brand/BRAND.md` (global fallback), read it before generating output and apply its tone, terminology, and examples to all text you produce. A skill-local `BRAND.md` overrides the global one; if neither exists, use a clean, professional default voice.

## Instructions

### 1. Build the ODG

A timed run of the day from crew call to wrap. Each row: time, activity, location, who's needed. Include the unglamorous but critical blocks — load-in, setup, lighting, lunch, buffer, teardown. Leave real buffer; shoots run long, and a schedule with no slack is a schedule that breaks by 11am. Put the hardest or most talent-dependent setup earliest while energy is high.

### 2. Build the shot list, grouped for the edit

Do not list shots in shooting order — list them in the categories the editor needs, so nothing is missed on set:

- **Hook shots** — the first 1–2 seconds that stop the scroll. Get 3+ options.
- **Body shots** — the main content, the substance of each piece.
- **CTA shots** — the ask: to camera, product in hand, on-screen text moment.
- **B-roll** — texture, detail, cutaways, hands, environment. Over-shoot this; you always want more in the edit.
- **Audio** — clean VO, ambient/room tone, any sync sound, a clap for sync if multi-cam.

For each shot: a short description, the framing, and which deliverable it feeds. Mark the must-gets so that if the day compresses, the crew knows what cannot be dropped.

### 3. Build the equipment checklist

Grouped tick-boxes: Camera & lenses, Support (tripod, gimbal), Lighting, Audio, Power (batteries, chargers — plural, always), Storage (cards, and a backup), Grip & misc, Talent/wardrobe/props. Include the items everyone forgets: spare batteries, card reader, gaff tape, water. This is a checklist to pack against, so make it tickable.

### 4. Write the crew briefing for WhatsApp

A single copy-paste block. Plain text, short lines, emoji sparingly for scanability. It contains: call time, address with a maps pin placeholder, dress/what-to-bring, the day's goal in one line, and a "reply 👍 to confirm" so you know who's actually coming. This is the message you send the night before.

### 5. Weather note

A one-line placeholder: `Weather [city], [date] — check morning of; wet-weather cover: [indoor fallback / reschedule trigger].` If any of the shoot is outdoors, name the fallback now, not at 7am in the rain.

### Output template

```
SHOOTING DAY — [Project] · [Date] · [City]

ODG (ORDER OF DAY)
| Time | Activity | Location | Who |
|------|----------|----------|-----|
| ...  | ...      | ...      | ... |

SHOT LIST
Hook:   [ ] [shot — framing — deliverable]  (must-get marked ★)
Body:   [ ] ...
CTA:    [ ] ...
B-roll: [ ] ...
Audio:  [ ] ...

EQUIPMENT CHECKLIST
Camera & lenses: [ ] ...
Support:         [ ] ...
Lighting:        [ ] ...
Audio:           [ ] ...
Power:           [ ] spare batteries [ ] chargers
Storage:         [ ] cards [ ] backup card [ ] card reader
Grip & misc:     [ ] gaff tape [ ] water [ ] ...
Talent/props:    [ ] ...

CREW BRIEFING (WhatsApp)
📍 [Project] shoot — [day, date]
🕘 Call: [time] @ [address] (pin: [link])
🎯 Goal: [one line]
👕 Bring: [wardrobe / gear / snacks]
Reply 👍 to confirm you're in.

WEATHER
[city], [date] — check morning of. Wet-weather plan: [fallback].
```

### Edge cases

- **Multi-location day:** repeat the ODG travel blocks explicitly and add travel time between locations — it is always underestimated.
- **Founder/talent with limited availability:** front-load every shot that needs them into a tight window and schedule around it.
- **Run-and-gun, no fixed script:** keep the shot categories but frame them as targets ("3 hooks, 5 body, 2 CTA, lots of B-roll") rather than exact shots.
- **Tiny crew (one operator):** simplify the briefing and flag which shots are impossible solo so they get planned or dropped in advance.

---

## 🇮🇹 Versione italiana

### Quando usare questa skill

Per pianificare una giornata di riprese: "shooting", "riprese", "giorno di ripresa", "ODG", "scaletta set". Trasforma lo shooting in un piano che tutta la crew può seguire dal telefono.

### Cosa fa

Produce l'ordine del giorno con orari e location, una shot list categorizzata come serve davvero a un montaggio social (hook, body, CTA, B-roll, audio), una checklist attrezzatura da spuntare, e un briefing crew pronto da incollare su WhatsApp. Chiude i due problemi eterni sul set: "dov'è la shot list" e "chi ha la call sheet".

### Cosa ti serve

1. **Progetto / cliente** e cosa riprendi (reel, ad, brand film, prodotto).
2. **Data, città e location** — con call time e orario di wrap.
3. **Deliverable** — quanti pezzi, formati e durate escono dalla giornata.
4. **Crew** — chi c'è e ruolo.
5. **Talent** — presenter, modella, founder, nessuno.
6. **Shot o beat chiave** se esistono. Altrimenti la skill propone la shot list dai deliverable.

### Voce del brand

Se esiste un file `BRAND.md` nella cartella di questa skill (`.claude/skills/shooting-day/BRAND.md`) o in `.claude/brand/BRAND.md` (fallback globale), leggilo prima di generare l'output e applica tono, terminologia ed esempi a tutto il testo che produci. Il `BRAND.md` locale ha la precedenza su quello globale.

### Istruzioni

1. **ODG.** Run cronometrato dalla call al wrap. Ogni riga: ora, attività, location, chi serve. Includi load-in, setup, luci, pranzo, buffer, teardown. Lascia buffer vero. Metti il setup più difficile o dipendente dal talent presto.
2. **Shot list, raggruppata per il montaggio.** Non in ordine di ripresa ma nelle categorie che servono all'editor:
   - **Hook** — i primi 1–2 secondi che fermano lo scroll. 3+ opzioni.
   - **Body** — il contenuto principale.
   - **CTA** — la richiesta: a camera, prodotto in mano, momento con testo a schermo.
   - **B-roll** — texture, dettagli, mani, ambiente. Sovra-riprendi.
   - **Audio** — VO pulita, ambiente/room tone, sync, ciak se multi-cam.
   Per ogni shot: descrizione, inquadratura, quale deliverable alimenta. Marca i must-get con ★.
3. **Checklist attrezzatura.** Tick-box raggruppati: Camera & ottiche, Supporti, Luci, Audio, Alimentazione (batterie, caricatori — sempre plurale), Storage (schede + backup), Grip & varie, Talent/wardrobe/props. Includi ciò che tutti dimenticano: batterie di scorta, lettore schede, gaff tape, acqua.
4. **Briefing per WhatsApp.** Un blocco copia-incolla: call time, indirizzo con pin, cosa portare, obiettivo in una riga, e "rispondi 👍 per confermare". È il messaggio della sera prima.
5. **Nota meteo.** Una riga con città e data, da controllare la mattina, con il piano B se c'è esterni.

### Template di output

```
SHOOTING DAY — [Progetto] · [Data] · [Città]

ODG (ORDINE DEL GIORNO)
| Ora | Attività | Location | Chi |
|-----|----------|----------|-----|

SHOT LIST
Hook:   [ ] [shot — inquadratura — deliverable]  (must-get ★)
Body:   [ ] ...
CTA:    [ ] ...
B-roll: [ ] ...
Audio:  [ ] ...

CHECKLIST ATTREZZATURA
Camera & ottiche: [ ] ...
Supporti:         [ ] ...
Luci:             [ ] ...
Audio:            [ ] ...
Alimentazione:    [ ] batterie scorta [ ] caricatori
Storage:          [ ] schede [ ] scheda backup [ ] lettore
Grip & varie:     [ ] gaff tape [ ] acqua [ ] ...
Talent/props:     [ ] ...

BRIEFING CREW (WhatsApp)
📍 Shoot [Progetto] — [giorno, data]
🕘 Call: [ora] @ [indirizzo] (pin: [link])
🎯 Obiettivo: [una riga]
👕 Porta: [wardrobe / gear / snack]
Rispondi 👍 per confermare.

METEO
[città], [data] — controlla la mattina. Piano pioggia: [fallback].
```

### Casi limite

- **Giornata multi-location:** esplicita i blocchi di trasferimento e aggiungi i tempi di viaggio.
- **Founder/talent con poca disponibilità:** concentra ogni shot che lo richiede in una finestra stretta.
- **Run-and-gun senza script:** mantieni le categorie ma come target ("3 hook, 5 body, 2 CTA, tanto B-roll").
- **Crew minima (un operatore):** semplifica il briefing e segnala gli shot impossibili da soli.
