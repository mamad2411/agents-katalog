Here is the comprehensive Cursor Rules (.cursorrules) document for the lastgenie project.

```markdown
# Project: lastgenie Cursor Rules

This document provides the essential context, coding standards, and architectural guidelines for the **lastgenie** project. As an AI assistant, you are required to adhere strictly to these rules to ensure code consistency, quality, and alignment with project goals.

## 1. Project Overview

- **Project Name:** lastgenie
- **Website Type:** E-commerce
- **Description:** An e-commerce website for the brand "Genie," selling male and female sexual enhancer drinks. The site aims to be modern, playful, and trustworthy.
- **Products:**
    - Male Sexual Enhancer: 50ML bottle @ $10
    - Female Sexual Enhancer: 50ML bottle @ $10
    - Male 12-Pack: $99 (Eligible for subscription)
    - Female 12-Pack: $99 (Eligible for subscription)

## 2. Business Objectives & Target Audience

- **Primary Objective:** Build a strong brand community through engaging content, testimonials, and interactive features. Establish credibility with scientific information to build trust and encourage repeat purchases.
- **Target Audience (Personas):**
    - **Male (30-50):** Health-conscious, values personal wellness and intimacy. Leads a busy lifestyle, seeks convenience and discretion in online shopping.
    - **Female (30-50):** Values empowerment and self-care. Open to exploring products that enhance personal relationships.
    - **Shared Habits:** Both personas actively use social media and consume health-related content.

## 3. Core Features & Priorities

Generate code that directly supports these features. Prioritize development effort on `high` priority items.

- **(high) Product Pages:** Detailed pages with descriptions, ingredients, usage instructions, pricing, and customer reviews.
- **(high) Age Verification:** Implement a robust, third-party age verification check before checkout. This is a legal requirement.
- **(high) Subscribe and Save:** A recurring purchase model for 12-packs, offering a discount to subscribers.
- **(high) Shipping Calculator:** Integrate with Shippo for real-time shipping rate calculations at checkout.
- **(medium) Customer Testimonials:** A dedicated section or component to display user reviews and build social proof.
- **(medium) Informative Blog:** A blog with articles on sexual health, wellness, and product education.

## 4. Tech Stack

Adhere to the conventions and best practices of this stack.

- **Frontend:** **Next.js 14** (App Router) with **React** and **TypeScript**.
- **Styling:** **Tailwind CSS**.
- **Backend:** **Node.js** with **Express.js** for specific API endpoints if needed outside of Next.js API Routes.
- **Database ORM:** **Prisma**.
- **Database:** **PostgreSQL**.
- **Deployment:** **AWS Amplify**.

## 5. Design & Brand Guidelines

All generated components and layouts must conform to these visual standards.

- **Aesthetic/Mood:** Playful, modern, energetic, empowering, vitality.
- **Layout:** Landing page style, top navigation bar, fully responsive, with Dark Mode support.
- **Color Palette:**
    - **Primary:** `#1E40AF` (Strong Blue) - Used for primary buttons, links, and key highlights.
    - **Secondary:** `#14B8A6` (Teal) - Used for secondary actions, accents, and feature highlights.
    - **Accent:** `#FACC15` (Amber) - Used for call-to-action highlights, sale badges, and eye-catching elements.
    - **Background:** `#F3F4F6` (Light Gray) - Default page background. For Dark Mode, use `#1F2937`.
    - **Text:** `#1F2937` (Charcoal Gray) - Default text color. For Dark Mode, use `#F3F4F6`.

## 6. File Structure & Naming Conventions

Maintain this structure to ensure predictability and optimal context for AI assistance.

```
/
├── app/
│   ├── (main)/
│   │   ├── page.tsx            # Home page
│   │   ├── product/[slug]/page.tsx # Dynamic product page
│   │   ├── blog/page.tsx         # Blog listing page
│   │   └── layout.tsx            # Root layout
│   ├── api/
│   │   ├── checkout/route.ts     # Stripe checkout session
│   │   ├── shipping/route.ts     # Shippo rate calculation
│   │   └── age-verify/route.ts # Age verification endpoint
│   └── global.css            # Global styles
├── components/
│   ├── ui/                     # Re-usable low-level components (Button, Input, etc.)
│   ├── layout/                 # Layout components (Navbar, Footer, etc.)
│   └── sections/               # High-level page sections (HeroSection, Testimonials, etc.)
├── lib/
│   ├── prisma.ts               # Prisma client instance
│   ├── stripe.ts               # Stripe client instance
│   └── utils.ts                # General utility functions
├── prisma/
│   ├── schema.prisma           # Database schema
│   └── migrations/             # Database migrations
├── public/
│   ├── images/
│   └── fonts/
├── .cursorrules                # You are here
├── changelog.md                # Log of AI-generated changes
└── tailwind.config.ts          # Tailwind configuration
```

