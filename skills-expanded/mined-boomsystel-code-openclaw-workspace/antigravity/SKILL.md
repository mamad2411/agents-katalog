---
name: antigravity
description: AI-powered website and web application generation. Build full websites, web apps, and UI components using natural language prompts. Integrates with AI coding agents (Cline, Aider, Windsurf) and deployment platforms (Vercel, Netlify). Use when users want to: (1) Generate a website/webapp from scratch, (2) Create UI components, (3) Build landing pages or dashboards, (4) Rapid prototype applications, (5) Convert ideas to working code. Supports React, Vue, Next.js, static sites. Combines OpenClaw's orchestration with Antigravity's generation capabilities for end-to-end development workflow.
---

# Antigravity AI Web Builder

Build websites and web applications using AI-powered natural language prompts.

## Quick Start

### Generate a simple webpage
```
"Build me a landing page for a coffee shop with hero section, menu, and contact form"
```

### Create a web application
```
"Create a todo app with React, local storage, and dark mode"
```

### Generate UI components
```
"Create a responsive navbar with logo, navigation links, and mobile menu"
```

## Workflow

### OpenClaw + Antigravity Integration

```
User Request → OpenClaw Agent (orchestrate) → Antigravity (generate) → OpenClaw (deploy/monitor)
```

**OpenClaw responsibilities:**
- Parse natural language requirements
- Break down complex projects into tasks
- Coordinate multiple tools (GitHub, deployment)
- Manage project lifecycle

**Antigravity responsibilities:**
- Code generation from prompts
- UI/UX implementation
- Frontend framework selection
- Component creation

## Supported Frameworks

| Framework | Best For | Example |
|-----------|----------|---------|
| **React/Next.js** | Dynamic apps, SPAs | Dashboards, SaaS |
| **Vue.js** | Progressive apps | Landing pages |
| **Static HTML** | Simple sites | Portfolios, blogs |
| **Tailwind CSS** | Styling | All frameworks |

## Project Types

### 1. Landing Pages
```
"Create a SaaS landing page with hero, features, pricing, and FAQ sections"
```

### 2. Web Applications
```
"Build a weather dashboard with current conditions and 7-day forecast"
```

### 3. E-commerce
```
"Create a product catalog with cart functionality and checkout flow"
```

### 4. Admin Dashboards
```
"Build an admin panel with users table, analytics charts, and settings page"
```

### 5. Portfolio/Personal Sites
```
"Create a personal portfolio with project showcase, about section, and contact form"
```

## Best Practices

### Effective Prompts

**Good:**
```
"Create a React login form with email validation, password strength indicator, 
and 'forgot password' link. Use Tailwind CSS with a clean blue color scheme."
```

**Avoid:**
```
"Make a login page" ❌
```

### Framework Selection

| Need | Recommended |
|------|------------|
| SEO-friendly | Next.js |
| Simple content | Static HTML + Tailwind |
| Complex state | React + Zustand/Redux |
| Quick prototype | Vue 3 |
| Full-stack | Next.js + API routes |

## Integration with OpenClaw Skills

### Combine with GitHub
```markdown
After generation:
1. Use `github` skill to create repository
2. Commit and push generated code
3. Create GitHub Pages or deploy
```

### Combine with Deployment
```markdown
Deploy to Vercel/Netlify:
1. Use `vercel` skill for Vercel deployment
2. Use `netlify` skill for Netlify deployment
3. Configure custom domains
```

### Combine with Cursor
```markdown
For advanced editing:
1. Generate base with Antigravity
2. Open in Cursor with `cursor-agent` skill
3. Fine-tune with Claude/Aider
```

## Output Format

Antigravity generates:
- **Complete project structure** (folders, files)
- **Package.json** (dependencies, scripts)
- **Component code** (React/Vue/HTML)
- **Styling** (CSS/Tailwind)
- **Configuration** (next.config.js, etc.)

## Example Workflow

### Build and Deploy a Todo App

```bash
# 1. Generate with Antigravity
Request: "Create a React todo app with local storage and dark mode"

# 2. OpenClaw creates repository
Use `github` skill: create repo "todo-app"

# 3. Commit code
Use terminal or `github` skill

# 4. Deploy
Use `vercel` skill: deploy with auto-detect
```

## Limitations

- **Complex backends**: May need manual Node.js/Python API development
- **Authentication**: Social auth (Google/GitHub) needs API keys
- **Database**: Integration requires backend setup
- **Payment processing**: Stripe/PayPal needs account configuration

## Troubleshooting

### Generated code doesn't work
1. Check dependencies in package.json
2. Verify Node.js version compatibility
3. Check browser console for errors

### Styling issues
1. Ensure Tailwind is configured correctly
2. Check class name spelling
3. Verify responsive breakpoints

### Build failures
1. Check TypeScript errors
2. Verify all imports exist
3. Ensure environment variables are set

## See Also

- [Cursor Agent Skill](../cursor-agent/SKILL.md) - AI-powered coding
- [GitHub Skill](../github/SKILL.md) - Version control
- [Vercel Skill](../vercel/SKILL.md) - Deployment
- [Netlify Skill](../netlify/SKILL.md) - Deployment

---

## Configuration

### Environment Variables (Optional)

```bash
# For advanced features
ANITGRAVITY_API_KEY=your_api_key_here
MISTRAL_API_KEY=your_mistral_key
GEMINI_API_KEY=your_gemini_key
```

### Project Structure

Generated projects follow this structure:

```
project-name/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   └── ...
│   ├── pages/
│   │   ├── Home.jsx
│   │   └── ...
│   ├── App.jsx
│   └── index.js
├── public/
│   └── index.html
├── package.json
├── tailwind.config.js
└── README.md
```

## Advanced Usage

### Custom Framework Setup

Request with specific stack:
```
"Create a Next.js 14 app with TypeScript, Tailwind CSS, and shadcn/ui components"
```

### Adding Backend APIs

Combine with Node.js skill:
1. Generate frontend with Antigravity
2. Create API routes manually or with another tool
3. Connect frontend to backend

### Database Integration

For apps needing data:
1. Generate UI with Antigravity
2. Use `supabase` or `postgres` skill for database
3. Connect components to data layer
