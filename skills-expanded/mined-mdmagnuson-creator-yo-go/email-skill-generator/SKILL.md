---
name: email-skill-generator
description: "Generate a project-specific transactional email skill. Use when a project has email: true or email integration (resend, sendgrid, etc). Triggers on: generate email skill, create email patterns, email-skill-generator."
type: meta
generates: transactional-email
trigger:
  capability: email
  integration: [resend, sendgrid, postmark, ses]
---

# Email Skill Generator

Generate a project-specific `transactional-email` skill that documents exactly how to send emails in THIS project.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing email implementation
3. Ask clarifying questions about email patterns
4. Generate `docs/skills/transactional-email/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Look for:
- `capabilities.email: true`
- Integration with name "resend", "sendgrid", "postmark", or "ses"

---

## Step 2: Analyze Existing Email Implementation

```bash
# Find email-related files
find . -type f \( -name "*email*" -o -name "*mail*" \) | grep -v node_modules

# Find email templates
find . -type d -name "*email*" | grep -v node_modules
find . -type f -name "*.tsx" | xargs grep -l "email\|Email" | head -10

# Find email sending logic
grep -r "resend\|sendgrid\|nodemailer\|ses\.\|postmark" --include="*.ts" | head -10
```

---

## Step 3: Clarifying Questions

```
I found the following email patterns:

Email Provider: [detected]
Email Templates: [React Email / HTML / Plain text]
Template Location: [path if found]

Please confirm or correct:

1. What email provider do you use?
   A. Resend
   B. SendGrid
   C. Postmark
   D. AWS SES
   E. Nodemailer (SMTP)
   F. Other: [specify]

2. How are email templates built?
   A. React Email components
   B. HTML templates
   C. Plain text
   D. Third-party template builder
   E. Mix

3. What types of emails do you send?
   A. Authentication (welcome, password reset)
   B. Transactional (receipts, confirmations)
   C. Notifications (alerts, updates)
   D. All of the above
```

---

## Step 4: Generate the Skill

Create `docs/skills/transactional-email/SKILL.md`:

```markdown
---
name: transactional-email
description: "Send transactional emails in [PROJECT_NAME]"
project-specific: true
generated-by: email-skill-generator
generated-at: [DATE]
---

# Transactional Email Skill

How to send emails in this project.

---

## Quick Reference

| Task | Function |
|------|----------|
| Send email | `sendEmail({ to, subject, template, data })` |
| Create template | Add to `[TEMPLATES_PATH]` |
| Preview template | `npm run email:dev` |

---

## Architecture

- **Provider:** [PROVIDER_NAME] (e.g., Resend)
- **Templates:** [React Email / HTML / Plain text]
- **Templates Path:** `[TEMPLATES_PATH]`
- **Email Client:** `[EMAIL_CLIENT_PATH]`

---

## Key Files

| File | Purpose |
|------|---------|
| `[EMAIL_CLIENT_PATH]` | Email client initialization |
| `[TEMPLATES_PATH]` | Email templates |
| `[SEND_EMAIL_PATH]` | sendEmail utility |

---

## Sending an Email

### Basic Usage

