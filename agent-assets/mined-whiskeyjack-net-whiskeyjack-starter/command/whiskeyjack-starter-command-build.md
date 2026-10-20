Build and verify the app.

## Steps

1. Run `npm run lint` – ESLint enforces the machine-checkable conventions
   (Phosphor-only icons, token colors rather than raw Tailwind palette hues or
   hardcoded hex, en dashes, React hook rules). Fix what it reports; reach for
   `eslint-disable` only when you can say why the rule is wrong in that spot.
2. Run `npm run build` from the project root – it runs `tsc` (type-check) then `vite build`.
3. Report any lint, type, or build errors, with the `file:line`.
4. If it succeeds, note the output bundle summary.

For a dev server instead, run `npm run dev`. Taking the app native (desktop /
mobile) adds a `src-tauri/` scaffold and builds through the Tauri CLI – wire
that in when you get there.
