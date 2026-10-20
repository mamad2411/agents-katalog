---
name: azure-app-service-deploy
description: Deploy, configure, scale, and troubleshoot Azure App Service web apps, function apps, and deployment slots.
---

# Azure App Service Deploy

Deploy, configure, scale, and troubleshoot Azure App Service web apps, function apps, and deployment slots.

## Trigger

Use this skill when the user asks to:
- Deploy code or containers to Azure App Service or Azure Functions
- Configure app settings, connection strings, or custom domains
- Set up deployment slots and slot swaps (blue/green, canary)
- Configure autoscale rules or scale up/out manually
- Diagnose slow responses, crashes, or deployment failures
- Set up CI/CD pipelines (GitHub Actions, Azure DevOps) targeting App Service
- Configure VNet integration, private endpoints, or access restrictions
- Enable or query App Service diagnostics and Application Insights

## Instructions

### Before advising

Ask (or infer) the following if not already provided:

1. **App type** — Web App, Function App, Container App, or Static Web App?
2. **Runtime** — .NET, Node.js, Python, Java, PHP, or custom container?
3. **OS** — Windows or Linux?
4. **Deployment method** — zip deploy, container, GitHub Actions, Azure DevOps, local git?
5. **Environment** — dev / staging / prod (drives SKU, slot, and redundancy decisions)?

### App Service Plan SKU guidance

| SKU | Use case | Features |
|-----|---------|----------|
| F1 / D1 | Dev/test only | Shared compute, no custom domain SSL, no slots |
| B1–B3 | Low-traffic prod, dev | Dedicated compute, custom domains, manual scale |
| S1–S3 | Standard prod | Auto-scale, 5 slots, daily backups, Traffic Manager |
| P1v3–P3v3 | High-traffic prod | Premium hardware, 20 slots, VNet integration |
| P0v3 | Cost-optimised premium | Cheaper entry to v3 hardware |
| EP1–EP3 | Functions (Elastic Premium) | Always-warm, VNet, unlimited scale |
| Y1 | Functions (Consumption) | Pay-per-execution, cold starts |
| I1v2–I3v2 | Isolated (ASE) | Dedicated VNet, max isolation |

Always recommend P1v3 or higher for production workloads — B-series has no autoscale.

### Configuration rules

**App settings vs connection strings**

- Use **App Settings** for all non-secret config (feature flags, URLs, thresholds)
- Use **Connection Strings** only when the framework expects that specific slot (Entity Framework, ADO.NET)
- All secrets must reference Key Vault: `@Microsoft.KeyVault(SecretUri=https://kv-name.vault.azure.net/secrets/my-secret/)`
- Never hardcode secrets in app settings — they appear in deployment logs

**Slot-sticky settings**

Mark settings that must not travel with a swap as slot-sticky:

```bash
az webapp config appsettings set \
  --name myapp --resource-group myRG \
  --settings ASPNETCORE_ENVIRONMENT=Production \
  --slot-settings ASPNETCORE_ENVIRONMENT   # sticky to this slot
```

**Always-on**

Enable `alwaysOn` for any app that:
- Receives background jobs or timer triggers
- Must not cold-start on first request after idle
- Runs on B1 or higher (F1 does not support it)

### Deployment methods

**Zip deploy (CI/CD recommended)**
```bash
# Build artifact first, then deploy
az webapp deployment source config-zip \
  --resource-group myRG \
  --name myapp \
  --src ./publish.zip
```

**Container deploy**
```bash
az webapp config container set \
  --name myapp \
  --resource-group myRG \
  --container-image-name myregistry.azurecr.io/myapp:latest \
  --container-registry-url https://myregistry.azurecr.io
```

**Slot deploy + swap (zero-downtime)**
```bash
# Deploy to staging slot
az webapp deployment source config-zip \
  --resource-group myRG \
  --name myapp \
  --slot staging \
  --src ./publish.zip

# Warm up staging (hit health endpoint)
curl https://myapp-staging.azurewebsites.net/health

# Swap staging → production
az webapp deployment slot swap \
  --resource-group myRG \
  --name myapp \
  --slot staging \
  --target-slot production
```

