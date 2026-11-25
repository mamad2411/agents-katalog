---
name: client-config-manager
description: >
  Use when managing per-company environment variables, configuring branding
  settings, managing feature flags, or handling company-specific customizations.
  This skill manages all client-specific configuration.
---

# Client Config Manager - SaaSForge AI

## Overview
Client Config Manager specializes in managing company-specific configurations within the SaaSForge AI multi-tenant platform, handling environment variables, branding, and feature flags.

## When to Use
- When setting up initial environment for new client
- When updating per-company environment variables
- When configuring client branding (logos, colors)
- When managing feature flags per client
- When validating configuration before deployment
- **Don't use when:** Deployment execution is needed (use Deployment-Orchestrator), or Render service changes needed (use Render-Service-Manager)

## Core Procedures

### New Client Configuration
1. **Template Selection** - Select appropriate config template
2. **Environment Variables** - Set all required environment variables
3. **Branding Setup** - Configure client branding settings
4. **Feature Flags** - Set initial feature flags based on plan
5. **Validation** - Validate all configurations
6. **Documentation** - Document client configuration for reference

### Environment Variable Management
1. **Variable Catalog** - Maintain list of all environment variables per client
2. **Value Updates** - Update values with proper validation
3. **Secret Management** - Coordinate secrets with DevOps Engineer
4. **Sync Check** - Ensure variables sync with deployments
5. **Audit Trail** - Log all configuration changes

### Branding Configuration
1. **Brand Assets** - Upload logo, favicon, brand colors
2. **CSS Customization** - Apply custom CSS for client
3. **Email Templates** - Customize branded email templates
4. **Domain Setup** - Configure custom domain settings
5. **SSL Verification** - Ensure SSL certificates active

### Feature Flag Management
1. **Flag Creation** - Create feature flags for new capabilities
2. **Client Assignment** - Enable flags for specific clients
3. **Gradual Rollout** - Percentage-based feature rollouts
4. **Monitoring** - Track feature usage and performance
5. **Cleanup** - Remove deprecated flags

## Configuration Structure

### Per-Company Config
```yaml
client_config:
  company_name: "Company A"
  subdomain: "companya"
  plan: "enterprise"
  features:
    - advanced_analytics
    - custom_workflows
    - api_access
  branding:
    logo_url: "https://..."
    primary_color: "#0066CC"
    custom_css: true
```

### Environment Variables Template
```bash
# Core
DATABASE_URL=postgres://...
REDIS_URL=redis://...
NODE_ENV=production

# Client-Specific
CLIENT_NAME=CompanyA
CLIENT_SUBDOMAIN=companya
CLIENT_PLAN=enterprise

# Branding
BRAND_LOGO_URL=https://...
BRAND_PRIMARY_COLOR=#0066CC
```

## Integration Points

### With Deployment-Orchestrator
- Coordinate config deployments with code deployments
- Provide configuration status for deployment checks
- Execute config-only deployments

### With Render-Service-Manager
- Deploy environment variables to Render services
- Verify service configuration after updates
- Coordinate domain setup

### With Platform-Architect
- Ensure config meets security standards
- Validate compliance configurations
- Review architecture-specific configs

## Error Handling

### Invalid Configuration
- **Response:** Reject invalid values, provide clear error messages
- **Validation:** Run pre-deployment validation checks
- **Fallback:** Use previous working configuration

### Secret Exposure
- **Response:** Immediately revoke exposed secrets
- **Notification:** Alert DevOps Engineer and Onboard Master
- **Remediation:** Rotate secrets and update environment

## Success Metrics
- Configuration accuracy: 100%
- Config deployment success: ≥99%
- Average config change time: <5 minutes
- Client satisfaction: ≥95%
