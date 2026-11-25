---
name: publish-article
description: "Safe single-article deployment to production. File-by-file only (never wildcards/recursion). Pre-deployment checklist, exact file targeting, post-deployment verification, rollback procedure."
---

# Publish Article Skill

## Overview

Publish Article handles the **safe, controlled deployment of a single approved article to production**. This is the moment of truth: the article leaves the newsroom and goes live to readers.

**Core principle:** **File-by-file deployment only. Never recursive, never wildcard operations. Never deploy anything except the exact article being published.**

This skill ensures:

- **No accidental overwrites** of other articles
- **No deployment of incomplete/unapproved content**
- **Atomic operations** (article either fully deployed or fully rolled back)
- **Verification before/after** deployment
- **Rollback capability** if something goes wrong post-publish

---

## Supported Deployment Platforms

| Platform | Protocol | Configuration | Example |
|---|---|---|---|
| **Google Cloud Storage (GCS)** | gsutil, API | Bucket name, folder structure | gs://news-bucket/articles/2025-04-01-story.html |
| **Amazon S3** | aws-cli, API | Bucket name, access key | s3://news-bucket/articles/2025-04-01-story.html |
| **Netlify** | git push, API, CLI | Deploy key, site ID | Connected to Git repo; deploy on push |
| **Vercel** | git push, API, CLI | Deploy token, project | Connected to Git repo; auto-deploy |
| **WordPress** | REST API, WP-CLI | Admin URL, auth token | POST to /wp-json/wp/v2/posts |
| **Static Site (SFTP)** | SFTP, SCP | Server host, credentials, path | sftp://news@server.com/public_html/articles/ |
| **GitHub Pages** | git push | Repo name, branch | Commit to gh-pages branch; auto-publish |

---

## Pre-Deployment Checklist

Before the article is deployed, **every item must be approved and completed**:

### Editorial Gate

- [ ] **Article approved by final-editor-review** (editorial review completed; legal defensibility confirmed)
- [ ] **Copy review passed** (readability, accessibility, SEO metadata verified)
- [ ] **Fact-check sign-off** obtained (all claims verified; sources documented)
- [ ] **No outstanding comments** from editor (all feedback addressed or explicitly rejected)

### Technical Gate

- [ ] **All images present and optimized** (<200KB each, 1200×628px minimum for social)
- [ ] **All links tested and working** (no 404s, no typos in URLs)
- [ ] **Video/audio files uploaded** (not embedded from temporary URLs; URLs point to permanent archive)
- [ ] **Metadata complete:**
  - [ ] Meta title (50–60 chars)
  - [ ] Meta description (155–160 chars)
  - [ ] Canonical URL (if reposting)
  - [ ] Open Graph tags (og:image, og:title, og:description, og:url)
  - [ ] Structured data (NewsArticle JSON-LD)

### Compliance Gate

- [ ] **Attribution complete** (byline, publication date, updated date if relevant)
- [ ] **Corrections/errata process** documented (link to corrections page, if applicable)
- [ ] **Paywall/access level** set (free, subscriber-only, metered)
- [ ] **Comments policy** applied (allow/disallow; moderation queue yes/no)
- [ ] **External links checked** (no dead links to external sources)

### Backup & Rollback Gate

- [ ] **Article backed up locally** (version control snapshot taken)
- [ ] **Rollback procedure documented** (specific commands/steps for reverting)
- [ ] **Deployment approver identified** (who will execute the deploy? who can approve rollback?)

---

## Pre-Deployment File Integrity Check

**Before deployment, verify the article file matches expectations:**

### HTML/Markup Validation

```bash
# Check for broken tags (example: validator.w3.org CLI)
# OR manual check in browser DevTools: Console tab for errors

# File size check (articles shouldn't exceed 2MB)
ls -lh article.html
# Expected output: -rw-r--r-- 1 user group 245K Apr 1 09:15 article.html

# Character encoding check (must be UTF-8)
file -b article.html
# Expected: HTML document, ASCII text

# Line count sanity check
wc -l article.html
# Expected: reasonable number (50–1000 depending on length)
```

### Image Integrity Check

```bash
# All images present
grep -o 'src="[^"]*"' article.html | sort | uniq

# Image file sizes (each should be <200KB)
for img in images/*.jpg images/*.png; do ls -lh "$img"; done
```

### Metadata Validation

```bash
# Check meta tags present
grep -E '(og:title|og:description|og:image|og:url)' article.html

# Check canonical URL
grep 'canonical' article.html

# Check structured data
grep 'application/ld+json' article.html
```

---

## Deployment Execution

### Step 1: Choose Your Platform

Your newsroom has configured deployment for one (or more) of these platforms. Identify which platform hosts the published article:

**GCS (Google Cloud Storage):**

