# Repo Referensi: insforge/insforge-skills

Repo: https://github.com/insforge/insforge-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/insforge_insforge-skills
API: curl "localhost:27126/repos/readme?name=insforge_insforge-skills"
Dibuat: 2026-09-16

## Cuplikan README
# insforge/insforge-skills

Source: https://github.com/insforge/insforge-skills
Fetched: 2026-09-16

## README
# InsForge Agent Skills

Agent Skills to help developers using AI agents build applications with [InsForge](https://insforge.dev) Backend-as-a-Service.

## Installation

### Codex plugin marketplace

Add this repository as a Codex plugin marketplace, then install the InsForge plugin:

```bash
codex plugin marketplace add InsForge/insforge-skills
codex plugin add insforge@insforge
```

After installing, start a new Codex thread and ask Codex to use InsForge or one of the bundled skills.

### Using the skills registry

```bash
npx -y skills add insforge/insforge-skills
```

### Claude Code

```bash
/install-skills insforge/insforge-skills
```

## Available Skills

<details>
<summary><strong>insforge</strong> - InsForge Backend-as-a-Service Development</summary>

Build full-stack applications with InsForge. This skill provides comprehensive guidance for:

- **Database**: CRUD operations, schema design, RLS policies, triggers
- **Authentication**: Sign up/in flows, OAuth, sessions, email verification
- **Storage**: File uploads, downloads, bucket management
- **Functions**: Serverless function deployment and invocation
- **AI**: OpenRouter via project Model Gateway key setup, chat completions, image/video/audio generation, embeddings, and model discovery
- **Real-time**: WebSocket connections, subscriptions, event publishing
- **Payments**: Stripe Checkout/Billing Portal and Razorpay Orders/Subscriptions
- **Deployments**: Frontend app deployment to InsForge hosting

**Key distinction**: Backend infrastructure uses the CLI skill. Most client integration uses `@insforge/sdk`; new AI features use OpenRouter APIs with an API key set up by `npx -y @insforge/cli ai setup`.

</details>

<details>
<summary><strong>insforge-cli</strong> - InsForge CLI Project Management</summary>

Create and manage InsForge projects from the command line. This skill provides comprehensive guidance for:

- **Authentication**: Login (OAuth/password), logout, session verification
- **Project Management**: Create, link, and inspect projects
- **Database**: Raw SQL execution, schema inspection, RLS, import/export
- **Edge Functions**: Deploy, invoke, and view function source
- **Storage**: Bucket and object management (upload, download, list)
- **Deployments**: Frontend app deployment and status tracking
- **AI**: OpenRouter key setup with `npx -y @insforge/cli ai setup`
- **Payme
