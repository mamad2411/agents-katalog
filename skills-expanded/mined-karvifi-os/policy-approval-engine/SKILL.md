---
name: policy-approval-engine
description: Design and implement the policy-service — approval routing, dangerous action gates, role resolution, fine-grained permissions, audit policies, and policy-as-code patterns for the Software Synthesis OS governance layer.
triggers: [policy engine, approval engine, approval routing, dangerous action gate, role resolution, fine-grained permissions, audit policy, policy-as-code, policy-service, governance, approval workflow]
---

# SKILL: Policy / Approval Engine

## Core Principle
Policy is code, not configuration. Policies are evaluated at call time — never cached across permission changes. The policy-service is the only authority on whether an action is allowed. No service bypasses it. Deny by default.

---

## 1. Core Policy Model

```typescript
// policy-service/types.ts

export interface PolicyEvaluationRequest {
  actor: Actor;
  action: PolicyAction;
  resource: PolicyResource;
  context: PolicyContext;
}

export interface Actor {
  userId: string;
  roles: string[];
  organizationId: string;
  workspaceId: string;
}

export interface PolicyAction {
  kind: ActionKind;
  nodeDefinition?: string;    // for node execution actions
  packageKey?: string;
  exportFormat?: string;
}

export type ActionKind =
  | 'graph.read'
  | 'graph.write'
  | 'graph.publish'
  | 'graph.execute'
  | 'artifact.read'
  | 'artifact.write'
  | 'artifact.export'
  | 'artifact.delete'
  | 'package.install'
  | 'package.uninstall'
  | 'node.execute'
  | 'email.send'
  | 'approval.create'
  | 'approval.resolve'
  | 'member.invite'
  | 'billing.manage';

export interface PolicyResource {
  type: 'graph' | 'artifact' | 'package' | 'workspace' | 'organization';
  id: string;
  ownerId?: string;
  workspaceId?: string;
}

export interface PolicyContext {
  installedPackages: string[];
  requestedNodeDefinition?: string;
  pendingApprovalId?: string;
  ipAddress?: string;
}

export type PolicyDecision = 'allow' | 'deny' | 'require_approval';

export interface PolicyResult {
  decision: PolicyDecision;
  reason: string;
  approvalRequirements?: ApprovalRequirement;
  auditRequired: boolean;
}
```

---

## 2. Role Hierarchy

```typescript
// policy-service/roles.ts

export type OrgRole = 'org_owner' | 'org_admin' | 'org_member';
export type WorkspaceRole = 'owner' | 'editor' | 'reviewer' | 'viewer';

// What each workspace role can do
const ROLE_PERMISSIONS: Record<WorkspaceRole, Set<ActionKind>> = {
  owner: new Set([
    'graph.read', 'graph.write', 'graph.publish', 'graph.execute',
    'artifact.read', 'artifact.write', 'artifact.export', 'artifact.delete',
    'package.install', 'package.uninstall',
    'node.execute', 'email.send',
    'approval.create', 'approval.resolve',
    'member.invite', 'billing.manage',
  ]),
  editor: new Set([
    'graph.read', 'graph.write', 'graph.execute',
    'artifact.read', 'artifact.write', 'artifact.export',
    'node.execute',
    'approval.create',
  ]),
  reviewer: new Set([
    'graph.read',
    'artifact.read', 'artifact.export',
    'approval.resolve',
  ]),
  viewer: new Set([
    'graph.read',
    'artifact.read',
  ]),
};

export function resolveEffectiveRole(
  actor: Actor,
  resourceWorkspaceId: string
): WorkspaceRole | null {
  // Org owners get owner in all workspaces
  if (actor.roles.includes('org_owner')) return 'owner';

  // Find workspace-specific role from actor.roles (format: "ws:<workspaceId>:<role>")
  for (const role of actor.roles) {
    const match = role.match(/^ws:([^:]+):(.+)$/);
    if (match && match[1] === resourceWorkspaceId) {
      return match[2] as WorkspaceRole;
    }
  }

  return null;
}

export function hasPermission(role: WorkspaceRole, action: ActionKind): boolean {
  return ROLE_PERMISSIONS[role]?.has(action) ?? false;
}
```

---

## 3. Dangerous Action Gates

Some actions always require an extra approval layer regardless of role.

