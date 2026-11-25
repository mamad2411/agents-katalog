---
name: keyvaultclient
description: "KeyVaultClient API skill. Use when working with KeyVaultClient for keys, deletedkeys, secrets. Covers 78 endpoints."
version: 1.0.0
generator: lapsh
---

# KeyVaultClient
API version: 7.0-preview

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /keys -- verify access
3. POST /keys/{key-name}/create -- create first create

## Endpoints

78 endpoints across 8 groups. See references/api-spec.lap for full details.

### keys
| Method | Path | Description |
|--------|------|-------------|
| POST | /keys/{key-name}/create | Creates a new key, stores it, then returns key parameters and attributes to the client. |
| PUT | /keys/{key-name} | Imports an externally created key, stores it, and returns key parameters and attributes to the client. |
| DELETE | /keys/{key-name} | Deletes a key of any type from storage in Azure Key Vault. |
| PATCH | /keys/{key-name}/{key-version} | The update key operation changes specified attributes of a stored key and can be applied to any key type and key version stored in Azure Key Vault. |
| GET | /keys/{key-name}/{key-version} | Gets the public part of a stored key. |
| GET | /keys/{key-name}/versions | Retrieves a list of individual key versions with the same key name. |
| GET | /keys | List keys in the specified vault. |
| POST | /keys/{key-name}/backup | Requests that a backup of the specified key be downloaded to the client. |
| POST | /keys/restore | Restores a backed up key to a vault. |
| POST | /keys/{key-name}/{key-version}/encrypt | Encrypts an arbitrary sequence of bytes using an encryption key that is stored in a key vault. |
| POST | /keys/{key-name}/{key-version}/decrypt | Decrypts a single block of encrypted data. |
| POST | /keys/{key-name}/{key-version}/sign | Creates a signature from a digest using the specified key. |
| POST | /keys/{key-name}/{key-version}/verify | Verifies a signature using a specified key. |
| POST | /keys/{key-name}/{key-version}/wrapkey | Wraps a symmetric key using a specified key. |
| POST | /keys/{key-name}/{key-version}/unwrapkey | Unwraps a symmetric key using the specified key that was initially used for wrapping that key. |

### deletedkeys
| Method | Path | Description |
|--------|------|-------------|
| GET | /deletedkeys | Lists the deleted keys in the specified vault. |
| GET | /deletedkeys/{key-name} | Gets the public part of a deleted key. |
| DELETE | /deletedkeys/{key-name} | Permanently deletes the specified key. |
| POST | /deletedkeys/{key-name}/recover | Recovers the deleted key to its latest version. |

### secrets
| Method | Path | Description |
|--------|------|-------------|
| PUT | /secrets/{secret-name} | Sets a secret in a specified key vault. |
| DELETE | /secrets/{secret-name} | Deletes a secret from a specified key vault. |
| PATCH | /secrets/{secret-name}/{secret-version} | Updates the attributes associated with a specified secret in a given key vault. |
| GET | /secrets/{secret-name}/{secret-version} | Get a specified secret from a given key vault. |
| GET | /secrets | List secrets in a specified key vault. |
| GET | /secrets/{secret-name}/versions | List all versions of the specified secret. |
| POST | /secrets/{secret-name}/backup | Backs up the specified secret. |
| POST | /secrets/restore | Restores a backed up secret to a vault. |

### deletedsecrets
| Method | Path | Description |
|--------|------|-------------|
| GET | /deletedsecrets | Lists deleted secrets for the specified vault. |
| GET | /deletedsecrets/{secret-name} | Gets the specified deleted secret. |
| DELETE | /deletedsecrets/{secret-name} | Permanently deletes the specified secret. |
| POST | /deletedsecrets/{secret-name}/recover | Recovers the deleted secret to the latest version. |

### certificates
| Method | Path | Description |
|--------|------|-------------|
| GET | /certificates | List certificates in a specified key vault |
| DELETE | /certificates/{certificate-name} | Deletes a certificate from a specified key vault. |
| PUT | /certificates/contacts | Sets the certificate contacts for the specified key vault. |
| GET | /certificates/contacts | Lists the certificate contacts for a specified key vault. |
| DELETE | /certificates/contacts | Deletes the certificate contacts for a specified key vault. |
| GET | /certificates/issuers | List certificate issuers for a specified key vault. |
| PUT | /certificates/issuers/{issuer-name} | Sets the specified certificate issuer. |
| PATCH | /certificates/issuers/{issuer-name} | Updates the specified certificate issuer. |
| GET | /certificates/issuers/{issuer-name} | Lists the specified certificate issuer. |
| DELETE | /certificates/issuers/{issuer-name} | Deletes the specified certificate issuer. |
| POST | /certificates/{certificate-name}/create | Creates a new certificate. |
| POST | /certificates/{certificate-name}/import | Imports a certificate into a specified key vault. |
| GET | /certificates/{certificate-name}/versions | List the versions of a certificate. |
| GET | /certificates/{certificate-name}/policy | Lists the policy for a certificate. |
| PATCH | /certificates/{certificate-name}/policy | Updates the policy for a certificate. |
| PATCH | /certificates/{certificate-name}/{certificate-version} | Updates the specified attributes associated with the given certificate. |
| GET | /certificates/{certificate-name}/{certificate-version} | Gets information about a certificate. |
| PATCH | /certificates/{certificate-name}/pending | Updates a certificate operation. |
| GET | /certificates/{certificate-name}/pending | Gets the creation operation of a certificate. |
| DELETE | /certificates/{certificate-name}/pending | Deletes the creation operation for a specific certificate. |
| POST | /certificates/{certificate-name}/pending/merge | Merges a certificate or a certificate chain with a key pair existing on the server. |
| POST | /certificates/{certificate-name}/backup | Backs up the specified certificate. |
| POST | /certificates/restore | Restores a backed up certificate to a vault. |

