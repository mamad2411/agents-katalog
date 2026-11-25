---
name: xtrf-home-portal-api
description: "XTRF Home Portal API skill. Use when working with XTRF Home Portal for browser, accounting, customers. Covers 341 endpoints."
version: 1.0.0
generator: lapsh
---

# XTRF Home Portal API
API version: 2.0

## Auth
ApiKey X-AUTH-ACCESS-TOKEN in header

## Base URL
https://presentation.s.xtrf.eu/home-api

## Setup
1. Set your API key in the appropriate header
2. GET /browser/csv -- verify access
3. POST /browser/views/for/{className} -- create first for

## Endpoints

341 endpoints across 20 groups. See references/api-spec.lap for full details.

### browser
| Method | Path | Description |
|--------|------|-------------|
| GET | /browser/csv | Searches for data (ie. customer, task, etc) and returns it in a CSV form. |
| GET | /browser | Searches for data (ie. customer, task, etc) and returns it in a tabular form. |
| GET | /browser/views/for/{className} | Returns views' brief. |
| POST | /browser/views/for/{className} | Creates view for given class. |
| GET | /browser/views/{viewId} | Returns all view's information. |
| PUT | /browser/views/{viewId} | Updates all view's information. |
| DELETE | /browser/views/{viewId} | Removes a view. |
| DELETE | /browser/views/{viewId}/columns/{columnName} | Deletes a single column from view. |
| GET | /browser/views/{viewId}/columns/{columnName}/settings | Returns column's specific settings. |
| PUT | /browser/views/{viewId}/columns/{columnName}/settings | Updates column's specific settings. |
| GET | /browser/views/{viewId}/columns | Returns columns defined in view. |
| PUT | /browser/views/{viewId}/columns | Updates columns in view. |
| GET | /browser/views/details/for/{className} | Returns current view's detailed information, suitable for browser. |
| GET | /browser/views/{viewId}/filter | Returns view's filter. |
| PUT | /browser/views/{viewId}/filter | Updates view's filter. |
| GET | /browser/views/{viewId}/settings/local | Returns view's local settings (for current user). |
| PUT | /browser/views/{viewId}/settings/local | Updates view's local settings (for current user). |
| GET | /browser/views/{viewId}/order | Returns view's order settings. |
| PUT | /browser/views/{viewId}/order | Updates view's order settings. |
| GET | /browser/views/{viewId}/permissions | Returns view's permissions. |
| PUT | /browser/views/{viewId}/permissions | Updates view's permissions. |
| GET | /browser/views/{viewId}/settings | Returns view's settings. |
| PUT | /browser/views/{viewId}/settings | Updates view's settings. |
| GET | /browser/views/details/for/{className}/{viewId} | Returns view's detailed information, suitable for browser. |
| POST | /browser/views/details/for/{className}/{viewId} | Selects given view as current and returns its detailed information, suitable for browser. |
| PUT | /browser/views/{viewId}/filter/{filterProperty} | Updates view's filter property. |

### accounting
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounting/customers/invoices | Lists all client invoices in all statuses (including not ready and drafts) that have been updated since a specific date. |
| POST | /accounting/customers/invoices | Creates a new invoice. |
| GET | /accounting/customers/invoices/{invoiceId}/payments | Returns all payments for the client invoice. |
| POST | /accounting/customers/invoices/{invoiceId}/payments | Adds a new payment to the client invoice. The invoice payment status (Not Paid, Partially Paid, Fully Paid) is automatically recalculated. |
| GET | /accounting/customers/invoices/{invoiceId} | Returns client invoice details. |
| DELETE | /accounting/customers/invoices/{invoiceId} | Removes a client invoice. |
| POST | /accounting/customers/invoices/documents | Allows for downloading multiple client invoice documents. |
| POST | /accounting/customers/invoices/xmlDocuments | Allows for downloading multiple client invoice xml documents. |
| POST | /accounting/customers/invoices/{invoiceId}/duplicate | Duplicate client invoice. |
| POST | /accounting/customers/invoices/{invoiceId}/duplicate/proForma | Duplicate client invoice as pro forma. |
| GET | /accounting/customers/invoices/ids | Returns client invoices' internal identifiers. |
| GET | /accounting/customers/invoices/{invoiceId}/dates | Returns dates of a given client invoice. |
| GET | /accounting/customers/invoices/{invoiceId}/document | Allows for downloading a given client invoice document. |
| GET | /accounting/customers/invoices/{invoiceId}/paymentTerms | Returns payment terms of a given client invoice. |
| GET | /accounting/customers/invoices/{invoiceId}/xmlDocument | Allows for downloading a given client invoice xml document. |
| POST | /accounting/customers/invoices/{invoiceId}/sendReminder | Sends reminder. |
| POST | /accounting/customers/invoices/sendReminders | Sends reminders. Returns number of sent e-mails. |
| DELETE | /accounting/customers/payments/{paymentId} | Removes a customer payment. |
| GET | /accounting/providers/invoices | Lists all vendor invoices in all statuses (including not ready and drafts) that have been updated since a specific date. |
| POST | /accounting/providers/invoices | Creates a new invoice. |
| GET | /accounting/providers/invoices/{invoiceId}/payments | Returns all payments for the vendor invoice. |
| POST | /accounting/providers/invoices/{invoiceId}/payments | Creates a new payment on the vendor account and assigns the payment to the invoice. |
| GET | /accounting/providers/invoices/{invoiceId} | Returns provider invoice details. |
| DELETE | /accounting/providers/invoices/{invoiceId} | Removes a provider invoice. |
| GET | /accounting/providers/invoices/ids | Returns vendor invoices' internal identifiers. |
| GET | /accounting/providers/invoices/{invoiceId}/document | Generates provider invoice document (PDF). |
| POST | /accounting/providers/invoices/{invoiceId}/send | Sends a provider invoice. |
| POST | /accounting/providers/invoices/{invoiceId}/status | Changes invoice status to given status. |
| DELETE | /accounting/providers/payments/{paymentId} | Removes a provider payment. |

