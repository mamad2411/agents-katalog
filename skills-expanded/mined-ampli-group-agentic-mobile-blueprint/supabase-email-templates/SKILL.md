# Supabase Email Templates

Customize Supabase Auth email templates for local development and production.

## When to use

- Create custom email templates (password reset, confirmation, etc.)
- Test templates locally with Inbucket
- Deploy templates to production

## Template Types

Use exact names: `recovery`, `confirmation`, `invite`, `magic_link`, `email_change`

## Setup

**1. Create template** at `supabase/templates/emails/recovery.html`:

```html
<body style="margin: 0; padding: 0;">
  <table style="max-width: 600px; margin: 0 auto;">
    <tr><td style="padding: 40px; text-align: center;">
      <h1>Your App</h1>
      <a href="{{ .ConfirmationURL }}" 
         style="display: inline-block; padding: 12px 32px; 
                background: #2563eb; color: #fff; border-radius: 6px;">
        Reset Password
      </a>
    </td></tr>
  </table>
</body>
```

**2. Configure** in `supabase/config.toml` (path relative to project root):

```toml
[auth.email.template.recovery]
subject = "Reset your password"
content_path = "./supabase/templates/emails/recovery.html"
```

**3. Restart** auth container:

```bash
docker restart supabase_auth_<project-name>
```

## Local Testing

**Test with Inbucket** at http://localhost:54324:

```bash
# Send test email
curl -X POST 'http://localhost:54321/auth/v1/recover' \
  -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# View at http://localhost:54324
```

## Template Variables

Available: `{{ .ConfirmationURL }}`, `{{ .Email }}`, `{{ .SiteURL }}`, `{{ .Token }}`

## Troubleshooting

**Default template still showing?**
- After `supabase start`, always restart auth: `docker restart supabase_auth_<project>`
- Send new test email (old emails cached)

**Template not found (404)?**
- After renaming files: `supabase stop && supabase start`
- Then restart auth container

**Template parse errors?**
- Use inline CSS only
- Avoid `rgba()` in CSS values
- Use hex colors only

## Production Deployment

Templates deploy via GitHub Actions using `deploy-templates.js`:

```yaml
- name: Deploy Email Templates
  run: node ./supabase/templates/deploy-templates.js
  env:
    SUPABASE_PROJECT_REF: ${{ secrets.SUPABASE_PROJECT_ID }}
    SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
```

## Best Practices

Use inline CSS only, max 600px width, table layouts, test in Inbucket first