### deletedcertificates
| Method | Path | Description |
|--------|------|-------------|
| GET | /deletedcertificates | Lists the deleted certificates in the specified vault currently available for recovery. |
| GET | /deletedcertificates/{certificate-name} | Retrieves information about the specified deleted certificate. |
| DELETE | /deletedcertificates/{certificate-name} | Permanently deletes the specified deleted certificate. |
| POST | /deletedcertificates/{certificate-name}/recover | Recovers the deleted certificate back to its current version under /certificates. |

### storage
| Method | Path | Description |
|--------|------|-------------|
| GET | /storage | List storage accounts managed by the specified key vault. This operation requires the storage/list permission. |
| POST | /storage/{storage-account-name}/backup | Backs up the specified storage account. |
| POST | /storage/restore | Restores a backed up storage account to a vault. |
| DELETE | /storage/{storage-account-name} | Deletes a storage account. This operation requires the storage/delete permission. |
| GET | /storage/{storage-account-name} | Gets information about a specified storage account. This operation requires the storage/get permission. |
| PUT | /storage/{storage-account-name} | Creates or updates a new storage account. This operation requires the storage/set permission. |
| PATCH | /storage/{storage-account-name} | Updates the specified attributes associated with the given storage account. This operation requires the storage/set/update permission. |
| POST | /storage/{storage-account-name}/regeneratekey | Regenerates the specified key value for the given storage account. This operation requires the storage/regeneratekey permission. |
| GET | /storage/{storage-account-name}/sas | List storage SAS definitions for the given storage account. This operation requires the storage/listsas permission. |
| DELETE | /storage/{storage-account-name}/sas/{sas-definition-name} | Deletes a SAS definition from a specified storage account. This operation requires the storage/deletesas permission. |
| GET | /storage/{storage-account-name}/sas/{sas-definition-name} | Gets information about a SAS definition for the specified storage account. This operation requires the storage/getsas permission. |
| PUT | /storage/{storage-account-name}/sas/{sas-definition-name} | Creates or updates a new SAS definition for the specified storage account. This operation requires the storage/setsas permission. |
| PATCH | /storage/{storage-account-name}/sas/{sas-definition-name} | Updates the specified attributes associated with the given SAS definition. This operation requires the storage/setsas permission. |

