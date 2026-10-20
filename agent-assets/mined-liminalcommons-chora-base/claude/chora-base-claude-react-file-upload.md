# SAP-035: React File Upload - Claude-Specific Awareness

**SAP ID**: SAP-035
**Name**: react-file-upload
**Full Name**: React File Upload & Storage
**Status**: pilot
**Version**: 1.0.0
**Created**: 2025-11-09
**Last Updated**: 2025-11-09

---

## 📖 Quick Reference

**New to SAP-035?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Quick setup with production-ready configuration
- 📚 **Time Savings** - 7% reduction
- 🎯 **Feature 1** - Core feature 1
- 🔧 **Feature 2** - Core feature 2
- 📊 **Feature 3** - Core feature 3
- 🔗 **Integration** - Works with SAP-020, SAP-032, SAP-033, SAP-034, SAP-041

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-035.
s.

---

## Quick Start for Claude

**SAP-035** provides production-ready file upload patterns for React/Next.js with **four provider options**. This file contains **Claude Code-specific patterns** for adopting and implementing file uploads.

### First-Time Adoption

1. Read [awareness-guide.md](awareness-guide.md) (5 min) - Quick reference for agents
2. Use provider decision tree to select storage provider (2 min)
3. Read [adoption-blueprint.md](adoption-blueprint.md) for chosen provider (15-30 min)
4. Follow step-by-step installation guide
5. Test upload flows

### Session Resumption

- Check user's current provider (UploadThing, Vercel Blob, Supabase, AWS S3)
- Resume from last step in adoption-blueprint.md
- Use troubleshooting guide if issues

---

## Progressive Context Loading

### Phase 1: Quick Discovery (0-5k tokens)

**Goal**: Understand user's upload needs and select provider

**Read**:
1. [awareness-guide.md](awareness-guide.md) - Quick reference
2. Provider decision tree section

**Output**: Provider recommendation (UploadThing, Vercel Blob, Supabase, or AWS S3)

**Example**:
```markdown
User: "I need file uploads for my Next.js app"

Claude (Phase 1):
1. Read awareness-guide.md (Quick Reference + Decision Tree)
2. Ask clarifying questions:
   - Using Vercel deployment? → Vercel Blob
   - Using Supabase database? → Supabase Storage
   - Using AWS infrastructure? → AWS S3
   - None of the above? → UploadThing (default for Next.js)
3. Recommend provider based on answers
```

---

### Phase 2: Implementation (5-30k tokens)

**Goal**: Adopt SAP-035 with chosen provider

**Read**:
1. [adoption-blueprint.md](adoption-blueprint.md) - Provider-specific setup
2. Provider's section in [protocol-spec.md](protocol-spec.md) - API reference (if needed)

**Output**: Working file upload implementation

**Example**:
```markdown
Claude (Phase 2):
1. Read adoption-blueprint.md → Option A (UploadThing) section
2. Follow steps 1-8:
   - npm install uploadthing @uploadthing/react
   - Create file router
   - Create upload component
   - Test upload
3. Verify success with validation checklist
```

---

### Phase 3: Advanced Patterns (30-50k tokens)

**Goal**: Add security, optimization, or advanced features

**Read**:
1. [protocol-spec.md](protocol-spec.md) - How-to guides + Tutorials
2. Security checklist in awareness-guide.md
3. Integration patterns (SAP-033, SAP-034)

**Output**: Production-ready uploads with security, validation, optimization

**Example**:
```markdown
Claude (Phase 3):
1. Read protocol-spec.md → "How to Implement File Validation"
2. Add client-side validation (Zod schema)
3. Add server-side validation (MIME check, magic bytes)
4. Read "How to Optimize Images"
5. Install sharp, add optimization function
6. Test optimized uploads
```

---

## Claude Code Integration

### Tool Usage Patterns

**When using Read tool**:
```
# Phase 1: Quick discovery
Read docs/skilled-awareness/react-file-upload/awareness-guide.md

# Phase 2: Implementation
Read docs/skilled-awareness/react-file-upload/adoption-blueprint.md

# Phase 3: Advanced patterns (if needed)
Read docs/skilled-awareness/react-file-upload/protocol-spec.md
```

---

**When using Bash tool for installation**:
```bash
# Install dependencies (varies by provider)
npm install uploadthing @uploadthing/react  # UploadThing
npm install @vercel/blob                     # Vercel Blob
npm install @supabase/supabase-js            # Supabase Storage
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner  # AWS S3

# Optional: Image optimization
npm install sharp

# Optional: File type validation
npm install file-type

# Optional: Drag-and-drop
npm install react-dropzone
```