### customers
| Method | Path | Description |
|--------|------|-------------|
| POST | /customers/persons | Creates a new person. |
| GET | /customers/persons/{personId} | Returns person details. |
| PUT | /customers/persons/{personId} | Updates an existing person. |
| DELETE | /customers/persons/{personId} | Removes a person. |
| POST | /customers/persons/accessToken | Generates a single use sign-in token. |
| GET | /customers/persons/ids | Returns persons' internal identifiers. |
| GET | /customers/persons/{personId}/contact | Returns contact of a given person. |
| PUT | /customers/persons/{personId}/contact | Updates contact of a given person. |
| GET | /customers/persons/{personId}/customFields | Returns custom fields of a given person. |
| PUT | /customers/persons/{personId}/customFields | Updates custom fields of a given person. |
| DELETE | /customers/priceLists/{priceListId} | Removes a customer price list. |
| GET | /customers | Returns list of simple clients representations |
| POST | /customers | Creates a new client. |
| GET | /customers/{customerId} | Returns client details. |
| PUT | /customers/{customerId} | Updates an existing client. |
| DELETE | /customers/{customerId} | Removes a client. |
| GET | /customers/{customerId}/priceProfiles/active | Returns list of active price profiles for a client. |
| GET | /customers/{customerId}/address | Returns address of a given client. |
| PUT | /customers/{customerId}/address | Updates address of a given client. |
| GET | /customers/ids | Returns clients' internal identifiers. |
| GET | /customers/{customerId}/budgetCodes | Returns list of available budget codes for a client. |
| GET | /customers/byAlias | Returns client details. |
| GET | /customers/{customerId}/categories | Returns categories of a given client. |
| PUT | /customers/{customerId}/categories | Updates categories of a given client. |
| GET | /customers/{customerId}/contact | Returns contact of a given client. |
| PUT | /customers/{customerId}/contact | Updates contact of a given client. |
| GET | /customers/{customerId}/correspondenceAddress | Returns correspondence address of a given client. |
| PUT | /customers/{customerId}/correspondenceAddress | Updates correspondence address of a given client. |
| GET | /customers/{customerId}/customFields/{customFieldKey} | Returns custom field of a given client. |
| PUT | /customers/{customerId}/customFields/{customFieldKey} | Updates given custom field of a given client. |
| GET | /customers/{customerId}/customFields | Returns custom fields of a given client. |
| PUT | /customers/{customerId}/customFields | Updates custom fields of a given client. |
| GET | /customers/{customerId}/settings/specializations | Returns specializations available for a given client in the Client Portal. |
| GET | /customers/{customerId}/industries | Returns industries of a given client. |
| PUT | /customers/{customerId}/industries | Updates industries of a given client. |
| GET | /customers/{customerId}/settings/languages | Returns languages available for a given client in the Client Portal. |
| GET | /customers/{customerId}/offices | Returns list of offices in the office structure in which the client is located. |
| GET | /customers/{customerId}/services | Returns list of available services for a client. |

### files
| Method | Path | Description |
|--------|------|-------------|
| POST | /files | Uploads a temporary file (ie. for XML import). Returns token which can be used in other API calls. |

### license
| Method | Path | Description |
|--------|------|-------------|
| GET | /license | Returns license content. |
| POST | /license/refresh | Refreshes license content. |

### macros
| Method | Path | Description |
|--------|------|-------------|
| POST | /macros/{macroId}/run | Executes a macro. |

### confidential-groups
| Method | Path | Description |
|--------|------|-------------|
| POST | /confidential-groups/sensitiveClients/client | Adds client to sensitive clients list. |
| GET | /confidential-groups/sensitiveClients | Returns sensitive clients list. |
| PUT | /confidential-groups/sensitiveClients | Updates sensitive clients list. |
| GET | /confidential-groups/sensitiveClients/isSensitive/{clientId} | Check if client is sensitive. |
| DELETE | /confidential-groups/sensitiveClients/client/{sensitiveClientId} | Removes sensitive client from sensitive clients list. |
| POST | /confidential-groups/trustedVendors/vendor | Adds vendor to trusted vendors list. |
| GET | /confidential-groups/trustedVendors | Returns trusted vendors list. |
| PUT | /confidential-groups/trustedVendors | Updates trusted vendors list. |
| DELETE | /confidential-groups/trustedVendors/vendor/{trustedVendorId} | Removes trusted vendor from trusted vendors list. |

### projectGroups
| Method | Path | Description |
|--------|------|-------------|
| GET | /projectGroups | Returns all project groups. |
| POST | /projectGroups | Creates a new Project Groups. |
| GET | /projectGroups/{projectGroupId} | Returns project group details. |
| PUT | /projectGroups/{projectGroupId} | Update project group details. |
| DELETE | /projectGroups/{projectGroupId} | Removes a project group. |
| PUT | /projectGroups/{projectGroupId}/linkProjects | Add projects to project group. |
| PUT | /projectGroups/{projectGroupId}/linkQuotes | Add quotes to project group. |
| PUT | /projectGroups/{projectGroupId}/unlinkProjects | Remove projects from project group. |
| PUT | /projectGroups/{projectGroupId}/unlinkQuotes | Remove quotes from project group. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/persons/{personId} | Returns person details. |
| DELETE | /providers/persons/{personId} | Removes a person. |
| GET | /providers/persons/ids | Returns persons' internal identifiers. |
| GET | /providers/persons/{personId}/contact | Returns contact of a given person. |
| GET | /providers/persons/{personId}/customFields | Returns custom fields of a given person. |
| POST | /providers/persons/{personId}/notification/invitation | Sends invitation to Vendor Portal. |
| DELETE | /providers/priceLists/{priceListId} | Removes a provider price list. |
| GET | /providers/{providerId} | Returns provider details. |
| DELETE | /providers/{providerId} | Removes a provider. |
| GET | /providers/{providerId}/address | Returns address of a given provider. |
| GET | /providers/ids | Returns providers' internal identifiers. |
| GET | /providers/{providerId}/competencies | Returns competencies of a given provider. |
| GET | /providers/{providerId}/contact | Returns contact of a given provider. |
| GET | /providers/{providerId}/correspondenceAddress | Returns correspondence address of a given provider. |
| GET | /providers/{providerId}/customFields | Returns custom fields of a given provider. |
| POST | /providers/{providerId}/notification/invitation | Sends invitations to Vendor Portal. |

