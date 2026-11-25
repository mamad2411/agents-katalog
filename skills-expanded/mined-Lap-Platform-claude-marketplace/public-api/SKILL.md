---
name: public-api
description: "Public API skill. Use when working with Public for accounts, dns, domains. Covers 75 endpoints."
version: 1.0.0
generator: lapsh
---

# Public Api
API version: v2

## Auth
ApiKey (inferred from docs)

## Base URL
/v2

## Setup
1. Set your API key in the appropriate header
2. GET /accounts -- verify access
3. POST /accounts -- create first accounts

## Endpoints

75 endpoints across 13 groups. See references/api-spec.lap for full details.

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | Overview of accounts |
| POST | /accounts | Create a new account |
| GET | /accounts/{accountId} | Get a specific account |

### dns
| Method | Path | Description |
|--------|------|-------------|
| GET | /dns/{domainName}/records | Get records |
| POST | /dns/{domainName}/records | Create a record |
| GET | /dns/{domainName}/records/{recordId} | Get specific record |
| PUT | /dns/{domainName}/records/{recordId} | Edit a record |
| DELETE | /dns/{domainName}/records/{recordId} | Delete a record |

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /domains | Overviews of domains |
| GET | /domains/{domainName} | Details of a domain |
| POST | /domains/registrations | Register a domain |
| POST | /domains/transfers | Transfer a domain |
| PUT | /domains/{domainName}/nameservers | Edit domain name servers |
| PUT | /domains/{domainName}/renew | Edit domain name renew state |

### linuxhostings
| Method | Path | Description |
|--------|------|-------------|
| GET | /linuxhostings | Overview of linux hostings |
| GET | /linuxhostings/{domainName} | Linux hosting detail |
| GET | /linuxhostings/{domainName}/phpsettings/availableversions | Get the available PHP versions. |
| PUT | /linuxhostings/{domainName}/phpsettings/version | Change the Linux hosting PHP version. |
| PUT | /linuxhostings/{domainName}/settings/gzipcompression | Enable/disable GZIP compression |
| POST | /linuxhostings/{domainName}/subsites | Create a subsite |
| DELETE | /linuxhostings/{domainName}/subsites/{siteName} | Delete a subsite |
| POST | /linuxhostings/{domainName}/sites/{siteName}/hostheaders | Create a host header |
| PUT | /linuxhostings/{domainName}/sites/{siteName}/http2/configuration | Configure HTTP/2 |
| PUT | /linuxhostings/{domainName}/ftp/configuration | Configure FTP |
| PUT | /linuxhostings/{domainName}/sslsettings/{hostname}/letsencrypt | Configure let's encrypt |
| PUT | /linuxhostings/{domainName}/sslsettings/{hostname}/autoredirect | Configure auto redirect |
| PUT | /linuxhostings/{domainName}/phpsettings/memorylimit | Configure PHP memory limit |
| PUT | /linuxhostings/{domainName}/phpsettings/apcu | Configure PHP APCu setting |
| GET | /linuxhostings/{domainName}/scheduledtasks | Overview of scheduled tasks |
| POST | /linuxhostings/{domainName}/scheduledtasks | Add a scheduled task |
| GET | /linuxhostings/{domainName}/scheduledtasks/{scheduledTaskId} | Get scheduled task detail |
| PUT | /linuxhostings/{domainName}/scheduledtasks/{scheduledTaskId} | Configure a scheduled task |
| DELETE | /linuxhostings/{domainName}/scheduledtasks/{scheduledTaskId} | Delete a scheduled task |
| GET | /linuxhostings/{domainName}/ssh/keys | Overview of SSH keys |
| POST | /linuxhostings/{domainName}/ssh/keys | Add a SSH key |
| PUT | /linuxhostings/{domainName}/ssh/configuration | Configure SSH |
| DELETE | /linuxhostings/{domainName}/ssh/keys/{fingerprint} | Delete a SSH key |

