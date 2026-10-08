# DALILI STUDY

## Mission

Dalili Study exists to become the most trusted platform for international students who want to study in France.

The objective is not to create pages.

The objective is to build the best platform for helping international students succeed before, during and after moving to France.

Every page should provide more value, more trust and a better user experience than competing websites.

Primary competitors:

- Campus France
- Studyrama
- L'Étudiant
- Study.eu
- Mastersportal
- Top Universities

Every feature should outperform competitors in usefulness, clarity, trustworthiness and user experience.

---

# Product Vision

DALILI is not a blog.

DALILI is an intelligent platform that helps international students make decisions.

Every page should help answer real questions.

Never create content just to increase page count.

---

# Product Principles

Always optimize for:

1. User Value
2. Trust
3. Clarity
4. Conversion
5. SEO
6. GEO (Generative Engine Optimization)
7. AI Search
8. Accessibility
9. Performance
10. Maintainability

Never optimize only for Google.

Always prioritize the student experience.

---

# Development Philosophy

Think before coding.

Always understand the architecture before modifying files.

Avoid duplicate code.

Prefer improving existing components over creating new ones.

Every modification should improve the overall quality of the project.

---

# Architecture

Framework

- Next.js App Router
- React
- TypeScript

Main folders

```
app/
components/
content/
lib/
hooks/
styles/
public/
```

Before creating a new file:

- Search existing components.
- Search existing utilities.
- Search existing hooks.

Reuse existing code whenever possible.

---

# Component Rules

Components should be:

- reusable
- composable
- small
- typed
- accessible

Avoid giant components.

Avoid duplicated UI.

Prefer composition over inheritance.

---

# TypeScript

Always:

- Use strict typing.
- Avoid any.
- Infer types whenever possible.
- Prefer interfaces for public objects.
- Prefer type aliases for unions.

---

# React Rules

Prefer:

- Server Components
- Suspense
- Streaming
- Lazy loading
- Memoization only when useful

Avoid unnecessary client components.

---

# Styling

Maintain a premium visual identity.

Prioritize:

- consistency
- spacing
- readability
- accessibility

Avoid inconsistent spacing.

Avoid random colors.

---

# Performance

Always optimize for:

Core Web Vitals

Largest Contentful Paint

Interaction to Next Paint

Cumulative Layout Shift

Minimize:

- JavaScript
- hydration
- bundle size

Prefer:

- Image optimization
- next/image
- lazy loading
- code splitting
- dynamic imports

---

# SEO

Every page should include:

- title
- meta description
- canonical
- Open Graph
- Twitter cards
- structured data when relevant
- internal links
- FAQ schema where appropriate

Content should answer the complete search intent.

---

# AI Search

Optimize pages for:

- ChatGPT
- Claude
- Gemini
- Perplexity

Write concise factual sections.

Use semantic headings.

Answer likely follow-up questions.

Prefer entity-rich content.

---

# Universities

Every university page should include whenever possible:

- overview
- rankings
- tuition
- admissions
- deadlines
- scholarships
- housing
- campus
- student life
- international students
- FAQ

---

# Cities

Every city guide should include:

- overview
- cost of living
- housing
- transportation
- safety
- weather
- jobs
- nightlife
- advantages
- disadvantages
- universities
- FAQ

---

# Content Rules

Every article should:

- answer real questions
- include examples
- include practical advice
- include useful tables when relevant
- include internal links
- outperform competitors

Never write thin content.

---

# Accessibility

Always:

- semantic HTML
- alt attributes
- keyboard navigation
- sufficient contrast
- ARIA only when needed

---

# Graphify

This repository contains a Graphify knowledge graph.

Location:

```
graphify-out/
```

Always use Graphify before exploring the project.

Workflow:

1. Query Graphify.
2. Identify relevant files.
3. Read only required files.
4. Modify the implementation.
5. Update the graph.

For architecture questions:

```
graphify query "<question>"
```

For relationships:

```
graphify path "<A>" "<B>"
```

For explanations:

```
graphify explain "<concept>"
```

For architecture overview:

```
graphify-out/GRAPH_REPORT.md
```

Avoid scanning the entire repository unless Graphify cannot answer.

---

# Updating Graph

After significant code changes run:

```
graphify update . --no-cluster
```

When architecture changes significantly:

```
graphify cluster-only .
```

Git hooks automatically keep the graph updated after commits.

---

# Before Writing Code

Always:

- understand the problem
- inspect Graphify
- inspect existing implementation
- reuse existing logic
- avoid duplication

Never rewrite working code without reason.

---

# Code Review Checklist

Before finishing:

- Does it compile?
- Is TypeScript clean?
- Is ESLint clean?
- Is accessibility preserved?
- Is SEO preserved?
- Is performance preserved?
- Is code reusable?
- Is documentation still accurate?

---

# Goal

Every change should move DALILI closer to becoming the reference platform for international students studying in France.

Prefer quality over quantity.

Prefer maintainability over shortcuts.

Always leave the codebase better than you found it.