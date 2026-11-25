---
name: use-xoxno
description: Use the XOXNO JoAi app plugin when the task needs XOXNO tools or workflows.
---

# XOXNO

Connect XOXNO to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the XOXNO tools available in this app.
- Explain what setup or authentication XOXNO needs before I run an action.
- Use XOXNO to help me with the task I describe next.

## Action Inventory

- `xoxno-claim-rewards` (contract) — Claim your eGold (EGLD) staking rewards from XOXNO.
- `xoxno-liquid-stake` (contract) — Stake eGold using Xoxno liquid staking to earn rewards. Receive liquid staking tokens that represent your staked position and can be used in DeFi protocols while earning staking rewards.
- `xoxno-liquid-unstake` (contract) — Unstake liquid staking tokens to initiate the withdrawal process. You will receive unstake tokens that can be redeemed for eGold after the unbonding period. Instant withdrawals may be available if liquidity is sufficient.
- `xoxno-liquid-withdraw` (contract) — Withdraw your eGold after the unbonding period has passed. Send your unstake tokens to claim the underlying eGold. The unbonding period must be complete before withdrawal is possible.
- `xoxno-redelegate-egld` (contract) — Restake your eGold (EGLD) staking rewards with XOXNO.
- `xoxno-stake-egld` (contract) — Stake your EGLD with XOXNO, a leading NFT marketplace and validator on MultiversX. Earn staking rewards while supporting the team behind one of the blockchain's most active ecosystem projects.
- `xoxno-undelegate-egld` (contract) — Unstake your eGold (EGLD) you have previously staked with XOXNO.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