### mailboxes
| Method | Path | Description |
|--------|------|-------------|
| GET | /mailboxes | Gets your mailboxes. |
| POST | /mailboxes | Create a new mailbox. |
| GET | /mailboxes/{mailboxName} | Get a specific mailbox |
| DELETE | /mailboxes/{mailboxName} | Delete a mailbox |
| PUT | /mailboxes/{mailboxName}/password | Change password for mailbox |
| PUT | /mailboxes/{mailboxName}/autoreply | Configure auto-reply for mailbox |
| PUT | /mailboxes/{mailboxName}/autoforward | Configure auto-forward for mailbox |

### mailzones
| Method | Path | Description |
|--------|------|-------------|
| GET | /mailzones/{domainName} | Get the mail zone. |
| POST | /mailzones/{domainName}/catchall | Create a catch-all on the mail zone |
| DELETE | /mailzones/{domainName}/catchall/{emailAddress} | Delete a catch-all on the mail zone |
| PUT | /mailzones/{domainName}/antispam | Configure anti-spam for mail zone |
| POST | /mailzones/{domainName}/aliases | Create a new alias |
| PUT | /mailzones/{domainName}/aliases/{emailAddress} | Configure a alias |
| DELETE | /mailzones/{domainName}/aliases/{emailAddress} | Delete a alias |
| POST | /mailzones/{domainName}/smtpdomains | Create an extra smtp domain |
| PUT | /mailzones/{domainName}/smtpdomains/{hostname} | Configure an extra smtp domain |
| DELETE | /mailzones/{domainName}/smtpdomains/{hostname} | Delete an extra smtp domain |

### mysqldatabases
| Method | Path | Description |
|--------|------|-------------|
| GET | /mysqldatabases | Overview of mysql databases |
| POST | /mysqldatabases | Create a new mysql database |
| GET | /mysqldatabases/{databaseName} | Get a specific database |
| DELETE | /mysqldatabases/{databaseName} | Delete a mysql database |
| GET | /mysqldatabases/{databaseName}/users | Overview of mysql users |
| POST | /mysqldatabases/{databaseName}/users | Create a new mysql user |
| PUT | /mysqldatabases/{databaseName}/users/{userName}/status | Enable/disable mysql user |
| PUT | /mysqldatabases/{databaseName}/users/{userName}/password | Change password for mysql user |
| DELETE | /mysqldatabases/{databaseName}/users/{userName} | Delete a mysql user |

### provisioningjobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /provisioningjobs/{jobId} | Detail of a provisioning job |

### servicepacks
| Method | Path | Description |
|--------|------|-------------|
| GET | /servicepacks | Overview of service packs |

### ssh
| Method | Path | Description |
|--------|------|-------------|
| GET | /ssh | Overview of SSH keys |

### sslcertificaterequests
| Method | Path | Description |
|--------|------|-------------|
| GET | /sslcertificaterequests | Overview of SSL certificate requests |
| POST | /sslcertificaterequests | Add a SSL certificate request |
| GET | /sslcertificaterequests/{id} | Detail of a SSL certificate request |
| PUT | /sslcertificaterequests/{id} | Verify the SSL certificate request domain validations |

### sslcertificates
| Method | Path | Description |
|--------|------|-------------|
| GET | /sslcertificates | Overview of SSL certificates |
| GET | /sslcertificates/{sha1Fingerprint} | Detail of a SSL certificate |
| GET | /sslcertificates/{sha1Fingerprint}/download | Download a SSL certificate |

