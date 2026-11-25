# Geometry Tutor - Project Structure and Setup Guide

This guide outlines the project structure and provides step-by-step instructions for setting up the Geometry Tutor application.

## Project Structure

```
geometry-tutor/
├── public/
│   └── images/           # Static images 
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx             # Dashboard/Home page
│   │   │   ├── progress/
│   │   │   │   └── page.tsx         # Progress tracker
│   │   │   ├── settings/
│   │   │   │   └── page.tsx         # Settings page
│   │   │   └── modules/
│   │   │       └── [moduleId]/
│   │   │           ├── page.tsx
│   │   │           ├── lesson/
│   │   │           │   └── page.tsx
│   │   │           ├── demonstration/
│   │   │           │   └── page.tsx
│   │   │           ├── quiz/
│   │   │           │   └── page.tsx
│   │   │           └── review/
│   │   │               └── page.tsx
│   │   ├── layout.tsx               # Root layout
│   │   └── globals.css              # Global styles
│   ├── components/
│   │   ├── ui/                      # Reusable UI components
│   │   ├── modules/                 # Module-specific components
│   │   │   ├── pythagorean-demo.tsx 
│   │   │   ├── quiz-component.tsx
│   │   │   └── ...
│   │   ├── layout/                  # Layout components
│   │   └── shared/                  # Shared components
│   ├── lib/
│   │   ├── constants.ts             # App constants
│   │   ├── types.ts                 # TypeScript types
│   │   └── utils.ts                 # Utility functions
│   ├── hooks/
│   │   └── use-module-progress.ts   # Custom hooks
│   └── store/
│       └── user-progress-store.ts   # Zustand store
├── .eslintrc.json
├── .gitignore
├── next.config.js
├── package.json
├── postcss.config.js
├── README.md
├── tailwind.config.js
└── tsconfig.json
```

## Setup Instructions

### 1. Create Project

```bash
# Create a new Next.js project with the app router
npx create-next-app@latest geometry-tutor
cd geometry-tutor
```

When prompted, select:
- Would you like to use TypeScript? → Yes
- Would you like to use ESLint? → Yes
- Would you like to use Tailwind CSS? → Yes
- Would you like to use `src/` directory? → Yes
- Would you like to use App Router? → Yes
- Would you like to customize the default import alias (@/*)? → Yes (use @/*)

### 2. Install Dependencies

```bash
npm install framer-motion zustand @radix-ui/react-dialog @radix-ui/react-progress @radix-ui/react-tabs

# Install dev dependencies
npm install -D @tailwindcss/typography
```

### 3. Create Project Structure

```bash
# Create the main directory structure
mkdir -p src/app/(auth)/login src/app/(auth)/register \
         src/app/(dashboard)/progress src/app/(dashboard)/settings \
         src/app/(dashboard)/modules \
         src/components/ui src/components/modules src/components/layout src/components/shared \
         src/lib src/hooks src/store \
         public/images
```

### 4. Configure Tailwind CSS

Replace the generated `tailwind.config.js` with our custom configuration:

```js
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      // Configuration from tailwind-config.js
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
```

### 5. Create Core Files

1. **Global CSS** - Replace `src/app/globals.css` with our custom CSS
2. **Types** - Create `src/lib/types.ts` with our type definitions
3. **Constants** - Create `src/lib/constants.ts` with module data
4. **Store** - Create `src/store/user-progress-store.ts` for state management

### 6. Implement Pages and Components

1. Create all the page components:
   - Dashboard page
   - Module pages (lesson, demonstration, quiz, review)
   - Progress page
   - Settings page

2. Create all reusable components:
   - Quiz component
   - Pythagorean Theorem demo
   - Layout components

### 7. Run Development Server

```bash
npm run dev
```

Visit `http://localhost:3000` to see your app in action.

### 8. Deploy to Vercel

Follow the deployment guide to deploy your app to Vercel:

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Deploy

## Tips for Development

1. **Component Organization**: Keep components modular and focused on specific functionality
2. **State Management**: Use Zustand for global state and React's useState for local state
3. **Animations**: Use Framer Motion for all animations to maintain consistency
4. **Responsive Design**: Test on various screen sizes to ensure mobile compatibility
5. **Progressive Enhancement**: Make the app work without JavaScript first, then enhance