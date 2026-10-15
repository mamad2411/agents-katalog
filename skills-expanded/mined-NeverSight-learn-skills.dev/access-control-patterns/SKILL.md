---
name: access-control-patterns
description: "Enterprise-grade access control patterns to prevent broken access control, IDOR, tenant data leaks, privilege escalation, and admin route exposure. Covers RBAC, ABAC, ownership checks, multi-tenant scoping, policy middleware, row-level security, and audit logging for Node.js, Cloudflare Workers, Laravel, and Python. Use when protecting routes, implementing roles, reviewing authorization, or fixing OWASP A01 findings."
version: "1.0"
---

# Access Control Patterns

Prevent users from accessing data or actions they are not allowed to access. Broken Access Control is OWASP A01 because it is the most common serious web vulnerability: user A can read user B's invoice, change another tenant's settings, or call an admin endpoint by guessing an ID.

## The Rule

**Authentication proves who the user is. Authorization proves what the user can do. You need both on every protected operation.**

## Core Principles

1. **Deny by default** -- no route is public unless explicitly marked public
2. **Check authorization server-side** -- never trust hidden buttons or client checks
3. **Scope every query by user or tenant** -- never fetch by raw ID alone
4. **Use centralized policies** -- avoid scattered `if (user.role === 'admin')` checks
5. **Separate roles from permissions** -- roles are bundles, permissions are actions
6. **Audit sensitive decisions** -- log denied and privileged actions

## Vulnerable Patterns

### IDOR: Insecure Direct Object Reference

BAD:

```typescript
app.get('/api/invoices/:id', async (req, res) => {
  const invoice = await db.invoice.findUnique({ where: { id: req.params.id } });
  res.json(invoice); // Any logged-in user can read any invoice by guessing ID
});
```

GOOD:

```typescript
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await db.invoice.findFirst({
    where: {
      id: req.params.id,
      tenantId: req.user.tenantId,
    },
  });

  if (!invoice) return res.status(404).json({ error: 'Not found' });
  res.json(invoice);
});
```

Return `404`, not `403`, when resource existence should not be revealed.

## Enterprise Authorization Model

Use this decision order for every protected operation:

1. Is the user authenticated?
2. Is the account active and not suspended?
3. Is the user inside the tenant/workspace being accessed?
4. Does the user have the required permission?
5. Does the resource belong to the user's tenant?
6. Are there object-level conditions? (owner, assigned user, approval state)
7. Should the action be audit logged?

## RBAC Pattern

```typescript
type Role = 'owner' | 'admin' | 'member' | 'viewer';
type Permission =
  | 'invoice:read'
  | 'invoice:create'
  | 'invoice:update'
  | 'invoice:delete'
  | 'user:invite'
  | 'billing:manage';

const ROLE_PERMISSIONS: Record<Role, Permission[]> = {
  owner: ['invoice:read', 'invoice:create', 'invoice:update', 'invoice:delete', 'user:invite', 'billing:manage'],
  admin: ['invoice:read', 'invoice:create', 'invoice:update', 'user:invite'],
  member: ['invoice:read', 'invoice:create'],
  viewer: ['invoice:read'],
};

function hasPermission(role: Role, permission: Permission): boolean {
  return ROLE_PERMISSIONS[role]?.includes(permission) ?? false;
}
```

## ABAC Pattern

Attribute-Based Access Control adds object-level conditions.

```typescript
interface AuthContext {
  userId: string;
  tenantId: string;
  role: Role;
  permissions: Permission[];
}

interface Invoice {
  id: string;
  tenantId: string;
  ownerId: string;
  status: 'draft' | 'sent' | 'paid';
}

function canUpdateInvoice(user: AuthContext, invoice: Invoice): boolean {
  if (invoice.tenantId !== user.tenantId) return false;
  if (!hasPermission(user.role, 'invoice:update')) return false;
  if (invoice.status === 'paid') return false;
  if (user.role === 'member' && invoice.ownerId !== user.userId) return false;
  return true;
}
```

## Node.js / Express Middleware

```typescript
function requireAuth(req: Request, res: Response, next: NextFunction) {
  if (!req.user) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  next();
}

function requirePermission(permission: Permission) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    if (!hasPermission(req.user.role, permission)) {
      auditLog({
        event: 'access.denied',
        userId: req.user.id,
        tenantId: req.user.tenantId,
        permission,
        path: req.path,
      });

      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
}

app.patch('/api/invoices/:id', requirePermission('invoice:update'), async (req, res) => {
  const invoice = await db.invoice.findFirst({
    where: { id: req.params.id, tenantId: req.user.tenantId },
  });

  if (!invoice) return res.status(404).json({ error: 'Not found' });
  if (!canUpdateInvoice(req.user, invoice)) return res.status(403).json({ error: 'Forbidden' });

  const updated = await db.invoice.update({
    where: { id: invoice.id },
    data: req.body,
  });

  res.json(updated);
});
```

## Cloudflare Workers Pattern