```bash
# Verify article file exists locally
ls -l article.html

# Set project (if not already set)
gcloud config set project my-newsroom-project

# Deploy SINGLE article (not directory)
gsutil cp article.html gs://news-bucket/articles/2025-04-01-story.html

# Verify deployment (check file exists)
gsutil ls gs://news-bucket/articles/2025-04-01-story.html
```

**S3 (Amazon Web Services):**

```bash
# Verify credentials configured
aws sts get-caller-identity

# Deploy SINGLE article
aws s3 cp article.html s3://news-bucket/articles/2025-04-01-story.html

# Verify deployment
aws s3 ls s3://news-bucket/articles/2025-04-01-story.html
```

**Static Site (SFTP):**

```bash
# Connect and deploy SINGLE article (NOT directory)
sftp news@server.com << EOF
cd public_html/articles/
put article.html 2025-04-01-story.html
bye
EOF

# Verify (optional: SSH in and check)
ssh news@server.com "ls -lh /home/news/public_html/articles/2025-04-01-story.html"
```

**Netlify (Git-based):**

```bash
# Article is already in Git repo at correct path
git add articles/2025-04-01-story.html
git commit -m "Publish article: [headline]"
git push origin main

# Netlify auto-deploys; check deploy log:
# https://app.netlify.com/sites/[site-name]/deploys
```

**WordPress (REST API):**

```bash
# Create post via REST API
curl -X POST https://newsroom.org/wp-json/wp/v2/posts \
  -H "Authorization: Bearer $WP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Article Title",
    "content": "<p>Article content here...</p>",
    "status": "publish",
    "featured_media": 123
  }'

# Expected response: HTTP 201 Created + post ID
```

### Step 2: Deployment Safety Checks (CRITICAL)

**BEFORE you execute deployment, answer these questions:**

- [ ] **Am I deploying exactly ONE article?** (If deploying >1 file, STOP and verify with editor)
- [ ] **Am I using the exact file path specified?** (Copy-paste from pre-deployment checklist; no guessing)
- [ ] **Am I NOT using wildcards or directories?** (e.g., `*.html` or `articles/` NOT allowed; only `2025-04-01-story.html`)
- [ ] **Have I tested the deployment command on a test file first?** (If possible, deploy test file to test bucket; verify it works)
- [ ] **Do I have a rollback command ready?** (Documented and tested before deployment)

**Red flag:** If ANY of the above is "no," STOP. Re-read this section.

### Step 3: Execute Deployment

```bash
# Log the deployment action (for audit trail)
echo "Deploying article: 2025-04-01-story.html | By: alice@newsroom.org | Time: $(date)" >> deploy.log

# EXECUTE DEPLOYMENT (exact command from pre-deployment checklist)
# Example: GCS
gsutil cp article.html gs://news-bucket/articles/2025-04-01-story.html

# Capture exit code
DEPLOY_STATUS=$?

if [ $DEPLOY_STATUS -eq 0 ]; then
  echo "Deployment successful"
else
  echo "Deployment FAILED (exit code: $DEPLOY_STATUS)"
  exit 1
fi
```

---

## Post-Deployment Verification

Immediately after deployment, verify the article is live and correct:

### Step 1: Verify File Deployed

```bash
# GCS
gsutil ls -l gs://news-bucket/articles/2025-04-01-story.html

# S3
aws s3 ls s3://news-bucket/articles/ | grep 2025-04-01-story.html

# Static site (SFTP)
ssh news@server.com "ls -lh /home/news/public_html/articles/2025-04-01-story.html"
```

**Expected output:** File exists, size matches original, timestamp is current (within last minute).

### Step 2: Verify Article is Accessible

**Test from two locations** (to verify CDN propagation if applicable):

```bash
# Get the article via HTTP (standard browser request)
curl -s -o /dev/null -w "%{http_code}" https://newsroom.org/articles/2025-04-01-story.html

# Expected: HTTP 200 (success), NOT 404 (not found) or 503 (error)

# (Optional) Check full response
curl -s https://newsroom.org/articles/2025-04-01-story.html | head -20
```

### Step 3: Verify Content Integrity

```bash
# Download article from published URL
curl -s https://newsroom.org/articles/2025-04-01-story.html > published.html

# Compare to original (should be identical or very similar)
diff article.html published.html

# If no differences: success
# If differences: investigate (may be auto-formatting by platform)
```

### Step 4: Verify Metadata

**Open the article in a browser and check:**

- [ ] **Headline displays correctly** (no encoding errors, special characters)
- [ ] **Images load** (all images visible, no broken image icons)
- [ ] **Links work** (click a few; confirm they open expected pages)
- [ ] **Byline present** (author name, publication date visible)
- [ ] **Social preview correct** (right-click; inspect Open Graph tags; should show correct og:image, og:title)

