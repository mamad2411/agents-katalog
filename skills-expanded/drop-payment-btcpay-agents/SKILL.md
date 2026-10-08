# AGENTS.md — drop-payment-btcpay

BTCPay Server cryptocurrency payment gateway plugin for Drop indie commerce
(#21).

## Toolchain

- Node >= 22, npm 10+
- `npm ci`, `npm run build`, `npm test`, `npm run typecheck`

## Contract

Built on [`@droposs/plugin-sdk`](https://www.npmjs.com/package/@droposs/plugin-sdk)
(plugin API v2, `^0.4.0` from the npm registry).

## Security invariants

- No placeholder base URL: `createPaymentIntent` throws until `apiBaseUrl`
  (storage) or `BTCPAY_BASE_URL` (env) points at a real deployment.
- `handleWebhook` verifies `BTCPay-Sig` before parsing: HMAC-SHA256 over the
  raw body, constant-time compare, and fails closed when the webhook secret is
  absent.
- Unsupported event types throw; they are never defaulted to `succeeded`.
- Uses only `node:crypto`; no new dependencies.
- The host must supply the raw webhook body for signatures to validate.
