---
name: bicep-best-practices
description: Apply portable Azure Bicep practices when authoring or reviewing modules, parameters, resource references, role-assignment names, tags, comments, linter settings, builds, or deployment what-if previews.
---

# Bicep Best Practices

Keep Bicep interfaces small, derive stable configuration close to its source, and prove each change with compiler and deployment-preview evidence.

## Minimize parameters

Before adding a parameter, inspect every caller and ask why the value varies. Keep it only when callers legitimately supply different values that cannot be derived from stable inputs or shared environment facts.

- Derive predictable resource names from a small identity such as application, environment, and region.
- Put genuinely environment-specific input values in parameter files.
- Read facts shared by every deployment in an environment from one typed configuration object or module.
- Avoid forwarding a parameter unchanged through layers merely to reach a leaf module.
- Retain an explicit override only for a documented, real exception.

Centralize repeated derivations once:

```bicep
param environment string
param workload string

var environmentUpper = toUpper(environment)
var configuration = environmentConfiguration[environment]
var resourceName = '${workload}-${environmentUpper}'
```

Do not scatter the same casing, naming, region, or resource-group calculation throughout a file.

## Preserve shared and resource-specific tags

Use the shared tag set directly when a resource adds nothing. When it has genuine resource-specific tags, preserve both sets with `union()`:

```bicep
tags: union(sharedTags, {
  resourceRole: 'api'
})
```

Never replace `union(sharedTags, {...})` with the base object during a parameter cleanup; the added keys are deployment data.

## Derive Azure resource IDs

Prefer an `existing` symbolic resource when Bicep can express the owning scope clearly:

```bicep
resource loggingWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: workspaceName
  scope: resourceGroup(loggingResourceGroupName)
}

var workspaceResourceId = loggingWorkspace.id
```

Use `resourceId()` when a cross-resource-group or cross-subscription ID is easier and unambiguous to derive:

```bicep
var workspaceResourceId = resourceId(
  loggingResourceGroupName,
  'Microsoft.OperationalInsights/workspaces',
  workspaceName
)
```

Pass the ARM resource ID, not a service-specific customer identifier. Do not parameterize an ID that is stable and derivable from known scope and name facts.

## Keep `guid()` inputs compile-time resolvable

Resource names must be available at deployment start. For role assignments and similar resources, give `guid()` only parameters, constants, and IDs from resources whose identities are already known:

```bicep
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(scopeResource.id, principalId, roleDefinitionId)
  scope: scopeResource
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      roleDefinitionId
    )
  }
}
```

Do not use `guid(module.outputs.principalId, ...)` in a resource name. A module output is deployment-time data and triggers BCP120. Resolve the output in the caller, then pass it into a child module whose naming expression can use that parameter.

## Use the linter as a design gate

Keep one intentional `bicepconfig.json` at the appropriate repository root. Enable the core linter and elevate safety-relevant rules, especially secure input handling and nested deployment scoping. Do not disable a rule simply to make a build green; correct the model or document a narrow, reviewed exception.

Compile every touched entry point:

```bash
az bicep build --file path/to/main.bicep
```

Treat linter diagnostics and compiler warnings as review input even when the command exits successfully.

## Preview deployment behavior

For a behavior change, run the narrowest applicable Azure deployment `what-if` at the real target scope after the build succeeds. For a refactor intended to be behavior-neutral, require zero unexpected resource-property drift.

Use a command appropriate to the deployment scope, for example:

```bash
az deployment group what-if \
  --resource-group <resource-group> \
  --template-file path/to/main.bicep \
  --parameters path/to/environment.bicepparam
```

Review destructive replacements, deletes, scope changes, and tag loss explicitly. A successful build proves syntax and type validity; it does not prove safe deployment behavior.

## Keep comments concise

Prefer clear symbolic names and `@description` metadata. Keep a comment only when it explains a non-obvious safety constraint, active blocker, or future action. Remove comments that restate the code, preserve obsolete history, expose internal identifiers, or narrate authorship.

## Review checklist

- Every parameter has demonstrated caller variation.
- Repeated shared environment facts have one source of truth.
- Stable names and IDs are derived instead of threaded through modules.
- `union()` preserves resource-specific tags.
- Cross-domain references use `existing` resources or a correctly scoped `resourceId()`.
- Every `guid()` input used for a resource name is compile-time resolvable; no BCP120 remains.
- The linter and `az bicep build` pass for every touched entry point.
- Deployment `what-if` has no unexplained changes.
- Comments meet the concise safety-and-intent bar.