### reports
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /reports/{reportId} | Removes a report. |
| POST | /reports/{reportId}/duplicate | Duplicates a report. |
| POST | /reports/export/xml | Exports reports definition to XML. |
| GET | /reports/{reportId}/result/csv | Generates CSV content for a report. |
| GET | /reports/{reportId}/result/printerFriendly | Generates printer friendly content for a report. |
| POST | /reports/import/xml | Imports reports definition from XML. |
| PUT | /reports/{reportId}/preferred | Marks report as preferred or not. |

### services
| Method | Path | Description |
|--------|------|-------------|
| GET | /services/all | Returns services list |
| GET | /services/active | Returns active services list |

### settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /settings/customFields | Returns Custom Fields configuration. |

### subscription
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscription/supports | This method can be used to determine if hooks are supported. |
| GET | /subscription | Returns all subscriptions |
| POST | /subscription | Subscribe to event |
| DELETE | /subscription/{subscriptionId} | Unsubscribe from event |

### system
| Method | Path | Description |
|--------|------|-------------|
| GET | /system/configuration/email | Get email configuration |
| GET | /system/configuration/ftp | Get FTP configuration |
| GET | /system/configuration | Get basic system configuration |
| GET | /system/timeZone | Get system timezone information |

### users
| Method | Path | Description |
|--------|------|-------------|
| PUT | /users/{userId}/password | Sets user's password to a new value. |
| GET | /users | Returns list of simple users representations |
| GET | /users/{userId} | Returns user details. |
| PUT | /users/{userId} | Updates an existing user. |
| GET | /users/{userId}/customFields/{customFieldKey} | Returns custom field of a given user. |
| PUT | /users/{userId}/customFields/{customFieldKey} | Updates given custom field of a given user. |
| GET | /users/{userId}/customFields | Returns custom fields of a given user. |
| PUT | /users/{userId}/customFields | Updates custom fields of a given user. |
| GET | /users/me | Returns currently signed in user details. |
| GET | /users/me/timeZone | Returns time zone preferred by user currently signed in. |

### dictionaries
| Method | Path | Description |
|--------|------|-------------|
| GET | /dictionaries/active | Returns active dictionary entities for all types. |
| GET | /dictionaries/{type}/active | Returns active values from a given dictionary. |
| GET | /dictionaries/all | Returns dictionary entities for all types. Both active and not active ones. |
| GET | /dictionaries/{type}/all | Returns all values (both active and not active) from a given dictionary. |
| GET | /dictionaries/{type}/{id} | Returns specific value from a given dictionary. |
| GET | /dictionaries/{type}/all/default | Returns a default value from a given dictionary. |
| GET | /dictionaries/currency/{isoCode}/exchangeRate | Returns currency exchange rates. |
| POST | /dictionaries/currency/{isoCode}/exchangeRate | Adding currency exchange rates. |
| POST | /v2/dictionaries/language |  |
| PATCH | /v2/dictionaries/language/{languageId} |  |
| POST | /v2/dictionaries/specialization |  |
| PATCH | /v2/dictionaries/specialization/{specializationId} |  |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /jobs/{jobId}/files/output |  |
| PUT | /jobs/{jobId}/vendor | Assigns vendor to a job in a project. |
| PUT | /jobs/{jobId}/status | Changes job status if possible (400 Bad Request is returned otherwise). |
| GET | /jobs/{jobId} | Returns job details by jobId. |
| GET | /jobs/{jobId}/files | Returns list of input and output files of a job. |
| GET | /jobs/{jobId}/files/{fileId} | Returns file metadata. |
| PUT | /jobs/{jobId}/dates | Updates dates of a given job. |
| PUT | /jobs/{jobId}/instructions | Updates instructions for a job. |
| POST | /v2/jobs/{jobId}/files/addExternalLink |  |
| POST | /v2/jobs/{jobId}/files/delivered/addLink | Adds file link to the project as a link delivered in the job. |
| PUT | /v2/jobs/{jobId}/files/delivered/add | Adds files to the project as delivered in the job. |
| PUT | /v2/jobs/{jobId}/vendor | Assigns vendor to a job in a project. |
| PUT | /v2/jobs/{jobId}/dates | Updates dates of a given job. |
| PUT | /v2/jobs/{jobId}/status | Changes job status if possible (400 Bad Request is returned otherwise). |
| GET | /v2/jobs/{jobId} | Returns details for a job. |
| DELETE | /v2/jobs/{jobId} | Deletes a job. |
| GET | /v2/jobs/for-external-id |  |
| GET | /v2/jobs/{jobId}/files/delivered | Returns list of files delivered in the job. |
| GET | /v2/jobs/{jobId}/files/sharedReferenceFiles | Returns list of files shared with the job as Reference Files. |
| GET | /v2/jobs/{jobId}/files/sharedWorkFiles | Returns list of files shared with the job as Work Files. |
| POST | /v2/jobs/merge | Merges given list of jobs into one job. |
| PUT | /v2/jobs/{jobId}/files/sharedReferenceFiles/share | Shares selected files as Reference Files with a job in a project. |
| PUT | /v2/jobs/{jobId}/files/sharedWorkFiles/share | Shares selected files as Work Files with a job in a project. |
| PUT | /v2/jobs/{jobId}/files/stopSharing | Stops sharing selected files with a job in a project. |
| PUT | /v2/jobs/{jobId}/instructions | Updates instructions for a job. |
| POST | /v2/jobs/{jobId}/files/delivered/upload | Uploads file to the project as a file delivered in the job. |
| POST | /v2/jobs/{jobId}/files/delivered/uploadFileByVendor | Uploads file to the project as a file delivered in the job, added by vendor. |

