# Rules for AI

This is a T3 Stack application with Clerk authentication. The stack is modern and well-integrated, focusing on type-safety and developer experience with the combination of TypeScript, tRPC, and Prisma.

## High Level Rules

- Use existing shadcn/ui components rather than installing new UI libraries. The correct command for installing shadcn/ui is `npx shadcn@latest add <component-name>`
- Leverage tRPC for all API endpoints rather than REST
- We are using Clerk for authentication
- We are using Supabase for database
- Work with the existing Prisma schema for database operations
- Follow the established Tailwind CSS patterns for styling
- Use the "~" path alias prefix for imports (e.g., "~/components/ui/button") rather than "@" as configured in the project's tsconfig.json and components.json
- When building new components for a specific page, they should be positioned inside the same directory as the page file in a folder called "components".
- Use the established color palette defined in tailwind.config.ts under the 'verbo' namespace:
  - verbo-green: #73ea91 (Primary action, success states)
  - verbo-purple: #872ce5 (Accent color, highlights)
  - verbo-blue: #53a1e8 (Secondary actions, information)
  - verbo-dark: #321864 (Text, headers, primary brand color)
  These colors can be used with Tailwind classes like 'text-verbo-dark' or 'bg-verbo-purple' and support opacity modifiers

## AI Models

- The models that I use are:
  - Google Gemini 2.0 Flash (gemini-2.0-flash-lite-preview-02-05)
  - Google Gemini 2.0 Flash Thinking (gemini-2.0-flash-thinking-exp-01-21)
  - OpenAI GPT-4o-mini (gpt-4o-mini)

## LLM Prompt Management

For LLM prompts in this codebase:

- Store all prompt templates in `src/lib/prompts/` with descriptive filenames
- Keep each prompt template in its own file for maintainability
- Expose prompt functions through `src/lib/prompts/index.ts`
- Use function parameters to pass dynamic content into prompts
- Document each prompt function with JSDoc comments explaining its purpose

# Types Organization

For TypeScript types in this codebase:

- Store shared types in the `src/types/` directory, organized by domain
- For LLM-related types, use `src/types/prompts.ts`
- Import types using the "~" path alias: `import { TypeName } from '~/types/domain'`
- Don't create types directly in feature/component files unless they're only used there
- Always use explicit types rather than 'any' when working with structured data
