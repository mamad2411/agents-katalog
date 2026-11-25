# TON Connect

Use this skill when a TON app needs a wallet session, a signed action, or a reliable reconnect flow.

## Inputs

- product surface and runtime environment
- wallet connection requirements
- transaction or message intent
- expected post-signature confirmation path

## Process

1. identify the exact user action that requires wallet state
2. define connect, reconnect, disconnect, and rejection behavior before writing UI code
3. prepare the smallest valid request the wallet must sign
4. tie session state updates to wallet events, not optimistic local guesses
5. show the user what happened after approval, rejection, or timeout

## Guardrails

- do not treat cached wallet data as proof that the user is still connected
- do not couple transaction preparation to visual components only
- do not hide approval-critical fields from the request being signed
- do not assume Telegram runtime quirks match a standalone browser

## Output

- a stable wallet session model
- a clear signed-action flow
- explicit failure handling for rejection, disconnect, and expired state