### Step 5: Verify Social Metadata

```bash
# Use platform API to check Open Graph tags
# Facebook Sharing Debugger
# https://developers.facebook.com/tools/debug/

# Twitter Card Validator
# https://cards-dev.twitter.com/validator

# OR use curl to check raw tags
curl -s https://newsroom.org/articles/2025-04-01-story.html | grep -E 'og:(title|description|image|url)'
```

### Step 6: Search Engine Indexing (optional, but check after a few hours)

```bash
# Google Search Console (manual check; not API-able)
# Go to: https://search.google.com/search-console/
# Inspect URL: https://newsroom.org/articles/2025-04-01-story.html
# Request indexing if not yet crawled

# (Advanced) Manually trigger crawler
curl -X POST 'https://www.google.com/ping?sitemap=https://newsroom.org/sitemap.xml'
```

---

## Rollback Procedure

If post-deployment verification fails, **roll back immediately**:

### Automatic Rollback (if using version control)

```bash
# For Git-based deployment (Netlify, Vercel, GitHub Pages)
# Find the commit that deployed the article
git log --oneline | head -5

# Revert the commit
git revert [commit-hash]
git push origin main

# Netlify/Vercel will auto-redeploy previous version
# Check status: https://app.netlify.com/sites/[site]/deploys
```

### Manual Rollback (GCS/S3)

```bash
# Option A: Delete the article (removes it entirely)
gsutil rm gs://news-bucket/articles/2025-04-01-story.html

# Option B: Restore from backup (if versioning enabled)
# GCS
gsutil cp gs://news-bucket/articles-backup/2025-04-01-story.html.bak \
  gs://news-bucket/articles/2025-04-01-story.html

# S3
aws s3 cp s3://news-bucket/articles-backup/2025-04-01-story.html.bak \
  s3://news-bucket/articles/2025-04-01-story.html
```

### Manual Rollback (Static Site / SFTP)

```bash
# Option A: Delete from live server
ssh news@server.com "rm /home/news/public_html/articles/2025-04-01-story.html"

# Option B: Restore from backup (pre-deployment snapshot)
scp articles-backup/2025-04-01-story.html.bak news@server.com:/home/news/public_html/articles/2025-04-01-story.html
```

### Manual Rollback (WordPress)

```bash
# Get the post ID
POST_ID=$(curl -s 'https://newsroom.org/wp-json/wp/v2/posts?search=Article%20Title&_fields=id' \
  -H "Authorization: Bearer $WP_TOKEN" | jq '.[0].id')

# Delete the post
curl -X DELETE https://newsroom.org/wp-json/wp/v2/posts/$POST_ID \
  -H "Authorization: Bearer $WP_TOKEN" \
  -d '{"force": true}'
```

### Document the Rollback

```yaml
rollback:
  date: "2025-04-01 10:15 AM"
  reason: "Images failed to load; metadata incomplete"
  by: "alice@newsroom.org"
  command: "gsutil rm gs://news-bucket/articles/2025-04-01-story.html"
  status: "success"
  next_steps: "Re-deploy after fixing image paths"
```

---

## Common Mistakes & Red Flags

### Deployment Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **Deploying directory instead of file** (`gsutil -m cp articles/* gs://bucket/`) | May overwrite other articles; creates chaos | Use explicit filename: `gsutil cp articles/2025-04-01-story.html gs://bucket/articles/...` |
| **Using wildcard** (`aws s3 cp *.html s3://bucket/`) | Uploads everything in current directory; disaster | Deploy one file at a time; verify path before executing |
| **Deploying unapproved version** (old draft instead of final) | Wrong content goes live; requires emergency rollback | Triple-check file path and version before deploy command |
| **No backup before deploying** (no rollback possible) | If something goes wrong, can't recover | Always maintain a pre-deployment backup (version control or manual copy) |
| **Deploying incomplete article** (missing images, metadata) | Broken page goes live; low user experience | Run pre-deployment checklist; verify all images uploaded |
| **Forgetting to update sitemap** (article not discoverable in search) | Search engines don't index; no organic traffic | After deployment, update sitemap.xml; ping Google |

### Verification Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **Not testing from live URL** (only checking local file) | May be cached differently on live server; may not work | Always test via actual published URL; use multiple browsers |
| **Assuming deployment succeeded without checking** | Article may have failed silently; readers see 404 | Always verify HTTP 200 + content check after deployment |
| **Only checking one aspect** (images but not metadata) | Metadata missing; social cards don't display | Use full post-deployment checklist (5 steps) |
| **Checking immediately after deploy** (before CDN propagates) | May see old cached version; false success | Wait 30 seconds; check from 2+ locations; check multiple times |
| **Not testing on mobile** | Mobile users see broken layout; don't discover problem | Test via mobile browser or responsive view in DevTools |

