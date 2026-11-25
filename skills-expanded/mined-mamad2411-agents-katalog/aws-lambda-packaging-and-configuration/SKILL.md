---
name: aws-lambda-packaging-and-configuration
description: >
  Packages an AWS Lambda function as a zip deployment package or container
  image, tunes memory/timeout/ephemeral storage, mitigates cold starts, and
  scopes the function's IAM execution role to least privilege. Use when the
  user asks to "package a Lambda function," "build a container image for
  Lambda," "reduce Lambda cold start latency," "tune Lambda memory or
  timeout," "add a Lambda layer," or "scope down a Lambda execution role."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# AWS Lambda Packaging and Configuration

## Purpose

A Lambda function's runtime behavior — how fast it starts, how much it
costs per invocation, and what it can access — is determined almost
entirely by decisions made at packaging and configuration time, not by
application code. Choosing zip vs. container image affects size limits and
build tooling; memory affects allocated CPU (not just RAM); and the
execution role's IAM policy determines the function's real security
blast radius. Getting these wrong doesn't usually fail fast — it shows up
later as throttling under load, unexplained latency, or an over-permissioned
function nobody scoped down after the initial "just get it working" deploy.

## When to use

- Packaging a new Lambda function and deciding between a zip deployment
  package and a container image (e.g. because of native binary dependencies,
  large ML libraries, or an existing container build pipeline).
- Tuning a function's memory, timeout, or ephemeral storage (`/tmp`) size
  for a workload that is timing out, running out of disk, or costing more
  than expected.
- Diagnosing or mitigating cold-start latency for a latency-sensitive
  synchronous workload (API Gateway/ALB-fronted functions, user-facing
  paths).
- Writing or reviewing a Lambda execution role's IAM policy, especially
  when someone has broadened it to unblock a deploy.
- Adding a Lambda layer for shared dependencies across multiple functions.
- Deciding whether a function needs VPC attachment at all, and if so,
  configuring it without starving cold-start latency or IP capacity.

## Prerequisites & environment

- AWS CLI v2 or an IaC tool (SAM, CDK, Terraform, CloudFormation) with
  permissions to create/update Lambda functions, IAM roles, and (for
  container images) push to Amazon ECR.
- For container image packaging: Docker (or another OCI-compatible
  builder) and an ECR repository the build can push to.
- Know your runtime's supported version at deploy time — AWS deprecates
  Lambda runtimes on a schedule (e.g. `python3.9`, `nodejs16.x` reach
  end-of-support over time); check `aws lambda list-runtimes` equivalent
  guidance in the AWS docs rather than assuming a version is still
  supported.
- A dedicated IAM execution role per function (or per closely related
  group of functions) — never a single shared "lambda-role" reused across
  unrelated functions.

## Step-by-step guidance

1. **Choose zip vs. container image packaging deliberately, not by
   default.** A zip deployment package is simplest for small,
   pure-language-runtime functions and deploys faster; it's capped at 50 MB
   zipped (via direct upload — larger via S3) and 250 MB unzipped including
   any layers. A container image (via ECR) supports up to 10 GB and is the
   better fit when you have large dependencies (ML frameworks, native
   binaries compiled for the target architecture) or want to reuse an
   existing container build/scan pipeline:
   ```dockerfile
   FROM public.ecr.aws/lambda/python:3.12
   COPY requirements.txt ${LAMBDA_TASK_ROOT}
   RUN pip install -r requirements.txt -t ${LAMBDA_TASK_ROOT}
   COPY app.py ${LAMBDA_TASK_ROOT}
   CMD ["app.handler"]
   ```
   ```bash
   docker build -t my-fn:latest .
   aws ecr get-login-password --region <REGION> \
     | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
   docker tag my-fn:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/my-fn:latest
   docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/my-fn:latest
   ```

