---
name: m2m-client-credentials
description: Implement Machine-to-Machine (M2M) authentication using SSOJet OAuth2 Client Credentials flow for backend services and daemons.
---

# Implement SSOJet M2M Authentication

This expert AI assistant guide walks you through implementing Machine-to-Machine (M2M) authentication using SSOJet's OAuth2 **Client Credentials** grant. This flow is designed for backend services, daemons, CLIs, and APIs that need to authenticate without a user being present.

## 1. Prerequisites

- A backend service, daemon, or API that needs to authenticate with SSOJet-protected resources.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- The M2M application's **Client ID** and **Client Secret** from SSOJet.

## 2. How It Works

The Client Credentials flow is a two-step process:

1. Your service sends its **Client ID** and **Client Secret** to SSOJet's token endpoint.
2. SSOJet verifies the credentials and returns an **Access Token**.
3. Your service uses the Access Token to call protected APIs.

There is **no user interaction**; this is a server-to-server authentication flow.

## 3. Implementation Steps

### Step 1: Create M2M Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyBackendService", type **Machine to Machine**).
4. Retrieve **Client ID** and **Client Secret**.
5. Note the **Token Endpoint** (e.g., `https://auth.ssojet.com/oauth2/token`).
6. Configure the **API/Audience** the M2M app is authorized to access.

### Step 2: Implement Token Retrieval

#### Node.js

```javascript
// m2m-auth.js
const fetch = require('node-fetch');

async function getM2MToken() {
  const response = await fetch('https://auth.ssojet.com/oauth2/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: process.env.SSOJET_CLIENT_ID,
      client_secret: process.env.SSOJET_CLIENT_SECRET,
      audience: process.env.SSOJET_API_AUDIENCE, // optional
      scope: 'read:data write:data', // requested scopes
    }),
  });

  if (!response.ok) {
    throw new Error(`Token request failed: ${response.statusText}`);
  }

  const data = await response.json();
  console.log('Access Token:', data.access_token);
  console.log('Expires In:', data.expires_in, 'seconds');
  return data.access_token;
}

// Usage: call a protected API
async function callProtectedAPI() {
  const token = await getM2MToken();

  const response = await fetch('https://api.example.com/data', {
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await response.json();
  console.log('API Response:', data);
}

callProtectedAPI();
```

#### Python

```python
# m2m_auth.py
import os
import requests

def get_m2m_token():
    response = requests.post(
        'https://auth.ssojet.com/oauth2/token',
        data={
            'grant_type': 'client_credentials',
            'client_id': os.getenv('SSOJET_CLIENT_ID'),
            'client_secret': os.getenv('SSOJET_CLIENT_SECRET'),
            'audience': os.getenv('SSOJET_API_AUDIENCE', ''),
            'scope': 'read:data write:data',
        },
    )
    response.raise_for_status()
    data = response.json()
    print(f"Access Token: {data['access_token']}")
    print(f"Expires In: {data['expires_in']} seconds")
    return data['access_token']


def call_protected_api():
    token = get_m2m_token()
    response = requests.get(
        'https://api.example.com/data',
        headers={'Authorization': f'Bearer {token}'},
    )
    print('API Response:', response.json())


if __name__ == '__main__':
    call_protected_api()
```

#### Go

```go
// m2m_auth.go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/clientcredentials"
)

func main() {
	config := &clientcredentials.Config{
		ClientID:     os.Getenv("SSOJET_CLIENT_ID"),
		ClientSecret: os.Getenv("SSOJET_CLIENT_SECRET"),
		TokenURL:     "https://auth.ssojet.com/oauth2/token",
		Scopes:       []string{"read:data", "write:data"},
	}

	token, err := config.Token(context.Background())
	if err != nil {
		log.Fatal("Token request failed:", err)
	}

	fmt.Println("Access Token:", token.AccessToken)
	fmt.Println("Expires:", token.Expiry)

	// Use token to call a protected API
	client := config.Client(context.Background())
	resp, err := client.Get("https://api.example.com/data")
	if err != nil {
		log.Fatal("API call failed:", err)
	}
	defer resp.Body.Close()
	fmt.Println("API Response Status:", resp.Status)
}
```

#### C# / .NET

```csharp
// M2MAuth.cs
using System.Net.Http.Headers;

var client = new HttpClient();

var tokenRequest = new FormUrlEncodedContent(new[]
{
    new KeyValuePair<string, string>("grant_type", "client_credentials"),
    new KeyValuePair<string, string>("client_id", Environment.GetEnvironmentVariable("SSOJET_CLIENT_ID")!),
    new KeyValuePair<string, string>("client_secret", Environment.GetEnvironmentVariable("SSOJET_CLIENT_SECRET")!),
    new KeyValuePair<string, string>("scope", "read:data write:data"),
});

var tokenResponse = await client.PostAsync("https://auth.ssojet.com/oauth2/token", tokenRequest);
tokenResponse.EnsureSuccessStatusCode();

var tokenData = await tokenResponse.Content.ReadFromJsonAsync<TokenResponse>();
Console.WriteLine($"Access Token: {tokenData!.AccessToken}");

// Call a protected API
client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", tokenData.AccessToken);
var apiResponse = await client.GetStringAsync("https://api.example.com/data");
Console.WriteLine($"API Response: {apiResponse}");

record TokenResponse(
    [property: System.Text.Json.Serialization.JsonPropertyName("access_token")] string AccessToken,
    [property: System.Text.Json.Serialization.JsonPropertyName("expires_in")] int ExpiresIn
);
```

#### cURL

```bash
# Get M2M token
curl -X POST https://auth.ssojet.com/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "scope=read:data write:data"
```

### Step 3: Token Caching (Best Practice)

Tokens should be cached and reused until they expire. Here is a Node.js example:

```javascript
// m2m-auth-cached.js
let cachedToken = null;
let tokenExpiry = 0;

async function getM2MToken() {
  // Return cached token if still valid (with 60s buffer)
  if (cachedToken && Date.now() < tokenExpiry - 60000) {
    return cachedToken;
  }

  const response = await fetch('https://auth.ssojet.com/oauth2/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: process.env.SSOJET_CLIENT_ID,
      client_secret: process.env.SSOJET_CLIENT_SECRET,
      scope: 'read:data write:data',
    }),
  });

  const data = await response.json();
  cachedToken = data.access_token;
  tokenExpiry = Date.now() + data.expires_in * 1000;

  return cachedToken;
}
```

### Step 4: Test the Connection

1. Set environment variables: `SSOJET_CLIENT_ID` and `SSOJET_CLIENT_SECRET`.
2. Run the script for your language.
3. Verify that an Access Token is returned.
4. Verify that the protected API responds successfully with the token.

## 4. Additional Considerations

- **Token Caching**: Always cache tokens and reuse them until expiry. Requesting a new token for every API call is inefficient and may trigger rate limits.
- **Security**: Store Client Secrets securely (environment variables, vault, secrets manager). Never hard-code them.
- **Scopes**: Request only the scopes your service actually needs (principle of least privilege).
- **Error Handling**: Handle token request failures, expired tokens, and API-level authorization errors.
- **Rate Limiting**: Be aware of SSOJet's rate limits on the token endpoint.

## 5. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **OAuth2 Spec**: Refer to [RFC 6749 Section 4.4](https://datatracker.ietf.org/doc/html/rfc6749#section-4.4) for the Client Credentials grant specification.