```typescript
// policy-service/dangerous-actions.ts

interface DangerousActionPolicy {
  definition: RegExp | string;
  requiresApproval: boolean;
  approvalRoles: WorkspaceRole[];
  auditRequired: boolean;
  reason: string;
}

const DANGEROUS_ACTION_POLICIES: DangerousActionPolicy[] = [
  {
    definition: /email\.send/,
    requiresApproval: true,
    approvalRoles: ['owner'],
    auditRequired: true,
    reason: 'Email sending requires owner approval to prevent accidental sends.',
  },
  {
    definition: /data\.delete/,
    requiresApproval: true,
    approvalRoles: ['owner'],
    auditRequired: true,
    reason: 'Data deletion is irreversible and requires owner approval.',
  },
  {
    definition: /export\.publish_external/,
    requiresApproval: true,
    approvalRoles: ['owner', 'editor'],
    auditRequired: true,
    reason: 'Publishing externally requires approval.',
  },
  {
    definition: 'billing.manage',
    requiresApproval: false,
    approvalRoles: [],
    auditRequired: true,
    reason: 'Billing changes are always audited.',
  },
];

export function checkDangerousAction(
  action: PolicyAction
): DangerousActionPolicy | null {
  const subject = action.nodeDefinition ?? action.kind;

  for (const policy of DANGEROUS_ACTION_POLICIES) {
    if (typeof policy.definition === 'string') {
      if (subject === policy.definition) return policy;
    } else {
      if (policy.definition.test(subject)) return policy;
    }
  }

  return null;
}
```

---

## 4. Policy Evaluator

```typescript
// policy-service/evaluator.ts

export function evaluatePolicy(req: PolicyEvaluationRequest): PolicyResult {
  const { actor, action, resource, context } = req;

  // Step 1: Resolve effective role
  const role = resolveEffectiveRole(actor, resource.workspaceId ?? actor.workspaceId);

  if (!role) {
    return {
      decision: 'deny',
      reason: 'Actor has no role in this workspace.',
      auditRequired: false,
    };
  }

  // Step 2: Check basic permission for action kind
  if (!hasPermission(role, action.kind)) {
    return {
      decision: 'deny',
      reason: `Role "${role}" does not have permission for action "${action.kind}".`,
      auditRequired: false,
    };
  }

  // Step 3: Check dangerous action policies
  const dangerousPolicy = checkDangerousAction(action);
  if (dangerousPolicy?.requiresApproval) {
    const canSelfApprove = dangerousPolicy.approvalRoles.includes(role);
    if (!canSelfApprove) {
      return {
        decision: 'require_approval',
        reason: dangerousPolicy.reason,
        approvalRequirements: {
          requiredApproverRoles: dangerousPolicy.approvalRoles,
          timeoutHours: 48,
        },
        auditRequired: true,
      };
    }
  }

  // Step 4: Package-level trust gates
  if (action.kind === 'node.execute' && action.packageKey) {
    const pkg = context.installedPackages.find(p => p === action.packageKey);
    if (!pkg && role !== 'owner') {
      return {
        decision: 'deny',
        reason: `Package "${action.packageKey}" is not installed in this workspace.`,
        auditRequired: false,
      };
    }
  }

  return {
    decision: 'allow',
    reason: `Role "${role}" has permission for action "${action.kind}".`,
    auditRequired: dangerousPolicy?.auditRequired ?? false,
  };
}
```

---

## 5. Approval Routing

```typescript
// policy-service/approval-router.ts

export interface ApprovalRequirement {
  requiredApproverRoles: WorkspaceRole[];
  timeoutHours: number;
}

export interface ApprovalRequest {
  workspaceId: string;
  requestedBy: string;
  approvalType: string;
  targetType: string;
  targetId: string;
  requirements: ApprovalRequirement;
  metadata?: Record<string, unknown>;
}

export async function routeApproval(
  request: ApprovalRequest,
  db: DatabaseClient
): Promise<string> {  // returns approvalId
  // Find all eligible approvers
  const eligibleApprovers = await db.query<{ userId: string }>(
    `SELECT om.user_id
     FROM organization_members om
     JOIN workspaces w ON w.organization_id = om.organization_id
     WHERE w.id = $1
       AND om.role = ANY($2)
       AND om.user_id != $3`,
    [request.workspaceId, request.requirements.requiredApproverRoles, request.requestedBy]
  );

  if (eligibleApprovers.length === 0) {
    throw new Error('No eligible approvers found for this action.');
  }

  // Create approval record
  const [approval] = await db.query<{ id: string }>(
    `INSERT INTO approvals (workspace_id, approval_type, target_type, target_id, requested_by, status)
     VALUES ($1, $2, $3, $4, $5, 'pending')
     RETURNING id`,
    [request.workspaceId, request.approvalType, request.targetType, request.targetId, request.requestedBy]
  );

  // Create approval steps (one per eligible approver, requires any one to resolve)
  for (const [idx, approver] of eligibleApprovers.entries()) {
    await db.execute(
      `INSERT INTO approval_steps (approval_id, approver_user_id, step_order, status)
       VALUES ($1, $2, $3, 'pending')`,
      [approval.id, approver.userId, idx]
    );
  }

  // Emit notification event
  await emitApprovalRequestedEvent({
    approvalId: approval.id,
    workspaceId: request.workspaceId,
    requestedBy: request.requestedBy,
    approverUserIds: eligibleApprovers.map(a => a.userId),
    timeoutHours: request.requirements.timeoutHours,
  });

  return approval.id;
}

export async function resolveApproval(
  approvalId: string,
  resolverId: string,
  decision: 'approved' | 'rejected',
  comment: string | null,
  db: DatabaseClient
): Promise<void> {
  await db.transaction(async (tx) => {
    // Update the specific step
    await tx.execute(
      `UPDATE approval_steps
       SET status = $1, comment = $2, acted_at = now()
       WHERE approval_id = $3 AND approver_user_id = $4`,
      [decision, comment, approvalId, resolverId]
    );

    // Update approval master status
    await tx.execute(
      `UPDATE approvals SET status = $1, resolved_at = now() WHERE id = $2`,
      [decision, approvalId]
    );
  });

  // Emit approval resolved event → runtime-service to resume or cancel run
  await emitApprovalResolvedEvent({ approvalId, decision });
}
```

