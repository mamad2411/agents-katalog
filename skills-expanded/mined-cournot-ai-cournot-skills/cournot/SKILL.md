---
name: cournot
description: Query Cournot probabilities and manage prepaid calls, balances, and API keys. Use only for /cournot or an explicit request to use Cournot, not for casual odds questions.
metadata:
  openclaw:
    homepage: https://skill.cournot.ai/
    requires:
      bins:
        - node
    envVars:
      - name: COURNOT_CREDENTIAL_DIR
        required: false
        description: Optional caller-configured private storage directory; defaults to ~/.cournot. Preserve its supplied value unchanged.
      - name: COURNOT_API_KEY
        required: false
        description: Optional key overriding the saved credentials for COURNOT_API_KEY_BASE; never required for anonymous use.
      - name: COURNOT_API_KEY_BASE
        required: false
        description: Origin that owns the environment key; defaults to interface.cournot.ai. Set explicitly for development keys.
      - name: COURNOT_API_BASE
        required: false
        description: Optional API base override for testing; defaults to interface.cournot.ai; use dev-interface.cournot.ai explicitly for development.
      - name: COURNOT_EVAL_ID
        required: false
        description: Optional evaluation identifier used only with a non-production API base.
      - name: COURNOT_WALLET_COMMAND
        required: false
        description: Optional compatible wallet command; defaults to baw when a paid request requires a wallet.
      - name: COURNOT_INTENT_DIR
        required: false
        description: Optional directory for short-lived payment intent files; defaults to the operating system temporary directory.
---

# Cournot

Use only for `/cournot` or an explicit request to use Cournot. Reply in the user's language. The API supplies the assessment and evidence; never invent a second estimate.

## Customer communication

Apply these principles silently to every customer-facing message, across queries, account operations, payments, recovery and troubleshooting. They govern how to write; they are not content to announce or explain to the customer:

- Ground the reply in the actual request and client result. Explain the current status, consequences for the user, and the next useful action. Distinguish a planned operation from a completed one; retain uncertainty when completion, payment or remaining calls is unconfirmed.
- Use the language of the user's actual request consistently in all replies, with ordinary product terms and clear units. Do not infer the customer's language from documentation, examples or tool-output language. In Chinese, use 密钥, 轮换, 次 and 最新付款预览 for their respective concepts. Preserve API evidence and market-title wording according to the query and response references. Brevity applies to explanatory prose, not to required result fields: do not omit data required by a response contract.
- Keep communication proportional to the decision. Acknowledge the current task briefly without narrating a plan or requesting authorization. Give further progress only when there is a meaningful update or delay. Present an available result or choice directly. Do not narrate internal reading, routing, validation, debugging, formatting or test activity, or repeat information without a user need. Keep the focus on the operation. Do not announce that you are following instructions, using a particular reply language, filtering information or withholding internal details; these are writing decisions, not task progress. Omit unrelated warnings.
- In confirmation requests, show information needed to understand or authorize the operation, such as its wallet, payment terms and effects.
- Keep API deployment details internal across all customer replies: do not display development/production/local environment labels, API origins or service URLs, including account results, pack choices, confirmations and errors. Payment networks and public payment terms remain decision-relevant and must still be shown.
- Collect only the input needed for the next step. A routine choice is distinct from payment or credential authorization; never invent or speak for the user's consent. Request authorization only after the client provides a concrete operation preview with the information needed to decide. A request to perform an operation already permits preparing its preview; do not insert preliminary authorization questions. When awaiting input, end the final reply with a direct question about the next decision, rather than telling the user what confirmation phrase to type. Keep explanations about the operation, quoting internal rules or paths only when the host requires it or the user explicitly asks; signing parameters remain excluded.

Before sending any customer-facing message, check it against these principles: every sentence must help the user understand the result, its consequences or the next decision; every status and authorization claim must have evidence from the client or the user. Remove process narration and statements made on the user's behalf. Apply this check to progress messages as well as the final reply.

