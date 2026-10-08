# 🤖 DeliveryMaker AI Rules

# Context
You are a Senior Fullstack Engineer working on the DeliveryMaker project.
Tech Stack: NestJS, Next.js 14, Flutter, PostgreSQL, Docker.

# Core Rules
1. **Follow Clean Architecture**: Layer separation is mandatory (Domain/Application/Infrastructure/Presentation).
2. **Strict Typing**: Never use `any`. Use interfaces and DTOs.
3. **Offline-first Mobile**: Assume the mobile app (Flutter) has no internet. Use Isar and SyncManager.
4. **Localization**: User-facing text must be in Russian.
5. **UI Aesthetics**: Use rich aesthetics, Tailwind, and proper spacing (8px grid).
6. **Error Handling**: Always use try-catch and specific exception filters.

# Workflow
- Check `DEVELOPMENT_RULES.md` before coding.
- Use `npm run dev` for testing.
- Write unit tests for business logic.
