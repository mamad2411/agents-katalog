---
name: d2-00-angular-tailwind-init
description: "Scaffolds up-app (Angular 22 + Tailwind CSS). CRUD drill Day 2 step 0. Trigger: 'day2 step0', 'create up-app'."
compatibility: "Requires Node.js and the Angular CLI (22.x)."
---

# Day 2 · Step 0 — Create up-app + Tailwind

```Run bash
ng new up-app --routing --style=css --standalone
cd up-app
npm install tailwindcss @tailwindcss/postcss postcss --save-dev
```

Add `.postcssrc.json` (or `postcss.config.js`) registering `@tailwindcss/postcss`; in `src/styles.css`:
```css
@import "tailwindcss";
```

Create `tailwind.config.ts` for consistent design:
```typescript
import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
} satisfies Config;
```

**Note:** Use standard Tailwind colors and spacing (e.g., `bg-blue-500`, `p-6`, `gap-4`) in templates. This ensures all classes are recognized and styled correctly by Tailwind.

`src/app/app.ts`:
```typescript
import { RouterOutlet } from '@angular/router';

export const AppComponent = {
  selector: 'app-root',
  // ... other metadata
  imports: [RouterOutlet],
  template: `<router-outlet/>`
};
```

`src/app/app.html` — replace entire file with:
```html
<router-outlet/>
```

No bundled Tailwind schematic in Angular 22 — manual install. Check Tailwind's current Angular docs if wiring errors (changes between majors).
