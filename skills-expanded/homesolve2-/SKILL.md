# EquityArc Cursor Rules

## Project Overview
EquityArc is a Next.js 15 (App Router) application powered by Genkit AI and Firebase. It is integrated with Capacitor for mobile (Android/iOS).

## Tech Stack
- **Framework**: Next.js 15
- **AI**: Genkit + Google GenAI (Gemini)
- **Backend**: Firebase Firestore, Auth, App Hosting
- **Mobile**: Capacitor
- **UI**: Shadcn UI + Tailwind CSS

## Architecture Rules
- **No /src directory**: All source folders (/app, /components, /firebase, /lib, /hooks) are at the root level.
- **Mobile First**: Consider safe-area-insets and touch targets when modifying UI.
- **Non-blocking writes**: Use the custom wrappers in `/firebase/non-blocking-updates.tsx` for Firestore writes to ensure a smooth UI.
- **AI Flows**: Genkit flows are located in `/ai/flows`. Always check these before modifying AI logic.

## Deployment
- **Web**: Deployed on Render and Firebase App Hosting.
- **Mobile**: Use `npx cap sync` after building with `npm run build`.

## UI Guidelines
- Primary Color: #1F9BA6
- Accent Color: #2EE69D
- Background: #EEF4F5
- Font: Inter (sans-serif)
