---
name: package-system-design
description: Design and implement the capability package runtime — manifest validation, dependency resolution, migration orchestration, package signing/trust, node definition contracts, and surface registration for the Software Synthesis OS package-registry service.
triggers: [package registry, capability package, package manifest, package install, package migration, package signing, node definition, surface registration, package dependency, package trust]
---

# SKILL: Package System Design

## Core Principle
A package is the unit of capability. It declares what nodes it provides, what surfaces it renders, what permissions it needs, and how it migrates. The registry enforces contracts. The runtime installs, resolves, and migrates — never executes domain logic.

---

## 1. Package Manifest Contract

Every package must ship a `manifest.json` at its root conforming to this schema:

```typescript
interface PackageManifest {
  $schema: string;                  // "https://your-os.dev/schemas/package-manifest/v1.json"
  packageKey: string;               // globally unique e.g. "engine.document"
  name: string;
  version: string;                  // semver
  publisher: string;                // "first-party" | org slug
  kind: PackageKind;
  description: string;
  minPlatformVersion?: string;      // semver range
  dependencies: string[];           // packageKey list
  entrypoints: {
    templates?: string[];
    surfaces?: string[];
    commands?: string[];
  };
  nodes: string[];                  // node definition keys
  permissions: PermissionKey[];
  policies: {
    dangerousWritesRequireApproval?: boolean;
    defaultRoles?: string[];
    rateLimit?: { runsPerHour: number };
  };
  ui: {
    preferredLayout?: 'split' | 'full' | 'sidebar' | 'canvas';
    supportsCanvas?: boolean;
    supportsOperatorMode?: boolean;
    icon?: string;
    color?: string;
  };
  migrations: MigrationEntry[];
  trust?: TrustMetadata;
}

type PackageKind =
  | 'engine.document'
  | 'engine.sheet'
  | 'engine.email'
  | 'engine.media'
  | 'compound'
  | 'connector'
  | 'policy'
  | 'primitive';

interface MigrationEntry {
  from: string;   // semver
  to: string;     // semver
  script: string; // migration script key
}

interface TrustMetadata {
  signature: string;       // Ed25519 signature over manifest content
  signerKeyId: string;     // public key fingerprint
  signedAt: string;        // ISO 8601
}
```

---

## 2. Manifest Validation

```typescript
// registry/manifest-validator.ts

import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import semver from 'semver';

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

export function validateManifest(raw: unknown): ManifestValidationResult {
  // Step 1: JSON schema check
  const schemaValid = ajv.compile(MANIFEST_JSON_SCHEMA)(raw);
  if (!schemaValid) {
    return { valid: false, errors: ajv.errorsText(ajv.errors) };
  }

  const manifest = raw as PackageManifest;

  // Step 2: semver validity
  if (!semver.valid(manifest.version)) {
    return { valid: false, errors: `Invalid semver: "${manifest.version}"` };
  }

  // Step 3: packageKey format
  if (!/^[a-z][a-z0-9._-]+$/.test(manifest.packageKey)) {
    return { valid: false, errors: `Invalid packageKey format: "${manifest.packageKey}"` };
  }

  // Step 4: node keys are non-empty unique list
  const nodeSet = new Set(manifest.nodes);
  if (nodeSet.size !== manifest.nodes.length) {
    return { valid: false, errors: 'Duplicate node keys in manifest.nodes' };
  }

  // Step 5: migration chain must be ordered
  for (const m of manifest.migrations) {
    if (!semver.valid(m.from) || !semver.valid(m.to)) {
      return { valid: false, errors: `Migration entry has invalid semver: ${m.from} -> ${m.to}` };
    }
    if (!semver.lt(m.from, m.to)) {
      return { valid: false, errors: `Migration "from" must be less than "to": ${m.from} -> ${m.to}` };
    }
  }

  return { valid: true };
}
```

---

## 3. Dependency Resolution

Resolve a full install set from direct dependencies using a topological sort with cycle detection.

