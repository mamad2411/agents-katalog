---
name: interswitch-setup
description: >-
  Set up the Interswitch API client, environment variables, OAuth 2.0 authentication,
  and TypeScript helpers for server-side payment integration. Use this skill whenever
  starting a new Interswitch integration, configuring API keys, creating a reusable
  fetch wrapper, or setting up the foundation for any Interswitch feature. Also use
  when you see errors related to missing CLIENT_ID, SECRET_KEY, authentication failures,
  or need to understand Interswitch's base URLs, passport OAuth flow, response format,
  currencies, or environment switching (test/live).
---

# Interswitch Setup

Set up the foundational Interswitch API client, OAuth 2.0 authentication, and environment configuration for TypeScript/JavaScript server-side applications.

## API Fundamentals

| Property | Value |
| --- | --- |
| Test Passport URL | `https://passport.k8.isw.la/passport/oauth/token` |
| Live Passport URL | `https://passport.interswitchng.com/passport/oauth/token` |
| Test Collections URL | `https://qa.interswitchng.com` |
| Live Collections URL | `https://interswitchng.com` |
| Test Web Checkout URL | `https://newwebpay.qa.interswitchng.com` |
| Live Web Checkout URL | `https://newwebpay.interswitchng.com` |
| Auth Method | OAuth 2.0 Client Credentials |
| Content Type | `application/json` |
| Amount Unit | **Minor currency** (kobo for NGN — multiply amount × 100) |
| Currency Code | `566` (NGN), `840` (USD) |

## Environment Variables

Create a `.env` file:

```env
# Environment: 'test' or 'live'
INTERSWITCH_ENV=test

# General Integration Credentials
TEST_CLIENT_ID=IKIAB23A4E2756605C1ABC33CE3C287E27267F660D61
TEST_SECRET_KEY=secret
TEST_MERCHANT_CODE=MX6072

# Card Payment API Credentials (separate set)
CARD_API_CLIENT_ID=IKIA3B827951EA3EC2E193C51DA1D22988F055FD27DE
CARD_API_SECRET_KEY=ajkdpGiF6PHVrwK
CARD_API_MERCHANT_CODE=MX21696
CARD_API_PAY_ITEM_ID=4177785

# Live credentials (get from Quickteller Business dashboard)
LIVE_CLIENT_ID=your_live_client_id
LIVE_SECRET_KEY=your_live_secret_key
LIVE_MERCHANT_CODE=your_live_merchant_code

# Optional
PAY_ITEM_ID=9405967
DEFAULT_WALLET_PIN=1234
```

