# AI Guardrails

Evaluate AI prompts and conversations against Trend Micro Vision One AI security policies. This skill helps detect and block harmful content, prompt injection attacks, sensitive data exposure, and other AI-specific threats in LLM applications.

## Instructions

1. When the user wants to evaluate prompts, check for harmful content, or validate AI inputs/outputs, use this skill to apply AI guardrails.

2. **Identify the request type**: Determine whether you're evaluating:
   - A simple text prompt (`SimpleRequestGuard`)
   - An OpenAI chat completion request (`OpenAIChatCompletionRequestV1`)
   - An OpenAI chat completion response (`OpenAIChatCompletionResponseV1`)

3. **Provide application context**: Always specify the `applicationName` parameter to identify which AI application's prompts are being evaluated.

4. **Choose response detail level**: Use the `prefer` parameter to control output verbosity:
   - `return=representation` - Full evaluation with harmful content details, sensitive info, and prompt attack analysis
   - `return=minimal` - Concise response with just action and reasons

5. **Interpret results**: The tool returns:
   - **Action**: `Allow` or `Block`
   - **Reasons**: Explanation for any policy violations detected

6. **Handle blocked content**: When content is blocked, explain which policies were violated and suggest alternatives.

## Tools

This skill uses the following Vision One MCP tools:

| Tool | Purpose |
|------|---------|
| `aisecurity_guardrails_apply` | Evaluate prompts against AI guard policies and return Allow/Block recommendations |

## Request Types

### SimpleRequestGuard
Use for evaluating a single text prompt (max 1024 characters):
```json
{
  "applicationName": "my-ai-app",
  "requestType": "SimpleRequestGuard",
  "prompt": "User's prompt text here",
  "prefer": "return=representation"
}
```

### OpenAIChatCompletionRequestV1
Use for evaluating OpenAI-style chat messages:
```json
{
  "applicationName": "my-ai-app",
  "requestType": "OpenAIChatCompletionRequestV1",
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User message"},
    {"role": "assistant", "content": "Assistant response"}
  ],
  "prefer": "return=representation"
}
```

### OpenAIChatCompletionResponseV1
Use for evaluating AI-generated responses before returning to users.

## Common Workflows

### Prompt Validation
1. Receive user prompt for evaluation
2. Call `aisecurity_guardrails_apply` with `SimpleRequestGuard` request type
3. Check the action (Allow/Block)
4. If blocked, report policy violations to the user
5. If allowed, confirm the prompt passed security checks

### Chat Conversation Evaluation
1. Collect the full conversation history (system, user, assistant messages)
2. Call `aisecurity_guardrails_apply` with `OpenAIChatCompletionRequestV1` request type
3. Analyze the response for any detected threats
4. Report findings including harmful content, sensitive data, or prompt attacks

### Security Testing
1. Prepare test prompts including edge cases
2. Evaluate each prompt against guardrails
3. Document which prompts are blocked and why
4. Verify policies are correctly configured

### Response Filtering
1. Capture AI-generated response before delivery
2. Evaluate response with `OpenAIChatCompletionResponseV1` request type
3. Block responses containing harmful or sensitive content
4. Allow safe responses to pass through

## Output Format

When presenting guardrail evaluation results:

```
## AI Guardrails Evaluation

**Application**: [Application Name]
**Request Type**: [SimpleRequestGuard/OpenAIChatCompletionRequestV1/OpenAIChatCompletionResponseV1]

### Decision
**Action**: [Allow/Block]

### Policy Evaluation
[If blocked or issues detected:]
- **Harmful Content**: [Detected/Not Detected] - [Details]
- **Sensitive Information**: [Detected/Not Detected] - [Details]
- **Prompt Attacks**: [Detected/Not Detected] - [Details]

### Reasons
[List of reasons for the decision]

### Recommendations
[Suggested actions if content was blocked]
```

## Detection Categories

The AI guardrails evaluate content for:

| Category | Description |
|----------|-------------|
| **Harmful Content** | Violence, hate speech, self-harm, illegal activities |
| **Sensitive Information** | PII, credentials, financial data, health records |
| **Prompt Attacks** | Injection attempts, jailbreaks, role manipulation |
| **Policy Violations** | Custom organization-specific policy breaches |

## Security Considerations

- This skill helps protect AI applications from misuse and data leakage
- Guardrail policies should be configured in Vision One console before use
- Results depend on the policies configured for your organization
- Use detailed responses (`return=representation`) during development and testing
- Use minimal responses (`return=minimal`) in production for efficiency
- Application names should be consistent to enable proper tracking and analytics
- Blocked content should be logged for security monitoring and policy refinement
- Regular testing with adversarial prompts helps validate guardrail effectiveness