```typescript
// registry/dependency-resolver.ts

export interface PackageIndex {
  get(packageKey: string): PackageManifest | null;
}

export interface ResolveResult {
  order: string[];          // install order (dependencies first)
  missing: string[];
  cycles: string[][];
}

export function resolveDependencies(
  roots: string[],
  index: PackageIndex
): ResolveResult {
  const missing: string[] = [];
  const cycles: string[][] = [];
  const visited = new Set<string>();
  const inStack = new Set<string>();
  const order: string[] = [];

  function visit(key: string, stack: string[]) {
    if (inStack.has(key)) {
      const cycleStart = stack.indexOf(key);
      cycles.push(stack.slice(cycleStart).concat(key));
      return;
    }
    if (visited.has(key)) return;

    const manifest = index.get(key);
    if (!manifest) {
      missing.push(key);
      return;
    }

    inStack.add(key);
    for (const dep of manifest.dependencies) {
      visit(dep, [...stack, key]);
    }
    inStack.delete(key);
    visited.add(key);
    order.push(key);
  }

  for (const root of roots) visit(root, []);
  return { order, missing, cycles };
}
```

---

## 4. Node Definition Contract

Each package ships node definitions. The graph compiler loads these to resolve port types.

```typescript
// packages/node-definition.ts

export interface NodeDefinitionContract {
  key: string;               // e.g. "rfp.ingest" — unique within package
  displayName: string;
  description: string;
  nodeType: NodeDefinition['type'];
  inputs: Record<string, NodePortSpec>;
  outputs: Record<string, NodePortSpec>;
  configSchema: JSONSchema;  // JSON schema for node.config
  executor: string;          // registered executor key for runtime-service
  supportsStreaming?: boolean;
  estimatedCostUnit?: string;
}

export interface NodePortSpec {
  type: string;              // "dataset" | "artifactRef" | "text" | "json" | "stream"
  label: string;
  optional?: boolean;
  default?: unknown;
}
```

**Loading node definitions:**
```typescript
// registry/node-registry.ts

export class NodeRegistry {
  private map = new Map<string, NodeDefinitionContract>();

  registerPackage(packageKey: string, defs: NodeDefinitionContract[]) {
    for (const def of defs) {
      const fullKey = `${packageKey}/${def.key}`;
      if (this.map.has(fullKey)) {
        throw new Error(`Node definition conflict: "${fullKey}" already registered`);
      }
      this.map.set(fullKey, def);
    }
  }

  get(packageKey: string, nodeKey: string): NodeDefinitionContract | null {
    return this.map.get(`${packageKey}/${nodeKey}`) ?? null;
  }

  getOutputType(packageKey: string, nodeKey: string, portName: string): string | null {
    return this.get(packageKey, nodeKey)?.outputs[portName]?.type ?? null;
  }
}
```

---

## 5. Surface Registration

Packages register named surface definitions that the surface-compiler resolves.

```typescript
// packages/surface-definition.ts

export interface SurfaceDefinition {
  key: string;               // e.g. "proposal_workspace"
  displayName: string;
  packageKey: string;
  layout: 'split' | 'full' | 'sidebar' | 'canvas' | 'tabbed';
  panels: SurfacePanelSpec[];
  supportsOperatorMode: boolean;
  supportedModes: ('builder' | 'operator' | 'viewer')[];
}

export interface SurfacePanelSpec {
  id: string;
  kind: 'editor' | 'card' | 'list' | 'canvas' | 'chat' | 'form';
  nodeRef?: string;          // binds to graph node
  title?: string;
  width?: 'narrow' | 'medium' | 'wide' | 'full';
  collapsible?: boolean;
}

// registry/surface-registry.ts
export class SurfaceRegistry {
  private map = new Map<string, SurfaceDefinition>();

  register(def: SurfaceDefinition) {
    const key = `${def.packageKey}/${def.key}`;
    if (this.map.has(key)) throw new Error(`Surface conflict: "${key}"`);
    this.map.set(key, def);
  }

  resolve(packageKey: string, surfaceKey: string): SurfaceDefinition | null {
    return this.map.get(`${packageKey}/${surfaceKey}`) ?? null;
  }
}
```

---

## 6. Migration Orchestration

Migrations run when a workspace upgrades a package version.

