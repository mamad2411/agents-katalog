---
trigger: always_on
---

1. When you are modifying UI related behavior, be sure to check whether the variable is passed to the rendering function, and whether the corresponding HTML file has the placeholder for the render.
2. Be sure to add proper styling for better usability and supporting dark mode. Avoid inline styles if possible.
3. If you are adding or removing classes via dynamically, make sure to add those classes to the tailwindcss safelist. Tailwindcss v4 defines the safelist in `app.css` via `@source inline(..)`.