\`\`\`typescript
import { sendEmail } from '@/lib/email'

await sendEmail({
  to: 'user@example.com',
  subject: 'Welcome to [Project]',
  template: 'welcome',
  data: {
    name: 'John',
    loginUrl: 'https://app.example.com/login',
  },
})
\`\`\`

### Implementation

\`\`\`typescript
// [EMAIL_CLIENT_PATH]
import { Resend } from 'resend'

export const resend = new Resend(process.env.RESEND_API_KEY)

// [SEND_EMAIL_PATH]
import { resend } from '@/lib/email/client'
import { renderTemplate } from '@/lib/email/templates'

interface SendEmailOptions {
  to: string | string[]
  subject: string
  template: string
  data: Record<string, unknown>
}

export async function sendEmail({ to, subject, template, data }: SendEmailOptions) {
  const html = await renderTemplate(template, data)
  
  const { error } = await resend.emails.send({
    from: process.env.EMAIL_FROM!,
    to,
    subject,
    html,
  })
  
  if (error) {
    console.error('Email send error:', error)
    throw error
  }
}
\`\`\`

---

## Creating a Template

### With React Email

\`\`\`typescript
// [TEMPLATES_PATH]/welcome.tsx
import {
  Body,
  Container,
  Head,
  Heading,
  Html,
  Link,
  Preview,
  Text,
} from '@react-email/components'

interface WelcomeEmailProps {
  name: string
  loginUrl: string
}

export default function WelcomeEmail({ name, loginUrl }: WelcomeEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Welcome to [Project Name]</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={h1}>Welcome, {name}!</Heading>
          <Text style={text}>
            Thanks for signing up. Get started by logging in:
          </Text>
          <Link href={loginUrl} style={button}>
            Log In
          </Link>
        </Container>
      </Body>
    </Html>
  )
}

const main = {
  backgroundColor: '#f6f9fc',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
}

const container = {
  backgroundColor: '#ffffff',
  margin: '0 auto',
  padding: '40px',
  borderRadius: '8px',
}

const h1 = {
  color: '#1a1a1a',
  fontSize: '24px',
  fontWeight: '600',
}

const text = {
  color: '#4a4a4a',
  fontSize: '16px',
  lineHeight: '24px',
}

const button = {
  backgroundColor: '#5046e5',
  borderRadius: '6px',
  color: '#fff',
  display: 'inline-block',
  padding: '12px 24px',
  textDecoration: 'none',
}
\`\`\`

### Rendering Templates

\`\`\`typescript
// [TEMPLATES_PATH]/index.ts
import { render } from '@react-email/render'
import WelcomeEmail from './welcome'
import PasswordResetEmail from './password-reset'
// ... other templates

const templates = {
  welcome: WelcomeEmail,
  'password-reset': PasswordResetEmail,
}

export async function renderTemplate(
  template: keyof typeof templates,
  data: Record<string, unknown>
) {
  const Template = templates[template]
  if (!Template) throw new Error(\`Unknown template: \${template}\`)
  
  return render(<Template {...data} />)
}
\`\`\`

---

## Common Email Types

### Welcome Email

\`\`\`typescript
await sendEmail({
  to: user.email,
  subject: 'Welcome to [Project]!',
  template: 'welcome',
  data: {
    name: user.name,
    loginUrl: \`\${process.env.NEXT_PUBLIC_URL}/login\`,
  },
})
\`\`\`

### Password Reset

\`\`\`typescript
await sendEmail({
  to: user.email,
  subject: 'Reset your password',
  template: 'password-reset',
  data: {
    name: user.name,
    resetUrl: \`\${process.env.NEXT_PUBLIC_URL}/reset-password?token=\${token}\`,
    expiresIn: '1 hour',
  },
})
\`\`\`

### Invoice/Receipt

\`\`\`typescript
await sendEmail({
  to: user.email,
  subject: \`Receipt for your payment - \${invoice.number}\`,
  template: 'receipt',
  data: {
    customerName: user.name,
    invoiceNumber: invoice.number,
    amount: formatCurrency(invoice.amount),
    date: formatDate(invoice.created_at),
    lineItems: invoice.line_items,
  },
})
\`\`\`

---

## Preview Templates Locally

\`\`\`bash
# Start email dev server
npm run email:dev
# or
npx email dev --dir [TEMPLATES_PATH]
\`\`\`

This opens a browser with live preview of all templates.

---

## Environment Variables

\`\`\`bash
# .env.local
RESEND_API_KEY=re_...
EMAIL_FROM="[Project Name] <noreply@example.com>"
\`\`\`

---

## Testing

### Unit Testing

\`\`\`typescript
// Mock the email client in tests
jest.mock('@/lib/email', () => ({
  sendEmail: jest.fn(),
}))

// Verify email was sent
expect(sendEmail).toHaveBeenCalledWith({
  to: 'user@example.com',
  subject: 'Welcome to [Project]!',
  template: 'welcome',
  data: expect.objectContaining({ name: 'John' }),
})
\`\`\`

### Manual Testing

Use Resend's test mode or catch-all address during development.

---

## Checklist

When adding a new email:

- [ ] Create template component
- [ ] Add to templates index
- [ ] Add TypeScript types for data
- [ ] Preview in email dev server
- [ ] Test on multiple email clients
- [ ] Handle send errors gracefully
```

---

## Step 5: Update project.json

Add to `skills.generated[]`:

```json
{
  "name": "transactional-email",
  "generatedFrom": "email-skill-generator",
  "generatedAt": "2026-02-20"
}
```
