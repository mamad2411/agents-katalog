---
name: twilio-messaging
description: "Twilio - Messaging API skill. Use when working with Twilio - Messaging for Services, a2p, Deactivations. Covers 58 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Messaging
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://messaging.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/a2p/BrandRegistrations -- verify access
3. POST /v1/Services/{ServiceSid}/AlphaSenders -- create first AlphaSenders

## Endpoints

58 endpoints across 5 groups. See references/api-spec.lap for full details.

### Services
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/Services/{ServiceSid}/AlphaSenders |  |
| GET | /v1/Services/{ServiceSid}/AlphaSenders |  |
| GET | /v1/Services/{ServiceSid}/AlphaSenders/{Sid} |  |
| DELETE | /v1/Services/{ServiceSid}/AlphaSenders/{Sid} |  |
| GET | /v1/Services/{MessagingServiceSid}/ChannelSenders |  |
| POST | /v1/Services/{MessagingServiceSid}/ChannelSenders |  |
| GET | /v1/Services/{MessagingServiceSid}/ChannelSenders/{Sid} |  |
| DELETE | /v1/Services/{MessagingServiceSid}/ChannelSenders/{Sid} |  |
| POST | /v1/Services/{ServiceSid}/DestinationAlphaSenders |  |
| GET | /v1/Services/{ServiceSid}/DestinationAlphaSenders |  |
| GET | /v1/Services/{ServiceSid}/DestinationAlphaSenders/{Sid} |  |
| DELETE | /v1/Services/{ServiceSid}/DestinationAlphaSenders/{Sid} |  |
| POST | /v1/Services/PreregisteredUsa2p |  |
| POST | /v1/Services/{ServiceSid}/PhoneNumbers |  |
| GET | /v1/Services/{ServiceSid}/PhoneNumbers |  |
| DELETE | /v1/Services/{ServiceSid}/PhoneNumbers/{Sid} |  |
| GET | /v1/Services/{ServiceSid}/PhoneNumbers/{Sid} |  |
| POST | /v1/Services |  |
| GET | /v1/Services |  |
| POST | /v1/Services/{Sid} |  |
| GET | /v1/Services/{Sid} |  |
| DELETE | /v1/Services/{Sid} |  |
| POST | /v1/Services/{ServiceSid}/ShortCodes |  |
| GET | /v1/Services/{ServiceSid}/ShortCodes |  |
| DELETE | /v1/Services/{ServiceSid}/ShortCodes/{Sid} |  |
| GET | /v1/Services/{ServiceSid}/ShortCodes/{Sid} |  |
| POST | /v1/Services/{MessagingServiceSid}/Compliance/Usa2p |  |
| GET | /v1/Services/{MessagingServiceSid}/Compliance/Usa2p |  |
| DELETE | /v1/Services/{MessagingServiceSid}/Compliance/Usa2p/{Sid} |  |
| GET | /v1/Services/{MessagingServiceSid}/Compliance/Usa2p/{Sid} |  |
| POST | /v1/Services/{MessagingServiceSid}/Compliance/Usa2p/{Sid} |  |
| GET | /v1/Services/{MessagingServiceSid}/Compliance/Usa2p/Usecases |  |
| GET | /v1/Services/Usecases |  |

### a2p
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/a2p/BrandRegistrations/{BrandRegistrationSid}/SmsOtp |  |
| GET | /v1/a2p/BrandRegistrations/{Sid} |  |
| POST | /v1/a2p/BrandRegistrations/{Sid} |  |
| GET | /v1/a2p/BrandRegistrations |  |
| POST | /v1/a2p/BrandRegistrations |  |
| POST | /v1/a2p/BrandRegistrations/{BrandSid}/Vettings |  |
| GET | /v1/a2p/BrandRegistrations/{BrandSid}/Vettings |  |
| GET | /v1/a2p/BrandRegistrations/{BrandSid}/Vettings/{BrandVettingSid} |  |

### Deactivations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/Deactivations | Fetch a list of all United States numbers that have been deactivated on a specific date. |

### LinkShortening
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/LinkShortening/Domains/{DomainSid}/Certificate |  |
| GET | /v1/LinkShortening/Domains/{DomainSid}/Certificate |  |
| DELETE | /v1/LinkShortening/Domains/{DomainSid}/Certificate |  |
| POST | /v1/LinkShortening/Domains/{DomainSid}/Config |  |
| GET | /v1/LinkShortening/Domains/{DomainSid}/Config |  |
| GET | /v1/LinkShortening/MessagingService/{MessagingServiceSid}/DomainConfig |  |
| GET | /v1/LinkShortening/Domains/{DomainSid}/ValidateDns |  |
| POST | /v1/LinkShortening/Domains/{DomainSid}/MessagingServices/{MessagingServiceSid} |  |
| DELETE | /v1/LinkShortening/Domains/{DomainSid}/MessagingServices/{MessagingServiceSid} |  |
| GET | /v1/LinkShortening/MessagingServices/{MessagingServiceSid}/Domain |  |
| POST | /v1/LinkShortening/Domains/{DomainSid}/RequestManagedCert |  |

