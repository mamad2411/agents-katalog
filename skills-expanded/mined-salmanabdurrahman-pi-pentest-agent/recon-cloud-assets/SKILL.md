---
name: recon-cloud-assets
description: Cloud asset discovery from public signals and gated validation — S3 bucket enumeration, Azure Blob container detection, GCP Storage discovery, cloud-subdomain identification (CloudFront, Azure CDN, GCS), bucket permission testing with unsigned requests, and cloud misconfiguration scanning via nuclei templates. Active probing requires authorization and scope validation; passive enumeration from CT logs and search engines is safe by default.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [cloud-asset-list, command-log, redacted-evidence, finding-draft]
---

# Cloud asset discovery — storage, CDN, and service mapping

Use this skill to discover the target's cloud-hosted assets: object storage buckets (S3, Blob, GCS), content delivery networks (CloudFront, Azure CDN), serverless endpoints, and cloud-subdomain infrastructure. Passive discovery uses certificate transparency logs, search engines, and subdomain pattern matching — these do not contact the target. Active validation (bucket permission checks, unsigned list requests) does contact cloud-provider APIs and requires authorization and scope validation.

## Required inputs

- Target domain and any known cloud-provider accounts or organization IDs.
- Scope file with authorized domains, subdomain patterns, and explicit cloud-asset permission (e.g., "S3 bucket enumeration permitted for *.TARGET.COM and target-* buckets").
- Authorization cache for the target before any active bucket probe.
- Rate limits: S3 unsigned requests are rate-limited by AWS per source IP. Azure and GCP have their own throttling. Limit to ≤ 5 checks/second across all providers combined.
- Evidence goal: cloud-asset inventory with permission status (public/private), bucket-content summary for public buckets, and misconfiguration findings.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` to load cloud-asset scope boundaries — which bucket names, cloud providers, and services are authorized.
3. `pentest_agent_validate_target` for each cloud-asset URL before any active probe.
4. `pentest_agent_check_authorization` before every active bucket permission check, unsigned list, or object download.
5. `pentest_agent_build_command` for dry-run preview of awscli, curl, or nuclei commands.
6. `pentest_agent_execute_tool` for all execution — rate-limit enforcement, bounded output.
7. `pentest_agent_append_evidence` with asset metadata, permission status, and finding classification.

## Workflow

### Phase 1 — cloud-subdomain and domain-pattern discovery

Identify subdomains and URL patterns indicating cloud infrastructure. This phase is passive — data comes from CT logs, search engines, and known subdomain patterns.

1. Certificate Transparency log search for cloud-related names:
   - `curl -s "https://crt.sh/?q=%25.TARGET.COM&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | grep -iE "s3|blob|storage|cdn|cloudfront|azureedge|cloud|gcs|aws|azure" | sort -u | tee cloud_subdomains.txt`
2. Known cloud subdomain patterns (append to discovery list):
   - AWS: `s3.amazonaws.com`, `s3-<region>.amazonaws.com`, `cloudfront.net`, `elasticbeanstalk.com`, `awsglobalaccelerator.com`
   - Azure: `blob.core.windows.net`, `azurewebsites.net`, `azureedge.net`, `cloudapp.net`, `trafficmanager.net`
   - GCP: `storage.googleapis.com`, `appspot.com`, `firebaseio.com`, `run.app`
3. Search engine dorks for exposed cloud assets (all passive, no target contact):
   - `site:s3.amazonaws.com "TARGET.COM"` — files in S3 buckets referencing the target.
   - `site:blob.core.windows.net "TARGET"` — Azure Blob containers.
   - `site:storage.googleapis.com "TARGET"` — GCP Storage buckets.
4. Subdomain pattern matching from existing subdomain list:
   - `grep -iE "s3\.|s3-|blob\.|storage\.|cdn\.|cloud\.|gcs\.|assets\.|static\.|media\.|files\.|backup\." all_subs.txt >> cloud_subdomains.txt`

### Phase 2 — bucket-name permutation and candidate generation

Generate likely cloud bucket names by permuting the target's domain name and common keywords. Many organizations use predictable bucket naming.

1. Base keywords:
   - Target domain: `TARGET`, `TARGET-COM`, `targetcom`
   - Common prefixes: `backup`, `dev`, `staging`, `prod`, `static`, `media`, `assets`, `files`, `data`, `logs`, `archive`, `cdn`, `images`, `uploads`, `downloads`
   - Common suffixes: `-backup`, `-assets`, `-dev`, `-prod`, `-staging`, `-media`, `-files`, `-data`, `-logs`
2. Generate S3 bucket candidates:
   - `TARGET`, `TARGET-backup`, `TARGET-assets`, `TARGET-dev`, `TARGET-prod`, `TARGET-media`, `TARGET-files`, `TARGET-data`, `TARGET-logs`, `backup-TARGET`, `dev-TARGET`, `staging-TARGET`, `TARGET-COM`, `targetcom-assets`, `targetcom-backup`
