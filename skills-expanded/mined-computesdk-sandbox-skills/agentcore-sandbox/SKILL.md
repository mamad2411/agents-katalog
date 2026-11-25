---
name: agentcore-sandbox
description: Guide for creating and managing AWS Bedrock AgentCore Code Interpreter sandboxes using ComputeSDK. Use when building applications that need AWS Bedrock AgentCore Code Interpreter provider for ComputeSDK - secure, session-based code execution sandboxes.
---

# AWS Bedrock AgentCore Code Interpreter Sandboxes with ComputeSDK

AWS Bedrock AgentCore Code Interpreter provider for ComputeSDK - secure, session-based code execution sandboxes.

## Setup

```bash
npm install computesdk @computesdk/agentcore
```

Set your credentials:

```bash
# .env
AWS_REGION=your_aws_region
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { agentcore } from '@computesdk/agentcore';

compute.setConfig({
  provider: agentcore({
    region: process.env.AWS_REGION,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from AWS Bedrock AgentCore Code Interpreter!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { agentcore } from '@computesdk/agentcore';

const sdk = agentcore({
    region: process.env.AWS_REGION,
  });
const sandbox = await sdk.sandbox.create();
```

## AWS Bedrock AgentCore Code Interpreter Configuration

```typescript
interface AgentCoreConfig {

  /** AWS region (e.g. 'us-west-2'). Falls back to AWS_REGION / AWS_DEFAULT_REGION. */
  region?: string;
  /**
   * Code interpreter to use. Defaults to the managed `aws.codeinterpreter.v1`.
   * Pass a custom interpreter id/ARN to use one created via the control plane.
   */
  codeInterpreterIdentifier?: string;
  /** Named profile from your AWS config/credentials files. */
  profile?: string;
  /** Explicit credentials. If omitted, the default AWS credential chain is used. */
  credentials?: AwsCredentialIdentity | AwsCredentialIdentityProvider;
  /** Session idle timeout in seconds (max 28800 / 8h). Overridden by per-create `timeout`. */
  sessionTimeoutSeconds?: number;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