---

**When using Write/Edit tool for implementation**:
```bash
# Create file router (UploadThing)
Write app/api/uploadthing/core.ts
Write app/api/uploadthing/route.ts
Write utils/uploadthing.ts

# Create upload API (Vercel Blob)
Write app/api/upload/route.ts

# Create upload component
Write components/upload/ImageUploader.tsx

# Create page
Write app/upload/page.tsx

# Update environment variables
Edit .env.local  # Add provider API keys
```

---

### Common Claude Code Workflows

#### Workflow 1: Adopt SAP-035 with UploadThing (15 min)

```markdown
User: "Add file uploads to my Next.js app"

Claude:
1. Read awareness-guide.md (Phase 1)
2. Recommend UploadThing (Next.js default, free 2GB, pre-built UI)
3. Read adoption-blueprint.md → Option A (Phase 2)
4. Execute installation via Bash tool:
   npm install uploadthing @uploadthing/react
5. Create files via Write tool:
   - app/api/uploadthing/core.ts (file router)
   - app/api/uploadthing/route.ts (API route)
   - utils/uploadthing.ts (helpers)
   - components/upload/ImageUploader.tsx (upload component)
   - app/upload/page.tsx (page)
6. Update .env.local via Edit tool (add UPLOADTHING_SECRET, UPLOADTHING_APP_ID)
7. Test via Bash tool:
   npm run dev
8. Verify with validation checklist
9. Report success to user
```

**Progressive Loading**: Phase 1 → Phase 2 (skip Phase 3 for basic setup)

---

#### Workflow 2: Add File Validation (10 min)

```markdown
User: "Add file validation to uploads"

Claude:
1. Read protocol-spec.md → "How to Implement File Validation" (Phase 3)
2. Install file-type via Bash tool:
   npm install file-type
3. Create validation function via Write tool:
   - lib/file-validation.ts (client + server validation)
4. Update file router via Edit tool:
   - Add server-side validation to .middleware()
5. Update upload component via Edit tool:
   - Add client-side validation
6. Test invalid uploads (>4MB file, .txt file)
7. Verify validation works
8. Report success to user
```

**Progressive Loading**: Phase 3 (assumes Phase 2 already complete)

---

#### Workflow 3: Add Image Optimization (10 min)

```markdown
User: "Optimize uploaded images to save storage"

Claude:
1. Read adoption-blueprint.md → "Optional: Add Image Optimization" (Phase 3)
2. Install sharp via Bash tool:
   npm install sharp
3. Create optimization function via Write tool:
   - lib/image-optimization.ts
4. Update file router via Edit tool:
   - Add .onUploadComplete() optimization
5. Test upload with large JPEG
6. Verify optimized version is smaller (WebP, ~50% size reduction)
7. Report success to user
```

**Progressive Loading**: Phase 3 (assumes Phase 2 already complete)

---

#### Workflow 4: Integrate with Database (SAP-034)

```markdown
User: "Save upload metadata to database"

Claude:
1. Verify SAP-034 adopted (Prisma/Drizzle available)
2. Create Prisma schema via Edit tool:
   - Add Upload model (url, userId, size, mimeType, createdAt)
3. Run migration via Bash tool:
   npx prisma migrate dev --name add-uploads
4. Update file router via Edit tool:
   - Add prisma.upload.create() to .onUploadComplete()
5. Test upload
6. Verify database record created (prisma studio)
7. Report success to user
```

**Progressive Loading**: Phase 3 (assumes SAP-034 and Phase 2 complete)

---

## Provider-Specific Patterns

### UploadThing (Recommended for Next.js)

**When to Use**:
- User using Next.js 13+
- Want rapid prototyping (<20 min setup)
- Need pre-built UI components
- Want type-safe file router
- Budget-conscious (free 2GB tier)

**Key Files**:
- `app/api/uploadthing/core.ts` - File router (type-safe endpoints)
- `app/api/uploadthing/route.ts` - API route handler
- `utils/uploadthing.ts` - React helpers
- `.env.local` - API keys (UPLOADTHING_SECRET, UPLOADTHING_APP_ID)