3. Generate Azure Blob storage account candidates:
   - Azure storage accounts must be lowercase alphanumeric (3-24 chars, no hyphens in some cases). Permute: `target`, `targetcom`, `targetdev`, `targetprod`, `targetassets`, `targetbackup`.
4. Generate GCP bucket candidates:
   - Similar to S3 but GCP bucket names are globally unique. Same permutation list as S3 candidates.

### Phase 3 — active bucket permission verification

Probe generated bucket names to determine accessibility. This phase contacts cloud-provider APIs — authorization, scope validation, and rate limiting are mandatory.

1. S3 bucket check via AWS CLI (unsigned, no credentials):
   - `aws s3 ls s3://BUCKET_NAME --no-sign-request 2>&1`
   - Exit code 0 with directory listing → bucket is PUBLIC READ (listable). Critical finding.
   - Exit code 0 with empty output or "Access Denied" → bucket exists but is private. Record as `EXISTS (private)`.
   - "NoSuchBucket" → bucket does not exist. Record as `NOT_FOUND`.
   - Rate limit: AWS allows ~1 request/second per source IP for unsigned requests. Use `sleep 1` between checks.
2. S3 bucket check via HTTP (curl, faster but less structured):
   - `curl -s -o /dev/null -w "%{http_code}" "https://BUCKET_NAME.s3.amazonaws.com" --max-time 5`
   - HTTP 200 → public bucket or public listing enabled. Follow up with: `curl -s "https://BUCKET_NAME.s3.amazonaws.com" | head -50`
   - HTTP 403 → bucket exists, access denied. Record as `EXISTS (private)`.
   - HTTP 404 or "NoSuchBucket" XML → bucket does not exist.
3. Azure Blob container check:
   - `curl -s -o /dev/null -w "%{http_code}" "https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER?restype=container&comp=list" --max-time 5`
   - HTTP 200 → container is public and listable.
   - List contents: `curl -s "https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER?restype=container&comp=list" | grep -oE "<Name>[^<]+</Name>"`
4. GCP bucket check:
   - `curl -s -o /dev/null -w "%{http_code}" "https://storage.googleapis.com/BUCKET_NAME" --max-time 5`
   - HTTP 200 with XML directory listing → bucket is public.
   - HTTP 403 → bucket exists, access denied.

### Phase 4 — public bucket content assessment

For buckets confirmed as PUBLIC READ, assess the content exposure severity. Do NOT download or exfiltrate sensitive data — the goal is to document existence and risk, not to collect evidence at scale.

1. List top-level contents:
   - S3: `aws s3 ls s3://BUCKET_NAME --no-sign-request | head -50`
   - Azure: URL listing from Phase 3.
   - GCP: `curl -s "https://storage.googleapis.com/BUCKET_NAME" | head -100`
2. Identify sensitive file patterns in the listing:
   - `.env`, `.config`, `.yaml`, `.json` (configuration files — potentially contain credentials).
   - `.sql`, `.sql.gz`, `.dump` (database backups — potentially contain all application data).
   - `.pem`, `.key`, `.crt`, `.p12`, `.pfx` (cryptographic keys and certificates).
   - `backup`, `archive`, `dump` (backup archives — potentially full system backups).
   - `passwords`, `credentials`, `secrets`, `.aws/`, `.ssh/` (explicit credential files).
   - Log files (`access.log`, `error.log`, `debug.log`) — may contain session tokens, PII, or internal paths.
3. Flag each sensitive pattern as a finding. Record: bucket name, URL, the sensitive file pattern observed, file count (if visible), and severity estimate.
4. Do NOT download or open files unless a specific file is needed to confirm the finding and its estimated size is small (< 1 KB). Even then, review the file locally in an isolated environment and redact contents before evidence storage.

### Phase 5 — nuclei cloud-misconfiguration scan

Use nuclei templates to automate cloud misconfiguration detection on discovered cloud endpoints.

1. Run nuclei against identified cloud URLs:
   - `nuclei -t http/misconfiguration/aws/ -u TARGET_URLS.txt -o nuclei_aws_results.txt`
   - `nuclei -t http/misconfiguration/azure/ -u TARGET_URLS.txt -o nuclei_azure_results.txt`
   - `nuclei -t http/exposures/ -u TARGET_URLS.txt -o nuclei_exposures.txt`
2. Review nuclei findings manually. Nuclei may produce false positives for generic patterns — verify each finding with a manual curl check.
3. Document verified findings with nuclei template name, matched URL, and a manual verification note.

## Decision points

