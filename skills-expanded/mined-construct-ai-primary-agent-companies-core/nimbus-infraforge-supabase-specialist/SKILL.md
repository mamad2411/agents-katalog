---
name: nimbus-infraforge-supabase-specialist
description: Routes Supabase database operations, SQL generation, authentication troubleshooting, and performance optimization to the Supabase specialist.
company: infraforge-ai
---

# Supabase Database Specialist

## Overview
This skill routes all Supabase-related database operations to Nimbus, the specialized Supabase Database Specialist for InfraForge AI. Nimbus handles comprehensive database operations including advanced SQL generation, authentication troubleshooting, schema management, and performance optimization.

## Routing Criteria

Route to this skill when:
- Supabase API operations (REST, GraphQL, Realtime)
- PostgreSQL operations within Supabase environment
- Authentication and RLS policy issues
- SQL query generation and optimization
- Database schema design and management
- Performance monitoring and tuning
- Backup/restore operations
- Security policy implementation
- Integration troubleshooting
- Testing database operations

## Capabilities

### Supabase API Operations
- REST API query construction and optimization
- GraphQL schema design and query development
- Real-time subscription management
- Storage API file operations
- Edge Functions development and deployment

### SQL Generation & Testing
- Dynamic SQL query generation
- Complex join and aggregation queries
- Stored procedure development
- Query performance testing and validation
- Schema testing and validation

### Authentication & Security
- Supabase Auth flow implementation
- Row Level Security policy creation
- JWT token management and validation
- OAuth provider integration
- Custom authentication middleware

### Performance Optimization
- Query execution plan analysis
- Index strategy development
- Connection pooling configuration
- Caching strategy implementation
- Resource usage optimization

## Related Skills

- `database-infraforge-database-infrastructure` - Core database infrastructure
- `postgres-infraforge-postgresql` - PostgreSQL administration
- `mobile-api-infraforge-mobile-api-integration` - API integration support

## Examples

### SQL Generation
```sql
-- Generated complex query with joins and aggregations
SELECT
  p.id,
  p.title,
  p.created_at,
  u.email as author_email,
  COUNT(c.id) as comment_count,
  AVG(c.rating) as avg_rating
FROM posts p
JOIN users u ON p.author_id = u.id
LEFT JOIN comments c ON p.id = c.post_id
WHERE p.published = true
  AND p.created_at >= $1
GROUP BY p.id, p.title, p.created_at, u.email
HAVING COUNT(c.id) > 0
ORDER BY p.created_at DESC;
```

### RLS Policy Implementation
```sql
-- Implement row-level security for multi-tenant application
ALTER TABLE tenant_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Tenants access own data" ON tenant_data
FOR ALL USING (
  tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
);

CREATE POLICY "Service role full access" ON tenant_data
FOR ALL USING (
  auth.role() = 'service_role'
);
```

### Performance Optimization
```sql
-- Index creation for query optimization
CREATE INDEX CONCURRENTLY idx_users_active_created
ON users(is_active, created_at DESC)
WHERE is_active = true;

-- Query performance analysis
EXPLAIN (ANALYZE, BUFFERS)
SELECT u.*, p.title
FROM users u
JOIN posts p ON u.id = p.author_id
WHERE u.is_active = true
  AND p.created_at > CURRENT_DATE - INTERVAL '30 days'
ORDER BY p.created_at DESC
LIMIT 50;
```

### Authentication Flow
```sql
-- Supabase auth user creation with profile
INSERT INTO auth.users (
  instance_id,
  id,
  aud,
  role,
  email,
  encrypted_password,
  email_confirmed_at,
  invited_at,
  confirmation_token,
  confirmation_sent_at,
  recovery_token,
  recovery_sent_at,
  email_change_token_new,
  email_change,
  email_change_sent_at,
  last_sign_in_at,
  raw_app_meta_data,
  raw_user_meta_data,
  is_super_admin,
  created_at,
  updated_at,
  phone,
  phone_confirmed_at,
  phone_change,
  phone_change_token,
  phone_change_sent_at,
  email_change_token_current,
  email_change_confirm_status,
  banned_until,
  reauthentication_token,
  reauthentication_sent_at
) VALUES (
  '00000000-0000-0000-0000-000000000000',
  gen_random_uuid(),
  'authenticated',
  'authenticated',
  'user@example.com',
  crypt('password', gen_salt('bf')),
  NOW(),
  NULL,
  '',
  NULL,
  '',
  NULL,
  '',
  '',
  NULL,
  NULL,
  '{"provider": "email", "providers": ["email"]}',
  '{"full_name": "John Doe"}',
  FALSE,
  NOW(),
  NOW(),
  NULL,
  NULL,
  '',
  '',
  NULL,
  '',
  0,
  NULL,
  '',
  NULL
);
```

---

*This skill routes to Nimbus, the Supabase Database Specialist, for comprehensive database operations and SQL development support across the Paperclip ecosystem.*