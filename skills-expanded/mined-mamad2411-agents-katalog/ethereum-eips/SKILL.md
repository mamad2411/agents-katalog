---
name: ethereum-eips
description: >-
  Ethereum EIPs: implement ERC-20 tokens, EIP-712 typed signing, ERC-4337 account abstraction, EIP-1193 providers and ERC-8004 agents. Covers ERC-20, EIP-712, ERC-4337, EIP-1193, ERC-8004. Use when implementing ERC-20, EIP-712, ERC-4337, EIP-1193, or ERC-8004. Triggers: ERC-20, EIP-712, ERC-4337, EIP-1193, ERC-8004.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Ethereum EIPs

Five Ethereum Improvement Proposals read from their Markdown source: ERC-20 (token standard), ERC-4337 (account abstraction using an alt mempool) and ERC-8004 (trustless agents) from the ethereum/ERCs repository, and EIP-712 (typed structured data hashing and signing) and EIP-1193 (Ethereum provider JavaScript API) from the ethereum/EIPs repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Token or smart contract author, wallet or provider implementer, ERC-4337 bundler, paymaster or account developer, or an ERC-8004 agent, client or validator.
- Target version: ERC-20 (current); EIP-712 (current); ERC-4337 (current); EIP-1193 (current); ERC-8004 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **ERC-20 Methods.** "Callers MUST handle `false` from `returns (bool success)`. Callers MUST NOT assume that `false` is never returned!"
2. **ERC-20 transfer.** "_Note_ Transfers of 0 values MUST be treated as normal transfers and fire the `Transfer` event."
3. **EIP-712 Definition of encodeType.** "If the struct type references other struct types (and these in turn reference even more struct types), then the set of referenced struct types is collected, sorted by name and appended to the encoding."
4. **EIP-712 Definition of domainSeparator.** "The user-agent _should_ refuse signing if it does not match the currently active chain."
5. **EIP-712 Replay attacks.** "It is _very important_ that implementers make sure the application behaves correctly when it sees the same signed message twice."
6. **ERC-4337 The UserOperation structure.** "To prevent replay attacks, either cross-chain or with multiple `EntryPoint` contract versions, the `signature` MUST depend on `chainid` and the `EntryPoint` address."
7. **ERC-4337 Smart Contract Account Interface.** "MUST validate the caller is a trusted `EntryPoint`"
8. **ERC-4337 Required EntryPoint contract functionality.** "A node/bundler MUST reject a `UserOperation` that fails the validation, meaning not adding it to the local mempool and not propagating it to other peers."
9. **EIP-1193 request.** "The Promise **MUST NOT** resolve with any RPC protocol-specific response objects, unless the RPC method's return type is so defined."
10. **EIP-1193 connect.** "If the Provider becomes connected, the Provider **MUST** emit the event named `connect`."
11. **ERC-8004 Agent URI and Agent Registration File.** "The _agentURI_ MUST resolve to the agent registration file."
12. **ERC-8004 Giving Feedback.** "The feedback submitter MUST NOT be the agent owner or an approved operator for _agentId_."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `json`, `jwt`, `did`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [ERC-20: Token Standard](https://raw.githubusercontent.com/ethereum/ERCs/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-20.md): Final, ethereum/ERCs commit 365b4c0, 2026-10-02, checked 2026-10-06.
- [EIP-712: Typed structured data hashing and signing](https://raw.githubusercontent.com/ethereum/EIPs/3b5f9676205139c72da3e80774a8f5f27b911072/EIPS/eip-712.md): Final, ethereum/EIPs commit 3b5f967, 2026-10-06, checked 2026-10-06.
- [ERC-4337: Account Abstraction Using Alt Mempool](https://raw.githubusercontent.com/ethereum/ERCs/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-4337.md): Final, ethereum/ERCs commit 365b4c0, 2026-10-02, checked 2026-10-06.
- [EIP-1193: Ethereum Provider JavaScript API](https://raw.githubusercontent.com/ethereum/EIPs/3b5f9676205139c72da3e80774a8f5f27b911072/EIPS/eip-1193.md): Final, ethereum/EIPs commit 3b5f967, 2026-10-06, checked 2026-10-06.
- [ERC-8004: Trustless Agents](https://raw.githubusercontent.com/ethereum/ERCs/365b4c02879f3e882b91281d42b4f57b406205e9/ERCS/erc-8004.md): Draft, ethereum/ERCs commit 365b4c0, 2026-10-02, checked 2026-10-06.
