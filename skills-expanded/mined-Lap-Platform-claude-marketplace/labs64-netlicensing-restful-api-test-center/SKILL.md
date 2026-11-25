---
name: labs64-netlicensing-restful-api-test-center
description: "Labs64 NetLicensing RESTful API Test Center API skill. Use when working with Labs64 NetLicensing RESTful API Test Center for product, productmodule, licensetemplate. Covers 40 endpoints."
version: 1.0.0
generator: lapsh
---

# Labs64 NetLicensing RESTful API Test Center
API version: 2.x

## Auth
basic

## Base URL
https://go.netlicensing.io/core/v2/rest

## Setup
1. Configure auth: basic
2. GET /product -- verify access
3. POST /product -- create first product

## Endpoints

40 endpoints across 9 groups. See references/api-spec.lap for full details.

### product
| Method | Path | Description |
|--------|------|-------------|
| GET | /product | List Products |
| POST | /product | Create Product |
| GET | /product/{productNumber} | Get Product |
| POST | /product/{productNumber} | Update Product |
| DELETE | /product/{productNumber} | Delete Product |

### productmodule
| Method | Path | Description |
|--------|------|-------------|
| GET | /productmodule | List Product Modules |
| POST | /productmodule | Create Product Module |
| GET | /productmodule/{productModuleNumber} | Get Product Module |
| POST | /productmodule/{productModuleNumber} | Update Product Module |
| DELETE | /productmodule/{productModuleNumber} | Delete Product Module |

### licensetemplate
| Method | Path | Description |
|--------|------|-------------|
| GET | /licensetemplate | List License Templates |
| POST | /licensetemplate | Create License Template |
| GET | /licensetemplate/{licenseTemplateNumber} | Get License Template |
| POST | /licensetemplate/{licenseTemplateNumber} | Update License Template |
| DELETE | /licensetemplate/{licenseTemplateNumber} | Delete License Template |

### licensee
| Method | Path | Description |
|--------|------|-------------|
| GET | /licensee | List Licensees |
| POST | /licensee | Create Licensee |
| GET | /licensee/{licenseeNumber} | Get Licensee |
| POST | /licensee/{licenseeNumber} | Update Licensee |
| DELETE | /licensee/{licenseeNumber} | Delete Licensee |
| POST | /licensee/{licenseeNumber}/validate | Validate Licensee |
| POST | /licensee/{licenseeNumber}/transfer | Transfer Licenses |

### license
| Method | Path | Description |
|--------|------|-------------|
| GET | /license | List Licenses |
| POST | /license | Create License |
| GET | /license/{licenseNumber} | Get License |
| POST | /license/{licenseNumber} | Update License |
| DELETE | /license/{licenseNumber} | Delete License |

### transaction
| Method | Path | Description |
|--------|------|-------------|
| GET | /transaction | List Transactions |
| POST | /transaction | Create Transaction |
| GET | /transaction/{transactionNumber} | Get Transaction |
| POST | /transaction/{transactionNumber} | Update Transaction |

### token
| Method | Path | Description |
|--------|------|-------------|
| GET | /token | List Tokens |
| POST | /token | Create token |
| GET | /token/{tokenNumber} | Get token |
| DELETE | /token/{tokenNumber} | Delete token |

### paymentmethod
| Method | Path | Description |
|--------|------|-------------|
| GET | /paymentmethod | List Payment Methods |
| GET | /paymentmethod/{paymentMethodNumber} | Get Payment Method |
| POST | /paymentmethod/{paymentMethodNumber} | Update Payment Method |

### utility
| Method | Path | Description |
|--------|------|-------------|
| GET | /utility/licensingModels | List Licensing Models |
| GET | /utility/licenseTypes | List License Types |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all product?" -> GET /product
- "Create a product?" -> POST /product
- "Get product details?" -> GET /product/{productNumber}
- "Delete a product?" -> DELETE /product/{productNumber}
- "List all productmodule?" -> GET /productmodule
- "Create a productmodule?" -> POST /productmodule
- "Get productmodule details?" -> GET /productmodule/{productModuleNumber}
- "Delete a productmodule?" -> DELETE /productmodule/{productModuleNumber}
- "List all licensetemplate?" -> GET /licensetemplate
- "Create a licensetemplate?" -> POST /licensetemplate
- "Get licensetemplate details?" -> GET /licensetemplate/{licenseTemplateNumber}
- "Delete a licensetemplate?" -> DELETE /licensetemplate/{licenseTemplateNumber}
- "List all licensee?" -> GET /licensee
- "Create a licensee?" -> POST /licensee
- "Get licensee details?" -> GET /licensee/{licenseeNumber}
- "Delete a licensee?" -> DELETE /licensee/{licenseeNumber}
- "Create a validate?" -> POST /licensee/{licenseeNumber}/validate
- "Create a transfer?" -> POST /licensee/{licenseeNumber}/transfer
- "List all license?" -> GET /license
- "Create a license?" -> POST /license
- "Get license details?" -> GET /license/{licenseNumber}
- "Delete a license?" -> DELETE /license/{licenseNumber}
- "List all transaction?" -> GET /transaction
- "Create a transaction?" -> POST /transaction
- "Get transaction details?" -> GET /transaction/{transactionNumber}
- "List all token?" -> GET /token
- "Create a token?" -> POST /token
- "Get token details?" -> GET /token/{tokenNumber}
- "Delete a token?" -> DELETE /token/{tokenNumber}
- "List all paymentmethod?" -> GET /paymentmethod
- "Get paymentmethod details?" -> GET /paymentmethod/{paymentMethodNumber}
- "List all licensingModels?" -> GET /utility/licensingModels
- "List all licenseTypes?" -> GET /utility/licenseTypes
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
