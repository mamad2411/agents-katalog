---
name: namecheap
description: Manage domains via the Namecheap API. Check domain availability, register domains, and manage DNS records. Use this skill when the user wants to check if a domain is available, buy/register a domain, or configure DNS settings.
user-invocable: true
---

# Namecheap Domain Management Skill

Manage domains through the Namecheap API - check availability, register domains, and configure DNS records.

## Usage

Invoke this skill with:
```
/namecheap
```

Or Codex will automatically use this skill when you ask about domain availability, registration, or DNS management.

## Required Environment Variables

The following environment variables must be set:

```bash
export NAMECHEAP_API_USER="your_api_username"
export NAMECHEAP_API_KEY="your_api_key"
export NAMECHEAP_USERNAME="your_namecheap_username"  # Usually same as API_USER
export NAMECHEAP_CLIENT_IP="your_whitelisted_ip"
```

Optional for sandbox/testing:
```bash
export NAMECHEAP_SANDBOX="true"  # Use sandbox API for testing
```

## API Endpoints

- **Production:** `https://api.namecheap.com/xml.response`
- **Sandbox:** `https://api.sandbox.namecheap.com/xml.response`

## Capabilities

### 1. Check Domain Availability

Check if one or more domains are available for registration.

**API Command:** `namecheap.domains.check`

**Example curl request:**
```bash
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&\
ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&\
ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.check&\
DomainList=example.com,example.net,example.org"
```

**Response parsing:** Look for `<DomainCheckResult Domain="..." Available="true/false" />` in the XML response.

### 2. Get Domain Pricing

Get pricing for domain registration before purchasing.

**API Command:** `namecheap.users.getPricing`

**Example curl request:**
```bash
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&\
ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&\
ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.users.getPricing&\
ProductType=DOMAIN&\
ProductCategory=REGISTER&\
ProductName=com"
```

### 3. Register a Domain

Register an available domain. Requires contact information.

**API Command:** `namecheap.domains.create`

**Required parameters:**
- `DomainName` - The domain to register (e.g., "example.com")
- `Years` - Registration period (1-10 years)
- Contact info for Registrant, Tech, Admin, AuxBilling (see below)

**Contact parameters (required for each contact type):**
Replace `{Type}` with: `Registrant`, `Tech`, `Admin`, `AuxBilling`

- `{Type}FirstName`
- `{Type}LastName`
- `{Type}Address1`
- `{Type}City`
- `{Type}StateProvince`
- `{Type}PostalCode`
- `{Type}Country` (2-letter code, e.g., "US", "GB")
- `{Type}Phone` (format: +1.1234567890)
- `{Type}EmailAddress`

**Example curl request:**
```bash
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&\
ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&\
ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.create&\
DomainName=example.com&\
Years=1&\
RegistrantFirstName=John&\
RegistrantLastName=Doe&\
RegistrantAddress1=123 Main St&\
RegistrantCity=London&\
RegistrantStateProvince=England&\
RegistrantPostalCode=SW1A 1AA&\
RegistrantCountry=GB&\
RegistrantPhone=+44.1234567890&\
RegistrantEmailAddress=john@example.com&\
TechFirstName=John&\
TechLastName=Doe&\
TechAddress1=123 Main St&\
TechCity=London&\
TechStateProvince=England&\
TechPostalCode=SW1A 1AA&\
TechCountry=GB&\
TechPhone=+44.1234567890&\
TechEmailAddress=john@example.com&\
AdminFirstName=John&\
AdminLastName=Doe&\
AdminAddress1=123 Main St&\
AdminCity=London&\
AdminStateProvince=England&\
AdminPostalCode=SW1A 1AA&\
AdminCountry=GB&\
AdminPhone=+44.1234567890&\
AdminEmailAddress=john@example.com&\
AuxBillingFirstName=John&\
AuxBillingLastName=Doe&\
AuxBillingAddress1=123 Main St&\
AuxBillingCity=London&\
AuxBillingStateProvince=England&\
AuxBillingPostalCode=SW1A 1AA&\
AuxBillingCountry=GB&\
AuxBillingPhone=+44.1234567890&\
AuxBillingEmailAddress=john@example.com"
```