2. **Create the function with an explicit, least-privilege execution
   role** — never attach a broad managed policy like administrator access
   "to make it work":
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       { "Effect": "Allow", "Principal": { "Service": "lambda.amazonaws.com" }, "Action": "sts:AssumeRole" }
     ]
   }
   ```
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       { "Effect": "Allow", "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], "Resource": "arn:aws:logs:<REGION>:<AWS_ACCOUNT_ID>:log-group:/aws/lambda/my-fn:*" },
       { "Effect": "Allow", "Action": ["s3:GetObject"], "Resource": "arn:aws:s3:::my-input-bucket/uploads/*" },
       { "Effect": "Allow", "Action": ["dynamodb:PutItem", "dynamodb:GetItem"], "Resource": "arn:aws:dynamodb:<REGION>:<AWS_ACCOUNT_ID>:table/my-fn-state" }
     ]
   }
   ```
   ```bash
   aws lambda create-function \
     --function-name my-fn \
     --package-type Zip \
     --runtime python3.12 \
     --handler app.handler \
     --role arn:aws:iam::<AWS_ACCOUNT_ID>:role/my-fn-execution-role \
     --zip-file fileb://function.zip \
     --memory-size 512 \
     --timeout 10 \
     --architectures arm64
   ```

3. **Tune memory deliberately — memory also determines allocated CPU**,
   not just available RAM. Lambda allocates CPU proportionally to the
   configured memory (128 MB–10,240 MB, in 1 MB increments); a
   CPU-bound function that "should have enough RAM" can still be slow
   simply because it's under-provisioned on CPU. Raising memory is often
   the correct fix for a slow-but-not-memory-hungry function, and because
   billing is duration × memory, a higher memory setting can sometimes
   *lower* total cost by finishing faster.

4. **Set timeout and ephemeral storage to match the actual workload**, not
   the default (`3` seconds timeout, `512` MB `/tmp`). Timeout ranges from
   1 to 900 seconds (15 minutes); ephemeral storage is configurable up to
   10,240 MB:
   ```bash
   aws lambda update-function-configuration \
     --function-name my-fn \
     --timeout 30 \
     --ephemeral-storage Size=2048
   ```

5. **Mitigate cold starts for latency-sensitive paths**, in order of
   impact: keep the deployment package/image small and dependency-light;
   initialize SDK clients, DB connections, and other reusable state
   *outside* the handler function body so they're reused across
   invocations within the same execution environment; avoid attaching the
   function to a VPC unless it genuinely needs to reach a private resource
   (VPC attachment adds networking setup overhead, though AWS's
   Hyperplane ENI model has reduced this compared to older
   one-ENI-per-invocation behavior); and for functions where p99 latency
   on the *first* invocation genuinely matters, enable Provisioned
   Concurrency:
   ```bash
   aws lambda put-provisioned-concurrency-config \
     --function-name my-fn \
     --qualifier prod \
     --provisioned-concurrent-executions 5
   ```
   Provisioned Concurrency must target a published version or alias, not
   `$LATEST` — plan a versioning/alias strategy alongside it.

6. **Use Lambda layers for shared dependencies across multiple functions**,
   not for every dependency in every function — a layer is a versioned zip
   of libraries mounted at `/opt`, counted against the same 250 MB
   unzipped limit as function code:
   ```bash
   aws lambda publish-layer-version \
     --layer-name shared-utils \
     --zip-file fileb://layer.zip \
     --compatible-runtimes python3.12
   ```

## Best practices

- Prefer `arm64` (Graviton) architecture for new functions where the
  runtime and dependencies support it — AWS documents it as generally
  offering better price-performance than `x86_64`; verify any native
  binary dependencies are built for the target architecture.
- Give each function (or tightly related group) its own execution role
  scoped to the specific resource ARNs it touches — a shared "does
  everything" role defeats least privilege and makes blast radius
  analysis impossible after an incident.
- Version functions and use aliases (`prod`, `staging`) as the stable
  target for Provisioned Concurrency and downstream integrations, rather
  than pointing everything at the mutable `$LATEST`.
- Keep container image layers cached and minimal (multi-stage builds,
  `.dockerignore`) — a bloated image slows both cold starts and CI build
  times.
- Treat memory tuning as a data-driven exercise: use AWS Lambda Power
  Tuning or CloudWatch duration/cost metrics across a few memory settings
  rather than guessing a round number.

