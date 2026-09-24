# Repo Referensi: microsoft/azure-skills

Repo: https://github.com/microsoft/azure-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/microsoft_azure-skills
API: curl "localhost:27126/repos/readme?name=microsoft_azure-skills"
Dibuat: 2026-09-16

## Cuplikan README
# microsoft/azure-skills

Source: https://github.com/microsoft/azure-skills
Fetched: 2026-09-16

## README
# Azure Skills Plugin

Azure work is not just a code problem. It is a decision problem: which service fits this app, what needs to be validated before deployment, which tools should run, and what guardrails matter. The Azure Skills Plugin packages Azure expertise and MCP-backed execution together so compatible coding agents can do real Azure work instead of giving generic cloud advice.

**[Explore the Azure Skills site](https://microsoft.github.io/azure-skills/)**
**[Landing page maintenance guide](landing-page/README.md)**

**[Install the plugin](#install-in-60-seconds)**

## One install, three layers of capability

### Azure skills: the brain

This plugin ships **curated Azure skills** that teach an agent how Azure work gets done. They provide workflows, decision trees, and guardrails for scenarios such as:

- **Build, deploy, and evolve** with `azure-prepare`, `azure-validate`, `azure-deploy`, `azure-upgrade`, `azure-enterprise-infra-planner`, `azure-hosted-copilot-sdk`, `azure-kubernetes`, and `airunway-aks-setup`
- **Troubleshoot, monitor, and govern** with `azure-diagnostics`, `appinsights-instrumentation`, `azure-compliance`, `azure-resource-lookup`, and `azure-quotas`
- **Optimize architecture and cost** with `azure-cost`, `azure-compute`, `azure-resource-visualizer`, and `azure-cloud-migrate`
- **Work across data, AI, identity, and platform services** with `azure-ai`, `azure-aigateway`, `azure-storage`, `azure-kusto`, `azure-messaging`, `azure-rbac`, `entra-app-registration`, and `microsoft-foundry`

### Azure MCP Server: the hands

The plugin wires in the **Azure MCP Server**, which gives your agent **200+ structured tools across 40+ Azure services**. That is the execution layer for listing resources, checking prices, querying logs, diagnosing issues, and driving real Azure workflows.

### Foundry MCP: the AI specialist

The plugin also includes **Foundry MCP** for Microsoft Foundry scenarios such as model discovery, model deployment, and agent workflows.

## Why this plugin is different

This is not a prompt pack. It is a packaged Azure capability layer:

- **Skills** teach the agent when to use Azure workflows and what to avoid.
- **MCP tools** let the agent act on live Azure and Foundry resources.
- **The plugin** keeps the guidance layer and execution layer aligned in one install.
- **Multi-host support** lets you use the same Azure capa
