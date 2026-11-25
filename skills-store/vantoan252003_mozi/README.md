# GoMove Client App

Flutter client app for ride-hailing and food delivery.

## Setup
```bash
cp .env.example .env
# Fill in .env values

flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs

flutter run --dart-define-from-file=.env
```

## Architecture
Clean Architecture. Read SKILL.md at root before coding.

## Key docs
- /SKILL.md             — Master architecture guide
- /CLAUDE.md            — Claude Code instructions
- /AGENTS.md            — OpenAI Codex instructions
- Each folder has its own SKILL.md with detailed implementation guidance