---

## 6. Audit Logging

```typescript
// policy-service/auditor.ts

export interface AuditEvent {
  organizationId: string;
  workspaceId: string;
  actorId: string;
  actionKind: ActionKind;
  resourceType: string;
  resourceId: string;
  decision: PolicyDecision;
  metadata?: Record<string, unknown>;
  ipAddress?: string;
  timestamp: string;
}

export async function recordAuditEvent(
  event: AuditEvent,
  db: DatabaseClient
): Promise<void> {
  await db.execute(
    `INSERT INTO audit_events
     (organization_id, workspace_id, actor_id, action_kind, resource_type, resource_id, decision, metadata, ip_address, created_at)
     VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, now())`,
    [
      event.organizationId,
      event.workspaceId,
      event.actorId,
      event.actionKind,
      event.resourceType,
      event.resourceId,
      event.decision,
      JSON.stringify(event.metadata ?? {}),
      event.ipAddress ?? null,
    ]
  );
}
```

---

## 7. Policy Service HTTP API

```typescript
// policy-service/routes.ts

// POST /policy/evaluate
// Body: PolicyEvaluationRequest
// Returns: PolicyResult
router.post('/policy/evaluate', async (req, res) => {
  const actor = extractActor(req);           // from JWT
  const { action, resource, context } = req.body;

  const result = evaluatePolicy({ actor, action, resource, context });

  if (result.auditRequired) {
    await recordAuditEvent({
      organizationId: actor.organizationId,
      workspaceId: actor.workspaceId,
      actorId: actor.userId,
      actionKind: action.kind,
      resourceType: resource.type,
      resourceId: resource.id,
      decision: result.decision,
      ipAddress: req.ip,
      timestamp: new Date().toISOString(),
    });
  }

  res.json(result);
});

// POST /policy/approval
// Body: ApprovalRequest
// Returns: { approvalId: string }
router.post('/policy/approval', requireAuth, async (req, res) => {
  const approvalId = await routeApproval(req.body, db);
  res.json({ approvalId });
});

// POST /policy/approval/:id/resolve
router.post('/policy/approval/:id/resolve', requireAuth, async (req, res) => {
  await resolveApproval(req.params.id, req.actor.userId, req.body.decision, req.body.comment, db);
  res.json({ ok: true });
});
```

---

## 8. Package Policy Defaults

Each package manifest can declare policy defaults that get applied at install time:

```typescript
// policy-service/package-policy-installer.ts

export function installPackagePolicies(
  manifest: PackageManifest,
  workspaceId: string,
  db: DatabaseClient
) {
  const { policies } = manifest;

  if (policies.dangerousWritesRequireApproval) {
    // Register all write node definitions from this package as requiring approval
    for (const nodeKey of manifest.nodes) {
      if (nodeKey.includes('write') || nodeKey.includes('send') || nodeKey.includes('delete')) {
        registerNodeApprovalPolicy(workspaceId, manifest.packageKey, nodeKey, db);
      }
    }
  }
}
```

---

## 9. Checklist

Before shipping policy-service changes:
- [ ] `evaluatePolicy` is a pure function — no I/O, no side effects (auditing happens outside)
- [ ] All deny decisions include a human-readable `reason` shown to the user
- [ ] Dangerous action definitions use regex patterns — never exact string matches only
- [ ] Approval routing fails fast if no eligible approvers exist (don't create orphan approvals)
- [ ] Audit events are written AFTER policy evaluation — never block the response
- [ ] `resolveApproval` uses a transaction — step + master status update is atomic
- [ ] Approval timeouts are enforced by a background job (not on-demand)
- [ ] Policy evaluation endpoint is rate-limited per actor (max 200 req/min)
- [ ] All audit events include `ipAddress` for compliance exports