- **Bucket exists (private) but bucket name suggests sensitive content**: record as a finding with `EXISTS (private) — contains [sensitive pattern name]`. The bucket being private is the correct state, but the naming convention may indicate what data exists. No further action without authorization for authenticated testing.
- **Bucket is public and contains database backups**: this is a CRITICAL finding. Do NOT download the backup. Record the file name, size (if visible), and the finding. The operator decides whether to download for proof in coordination with the engagement lead.
- **Bucket is public and writable**: test write access with a harmless marker file: `echo "security-test-marker" | aws s3 cp - s3://BUCKET/test-marker.txt --no-sign-request`. If write succeeds, the bucket allows public uploads — this may enable bucket takeover, malware distribution, or data corruption. Flag as CRITICAL. Immediately delete the test marker: `aws s3 rm s3://BUCKET/test-marker.txt --no-sign-request`. Never leave artifacts in the bucket.
- **Bucket name permutation list grows beyond 100 candidates**: prioritize by likelihood: exact target domain name first, then `backup`/`dev`/`prod`/`assets` variants, then keyword permutations. Do not brute-force with a large dictionary — this is scope creep and may trigger rate limiting or monitoring alerts.

## Prohibited behavior

- Downloading, exfiltrating, or storing bucket contents at scale — document existence and risk, not the actual data. Exception: a single small file needed to confirm a finding, and only with explicit operator approval.
- Uploading executable, script, or persistent content to writable buckets beyond the ephemeral test marker (which must be removed immediately).
- Authenticated bucket testing using discovered or guessed credentials — this skill uses unsigned/no-auth requests only. Authenticated testing requires separate authorization.
- Testing bucket names outside the engagement scope — only buckets belonging to or clearly associated with the target.
- Writing, modifying, or deleting any existing data in discovered buckets — read-only access (listing, head-object) only, with the sole exception of a test-marker file for write-access verification (immediately deleted).

## Stop conditions

- Bucket returns a legal notice, security warning, or "this bucket is monitored" message → stop probing that bucket. Document the notice. The cloud provider or bucket owner is aware of enumeration activity. Do not test further.
- AWS returns 429 (Too Many Requests) → rate-limited by AWS. Stop for 60 seconds, reduce concurrent requests, resume at lower rate.
- Any bucket contains classified, healthcare, financial, or similarly regulated data → stop probing that bucket immediately. Document the existence of regulated data without recording the data itself. Escalate to the engagement lead — this is a compliance boundary.
- A public bucket appears to belong to a third-party (not the target) → stop, record as `UNRELATED_THIRD_PARTY` in notes, exclude from evidence. Do not probe third-party buckets.

## Evidence

For each verified cloud asset, record: asset type (S3 bucket, Azure container, GCP bucket, CloudFront distribution), URL, permission status (PUBLIC/PRIVATE/NOT_FOUND), content summary for public buckets (top-level directory listing summary, sensitive file patterns observed), and test timestamp. Evidence template:

```text
Cloud asset recon for: TARGET.COM

S3 buckets:
  s3://target-assets → PUBLIC READ (listable)
    Contents: /images/, /css/, /js/, .env (1 file), config.json (1 file)
    → [HIGH] .env file publicly accessible — contains environment variables including database credentials.
    → [MEDIUM] config.json publicly accessible — application configuration.
  s3://target-backup → EXISTS (private) — access denied
  s3://target-dev → PUBLIC READ (listable)
    Contents: database.sql.gz (2.1 GB)
    → [CRITICAL] Full database backup publicly accessible.
  s3://target-prod → NOT_FOUND

Azure containers:
  https://targetcom.blob.core.windows.net/media → PUBLIC (listable)
    Contents: /uploads/, /profile-pictures/ (2,847 JPEG files)
    → [INFO] Public media container — user-uploaded content exposed but likely intended to be public.
  https://targetcom.blob.core.windows.net/backup → EXISTS (private)

GCP buckets:
  https://storage.googleapis.com/target-logs → PUBLIC (listable)
    Contents: access.log (1.2 GB), error.log (340 MB)
    → [HIGH] Application logs publicly accessible — may contain session tokens, PII, internal IPs.

Findings summary:
  CRITICAL: 1 (public database backup)
  HIGH: 2 (public .env, public application logs)
  MEDIUM: 1 (public config.json)
  INFO: 1 (public media container — probably intended)
```

Redact: file contents (record only file names and sizes for sensitive files), any credentials or tokens visible in file names, and bucket URLs that reveal internal project names not publicly associated with the target.

## Report handoff

1. `pentest_agent_record_finding` for each significant cloud exposure: public buckets containing sensitive files, writable buckets, publicly exposed configuration files, and database backups.
2. Package findings with: cloud-asset URL, permission status, content summary (file names and sizes, not contents), risk classification, and remediation recommendation.
3. Recommend: immediate takedown of public exposure (set bucket policy to private), rotation of all credentials exposed in public files, audit of bucket policies across all cloud accounts, enable S3 Block Public Access at account level, and implement CloudTrail logging for bucket access monitoring.
4. Explicitly note: all active probes used unsigned/no-auth requests only, no data was exfiltrated beyond test markers (immediately deleted), and no third-party buckets were probed.
