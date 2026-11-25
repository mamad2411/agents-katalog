---
name: create-pulumi-stack
description: "Create or extend Pulumi stacks and programs. Use when: adding resources to an existing stack, creating a new stack, adding ComponentResources, wiring stack references, updating stack config."
---

# Create Pulumi Stack/Component

Creates or extends Pulumi Python programs following the Contoso infrastructure hierarchy.

## When to Use
- Adding a new Azure resource to an existing stack
- Creating a new Pulumi stack (networking, security, app, etc.)
- Adding a shared `ComponentResource` class used across stacks
- Wiring cross-stack references via `pulumi.StackReference`
- Adding or rotating stack config/secrets

## Hierarchy

```
infra/
  components/                   ← shared ComponentResource classes
  networking/                   ← networking stack (deployed first)
    Pulumi.yaml
    Pulumi.dev.yaml / Pulumi.prod.yaml
    __main__.py
    requirements.txt
  security/                     ← depends on networking
    ...
  app/                          ← depends on networking + security
    ...
```

## Procedure

### Task A: Add a New Resource to an Existing Stack

#### 1. Check `infra/components/` for a matching `ComponentResource`

#### 2. Import and instantiate in `__main__.py`

```python
import sys
from pathlib import Path

import pulumi

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components.key_vault import KeyVaultComponent

cfg = pulumi.Config("contoso")
env = cfg.require("environment")
prefix = cfg.require("prefix")
rg = cfg.require("resourceGroupName")
tenant_id = cfg.require("tenantId")

default_tags = {
    "environment": env,
    "managed_by": "Pulumi",
    "product": "security",
}

kv = KeyVaultComponent("keyvault", {
    "resource_group_name": rg,
    "location": pulumi.Config("azure-native").require("location"),
    "tenant_id": tenant_id,
    "default_tags": default_tags,
})

pulumi.export("vault_id", kv.vault.id)
pulumi.export("vault_uri", kv.vault.properties.vault_uri)
```

#### 3. Preview

```bash
pulumi preview --stack dev
```

### Task B: Create a New Stack

#### 1. `Pulumi.yaml`

```yaml
name: contoso-{stack-name}
runtime: python
description: "{Description} for Contoso Azure platform"
```

#### 2. `Pulumi.dev.yaml`

```yaml
config:
  azure-native:location: westeurope
  contoso:environment: "dev"
  contoso:prefix: "app-weu-dev"
  contoso:resourceGroupName: "rg-{stack}-dev-weu"
  contoso:tenantId: "00000000-0000-0000-0000-000000000000"
```

#### 3. `requirements.txt`

```
pulumi>=3.0.0,<4.0.0
pulumi-azure-native>=2.0.0,<3.0.0
```

#### 4. Set secrets

```bash
pulumi config set --secret --stack dev contoso:clientSecret <value>
```

#### 5. Preview and deploy

```bash
pulumi preview --stack dev
pulumi up --stack dev --yes
```

### Task C: Add a Shared ComponentResource

Create `infra/components/{name}.py`:

```python
import pulumi
import pulumi_azure_native as azure

class {Name}Component(pulumi.ComponentResource):
    def __init__(self, name: str, args: dict, opts: pulumi.ResourceOptions | None = None):
        super().__init__("contoso:components:{Name}", name, {}, opts)
        child_opts = pulumi.ResourceOptions(parent=self)

        # Create resources here using child_opts
        # ...

        self.register_outputs({...})
```

## Cross-Stack Reference Pattern

```python
networking = pulumi.StackReference(f"contoso/networking/{env}")
vnet_id = networking.get_output("vnet_id")

# Handle None for plan-time safety:
subnet_id = networking.get_output("subnets").apply(
    lambda s: (s or {}).get("default", "/subscriptions/mock/subnets/default")
)
```

## Validation Checklist
1. `pulumi preview --stack dev` passes with no unintended replacements
2. All required config keys are set in `Pulumi.{env}.yaml` or as secrets
3. Stack references handle `None` for plan-time safety
4. No secrets or account IDs hardcoded in `__main__.py`
5. New outputs exported from `__main__.py`
6. `ComponentResource` registered with `self.register_outputs({...})`