### Rollback Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| **Trying to "fix" the live article** instead of rolling back | May make it worse; wastes time; better to start over | Roll back immediately; fix offline; redeploy fresh |
| **Deleting article without checking if it's still being read** | Early readers miss article; confusion; embarrassment | Rollback ASAP; add note to homepage ("Article temporarily removed for updates") |
| **Rollback command typed wrong** (deletes wrong article) | Deletes innocent article; chaos; reputation damage | Always test rollback command on test data first |
| **No rollback procedure documented** | When disaster happens, don't know what to do | BEFORE deployment, document and test rollback steps |

---

## Critical Safety Rules

### Rule 1: File-by-File Only

**NEVER use:**
```bash
# WRONG: Recursive deploy
gsutil -m cp articles/* gs://bucket/articles/

# WRONG: Wildcard deploy
aws s3 cp *.html s3://bucket/

# WRONG: Directory deploy
sftp news@server << EOF
  cd public_html
  put -r articles/
EOF
```

**ALWAYS use:**
```bash
# RIGHT: Single file
gsutil cp articles/2025-04-01-story.html gs://bucket/articles/2025-04-01-story.html

# RIGHT: Explicit path
aws s3 cp articles/2025-04-01-story.html s3://bucket/articles/2025-04-01-story.html
```

### Rule 2: Atomic Deployment (All or Nothing)

Either the article is fully deployed and verified, or it's rolled back. No partial/broken states.

```bash
# Deploy
gsutil cp article.html gs://bucket/articles/2025-04-01-story.html

# Verify
curl -s https://newsroom.org/articles/2025-04-01-story.html | grep -q "Article Title"

# If verification fails, rollback immediately
if [ $? -ne 0 ]; then
  echo "Verification failed. Rolling back..."
  gsutil rm gs://bucket/articles/2025-04-01-story.html
  exit 1
fi

echo "Deployment and verification successful"
```

### Rule 3: Editorial Approval Before Deployment

**DO NOT DEPLOY** until all gates are passed:

- [ ] Editorial approved (final-editor-review complete)
- [ ] Copy review approved
- [ ] Fact-check approved
- [ ] Pre-deployment checklist signed off

---

## Deployment Workflow Checklist

### Pre-Deployment (30 min before go-live)

- [ ] **Gather approvals** (editorial, copy, fact-check sign-off)
- [ ] **Run pre-deployment checklist** (all items marked complete)
- [ ] **Verify file integrity** (HTML valid, images present, metadata complete)
- [ ] **Prepare rollback procedure** (document exact commands)
- [ ] **Brief deployment approver** (who will authorize? how to reach?)

### Deployment (go-live moment)

- [ ] **Answer safety questions** (single file? exact path? no wildcards?)
- [ ] **Execute deployment command** (copy-paste exact command from checklist)
- [ ] **Document deployment action** (log who/what/when)
- [ ] **Capture exit code** (0 = success, non-zero = failure)

### Post-Deployment (30 min after go-live)

- [ ] **Verify file deployed** (ls/check confirms file exists)
- [ ] **Verify HTTP 200** (article loads in browser)
- [ ] **Content integrity check** (diff original vs. published)
- [ ] **Metadata verification** (og:tags, canonical, structured data correct)
- [ ] **Social preview check** (og:image displays correctly)
- [ ] **Manual spot-check** (open in browser; check images, links, byline)

### If Something Goes Wrong

- [ ] **Stop immediately** (don't try to patch)
- [ ] **Roll back** (execute pre-prepared rollback command)
- [ ] **Document issue** (what failed? why?)
- [ ] **Fix offline** (correct the problem locally)
- [ ] **Re-deploy** (full deployment + verification cycle again)

---

## Escrow & Collaboration

If article is collaborative (multiple reporters, editors):

1. **One person owns deployment** (prevent multiple deployments of same article)
2. **Deployment approver** is editor (signs off on checklist)
3. **Deployment executor** is tech/manager (actually runs commands)
4. **Rollback authority** is editor (decides to roll back if issues arise)

**Communication protocol:**

```
Reporter Alice: "Article ready for deployment checklist"
Editor Bob: "Approved. Running checklist... ✓ All items complete. Deploying at 9:00 AM."
Tech Manager Carol: "Confirmed. Standing by for verification."
[Deployment at 9:00 AM]
Carol: "Article deployed. Running verification... ✓ All checks pass. Live!"
Bob: "Confirmed. Article is live. Notifying social team."
```

---

## Escalation

If deployment fails or article has issues post-publication:

1. **Editors**: Decide whether to roll back or push forward
2. **Tech**: Executes rollback or deployment fix
3. **Communications**: Update homepage/social if article is pulled
4. **Legal** (if needed): Review article for liability if corrections posted