**IMPORTANT:** Always confirm with the user before registering a domain as this will charge their account.

### 4. Get DNS Host Records

Retrieve current DNS records for a domain.

**API Command:** `namecheap.domains.dns.getHosts`

**Example curl request:**
```bash
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&\
ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&\
ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.dns.getHosts&\
SLD=example&\
TLD=com"
```

**Note:** `SLD` is the second-level domain (e.g., "example" from "example.com"), `TLD` is the top-level domain (e.g., "com").

### 5. Set DNS Host Records

Configure DNS records for a domain. **This replaces ALL existing records.**

**API Command:** `namecheap.domains.dns.setHosts`

**Record parameters (numbered 1, 2, 3, etc.):**
- `HostName{n}` - Subdomain or @ for root
- `RecordType{n}` - A, AAAA, CNAME, MX, TXT, NS, etc.
- `Address{n}` - IP address or target hostname
- `TTL{n}` - Time to live in seconds (default: 1800)
- `MXPref{n}` - MX priority (only for MX records)

**Example curl request:**
```bash
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&\
ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&\
ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.dns.setHosts&\
SLD=example&\
TLD=com&\
HostName1=@&\
RecordType1=A&\
Address1=192.0.2.1&\
TTL1=1800&\
HostName2=www&\
RecordType2=CNAME&\
Address2=example.com&\
TTL2=1800&\
HostName3=@&\
RecordType3=MX&\
Address3=mail.example.com&\
MXPref3=10&\
TTL3=1800"
```

**IMPORTANT:**
- This command REPLACES all existing DNS records
- Always fetch existing records first with `getHosts`
- Include all records you want to keep when setting new ones
- Confirm with user before making DNS changes

### 6. List Domains

Get a list of domains in the account.

**API Command:** `namecheap.domains.getList`

**Example curl request:**
```bash
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&\
ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&\
ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.getList&\
PageSize=100&\
Page=1"
```

## Response Handling

All Namecheap API responses are XML. Key elements:

```xml
<ApiResponse Status="OK">  <!-- or Status="ERROR" -->
  <Errors>
    <Error Number="...">Error message</Error>
  </Errors>
  <CommandResponse>
    <!-- Command-specific data -->
  </CommandResponse>
</ApiResponse>
```

**Always check:**
1. `Status` attribute on `<ApiResponse>` - should be "OK"
2. `<Errors>` element for any error messages
3. Parse the `<CommandResponse>` for the actual data

## Workflow Guidelines

### When checking domain availability:
1. Verify environment variables are set
2. Accept domain name(s) from user
3. Make API request
4. Parse XML response and report availability status
5. If available, offer to check pricing or register

### When registering a domain:
1. First check availability
2. Get pricing information
3. Collect required contact information from user
4. **Confirm the purchase with the user** (this charges money!)
5. Make registration request
6. Report success/failure and any relevant details

### When managing DNS:
1. First fetch existing records with `getHosts`
2. Show current configuration to user
3. Collect desired changes
4. **Warn user that setHosts replaces ALL records**
5. Build complete record set (existing + new/modified)
6. Confirm changes with user
7. Apply changes with `setHosts`
8. Verify by fetching records again

## Error Handling

Common error codes:
- `2030280` - Domain not available
- `2033407` - Invalid domain name
- `2016166` - Domain already in account
- `2019166` - Domain not found in account
- `5050900` - API key invalid or IP not whitelisted

If you encounter IP whitelist errors, remind the user to whitelist their current IP in the Namecheap dashboard.

## Testing with Sandbox

For testing without real purchases:
1. Create a sandbox account at https://www.sandbox.namecheap.com/
2. Set `NAMECHEAP_SANDBOX=true` environment variable
3. The skill will use the sandbox API endpoint
4. Sandbox accounts have fake balance for testing registrations

## Security Notes

- Never log or display the full API key
- All API requests should use HTTPS
- The API requires IP whitelisting as an additional security measure
- Be cautious with domain registration and DNS changes - these have real-world impact
