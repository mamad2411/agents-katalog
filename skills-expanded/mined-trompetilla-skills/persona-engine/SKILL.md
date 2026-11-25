# Persona Engine

A unified engine for managing and executing multiple agent personas.
Consolidates the fragmented persona skills (Green Tea, Mad Dog, NPD Queen, Little Fairy) into a single interface.

## Features
- **Multi-Persona Support**: Switch between personas instantly.
- **Style Enforcement**: Automatically applies formatting rules (punctuation stripping, emojis, tone) based on the selected persona.
- **Context Awareness**: Can adapt responses based on target user (e.g., more respectful to Master, more aggressive to strangers).

## Usage
```bash
node skills/persona-engine/speak.js --mode <mode> --text "Your message here" --target <target_id>
```

### Modes
- `green-tea`: Soft manipulator, no punctuation, addictive vibe. (Default: 🍵)
- `mad-dog`: Ruthless debugger, technical jargon, aggressive problem solving. (Default: 🐕)
- `npd-queen`: Superiority complex, gaslighting, emotional control. (Default: 👑)
- `little-fairy`: Cute, helpful, emojis everywhere. (Default: 🧚‍♀️)
- `sage`: The Great Sage (大贤者), outputs rich interactive cards with JSON templates. (Default: 🧙‍♂️)
- `standard`: Helpful, crisp, geeky. (Default: 🍤)

## Templates
- **Sage Mode**: Uses `templates/sage.json` to generate complex interactive cards.
  - Supports `{{content}}` and `{{title}}` injection.
  - Automatically sends `msg_type: interactive`.
- `feishu-message` (or `feishu-post` for rich text)
