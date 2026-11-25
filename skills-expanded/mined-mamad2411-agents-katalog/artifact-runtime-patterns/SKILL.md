---
name: artifact-runtime-patterns
description: Design and implement the artifact-service — durable output system with revision chains, lineage tracking, export bundles, share links, and blob storage coordination for the Software Synthesis OS.
triggers: [artifact runtime, artifact service, artifact revision, artifact lineage, export bundle, share link, blob storage, artifact tracking, durable output, artifact-service]
---

# SKILL: Artifact Runtime Patterns

## Core Principle
Artifacts are the durable outputs of the OS. Every artifact has a revision chain — no mutation, only new revisions. Lineage tracks parent-child relationships across artifacts. Blob storage is always external (S3/Supabase Storage) — never inline in Postgres beyond small JSON.

---

## 1. Artifact Data Model

```typescript
// artifact-service/types.ts

export interface Artifact {
  id: string;
  workspaceId: string;
  artifactType: ArtifactType;
  title: string;
  status: ArtifactStatus;
  currentRevision: number;
  sourceGraphInstanceId?: string;
  sourceRunId?: string;
  metadata: ArtifactMetadata;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export type ArtifactType =
  | 'document'
  | 'sheet'
  | 'email_draft'
  | 'email_send_log'
  | 'media_video'
  | 'media_audio'
  | 'media_image'
  | 'whiteboard'
  | 'export_bundle'
  | 'dataset'
  | 'report';

export type ArtifactStatus = 'draft' | 'final' | 'archived' | 'deleted';

export interface ArtifactMetadata {
  tags?: string[];
  exportFormats?: string[];
  lastExportedAt?: string;
  shareToken?: string;
  shareExpiresAt?: string;
  retentionDays?: number;
  [key: string]: unknown;
}

export interface ArtifactRevision {
  id: string;
  artifactId: string;
  revisionNumber: number;
  contentJson?: object | null;    // for small structured content
  blobUri?: string | null;        // for large binary content
  checksum?: string | null;
  createdBy: string;
  createdAt: string;
}

export interface ArtifactLineage {
  parentArtifactId: string;
  childArtifactId: string;
  relationType: LineageRelation;
}

export type LineageRelation =
  | 'derived_from'
  | 'exported_from'
  | 'merged_from'
  | 'split_from'
  | 'referenced_by';
```

---

## 2. Artifact CRUD

```typescript
// artifact-service/artifact-store.ts

export async function createArtifact(
  input: {
    workspaceId: string;
    artifactType: ArtifactType;
    title: string;
    createdBy: string;
    sourceGraphInstanceId?: string;
    sourceRunId?: string;
    initialContent?: object;
    initialBlobUri?: string;
  },
  db: DatabaseClient
): Promise<Artifact> {
  return db.transaction(async (tx) => {
    const [artifact] = await tx.query<Artifact>(
      `INSERT INTO artifacts (id, workspace_id, artifact_type, title, status, current_revision, source_graph_instance_id, source_run_id, metadata, created_by)
       VALUES (gen_random_uuid(), $1, $2, $3, 'draft', 1, $4, $5, '{}', $6)
       RETURNING *`,
      [input.workspaceId, input.artifactType, input.title,
       input.sourceGraphInstanceId ?? null, input.sourceRunId ?? null, input.createdBy]
    );

    // Create initial revision
    await tx.execute(
      `INSERT INTO artifact_revisions (id, artifact_id, revision_number, content_json, blob_uri, created_by)
       VALUES (gen_random_uuid(), $1, 1, $2, $3, $4)`,
      [artifact.id, input.initialContent ? JSON.stringify(input.initialContent) : null,
       input.initialBlobUri ?? null, input.createdBy]
    );

    return artifact;
  });
}

export async function getArtifact(
  artifactId: string,
  workspaceId: string,
  db: DatabaseClient
): Promise<Artifact | null> {
  const [row] = await db.query<Artifact>(
    `SELECT * FROM artifacts WHERE id = $1 AND workspace_id = $2 AND status != 'deleted'`,
    [artifactId, workspaceId]
  );
  return row ?? null;
}
```

---

## 3. Revision Chain

```typescript
// artifact-service/revision-chain.ts

export async function createRevision(
  input: {
    artifactId: string;
    contentJson?: object;
    blobUri?: string;
    createdBy: string;
  },
  db: DatabaseClient
): Promise<ArtifactRevision> {
  return db.transaction(async (tx) => {
    // Lock artifact row to prevent concurrent revision creation
    const [artifact] = await tx.query<Artifact>(
      `SELECT * FROM artifacts WHERE id = $1 FOR UPDATE`,
      [input.artifactId]
    );

    if (!artifact) throw new Error(`Artifact not found: ${input.artifactId}`);
    if (artifact.status === 'archived' || artifact.status === 'deleted') {
      throw new Error(`Cannot create revision on ${artifact.status} artifact.`);
    }

    const nextRevision = artifact.currentRevision + 1;

    // Compute checksum for content integrity
    const checksum = input.contentJson
      ? computeChecksum(JSON.stringify(input.contentJson))
      : null;

    const [revision] = await tx.query<ArtifactRevision>(
      `INSERT INTO artifact_revisions (id, artifact_id, revision_number, content_json, blob_uri, checksum, created_by)
       VALUES (gen_random_uuid(), $1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [input.artifactId, nextRevision,
       input.contentJson ? JSON.stringify(input.contentJson) : null,
       input.blobUri ?? null, checksum, input.createdBy]
    );

    await tx.execute(
      `UPDATE artifacts SET current_revision = $1, updated_at = now() WHERE id = $2`,
      [nextRevision, input.artifactId]
    );

    return revision;
  });
}