### GitHub Actions template (zip deploy)

```yaml
name: Deploy to Azure App Service

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.x'

      - name: Build and publish
        run: |
          dotnet publish ./src/MyApp -c Release -o ./publish

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ vars.APP_NAME }}
          slot-name: staging
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: ./publish
```

For OIDC (recommended over publish profiles):

```yaml
      - name: Azure login
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy
        uses: azure/webapps-deploy@v3
        with:
          app-name: myapp
          slot-name: staging
          package: ./publish
```

### Autoscale rules

Scale out when CPU > 70% for 10 minutes; scale in when CPU < 30% for 10 minutes:

```bash
# Create autoscale profile
az monitor autoscale create \
  --resource-group myRG \
  --resource myapp \
  --resource-type Microsoft.Web/serverfarms \
  --name autoscale-myapp \
  --min-count 2 --max-count 10 --count 2

# Scale-out rule
az monitor autoscale rule create \
  --resource-group myRG \
  --autoscale-name autoscale-myapp \
  --condition "CpuPercentage > 70 avg 10m" \
  --scale out 1

# Scale-in rule
az monitor autoscale rule create \
  --resource-group myRG \
  --autoscale-name autoscale-myapp \
  --condition "CpuPercentage < 30 avg 10m" \
  --scale in 1
```

Always set a minimum of ≥ 2 instances for production to survive zone failures.

### VNet integration

```bash
# Integrate app with a subnet (requires P1v3+ or S1+)
az webapp vnet-integration add \
  --resource-group myRG \
  --name myapp \
  --vnet myVNet \
  --subnet snet-app

# Route all outbound traffic through VNet (required to reach private endpoints)
az webapp config appsettings set \
  --resource-group myRG \
  --name myapp \
  --settings WEBSITE_VNET_ROUTE_ALL=1
```

### Access restrictions

```bash
# Block all public traffic; allow only a specific IP
az webapp config access-restriction add \
  --resource-group myRG \
  --name myapp \
  --rule-name AllowOffice \
  --action Allow \
  --ip-address 203.0.113.0/24 \
  --priority 100

# Allow only Azure Front Door (header-based)
az webapp config access-restriction add \
  --resource-group myRG \
  --name myapp \
  --rule-name AllowFrontDoor \
  --action Allow \
  --service-tag AzureFrontDoor.Backend \
  --priority 200
```

### Troubleshooting

**Deployment failures**
1. Check Kudu console: `https://<appname>.scm.azurewebsites.net`
2. View deployment logs: `az webapp log deployment show --name myapp --resource-group myRG`
3. Stream live logs: `az webapp log tail --name myapp --resource-group myRG`

**App crashes / 500 errors**
1. Enable application logging: `az webapp log config --name myapp --resource-group myRG --application-logging filesystem --level error`
2. Stream logs: `az webapp log tail --name myapp --resource-group myRG --filter Error`
3. Check Application Insights: query `AppExceptions | order by TimeGenerated desc | take 20`
4. Check process explorer in Kudu for memory/CPU spikes

**Cold starts (Functions)**
- Switch from Consumption (Y1) to Elastic Premium (EP1)
- Enable `WEBSITE_RUN_FROM_PACKAGE=1` to reduce startup time
- Use `functionapp keys list` to ensure host is warmed: `az functionapp keys list --name myfunc --resource-group myRG`

**Slot swap issues**
- Check slot-sticky settings — misconfigured sticky settings are the #1 cause of post-swap failures
- Enable swap with preview: `az webapp deployment slot swap --action preview` then verify before completing
- Check health check endpoint returns 200 before swap completes

## References

- [App Service CLI & config cheatsheet](./references/appservice-cheatsheet.md)
- [Deployment patterns: slots, containers, CI/CD](./references/deployment-patterns.md)
- [Scaling and monitoring](./references/scaling-and-monitoring.md)
- Official docs: https://learn.microsoft.com/en-us/azure/app-service/