## Common pitfalls

- **Symptom:** A CPU-bound function intermittently times out or runs
  slowly even though it never approaches its memory limit.
  **Fix:** Increase memory anyway — CPU is allocated proportionally to
  memory, so a function with plenty of spare RAM can still be
  CPU-starved; re-test duration at a higher memory setting rather than
  assuming memory headroom means CPU headroom too.

- **Symptom:** First invocation after an idle period is noticeably slower
  than steady-state invocations, especially for a VPC-attached function
  with a large deployment package.
  **Fix:** Trim the package/image, move client/connection initialization
  outside the handler, drop VPC attachment if the function doesn't
  actually need private-network access, and enable Provisioned Concurrency
  for the specific alias serving latency-sensitive traffic.

- **Symptom:** The execution role was broadened to
  `"Action": "*", "Resource": "*"` (or a broad managed policy attached)
  during troubleshooting "to make it work," and never scoped back down.
  **Fix:** Treat this as a real security finding, not a shortcut — replace
  it with the specific actions and resource ARNs the function actually
  calls, verified against CloudTrail if it's unclear what the function
  uses.

- **Symptom:** `aws lambda create-function` (or CI upload) fails with a
  package-too-large error.
  **Fix:** Zip direct-upload is capped at 50 MB; upload to S3 first and
  reference `S3Bucket`/`S3Key`, or switch to container image packaging
  (10 GB limit) if dependencies are inherently large.

- **Symptom:** The function works locally but fails at runtime with an
  import/native-library-load error.
  **Fix:** A native dependency was built for the wrong CPU architecture —
  rebuild dependencies (or the container image) for the same architecture
  configured on the function (`arm64` vs `x86_64`).

## Worked example

**Scenario:** An image-processing function (Python, Pillow, with native
image-codec bindings) needs to resize uploaded images from S3 and write
results to DynamoDB, with low p99 latency for a user-facing upload flow.

Packaging: native Pillow dependencies make a container image the better
fit, built `FROM public.ecr.aws/lambda/python:3.12`, pushed to ECR as
shown in step 1.

Configuration:
```bash
aws lambda create-function \
  --function-name image-resizer \
  --package-type Image \
  --code ImageUri=<AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/image-resizer:latest \
  --role arn:aws:iam::<AWS_ACCOUNT_ID>:role/image-resizer-execution-role \
  --memory-size 1769 \
  --timeout 15 \
  --ephemeral-storage Size=1024 \
  --architectures arm64
```
`1769` MB was chosen deliberately — it's the point at which Lambda
allocates the equivalent of one full vCPU, and testing across a few
memory settings showed it minimized duration × cost for this CPU-bound
resize operation. The execution role (step 2 pattern) is scoped to
`s3:GetObject` on `arn:aws:s3:::uploads-bucket/incoming/*` and
`dynamodb:PutItem`/`GetItem` on the single results table — not full S3 or
DynamoDB access.

Cold-start mitigation: a `prod` alias points at the current published
version, with Provisioned Concurrency of `3` on that alias so the
user-facing upload path never pays a cold start during business hours;
a lower-traffic `batch` alias (used for a nightly reprocessing job) has no
provisioned concurrency, since occasional cold starts there are
acceptable.

Before this configuration ships, run it through
[aws-lambda-configuration-validation](../aws-lambda-configuration-validation/SKILL.md)
to confirm the reserved/provisioned concurrency numbers don't starve the
account's shared concurrency pool and that the environment variables and
role policy don't regress.

## Cross-references

- [aws-lambda-configuration-validation](../aws-lambda-configuration-validation/SKILL.md) — pre-deploy checks (reserved concurrency budget, VPC subnet capacity, IAM scope) for the configuration produced here.
- [azure-functions-configuration](../azure-functions-configuration/SKILL.md) — equivalent packaging/hosting-plan decisions and cold-start tradeoffs on Azure.
- [google-cloud-functions-configuration](../google-cloud-functions-configuration/SKILL.md) — equivalent packaging and scaling configuration on Google Cloud Functions Gen1/Gen2.
