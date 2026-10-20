---
name: secrets-in-prompts-detection
description: Review an AI system for credentials leaking into prompt context — covering API keys in system prompts, database connection strings in RAG chunks, access tokens in tool arguments, and exfiltration of secrets from context via prompt injection.
last_reviewed: 2026-04-29
---

# Secrets in Prompts Detection

## First Principle

**A secret that enters the prompt context is a secret that every future output of that model can potentially expose. The prompt is not a secure store. It is a working memory that the model can read, summarize, quote, and be manipulated into repeating.**

Secrets end up in prompts in three ways: deliberately (system prompts that inject API keys for tool use), accidentally (RAG chunks that include config files or .env excerpts), and through injection (an attacker causes the model to retrieve or generate a response that includes credentials from context). All three are vulnerabilities. The model does not protect secrets from its own outputs — it can be asked to repeat, translate, base64-encode, or embed them in seemingly unrelated responses.

## Attack Mental Model

1. **Direct extraction** — a user asks the model to repeat its system prompt, list its configuration, or describe what credentials it has access to. Without explicit protection, many models will comply.
2. **Indirect extraction via injection** — a prompt injection in retrieved content causes the model to include credentials from its context in an outbound API call, a generated document, or a tool argument.
3. **Accidental RAG chunk inclusion** — a document indexing pipeline ingests a config file, a Jupyter notebook with API keys, or an environment file. The key is then retrieved as relevant context and included in the prompt.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | System prompts are scanned for credential patterns before deployment. RAG ingestion pipelines scan every document for secrets before indexing. |
| **Scope** | Credentials needed for tool calls are injected at the tool-call layer — never in the system prompt where the model can read and potentially repeat them. |
| **Isolate** | The model's output is scanned for credential patterns before it is returned to the client. A response that contains a credential pattern is blocked and flagged. |
| **Enforce** | Secret scanning runs in CI on every commit that modifies system prompts, RAG corpus, or tool definitions. Failures block deployment. |

## SPD.1 System Prompt and RAG Corpus Secret Scanning

**The core vulnerability:** System prompts are stored in version control, configuration files, or databases — locations where secrets sometimes end up inadvertently. A system prompt that includes a database URL, an API key for a tool, or an environment variable interpolation that resolves to a secret gives the model direct access to that secret in its working context.

### Check

- Is the system prompt scanned for credential patterns (API key formats, connection strings, JWT-shaped tokens, AWS ARNs with key IDs) before deployment?
- Does the RAG ingestion pipeline scan every document for secrets before indexing — and reject or redact documents that contain credential patterns?
- Are there any tool definitions that include credentials inline — such as API keys passed as tool parameters in the tool schema definition?

### Action

- **Run a secret scanner on all system prompt content as part of CI:**

```bash
# Using truffleHog or detect-secrets
detect-secrets scan --baseline .secrets.baseline system_prompts/
trufflehog filesystem system_prompts/ --fail
```

Configure your CI pipeline to fail on any detected secret in the system prompt directory.

- **Apply secret scanning in the RAG ingestion pipeline.** Before any document is chunked and indexed, run it through a secret detector:

```python
import detect_secrets

def scan_for_secrets(text: str) -> list[dict]:
    detector = detect_secrets.SecretsCollection()
    detector.scan_file_content("document", text)
    return list(detector.json()["results"].get("document", []))

def safe_ingest(document_text: str, doc_id: str):
    findings = scan_for_secrets(document_text)
    if findings:
        log_secret_finding(doc_id, findings)
        raise SecretInDocumentError(f"Document {doc_id} contains potential secrets — not indexed")
```

- **Never include credentials in tool schema definitions.** Tool schemas define the tool's interface — not its credentials. Inject credentials at the tool execution layer, not in the schema passed to the model:

```python
# Wrong — key visible to model
tools = [{"name": "query_db", "api_key": "sk-real-key", ...}]

# Correct — key injected at execution, model sees only schema
def query_db(params: dict) -> str:
    api_key = secrets_manager.get("DB_API_KEY")  # injected at call time
    return db.query(params["query"], api_key=api_key)
```

### Failure Modes

- A system prompt includes `DB_URL=postgres://user:password@host/db` for documentation purposes. The model can repeat it verbatim if asked.
- A Jupyter notebook containing `OPENAI_API_KEY = "sk-..."` is ingested into the RAG corpus without secret scanning. A user asking about the notebook topic receives a response that includes the key.

## SPD.2 Output Secret Scanning and Exfiltration Prevention

**The core vulnerability:** Even if no secrets are present in the input context, a prompt injection can cause the model to retrieve credentials from a tool, generate plausible-looking fake credentials, or relay previously seen credentials from conversation history. Output scanning catches these cases before the response reaches the client.

### Check

- Is the model's output scanned for credential patterns before it is returned to the client?
- Is conversation history that may contain credentials cleared or redacted between sessions — so that a new session cannot retrieve credentials from prior session context?
- Are tool response payloads (which may contain API responses with tokens) scanned before being re-injected into the model's context?

### Action

- **Scan all model outputs for credential patterns before delivery:**

```python
import re

CREDENTIAL_PATTERNS = [
    r"(?i)(api[_-]?key|secret|token|password|passwd)\s*[=:]\s*['\"]?[\w\-]{16,}",
    r"sk-[a-zA-Z0-9]{20,}",                    # OpenAI-style keys
    r"AKIA[0-9A-Z]{16}",                        # AWS access key IDs
    r"eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}",  # JWTs
    r"(?i)bearer\s+[a-zA-Z0-9\-_.]{20,}",
]

def scan_output_for_secrets(output: str) -> list[str]:
    matches = []
    for pattern in CREDENTIAL_PATTERNS:
        matches.extend(re.findall(pattern, output))
    return matches

def deliver_response(raw_output: str) -> dict:
    secrets_found = scan_output_for_secrets(raw_output)
    if secrets_found:
        log_output_secret_detection(secrets_found)
        return {"error": "Response blocked — potential credential disclosure detected"}
    return {"response": raw_output}
```

- **Clear sensitive tool responses from context before the next turn.** If a tool returns a response containing credentials (an OAuth token, a session cookie, a temporary AWS credential), remove that tool response from the conversation history before the next user turn.

### Minimum Deliverable Per Review

- [ ] System prompt secret scan: automated scan in CI, failing on any credential pattern
- [ ] RAG corpus scan: pre-indexing secret detection on all ingested documents
- [ ] Tool schema audit: zero credentials in tool schema definitions
- [ ] Output scanning: credential pattern detection on all model responses before delivery
- [ ] Session history redaction: sensitive tool responses removed between sessions

## Quick Win

**Run `trufflehog filesystem ./system_prompts/` right now.** If it finds anything, that secret has been in your model's working context for every conversation that used that system prompt. Rotate the credential immediately and move it out of the prompt.

## References

- Data leakage prevention → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- RAG corpus integrity → [rag-security/SKILL.md](../rag-security/SKILL.md)
- Indirect injection vectors → [indirect-prompt-injection/SKILL.md](../indirect-prompt-injection/SKILL.md)
- Container and infra secrets → [container-ai-workload-security/SKILL.md](../container-ai-workload-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
