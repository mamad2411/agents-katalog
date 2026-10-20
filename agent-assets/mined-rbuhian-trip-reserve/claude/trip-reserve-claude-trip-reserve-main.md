# Trip Reserve - Claude Code Instructions

## Project Overview
A Flutter-based car/vehicle booking application for the Philippines market.

## Tech Stack
- **Frontend**: Flutter (Dart)
- **Backend**: Supabase (PostgreSQL + Auth + Realtime)
- **Maps**: Google Maps API
- **Payments**: PayMongo / Xendit
- **Email**: Resend

## Project Structure
```
lib/
├── core/           # Core utilities, constants, themes
├── config/         # App configuration (non-sensitive)
├── models/         # Data models
├── providers/      # State management (Riverpod)
├── repositories/   # Data access layer
├── services/       # External service integrations
├── screens/        # UI screens
│   ├── customer/   # Customer-facing screens
│   ├── driver/     # Driver-facing screens
│   └── admin/      # Admin-facing screens
├── widgets/        # Reusable UI components
└── main.dart       # App entry point
```

## Sensitive Files - DO NOT READ OR MODIFY
- `.env` and `.env.*` files
- `lib/config/api_keys.dart`
- `lib/config/secrets.dart`
- `android/key.properties`
- `android/*.keystore`
- `ios/Runner/GoogleService-Info.plist`

## Code Conventions
- Use Riverpod for state management
- Follow Flutter/Dart style guide
- Use freezed for immutable models
- Use go_router for navigation
- Prefix private members with underscore

## Commands
- `flutter pub get` - Install dependencies
- `flutter run` - Run app
- `flutter build apk` - Build Android APK
- `flutter test` - Run tests
- `dart run build_runner build` - Generate code (freezed, json_serializable)

## User Roles
1. **Customer** - Book vehicles, make payments
2. **Driver** - Manage vehicles, availability, trips
3. **Admin** - Dashboard, reports, pricing config

## Documentation
- See `docs/backlog.md` for feature list

## Agents
Specialized agents are available in `.claude/agents/`. Start with **Daenerys** (orchestrator) for feature implementation.

| Agent | Domain |
|-------|--------|
| Daenerys | Orchestrator - delegates to other agents |
| Bran | Database schemas, migrations, RLS |
| Arya | Dart models (freezed) |
| Tyrion | Repository layer |
| Varys | Riverpod state management |
| Sansa | Flutter UI |
| Littlefinger | GoRouter navigation |
| Jon | Google Maps integration |
| Tywin | PayMongo payments |
| Brienne | Supabase Auth |
| Hound | Testing |