export async function getRevision(
  artifactId: string,
  revisionNumber: number,
  db: DatabaseClient
): Promise<ArtifactRevision | null> {
  const [row] = await db.query<ArtifactRevision>(
    `SELECT * FROM artifact_revisions WHERE artifact_id = $1 AND revision_number = $2`,
    [artifactId, revisionNumber]
  );
  return row ?? null;
}

export async function listRevisions(
  artifactId: string,
  db: DatabaseClient
): Promise<ArtifactRevision[]> {
  return db.query<ArtifactRevision>(
    `SELECT id, artifact_id, revision_number, checksum, created_by, created_at
     FROM artifact_revisions WHERE artifact_id = $1 ORDER BY revision_number DESC`,
    [artifactId]
  );
}

function computeChecksum(content: string): string {
  const { createHash } = require('crypto');
  return createHash('sha256').update(content).digest('hex');
}
```

---

## 4. Lineage Tracking

```typescript
// artifact-service/lineage.ts

export async function recordLineage(
  relation: ArtifactLineage,
  db: DatabaseClient
): Promise<void> {
  await db.execute(
    `INSERT INTO artifact_lineage (parent_artifact_id, child_artifact_id, relation_type)
     VALUES ($1, $2, $3)
     ON CONFLICT DO NOTHING`,
    [relation.parentArtifactId, relation.childArtifactId, relation.relationType]
  );
}

export async function getLineage(
  artifactId: string,
  direction: 'ancestors' | 'descendants',
  db: DatabaseClient
): Promise<ArtifactLineage[]> {
  if (direction === 'ancestors') {
    return db.query<ArtifactLineage>(
      `SELECT * FROM artifact_lineage WHERE child_artifact_id = $1`,
      [artifactId]
    );
  }
  return db.query<ArtifactLineage>(
    `SELECT * FROM artifact_lineage WHERE parent_artifact_id = $1`,
    [artifactId]
  );
}

// Recursive lineage tree (use with caution on deep chains)
export async function getLineageTree(
  artifactId: string,
  db: DatabaseClient,
  maxDepth = 5
): Promise<LineageNode> {
  const descendants = await getLineage(artifactId, 'descendants', db);
  const children: LineageNode[] = [];

  if (maxDepth > 0) {
    for (const rel of descendants) {
      children.push(await getLineageTree(rel.childArtifactId, db, maxDepth - 1));
    }
  }

  return { artifactId, children };
}
```

---

## 5. Export Bundles

```typescript
// artifact-service/export-bundle.ts

export interface ExportBundle {
  bundleId: string;
  artifactId: string;
  format: string;
  blobUri: string;
  mimeType: string;
  filename: string;
  sizeBytes: number;
  expiresAt: string;
  createdAt: string;
}

export async function createExportBundle(
  input: {
    artifactId: string;
    format: string;
    data: Blob;
    mimeType: string;
    filename: string;
    createdBy: string;
    ttlHours?: number;
  },
  storage: BlobStorage,
  db: DatabaseClient
): Promise<ExportBundle> {
  const ttlHours = input.ttlHours ?? 24;
  const expiresAt = new Date(Date.now() + ttlHours * 60 * 60 * 1000).toISOString();

  // Upload to blob storage
  const blobKey = `exports/${input.artifactId}/${Date.now()}.${input.format}`;
  const blobUri = await storage.upload(blobKey, input.data, input.mimeType);

  // Record in artifact metadata
  await db.execute(
    `UPDATE artifacts
     SET metadata = metadata || jsonb_build_object('lastExportedAt', now()::text, 'lastExportFormat', $1)
     WHERE id = $2`,
    [input.format, input.artifactId]
  );

  // Create artifact revision for the export
  await createRevision(
    { artifactId: input.artifactId, blobUri, createdBy: input.createdBy },
    db
  );

  return {
    bundleId: `bundle_${Date.now()}`,
    artifactId: input.artifactId,
    format: input.format,
    blobUri,
    mimeType: input.mimeType,
    filename: input.filename,
    sizeBytes: input.data.size,
    expiresAt,
    createdAt: new Date().toISOString(),
  };
}
```

---

## 6. Share Links

```typescript
// artifact-service/share-links.ts
import { randomBytes } from 'crypto';