### projects
| Method | Path | Description |
|--------|------|-------------|
| POST | /projects | Creates a new Classic Project. |
| POST | /projects/{projectId}/languageCombinations | Creates a new language combination for a given project without creating a task. |
| POST | /projects/{projectId}/finance/payables | Adds a payable to a project. |
| POST | /projects/{projectId}/finance/receivables | Adds a receivable to a project. |
| POST | /projects/{projectId}/tasks | Creates a new task for a given project. |
| GET | /projects/{projectId} | Returns project details. |
| DELETE | /projects/{projectId} | Removes a project. |
| PUT | /projects/{projectId}/finance/payables/{payableId} | Updates a simple payable. |
| DELETE | /projects/{projectId}/finance/payables/{payableId} | Deletes a payable. |
| PUT | /projects/{projectId}/finance/receivables/{receivableId} | Updates a simple receivable. |
| DELETE | /projects/{projectId}/finance/receivables/{receivableId} | Deletes a receivable. |
| GET | /projects/ids | Returns projects' internal identifiers. |
| GET | /projects/{projectId}/contacts | Returns contacts of a given project. |
| PUT | /projects/{projectId}/contacts | Updates contacts of a given project. |
| GET | /projects/{projectId}/customFields | Returns custom fields of a given project. |
| PUT | /projects/{projectId}/customFields | Updates custom fields of a given project. |
| GET | /projects/{projectId}/dates | Returns dates of a given project. |
| PUT | /projects/{projectId}/dates | Updates dates of a given project. |
| GET | /projects/files/{fileId}/download | Downloads a file. |
| GET | /projects/{projectId}/finance | Returns finance of a given project. |
| GET | /projects/{projectId}/instructions | Returns instructions of a given project. |
| PUT | /projects/{projectId}/instructions | Updates instructions of a given project. |
| POST | /v2/projects/{projectId}/files/addExternalLinks |  |
| POST | /v2/projects/{projectId}/externalInfo |  |
| POST | /v2/projects/{projectId}/files/addLink | Adds file links to the project as added by PM. |
| PUT | /v2/projects/{projectId}/files/add | Adds files to the project as added by PM. |
| POST | /v2/projects/{projectId}/addJob |  |
| PUT | /v2/projects/{projectId}/files/addTargetFile | Adds target file to the project as added by PM. |
| POST | /v2/projects/files/archive | Prepares a ZIP archive that contains the specified files. |
| PUT | /v2/projects/{projectId}/status | Changes project status if possible (400 Bad Request is returned otherwise). |
| POST | /v2/projects | Creates a new Smart Project. |
| POST | /v2/projects/{projectId}/createCatToolProject | Creates Cat Tool Project corresponding to XTRF project. |
| POST | /v2/projects/{projectId}/finance/payables | Adds a payable to a project. |
| POST | /v2/projects/{projectId}/finance/receivables | Adds a receivable to a project. |
| DELETE | /v2/projects/{projectId}/files/{fileId} | Deletes a file. |
| PUT | /v2/projects/{projectId}/finance/payables/{payableId} | Updates a simple payable. |
| DELETE | /v2/projects/{projectId}/finance/payables/{payableId} | Deletes a payable. |
| PUT | /v2/projects/{projectId}/finance/receivables/{receivableId} | Updates a simple receivable. |
| DELETE | /v2/projects/{projectId}/finance/receivables/{receivableId} | Deletes a receivable. |
| GET | /v2/projects/for-external-id/{externalProjectId} | Returns project details. |
| GET | /v2/projects/{projectId} | Returns project details. |
| GET | /v2/projects/{projectId}/catToolProject | Returns if cat tool project is created or queued. |
| GET | /v2/projects/catToolProjectTemplates | Returns CAT Tool project templates available for selection in XTRF. |
| GET | /v2/projects/{projectId}/clientContacts | Returns Client Contacts information for a project. |
| PUT | /v2/projects/{projectId}/clientContacts | Updates Client Contacts for a project. |
| GET | /v2/projects/{projectId}/customFields | Returns a list of custom field keys and values for a project. |
| GET | /v2/projects/{projectId}/files/deliverable | Returns list of files in a project, that are ready to be delivered to client. |
| GET | /v2/projects/files/{fileId} | Returns details of a file. |
| GET | /v2/projects/files/{fileId}/download/{fileName} | Downloads a file content. |
| GET | /v2/projects/{projectId}/files | Returns list of files in a project. |
| GET | /v2/projects/{projectId}/finance | Returns finance information for a project. |
| GET | /v2/projects/{projectId}/jobs | Returns list of jobs in a project. |
| GET | /v2/projects/{projectId}/process | Returns process id. |
| PUT | /v2/projects/{projectId}/catToolProjectTemplateDetails | Updates template details for a project. |
| PUT | /v2/projects/{projectId}/clientDeadline | Updates Client Deadline for a project. |
| PUT | /v2/projects/{projectId}/clientNotes | Updates Client Notes for a project. |
| PUT | /v2/projects/{projectId}/clientReferenceNumber | Updates Client Reference Number for a project. |
| PUT | /v2/projects/{projectId}/customFields/{key} | Updates a custom field with a specified key in a project |
| PUT | /v2/projects/{projectId}/internalNotes | Updates Internal Notes for a project. |
| PUT | /v2/projects/{projectId}/orderDate | Updates Order Date for a project. |
| PUT | /v2/projects/{projectId}/processType |  |
| PUT | /v2/projects/{projectId}/sourceLanguage | Updates source language for a project. |
| PUT | /v2/projects/{projectId}/specialization | Updates specialization for a project. |
| PUT | /v2/projects/{projectId}/targetLanguages | Updates target languages for a project. |
| PUT | /v2/projects/{projectId}/vendorInstructions | Updates instructions for all vendors performing the jobs in a project. |
| PUT | /v2/projects/{projectId}/volume | Updates volume for a project. |
| POST | /v2/projects/{projectId}/files/upload | Uploads file to the project as a file uploaded by PM. |

