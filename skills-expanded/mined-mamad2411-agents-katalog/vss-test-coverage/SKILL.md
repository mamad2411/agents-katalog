---
name: vss-test-coverage
description: Authoritative test specification for the Video Search and Summarization (vss) starter pack. Split into phase-specific files for optimal agent execution.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebFetch, Write, Edit
argument-hint: [section] (optional — "api", "ui", "infra", or omit to run all three)
---

# Video Search and Summarization — Test Coverage Specification

Source of truth for what to test on a deployed VSS stack. Covers the VSS Oracle UX frontend (Next.js), the VSS engine backend (NVIDIA Blueprint), supporting services (download-service, PostgreSQL, FSS), and OCI infrastructure.

**Frontend repo:** `grantneumanoracle/vss-oracle-ux` (Next.js 16, React 19, Prisma, Radix UI, Tailwind)
**Backend:** NVIDIA VSS Engine 2.4.0 — multi-NIM pipeline (embedding, reranking, LLM) + Elasticsearch + Neo4j
**Deployment:** Terraform → OKE → Corrino Blueprint + Kubernetes resources in `app-vss-oracle-ux.tf`

---

## Invocation Behavior

- **`/vss-test-coverage infra`** — Read and execute `infra-tests.md` only.
- **`/vss-test-coverage api`** — Read and execute `api-tests.md` only.
- **`/vss-test-coverage ui`** — Read and execute `ui-tests.md` only.
- **`/vss-test-coverage`** (no argument) — Execute ALL three in order: `infra-tests.md`, then `api-tests.md`, then `ui-tests.md`.

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    VSS Oracle UX (Next.js)                   │
│  Port 3000 — exposed via ingress at starter_pack_url         │
│                                                              │
│  /api/vss/config        → K8s API or direct HTTP to backend  │
│  /api/vss/summarize     → VSS backend /summarize             │
│  /api/vss/video-stream  → FSS cache /mnt/fss/cache           │
│  /api/download-and-upload → download-service:8080             │
│  /api/list-bucket-files → OCI Object Storage SDK             │
│  /api/jobs/*            → PostgreSQL (Prisma)                │
│  /api/videos/*          → PostgreSQL (Prisma)                │
│                                                              │
│  Pages: / (Home), /content-review, /settings, /analytics     │
└──────────────────┬──────────────────┬───────────────────────┘
                   │                  │
        ┌──────────▼──────┐  ┌────────▼─────────┐
        │  VSS Backend    │  │ Download Service  │
        │  (recipe pod)   │  │ vss-download-svc  │
        │  :8000          │  │ :8080             │
        │  /summarize     │  └────────┬──────────┘
        │  /health/ready  │           │
        │  /health/live   │     ┌─────▼──────┐
        └──────┬──────────┘     │ OCI Object │
               │                │ Storage    │
    ┌──────────┼──────────┐     └────────────┘
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼────┐
│Elastic│ │Neo4j  │ │NIM pods│
│Search │ │       │ │embed+  │
│       │ │       │ │rerank+ │
│       │ │       │ │LLM     │
└───────┘ └───────┘ └────────┘
        ┌─────────────────┐
        │  PostgreSQL     │
        │  (Prisma DB)    │
        │  videos,        │
        │  summaries,     │
        │  row_reviews,   │
        │  jobs           │
        └─────────────────┘
```

---

## 2. Environment Variables for Testing

| Variable           | Required            | Description                                                                        |
| ------------------ | ------------------- | ---------------------------------------------------------------------------------- |
| `STARTER_PACK_URL` | Yes                 | Base URL of the deployed VSS frontend (e.g. `https://vss-frontend.1-2-3-4.nip.io`) |
| `VSS_BUCKET_NAME`  | For bucket tests    | OCI Object Storage bucket containing test video files                              |
| `VSS_OBJECT_KEY`   | For summarize tests | Object key of a test video file in the bucket                                      |

---

## 3. API Endpoints — Complete Inventory

All API routes are Next.js server routes at `/api/...` on the frontend URL. They proxy to backend services or query PostgreSQL directly.

### 3.1 Backend Configuration

| ID   | Endpoint          | Method | Request | Response (200)                                                           | Purpose                                                                                                     |
| ---- | ----------------- | ------ | ------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| VA-1 | `/api/vss/config` | GET    | —       | `{ success: true, capabilities: { enableAudio: bool, enableCv: bool } }` | Checks VSS backend capabilities. Attempts K8s API detection in prod; falls back to direct HTTP. 5s timeout. |

**Verification:**

- HTTP 200
- `success === true`
- `capabilities` object has `enableAudio` and `enableCv` boolean fields
- Does NOT crash if backend is slow (returns `{ success: true, capabilities: { enableAudio: false, enableCv: false } }` on timeout)

### 3.2 Video Streaming

| ID   | Endpoint                | Method | Request                           | Response                                               | Purpose                                                                                            |
| ---- | ----------------------- | ------ | --------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| VA-2 | `/api/vss/video-stream` | GET    | `?bucket=<name>&objectName=<key>` | 200 (full) or 206 (range) with `Content-Type: video/*` | Streams cached video from FSS mount (`/mnt/fss/cache`). Supports HTTP Range headers for scrubbing. |

**Verification:**

- Requires a video that was previously downloaded (via `/api/download-and-upload`)
- Returns `video/mp4`, `video/webm`, `video/ogg`, or `video/quicktime`
- Range requests return 206 with `Content-Range` header
- 404 if file not cached on FSS

### 3.3 Video Summarization

| ID   | Endpoint             | Method | Request Body                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Response (200)                                                    | Purpose                                                                                  |
| ---- | -------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| VA-3 | `/api/vss/summarize` | POST   | `{ fileId, prompt?, model?, temperature?, top_p?, top_k?, max_tokens?, seed?, num_frames_per_chunk?, vlm_input_width?, vlm_input_height?, summarize_temperature?, summarize_top_p?, summarize_max_tokens?, chat_temperature?, chat_top_p?, chat_max_tokens?, notification_temperature?, notification_top_p?, notification_max_tokens?, summarize_batch_size?, rag_batch_size?, rag_top_k?, enable_audio?, enable_cv_metadata?, cv_pipeline_prompt?, chunk_duration?, caption_summarization_prompt?, summary_aggregation_prompt? }` | `{ success: true, result: { summarization: "<timeline text>" } }` | Calls VSS backend `/summarize`. 30-minute timeout. Returns pipe-delimited timeline rows. |

**Verification:**

- HTTP 200 with `success: true`
- `result.summarization` is a non-empty string
- Timeline format: lines like `120.0:125.0 | Categories: Violence, Alcohol | Event: ...`
- On failure: `{ success: false, error: "<message>" }`
- Requires: a prior `/api/download-and-upload` to stage the file

**Timeline output format (parsed by `lib/format-utils.ts`):**

```
120.0:125.0 | Categories: Violence, Alcohol | Event: Gun visible, person drinks
540.0:545.0 | Categories: Brand messaging | Event: Nike logo on clothing
```

### 3.4 File Upload via Download Service

| ID   | Endpoint                   | Method | Request Body                                 | Response (200)                                                                                           | Purpose                                                                                                                  |
| ---- | -------------------------- | ------ | -------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| VA-4 | `/api/download-and-upload` | POST   | `{ bucketName: string, objectName: string }` | `{ success: true, fileId: string, bytes: number, filename: string, mediaType: string, purpose: string }` | Downloads file from OCI Object Storage to FSS cache, then uploads to VSS API. Returns a `fileId` used for summarization. |

**Verification:**

- HTTP 200, `success: true`
- `fileId` is a non-empty string (used as input to `/api/vss/summarize`)
- `bytes > 0`, `mediaType` matches video MIME type
- On failure: `{ success: false, error: "<message>" }`
- Requires: valid bucket name and object key accessible from the cluster

### 3.5 Bucket File Listing

| ID   | Endpoint                 | Method | Request Body             | Response (200)                                                                       | Purpose                                                                        |
| ---- | ------------------------ | ------ | ------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| VA-5 | `/api/list-bucket-files` | POST   | `{ bucketName: string }` | `{ success: true, bucketName: string, files: [{ name, size, timeCreated, etag? }] }` | Lists objects in OCI Object Storage bucket. Scoped to the stack's compartment. |

**Verification:**

- HTTP 200, `success: true`, `files` is array
- Each file has `name` (string), `size` (number), `timeCreated` (ISO date string)
- Invalid bucket: `{ success: false, error: "..." }` — must NOT crash the server (500)

### 3.6 Jobs Queue

| ID   | Endpoint                 | Method | Request Body                                                    | Response (200)                                                           | Purpose                                                                                    |
| ---- | ------------------------ | ------ | --------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| VA-6 | `/api/jobs`              | GET    | —                                                               | `[{ id, status, bucketName, objectKey, summaryId?, error?, createdAt }]` | Lists all summarization jobs (newest first, max 100).                                      |
| VA-7 | `/api/jobs`              | POST   | `{ bucketName: string, objectKeys: string[], params?: object }` | `{ jobs: [{ id, objectKey, status }] }`                                  | Enqueues one job per objectKey with PENDING status.                                        |
| VA-8 | `/api/jobs/process-next` | POST   | —                                                               | `{ processed: bool, jobId?, status?, summaryId?, error?, message? }`     | Picks next PENDING job, uploads to VSS, runs summarize, persists to DB. 30-minute timeout. |

**Verification (VA-6):**

- HTTP 200, returns array
- Each job has `id`, `status` ∈ {`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`}, `bucketName`, `objectKey`, `createdAt`
- Empty array is valid (no jobs yet)

**Verification (VA-7):**

- HTTP 200, `jobs` array has one entry per `objectKey`
- Each entry has `status: "PENDING"`
- Requires: valid bucket name and existing objects

**Verification (VA-8):**

- HTTP 200
- `processed: true` means a job was picked up; `false` means no pending jobs
- When `processed: true`: `jobId` and `status` present

### 3.7 Summary Persistence (Content Review Data)

| ID    | Endpoint                          | Method | Request                                               | Response (200)                                                                                           | Purpose                                                                            |
| ----- | --------------------------------- | ------ | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| VA-9  | `/api/videos/summaries`           | GET    | `?page=1&limit=50`                                    | `{ data: [{ summaryId, videoId, bucketName, objectKey, resultLength, updatedAt }], total, page, limit }` | Paginated list of all summaries (newest first).                                    |
| VA-10 | `/api/videos/summary`             | GET    | `?bucket=<name>&objectKey=<key>`                      | `{ videoId, summaryId, resultText, resultLength }`                                                       | Fetch full summary text for a specific video.                                      |
| VA-11 | `/api/videos/summary`             | POST   | `{ bucketName, objectKey, resultText, resultLength }` | `{ videoId, summaryId }`                                                                                 | Create or update (upsert) a video summary.                                         |
| VA-12 | `/api/videos/summary/[summaryId]` | DELETE | —                                                     | `{ ok: true }`                                                                                           | Deletes summary, its row reviews, and the associated video record. Cascade delete. |

**Verification (VA-9):**

- HTTP 200, `data` is array, `total` is number
- Pagination: `page` and `limit` match query params, `data.length <= limit`
- Each item has `summaryId`, `videoId`, `bucketName`, `objectKey`, `resultLength`, `updatedAt`

**Verification (VA-10):**

- HTTP 200 if summary exists; 404 if not
- `resultText` is the full timeline string
- `resultLength === resultText.length`

**Verification (VA-11):**

- HTTP 200, returns `videoId` and `summaryId`
- Upsert: same bucket+objectKey → updates existing record (same videoId)

**Verification (VA-12):**

- HTTP 200, `{ ok: true }`
- After delete: GET `/api/videos/summary?bucket=...&objectKey=...` returns 404
- Row reviews for that summaryId are also deleted (cascade)

### 3.8 Row Reviews (Timeline Editing)

| ID    | Endpoint                                  | Method | Request                                                                                     | Response (200)                                                                              | Purpose                                                         |
| ----- | ----------------------------------------- | ------ | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| VA-13 | `/api/videos/summary/[summaryId]/reviews` | GET    | —                                                                                           | `{ rowEdits: Record<string, RowEdit>, rowReviews: Record<string, "approved"\|"rejected"> }` | Fetch all row edits and approval status for a summary.          |
| VA-14 | `/api/videos/summary/[summaryId]/reviews` | PUT    | `{ rowEdits: Record<string, RowEdit>, rowReviews: Record<string, "approved"\|"rejected"> }` | `{ ok: true }`                                                                              | Replace all row reviews for a summary (delete old, create new). |

**RowEdit shape:**

```json
{ "event": "string?", "categories": ["string"]?, "comment": "string?", "startSec": number?, "endSec": number? }
```

**Verification (VA-13):**

- HTTP 200
- `rowEdits` and `rowReviews` are both objects (can be empty `{}`)

**Verification (VA-14):**

- HTTP 200, `{ ok: true }`
- Subsequent GET returns the same `rowEdits` and `rowReviews` that were PUT

### 3.9 VSS Backend Health (Direct — via blueprint ingress)

These are the VSS engine's own endpoints, NOT proxied through the Next.js frontend. They're exposed on the backend service directly (typically internal to cluster, but may be accessible via a separate ingress or port-forward).

| ID    | Endpoint        | Method | Response                        | Purpose                                                               |
| ----- | --------------- | ------ | ------------------------------- | --------------------------------------------------------------------- |
| VA-15 | `/health/ready` | GET    | 200 when all NIM models loaded  | Full pipeline readiness — embedding + reranking + LLM all initialized |
| VA-16 | `/health/live`  | GET    | 200 when engine process running | Process liveness only — does not guarantee models are loaded          |

**Note:** These are on the VSS backend service (port 8000), NOT on the frontend URL. If there's no direct ingress, test via `kubectl port-forward` or the `/api/vss/config` proxy which indirectly confirms backend availability.

---

## 4. UI Pages — Complete Inventory

### 4.1 Home Page (`/`)

**Component:** `FileBrowserCard` inside `(vss)/page.tsx`
**Context provider:** `VssContext` wraps all `(vss)` routes

> **IMPORTANT — Bucket auto-loading behavior:**
> The bucket name is configured in the **Settings page** (`/settings`) and persisted to `localStorage` key `vss-bucket`. When the Home page loads, it **automatically reads the bucket from localStorage and lists files** — there is no manual "enter bucket name → click List Files" step needed. If the bucket is already set in Settings (which it is for deployed stacks), the Home page will show the file list immediately on load.
>
> The Home page is **not for configuring the bucket** — it is for **browsing and processing files** that are already in the configured bucket. The bucket name input (VU-3) and "List Files" button (VU-4) exist as a fallback but are typically pre-populated and auto-triggered.

| ID    | Element                          | Selector Hint                                                       | Interaction                                     | Verification                                                                                                                                                                                                                                                         |
| ----- | -------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VU-1  | Page title / header              | `text="AI Broadcast Compliance"` or Oracle logo                     | None (visual)                                   | Text or image visible after load                                                                                                                                                                                                                                     |
| VU-2  | Navigation sidebar               | Links: Home, Content Review, Analytics, Settings                    | Click each link                                 | URL changes to correct route                                                                                                                                                                                                                                         |
| VU-3  | Bucket name in Settings          | Navigate to `/settings`                                             | Check bucket field                              | Verify the bucket name field on the Settings page is populated. This confirms the bucket is configured. **No interaction needed on the Home page for this check.**                                                                                                   |
| VU-4  | File list loads on Home          | Navigate to `/`, click refresh button                               | Verify file list                                | Click the **refresh button** on the Home page. Verify the file list populates with files from the configured bucket. If an error appears saying "bucket does not exist in compartment" or similar, **stop and ask the user** to create the bucket — do not continue. |
| VU-5  | File search input                | `input` with placeholder containing "Search" or "Filter"            | Type filename                                   | Filters displayed file list                                                                                                                                                                                                                                          |
| VU-6  | File list table/grid             | Table rows or cards showing file names, sizes, dates                | Click row to select                             | Selected file highlighted; enables action buttons                                                                                                                                                                                                                    |
| VU-7  | Parameter sections (collapsible) | Accordion/collapsible sections for VLM, RAG, Summarize params       | Expand/collapse                                 | Section content toggles visibility. **Note:** Current UI may show a simplified batch mode without exposed parameter accordion — mark N/A if no collapsible parameter sections are visible.                                                                           |
| VU-8  | Prompt text areas (3)            | `textarea` elements for caption, summarization, aggregation prompts | Edit text                                       | Values persist to localStorage key `vss-params`                                                                                                                                                                                                                      |
| VU-9  | "Upload & Summarize" button      | `button` with text containing "Summarize"                           | Click after selecting file                      | Triggers download-and-upload → summarize chain; shows progress; auto-navigates to /content-review on success                                                                                                                                                         |
| VU-10 | Batch "Upload & Analyze" button  | `button` with text containing "Analyze"                             | Click with multiple files selected (checkboxes) | Enqueues jobs via POST `/api/jobs`; shows queue progress                                                                                                                                                                                                             |
| VU-11 | Model selector                   | Dropdown/select for model (default: `cosmos-reason1`)               | Change selection                                | Updates summarization params                                                                                                                                                                                                                                         |
| VU-12 | Chunk duration input             | Number input for chunk_duration                                     | Enter value                                     | Updates summarization params                                                                                                                                                                                                                                         |
| VU-13 | Audio/CV toggles                 | Checkbox/toggle for `enable_audio` and `enable_cv_metadata`         | Toggle                                          | Only shown when backend capabilities are enabled (from `/api/vss/config`)                                                                                                                                                                                            |

### 4.2 Content Review Page (`/content-review`)

**Component:** `content-review/page.tsx`

| ID    | Element                      | Selector Hint                                             | Interaction             | Verification                                                                                |
| ----- | ---------------------------- | --------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------- |
| VU-20 | Tab bar for videos           | Tabs (Radix UI) — one per summarized video                | Click tab               | Loads that video's summary + reviews from DB                                                |
| VU-21 | Pagination (prev/next)       | Buttons for navigating pages (5 tabs per page)            | Click next/prev         | Tab set changes; new summaries loaded                                                       |
| VU-22 | Video player                 | `<video>` element at top of page                          | Play/pause/scrub        | Plays cached video from `/api/vss/video-stream`                                             |
| VU-23 | Timeline table               | Table with columns: Time Range, Categories, Event, Status | Scroll/read             | Rows parsed from summary `resultText`                                                       |
| VU-24 | Row edit — event description | Editable text field in row                                | Click edit, change text | Edited value stored in `rowEdits` state                                                     |
| VU-25 | Row edit — categories        | Multi-select or tag editor per row                        | Add/remove categories   | Categories: Violence, Alcohol, Smoking, Language/Profanity, Brand messaging                 |
| VU-26 | Row edit — time range        | Number inputs for startSec / endSec                       | Change values           | Timestamp range updated                                                                     |
| VU-27 | Row edit — comment           | Text area for reviewer comment                            | Type comment            | Stored in `rowEdits`                                                                        |
| VU-28 | Approve button per row       | Button with "Approve" or checkmark                        | Click                   | Row status → `approved`; visual indicator changes                                           |
| VU-29 | Reject button per row        | Button with "Reject" or X mark                            | Click                   | Row status → `rejected`; visual indicator changes                                           |
| VU-30 | Save reviews button          | Button to persist all edits                               | Click                   | Triggers PUT `/api/videos/summary/[id]/reviews`; saved to DB                                |
| VU-31 | Delete summary button        | Button with "Delete"                                      | Click                   | Triggers DELETE `/api/videos/summary/[id]`; cascade removes video + reviews; tab disappears |
| VU-32 | Category stats bar chart     | Recharts bar chart showing category frequency             | Visual only             | Chart renders with correct category counts from timeline data                               |

### 4.3 Settings Page (`/settings`)

| ID    | Element                  | Selector Hint                          | Interaction | Verification                                      |
| ----- | ------------------------ | -------------------------------------- | ----------- | ------------------------------------------------- |
| VU-40 | Bucket name field        | Input (read-only or editable)          | View/edit   | Shows current bucket from localStorage            |
| VU-41 | Prompt text areas        | Three multi-line read-only areas       | View        | Shows caption, summarization, aggregation prompts |
| VU-42 | Default parameter values | Display of model, chunk_duration, etc. | View        | Non-empty values displayed                        |

### 4.4 Analytics Page (`/analytics`)

| ID    | Element             | Selector Hint                                        | Interaction | Verification                                       |
| ----- | ------------------- | ---------------------------------------------------- | ----------- | -------------------------------------------------- |
| VU-50 | Coming soon message | Text containing "Coming soon" or similar placeholder | View        | Page loads without error; placeholder text visible |

---

## 5. User Flows — End-to-End Journeys

> **Note:** These flows are tested as part of the unified UI test matrix (section 7.2). This section documents the detailed step sequences for reference. VF-1 and VF-2 → VU-10 (batch multi-video processing), VF-3 → VU-28/29 + VU-30, VF-4 → VU-31, VF-5 → VU-2. Single-video analysis (VF-1/VU-9) has been replaced by multi-video batch processing (VU-10) which covers the same flow for multiple files.

### Flow F-1: Single Video Analysis (P0) → tested as VU-9

**Preconditions:** Deployed VSS stack, valid bucket with video files, all NIM pods Running, bucket configured in Settings.

1. Navigate to `/` (Home)
2. Verify file list auto-loads from the bucket configured in Settings (no need to enter bucket name or click "List Files" — the bucket is already set in localStorage)
3. Verify file list appears (≥1 file)
4. Select a video file from the list
5. (Optional) Adjust parameters: model, chunk_duration, prompts
6. Click "Upload & Summarize"
7. Wait for progress indicators (download → upload → summarize)
8. Verify auto-navigation to `/content-review`
9. Verify new tab appears for the analyzed video
10. Verify timeline table has ≥1 row with timestamp, categories, event text

**API calls in order:** POST `/api/list-bucket-files` → POST `/api/download-and-upload` → POST `/api/vss/summarize` → POST `/api/videos/summary` → redirect to `/content-review`

### Flow F-2: Batch Queue Processing (P1)

**Preconditions:** Same as F-1.

1. Navigate to `/` (Home)
2. Verify file list auto-loads from the configured bucket
3. Select multiple videos via checkboxes
4. Click "Upload & Analyze"
5. Verify jobs enqueued (job count matches selected files)
6. Wait for processing (poll `/api/jobs` for status changes)
7. Verify completed jobs appear in Content Review

**API calls:** POST `/api/list-bucket-files` → POST `/api/jobs` → (per job) POST `/api/jobs/process-next` → ... → GET `/api/jobs` (polling)

### Flow F-3: Content Review & Editing (P1)

**Preconditions:** At least one completed summary exists in DB.

1. Navigate to `/content-review`
2. Verify tab bar shows ≥1 video tab
3. Click first tab → verify timeline table loads
4. Approve a row → verify visual indicator (green/check)
5. Reject a row → verify visual indicator (red/X)
6. Edit an event description → verify text field accepts input
7. Add a comment to a row
8. Click Save → verify PUT API call succeeds
9. Refresh page → verify edits persisted (GET reviews returns saved data)

**API calls:** GET `/api/videos/summaries` → GET `/api/videos/summary?...` → GET `/api/videos/summary/[id]/reviews` → PUT `/api/videos/summary/[id]/reviews`

### Flow F-4: Delete Summary (P1)

1. Navigate to `/content-review`
2. Note total tab count
3. Click delete on a summary
4. Verify tab disappears
5. Verify GET `/api/videos/summaries` returns `total - 1`
6. Verify GET `/api/videos/summary?bucket=...&objectKey=...` returns 404

### Flow F-5: Navigation (P2)

1. From any page, click each sidebar link: Home, Content Review, Analytics, Settings
2. Verify URL changes correctly: `/`, `/content-review`, `/analytics`, `/settings`
3. Verify each page renders without error (no blank white screen, no 500)

---

## 6. Infrastructure Components

### 6.1 Kubernetes Resources (deployed by Terraform)

| Resource                | Type                        | Namespace | Source                       |
| ----------------------- | --------------------------- | --------- | ---------------------------- |
| `vss-oracle-ux`         | Deployment                  | default   | `app-vss-oracle-ux.tf`       |
| `vss-oracle-ux`         | Service (ClusterIP:80→3000) | default   | `app-vss-oracle-ux.tf`       |
| `vss-oracle-ux-ingress` | Ingress                     | default   | `app-vss-oracle-ux.tf`       |
| `vss-oracle-ux-config`  | ConfigMap                   | default   | `app-vss-oracle-ux.tf`       |
| `vss-download-service`  | Deployment                  | default   | `app-vss-oracle-ux.tf`       |
| `vss-download-service`  | Service (ClusterIP:8080)    | default   | `app-vss-oracle-ux.tf`       |
| `vss-fss-pv`            | PersistentVolume            | —         | FSS mount for video cache    |
| `vss-fss-pvc`           | PersistentVolumeClaim       | default   | Claims FSS PV                |
| `vss-db-url`            | Secret                      | default   | PostgreSQL connection string |
| `vss-oracle-ux-tls`     | Secret (cert-manager)       | default   | TLS cert for ingress         |

### 6.2 Blueprint-Deployed Pods (via Corrino)

| Pod prefix                                | Purpose                                 | GPU                  | Startup time |
| ----------------------------------------- | --------------------------------------- | -------------------- | ------------ |
| `recipe-vss-deployment-*-vss-engine-*`    | VSS engine (main summarization service) | Yes (GPU4.8 or L40S) | 10-15 min    |
| `recipe-vss-deployment-*-elasticsearch-*` | Elasticsearch for search index          | No                   | 2-5 min      |
| `recipe-vss-deployment-*-neo4j-*`         | Neo4j graph database                    | No                   | 2-3 min      |
| `recipe-vss-deployment-*-embedding-*`     | Embedding NIM model                     | Yes                  | 15-20 min    |
| `recipe-vss-deployment-*-reranking-*`     | Reranking NIM model                     | Yes                  | 10-15 min    |
| `recipe-vss-deployment-*-nim-llm-*`       | LLM NIM model (cosmos-reason1)          | Yes                  | 15-30 min    |

### 6.3 OCI Resources

| Resource                              | Purpose                                                         |
| ------------------------------------- | --------------------------------------------------------------- |
| File Storage (FSS) + Mount Target     | Shared cache for downloaded videos between frontend and backend |
| Object Storage bucket (user-provided) | Source of video files to analyze                                |
| Load Balancer (via ingress-nginx)     | Routes external traffic to cluster                              |

---

## 7. Test Matrix

> **Legend:**
>
> - **Surface**: `API` = HTTP only | `UI` = browser (includes end-to-end flows) | `Infra` = kubectl/OCI CLI
> - **P**: `P0` = blocks release | `P1` = fix before next cycle | `P2` = nice to have
> - **Type**: `smoke` = fast broad | `regression` = specific behavior | `e2e` = full journey (may take 30+ min)
> - **Timeout**: Max wait time for the test. Tests with long timeouts (e.g., 35min for summarization) must NOT be skipped — wait patiently.

> **MANDATORY: Execute ALL tests in EVERY section, in the order listed (by ascending ID). Do NOT skip, reorder, or omit any test. If a test fails, record the failure and continue to the next test. If you are stuck or unsure about a test's verification criteria, stop and ask the user for guidance — do NOT silently skip it or mark it N/A without explaining why.**

### 7.1 API Tests

| #   | ID    | Test                        | Endpoint                               | Method | Verification                                                                 | P   | Type       | Preconditions               |
| --- | ----- | --------------------------- | -------------------------------------- | ------ | ---------------------------------------------------------------------------- | --- | ---------- | --------------------------- |
| 1   | VA-1  | Backend config              | `/api/vss/config`                      | GET    | 200, `success: true`, `capabilities.enableAudio` and `enableCv` are booleans | P0  | smoke      | Frontend pod Running        |
| 2   | VA-2  | Video streaming             | `/api/vss/video-stream`                | GET    | 200/206 with `video/*` content-type, or 404 if not cached                    | P1  | smoke      | Video previously downloaded |
| 3   | VA-3  | Summarize video             | `/api/vss/summarize`                   | POST   | 200, `success: true`, `result.summarization` contains timeline rows          | P0  | e2e        | File uploaded via VA-4      |
| 4   | VA-4  | Download & upload file      | `/api/download-and-upload`             | POST   | 200, `success: true`, `fileId` non-empty                                     | P0  | e2e        | Valid bucket + object       |
| 5   | VA-5a | List bucket files (valid)   | `/api/list-bucket-files`               | POST   | 200, `success: true`, `files` is array with file objects                     | P1  | smoke      | Valid `VSS_BUCKET_NAME`     |
| 6   | VA-5b | List bucket files (invalid) | `/api/list-bucket-files`               | POST   | Non-500 response, `success: false`, `error` string present                   | P1  | regression | None                        |
| 7   | VA-6  | List jobs                   | `/api/jobs`                            | GET    | 200, array of job objects (can be empty)                                     | P1  | smoke      | Frontend pod Running        |
| 8   | VA-7  | Enqueue jobs                | `/api/jobs`                            | POST   | 200, `jobs` array with PENDING entries                                       | P1  | e2e        | Valid bucket + objects      |
| 9   | VA-8  | Process next job            | `/api/jobs/process-next`               | POST   | 200, `processed: true/false`                                                 | P1  | e2e        | Pending job in queue        |
| 10  | VA-9a | List summaries              | `/api/videos/summaries`                | GET    | 200, `data` array, `total` number, `page`/`limit` match params               | P0  | smoke      | Frontend pod Running        |
| 11  | VA-9b | Summaries pagination        | `/api/videos/summaries?page=1&limit=2` | GET    | 200, `data.length <= 2`, `page === 1`, `limit === 2`                         | P1  | regression | None                        |
| 12  | VA-10 | Get summary detail          | `/api/videos/summary`                  | GET    | 200, `resultText` non-empty, `resultLength > 0`                              | P0  | smoke      | ≥1 summary exists           |
| 13  | VA-11 | Create/update summary       | `/api/videos/summary`                  | POST   | 200, `videoId` and `summaryId` returned                                      | P1  | regression | None                        |
| 14  | VA-12 | Delete summary              | `/api/videos/summary/[id]`             | DELETE | 200, `{ ok: true }`; subsequent GET returns 404                              | P1  | regression | ≥1 summary exists           |
| 15  | VA-13 | Get row reviews             | `/api/videos/summary/[id]/reviews`     | GET    | 200, `rowEdits` and `rowReviews` are objects                                 | P1  | smoke      | ≥1 summary exists           |
| 16  | VA-14 | Update row reviews          | `/api/videos/summary/[id]/reviews`     | PUT    | 200, `{ ok: true }`; subsequent GET returns same data                        | P1  | regression | ≥1 summary exists           |

### 7.2 UI Tests

> **Ordering:** Tests are ordered by logical flow — prerequisite steps come first. Batch processing (VU-10) must complete before Content Review tests can run. **NEVER skip a test because it takes a long time to process.** Set appropriate timeouts and wait for completion. Multi-video batch processing can take 60-90 minutes — that is expected.

| #   | ID       | Test                                 | Page              | Verification                                                                                                                                                                                                                                                                                                                                                                                                                                                         | P   | Type  | Timeout   |
| --- | -------- | ------------------------------------ | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- | ----- | --------- |
| 1   | VU-1     | Header/title visible                 | `/`               | "AI Broadcast Compliance" or Oracle logo visible                                                                                                                                                                                                                                                                                                                                                                                                                     | P0  | smoke | 30s       |
| 2   | VU-3     | Bucket configured in Settings        | `/settings`       | Navigate to Settings page. Verify the bucket name field is populated. This confirms the bucket is configured for the deployment.                                                                                                                                                                                                                                                                                                                                     | P0  | smoke | 30s       |
| 3   | VU-2     | Sidebar navigation (all pages)       | all               | All 4 links (Home, Content Review, Analytics, Settings) navigate to correct URLs; each page renders without error                                                                                                                                                                                                                                                                                                                                                    | P1  | smoke | 30s       |
| 4   | VU-4     | File list loads on refresh           | `/`               | Navigate to Home page and click the **refresh button**. Verify the file list populates with files from the configured bucket. If an error appears saying "bucket does not exist in compartment" or similar, **stop the test run and ask the user** to create the bucket before continuing.                                                                                                                                                                           | P0  | e2e   | 60s       |
| 5   | VU-6     | File selection                       | `/`               | Click a file row → visual selection indicator                                                                                                                                                                                                                                                                                                                                                                                                                        | P1  | smoke | 30s       |
| 6   | VU-7     | Parameter sections toggle            | `/`               | Collapsible sections expand/collapse on click                                                                                                                                                                                                                                                                                                                                                                                                                        | P2  | smoke | 30s       |
| 7   | VU-10    | Batch Upload & Analyze (multi-video) | `/`               | Select ≥2 video files via checkboxes → click "Upload & Analyze" → verify jobs are queued (job count matches selected files) → watch jobs process consecutively (each transitions PENDING → PROCESSING → COMPLETED in order) → wait until ALL jobs reach COMPLETED status → navigate to `/content-review` → verify a new tab exists for each processed video. **Do NOT use API calls — verify entirely through the UI.** Poll the queue/progress UI, not `/api/jobs`. | P0  | e2e   | **90min** |
| 8   | VU-20    | Content Review tabs                  | `/content-review` | Tab bar shows ≥1 tab per processed video; tab click loads summary                                                                                                                                                                                                                                                                                                                                                                                                    | P0  | smoke | 30s       |
| 9   | VU-23    | Timeline table renders               | `/content-review` | Table with Time Range, Categories, Event columns; ≥1 row with timestamps, categories, event text                                                                                                                                                                                                                                                                                                                                                                     | P0  | smoke | 30s       |
| 10  | VU-28/29 | Approve/Reject rows                  | `/content-review` | Approve and Reject buttons change row visual state (green/check, red/X)                                                                                                                                                                                                                                                                                                                                                                                              | P1  | e2e   | 30s       |
| 11  | VU-30    | Save & verify reviews                | `/content-review` | Save button triggers PUT `/api/videos/summary/[id]/reviews`; refresh page; edits persist (GET returns saved data)                                                                                                                                                                                                                                                                                                                                                    | P1  | e2e   | 30s       |
| 12  | VU-32    | Category stats chart                 | `/content-review` | Bar chart renders with category labels (Recharts)                                                                                                                                                                                                                                                                                                                                                                                                                    | P2  | smoke | 30s       |
| 14  | VU-31    | Delete summary cascade               | `/content-review` | Delete button removes tab; GET `/api/videos/summary?...` returns 404; row reviews cascade deleted                                                                                                                                                                                                                                                                                                                                                                    | P1  | e2e   | 30s       |
| 15  | VU-40    | Settings page                        | `/settings`       | Bucket name, prompts, parameters displayed                                                                                                                                                                                                                                                                                                                                                                                                                           | P2  | smoke | 30s       |
| 16  | VU-50    | Analytics placeholder                | `/analytics`      | "Coming soon" text visible; no error                                                                                                                                                                                                                                                                                                                                                                                                                                 | P2  | smoke | 30s       |

### 7.3 Infrastructure Tests

| #   | ID   | Test                         | Verification                                                                                                      | P   | Type       |
| --- | ---- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------- | --- | ---------- |
| 1   | VI-1 | Frontend pod Running         | `kubectl get pods -l app=vss-oracle-ux` → Running                                                                 | P0  | smoke      |
| 2   | VI-2 | Download service pod Running | `kubectl get pods -l app=vss-download-service` → Running                                                          | P0  | smoke      |
| 3   | VI-3 | Blueprint pods Running       | All `recipe-vss-deployment-*` pods Running (vss-engine, elasticsearch, neo4j, embedding, reranking, nim-llm)      | P0  | smoke      |
| 4   | VI-4 | FSS PVC bound                | `kubectl get pvc` shows `vss-fss-pvc` Bound                                                                       | P0  | smoke      |
| 5   | VI-5 | ConfigMap data correct       | `kubectl get cm vss-oracle-ux-config -o json` has `VSS_API_BASE_URL`, `DOWNLOAD_SERVICE_URL`, `FILE_STORAGE_PATH` | P1  | regression |
| 6   | VI-6 | Ingress has TLS cert         | `kubectl get ingress vss-oracle-ux-ingress -o jsonpath='{.spec.tls[0].secretName}'` = `vss-oracle-ux-tls`         | P1  | smoke      |
| 7   | VI-7 | DB Secret exists             | `kubectl get secret vss-db-url` exists with `DATABASE_URL` key                                                    | P0  | smoke      |

---

## 8. Database Schema (Prisma)

For reference when writing data-layer tests or debugging:

```prisma
model Video {
  id         String   @id @default(cuid())
  bucketName String
  objectKey  String
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt
  summary    Summary?
  @@unique([bucketName, objectKey])
  @@index([bucketName])
}

model Summary {
  id           String      @id @default(cuid())
  videoId      String      @unique
  video        Video       @relation(...)
  resultText   String      @db.Text
  resultLength Int
  createdAt    DateTime    @default(now())
  updatedAt    DateTime    @updatedAt
  rowReviews   RowReview[]
}

model RowReview {
  id         String   @id @default(cuid())
  summaryId  String
  summary    Summary  @relation(...)
  rowIndex   Int
  status     String?          // "approved" | "rejected"
  event      String?  @db.Text
  categories String[]
  comment    String?  @db.Text
  startSec   Float?
  endSec     Float?
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt
  @@unique([summaryId, rowIndex])
  @@index([summaryId])
}

model SummarizationJob {
  id         String                 @id @default(cuid())
  status     SummarizationJobStatus // PENDING | PROCESSING | COMPLETED | FAILED
  bucketName String
  objectKey  String
  fileId     String?
  summaryId  String?
  error      String?  @db.Text
  params     Json?
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt
  @@index([status])
  @@index([createdAt])
}
```

---

## 9. Known Issues & Stability Notes

| Issue                                        | Impact                                                    | Mitigation                                                               |
| -------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------ |
| NIM model startup takes 15-30 min            | `/health/ready` fails until all loaded; summarize fails   | Wait for all blueprint pods Running before testing API                   |
| FSS mount may fail if mount target not ready | Download service errors; video-stream 404s                | Check `kubectl get pvc` bound status first                               |
| 30-minute timeout on summarize               | Long-running POST can timeout nginx or client             | Ingress has `proxy-read-timeout: 1800`; test should set matching timeout |
| Cosmos-reason1 model cold start              | First summarize request after deploy may be slow          | Allow 5-10 min extra on first summarize call                             |
| OCI Object Storage auth                      | Bucket listing fails if Instance Principal not configured | Verify `COMPARTMENT_ID` and `TENANCY_NAMESPACE` in configmap             |
| PostgreSQL not ready                         | All /api/videos/\* and /api/jobs endpoints fail           | Check `vss-db-url` secret exists and Prisma migration ran                |

---

## Maintenance

- Re-run this skill when `app-vss-oracle-ux.tf` or `blueprint_files.tf` changes for VSS
- Update API inventory if `vss-oracle-ux` frontend image version changes (new routes may be added)
- IDs (VA-_, VU-_, VI-_) are stable — never renumber, only append. VF-_ IDs are retired (merged into VU-\*).
- If an endpoint is removed, mark `DEPRECATED` — do not delete from this spec
