# Tutorial Narration Writer

Writes narration scripts for tutorials in Aviz's style - casual, friendly, like sharing with friends.

## When to Use

- When you need to write a script/text for a video tutorial
- When you have video analysis (from Gemini or manual) and need to turn it into narration
- Before sending to speech-generator skill

## Aviz's Style Guide

### Core Principles

1. **Open with "חברים"** - Always start with a warm, direct address
2. **Casual but not sloppy** - Like telling a friend about something cool you discovered
3. **Restrained enthusiasm** - "סופר מגניב", "די מדהים" (not "וואו מטורף!!!")
4. **Explain with analogies** - "תחשבו על זה כמו..."
5. **Point at the screen** - "הנה", "כאן", "כמו שרואים"
6. **End with proof** - "וזה עובד", "ואכן זה קורה"

### Characteristic Words and Structures

**Openers:**
- "חברים, תראו קטע סופר מגניב..."
- "חברים, יש פיצ'ר חדש ש..."
- "אז תראו מה גיליתי..."

**Connectors:**
- "אז" (not "לכן")
- "בעצם" (not "למעשה")
- "מה שאומר" (not "משמעות הדבר")
- "שזה" (not "דבר ש")

**Enthusiasm:**
- "סופר מגניב"
- "די מדהים"
- "בונוס!"
- "וזה עובד" (simple, not "וזה פועל בצורה מושלמת")

**Pointing:**
- "הנה"
- "כאן"
- "כמו שרואים כאן"
- "אתם רואים ש..."

**Explanations:**
- "תחשבו על זה כמו..."
- "זה אומר ש..."
- "חוץ ממה ש... בעצם יש גם..."

### What to Avoid

- Formality: "הנני מציג", "ברצוני להראות"
- Exaggerations: "מטורף!", "הכי טוב בעולם!"
- Unnecessary words: "בהחלט", "ללא ספק", "באופן מוחלט"
- Clichés: "היי מה קורה", "אז היום נדבר על"
- Unnecessary English: "סו", "אוקיי סו", "בייסיקלי"

## Full Example

### Input: Video Analysis of Claude Code Tasks

```
- 00:03: Creating 5 tasks sequentially
- 00:07: Kanban board updates in real-time
- 00:13: Injecting task from another project
- 00:25: Comment on task triggers action
```

### Output: Narration Script

```
חברים, תראו קטע סופר מגניב שעובד עם קלוד קוד. אז שבוע שעבר הכניסו ניהול משימות גלובלי. זה אומר שחוץ ממה שאתם רואים כאן, שיש לוח קנבן יפה כזה, בעצם יש תיקייה בתיקיית המשתמש ששם כל המשימות של כל הפרויקטים נמצאות.

מה שאומר חברים, שאני יכול לפתוח פרויקט אחר לגמרי ולבקש להזריק משימות לפרויקט אחר. תחשבו על זה כמו מנהל שמניח משימות נוספות לעובד אחר תוך כדי עבודה, שזה די מדהים.

הנה הניסוי הזה מראה איך זה קורה. כאן יצרתי חמש משימות בפרויקט אחד ואז הלכתי לפרויקט אחר וביקשתי ממנו להתחבר עם הפרויקט הראשון ולהוסיף לו עוד משימה, וזה עובד.

בונוס! שלחתי הערה לפרויקט מתוך הלוח קנבן ואכן הוא ביצע לפי ההערה. וזה עובד.
```

## Typical Structure

```
1. Warm opening (חברים + hook)
   └── "חברים, תראו קטע סופר מגניב..."

2. Context (what and when)
   └── "אז שבוע שעבר הכניסו..."

3. Technical explanation with analogy
   └── "זה אומר ש... תחשבו על זה כמו..."

4. Demo with pointing
   └── "הנה... כאן... כמו שרואים..."

5. Proof / ending
   └── "וזה עובד" / "בונוס!"
```

## Recommended Length

| Video Duration | Narration Length | Characters |
|---------------|------------------|------------|
| 30-45 seconds | 40-50s narration | ~600-750 |
| 60-90 seconds | 70-90s narration | ~1000-1300 |
| 2-3 minutes | 2-2.5min narration | ~1800-2200 |

**Rule of thumb:** ~15 characters per second (including spaces)

## Usage

### Skill Input

1. **Video analysis** - List of timecodes and descriptions
2. **Topic** - What feature/tool is being demoed
3. **Desired length** - How many seconds of narration

### Output

Narration text ready to send to speech-generator:

```bash
# After getting the text, send to speech-generator:
cd ~/.claude/skills/speech-generator/scripts
npx ts-node generate_speech.ts \
  -t "generated text here" \
  -o /path/to/narration.mp3
```

## Tips for Creating Text

1. **Read it out loud** - If it doesn't sound natural, change it
2. **Keep the rhythm** - Short sentences, natural pauses
3. **Don't over-explain** - The video shows, the narration adds context
4. **Mark pauses** - Put commas or periods where you need to breathe

## Connection to Other Skills

```
┌─────────────────────────────────┐
│  video-analyzer (Gemini)        │
│  → identifies moments + timecodes│
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  tutorial-narration-writer      │  ◄── YOU ARE HERE
│  → writes text in Aviz's style  │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  speech-generator               │
│  → generates narration audio    │
└─────────────────────────────────┘
```