### deletedstorage
| Method | Path | Description |
|--------|------|-------------|
| GET | /deletedstorage | Lists deleted storage accounts for the specified vault. |
| GET | /deletedstorage/{storage-account-name} | Gets the specified deleted storage account. |
| DELETE | /deletedstorage/{storage-account-name} | Permanently deletes the specified storage account. |
| POST | /deletedstorage/{storage-account-name}/recover | Recovers the deleted storage account. |
| GET | /deletedstorage/{storage-account-name}/sas | Lists deleted SAS definitions for the specified vault and storage account. |
| GET | /deletedstorage/{storage-account-name}/sas/{sas-definition-name} | Gets the specified deleted sas definition. |
| POST | /deletedstorage/{storage-account-name}/sas/{sas-definition-name}/recover | Recovers the deleted SAS definition. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a create?" -> POST /keys/{key-name}/create
- "Update a key?" -> PUT /keys/{key-name}
- "Delete a key?" -> DELETE /keys/{key-name}
- "Partially update a key?" -> PATCH /keys/{key-name}/{key-version}
- "Get key details?" -> GET /keys/{key-name}/{key-version}
- "List all versions?" -> GET /keys/{key-name}/versions
- "List all keys?" -> GET /keys
- "Create a backup?" -> POST /keys/{key-name}/backup
- "Create a restore?" -> POST /keys/restore
- "Create a encrypt?" -> POST /keys/{key-name}/{key-version}/encrypt
- "Create a decrypt?" -> POST /keys/{key-name}/{key-version}/decrypt
- "Create a sign?" -> POST /keys/{key-name}/{key-version}/sign
- "Create a verify?" -> POST /keys/{key-name}/{key-version}/verify
- "Create a wrapkey?" -> POST /keys/{key-name}/{key-version}/wrapkey
- "Create a unwrapkey?" -> POST /keys/{key-name}/{key-version}/unwrapkey
- "List all deletedkeys?" -> GET /deletedkeys
- "Get deletedkey details?" -> GET /deletedkeys/{key-name}
- "Delete a deletedkey?" -> DELETE /deletedkeys/{key-name}
- "Create a recover?" -> POST /deletedkeys/{key-name}/recover
- "Update a secret?" -> PUT /secrets/{secret-name}
- "Delete a secret?" -> DELETE /secrets/{secret-name}
- "Partially update a secret?" -> PATCH /secrets/{secret-name}/{secret-version}
- "Get secret details?" -> GET /secrets/{secret-name}/{secret-version}
- "List all secrets?" -> GET /secrets
- "List all versions?" -> GET /secrets/{secret-name}/versions
- "List all deletedsecrets?" -> GET /deletedsecrets
- "Get deletedsecret details?" -> GET /deletedsecrets/{secret-name}
- "Delete a deletedsecret?" -> DELETE /deletedsecrets/{secret-name}
- "Create a recover?" -> POST /deletedsecrets/{secret-name}/recover
- "Create a backup?" -> POST /secrets/{secret-name}/backup
- "Create a restore?" -> POST /secrets/restore
- "List all certificates?" -> GET /certificates
- "Delete a certificate?" -> DELETE /certificates/{certificate-name}
- "List all contacts?" -> GET /certificates/contacts
- "List all issuers?" -> GET /certificates/issuers
- "Update a issuer?" -> PUT /certificates/issuers/{issuer-name}
- "Partially update a issuer?" -> PATCH /certificates/issuers/{issuer-name}
- "Get issuer details?" -> GET /certificates/issuers/{issuer-name}
- "Delete a issuer?" -> DELETE /certificates/issuers/{issuer-name}
- "Create a create?" -> POST /certificates/{certificate-name}/create
- "Create a import?" -> POST /certificates/{certificate-name}/import
- "List all versions?" -> GET /certificates/{certificate-name}/versions
- "List all policy?" -> GET /certificates/{certificate-name}/policy
- "Partially update a certificate?" -> PATCH /certificates/{certificate-name}/{certificate-version}
- "Get certificate details?" -> GET /certificates/{certificate-name}/{certificate-version}
- "List all pending?" -> GET /certificates/{certificate-name}/pending
- "Create a merge?" -> POST /certificates/{certificate-name}/pending/merge
- "Create a backup?" -> POST /certificates/{certificate-name}/backup
- "Create a restore?" -> POST /certificates/restore
- "List all deletedcertificates?" -> GET /deletedcertificates
- "Get deletedcertificate details?" -> GET /deletedcertificates/{certificate-name}
- "Delete a deletedcertificate?" -> DELETE /deletedcertificates/{certificate-name}
- "Create a recover?" -> POST /deletedcertificates/{certificate-name}/recover
- "List all storage?" -> GET /storage
- "List all deletedstorage?" -> GET /deletedstorage
- "Get deletedstorage details?" -> GET /deletedstorage/{storage-account-name}
- "Delete a deletedstorage?" -> DELETE /deletedstorage/{storage-account-name}
- "Create a recover?" -> POST /deletedstorage/{storage-account-name}/recover
- "Create a backup?" -> POST /storage/{storage-account-name}/backup
- "Create a restore?" -> POST /storage/restore
- "Delete a storage?" -> DELETE /storage/{storage-account-name}
- "Get storage details?" -> GET /storage/{storage-account-name}
- "Update a storage?" -> PUT /storage/{storage-account-name}
- "Partially update a storage?" -> PATCH /storage/{storage-account-name}
- "Create a regeneratekey?" -> POST /storage/{storage-account-name}/regeneratekey
- "List all sas?" -> GET /storage/{storage-account-name}/sas
- "List all sas?" -> GET /deletedstorage/{storage-account-name}/sas
- "Get sa details?" -> GET /deletedstorage/{storage-account-name}/sas/{sas-definition-name}
- "Create a recover?" -> POST /deletedstorage/{storage-account-name}/sas/{sas-definition-name}/recover
- "Delete a sa?" -> DELETE /storage/{storage-account-name}/sas/{sas-definition-name}
- "Get sa details?" -> GET /storage/{storage-account-name}/sas/{sas-definition-name}
- "Update a sa?" -> PUT /storage/{storage-account-name}/sas/{sas-definition-name}
- "Partially update a sa?" -> PATCH /storage/{storage-account-name}/sas/{sas-definition-name}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