### quotes
| Method | Path | Description |
|--------|------|-------------|
| POST | /quotes/{quoteId}/languageCombinations | Creates a new language combination for a given quote without creating a task. |
| POST | /quotes/{quoteId}/finance/payables | Adds a payable. |
| POST | /quotes/{quoteId}/finance/receivables | Adds a receivable. |
| POST | /quotes/{quoteId}/tasks | Creates a new task for a given quote. |
| GET | /quotes/{quoteId} | Returns quote details. |
| DELETE | /quotes/{quoteId} | Removes a quote. |
| PUT | /quotes/{quoteId}/finance/payables/{payableId} | Updates a simple payable. |
| DELETE | /quotes/{quoteId}/finance/payables/{payableId} | Deletes a payable. |
| PUT | /quotes/{quoteId}/finance/receivables/{receivableId} | Updates a simple receivable. |
| DELETE | /quotes/{quoteId}/finance/receivables/{receivableId} | Deletes a receivable. |
| GET | /quotes/ids | Returns quotes' internal identifiers. |
| GET | /quotes/{quoteId}/customFields | Returns custom fields of a given quote. |
| PUT | /quotes/{quoteId}/customFields | Updates custom fields of a given quote. |
| GET | /quotes/{quoteId}/dates | Returns dates of a given quote. |
| GET | /quotes/{quoteId}/finance | Returns finance of a given quote. |
| GET | /quotes/{quoteId}/instructions | Returns instructions of a given quote. |
| PUT | /quotes/{quoteId}/instructions | Updates instructions of a given quote. |
| POST | /quotes/{quoteId}/confirmation/send | Sends a quote for customer confirmation. |
| POST | /quotes/{quoteId}/start | Starts a quote. |
| POST | /v2/quotes/{quoteId}/files/addExternalLinks |  |
| POST | /v2/quotes/{quoteId}/externalInfo |  |
| POST | /v2/quotes/{quoteId}/files/addLink | Adds file links to the quote as added by PM. |
| PUT | /v2/quotes/{quoteId}/files/add | Adds files to the quote as added by PM. |
| POST | /v2/quotes/{quoteId}/addJob |  |
| PUT | /v2/quotes/{quoteId}/files/addTargetFile | Adds target file to the quote as added by PM. |
| POST | /v2/quotes/files/archive | Prepares a ZIP archive that contains the specified files. |
| PUT | /v2/quotes/{quoteId}/status | Changes quote status if possible (400 Bad Request is returned otherwise). |
| POST | /v2/quotes | Creates a new Smart Quote. |
| POST | /v2/quotes/{quoteId}/finance/payables | Adds a payable to a quote. |
| POST | /v2/quotes/{quoteId}/finance/receivables | Adds a receivable to a quote. |
| DELETE | /v2/quotes/{quoteId}/files/{fileId} | Deletes a file. |
| PUT | /v2/quotes/{quoteId}/finance/payables/{payableId} | Updates a simple payable. |
| DELETE | /v2/quotes/{quoteId}/finance/payables/{payableId} | Deletes a payable. |
| PUT | /v2/quotes/{quoteId}/finance/receivables/{receivableId} | Updates a simple receivable. |
| DELETE | /v2/quotes/{quoteId}/finance/receivables/{receivableId} | Deletes a receivable. |
| GET | /v2/quotes/for-external-id/{externalProjectId} | Returns quote details. |
| GET | /v2/quotes/{quoteId} | Returns quote details. |
| GET | /v2/quotes/{quoteId}/clientContacts | Returns Client Contacts information for a quote. |
| PUT | /v2/quotes/{quoteId}/clientContacts | Updates Client Contacts for a quote. |
| GET | /v2/quotes/{quoteId}/customFields | Returns a list of custom field keys and values for a project. |
| GET | /v2/quotes/files/{fileId} | Returns details of a file. |
| GET | /v2/quotes/files/{fileId}/download/{fileName} | Downloads a file content. |
| GET | /v2/quotes/{quoteId}/files | Returns list of files in a quote. |
| GET | /v2/quotes/{quoteId}/finance | Returns finance information for a quote. |
| GET | /v2/quotes/{quoteId}/jobs | Returns list of jobs in a quote. |
| GET | /v2/quotes/{quoteId}/process | Returns process id. |
| PUT | /v2/quotes/{quoteId}/businessDays | Updates Business Days for a quote. |
| PUT | /v2/quotes/{quoteId}/catToolProjectTemplateDetails | Updates template details for a quote. |
| PUT | /v2/quotes/{quoteId}/clientNotes | Updates Client Notes for a quote. |
| PUT | /v2/quotes/{quoteId}/clientReferenceNumber | Updates Client Reference Number for a quote. |
| PUT | /v2/quotes/{quoteId}/customFields/{key} | Updates a custom field with a specified key in a quote. |
| PUT | /v2/quotes/{quoteId}/expectedDeliveryDate | Updates Expected Delivery Date for a quote. |
| PUT | /v2/quotes/{quoteId}/internalNotes | Updates Internal Notes for a quote. |
| PUT | /v2/quotes/{quoteId}/processType |  |
| PUT | /v2/quotes/{quoteId}/quoteExpiry | Updates Quote Expiry Date for a quote. |
| PUT | /v2/quotes/{quoteId}/sourceLanguage | Updates source language for a quote. |
| PUT | /v2/quotes/{quoteId}/specialization | Updates specialization for a quote. |
| PUT | /v2/quotes/{quoteId}/targetLanguages | Updates target languages for a quote. |
| PUT | /v2/quotes/{quoteId}/vendorInstructions | Updates instructions for all vendors performing the jobs in a quote. |
| PUT | /v2/quotes/{quoteId}/volume | Updates volume for a quote. |
| POST | /v2/quotes/{quoteId}/files/upload | Uploads file to the quote as a file uploaded by PM. |