```typescript
interface AuthContext {
  userId: string;
  tenantId: string;
  role: Role;
}

async function requireAuth(request: Request, env: Env): Promise<AuthContext> {
  const token = request.headers.get('Authorization')?.replace('Bearer ', '');
  if (!token) throw new HttpError(401, 'Authentication required');

  const session = await verifySession(token, env);
  if (!session) throw new HttpError(401, 'Invalid session');

  return session;
}

function requirePermission(auth: AuthContext, permission: Permission): void {
  if (!hasPermission(auth.role, permission)) {
    throw new HttpError(403, 'Forbidden');
  }
}

async function getTenantScopedInvoice(db: D1Database, auth: AuthContext, invoiceId: string) {
  return db.prepare(
    'SELECT * FROM invoices WHERE id = ? AND tenant_id = ?'
  ).bind(invoiceId, auth.tenantId).first();
}
```

## Laravel Policy Pattern

```php
// app/Policies/InvoicePolicy.php
class InvoicePolicy
{
    public function view(User $user, Invoice $invoice): bool
    {
        return $user->tenant_id === $invoice->tenant_id
            && $user->hasPermission('invoice:read');
    }

    public function update(User $user, Invoice $invoice): bool
    {
        return $user->tenant_id === $invoice->tenant_id
            && $user->hasPermission('invoice:update')
            && $invoice->status !== 'paid';
    }
}

// Controller
public function update(Request $request, Invoice $invoice)
{
    $this->authorize('update', $invoice);
    $invoice->update($request->validated());
    return response()->json($invoice);
}
```

Always add tenant scoping to route model binding or global scopes:

```php
protected static function booted()
{
    static::addGlobalScope('tenant', function (Builder $builder) {
        if (auth()->check()) {
            $builder->where('tenant_id', auth()->user()->tenant_id);
        }
    });
}
```

## Python FastAPI Pattern

```python
from fastapi import Depends, HTTPException

def require_permission(permission: str):
    def dependency(user: User = Depends(current_user)):
        if permission not in user.permissions:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return dependency

@app.patch("/invoices/{invoice_id}")
async def update_invoice(
    invoice_id: str,
    payload: InvoiceUpdate,
    user: User = Depends(require_permission("invoice:update")),
):
    invoice = await db.fetch_one(
        "SELECT * FROM invoices WHERE id = :id AND tenant_id = :tenant_id",
        {"id": invoice_id, "tenant_id": user.tenant_id},
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")

    if invoice["status"] == "paid":
        raise HTTPException(status_code=403, detail="Forbidden")

    return await update_invoice_record(invoice_id, payload)
```

## Database Row-Level Security

For PostgreSQL, enforce tenant isolation at the database layer too.

```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON invoices
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Set this per request/transaction
SELECT set_config('app.current_tenant_id', 'tenant-uuid-here', true);
```

RLS does not replace application authorization, but it reduces blast radius when developers forget a tenant filter.

## Admin Route Protection

Admin routes require stronger controls:

- Separate `admin:*` permissions from user roles
- Require MFA for admin actions
- Require recent authentication for sensitive changes
- Audit log all admin reads and writes
- Never rely on frontend route hiding
- Block admin access from unknown IPs where possible

```typescript
function requireAdminAction(action: Permission) {
  return [
    requireAuth,
    requirePermission(action),
    requireRecentMfa({ maxAgeMinutes: 15 }),
    auditAdminAction(action),
  ];
}
```

## Access Control Audit Checklist

- [ ] Every protected route has authentication middleware
- [ ] Every sensitive action has permission checks
- [ ] Every resource query is scoped by `tenantId` or `userId`
- [ ] Raw ID lookups are not used for tenant-owned resources
- [ ] Users cannot access another tenant's data by changing URL IDs
- [ ] Frontend checks are duplicated server-side
- [ ] Admin routes require explicit admin permissions
- [ ] Admin actions require MFA or recent re-authentication
- [ ] Denied access attempts are audit logged
- [ ] Resource existence is not leaked when unauthorized
- [ ] Roles and permissions are centrally defined
- [ ] Database RLS or equivalent guardrails exist for multi-tenant apps
- [ ] Tests cover cross-tenant access attempts

## Required Tests

Every multi-tenant project must include these tests:

```typescript
it('prevents user from reading another tenant invoice', async () => {
  const tenantAInvoice = await createInvoice({ tenantId: 'tenant-a' });
  const tenantBUser = await createUser({ tenantId: 'tenant-b' });

  const response = await request(app)
    .get(`/api/invoices/${tenantAInvoice.id}`)
    .set('Authorization', `Bearer ${tokenFor(tenantBUser)}`);

  expect(response.status).toBe(404);
});
```

## PDPA 2024 Consequence

Broken access control is the fastest way to create a reportable personal data breach. If one customer can access another customer's personal data, the developer failed to implement basic authorization and tenant isolation. Under PDPA 2024 Seksyen 5(1) and 5(2), this can trigger up to RM1,000,000 fine or 3 years imprisonment.