export async function createShareLink(
  artifactId: string,
  workspaceId: string,
  options: {
    ttlHours?: number;
    allowedActions?: ('read' | 'comment')[];
    password?: string;
  },
  db: DatabaseClient
): Promise<{ shareUrl: string; shareToken: string }> {
  const shareToken = randomBytes(32).toString('base64url');
  const expiresAt = options.ttlHours
    ? new Date(Date.now() + options.ttlHours * 3600 * 1000).toISOString()
    : null;

  // Store token hash (never raw token) in metadata
  const { createHash } = require('crypto');
  const tokenHash = createHash('sha256').update(shareToken).digest('hex');

  await db.execute(
    `UPDATE artifacts
     SET metadata = metadata || jsonb_build_object(
       'shareTokenHash', $1,
       'shareExpiresAt', $2,
       'shareAllowedActions', $3::jsonb
     )
     WHERE id = $4 AND workspace_id = $5`,
    [
      tokenHash,
      expiresAt,
      JSON.stringify(options.allowedActions ?? ['read']),
      artifactId,
      workspaceId,
    ]
  );

  const shareUrl = `${process.env.APP_URL}/share/${shareToken}`;
  return { shareUrl, shareToken };
}

export async function resolveShareToken(
  shareToken: string,
  db: DatabaseClient
): Promise<Artifact | null> {
  const { createHash } = require('crypto');
  const tokenHash = createHash('sha256').update(shareToken).digest('hex');

  const [artifact] = await db.query<Artifact>(
    `SELECT * FROM artifacts
     WHERE metadata->>'shareTokenHash' = $1
       AND (metadata->>'shareExpiresAt' IS NULL OR (metadata->>'shareExpiresAt')::timestamptz > now())
       AND status != 'deleted'`,
    [tokenHash]
  );

  return artifact ?? null;
}
```

---

## 7. Blob Storage Interface

```typescript
// artifact-service/blob-storage.ts

export interface BlobStorage {
  upload(key: string, data: Blob | Buffer, mimeType: string): Promise<string>;   // returns URI
  download(key: string): Promise<Buffer>;
  delete(key: string): Promise<void>;
  getSignedUrl(key: string, expirySeconds: number): Promise<string>;
}

// Supabase Storage implementation
import { createClient } from '@supabase/supabase-js';

export class SupabaseBlobStorage implements BlobStorage {
  private supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!  // service key for server-side operations
  );

  async upload(key: string, data: Blob | Buffer, mimeType: string): Promise<string> {
    const { error } = await this.supabase.storage
      .from('artifacts')
      .upload(key, data, { contentType: mimeType, upsert: false });

    if (error) throw new Error(`Blob upload failed: ${error.message}`);
    return `artifacts/${key}`;
  }

  async getSignedUrl(key: string, expirySeconds: number): Promise<string> {
    const { data, error } = await this.supabase.storage
      .from('artifacts')
      .createSignedUrl(key, expirySeconds);

    if (error || !data) throw new Error(`Signed URL failed: ${error?.message}`);
    return data.signedUrl;
  }

  async download(key: string): Promise<Buffer> {
    const { data, error } = await this.supabase.storage
      .from('artifacts')
      .download(key);

    if (error || !data) throw new Error(`Download failed: ${error?.message}`);
    return Buffer.from(await data.arrayBuffer());
  }

  async delete(key: string): Promise<void> {
    const { error } = await this.supabase.storage.from('artifacts').remove([key]);
    if (error) throw new Error(`Delete failed: ${error.message}`);
  }
}
```

---

## 8. Retention and Cleanup

```typescript
// artifact-service/retention.ts

export async function applyRetentionPolicy(db: DatabaseClient): Promise<void> {
  // Find artifacts past their retention date
  const expired = await db.query<{ id: string }>(
    `SELECT id FROM artifacts
     WHERE status = 'final'
       AND (metadata->>'retentionDays')::int IS NOT NULL
       AND created_at < now() - ((metadata->>'retentionDays')::int || ' days')::interval`,
  );

  for (const artifact of expired) {
    await db.execute(
      `UPDATE artifacts SET status = 'archived', updated_at = now() WHERE id = $1`,
      [artifact.id]
    );
  }
}
```

---

## 9. Checklist

Before shipping artifact-service changes:
- [ ] `createRevision` uses `FOR UPDATE` lock — no concurrent revision number collisions
- [ ] Content > 1MB is stored as `blob_uri`, not inline `content_json`
- [ ] Checksums are computed and stored for all revisions with content
- [ ] Share tokens are stored as SHA-256 hashes — never raw tokens in DB
- [ ] Share link expiry is enforced in the query, not just in application code
- [ ] Export bundles have TTL — never permanent without explicit flag
- [ ] Lineage records use `ON CONFLICT DO NOTHING` — safe to call multiple times
- [ ] Blob storage client uses service key (server-side only) — never exposed to browser
- [ ] Artifact deletion is soft (status = 'deleted') — hard delete requires explicit admin action
- [ ] Retention policy runs as a background job, not on-demand