The CLIENT_ID and SECRET_KEY must NEVER appear in client-side code or public repositories. Get live credentials from [Quickteller Business Dashboard](https://business.quickteller.com/developertools).

## OAuth 2.0 Authentication

Interswitch uses OAuth 2.0 Client Credentials flow. Encode `clientId:secretKey` as Base64 and POST to the passport endpoint:

```typescript
interface InterswitchConfig {
  env: 'test' | 'live';
  clientId: string;
  secretKey: string;
  merchantCode: string;
  passportUrl: string;
  collectionsBaseUrl: string;
  walletBaseUrl: string;
}

function getConfig(): InterswitchConfig {
  const isLive = process.env.INTERSWITCH_ENV === 'live';
  return {
    env: isLive ? 'live' : 'test',
    clientId: isLive
      ? process.env.LIVE_CLIENT_ID!
      : process.env.TEST_CLIENT_ID!,
    secretKey: isLive
      ? process.env.LIVE_SECRET_KEY!
      : process.env.TEST_SECRET_KEY!,
    merchantCode: isLive
      ? process.env.LIVE_MERCHANT_CODE!
      : process.env.TEST_MERCHANT_CODE!,
    passportUrl: isLive
      ? 'https://passport.interswitchng.com/passport/oauth/token'
      : 'https://passport.k8.isw.la/passport/oauth/token',
    collectionsBaseUrl: isLive
      ? 'https://interswitchng.com'
      : 'https://qa.interswitchng.com',
    walletBaseUrl: isLive
      ? 'https://interswitchng.com'
      : 'https://qa.interswitchng.com',
  };
}
```

## Generate Access Token

```typescript
interface AccessTokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  scope: string;
  merchant_code: string;
  requestor_id: string;
  payable_id: string;
  jti: string;
}

async function generateAccessToken(): Promise<AccessTokenResponse> {
  const config = getConfig();
  const credentials = Buffer.from(
    `${config.clientId}:${config.secretKey}`
  ).toString('base64');

  const response = await fetch(
    `${config.passportUrl}?grant_type=client_credentials`,
    {
      method: 'POST',
      headers: {
        Authorization: `Basic ${credentials}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }
  );

  if (!response.ok) {
    throw new Error(`Auth failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
```

## Reusable Auth Headers

```typescript
async function getAuthHeaders(): Promise<Record<string, string>> {
  const token = await generateAccessToken();
  return {
    Authorization: `Bearer ${token.access_token}`,
    'Content-Type': 'application/json',
  };
}
```

## Collections Passport (Passport v2)

Some endpoints (wallet-pay, split settlement) use a separate passport-v2 token:

```typescript
async function generateCollectionsAccessToken(): Promise<AccessTokenResponse> {
  const config = getConfig();
  const isLive = config.env === 'live';

  const splitPassportUrl = isLive
    ? 'https://passport.interswitchng.com/passport-v2/oauth/token'
    : 'https://passport.k8.isw.la/passport-v2/oauth/token';

  const credentials = Buffer.from(
    `${config.clientId}:${config.secretKey}`
  ).toString('base64');

  const response = await fetch(
    `${splitPassportUrl}?grant_type=client_credentials`,
    {
      method: 'POST',
      headers: {
        Authorization: `Basic ${credentials}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }
  );

  if (!response.ok) {
    throw new Error(`Collections auth failed: ${response.status}`);
  }

  return response.json();
}
```

## Generic API Request Helper

```typescript
async function interswitchRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  useCollectionsAuth = false
): Promise<T> {
  const config = getConfig();
  const headers = useCollectionsAuth
    ? await getCollectionsAuthHeaders()
    : await getAuthHeaders();

  const url = endpoint.startsWith('http')
    ? endpoint
    : `${config.collectionsBaseUrl}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: { ...headers, ...options.headers },
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Interswitch API error ${response.status}: ${errorBody}`);
  }

  return response.json();
}

async function getCollectionsAuthHeaders(): Promise<Record<string, string>> {
  const token = await generateCollectionsAccessToken();
  return {
    Authorization: `Bearer ${token.access_token}`,
    'Content-Type': 'application/json',
  };
}
```

## Token Caching

Cache tokens to avoid unnecessary passport calls:

```typescript
let cachedToken: { token: AccessTokenResponse; expiresAt: number } | null = null;

async function getCachedAccessToken(): Promise<string> {
  const now = Date.now();
  if (cachedToken && cachedToken.expiresAt > now) {
    return cachedToken.token.access_token;
  }

  const token = await generateAccessToken();
  cachedToken = {
    token,
    expiresAt: now + token.expires_in * 1000 - 60000, // 1 min buffer
  };

  return token.access_token;
}
```

## InterswitchAuth (Legacy)

Some legacy endpoints use InterswitchAuth headers instead of OAuth:

```typescript
import crypto from 'crypto';

function getInterswitchAuthHeaders(
  httpMethod: string,
  resourceUrl: string,
  clientId: string,
  secretKey: string
): Record<string, string> {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const nonce = crypto.randomUUID();
  const signatureCipher = `${httpMethod}&${encodeURIComponent(resourceUrl)}&${timestamp}&${nonce}&${clientId}&${secretKey}`;
  const signature = crypto
    .createHash('sha512')
    .update(signatureCipher)
    .digest('base64');

  return {
    Authorization: `InterswitchAuth ${Buffer.from(clientId).toString('base64')}`,
    Timestamp: timestamp,
    Nonce: nonce,
    Signature: signature,
    SignatureMethod: 'SHA512',
    'Content-Type': 'application/json',
  };
}
```

## Developer Resources

| Resource | URL |
| --- | --- |
| API Documentation | https://docs.interswitchgroup.com/docs/home |
| API Reference | https://isw-api.readme.io/reference |
| Developer Console | https://developer.interswitchgroup.com/ |
| Quickteller Business | https://business.quickteller.com |
| Developer Community (Slack) | https://iswdevelopercommunity.slack.com |
