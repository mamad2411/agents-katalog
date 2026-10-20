# Custom Agent Configurations

This directory contains custom agent configurations for the Snipe Web3 trading platform. Custom agents are specialized AI assistants that have deep knowledge of specific aspects of the codebase.

## Quick Start

1. **Copy the template**: Start with `custom-agent-template.agent.md`
2. **Customize it**: Fill in the name, description, and specific instructions
3. **Test locally**: Use the [Copilot CLI](https://gh.io/customagents/cli) to test your agent
4. **Deploy**: Merge your agent file to the main branch to make it available

## Available Templates

### `custom-agent-template.agent.md`
Comprehensive template for creating specialized agents with:
- Platform-specific knowledge (Firebase, Wallet integration, Admin system)
- Code patterns and best practices
- Common issues and solutions
- Testing checklist

## Example Agent Ideas

### Firebase Expert Agent
**Purpose**: Specialized in Firebase Firestore operations, real-time listeners, security rules
**Name**: `firebase-expert.agent.md`

### Wallet Specialist Agent
**Purpose**: Expert in multi-wallet provider integration (11 providers supported)
**Name**: `wallet-specialist.agent.md`

### Admin System Agent
**Purpose**: Role-based access control, permissions, and admin features
**Name**: `admin-specialist.agent.md`

### UI/UX Agent
**Purpose**: React component development, Tailwind styling, responsive design
**Name**: `ui-specialist.agent.md`

### Security Agent
**Purpose**: Security best practices, authentication, authorization, data validation
**Name**: `security-specialist.agent.md`

## Creating Your Own Agent

### Step 1: Copy the Template
```bash
cp custom-agent-template.agent.md my-new-agent.agent.md
```

### Step 2: Edit the Frontmatter
```yaml
---
name: Your Agent Name
description: Brief description of what this agent does
---
```

### Step 3: Customize the Content
- Define the agent's expertise areas
- Add specific knowledge relevant to the domain
- Include code examples and patterns
- Add troubleshooting tips

### Step 4: Test Locally
```bash
# Install Copilot CLI if not already installed
gh copilot agent test my-new-agent.agent.md
```

### Step 5: Deploy
```bash
git add .github/agents/my-new-agent.agent.md
git commit -m "Add custom agent for [domain]"
git push
```

## Agent Naming Convention

Use descriptive names that indicate the agent's specialization:
- `{domain}-{role}.agent.md` format
- Examples:
  - `firebase-expert.agent.md`
  - `wallet-specialist.agent.md`
  - `admin-permissions.agent.md`
  - `testing-automation.agent.md`

## Best Practices

### Do's ✅
- Keep agents focused on specific domains
- Include practical code examples
- Reference key files and documentation
- Provide common issue solutions
- Test thoroughly before deploying

### Don'ts ❌
- Don't create overly broad agents
- Don't duplicate information across agents
- Don't include sensitive information (credentials, keys)
- Don't forget to update when the codebase changes

## Platform-Specific Context

All agents should be aware of:

### Architecture
- **Frontend**: React 18 + Vite in `Onchainweb/`
- **Backend**: Firebase (Firestore + Auth)
- **Fallback**: localStorage when Firebase unavailable
- **Legacy**: Express/MongoDB (deprecated)

### Key Files
- `src/lib/firebase.js` - Firebase singleton
- `src/config/firebase.config.js` - Configuration
- `src/lib/walletConnect.jsx` - Wallet integration
- `src/lib/adminAuth.js` - Admin system
- `src/lib/errorHandling.js` - Error utilities

### Critical Patterns
- Always check `isFirebaseAvailable` before Firebase ops
- Use `onSnapshot` listeners, never poll
- Clean up listeners in useEffect
- Support 11 wallet providers
- Never reinitialize Firebase singleton

## Maintenance

### When to Update Agents
- When architectural changes occur
- When new patterns are established
- When common issues are identified
- When dependencies are updated

### Review Process
1. Test agent locally
2. Ensure it follows platform patterns
3. Verify no sensitive information
4. Get peer review if making significant changes

## Resources

- [GitHub Copilot Custom Agents Documentation](https://gh.io/customagents/config)
- [Copilot CLI Guide](https://gh.io/customagents/cli)
- [Snipe Platform Documentation](../../README.md)
- [Quick Start Guide](../../QUICK_START_GUIDE.md)
- [Backend Replacement Guide](../../BACKEND_REPLACEMENT.md)
- [Admin User Guide](../../ADMIN_USER_GUIDE.md)

## Need Help?

- Check the [main documentation](../../README.md)
- Review the [custom agent template](custom-agent-template.agent.md)
- Open an issue if you encounter problems
- Ask in the team chat for guidance

---

**Remember**: Custom agents are powerful tools that help maintain consistency and quality across the codebase. Take time to create thoughtful, focused agents that genuinely help development.