**Claude Pattern**:
```typescript
// 1. Create file router with auth
.middleware(async () => {
  const user = await auth() // SAP-033
  if (!user) throw new Error("Unauthorized")
  return { userId: user.id }
})

// 2. Use pre-built component
import { UploadButton } from "@/utils/uploadthing"

<UploadButton
  endpoint="imageUploader"
  onClientUploadComplete={(res) => console.log(res)}
/>
```

---

### Vercel Blob (Vercel Deployments)

**When to Use**:
- User deploying on Vercel
- Need edge-optimized storage (<50ms latency globally)
- Want client-side direct uploads
- Willing to pay ($0.05/GB, no free tier)

**Key Files**:
- `app/api/upload/route.ts` - Upload API route
- `components/upload/BlobUploader.tsx` - Upload component
- `.env.local` - API token (BLOB_READ_WRITE_TOKEN)

**Claude Pattern**:
```typescript
// 1. Upload to Vercel Blob
import { put } from '@vercel/blob'

const blob = await put(file.name, file, {
  access: 'public',
  addRandomSuffix: true
})

// 2. Client-side form upload
<form onSubmit={handleUpload}>
  <input type="file" name="file" />
  <button>Upload</button>
</form>
```

---

### Supabase Storage (Supabase Projects)

**When to Use**:
- User using Supabase for database
- Need Row-Level Security (RLS)
- Want image transformations (resize, crop, format)
- Cost-conscious ($0.021/GB, cheapest provider)

**Key Files**:
- `lib/supabase.ts` - Supabase client
- SQL policies (RLS rules)
- `components/upload/SupabaseUploader.tsx` - Upload component
- `.env.local` - Supabase URL and anon key

**Claude Pattern**:
```typescript
// 1. Upload with RLS
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${user.id}/avatar.png`, file)

// 2. Get public URL
const { data: urlData } = supabase.storage
  .from('avatars')
  .getPublicUrl(data.path)

// 3. Image transformation
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('avatar.png', {
    transform: {
      width: 200,
      height: 200,
      resize: 'cover'
    }
  })
```

---

### AWS S3 (Enterprise)

**When to Use**:
- User has existing AWS infrastructure
- Need enterprise features (compliance, versioning, lifecycle)
- Large file support (>500MB, up to 5TB)
- Need 11 nines durability

**Key Files**:
- `lib/s3.ts` - S3 client
- `app/api/s3/presigned-url/route.ts` - Presigned URL API
- `components/upload/S3Uploader.tsx` - Upload component
- `.env.local` - AWS credentials (ACCESS_KEY_ID, SECRET_ACCESS_KEY, BUCKET_NAME)

**Claude Pattern**:
```typescript
// 1. Generate presigned URL
import { getSignedUrl } from "@aws-sdk/s3-request-presigner"

const url = await getSignedUrl(s3Client, command, {
  expiresIn: 3600 // 1 hour
})

// 2. Client uploads directly to S3
await fetch(url, {
  method: 'PUT',
  body: file,
  headers: { 'Content-Type': file.type }
})
```

---

## Integration Patterns

### SAP-033 (Authentication)

**Pattern**: Require authentication for all uploads

```typescript
// UploadThing
.middleware(async () => {
  const user = await auth() // SAP-033
  if (!user) throw new Error("Unauthorized")
  return { userId: user.id }
})

// Vercel Blob API route
export async function POST(request: Request) {
  const session = await auth() // SAP-033
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })
  // Upload...
}

// Supabase RLS
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK (auth.uid() IS NOT NULL);
```

---

### SAP-034 (Database Integration)

**Pattern**: Save file metadata to database

```typescript
.onUploadComplete(async ({ metadata, file }) => {
  await prisma.upload.create({ // SAP-034
    data: {
      url: file.url,
      filename: file.name,
      mimeType: file.type,
      size: file.size,
      userId: metadata.userId
    }
  })
})
```

---

### SAP-041 (Form Validation)

**Pattern**: File upload forms with Zod validation

```typescript
import { z } from 'zod' // SAP-041

const schema = z.object({
  file: z.instanceof(File)
    .refine(file => file.size <= 4 * 1024 * 1024, "Max 4MB")
    .refine(file => ['image/jpeg', 'image/png'].includes(file.type), "Only JPEG/PNG")
})
```

---

### SAP-032 (Performance Optimization)

**Pattern**: Image optimization with sharp.js

```typescript
import sharp from 'sharp' // SAP-032

const optimized = await sharp(buffer)
  .resize(1920, 1080)
  .webp({ quality: 85 })
  .toBuffer()
