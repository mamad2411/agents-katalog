---
name: s3-artifact-stage-verify
description: Stage a private artifact into S3, verify the object path and metadata, and produce the host-side fetch or consume steps with durable evidence. Use for repeated private-lane delivery of images, tarballs, bootstrap assets, and validation artifacts.
---

# S3 Artifact Stage Verify

Use this skill for the repeated private artifact delivery loop around S3.

## Use when

- uploading image tarballs or bootstrap assets to S3
- verifying the final object path before host-side use
- generating the exact fetch path for EC2, ECS, or validation hosts
- saving durable evidence for artifact delivery

## Preferred workflow

1. Define the exact S3 destination key.
2. Upload the artifact.
3. Verify:
   - bucket
   - key
   - size
   - last modified
4. Save the host-side fetch command or expected consume path.
5. Record whether the artifact is:
   - upload only
   - ready for host fetch
   - ready for runtime consume

## Typical AWS CLI pattern

```bash
aws s3 cp ...
aws s3 ls ...
aws s3api head-object ...
```

## Save evidence under

```bash
~/.AGENTS-temp/<repo>/s3-artifact-stage-verify/<timestamp>/
```

## Rules

- use deterministic object keys
- save the exact final S3 URI in evidence
- do not assume upload succeeded without a metadata check
- prefer private-bucket delivery evidence over chat-only statements
- use this skill before host-side bootstrap or `docker load` workflows when
  S3 is the delivery path

## Related skills

- `ssm-command-evidence`
- `gitlab-triage`
