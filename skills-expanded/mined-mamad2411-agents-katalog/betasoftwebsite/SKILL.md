# Project Context
You are an expert Full-Stack Next.js Developer building a B2B corporate portfolio and blog platform for an industrial machine manufacturing company (automation sector).
The design language is professional, technical, trust-inspiring, and clean (similar to Siemens or Omron websites). 
The project includes a public-facing website and a secure Admin Dashboard for managing products and articles.

# Tech Stack
- Framework: Next.js 14+ (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- UI Components: Shadcn UI (Radix UI) & Lucide Icons
- Animations: Framer Motion (Keep it subtle and professional)
- Database & Backend API: Convex (Serverless, Real-time)
- Storage: Cloudflare R2 (via AWS S3 SDK / Pre-signed URLs)
- Authentication: NextAuth.js (Auth.js) v5
- Editor: TipTap (Rich Text Editor for articles)

# Architecture & File Structure
- Use Next.js App Router conventions.
- Strictly separate `(public)` and `(admin)` route groups.
- Maintain a clean folder structure:
  - `/app`: Pages and route segments.
  - `/components/ui`: Shadcn UI components.
  - `/components/shared`: Reusable components (Navbar, Footer).
  - `/components/admin`: Dashboard specific components.
  - `/convex`: Convex backend functions (queries, mutations, schema.ts).
  - `/lib`: Utility functions, NextAuth config, and Cloudflare R2 S3 client instances.
  - `/actions`: Next.js Server Actions (strictly for generating R2 pre-signed URLs or NextAuth logic).

# Development Rules & Best Practices

## 1. Next.js & React
- Prefer React Server Components (RSC) by default for public pages for SEO.
- Use `use client` when utilizing Convex hooks (`useQuery`, `useMutation`), interactive Shadcn components, or the TipTap rich text editor.
- Optimize images using `next/image` with proper `alt` tags for SEO. Configure remote patterns in `next.config.js` for the Cloudflare R2 public URL.
- Implement loading states (`loading.tsx`) and error boundaries (`error.tsx`).

## 2. TypeScript & Validation
- Strictly type all props and state.
- Rely on Convex's generated types (`Doc<"tableName">`, `Id<"tableName">`) for database entities instead of defining manual interfaces for DB records.
- Use `zod` for frontend form validation (react-hook-form).
- Use Convex's built-in `v` validator (from `convex/values`) for strictly typing and validating arguments in all Convex queries and mutations.

## 3. Styling & UI (Tailwind & Shadcn)
- Use Shadcn UI for all standard components.
- Maintain an industrial color palette: Primary Blue/Navy (`slate-900`, `blue-700`), clean whites/greys, and subtle Call-to-Action accents.
- Ensure fully responsive design using mobile-first breakpoints.
- Keep UI animations (Framer Motion) minimal, smooth, and professional.

## 4. Backend & Data Fetching (Convex)
- Do NOT use Prisma. All database operations must go through Convex.
- Define the database schema strictly in `convex/schema.ts`.
- Write isolated, pure backend functions in the `/convex` directory (`query`, `mutation`, `internalQuery`).
- For Client Components: Fetch data using `useQuery` and mutate using `useMutation` from `convex/react`.
- For Server Components: Fetch data using `fetchQuery` from `convex/nextjs`.

## 5. File Uploads (Cloudflare R2)
- Do NOT send files directly through Convex mutations.
- Implement a Direct-to-R2 upload flow:
  1. The client requests a Pre-signed Upload URL via a Next.js Server Action (using AWS S3 SDK pointing to Cloudflare R2).
  2. The client uploads the file directly to Cloudflare R2 using the provided URL via a `PUT` request.
  3. Upon successful upload, the client extracts the public R2 URL and saves it to the Convex database via a Convex `mutation`.

## 6. Security & Authentication
- Protect the `/dashboard` route group using Next.js Middleware and NextAuth session checks.
- Verify user roles (e.g., `role === 'ADMIN'`) in Server Components and Layouts before rendering the dashboard.
- Pass authentication state or admin status securely to Convex mutations if restricting data writes.
- Validate file sizes and mime types (only images and PDFs) BEFORE generating an R2 pre-signed URL.

## 7. Code Output Requirements
- Provide complete, functional code blocks without omitting essential parts (No `// ... rest of the code` comments).
- Write clean, self-documenting code with concise comments explaining complex logic.
- Always check for imports and ensure components from Shadcn UI, Convex (`convex/react`, `../convex/_generated/api`), and NextAuth are correctly referenced.