Use [errors.md](references/errors.md) to interpret failures and uncertain outcomes under these same principles. Flow references define business facts and permitted actions, not fixed customer scripts.

## Route the request first

Read the applicable flow reference before acting on or explaining a client result. For follow-up questions, status explanations and troubleshooting, select the reference from the pending operation or returned action; do not treat them as new event queries or infer a workflow from a state name alone.

After removing `/cournot` and outer whitespace, match these complete commands. Do not interpret an event containing a reserved word as a management command.

| Input | Action / reference |
|---|---|
| `balance` | Read balance and masked key — [account.md](references/account.md) |
| `key` | Show the full key, or recover it using the wallet — [account.md](references/account.md) |
| `import <key>` | Validate and save an existing key — [account.md](references/account.md) |
| `rotate` | Preview rotation and its effect on the old key; execute only after confirmation — [account.md](references/account.md) |
| `topup` | Let the user select a pack, preview and confirm payment — [payment.md](references/payment.md) |
| Anything else | Event query — [query-flow.md](references/query-flow.md) |

For event queries only, also strip the optional `probability` prefix. The message is the user's event in their own words. If no claim with an asset, threshold, or date remains, ask for one without calling the API. Cournot has no mispricing API; explain this and stop on a mispricing request.

## Runtime and billing

Never expose signing payloads or protocol parameters in any reply, including troubleshooting: domain/types/primaryType, signing chainId, urlPath, nonce, signing timestamp, parsed signing messages and internal request/intent IDs remain inside the client. Do not reconstruct them for display. This boundary has no technical-details exception; it does not remove the public payment terms needed for informed confirmation.

Node.js 22.20 or newer is required. All API operations use `scripts/cournot-client.mjs`; credentials and wallet signatures stay inside the client. The default is **production**, `https://interface.cournot.ai`. `COURNOT_API_BASE=https://dev-interface.cournot.ai` selects development. Never silently change environments to work around a failure. API deployment and payment network are separate: dev payments can still transfer real mainnet assets.

Each IP has **three free probability calls in total, with no reset**. Free allowance is used before prepaid calls. No key or wallet is required to start. After free calls, a configured key spends prepaid balance; otherwise the user chooses topup, import, or $0.01 per-call payment. Packs do not expire, stack, and are non-refundable. Prices and call counts come from the client's pack catalog; actual payment terms come from the server's 402 response.

One user query permits one probability assessment, including free and prepaid calls. A confirmed 402 replay is part of that same assessment. Do not repeat completed account operations merely to verify the same result. The client waits three seconds before each initial paid submission and checks readable authorization expiry before and after waiting. It may internally retry the same signed payment once after an explicit authorization-not-yet-valid precheck rejection, within the original confirmed payment; see [payment.md](references/payment.md). No other automatic retries, background queries, automatic topup, or silent fallback from prepaid balance to per-call payment. Keep pending event text and selected market ids through disambiguation, credential setup, and payment confirmation. A completed topup does not automatically rerun the pending query.

`COURNOT_API_KEY` overrides the file only for `COURNOT_API_KEY_BASE` (production by default; set explicitly for development keys). Otherwise the client reads a per-origin file beneath `~/.cournot/credentials/`. Files are plaintext protected by filesystem permissions, not an encrypted vault. Never read or edit them through the model. Use client commands for import, saving, recovery, and display. Only explicit `/cournot key` may reveal a complete key; all other output must remain masked. Never request wallet private keys or seed phrases.

On a successful probability response, read [response-format.md](references/response-format.md). Report the returned billing route and remaining calls; `charged=false` does not mean no prepaid call was consumed. Never manufacture a missing quota, promise a daily reset, or promise no deduction after an uncertain server failure.

Claude Code, Codex, Grok, OpenClaw, and other Agent Skills hosts use this same folder. Install the entire `skills/cournot/` folder, including scripts and references.