```

---

## Common Claude Code Pitfalls

### Pitfall 1: Reading All Docs Upfront

**Problem**: Reading all 5 artifacts (charter, spec, guide, blueprint, ledger) = 30+ min

**Fix**: Use progressive loading
- Phase 1: awareness-guide.md only (5 min)
- Phase 2: adoption-blueprint.md for chosen provider (15-30 min)
- Phase 3: protocol-spec.md for advanced patterns (only if needed)

---

### Pitfall 2: Not Checking Provider Constraints

**Problem**: Recommending UploadThing for non-Next.js project

**Fix**: Check user's stack before recommending provider
- Next.js → UploadThing ✅
- Vercel → Vercel Blob ✅
- Supabase → Supabase Storage ✅
- AWS → AWS S3 ✅
- None → Ask user, then recommend UploadThing (most flexible)

---

### Pitfall 3: Skipping Server-Side Validation

**Problem**: Only implementing client-side validation (insecure)

**Fix**: Always add server-side validation
- Read "How to Implement File Validation" in protocol-spec.md
- Add MIME check, magic byte verification
- Never rely on client-side validation alone

---

### Pitfall 4: Missing Environment Variables

**Problem**: Creating code without updating .env.local

**Fix**: After creating API routes, always:
1. Edit .env.local with provider keys
2. Remind user to get keys from provider dashboard
3. Restart dev server for env vars to load

---

### Pitfall 5: Not Testing After Implementation

**Problem**: Assuming setup works without verification

**Fix**: Always test upload flows:
1. Run `npm run dev` via Bash tool
2. Navigate to `/upload`
3. Upload test file
4. Verify success
5. Check validation checklist

---

## Claude-Specific Tips

### Tip 1: Use Provider Decision Tree First

Before reading adoption-blueprint.md, ask user:
- "Are you deploying on Vercel?" → Vercel Blob
- "Are you using Supabase for your database?" → Supabase Storage
- "Do you have existing AWS infrastructure?" → AWS S3
- "None of the above?" → UploadThing

**Why**: Saves time by reading only relevant provider section

---

### Tip 2: Validate Prerequisites

Before starting implementation, verify:
```bash
# Check Next.js version
npx next --version  # Should be 15.1+

# Check if auth is available (SAP-033)
# Ask user: "Do you have authentication set up? Can you call `auth()` function?"

# Check if database is available (SAP-034)
# Ask user: "Do you have Prisma or Drizzle set up?"
```

**Why**: Prevents errors mid-implementation

---

### Tip 3: Use Validation Checklist

After implementation, run through validation checklist:
- [ ] Upload completes successfully
- [ ] Image displays
- [ ] Database record created (if SAP-034)
- [ ] Authentication required (test logged out)
- [ ] File size validation works (test >4MB file)
- [ ] File type validation works (test .txt file)

**Why**: Ensures production readiness

---

### Tip 4: Reference Protocol Spec for Troubleshooting

If user reports error, check:
1. protocol-spec.md → "Troubleshooting Guide"
2. Common issues:
   - "CORS error" → Check CORS config
   - "Unauthorized" → Check auth middleware
   - "Upload succeeds but image not displaying" → Check file access (public/private)

**Why**: Most issues already documented with solutions

---

### Tip 5: Suggest Incremental Adoption

**Recommended Order**:
1. Basic upload (Phase 2: adoption-blueprint.md)
2. File validation (Phase 3: protocol-spec.md → "How to Implement File Validation")
3. Database integration (SAP-034)
4. Image optimization (protocol-spec.md → "How to Optimize Images")
5. Virus scanning (optional, protocol-spec.md → "How to Add Virus Scanning")

**Why**: Incremental validation, easier debugging

---

## Quick Command Reference

### Installation Commands

```bash
# UploadThing
npm install uploadthing @uploadthing/react

# Vercel Blob
npm install @vercel/blob

# Supabase Storage
npm install @supabase/supabase-js

# AWS S3
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner

# Image optimization
npm install sharp

# File validation
npm install file-type

# Drag-and-drop
npm install react-dropzone
```

---

### Validation Commands

```bash
# Test Next.js version
npx next --version

# Run development server
npm run dev

# Open Prisma Studio (check database records)
npx prisma studio

# Run migrations (if adding Upload model)
npx prisma migrate dev --name add-uploads
```

---

## Example Claude Code Session

```markdown
User: "I need file uploads for my Next.js app with Supabase"

