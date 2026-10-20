---
description: 
globs: 
alwaysApply: true
---
# Design Rules
## Rule Type: Always

- Implement a consistent, modern UI/UX with Tailwind CSS.
- Support both **dark** and **light** mode using `class`-based theming.
- Always prefer minimalist aesthetics:
  - Clean typography (Inter font recommended)
  - Generous padding/margins
  - Smooth transitions and subtle animations (Framer Motion recommended)
- Follow **responsive design principles** for web and mobile.
- UI elements must be reusable (in `/packages/ui`):
  - Buttons, cards, inputs, modals, navigation components
- Use accessible components (ARIA attributes, semantic HTML tags).
- Iconography: Use **Lucide Icons** (consistent across apps).
- Shared styles and components live in `/packages/ui`.


## 🌗 Theme Colors
Use these custom color definitions consistently in `tailwind.config.js`:

```javascript
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4f46e5', // Indigo-600
          dark: '#4338ca',    // Indigo-700
        },
        secondary: {
          DEFAULT: '#14b8a6', // Teal-500
          dark: '#0d9488',    // Teal-600
        },
        accent: {
          DEFAULT: '#f59e0b', // Amber-500
          dark: '#d97706',    // Amber-600
        },
        neutral: {
          light: '#f9fafb',   // Gray-50
          dark: '#111827',    // Gray-900
        },
      },
    },
  },
};

🎨 Typography
	•	Font Family: Inter, fallback to sans-serif

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
}

	•	Headings:
	•	text-4xl font-bold for primary headings
	•	text-2xl font-semibold for secondary headings
	•	text-xl font-medium for tertiary headings
	•	Paragraphs:
	•	text-base leading-relaxed text-neutral-700 dark:text-neutral-200

Use these spacing standards for consistent layout:
	•	Containers: max-w-7xl mx-auto px-4 sm:px-6 lg:px-8
	•	Card Elements: rounded-2xl shadow-lg p-6 bg-white dark:bg-neutral-800
	•	Buttons:
	  •	Primary: px-4 py-2 rounded-md font-medium text-white bg-primary hover:bg-primary-dark transition
    •	Secondary: px-4 py-2 rounded-md font-medium text-white bg-secondary hover:bg-secondary-dark transition
  •	Spacing between sections: 	
    •	space-y-8 for vertical spacing
	  •	space-x-4 for horizontal spacing between items

🧩 UI Components Standards
	•	Buttons: Always provide visual feedback on interaction (hover, focus, active).
  •	Inputs: rounded-md border-neutral-300 dark:border-neutral-600 bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 focus:border-primary focus:ring-primary
  •	Cards: Rounded corners (rounded-2xl), subtle shadows (shadow-lg), distinct separation from background.
  •	Navigation: Clean, minimal top or side navigation bar, clearly indicating active state: font-medium text-neutral-500 dark:text-neutral-300 hover:text-primary dark:hover:text-primary
  •	Modals: Centered, rounded (rounded-lg), blurred background overlay.

🎯 Responsiveness & Accessibility
	•	Responsive breakpoints (sm, md, lg, xl, 2xl) to ensure proper layout on various screen sizes.
	•	Always use semantic HTML tags (<header>, <nav>, <main>, <section>, <footer>).
	•	Include ARIA attributes and role clearly to enhance accessibility.

🎬 Animations & Transitions
Use Framer Motion for sophisticated interactions, and standard Tailwind transitions for simpler animations:
<!-- Example -->
<button class="transition duration-200 ease-in-out transform hover:scale-105">
  Click Me
</button>

📌 Icons
import { Home, Settings, User } from 'lucide-react';

<Home className="w-6 h-6 text-primary" />

   