### Tollfree
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/Tollfree/Verifications/{Sid} | Retrieve a tollfree verification |
| POST | /v1/Tollfree/Verifications/{Sid} | Edit a tollfree verification |
| DELETE | /v1/Tollfree/Verifications/{Sid} | Delete a tollfree verification |
| GET | /v1/Tollfree/Verifications | List tollfree verifications |
| POST | /v1/Tollfree/Verifications | Create a tollfree verification |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a AlphaSender?" -> POST /v1/Services/{ServiceSid}/AlphaSenders
- "List all AlphaSenders?" -> GET /v1/Services/{ServiceSid}/AlphaSenders
- "Get AlphaSender details?" -> GET /v1/Services/{ServiceSid}/AlphaSenders/{Sid}
- "Delete a AlphaSender?" -> DELETE /v1/Services/{ServiceSid}/AlphaSenders/{Sid}
- "Create a SmsOtp?" -> POST /v1/a2p/BrandRegistrations/{BrandRegistrationSid}/SmsOtp
- "Get BrandRegistration details?" -> GET /v1/a2p/BrandRegistrations/{Sid}
- "List all BrandRegistrations?" -> GET /v1/a2p/BrandRegistrations
- "Create a BrandRegistration?" -> POST /v1/a2p/BrandRegistrations
- "Create a Vetting?" -> POST /v1/a2p/BrandRegistrations/{BrandSid}/Vettings
- "List all Vettings?" -> GET /v1/a2p/BrandRegistrations/{BrandSid}/Vettings
- "Get Vetting details?" -> GET /v1/a2p/BrandRegistrations/{BrandSid}/Vettings/{BrandVettingSid}
- "List all ChannelSenders?" -> GET /v1/Services/{MessagingServiceSid}/ChannelSenders
- "Create a ChannelSender?" -> POST /v1/Services/{MessagingServiceSid}/ChannelSenders
- "Get ChannelSender details?" -> GET /v1/Services/{MessagingServiceSid}/ChannelSenders/{Sid}
- "Delete a ChannelSender?" -> DELETE /v1/Services/{MessagingServiceSid}/ChannelSenders/{Sid}
- "List all Deactivations?" -> GET /v1/Deactivations
- "Create a DestinationAlphaSender?" -> POST /v1/Services/{ServiceSid}/DestinationAlphaSenders
- "List all DestinationAlphaSenders?" -> GET /v1/Services/{ServiceSid}/DestinationAlphaSenders
- "Get DestinationAlphaSender details?" -> GET /v1/Services/{ServiceSid}/DestinationAlphaSenders/{Sid}
- "Delete a DestinationAlphaSender?" -> DELETE /v1/Services/{ServiceSid}/DestinationAlphaSenders/{Sid}
- "Create a Certificate?" -> POST /v1/LinkShortening/Domains/{DomainSid}/Certificate
- "List all Certificate?" -> GET /v1/LinkShortening/Domains/{DomainSid}/Certificate
- "Create a Config?" -> POST /v1/LinkShortening/Domains/{DomainSid}/Config
- "List all Config?" -> GET /v1/LinkShortening/Domains/{DomainSid}/Config
- "List all DomainConfig?" -> GET /v1/LinkShortening/MessagingService/{MessagingServiceSid}/DomainConfig
- "List all ValidateDns?" -> GET /v1/LinkShortening/Domains/{DomainSid}/ValidateDns
- "Create a PreregisteredUsa2p?" -> POST /v1/Services/PreregisteredUsa2p
- "Delete a MessagingService?" -> DELETE /v1/LinkShortening/Domains/{DomainSid}/MessagingServices/{MessagingServiceSid}
- "List all Domain?" -> GET /v1/LinkShortening/MessagingServices/{MessagingServiceSid}/Domain
- "Create a PhoneNumber?" -> POST /v1/Services/{ServiceSid}/PhoneNumbers
- "List all PhoneNumbers?" -> GET /v1/Services/{ServiceSid}/PhoneNumbers
- "Delete a PhoneNumber?" -> DELETE /v1/Services/{ServiceSid}/PhoneNumbers/{Sid}
- "Get PhoneNumber details?" -> GET /v1/Services/{ServiceSid}/PhoneNumbers/{Sid}
- "Create a RequestManagedCert?" -> POST /v1/LinkShortening/Domains/{DomainSid}/RequestManagedCert
- "Create a Service?" -> POST /v1/Services
- "List all Services?" -> GET /v1/Services
- "Get Service details?" -> GET /v1/Services/{Sid}
- "Delete a Service?" -> DELETE /v1/Services/{Sid}
- "Create a ShortCode?" -> POST /v1/Services/{ServiceSid}/ShortCodes
- "List all ShortCodes?" -> GET /v1/Services/{ServiceSid}/ShortCodes
- "Delete a ShortCode?" -> DELETE /v1/Services/{ServiceSid}/ShortCodes/{Sid}
- "Get ShortCode details?" -> GET /v1/Services/{ServiceSid}/ShortCodes/{Sid}
- "Get Verification details?" -> GET /v1/Tollfree/Verifications/{Sid}
- "Delete a Verification?" -> DELETE /v1/Tollfree/Verifications/{Sid}
- "List all Verifications?" -> GET /v1/Tollfree/Verifications
- "Create a Verification?" -> POST /v1/Tollfree/Verifications
- "Create a Usa2p?" -> POST /v1/Services/{MessagingServiceSid}/Compliance/Usa2p
- "List all Usa2p?" -> GET /v1/Services/{MessagingServiceSid}/Compliance/Usa2p
- "Delete a Usa2p?" -> DELETE /v1/Services/{MessagingServiceSid}/Compliance/Usa2p/{Sid}
- "Get Usa2p details?" -> GET /v1/Services/{MessagingServiceSid}/Compliance/Usa2p/{Sid}
- "List all Usecases?" -> GET /v1/Services/{MessagingServiceSid}/Compliance/Usa2p/Usecases
- "List all Usecases?" -> GET /v1/Services/Usecases
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