Claude (thinking):
- Next.js + Supabase → Supabase Storage is ideal
- Check if Supabase already set up (SAP-034 likely adopted)

Claude (Phase 1: Discovery - 5 min):
1. Read awareness-guide.md
2. Recommend Supabase Storage (RLS, image transforms, $0.021/GB cheapest)

Claude (response):
"I recommend Supabase Storage for your Next.js + Supabase setup. It offers:
- Row-Level Security (RLS) for multi-tenant apps
- Built-in image transformations
- Cheapest storage ($0.021/GB)
- Tight PostgreSQL integration

Setup time: ~20 minutes. Shall I proceed?"

User: "Yes, please set it up"

Claude (Phase 2: Implementation - 20 min):
1. Read adoption-blueprint.md → Option C (Supabase Storage)
2. Create storage bucket (guide user to Supabase Dashboard)
3. Install via Bash:
   npm install @supabase/supabase-js
4. Create via Write:
   - lib/supabase.ts (Supabase client)
   - components/upload/SupabaseUploader.tsx (upload component)
   - app/upload/page.tsx (page)
5. Create RLS policies (guide user to SQL Editor, provide SQL)
6. Update .env.local (guide user to get SUPABASE_URL, SUPABASE_ANON_KEY)
7. Test via Bash:
   npm run dev
8. Verify with validation checklist

Claude (response):
"Supabase Storage setup complete! ✅

Created files:
- lib/supabase.ts - Supabase client
- components/upload/SupabaseUploader.tsx - Upload component
- app/upload/page.tsx - Upload page

RLS policies configured:
- Authenticated users can upload
- Users can access their own files

Test: Navigate to /upload and upload an image.

Next steps:
- Add file validation (10 min)
- Optimize images with sharp.js (10 min)
- Save metadata to database (already integrated with Supabase)"

Result: Supabase Storage adopted, user has working uploads
Time: 25 minutes (Phase 1 + Phase 2 only)
```

**Key Points**:
- Phase 1: Quick provider recommendation (5 min)
- Phase 2: Complete implementation (20 min)
- Skipped Phase 3: Not needed for basic setup
- Updated docs, tested, verified

---

## Support & Resources

**SAP Documentation**:
- **Awareness Guide**: [awareness-guide.md](awareness-guide.md) - Quick reference for agents
- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete API reference, how-to, tutorials
- **Adoption Blueprint**: [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step installation
- **Capability Charter**: [capability-charter.md](capability-charter.md) - Problem/solution design
- **Ledger**: [ledger.md](ledger.md) - Metrics, adoption tracking, feedback

**Provider Documentation**:
- **UploadThing**: [docs.uploadthing.com](https://docs.uploadthing.com)
- **Vercel Blob**: [vercel.com/docs/storage/vercel-blob](https://vercel.com/docs/storage/vercel-blob)
- **Supabase Storage**: [supabase.com/docs/guides/storage](https://supabase.com/docs/guides/storage)
- **AWS S3**: [docs.aws.amazon.com/s3](https://docs.aws.amazon.com/s3)

**Related SAPs**:
- **SAP-033**: [react-authentication](../react-authentication/) - Upload authorization
- **SAP-034**: [react-database-integration](../react-database-integration/) - File metadata storage
- **SAP-041**: [react-form-validation](../react-form-validation/) - Upload forms
- **SAP-032**: [react-performance-optimization](../react-performance-optimization/) - Image optimization

---

## Version History

### 1.0.0 (2025-11-09) - Initial Release

**Added**:
- Claude-specific patterns for SAP-035
- Progressive context loading strategy (Phase 1/2/3)
- Provider-specific patterns (UploadThing, Vercel Blob, Supabase, AWS S3)
- Integration patterns (SAP-033, SAP-034, SAP-041, SAP-032)
- Common Claude Code pitfalls and solutions
- Quick command reference
- Example Claude Code session

**Status**: Pilot (awaiting first production adoption)

---

## Next Steps

1. **Phase 1**: Read [awareness-guide.md](awareness-guide.md) for quick reference
2. **Provider Selection**: Use decision tree to choose provider
3. **Phase 2**: Read [adoption-blueprint.md](adoption-blueprint.md) for implementation
4. **Phase 3 (if needed)**: Read [protocol-spec.md](protocol-spec.md) for advanced patterns
5. **Validate**: Use validation checklist to verify production readiness

**Questions?** See [protocol-spec.md](protocol-spec.md) for detailed how-to guides and tutorials.