### tasks
| Method | Path | Description |
|--------|------|-------------|
| POST | /tasks/{taskId}/files/input | Adds files to a given task. |
| DELETE | /tasks/{taskId} | Removes a task. |
| GET | /tasks/{taskId}/contacts | Returns contacts of a given task. |
| PUT | /tasks/{taskId}/contacts | Updates contacts of a given task. |
| GET | /tasks/{taskId}/customFields | Returns custom fields of a given task. |
| PUT | /tasks/{taskId}/customFields | Updates custom fields of a given task. |
| GET | /tasks/{taskId}/dates | Returns dates of a given task. |
| PUT | /tasks/{taskId}/dates | Updates dates of a given task. |
| GET | /tasks/{taskId}/instructions | Returns instructions of a given task. |
| PUT | /tasks/{taskId}/instructions | Updates instructions of a given task. |
| GET | /tasks/{taskId}/progress | Returns progress of a given task. |
| GET | /tasks/{taskId}/files | Returns lists of files of a given task. |
| POST | /tasks/{taskId}/start | Starts a task. |
| PUT | /tasks/{taskId}/clientTaskPONumber | Updates Client Task PO Number of a given task. |
| PUT | /tasks/{taskId}/name | Updates name of a given task. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all csv?" -> GET /browser/csv
- "List all browser?" -> GET /browser
- "Get for details?" -> GET /browser/views/for/{className}
- "Get view details?" -> GET /browser/views/{viewId}
- "Update a view?" -> PUT /browser/views/{viewId}
- "Delete a view?" -> DELETE /browser/views/{viewId}
- "Delete a column?" -> DELETE /browser/views/{viewId}/columns/{columnName}
- "List all settings?" -> GET /browser/views/{viewId}/columns/{columnName}/settings
- "List all columns?" -> GET /browser/views/{viewId}/columns
- "Get for details?" -> GET /browser/views/details/for/{className}
- "List all filter?" -> GET /browser/views/{viewId}/filter
- "List all local?" -> GET /browser/views/{viewId}/settings/local
- "List all order?" -> GET /browser/views/{viewId}/order
- "List all permissions?" -> GET /browser/views/{viewId}/permissions
- "List all settings?" -> GET /browser/views/{viewId}/settings
- "Get for details?" -> GET /browser/views/details/for/{className}/{viewId}
- "Update a filter?" -> PUT /browser/views/{viewId}/filter/{filterProperty}
- "List all invoices?" -> GET /accounting/customers/invoices
- "Create a invoice?" -> POST /accounting/customers/invoices
- "List all payments?" -> GET /accounting/customers/invoices/{invoiceId}/payments
- "Create a payment?" -> POST /accounting/customers/invoices/{invoiceId}/payments
- "Get invoice details?" -> GET /accounting/customers/invoices/{invoiceId}
- "Delete a invoice?" -> DELETE /accounting/customers/invoices/{invoiceId}
- "Create a document?" -> POST /accounting/customers/invoices/documents
- "Create a xmlDocument?" -> POST /accounting/customers/invoices/xmlDocuments
- "Create a duplicate?" -> POST /accounting/customers/invoices/{invoiceId}/duplicate
- "Create a proForma?" -> POST /accounting/customers/invoices/{invoiceId}/duplicate/proForma
- "List all ids?" -> GET /accounting/customers/invoices/ids
- "List all dates?" -> GET /accounting/customers/invoices/{invoiceId}/dates
- "List all document?" -> GET /accounting/customers/invoices/{invoiceId}/document
- "List all paymentTerms?" -> GET /accounting/customers/invoices/{invoiceId}/paymentTerms
- "List all xmlDocument?" -> GET /accounting/customers/invoices/{invoiceId}/xmlDocument
- "Create a sendReminder?" -> POST /accounting/customers/invoices/{invoiceId}/sendReminder
- "Create a sendReminder?" -> POST /accounting/customers/invoices/sendReminders
- "Delete a payment?" -> DELETE /accounting/customers/payments/{paymentId}
- "Create a person?" -> POST /customers/persons
- "Get person details?" -> GET /customers/persons/{personId}
- "Update a person?" -> PUT /customers/persons/{personId}
- "Delete a person?" -> DELETE /customers/persons/{personId}
- "Create a accessToken?" -> POST /customers/persons/accessToken
- "List all ids?" -> GET /customers/persons/ids
- "List all contact?" -> GET /customers/persons/{personId}/contact
- "List all customFields?" -> GET /customers/persons/{personId}/customFields
- "Delete a priceList?" -> DELETE /customers/priceLists/{priceListId}
- "List all customers?" -> GET /customers
- "Create a customer?" -> POST /customers
- "Get customer details?" -> GET /customers/{customerId}
- "Update a customer?" -> PUT /customers/{customerId}
- "Delete a customer?" -> DELETE /customers/{customerId}
- "List all active?" -> GET /customers/{customerId}/priceProfiles/active
- "List all address?" -> GET /customers/{customerId}/address
- "List all ids?" -> GET /customers/ids
- "List all budgetCodes?" -> GET /customers/{customerId}/budgetCodes
- "List all byAlias?" -> GET /customers/byAlias
- "List all categories?" -> GET /customers/{customerId}/categories
- "List all contact?" -> GET /customers/{customerId}/contact
- "List all correspondenceAddress?" -> GET /customers/{customerId}/correspondenceAddress
- "Get customField details?" -> GET /customers/{customerId}/customFields/{customFieldKey}
- "Update a customField?" -> PUT /customers/{customerId}/customFields/{customFieldKey}
- "List all customFields?" -> GET /customers/{customerId}/customFields
- "List all specializations?" -> GET /customers/{customerId}/settings/specializations
- "List all industries?" -> GET /customers/{customerId}/industries
- "List all languages?" -> GET /customers/{customerId}/settings/languages
- "List all offices?" -> GET /customers/{customerId}/offices
- "List all services?" -> GET /customers/{customerId}/services
- "Create a file?" -> POST /files
- "List all license?" -> GET /license
- "Create a refresh?" -> POST /license/refresh
- "Create a run?" -> POST /macros/{macroId}/run
- "Create a client?" -> POST /confidential-groups/sensitiveClients/client
- "List all sensitiveClients?" -> GET /confidential-groups/sensitiveClients
- "Get isSensitive details?" -> GET /confidential-groups/sensitiveClients/isSensitive/{clientId}
- "Delete a client?" -> DELETE /confidential-groups/sensitiveClients/client/{sensitiveClientId}
- "Create a vendor?" -> POST /confidential-groups/trustedVendors/vendor
- "List all trustedVendors?" -> GET /confidential-groups/trustedVendors
- "Delete a vendor?" -> DELETE /confidential-groups/trustedVendors/vendor/{trustedVendorId}
- "List all projectGroups?" -> GET /projectGroups
- "Create a projectGroup?" -> POST /projectGroups
- "Get projectGroup details?" -> GET /projectGroups/{projectGroupId}
- "Update a projectGroup?" -> PUT /projectGroups/{projectGroupId}
- "Delete a projectGroup?" -> DELETE /projectGroups/{projectGroupId}
- "List all invoices?" -> GET /accounting/providers/invoices
- "Create a invoice?" -> POST /accounting/providers/invoices
- "List all payments?" -> GET /accounting/providers/invoices/{invoiceId}/payments
- "Create a payment?" -> POST /accounting/providers/invoices/{invoiceId}/payments
- "Get invoice details?" -> GET /accounting/providers/invoices/{invoiceId}
- "Delete a invoice?" -> DELETE /accounting/providers/invoices/{invoiceId}
- "List all ids?" -> GET /accounting/providers/invoices/ids
- "List all document?" -> GET /accounting/providers/invoices/{invoiceId}/document
- "Create a send?" -> POST /accounting/providers/invoices/{invoiceId}/send
- "Create a status?" -> POST /accounting/providers/invoices/{invoiceId}/status
- "Delete a payment?" -> DELETE /accounting/providers/payments/{paymentId}
- "Get person details?" -> GET /providers/persons/{personId}
- "Delete a person?" -> DELETE /providers/persons/{personId}
- "List all ids?" -> GET /providers/persons/ids
- "List all contact?" -> GET /providers/persons/{personId}/contact
- "List all customFields?" -> GET /providers/persons/{personId}/customFields
- "Create a invitation?" -> POST /providers/persons/{personId}/notification/invitation
- "Delete a priceList?" -> DELETE /providers/priceLists/{priceListId}
- "Get provider details?" -> GET /providers/{providerId}
- "Delete a provider?" -> DELETE /providers/{providerId}
- "List all address?" -> GET /providers/{providerId}/address
- "List all ids?" -> GET /providers/ids
- "List all competencies?" -> GET /providers/{providerId}/competencies
- "List all contact?" -> GET /providers/{providerId}/contact
- "List all correspondenceAddress?" -> GET /providers/{providerId}/correspondenceAddress
- "List all customFields?" -> GET /providers/{providerId}/customFields
- "Create a invitation?" -> POST /providers/{providerId}/notification/invitation
- "Delete a report?" -> DELETE /reports/{reportId}
- "Create a duplicate?" -> POST /reports/{reportId}/duplicate
- "Create a xml?" -> POST /reports/export/xml
- "List all csv?" -> GET /reports/{reportId}/result/csv
- "List all printerFriendly?" -> GET /reports/{reportId}/result/printerFriendly
- "Create a xml?" -> POST /reports/import/xml
- "List all all?" -> GET /services/all
- "List all active?" -> GET /services/active
- "List all customFields?" -> GET /settings/customFields
- "List all supports?" -> GET /subscription/supports
- "List all subscription?" -> GET /subscription
- "Create a subscription?" -> POST /subscription
- "Delete a subscription?" -> DELETE /subscription/{subscriptionId}
- "List all email?" -> GET /system/configuration/email
- "List all ftp?" -> GET /system/configuration/ftp
- "List all configuration?" -> GET /system/configuration
- "List all timeZone?" -> GET /system/timeZone
- "List all users?" -> GET /users
- "Get user details?" -> GET /users/{userId}
- "Update a user?" -> PUT /users/{userId}
- "Get customField details?" -> GET /users/{userId}/customFields/{customFieldKey}
- "Update a customField?" -> PUT /users/{userId}/customFields/{customFieldKey}
- "List all customFields?" -> GET /users/{userId}/customFields
- "List all me?" -> GET /users/me
- "List all timeZone?" -> GET /users/me/timeZone
- "List all active?" -> GET /dictionaries/active
- "List all active?" -> GET /dictionaries/{type}/active
- "List all all?" -> GET /dictionaries/all
- "List all all?" -> GET /dictionaries/{type}/all
- "Get dictionary details?" -> GET /dictionaries/{type}/{id}
- "List all default?" -> GET /dictionaries/{type}/all/default
- "List all exchangeRate?" -> GET /dictionaries/currency/{isoCode}/exchangeRate
- "Create a exchangeRate?" -> POST /dictionaries/currency/{isoCode}/exchangeRate
- "Create a output?" -> POST /jobs/{jobId}/files/output
- "Get job details?" -> GET /jobs/{jobId}
- "List all files?" -> GET /jobs/{jobId}/files
- "Get file details?" -> GET /jobs/{jobId}/files/{fileId}
- "Create a project?" -> POST /projects
- "Create a languageCombination?" -> POST /projects/{projectId}/languageCombinations
- "Create a payable?" -> POST /projects/{projectId}/finance/payables
- "Create a receivable?" -> POST /projects/{projectId}/finance/receivables
- "Create a task?" -> POST /projects/{projectId}/tasks
- "Get project details?" -> GET /projects/{projectId}
- "Delete a project?" -> DELETE /projects/{projectId}
- "Update a payable?" -> PUT /projects/{projectId}/finance/payables/{payableId}
- "Delete a payable?" -> DELETE /projects/{projectId}/finance/payables/{payableId}
- "Update a receivable?" -> PUT /projects/{projectId}/finance/receivables/{receivableId}
- "Delete a receivable?" -> DELETE /projects/{projectId}/finance/receivables/{receivableId}
- "List all ids?" -> GET /projects/ids
- "List all contacts?" -> GET /projects/{projectId}/contacts
- "List all customFields?" -> GET /projects/{projectId}/customFields
- "List all dates?" -> GET /projects/{projectId}/dates
- "List all download?" -> GET /projects/files/{fileId}/download
- "List all finance?" -> GET /projects/{projectId}/finance
- "List all instructions?" -> GET /projects/{projectId}/instructions
- "Create a languageCombination?" -> POST /quotes/{quoteId}/languageCombinations
- "Create a payable?" -> POST /quotes/{quoteId}/finance/payables
- "Create a receivable?" -> POST /quotes/{quoteId}/finance/receivables
- "Create a task?" -> POST /quotes/{quoteId}/tasks
- "Get quote details?" -> GET /quotes/{quoteId}
- "Delete a quote?" -> DELETE /quotes/{quoteId}
- "Update a payable?" -> PUT /quotes/{quoteId}/finance/payables/{payableId}
- "Delete a payable?" -> DELETE /quotes/{quoteId}/finance/payables/{payableId}
- "Update a receivable?" -> PUT /quotes/{quoteId}/finance/receivables/{receivableId}
- "Delete a receivable?" -> DELETE /quotes/{quoteId}/finance/receivables/{receivableId}
- "List all ids?" -> GET /quotes/ids
- "List all customFields?" -> GET /quotes/{quoteId}/customFields
- "List all dates?" -> GET /quotes/{quoteId}/dates
- "List all finance?" -> GET /quotes/{quoteId}/finance
- "List all instructions?" -> GET /quotes/{quoteId}/instructions
- "Create a send?" -> POST /quotes/{quoteId}/confirmation/send
- "Create a start?" -> POST /quotes/{quoteId}/start
- "Create a input?" -> POST /tasks/{taskId}/files/input
- "Delete a task?" -> DELETE /tasks/{taskId}
- "List all contacts?" -> GET /tasks/{taskId}/contacts
- "List all customFields?" -> GET /tasks/{taskId}/customFields
- "List all dates?" -> GET /tasks/{taskId}/dates
- "List all instructions?" -> GET /tasks/{taskId}/instructions
- "List all progress?" -> GET /tasks/{taskId}/progress
- "List all files?" -> GET /tasks/{taskId}/files
- "Create a start?" -> POST /tasks/{taskId}/start
- "Create a language?" -> POST /v2/dictionaries/language
- "Partially update a language?" -> PATCH /v2/dictionaries/language/{languageId}
- "Create a specialization?" -> POST /v2/dictionaries/specialization
- "Partially update a specialization?" -> PATCH /v2/dictionaries/specialization/{specializationId}
- "Create a addExternalLink?" -> POST /v2/jobs/{jobId}/files/addExternalLink
- "Create a addLink?" -> POST /v2/jobs/{jobId}/files/delivered/addLink
- "Get job details?" -> GET /v2/jobs/{jobId}
- "Delete a job?" -> DELETE /v2/jobs/{jobId}
- "List all for-external-id?" -> GET /v2/jobs/for-external-id
- "List all delivered?" -> GET /v2/jobs/{jobId}/files/delivered
- "List all sharedReferenceFiles?" -> GET /v2/jobs/{jobId}/files/sharedReferenceFiles
- "List all sharedWorkFiles?" -> GET /v2/jobs/{jobId}/files/sharedWorkFiles
- "Create a merge?" -> POST /v2/jobs/merge
- "Create a upload?" -> POST /v2/jobs/{jobId}/files/delivered/upload
- "Create a uploadFileByVendor?" -> POST /v2/jobs/{jobId}/files/delivered/uploadFileByVendor
- "Create a addExternalLink?" -> POST /v2/projects/{projectId}/files/addExternalLinks
- "Create a externalInfo?" -> POST /v2/projects/{projectId}/externalInfo
- "Create a addLink?" -> POST /v2/projects/{projectId}/files/addLink
- "Create a addJob?" -> POST /v2/projects/{projectId}/addJob
- "Create a archive?" -> POST /v2/projects/files/archive
- "Create a project?" -> POST /v2/projects
- "Create a createCatToolProject?" -> POST /v2/projects/{projectId}/createCatToolProject
- "Create a payable?" -> POST /v2/projects/{projectId}/finance/payables
- "Create a receivable?" -> POST /v2/projects/{projectId}/finance/receivables
- "Delete a file?" -> DELETE /v2/projects/{projectId}/files/{fileId}
- "Update a payable?" -> PUT /v2/projects/{projectId}/finance/payables/{payableId}
- "Delete a payable?" -> DELETE /v2/projects/{projectId}/finance/payables/{payableId}
- "Update a receivable?" -> PUT /v2/projects/{projectId}/finance/receivables/{receivableId}
- "Delete a receivable?" -> DELETE /v2/projects/{projectId}/finance/receivables/{receivableId}
- "Get for-external-id details?" -> GET /v2/projects/for-external-id/{externalProjectId}
- "Get project details?" -> GET /v2/projects/{projectId}
- "List all catToolProject?" -> GET /v2/projects/{projectId}/catToolProject
- "List all catToolProjectTemplates?" -> GET /v2/projects/catToolProjectTemplates
- "List all clientContacts?" -> GET /v2/projects/{projectId}/clientContacts
- "List all customFields?" -> GET /v2/projects/{projectId}/customFields
- "List all deliverable?" -> GET /v2/projects/{projectId}/files/deliverable
- "Get file details?" -> GET /v2/projects/files/{fileId}
- "Get download details?" -> GET /v2/projects/files/{fileId}/download/{fileName}
- "List all files?" -> GET /v2/projects/{projectId}/files
- "List all finance?" -> GET /v2/projects/{projectId}/finance
- "List all jobs?" -> GET /v2/projects/{projectId}/jobs
- "List all process?" -> GET /v2/projects/{projectId}/process
- "Update a customField?" -> PUT /v2/projects/{projectId}/customFields/{key}
- "Create a upload?" -> POST /v2/projects/{projectId}/files/upload
- "Create a addExternalLink?" -> POST /v2/quotes/{quoteId}/files/addExternalLinks
- "Create a externalInfo?" -> POST /v2/quotes/{quoteId}/externalInfo
- "Create a addLink?" -> POST /v2/quotes/{quoteId}/files/addLink
- "Create a addJob?" -> POST /v2/quotes/{quoteId}/addJob
- "Create a archive?" -> POST /v2/quotes/files/archive
- "Create a quote?" -> POST /v2/quotes
- "Create a payable?" -> POST /v2/quotes/{quoteId}/finance/payables
- "Create a receivable?" -> POST /v2/quotes/{quoteId}/finance/receivables
- "Delete a file?" -> DELETE /v2/quotes/{quoteId}/files/{fileId}
- "Update a payable?" -> PUT /v2/quotes/{quoteId}/finance/payables/{payableId}
- "Delete a payable?" -> DELETE /v2/quotes/{quoteId}/finance/payables/{payableId}
- "Update a receivable?" -> PUT /v2/quotes/{quoteId}/finance/receivables/{receivableId}
- "Delete a receivable?" -> DELETE /v2/quotes/{quoteId}/finance/receivables/{receivableId}
- "Get for-external-id details?" -> GET /v2/quotes/for-external-id/{externalProjectId}
- "Get quote details?" -> GET /v2/quotes/{quoteId}
- "List all clientContacts?" -> GET /v2/quotes/{quoteId}/clientContacts
- "List all customFields?" -> GET /v2/quotes/{quoteId}/customFields
- "Get file details?" -> GET /v2/quotes/files/{fileId}
- "Get download details?" -> GET /v2/quotes/files/{fileId}/download/{fileName}
- "List all files?" -> GET /v2/quotes/{quoteId}/files
- "List all finance?" -> GET /v2/quotes/{quoteId}/finance
- "List all jobs?" -> GET /v2/quotes/{quoteId}/jobs
- "List all process?" -> GET /v2/quotes/{quoteId}/process
- "Update a customField?" -> PUT /v2/quotes/{quoteId}/customFields/{key}
- "Create a upload?" -> POST /v2/quotes/{quoteId}/files/upload
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
