---
name: recipevault-skills-technologies
description: Comprehensive inventory of the programming languages, frameworks, libraries, tools, and DevOps technologies used in RecipeVault.
---

# 🎓 RecipeVault Skills & Technologies

A comprehensive inventory of all programming languages, frameworks, libraries, tools, and DevOps technologies used in the RecipeVault (RecipeApp) project.

---

## 📚 Table of Contents

- [Frontend Skills](#frontend-skills)
- [Backend Skills](#backend-skills)
- [DevOps & Infrastructure](#devops--infrastructure)
- [Development Tools](#development-tools)
- [Architecture Patterns](#architecture-patterns)

---

## Frontend Skills

### Core Framework & Build Tools

| Technology                  | Version | Purpose                                           |
| --------------------------- | ------- | ------------------------------------------------- |
| **React**                   | 19      | UI framework for building interactive components  |
| **Vite**                    | 8       | Lightning-fast build tool and dev server with HMR |
| **TypeScript**              | ~6.0.2  | Static type checking for JavaScript               |
| **JavaScript (ES Modules)** | ES2022+ | Modern JavaScript with modular architecture       |

### Styling & UI Components

| Technology                   | Version         | Purpose                                                |
| ---------------------------- | --------------- | ------------------------------------------------------ |
| **Tailwind CSS**             | v4              | Utility-first CSS framework for rapid UI design        |
| **@tailwindcss/vite**        | ^4.3.0          | Vite plugin for optimized Tailwind CSS compilation     |
| **Radix UI**                 | -               | Unstyled, accessible component primitives              |
| **Shadcn UI**                | latest          | Pre-built, customizable Radix UI components            |
| **clsx / tailwind-merge**    | ^2.1.1 / ^3.6.0 | Utility functions for conditional CSS class management |
| **class-variance-authority** | ^0.7.1          | Type-safe CSS class composition library                |

### Animations & Visual Effects

| Technology                    | Version | Purpose                                                                            |
| ----------------------------- | ------- | ---------------------------------------------------------------------------------- |
| **GSAP**                      | 3.x     | Professional-grade animation library for staggered card entrance & hero animations |
| **Intersection Observer API** | native  | Built-in browser API for infinite scroll detection                                 |

### HTTP & Data Fetching

| Technology | Version | Purpose                                         |
| ---------- | ------- | ----------------------------------------------- |
| **Axios**  | ^1.16.1 | Promise-based HTTP client for API communication |

### Icons & Assets

| Technology       | Version | Purpose                                    |
| ---------------- | ------- | ------------------------------------------ |
| **Lucide React** | ^1.17.0 | Lightweight, customizable SVG icon library |

### Development & Testing

| Technology            | Purpose                                 |
| --------------------- | --------------------------------------- | ------------------------------------- |
| **ESLint**            | JavaScript/JSX linting for code quality |
| **Vite React Plugin** | ^6.0.2                                  | React-specific optimizations for Vite |

### Frontend Patterns & Concepts

- **Component-based Architecture** – Modular React components (Navbar, SearchBar, RecipeGrid, RecipeCard, RecipeModal, RecipeDetailModal)
- **Custom Hooks** – `useRecipes()` for API abstraction and state management
- **Portal API** – For rendering search dropdown outside the component tree
- **Infinite Scroll** – Intersection Observer API for pagination on scroll
- **Typeahead Search** – 300ms debounced dropdown with keyboard navigation
- **Responsive Design** – Mobile-first grid layout with Tailwind CSS
- **Glassmorphism** – Semi-transparent UI with backdrop blur effects
- **Dark UI Theme** – Shadcn UI with dark mode styling

---

## Backend Skills

### Runtime & Framework

| Technology                  | Version  | Purpose                                       |
| --------------------------- | -------- | --------------------------------------------- |
| **Node.js**                 | 20.x LTS | JavaScript runtime environment                |
| **Express.js**              | 5.2.1    | Minimalist REST API web framework             |
| **JavaScript (ES Modules)** | ES2022+  | Modern JavaScript with `import/export` syntax |

### Database & ODM

| Technology        | Version | Purpose                                                           |
| ----------------- | ------- | ----------------------------------------------------------------- |
| **MongoDB Atlas** | Cloud   | Cloud-hosted NoSQL database                                       |
| **Mongoose**      | 9.6.3   | MongoDB object data modeling (ODM) library with schema validation |

### HTTP & External APIs

| Technology | Version | Purpose                                                      |
| ---------- | ------- | ------------------------------------------------------------ |
| **Axios**  | ^1.7.2  | HTTP client for calling external DummyJSON API               |
| **CORS**   | 2.x     | Cross-Origin Resource Sharing middleware for frontend access |

### Configuration & Secrets

| Technology | Version | Purpose                                           |
| ---------- | ------- | ------------------------------------------------- |
| **dotenv** | 17.4.2  | Environment variable management from `.env` files |

### Backend Patterns & Concepts

- **REST API Design** – Standard HTTP methods (GET, POST, PUT, DELETE)
- **Smart Caching Logic** – Parallel queries to local DB and external API, auto-save new results
- **Pagination** – Offset-based pagination with `page` and `limit` params
- **Upsert Operations** – Save new API results to MongoDB automatically
- **Error Handling** – Graceful fallbacks when external API fails
- **Health Checks** – `/health` endpoint for service monitoring
- **Request Validation** – Schema-based validation via Mongoose
- **Async/Await** – Modern async patterns for API calls

### Development & Quality

| Technology                 | Purpose                                         |
| -------------------------- | ----------------------------------------------- | ------------------------------------------------------ |
| **Nodemon**                | ^3.1.4                                          | Auto-restart server on file changes during development |
| **ESLint**                 | Linting for JavaScript code quality             |
| **Node syntax validation** | Built-in `node --check` for syntax verification |

---

## DevOps & Infrastructure

### CI/CD Pipeline

| Technology         | Purpose                                                   |
| ------------------ | --------------------------------------------------------- |
| **GitHub Actions** | Automation framework for build, test, deploy workflows    |
| **Render.com**     | Cloud hosting platform for backend deployment             |
| **Vercel**         | Optimized hosting for React frontend with edge deployment |
| **Dependabot**     | Automated dependency update pull requests                 |

### Deployment & Hosting

| Platform            | Purpose                                                    |
| ------------------- | ---------------------------------------------------------- |
| **Render**          | Deploy Express backend (staging + production environments) |
| **Vercel**          | Deploy React/Vite frontend with automatic preview URLs     |
| **GitHub Releases** | Store version tags and changelogs                          |

### Security & Audits

| Tool                | Purpose                                    |
| ------------------- | ------------------------------------------ |
| **npm audit**       | Vulnerability scanning for dependencies    |
| **Secret scanning** | Detect accidentally committed `.env` files |
| **npm outdated**    | Report outdated dependencies               |

### CI/CD Workflows

1. **ci.yml** – Runs on every push/PR: lint, build, audit, test
2. **cd-production.yml** – Deploy main branch to production
3. **cd-staging.yml** – Deploy develop branch to preview
4. **security-audit.yml** – Weekly security scans

---

## Development Tools

### Version Control

| Technology        | Purpose                                             |
| ----------------- | --------------------------------------------------- |
| **Git**           | Distributed version control system                  |
| **Git Worktrees** | Isolated branch workspaces for parallel development |
| **GitHub**        | Repository hosting, PR reviews, issue tracking      |

### Package Management

| Technology            | Purpose                                        |
| --------------------- | ---------------------------------------------- |
| **npm**               | JavaScript package manager for dependencies    |
| **package-lock.json** | Lock file for reproducible dependency versions |

### Code Quality & Linting

| Technology        | Purpose                                         |
| ----------------- | ----------------------------------------------- |
| **ESLint**        | Static analysis for JavaScript/JSX code quality |
| **ESLint Config** | Shared rules across frontend and backend        |

### Testing (Future)

| Technology                    | Purpose                                                |
| ----------------------------- | ------------------------------------------------------ |
| **Jest**                      | Unit/integration testing framework (backend, optional) |
| **Supertest**                 | HTTP assertion library (backend API testing)           |
| **Vitest**                    | Lightning-fast unit test runner (frontend)             |
| **@testing-library/react**    | React component testing utilities                      |
| **@testing-library/jest-dom** | DOM matchers for testing                               |

### Documentation

| Technology               | Purpose                                             |
| ------------------------ | --------------------------------------------------- |
| **Markdown**             | README, SKILL, SECURITY documentation               |
| **Conventional Commits** | Structured commit messages (feat:, fix:, ci:, etc.) |

---

## Architecture Patterns

### Design Patterns

- **MVC (Model-View-Controller)** – Express routes + Mongoose models + React components
- **Smart Caching Pattern** – Dual-source query (DB + API) with automatic persistence
- **Composition Pattern** – Shadcn UI + Radix primitives for flexible component building
- **Custom Hooks Pattern** – Abstraction of API logic (`useRecipes`)
- **Portal Pattern** – React Portal for search dropdown overlay

### API Patterns

- **REST Architecture** – Stateless, resource-based endpoints
- **Hybrid Search** – Local DB + external API in parallel
- **Typeahead Suggestions** – Efficient prefix search for dropdown
- **Pagination** – Server-side pagination with offset/limit
- **CORS** – Cross-origin resource sharing for frontend access

### Frontend Patterns

- **Component Composition** – Small, focused, reusable React components
- **Utility-First CSS** – Tailwind CSS for atomic styling
- **Theme System** – Shadcn UI dark mode support
- **Responsive Design** – Mobile-first Tailwind breakpoints
- **Animation Library** – GSAP for sophisticated motion effects

### Backend Patterns

- **Middleware Stack** – Express CORS, JSON parsing, error handling
- **Schema Validation** – Mongoose schemas for data integrity
- **Connection Pooling** – MongoDB Atlas connection management
- **Error Handling** – Try-catch with graceful fallbacks
- **Environment Isolation** – Separate `.env` for dev/staging/prod

---

## Skill Taxonomy

### Languages & Runtimes

- JavaScript (ES2022+)
- TypeScript
- JSON (configuration, API responses)
- YAML (GitHub Actions workflows)
- Markdown (documentation)
- Bash (deployment scripts)

### Frontend Specializations

- React Component Development
- CSS-in-JS & Utility-First Styling
- Animation Engineering (GSAP)
- Accessibility (Radix UI primitives)
- Responsive Web Design
- HTTP Clients & API Integration

### Backend Specializations

- REST API Design
- Node.js/Express Development
- MongoDB/Mongoose ODM
- Database Schema Design
- Third-party API Integration
- Caching Strategies

### DevOps Specializations

- GitHub Actions Automation
- CI/CD Pipeline Architecture
- Docker/Container fundamentals (via Render)
- Infrastructure as Code (GitHub Actions YAML)
- Monitoring & Alerting
- Security Scanning & Audits

### Soft Skills Applied

- Git-based Collaboration (feature branches, PRs, reviews)
- Conventional Commit Messages
- Technical Documentation (README, SKILL, SECURITY)
- Problem Solving (smart caching logic)
- Code Review & Testing Culture

---

## Summary Statistics

| Category                  | Count                                |
| ------------------------- | ------------------------------------ |
| **Frontend Dependencies** | 12 direct                            |
| **Backend Dependencies**  | 5 direct                             |
| **DevOps Platforms**      | 3 (GitHub Actions, Render, Vercel)   |
| **Database Systems**      | 1 (MongoDB Atlas)                    |
| **Languages**             | 3 (JavaScript, TypeScript, Markdown) |
| **API Endpoints**         | 6+ REST endpoints                    |
| **CI/CD Workflows**       | 4 workflows                          |
| **Components**            | 7+ React components                  |
| **Development Tools**     | 10+ tools & libraries                |

---

## Learning Path for New Contributors

### Essential Frontend Knowledge

1. React Fundamentals (components, hooks, state)
2. Tailwind CSS (utility classes, responsive design)
3. TypeScript basics (types, interfaces)
4. Axios HTTP requests
5. GSAP animations (optional for advanced features)

### Essential Backend Knowledge

1. Express.js routing & middleware
2. MongoDB & Mongoose schemas
3. REST API principles
4. Async/await patterns
5. Error handling & validation

### Essential DevOps Knowledge

1. Git workflow (branches, PRs, merges)
2. GitHub Actions (workflows, triggers, secrets)
3. Environment variables & `.env` files
4. npm scripts & package management
5. Basic CI/CD concepts

### Optional Deep Dives

- Shadcn UI component library
- GSAP timeline animations
- MongoDB aggregation pipelines
- Docker containerization
- Advanced TypeScript patterns

---

<div align="center">

**[⬆ Back to top](#-recipevault-skills--technologies)**

Last Updated: 2026-08-09

</div>