```typescript
// registry/migration-runner.ts

export interface MigrationContext {
  workspaceId: string;
  packageKey: string;
  fromVersion: string;
  toVersion: string;
  db: DatabaseClient;
}

export interface MigrationScript {
  key: string;
  up(ctx: MigrationContext): Promise<void>;
  dry_run?(ctx: MigrationContext): Promise<string[]>; // returns change descriptions
}

export class MigrationRunner {
  private scripts = new Map<string, MigrationScript>();

  register(script: MigrationScript) {
    this.scripts.set(script.key, script);
  }

  async migrate(ctx: MigrationContext, entries: MigrationEntry[]): Promise<MigrationReport> {
    const chain = this.buildChain(ctx.fromVersion, ctx.toVersion, entries);
    const results: MigrationStepResult[] = [];

    for (const entry of chain) {
      const script = this.scripts.get(entry.script);
      if (!script) throw new Error(`Migration script not found: "${entry.script}"`);

      try {
        await ctx.db.transaction(async (tx) => {
          await script.up({ ...ctx, db: tx });
          await tx.execute(
            `INSERT INTO package_migration_history (workspace_id, package_key, from_version, to_version, script, migrated_at)
             VALUES ($1, $2, $3, $4, $5, now())`,
            [ctx.workspaceId, ctx.packageKey, entry.from, entry.to, entry.script]
          );
        });
        results.push({ entry, status: 'success' });
      } catch (err) {
        results.push({ entry, status: 'failed', error: String(err) });
        break; // stop on first failure
      }
    }

    return { workspaceId: ctx.workspaceId, steps: results };
  }

  private buildChain(from: string, to: string, entries: MigrationEntry[]): MigrationEntry[] {
    // Build path from `from` to `to` through migration entries
    const chain: MigrationEntry[] = [];
    let current = from;

    while (current !== to) {
      const next = entries.find(e => e.from === current);
      if (!next) throw new Error(`No migration path from "${current}" to "${to}"`);
      chain.push(next);
      current = next.to;
    }

    return chain;
  }
}
```

---

## 7. Package Signing and Trust

```typescript
// registry/package-trust.ts
import { createVerify } from 'crypto';

export type TrustLevel = 'first_party' | 'verified_partner' | 'community' | 'untrusted';

export function verifyPackageSignature(
  manifest: PackageManifest,
  publicKeyPem: string
): boolean {
  const { trust, ...manifestWithoutTrust } = manifest;
  if (!trust) return false;

  const content = JSON.stringify(manifestWithoutTrust, null, 2);
  const verifier = createVerify('Ed25519');
  verifier.update(content);

  try {
    return verifier.verify(publicKeyPem, trust.signature, 'base64');
  } catch {
    return false;
  }
}

export function resolveTrustLevel(manifest: PackageManifest, trustedKeyIds: Set<string>): TrustLevel {
  if (manifest.publisher === 'first-party') return 'first_party';
  if (manifest.trust && trustedKeyIds.has(manifest.trust.signerKeyId)) return 'verified_partner';
  if (manifest.trust) return 'community';
  return 'untrusted';
}
```

---

## 8. Install Flow

```
POST /packages/install
  → validateManifest()
  → resolveDependencies()
  → verifyPackageSignature()
  → resolveTrustLevel()
  → if trust < required_level → BLOCK with reason
  → upsert capability_packages + capability_package_versions
  → upsert workspace_package_installs
  → registerNodes() into NodeRegistry
  → registerSurfaces() into SurfaceRegistry
  → runMigrations() if upgrading
  → emit PackageInstalledEvent → graph-service, surface-compiler
```

---

## 9. Checklist

Before shipping any package registry change:
- [ ] Manifest JSON schema is versioned in `/schemas/package-manifest/vN.json`
- [ ] Dependency resolver detects cycles and returns them — never silently ignores
- [ ] Migration runner uses transactions — partial migrations must roll back
- [ ] Migration history table exists and is append-only
- [ ] `verifyPackageSignature` is called for all non-first-party packages
- [ ] `untrusted` packages are blocked by default (configurable per org)
- [ ] Node key conflicts across packages throw hard errors on startup
- [ ] Package install is idempotent — installing same version twice is a no-op
