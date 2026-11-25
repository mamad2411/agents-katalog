---
name: identity-provider-okta
description: "--| | login | userName | Okta -> App | | firstName | name."
domain: cybersecurity
---

--|
| login | userName | Okta -> App |
| firstName | name.givenName | Okta -> App |
| lastName | name.familyName | Okta -> App |
| email | emails[type eq "work"].value | Okta -> App |
| department | urn:ietf:params:scim:schemas:extension:enterprise:2.0:User:department | Okta -> App |

### Step 4: Implement Error Handling

SCIM specifies standard error response format:

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "detail": "User already exists",
  "status": "409",
  "scimType": "uniqueness"
}
```

Common error codes: 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 409 (Conflict), 500 (Internal Server Error).

### Step 5: Test with Runscope/Okta SCIM Validator

Okta provides an automated SCIM test suite (via Runscope/BlazeMeter) that validates your SCIM implementation against all required operations:

1. Import the Okta SCIM 2.0 test suite from the OIN submission portal
2. Configure the base URL and authentication token
3. Run the full test suite covering user CRUD, filtering, and pagination
4. Fix any failing tests before submitting to OIN

## Validation Checklist

- [ ] SCIM server accessible over HTTPS with valid TLS certificate
- [ ] Bearer token authentication enforced on all endpoints
- [ ] User creation returns 201 with full user representation
- [ ] User search by `userName eq "..."` filter works correctly
- [ ] Pagination parameters (`startIndex`, `count`) handled properly
- [ ] User deactivation sets `active: false` (not hard delete)
- [ ] PATCH operations support `add`, `replace`, `remove` ops
- [ ] Group push creates and manages group memberships
- [ ] Okta SCIM validator test suite passes all tests
- [ ] Error responses conform to SCIM error schema

## References

- [SCIM 2.0 Protocol RFC 7644](https://tools.ietf.org/html/rfc7644)
- [Okta SCIM Developer Guide](https://developer.okta.com/docs/guides/scim-provisioning-integration-overview/main/)
- [Build a SCIM API Service - Okta](https://developer.okta.com/docs/guides/scim-provisioning-integration-prepare/main/)
- [SCIM Core Schema RFC 7643](https://tools.ietf.org/html/rfc7643)