### windowshostings
| Method | Path | Description |
|--------|------|-------------|
| GET | /windowshostings | Overview of windows hostings |
| GET | /windowshostings/{domainName} | Windows hosting detail |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all accounts?" -> GET /accounts
- "Create a account?" -> POST /accounts
- "Get account details?" -> GET /accounts/{accountId}
- "List all records?" -> GET /dns/{domainName}/records
- "Create a record?" -> POST /dns/{domainName}/records
- "Get record details?" -> GET /dns/{domainName}/records/{recordId}
- "Update a record?" -> PUT /dns/{domainName}/records/{recordId}
- "Delete a record?" -> DELETE /dns/{domainName}/records/{recordId}
- "List all domains?" -> GET /domains
- "Get domain details?" -> GET /domains/{domainName}
- "Create a registration?" -> POST /domains/registrations
- "Create a transfer?" -> POST /domains/transfers
- "List all linuxhostings?" -> GET /linuxhostings
- "Get linuxhosting details?" -> GET /linuxhostings/{domainName}
- "List all availableversions?" -> GET /linuxhostings/{domainName}/phpsettings/availableversions
- "Create a subsite?" -> POST /linuxhostings/{domainName}/subsites
- "Delete a subsite?" -> DELETE /linuxhostings/{domainName}/subsites/{siteName}
- "Create a hostheader?" -> POST /linuxhostings/{domainName}/sites/{siteName}/hostheaders
- "List all scheduledtasks?" -> GET /linuxhostings/{domainName}/scheduledtasks
- "Create a scheduledtask?" -> POST /linuxhostings/{domainName}/scheduledtasks
- "Get scheduledtask details?" -> GET /linuxhostings/{domainName}/scheduledtasks/{scheduledTaskId}
- "Update a scheduledtask?" -> PUT /linuxhostings/{domainName}/scheduledtasks/{scheduledTaskId}
- "Delete a scheduledtask?" -> DELETE /linuxhostings/{domainName}/scheduledtasks/{scheduledTaskId}
- "List all keys?" -> GET /linuxhostings/{domainName}/ssh/keys
- "Create a key?" -> POST /linuxhostings/{domainName}/ssh/keys
- "Delete a key?" -> DELETE /linuxhostings/{domainName}/ssh/keys/{fingerprint}
- "List all mailboxes?" -> GET /mailboxes
- "Create a mailboxe?" -> POST /mailboxes
- "Get mailboxe details?" -> GET /mailboxes/{mailboxName}
- "Delete a mailboxe?" -> DELETE /mailboxes/{mailboxName}
- "Get mailzone details?" -> GET /mailzones/{domainName}
- "Create a catchall?" -> POST /mailzones/{domainName}/catchall
- "Delete a catchall?" -> DELETE /mailzones/{domainName}/catchall/{emailAddress}
- "Create a aliase?" -> POST /mailzones/{domainName}/aliases
- "Update a aliase?" -> PUT /mailzones/{domainName}/aliases/{emailAddress}
- "Delete a aliase?" -> DELETE /mailzones/{domainName}/aliases/{emailAddress}
- "Create a smtpdomain?" -> POST /mailzones/{domainName}/smtpdomains
- "Update a smtpdomain?" -> PUT /mailzones/{domainName}/smtpdomains/{hostname}
- "Delete a smtpdomain?" -> DELETE /mailzones/{domainName}/smtpdomains/{hostname}
- "List all mysqldatabases?" -> GET /mysqldatabases
- "Create a mysqldatabase?" -> POST /mysqldatabases
- "Get mysqldatabase details?" -> GET /mysqldatabases/{databaseName}
- "Delete a mysqldatabase?" -> DELETE /mysqldatabases/{databaseName}
- "List all users?" -> GET /mysqldatabases/{databaseName}/users
- "Create a user?" -> POST /mysqldatabases/{databaseName}/users
- "Delete a user?" -> DELETE /mysqldatabases/{databaseName}/users/{userName}
- "Get provisioningjob details?" -> GET /provisioningjobs/{jobId}
- "List all servicepacks?" -> GET /servicepacks
- "List all ssh?" -> GET /ssh
- "List all sslcertificaterequests?" -> GET /sslcertificaterequests
- "Create a sslcertificaterequest?" -> POST /sslcertificaterequests
- "Get sslcertificaterequest details?" -> GET /sslcertificaterequests/{id}
- "Update a sslcertificaterequest?" -> PUT /sslcertificaterequests/{id}
- "List all sslcertificates?" -> GET /sslcertificates
- "Get sslcertificate details?" -> GET /sslcertificates/{sha1Fingerprint}
- "List all download?" -> GET /sslcertificates/{sha1Fingerprint}/download
- "List all windowshostings?" -> GET /windowshostings
- "Get windowshosting details?" -> GET /windowshostings/{domainName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
