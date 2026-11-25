---
name: project-workshop-generator
description: A universal workshop generator that analyzes ANY codebase to create structured onboarding material (Markdown + Remotion scripts). It automatically identifies the tech stack, project goals, and setup procedures to produce tailored training for developers and managers. Use when a user says "create a workshop", "generate onboarding docs", "explain this project to the team", or "make a video presentation" for any repository. Outputs -> structured Markdown workshop + Remotion slide script.
---

# Universal Project Workshop Generator

This skill transforms any repository into a comprehensive 5-module workshop. It is stack-agnostic and adapts its content based on the identified architecture and project type.

## Workflow

### 1. Project Discovery (MANDATORY)

Before generating any content, the agent MUST:

- **Identify Stack**: Check for `package.json` (JS/TS), `requirements.txt`/`pyproject.toml` (Python), `Cargo.toml` (Rust), `go.mod` (Go), etc.
- **Identify Architecture**: Look for `src/`, `app/`, `lib/`, `migrations/`, `docker-compose.yml`, or `kubernetes/` directories.
- **Extract Vision**: Read `README.md`, `docs/`, or any high-level architecture diagrams to understand the "Why" and "Who" of the project.

### 2. Workshop Structure

ALWAYS generate the workshop using this universal 5-module framework, tailored to the discovered data:

0. **Module 0: Prerequisites Check**
   - Required software versions
   - Access/credentials needed
   - Expected attendee skill level (beginner / mid / senior)

1. **Module 1: Vision & Strategy (Management focus)**
   - **Context**: Project goals, target users, and key value proposition.
   - **Business Impact**: ROI or strategic importance identified from documentation.

2. **Module 2: Technical Deep Dive (Developer focus)**
   - **System Architecture**: High-level overview of the identified stack and components.
   - **Data Flow**: Explanation of how the core feature works (e.g., Request -> Controller -> DB).

3. **Module 3: Setup & Configuration (Hands-on)**
   - **Environment**: Toolchain installation (e.g., "Install pnpm and Docker").
   - **Bootstrap**: Step-by-step commands to get the project running locally.
   - **Secrets**: List of required environment variables found in `.env.example` or config files.

4. **Module 4: Usage & Workflow (Standard users)**
   - **Main Features**: How to use the primary functionality of the project.
   - **Dev Workflow**: How to run tests, linting, and build commands.

5. **Module 5: Practical Exercises (Labs)**
   - **The Lab**: Generate 2-3 exercises at different difficulty levels:
      - Easy: reproduce an existing feature
      - Medium: add a small new feature
      - Hard: debug a broken scenario

## Remotion Video Scripting

Generate a generic `workshop-video.tsx` that acts as a slide deck.

- Use the project's name as the main title.
- Create slides for each module using the data extracted during the discovery phase.
- Ensure the template is valid React/Remotion code.

## Guidelines

- **Language**: DEFAULT to the language of the README.md or the user's prompt. If none is detectable, use English.
- **Agnosticism**: Never assume a specific technology (like Supabase or GitHub) unless you have confirmed its presence in the current repository.
- **Self-Correction**: If documentation is missing, the skill should guide the user on how to provide the missing context before generating the workshop.
- **Accuracy**: Base setup instructions ONLY on actual files found in the repo (e.g., don't suggest `npm install` if there's only a `yarn.lock`).