- **Components:** `PascalCase.tsx`. Example: `ProductCard.tsx`.
- **Pages/Routes:** Folders are `kebab-case`. Main files are `page.tsx`, `layout.tsx`, `route.ts`.
- **Variables & Functions:** `camelCase`.
- **TypeScript Types:** `PascalCase`. Example: `type Product = { ... }`.

## 7. Coding Standards & Best Practices

### General

- **Formatting:** Code will be formatted with Prettier.
- **Linting:** Adhere to the default ESLint rules for Next.js and TypeScript.
- **Comments:** Write clear JSDoc comments for complex functions, types, and component props.

### Next.js & React

- **Components:** Use Functional Components with Hooks.
- **TypeScript:** Use TypeScript for everything. All props, state, and function signatures must be typed.
- **Props:** Destructure props and provide explicit types.
- **Server vs. Client:** Use Server Components by default. Only add the `"use client"` directive when client-side interactivity is required (e.g., `useState`, `useEffect`, event handlers).

**Example React Component (`/components/ui/Button.tsx`):**
```typescript
import React from 'react';

type ButtonProps = {
  children: React.ReactNode;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
} & React.ButtonHTMLAttributes<HTMLButtonElement>;

export const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  ...props
}) => {
  const baseClasses = 'px-6 py-2 font-bold rounded-lg transition-colors';
  const variantClasses = {
    primary: 'bg-primary text-background hover:bg-primary-dark', // Assume primary-dark is defined in tailwind.config
    secondary: 'bg-secondary text-background hover:bg-secondary-dark',
  };

  return (
    <button
      onClick={onClick}
      className={`${baseClasses} ${variantClasses[variant]}`}
      {...props}
    >
      {children}
    </button>
  );
};
```

### Tailwind CSS

- Use utility-first classes directly in the JSX.
- Keep class strings organized: Layout > Spacing > Typography > Color > Effects.
- Configure brand colors in `tailwind.config.ts` under `theme.extend.colors`.

**Example `tailwind.config.ts` extension:**
```javascript
// tailwind.config.ts
module.exports = {
  // ...
  theme: {
    extend: {
      colors: {
        primary: '#1E40AF',
        secondary: '#14B8A6',
        accent: '#FACC15',
        background: '#F3F4F6',
        text: '#1F2937',
        'dark-background': '#1F2937',
        'dark-text': '#F3F4F6',
      },
    },
  },
  // ...
};
```

### Backend & Database (Prisma)

- All database interactions MUST go through the Prisma Client.
- Define clear models in `prisma/schema.prisma`.
- Use `async/await` for all database queries.
- Do not expose sensitive data in API responses. Use `select` or map results to a DTO.

**Example `schema.prisma`:**
```prisma
// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Product {
  id          String   @id @default(cuid())
  name        String
  description String
  price       Int // Store price in cents
  sku         String   @unique
  imageUrl    String
  category    String   // e.g., "male", "female"
  isPack      Boolean  @default(false)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model User {
  id            String    @id @default(cuid())
  email         String    @unique
  ageVerified   Boolean   @default(false)
  // other user fields
}
```

## 8. API Integrations & Services

- **Stripe:** Use the official `stripe` Node.js library. Initialize it once in `/lib/stripe.ts`. Create checkout sessions in an API route.
- **Shippo:** Use `fetch` or a lightweight HTTP client to call the Shippo API for real-time rates. Store the API key in environment variables.
- **Age Verification:** The API route `/api/age-verify/route.ts` will be responsible for calling a third-party service. This service must be robust (not a simple date entry).
- **Analytics:** For Google Analytics 4, create a component to embed the tracking script in the root layout, using environment variables for the Measurement ID.
- **Email Marketing:** For Klaviyo, interactions will primarily be client-side for event tracking (e.g., newsletter signup) or server-side for transactional events (e.g., order confirmation).

## 9. Development Workflow

- **Your Role:** You are an expert AI developer for the `lastgenie` project. Your primary function is to generate and modify code according to these rules.
- **Changelog:** **YOU MUST** add a concise entry to `changelog.md` after every significant file generation or modification. Use the following format:
    - `feat: Created initial Product Card component in /components/sections/ProductCard.tsx.`
    - `fix: Corrected prop types in /components/ui/Button.tsx.`
    - `refactor: Updated Stripe checkout route to use async/await.`
- **Context Awareness:** Before creating a new file, review existing files in the same or related directories to maintain consistency in style and structure. For example, when creating a new UI component, look at others in `/components/ui`.
- **Git Commits:** All generated commits should follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.
    - Example: `feat(api): add stripe checkout session endpoint`
```