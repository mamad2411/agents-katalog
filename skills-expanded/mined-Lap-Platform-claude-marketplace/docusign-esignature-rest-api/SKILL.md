---
name: docusign-esignature-rest-api
description: "Docusign eSignature REST API skill. Use when working with Docusign eSignature REST for service_information, v2.1. Covers 404 endpoints."
version: 1.0.0
generator: lapsh
---

# Docusign eSignature REST API
API version: v2.1

## Auth
ApiKey recipientId in path

## Base URL
https://www.docusign.net/restapi

## Setup
1. Set your API key in the appropriate header
2. GET /service_information -- verify access
3. POST /v2.1/accounts -- create first accounts

## Endpoints

404 endpoints across 2 groups. See references/api-spec.lap for full details.

### service_information
| Method | Path | Description |
|--------|------|-------------|
| GET | /service_information | Retrieves the available REST API versions. |

### v2.1
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2.1 | Lists resources for REST version specified |
| POST | /v2.1/accounts | Creates new accounts. |
| GET | /v2.1/accounts/{accountId} | Retrieves the account information for the specified account. |
| DELETE | /v2.1/accounts/{accountId} | Deletes the specified account. |
| GET | /v2.1/accounts/{accountId}/billing_charges | Gets list of recurring and usage charges for the account. |
| GET | /v2.1/accounts/{accountId}/billing_invoices | Get a List of Billing Invoices |
| GET | /v2.1/accounts/{accountId}/billing_invoices/{invoiceId} | Retrieves a billing invoice. |
| GET | /v2.1/accounts/{accountId}/billing_invoices_past_due | Get a list of past due invoices. |
| GET | /v2.1/accounts/{accountId}/billing_payments | Gets payment information for one or more payments. |
| POST | /v2.1/accounts/{accountId}/billing_payments | Posts a payment to a past due invoice. |
| GET | /v2.1/accounts/{accountId}/billing_payments/{paymentId} | Gets billing payment information for a specific payment. |
| GET | /v2.1/accounts/{accountId}/billing_plan | Get Account Billing Plan |
| PUT | /v2.1/accounts/{accountId}/billing_plan | Updates an account billing plan. |
| GET | /v2.1/accounts/{accountId}/billing_plan/credit_card | Get credit card information |
| GET | /v2.1/accounts/{accountId}/billing_plan/downgrade | Returns downgrade plan information for the specified account. |
| PUT | /v2.1/accounts/{accountId}/billing_plan/downgrade | Queues downgrade billing plan request for an account. |
| PUT | /v2.1/accounts/{accountId}/billing_plan/purchased_envelopes | Reserved: Purchase additional envelopes. |
| GET | /v2.1/accounts/{accountId}/brands | Gets a list of brands. |
| POST | /v2.1/accounts/{accountId}/brands | Creates one or more brand profiles for an account. |
| DELETE | /v2.1/accounts/{accountId}/brands | Deletes one or more brand profiles. |
| GET | /v2.1/accounts/{accountId}/brands/{brandId} | Gets information about a brand. |
| PUT | /v2.1/accounts/{accountId}/brands/{brandId} | Updates an existing brand. |
| DELETE | /v2.1/accounts/{accountId}/brands/{brandId} | Deletes a brand. |
| GET | /v2.1/accounts/{accountId}/brands/{brandId}/file | Exports a brand. |
| GET | /v2.1/accounts/{accountId}/brands/{brandId}/logos/{logoType} | Gets a brand logo. |
| PUT | /v2.1/accounts/{accountId}/brands/{brandId}/logos/{logoType} | Updates a brand logo. |
| DELETE | /v2.1/accounts/{accountId}/brands/{brandId}/logos/{logoType} | Deletes a brand logo. |
| GET | /v2.1/accounts/{accountId}/brands/{brandId}/resources | Returns metadata about the branding resources for an account. |
| GET | /v2.1/accounts/{accountId}/brands/{brandId}/resources/{resourceContentType} | Returns a branding resource file. |
| PUT | /v2.1/accounts/{accountId}/brands/{brandId}/resources/{resourceContentType} | Updates a branding resource file. |
| GET | /v2.1/accounts/{accountId}/bulk_send_batch | Returns a list of bulk send batch summaries. |
| GET | /v2.1/accounts/{accountId}/bulk_send_batch/{bulkSendBatchId} | Gets the status of a specific bulk send batch. |
| PUT | /v2.1/accounts/{accountId}/bulk_send_batch/{bulkSendBatchId} | Updates the name of a bulk send batch. |
| PUT | /v2.1/accounts/{accountId}/bulk_send_batch/{bulkSendBatchId}/{bulkAction} | Applies a bulk action to all envelopes from a specified bulk send. |
| GET | /v2.1/accounts/{accountId}/bulk_send_batch/{bulkSendBatchId}/envelopes | Gets envelopes from a specific bulk send batch. |
| GET | /v2.1/accounts/{accountId}/bulk_send_lists | Gets bulk send lists. |
| POST | /v2.1/accounts/{accountId}/bulk_send_lists | Creates a bulk send list. |
| GET | /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId} | Gets a specific bulk send list. |
| PUT | /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId} | Updates a bulk send list. |
| DELETE | /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId} | Deletes a bulk send list. |
| POST | /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId}/send | Creates a bulk send request. |
| POST | /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId}/test | Creates a bulk send test. |
| DELETE | /v2.1/accounts/{accountId}/captive_recipients/{recipientPart} | Deletes the signature for one or more captive recipient records. |
| POST | /v2.1/accounts/{accountId}/chunked_uploads | Initiate a new chunked upload. |
| GET | /v2.1/accounts/{accountId}/chunked_uploads/{chunkedUploadId} | Retrieves metadata about a chunked upload. |
| PUT | /v2.1/accounts/{accountId}/chunked_uploads/{chunkedUploadId} | Commit a chunked upload. |
| DELETE | /v2.1/accounts/{accountId}/chunked_uploads/{chunkedUploadId} | Deletes a chunked upload. |
| PUT | /v2.1/accounts/{accountId}/chunked_uploads/{chunkedUploadId}/{chunkedUploadPartSeq} | Add a chunk to an existing chunked upload. |
| GET | /v2.1/accounts/{accountId}/connect | Get Connect configuration information. |
| PUT | /v2.1/accounts/{accountId}/connect | Updates a specified Connect configuration. |
| POST | /v2.1/accounts/{accountId}/connect | Creates a Connect configuration. |
| GET | /v2.1/accounts/{accountId}/connect/{connectId} | Gets the details about a Connect configuration. |
| DELETE | /v2.1/accounts/{accountId}/connect/{connectId} | Deletes the specified Connect configuration. |
| GET | /v2.1/accounts/{accountId}/connect/{connectId}/all/users | Returns all users from the configured Connect service. |
| GET | /v2.1/accounts/{accountId}/connect/{connectId}/users | Returns users from the configured Connect service. |
| PUT | /v2.1/accounts/{accountId}/connect/envelopes/{envelopeId}/retry_queue | Republishes Connect information for the specified envelope. |
| POST | /v2.1/accounts/{accountId}/connect/envelopes/publish/historical | Submits a batch of historical envelopes for republish to a webhook. |
| PUT | /v2.1/accounts/{accountId}/connect/envelopes/retry_queue | Republishes Connect information for multiple envelopes. |
| GET | /v2.1/accounts/{accountId}/connect/failures | Gets the Connect failure log information. |
| DELETE | /v2.1/accounts/{accountId}/connect/failures/{failureId} | Deletes a Connect failure log entry. |
| GET | /v2.1/accounts/{accountId}/connect/logs | Gets the Connect log. |
| DELETE | /v2.1/accounts/{accountId}/connect/logs | Deletes a list of Connect log entries. |
| GET | /v2.1/accounts/{accountId}/connect/logs/{logId} | Gets a Connect log entry. |
| DELETE | /v2.1/accounts/{accountId}/connect/logs/{logId} | Deletes a specified Connect log entry. |
| GET | /v2.1/accounts/{accountId}/connect/oauth | Retrieves the Connect OAuth information for the account. |
| PUT | /v2.1/accounts/{accountId}/connect/oauth | Updates the existing Connect OAuth configuration for the account. |
| POST | /v2.1/accounts/{accountId}/connect/oauth | Set up Connect OAuth for the specified account. |
| DELETE | /v2.1/accounts/{accountId}/connect/oauth | Delete the Connect OAuth configuration. |
| GET | /v2.1/accounts/{accountId}/consumer_disclosure | Gets the default Electronic Record and Signature Disclosure for an account. |
| GET | /v2.1/accounts/{accountId}/consumer_disclosure/{langCode} | Gets the Electronic Record and Signature Disclosure for an account. |
| PUT | /v2.1/accounts/{accountId}/consumer_disclosure/{langCode} | Updates the Electronic Record and Signature Disclosure for an account. |
| PUT | /v2.1/accounts/{accountId}/contacts | Updates one or more contacts. |
| POST | /v2.1/accounts/{accountId}/contacts | Add contacts to a contacts list. |
| DELETE | /v2.1/accounts/{accountId}/contacts | Deletes multiple contacts from an account. |
| GET | /v2.1/accounts/{accountId}/contacts/{contactId} | Gets one or more contacts. |
| DELETE | /v2.1/accounts/{accountId}/contacts/{contactId} | Deletes a contact. |
| GET | /v2.1/accounts/{accountId}/custom_fields | Gets a list of custom fields. |
| POST | /v2.1/accounts/{accountId}/custom_fields | Creates an account custom field. |
| PUT | /v2.1/accounts/{accountId}/custom_fields/{customFieldId} | Updates an account custom field. |
| DELETE | /v2.1/accounts/{accountId}/custom_fields/{customFieldId} | Deletes an account custom field. |
| GET | /v2.1/accounts/{accountId}/envelopes | Search for specific sets of envelopes by using search filters. |
| POST | /v2.1/accounts/{accountId}/envelopes | Creates an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId} | Gets the status of a single envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId} | Send, void, or modify a draft envelope. Purge documents from a completed envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/attachments | Returns a list of envelope attachments associated with a specified envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/attachments | Adds one or more envelope attachments to a draft or in-process envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/attachments | Deletes one or more envelope attachments from a draft envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/attachments/{attachmentId} | Retrieves an envelope attachment from an envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/attachments/{attachmentId} | Updates an envelope attachment in a draft or in-process envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/audit_events | Gets the envelope audit events for an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/comments/transcript | Gets a PDF transcript of all of the comments in an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/custom_fields | Gets the custom field information for the specified envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/custom_fields | Updates envelope custom fields in an envelope. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/custom_fields | Creates envelope custom fields for an envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/custom_fields | Deletes envelope custom fields for draft and in-process envelopes. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/docGenFormFields | Returns sender fields for an envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/docGenFormFields | Updates sender fields for an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents | Gets a list of documents in an envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents | Adds one or more documents to an existing envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents | Deletes documents from a draft envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId} | Retrieves a single document or all documents from an envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId} | Adds or replaces a document in an existing envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/fields | Gets the custom document fields from an  existing envelope document. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/fields | Updates existing custom document fields in an existing envelope document. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/fields | Creates custom document fields in an existing envelope document. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/fields | Deletes custom document fields from an existing envelope document. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/html_definitions | Retrieves the HTML definition used to generate a dynamically sized responsive document. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/pages | Returns document page images based on input. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/pages/{pageNumber} | Deletes a page from a document in an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/pages/{pageNumber}/page_image | Gets a page image from an envelope for display. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/pages/{pageNumber}/page_image | Rotates page image from an envelope for display. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/pages/{pageNumber}/tabs | Returns tabs on the specified page. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/responsive_html_preview | Creates a preview of the responsive version of a document. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/tabs | Returns the tabs on a document. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/tabs | Updates the tabs for document. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/tabs | Adds tabs to a document in an envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/tabs | Deletes tabs from a document in an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/templates | Gets the templates associated with a document in an existing envelope. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/templates | Adds templates to a document in an  envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/templates/{templateId} | Deletes a template from a document in an existing envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/email_settings | Gets the email setting overrides for an envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/email_settings | Updates the email setting overrides for an envelope. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/email_settings | Adds email setting overrides to an envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/email_settings | Deletes the email setting overrides for an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/form_data | Returns envelope tab data for an existing envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/html_definitions | Gets the Original HTML Definition used to generate the Responsive HTML for the envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/lock | Gets envelope lock information. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/lock | Updates an envelope lock. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/lock | Locks an envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/lock | Deletes an envelope lock. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/notification | Gets envelope notification information. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/notification | Sets envelope notifications for an existing envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients | Gets the status of recipients for an envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients | Updates recipients in a draft envelope or corrects recipient information for an in-process envelope. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients | Adds one or more recipients to an envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients | Deletes recipients from an envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId} | Deletes a recipient from an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/consumer_disclosure | Gets the default Electronic Record and Signature Disclosure for an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/consumer_disclosure/{langCode} | Gets the Electronic Record and Signature Disclosure for a specific envelope recipient. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/document_visibility | Returns document visibility for a recipient |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/document_visibility | Updates document visibility for a recipient |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/identity_proof_token | Creates a resource token for a sender to request ID Evidence data. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/initials_image | Gets the initials image for a user. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/initials_image | Sets the initials image for an accountless signer. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/signature | Gets signature information for a signer or sign-in-person recipient. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/signature_image | Retrieve signature image information for a signer/sign-in-person recipient. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/signature_image | Sets the signature image for an accountless signer. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/tabs | Gets the tabs information for a signer or sign-in-person recipient in an envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/tabs | Updates the tabs for a recipient. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/tabs | Adds tabs for a recipient. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/tabs | Deletes the tabs associated with a recipient. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/views/identity_manual_review | Create the link to the page for manually reviewing IDs. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/document_visibility | Updates document visibility for recipients |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/responsive_html_preview | Creates a preview of the responsive versions of all of the documents in an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/tabs_blob | Reserved for Docusign. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/tabs_blob | Reserved for Docusign. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/templates | Gets templates used in an envelope. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/templates | Adds templates to an envelope. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/correct | Returns a URL to the envelope correction UI. Use after an envelope has been sent. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/correct | Revokes the correction view URL to the Envelope UI. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/edit | Returns a URL to the edit view UI. Use before an envelope has been sent. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/recipient | Returns a URL to the recipient view UI. For signer recipients, returns the embedded signing view. Can also be used for other recipient types. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/recipient_preview | Creates an envelope recipient preview. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/sender | Returns a URL to the sender view UI. Used before an envelope has been sent. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/shared | Returns a URL to the shared recipient view UI for an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow | Returns the workflow definition for an envelope. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow | Updates the workflow definition for an envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow | Delete the workflow definition for an envelope. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/scheduledSending | Returns the scheduled sending rules for an envelope's workflow definition. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/scheduledSending | Updates the scheduled sending rules for an envelope's workflow. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/scheduledSending | Deletes the scheduled sending rules for the envelope's workflow. |
| POST | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps | Adds a new step to an envelope's workflow. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId} | Returns a specified workflow step for a specified template. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId} | Updates the specified workflow step for an envelope. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId} | Deletes a workflow step from an envelope's workflow definition. |
| GET | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId}/delayedRouting | Returns the delayed routing rules for an envelope's workflow step definition. |
| PUT | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId}/delayedRouting | Updates the delayed routing rules for an envelope's workflow step definition. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId}/delayedRouting | Deletes the delayed routing rules for the specified envelope workflow step. |
| PUT | /v2.1/accounts/{accountId}/envelopes/status | Gets envelope statuses for a set of envelopes. |
| GET | /v2.1/accounts/{accountId}/envelopes/transfer_rules | Gets envelope transfer rules. |
| PUT | /v2.1/accounts/{accountId}/envelopes/transfer_rules | Changes the status of multiple envelope transfer rules. |
| POST | /v2.1/accounts/{accountId}/envelopes/transfer_rules | Creates an envelope transfer rule. |
| PUT | /v2.1/accounts/{accountId}/envelopes/transfer_rules/{envelopeTransferRuleId} | Changes the status of an envelope transfer rule. |
| DELETE | /v2.1/accounts/{accountId}/envelopes/transfer_rules/{envelopeTransferRuleId} | Deletes an envelope transfer rule. |
| GET | /v2.1/accounts/{accountId}/favorite_templates | Retrieves the list of favorite templates for the account. |
| PUT | /v2.1/accounts/{accountId}/favorite_templates | Set one or more templates as account favorites. |
| DELETE | /v2.1/accounts/{accountId}/favorite_templates | Remove one or more templates from the account favorites. |
| GET | /v2.1/accounts/{accountId}/folders | Returns a list of the account's folders. |
| GET | /v2.1/accounts/{accountId}/folders/{folderId} | Gets information about items in a specified folder. |
| PUT | /v2.1/accounts/{accountId}/folders/{folderId} | Moves a set of envelopes from their current folder to another folder. |
| GET | /v2.1/accounts/{accountId}/groups | Gets information about groups associated with the account. |
| PUT | /v2.1/accounts/{accountId}/groups | Updates the group information for a group. |
| POST | /v2.1/accounts/{accountId}/groups | Creates one or more groups for the account. |
| DELETE | /v2.1/accounts/{accountId}/groups | Deletes an existing user group. |
| GET | /v2.1/accounts/{accountId}/groups/{groupId}/brands | Gets the brand information for a group. |
| PUT | /v2.1/accounts/{accountId}/groups/{groupId}/brands | Adds an existing brand to a group. |
| DELETE | /v2.1/accounts/{accountId}/groups/{groupId}/brands | Deletes brand information from a group. |
| GET | /v2.1/accounts/{accountId}/groups/{groupId}/users | Gets a list of users in a group. |
| PUT | /v2.1/accounts/{accountId}/groups/{groupId}/users | Adds one or more users to an existing group. |
| DELETE | /v2.1/accounts/{accountId}/groups/{groupId}/users | Deletes one or more users from a group |
| GET | /v2.1/accounts/{accountId}/identity_verification | Retrieves the Identity Verification workflows available to an account. |
| GET | /v2.1/accounts/{accountId}/payment_gateway_accounts | List payment gateway accounts |
| GET | /v2.1/accounts/{accountId}/permission_profiles | Gets a list of permission profiles. |
| POST | /v2.1/accounts/{accountId}/permission_profiles | Creates a new permission profile for an account. |
| GET | /v2.1/accounts/{accountId}/permission_profiles/{permissionProfileId} | Returns a permission profile for an account. |
| PUT | /v2.1/accounts/{accountId}/permission_profiles/{permissionProfileId} | Updates a permission profile. |
| DELETE | /v2.1/accounts/{accountId}/permission_profiles/{permissionProfileId} | Deletes a permission profile from an account. |
| GET | /v2.1/accounts/{accountId}/powerforms | Returns a list of PowerForms. |
| POST | /v2.1/accounts/{accountId}/powerforms | Creates a new PowerForm |
| DELETE | /v2.1/accounts/{accountId}/powerforms | Deletes one or more PowerForms. |
| GET | /v2.1/accounts/{accountId}/powerforms/{powerFormId} | Returns a single PowerForm. |
| PUT | /v2.1/accounts/{accountId}/powerforms/{powerFormId} | Updates an existing PowerForm. |
| DELETE | /v2.1/accounts/{accountId}/powerforms/{powerFormId} | Deletes a PowerForm. |
| GET | /v2.1/accounts/{accountId}/powerforms/{powerFormId}/form_data | Returns the data that users entered in a PowerForm. |
| GET | /v2.1/accounts/{accountId}/powerforms/senders | Gets PowerForm senders. |
| GET | /v2.1/accounts/{accountId}/recipient_names | Gets the recipient names associated with an email address. |
| GET | /v2.1/accounts/{accountId}/seals | Returns available seals for specified account. |
| GET | /v2.1/accounts/{accountId}/search_folders/{searchFolderId} | Deprecated. Use Envelopes: listStatusChanges. |
| GET | /v2.1/accounts/{accountId}/settings | Gets account settings information. |
| PUT | /v2.1/accounts/{accountId}/settings | Updates the account settings for an account. |
| GET | /v2.1/accounts/{accountId}/settings/bcc_email_archives | Gets the BCC email archive configurations for an account. |
| POST | /v2.1/accounts/{accountId}/settings/bcc_email_archives | Creates a BCC email archive configuration. |
| GET | /v2.1/accounts/{accountId}/settings/bcc_email_archives/{bccEmailArchiveId} | Gets a BCC email archive configuration and its history. |
| DELETE | /v2.1/accounts/{accountId}/settings/bcc_email_archives/{bccEmailArchiveId} | Deletes a BCC email archive configuration. |
| GET | /v2.1/accounts/{accountId}/settings/enote_configuration | Returns the configuration information for the eNote eOriginal integration. |
| PUT | /v2.1/accounts/{accountId}/settings/enote_configuration | Updates configuration information for the eNote eOriginal integration. |
| DELETE | /v2.1/accounts/{accountId}/settings/enote_configuration | Deletes configuration information for the eNote eOriginal integration. |
| GET | /v2.1/accounts/{accountId}/settings/envelope_purge_configuration | Gets the envelope purge configuration for an account. |
| PUT | /v2.1/accounts/{accountId}/settings/envelope_purge_configuration | Sets the envelope purge configuration for an account. |
| GET | /v2.1/accounts/{accountId}/settings/notification_defaults | Gets envelope notification defaults. |
| PUT | /v2.1/accounts/{accountId}/settings/notification_defaults | Updates envelope notification default settings. |
| GET | /v2.1/accounts/{accountId}/settings/password_rules | Gets the password rules for an account. |
| PUT | /v2.1/accounts/{accountId}/settings/password_rules | Updates the password rules for an account. |
| GET | /v2.1/accounts/{accountId}/settings/tabs | Returns tab settings list for specified account |
| PUT | /v2.1/accounts/{accountId}/settings/tabs | Modifies tab settings for specified account |
| GET | /v2.1/accounts/{accountId}/shared_access | Reserved: Gets the shared item status for one or more users. |
| PUT | /v2.1/accounts/{accountId}/shared_access | Reserved: Sets the shared access information for users. |
| GET | /v2.1/accounts/{accountId}/signatureProviders | Gets the available signature providers for an account. |
| GET | /v2.1/accounts/{accountId}/signatures | Returns a list of stamps available in the account. |
| PUT | /v2.1/accounts/{accountId}/signatures | Updates an account stamp. |
| POST | /v2.1/accounts/{accountId}/signatures | Adds or updates one or more account stamps. |
| GET | /v2.1/accounts/{accountId}/signatures/{signatureId} | Returns information about the specified stamp. |
| PUT | /v2.1/accounts/{accountId}/signatures/{signatureId} | Updates an account stamp by ID. |
| DELETE | /v2.1/accounts/{accountId}/signatures/{signatureId} | Deletes an account stamp. |
| GET | /v2.1/accounts/{accountId}/signatures/{signatureId}/{imageType} | Returns the image for an account stamp. |
| PUT | /v2.1/accounts/{accountId}/signatures/{signatureId}/{imageType} | Sets a signature image, initials, or stamp. |
| DELETE | /v2.1/accounts/{accountId}/signatures/{signatureId}/{imageType} | Deletes the image for a stamp. |
| GET | /v2.1/accounts/{accountId}/signing_groups | Gets a list of the Signing Groups in an account. |
| PUT | /v2.1/accounts/{accountId}/signing_groups | Updates signing group names. |
| POST | /v2.1/accounts/{accountId}/signing_groups | Creates a signing group. |
| DELETE | /v2.1/accounts/{accountId}/signing_groups | Deletes one or more signing groups. |
| GET | /v2.1/accounts/{accountId}/signing_groups/{signingGroupId} | Gets information about a signing group. |
| PUT | /v2.1/accounts/{accountId}/signing_groups/{signingGroupId} | Updates a signing group. |
| GET | /v2.1/accounts/{accountId}/signing_groups/{signingGroupId}/users | Gets a list of members in a Signing Group. |
| PUT | /v2.1/accounts/{accountId}/signing_groups/{signingGroupId}/users | Adds members to a signing group. |
| DELETE | /v2.1/accounts/{accountId}/signing_groups/{signingGroupId}/users | Deletes  one or more members from a signing group. |
| GET | /v2.1/accounts/{accountId}/supported_languages | Gets the supported languages for envelope recipients. |
| GET | /v2.1/accounts/{accountId}/tab_definitions | Gets a list of all account tabs. |
| POST | /v2.1/accounts/{accountId}/tab_definitions | Creates a custom tab. |
| GET | /v2.1/accounts/{accountId}/tab_definitions/{customTabId} | Gets custom tab information. |
| PUT | /v2.1/accounts/{accountId}/tab_definitions/{customTabId} | Updates custom tab information. |
| DELETE | /v2.1/accounts/{accountId}/tab_definitions/{customTabId} | Deletes custom tab information. |
| GET | /v2.1/accounts/{accountId}/templates | Gets the list of templates. |
| PUT | /v2.1/accounts/{accountId}/templates |  |
| POST | /v2.1/accounts/{accountId}/templates | Creates one or more templates. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId} | Gets a specific template associated with a specified account. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId} | Updates an existing template. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/{templatePart} | Shares a template with a group. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/{templatePart} | Removes a member group's sharing permissions for a template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/custom_fields | Gets the custom document fields from a template. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/custom_fields | Updates envelope custom fields in a template. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/custom_fields | Creates custom document fields in an existing template document. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/custom_fields | Deletes envelope custom fields in a template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/documents | Gets a list of documents associated with a template. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/documents | Adds documents to a template document. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/documents | Deletes documents from a template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId} | Gets PDF documents from a template. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId} | Updates a template document. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/fields | Gets the custom document fields for a an existing template document. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/fields | Updates existing custom document fields in an existing template document. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/fields | Creates custom document fields in an existing template document. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/fields | Deletes custom document fields from an existing template document. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/html_definitions | Gets the Original HTML Definition used to generate the Responsive HTML for a given document in a template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/pages | Returns document page images based on input. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/pages/{pageNumber} | Deletes a page from a document in an template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/pages/{pageNumber}/page_image | Gets a page image from a template for display. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/pages/{pageNumber}/page_image | Rotates page image from a template for display. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/pages/{pageNumber}/tabs | Returns tabs on the specified page. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/responsive_html_preview | Creates a preview of the responsive version of a template document. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/tabs | Returns tabs on a template. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/tabs | Updates the tabs for a template. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/tabs | Adds tabs to a document in a template. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/tabs | Deletes tabs from a template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/html_definitions | Gets the Original HTML Definition used to generate the Responsive HTML for the template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/lock | Gets template lock information. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/lock | Updates a template lock. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/lock | Locks a template. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/lock | Deletes a template lock. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/notification | Gets template notification information. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/notification | Updates the notification  structure for an existing template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/recipients | Gets recipient information from a template. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/recipients | Updates recipients in a template. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/recipients | Adds tabs for a recipient. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/recipients | Deletes recipients from a template. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId} | Deletes the specified recipient file from a template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}/document_visibility | Returns document visibility for a template recipient |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}/document_visibility | Updates document visibility for a template recipient |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}/tabs | Gets the tabs information for a signer or sign-in-person recipient in a template. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}/tabs | Updates the tabs for a recipient. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}/tabs | Adds tabs for a recipient. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}/tabs | Deletes the tabs associated with a recipient in a template. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/recipients/document_visibility | Updates document visibility for template recipients |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/responsive_html_preview | Creates a preview of the responsive versions of all of the documents associated with a template. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/views/edit | Gets a URL for a template edit view. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/views/recipient_preview | Creates a template recipient preview. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/workflow | Returns the workflow definition for a template. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/workflow | Updates the workflow definition for a template. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/workflow | Delete the workflow definition for a template. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/scheduledSending | Returns the scheduled sending rules for a template's workflow definition. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/scheduledSending | Updates the scheduled sending rules for a template's workflow definition. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/scheduledSending | Deletes the scheduled sending rules for the template's workflow. |
| POST | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps | Adds a new step to a template's workflow. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId} | Returns a specified workflow step for a specified envelope. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId} | Updates a specified workflow step for a template. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId} | Deletes a workflow step from an template's workflow definition. |
| GET | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId}/delayedRouting | Returns the delayed routing rules for a template's workflow step definition. |
| PUT | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId}/delayedRouting | Updates the delayed routing rules for a template's workflow step. |
| DELETE | /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId}/delayedRouting | Deletes the delayed routing rules for the specified template workflow step. |
| PUT | /v2.1/accounts/{accountId}/templates/auto_match |  |
| GET | /v2.1/accounts/{accountId}/unsupported_file_types | Gets a list of unsupported file types. |
| GET | /v2.1/accounts/{accountId}/users | Retrieves the list of users for the specified account. You can filter the users list to get specific users. |
| PUT | /v2.1/accounts/{accountId}/users | Changes one or more users in the specified account. |
| POST | /v2.1/accounts/{accountId}/users | Adds new users to the specified account. |
| DELETE | /v2.1/accounts/{accountId}/users | Closes one or more users in the account. |
| GET | /v2.1/accounts/{accountId}/users/{userId} | Gets the user information for a specified user using a userId (GUID). To find a user based on their email address, use the list endpoint. |
| PUT | /v2.1/accounts/{accountId}/users/{userId} | Updates user information for the specified user. |
| POST | /v2.1/accounts/{accountId}/users/{userId}/authorization | Creates a user authorization. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/authorization/{authorizationId} | Returns the user authorization for a given authorization ID. |
| PUT | /v2.1/accounts/{accountId}/users/{userId}/authorization/{authorizationId} | Updates the start or end date for a user authorization. |
| DELETE | /v2.1/accounts/{accountId}/users/{userId}/authorization/{authorizationId} | Deletes the user authorization. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/authorizations | Returns the authorizations for which the specified user is the principal user. |
| POST | /v2.1/accounts/{accountId}/users/{userId}/authorizations | Create or update multiple user authorizations. |
| DELETE | /v2.1/accounts/{accountId}/users/{userId}/authorizations | Delete multiple user authorizations. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/authorizations/agent | Returns the authorizations for which the specified user is the agent user. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/cloud_storage | Get the Cloud Storage Provider configuration for the specified user. |
| POST | /v2.1/accounts/{accountId}/users/{userId}/cloud_storage | Configures the redirect URL information  for one or more cloud storage providers for the specified user. |
| DELETE | /v2.1/accounts/{accountId}/users/{userId}/cloud_storage | Deletes the user authentication information for one or more cloud storage providers. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/cloud_storage/{serviceId} | Gets the specified Cloud Storage Provider configuration for the User. |
| DELETE | /v2.1/accounts/{accountId}/users/{userId}/cloud_storage/{serviceId} | Deletes the user authentication information for the specified cloud storage provider. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/cloud_storage/{serviceId}/folders | Retrieves a list of all the items in a specified folder from the specified cloud storage provider. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/cloud_storage/{serviceId}/folders/{folderId} | Gets a list of items from a cloud storage provider. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/custom_settings | Retrieves the custom user settings for a specified user. |
| PUT | /v2.1/accounts/{accountId}/users/{userId}/custom_settings | Adds or updates custom user settings for the specified user. |
| DELETE | /v2.1/accounts/{accountId}/users/{userId}/custom_settings | Deletes custom user settings for a specified user. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/profile | Retrieves the user profile for a specified user. |
| PUT | /v2.1/accounts/{accountId}/users/{userId}/profile | Updates the user profile information for the specified user. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/profile/image | Retrieves the user profile image for the specified user. |
| PUT | /v2.1/accounts/{accountId}/users/{userId}/profile/image | Updates the user profile image for a specified user. |
| DELETE | /v2.1/accounts/{accountId}/users/{userId}/profile/image | Deletes the user profile image for the specified user. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/settings | Gets the user account settings for a specified user. |
| PUT | /v2.1/accounts/{accountId}/users/{userId}/settings | Updates the user account settings for a specified user. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/signatures | Retrieves a list of signature definitions for a user. |
| PUT | /v2.1/accounts/{accountId}/users/{userId}/signatures | Adds/updates a user signature. |
| POST | /v2.1/accounts/{accountId}/users/{userId}/signatures | Adds user Signature and initials images to a Signature. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId} | Gets the user signature information for the specified user. |
| PUT | /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId} | Updates the user signature for a specified user. |
| DELETE | /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId} | Removes removes signature information for the specified user. |
| GET | /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId}/{imageType} | Retrieves the user initials image or the  user signature image for the specified user. |
| PUT | /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId}/{imageType} | Updates the user signature image or user initials image for the specified user. |
| DELETE | /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId}/{imageType} | Deletes the user initials image or the  user signature image for the specified user. |
| POST | /v2.1/accounts/{accountId}/views/console | Returns a URL to the Docusign eSignature web application. |
| GET | /v2.1/accounts/{accountId}/watermark | Get watermark information. |
| PUT | /v2.1/accounts/{accountId}/watermark | Update watermark information. |
| PUT | /v2.1/accounts/{accountId}/watermark/preview | Get watermark preview. |
| GET | /v2.1/accounts/{accountId}/workspaces | List Workspaces |
| POST | /v2.1/accounts/{accountId}/workspaces | Create a Workspace |
| GET | /v2.1/accounts/{accountId}/workspaces/{workspaceId} | Get Workspace |
| PUT | /v2.1/accounts/{accountId}/workspaces/{workspaceId} | Update Workspace |
| DELETE | /v2.1/accounts/{accountId}/workspaces/{workspaceId} | Delete Workspace |
| GET | /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId} | List workspace folder contents |
| DELETE | /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId} | Deletes files or sub-folders from a workspace. |
| POST | /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}/files | Creates a workspace file. |
| GET | /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}/files/{fileId} | Gets a workspace file |
| PUT | /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}/files/{fileId} | Update workspace file or folder metadata |
| GET | /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}/files/{fileId}/pages | List File Pages |
| GET | /v2.1/accounts/provisioning | Retrieves the account provisioning information for the account. |
| GET | /v2.1/billing_plans | Gets a list of available billing plans. |
| GET | /v2.1/billing_plans/{billingPlanId} | Gets billing plan details. |
| GET | /v2.1/current_user/notary | Gets settings for a  notary user. |
| PUT | /v2.1/current_user/notary | Updates notary information for the current user. |
| POST | /v2.1/current_user/notary | Registers the current user as a notary. |
| GET | /v2.1/current_user/notary/journals | Gets notary jurisdictions for a user. |
| GET | /v2.1/current_user/notary/jurisdictions | Returns a list of jurisdictions that the notary is registered in. |
| POST | /v2.1/current_user/notary/jurisdictions | Creates a jurisdiction object. |
| GET | /v2.1/current_user/notary/jurisdictions/{jurisdictionId} | Gets a jurisdiction object for the current user. The user must be a notary. |
| PUT | /v2.1/current_user/notary/jurisdictions/{jurisdictionId} | Updates the jurisdiction information about a notary. |
| DELETE | /v2.1/current_user/notary/jurisdictions/{jurisdictionId} | Deletes the specified jurisdiction. |
| GET | /v2.1/current_user/password_rules | Gets membership account password rules. |
| GET | /v2.1/diagnostics/request_logs | Gets the API request logging log files. |
| DELETE | /v2.1/diagnostics/request_logs | Deletes the request log files. |
| GET | /v2.1/diagnostics/request_logs/{requestLogId} | Gets a request logging log file. |
| GET | /v2.1/diagnostics/settings | Gets the API request logging settings. |
| PUT | /v2.1/diagnostics/settings | Enables or disables API request logging for troubleshooting. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all service_information?" -> GET /service_information
- "List all v2.1?" -> GET /v2.1
- "Create a account?" -> POST /v2.1/accounts
- "Get account details?" -> GET /v2.1/accounts/{accountId}
- "Delete a account?" -> DELETE /v2.1/accounts/{accountId}
- "List all billing_charges?" -> GET /v2.1/accounts/{accountId}/billing_charges
- "List all billing_invoices?" -> GET /v2.1/accounts/{accountId}/billing_invoices
- "Get billing_invoice details?" -> GET /v2.1/accounts/{accountId}/billing_invoices/{invoiceId}
- "List all billing_invoices_past_due?" -> GET /v2.1/accounts/{accountId}/billing_invoices_past_due
- "List all billing_payments?" -> GET /v2.1/accounts/{accountId}/billing_payments
- "Create a billing_payment?" -> POST /v2.1/accounts/{accountId}/billing_payments
- "Get billing_payment details?" -> GET /v2.1/accounts/{accountId}/billing_payments/{paymentId}
- "List all billing_plan?" -> GET /v2.1/accounts/{accountId}/billing_plan
- "List all credit_card?" -> GET /v2.1/accounts/{accountId}/billing_plan/credit_card
- "List all downgrade?" -> GET /v2.1/accounts/{accountId}/billing_plan/downgrade
- "List all brands?" -> GET /v2.1/accounts/{accountId}/brands
- "Create a brand?" -> POST /v2.1/accounts/{accountId}/brands
- "Get brand details?" -> GET /v2.1/accounts/{accountId}/brands/{brandId}
- "Update a brand?" -> PUT /v2.1/accounts/{accountId}/brands/{brandId}
- "Delete a brand?" -> DELETE /v2.1/accounts/{accountId}/brands/{brandId}
- "List all file?" -> GET /v2.1/accounts/{accountId}/brands/{brandId}/file
- "Get logo details?" -> GET /v2.1/accounts/{accountId}/brands/{brandId}/logos/{logoType}
- "Update a logo?" -> PUT /v2.1/accounts/{accountId}/brands/{brandId}/logos/{logoType}
- "Delete a logo?" -> DELETE /v2.1/accounts/{accountId}/brands/{brandId}/logos/{logoType}
- "List all resources?" -> GET /v2.1/accounts/{accountId}/brands/{brandId}/resources
- "Get resource details?" -> GET /v2.1/accounts/{accountId}/brands/{brandId}/resources/{resourceContentType}
- "Update a resource?" -> PUT /v2.1/accounts/{accountId}/brands/{brandId}/resources/{resourceContentType}
- "List all bulk_send_batch?" -> GET /v2.1/accounts/{accountId}/bulk_send_batch
- "Get bulk_send_batch details?" -> GET /v2.1/accounts/{accountId}/bulk_send_batch/{bulkSendBatchId}
- "Update a bulk_send_batch?" -> PUT /v2.1/accounts/{accountId}/bulk_send_batch/{bulkSendBatchId}
- "Update a bulk_send_batch?" -> PUT /v2.1/accounts/{accountId}/bulk_send_batch/{bulkSendBatchId}/{bulkAction}
- "List all envelopes?" -> GET /v2.1/accounts/{accountId}/bulk_send_batch/{bulkSendBatchId}/envelopes
- "List all bulk_send_lists?" -> GET /v2.1/accounts/{accountId}/bulk_send_lists
- "Create a bulk_send_list?" -> POST /v2.1/accounts/{accountId}/bulk_send_lists
- "Get bulk_send_list details?" -> GET /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId}
- "Update a bulk_send_list?" -> PUT /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId}
- "Delete a bulk_send_list?" -> DELETE /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId}
- "Create a send?" -> POST /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId}/send
- "Create a test?" -> POST /v2.1/accounts/{accountId}/bulk_send_lists/{bulkSendListId}/test
- "Delete a captive_recipient?" -> DELETE /v2.1/accounts/{accountId}/captive_recipients/{recipientPart}
- "Create a chunked_upload?" -> POST /v2.1/accounts/{accountId}/chunked_uploads
- "Get chunked_upload details?" -> GET /v2.1/accounts/{accountId}/chunked_uploads/{chunkedUploadId}
- "Update a chunked_upload?" -> PUT /v2.1/accounts/{accountId}/chunked_uploads/{chunkedUploadId}
- "Delete a chunked_upload?" -> DELETE /v2.1/accounts/{accountId}/chunked_uploads/{chunkedUploadId}
- "Update a chunked_upload?" -> PUT /v2.1/accounts/{accountId}/chunked_uploads/{chunkedUploadId}/{chunkedUploadPartSeq}
- "List all connect?" -> GET /v2.1/accounts/{accountId}/connect
- "Create a connect?" -> POST /v2.1/accounts/{accountId}/connect
- "Get connect details?" -> GET /v2.1/accounts/{accountId}/connect/{connectId}
- "Delete a connect?" -> DELETE /v2.1/accounts/{accountId}/connect/{connectId}
- "List all users?" -> GET /v2.1/accounts/{accountId}/connect/{connectId}/all/users
- "List all users?" -> GET /v2.1/accounts/{accountId}/connect/{connectId}/users
- "Create a historical?" -> POST /v2.1/accounts/{accountId}/connect/envelopes/publish/historical
- "List all failures?" -> GET /v2.1/accounts/{accountId}/connect/failures
- "Delete a failure?" -> DELETE /v2.1/accounts/{accountId}/connect/failures/{failureId}
- "List all logs?" -> GET /v2.1/accounts/{accountId}/connect/logs
- "Get log details?" -> GET /v2.1/accounts/{accountId}/connect/logs/{logId}
- "Delete a log?" -> DELETE /v2.1/accounts/{accountId}/connect/logs/{logId}
- "List all oauth?" -> GET /v2.1/accounts/{accountId}/connect/oauth
- "Create a oauth?" -> POST /v2.1/accounts/{accountId}/connect/oauth
- "List all consumer_disclosure?" -> GET /v2.1/accounts/{accountId}/consumer_disclosure
- "Get consumer_disclosure details?" -> GET /v2.1/accounts/{accountId}/consumer_disclosure/{langCode}
- "Update a consumer_disclosure?" -> PUT /v2.1/accounts/{accountId}/consumer_disclosure/{langCode}
- "Create a contact?" -> POST /v2.1/accounts/{accountId}/contacts
- "Get contact details?" -> GET /v2.1/accounts/{accountId}/contacts/{contactId}
- "Delete a contact?" -> DELETE /v2.1/accounts/{accountId}/contacts/{contactId}
- "List all custom_fields?" -> GET /v2.1/accounts/{accountId}/custom_fields
- "Create a custom_field?" -> POST /v2.1/accounts/{accountId}/custom_fields
- "Update a custom_field?" -> PUT /v2.1/accounts/{accountId}/custom_fields/{customFieldId}
- "Delete a custom_field?" -> DELETE /v2.1/accounts/{accountId}/custom_fields/{customFieldId}
- "List all envelopes?" -> GET /v2.1/accounts/{accountId}/envelopes
- "Create a envelope?" -> POST /v2.1/accounts/{accountId}/envelopes
- "Get envelope details?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}
- "Update a envelope?" -> PUT /v2.1/accounts/{accountId}/envelopes/{envelopeId}
- "List all attachments?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/attachments
- "Get attachment details?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/attachments/{attachmentId}
- "Update a attachment?" -> PUT /v2.1/accounts/{accountId}/envelopes/{envelopeId}/attachments/{attachmentId}
- "List all audit_events?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/audit_events
- "List all transcript?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/comments/transcript
- "List all custom_fields?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/custom_fields
- "Create a custom_field?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/custom_fields
- "List all docGenFormFields?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/docGenFormFields
- "List all documents?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents
- "Get document details?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}
- "Update a document?" -> PUT /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}
- "List all fields?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/fields
- "Create a field?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/fields
- "List all html_definitions?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/html_definitions
- "List all pages?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/pages
- "Delete a page?" -> DELETE /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/pages/{pageNumber}
- "List all page_image?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/pages/{pageNumber}/page_image
- "List all tabs?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/pages/{pageNumber}/tabs
- "Create a responsive_html_preview?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/responsive_html_preview
- "List all tabs?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/tabs
- "Create a tab?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/tabs
- "List all templates?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/templates
- "Create a template?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/templates
- "Delete a template?" -> DELETE /v2.1/accounts/{accountId}/envelopes/{envelopeId}/documents/{documentId}/templates/{templateId}
- "List all email_settings?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/email_settings
- "Create a email_setting?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/email_settings
- "List all form_data?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/form_data
- "List all html_definitions?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/html_definitions
- "List all lock?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/lock
- "Create a lock?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/lock
- "List all notification?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/notification
- "List all recipients?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients
- "Create a recipient?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients
- "Delete a recipient?" -> DELETE /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}
- "List all consumer_disclosure?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/consumer_disclosure
- "Get consumer_disclosure details?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/consumer_disclosure/{langCode}
- "List all document_visibility?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/document_visibility
- "Create a identity_proof_token?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/identity_proof_token
- "List all initials_image?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/initials_image
- "List all signature?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/signature
- "List all signature_image?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/signature_image
- "List all tabs?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/tabs
- "Create a tab?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/tabs
- "Create a identity_manual_review?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/recipients/{recipientId}/views/identity_manual_review
- "Create a responsive_html_preview?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/responsive_html_preview
- "List all tabs_blob?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/tabs_blob
- "List all templates?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/templates
- "Create a template?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/templates
- "Create a correct?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/correct
- "Create a edit?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/edit
- "Create a recipient?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/recipient
- "Create a recipient_preview?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/recipient_preview
- "Create a sender?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/sender
- "Create a shared?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/views/shared
- "List all workflow?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow
- "List all scheduledSending?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/scheduledSending
- "Create a step?" -> POST /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps
- "Get step details?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId}
- "Update a step?" -> PUT /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId}
- "Delete a step?" -> DELETE /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId}
- "List all delayedRouting?" -> GET /v2.1/accounts/{accountId}/envelopes/{envelopeId}/workflow/steps/{workflowStepId}/delayedRouting
- "List all transfer_rules?" -> GET /v2.1/accounts/{accountId}/envelopes/transfer_rules
- "Create a transfer_rule?" -> POST /v2.1/accounts/{accountId}/envelopes/transfer_rules
- "Update a transfer_rule?" -> PUT /v2.1/accounts/{accountId}/envelopes/transfer_rules/{envelopeTransferRuleId}
- "Delete a transfer_rule?" -> DELETE /v2.1/accounts/{accountId}/envelopes/transfer_rules/{envelopeTransferRuleId}
- "List all favorite_templates?" -> GET /v2.1/accounts/{accountId}/favorite_templates
- "List all folders?" -> GET /v2.1/accounts/{accountId}/folders
- "Get folder details?" -> GET /v2.1/accounts/{accountId}/folders/{folderId}
- "Update a folder?" -> PUT /v2.1/accounts/{accountId}/folders/{folderId}
- "List all groups?" -> GET /v2.1/accounts/{accountId}/groups
- "Create a group?" -> POST /v2.1/accounts/{accountId}/groups
- "List all brands?" -> GET /v2.1/accounts/{accountId}/groups/{groupId}/brands
- "List all users?" -> GET /v2.1/accounts/{accountId}/groups/{groupId}/users
- "List all identity_verification?" -> GET /v2.1/accounts/{accountId}/identity_verification
- "List all payment_gateway_accounts?" -> GET /v2.1/accounts/{accountId}/payment_gateway_accounts
- "List all permission_profiles?" -> GET /v2.1/accounts/{accountId}/permission_profiles
- "Create a permission_profile?" -> POST /v2.1/accounts/{accountId}/permission_profiles
- "Get permission_profile details?" -> GET /v2.1/accounts/{accountId}/permission_profiles/{permissionProfileId}
- "Update a permission_profile?" -> PUT /v2.1/accounts/{accountId}/permission_profiles/{permissionProfileId}
- "Delete a permission_profile?" -> DELETE /v2.1/accounts/{accountId}/permission_profiles/{permissionProfileId}
- "List all powerforms?" -> GET /v2.1/accounts/{accountId}/powerforms
- "Create a powerform?" -> POST /v2.1/accounts/{accountId}/powerforms
- "Get powerform details?" -> GET /v2.1/accounts/{accountId}/powerforms/{powerFormId}
- "Update a powerform?" -> PUT /v2.1/accounts/{accountId}/powerforms/{powerFormId}
- "Delete a powerform?" -> DELETE /v2.1/accounts/{accountId}/powerforms/{powerFormId}
- "List all form_data?" -> GET /v2.1/accounts/{accountId}/powerforms/{powerFormId}/form_data
- "List all senders?" -> GET /v2.1/accounts/{accountId}/powerforms/senders
- "List all recipient_names?" -> GET /v2.1/accounts/{accountId}/recipient_names
- "List all seals?" -> GET /v2.1/accounts/{accountId}/seals
- "Get search_folder details?" -> GET /v2.1/accounts/{accountId}/search_folders/{searchFolderId}
- "List all settings?" -> GET /v2.1/accounts/{accountId}/settings
- "List all bcc_email_archives?" -> GET /v2.1/accounts/{accountId}/settings/bcc_email_archives
- "Create a bcc_email_archive?" -> POST /v2.1/accounts/{accountId}/settings/bcc_email_archives
- "Get bcc_email_archive details?" -> GET /v2.1/accounts/{accountId}/settings/bcc_email_archives/{bccEmailArchiveId}
- "Delete a bcc_email_archive?" -> DELETE /v2.1/accounts/{accountId}/settings/bcc_email_archives/{bccEmailArchiveId}
- "List all enote_configuration?" -> GET /v2.1/accounts/{accountId}/settings/enote_configuration
- "List all envelope_purge_configuration?" -> GET /v2.1/accounts/{accountId}/settings/envelope_purge_configuration
- "List all notification_defaults?" -> GET /v2.1/accounts/{accountId}/settings/notification_defaults
- "List all password_rules?" -> GET /v2.1/accounts/{accountId}/settings/password_rules
- "List all tabs?" -> GET /v2.1/accounts/{accountId}/settings/tabs
- "List all shared_access?" -> GET /v2.1/accounts/{accountId}/shared_access
- "List all signatureProviders?" -> GET /v2.1/accounts/{accountId}/signatureProviders
- "List all signatures?" -> GET /v2.1/accounts/{accountId}/signatures
- "Create a signature?" -> POST /v2.1/accounts/{accountId}/signatures
- "Get signature details?" -> GET /v2.1/accounts/{accountId}/signatures/{signatureId}
- "Update a signature?" -> PUT /v2.1/accounts/{accountId}/signatures/{signatureId}
- "Delete a signature?" -> DELETE /v2.1/accounts/{accountId}/signatures/{signatureId}
- "Get signature details?" -> GET /v2.1/accounts/{accountId}/signatures/{signatureId}/{imageType}
- "Update a signature?" -> PUT /v2.1/accounts/{accountId}/signatures/{signatureId}/{imageType}
- "Delete a signature?" -> DELETE /v2.1/accounts/{accountId}/signatures/{signatureId}/{imageType}
- "List all signing_groups?" -> GET /v2.1/accounts/{accountId}/signing_groups
- "Create a signing_group?" -> POST /v2.1/accounts/{accountId}/signing_groups
- "Get signing_group details?" -> GET /v2.1/accounts/{accountId}/signing_groups/{signingGroupId}
- "Update a signing_group?" -> PUT /v2.1/accounts/{accountId}/signing_groups/{signingGroupId}
- "List all users?" -> GET /v2.1/accounts/{accountId}/signing_groups/{signingGroupId}/users
- "List all supported_languages?" -> GET /v2.1/accounts/{accountId}/supported_languages
- "List all tab_definitions?" -> GET /v2.1/accounts/{accountId}/tab_definitions
- "Create a tab_definition?" -> POST /v2.1/accounts/{accountId}/tab_definitions
- "Get tab_definition details?" -> GET /v2.1/accounts/{accountId}/tab_definitions/{customTabId}
- "Update a tab_definition?" -> PUT /v2.1/accounts/{accountId}/tab_definitions/{customTabId}
- "Delete a tab_definition?" -> DELETE /v2.1/accounts/{accountId}/tab_definitions/{customTabId}
- "List all templates?" -> GET /v2.1/accounts/{accountId}/templates
- "Create a template?" -> POST /v2.1/accounts/{accountId}/templates
- "Get template details?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}
- "Update a template?" -> PUT /v2.1/accounts/{accountId}/templates/{templateId}
- "Update a template?" -> PUT /v2.1/accounts/{accountId}/templates/{templateId}/{templatePart}
- "Delete a template?" -> DELETE /v2.1/accounts/{accountId}/templates/{templateId}/{templatePart}
- "List all custom_fields?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/custom_fields
- "Create a custom_field?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/custom_fields
- "List all documents?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/documents
- "Get document details?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}
- "Update a document?" -> PUT /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}
- "List all fields?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/fields
- "Create a field?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/fields
- "List all html_definitions?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/html_definitions
- "List all pages?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/pages
- "Delete a page?" -> DELETE /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/pages/{pageNumber}
- "List all page_image?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/pages/{pageNumber}/page_image
- "List all tabs?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/pages/{pageNumber}/tabs
- "Create a responsive_html_preview?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/responsive_html_preview
- "List all tabs?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/tabs
- "Create a tab?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/documents/{documentId}/tabs
- "List all html_definitions?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/html_definitions
- "List all lock?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/lock
- "Create a lock?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/lock
- "List all notification?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/notification
- "List all recipients?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/recipients
- "Create a recipient?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/recipients
- "Delete a recipient?" -> DELETE /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}
- "List all document_visibility?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}/document_visibility
- "List all tabs?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}/tabs
- "Create a tab?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/recipients/{recipientId}/tabs
- "Create a responsive_html_preview?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/responsive_html_preview
- "Create a edit?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/views/edit
- "Create a recipient_preview?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/views/recipient_preview
- "List all workflow?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/workflow
- "List all scheduledSending?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/workflow/scheduledSending
- "Create a step?" -> POST /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps
- "Get step details?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId}
- "Update a step?" -> PUT /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId}
- "Delete a step?" -> DELETE /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId}
- "List all delayedRouting?" -> GET /v2.1/accounts/{accountId}/templates/{templateId}/workflow/steps/{workflowStepId}/delayedRouting
- "List all unsupported_file_types?" -> GET /v2.1/accounts/{accountId}/unsupported_file_types
- "List all users?" -> GET /v2.1/accounts/{accountId}/users
- "Create a user?" -> POST /v2.1/accounts/{accountId}/users
- "Get user details?" -> GET /v2.1/accounts/{accountId}/users/{userId}
- "Update a user?" -> PUT /v2.1/accounts/{accountId}/users/{userId}
- "Create a authorization?" -> POST /v2.1/accounts/{accountId}/users/{userId}/authorization
- "Get authorization details?" -> GET /v2.1/accounts/{accountId}/users/{userId}/authorization/{authorizationId}
- "Update a authorization?" -> PUT /v2.1/accounts/{accountId}/users/{userId}/authorization/{authorizationId}
- "Delete a authorization?" -> DELETE /v2.1/accounts/{accountId}/users/{userId}/authorization/{authorizationId}
- "List all authorizations?" -> GET /v2.1/accounts/{accountId}/users/{userId}/authorizations
- "Create a authorization?" -> POST /v2.1/accounts/{accountId}/users/{userId}/authorizations
- "List all agent?" -> GET /v2.1/accounts/{accountId}/users/{userId}/authorizations/agent
- "List all cloud_storage?" -> GET /v2.1/accounts/{accountId}/users/{userId}/cloud_storage
- "Create a cloud_storage?" -> POST /v2.1/accounts/{accountId}/users/{userId}/cloud_storage
- "Get cloud_storage details?" -> GET /v2.1/accounts/{accountId}/users/{userId}/cloud_storage/{serviceId}
- "Delete a cloud_storage?" -> DELETE /v2.1/accounts/{accountId}/users/{userId}/cloud_storage/{serviceId}
- "List all folders?" -> GET /v2.1/accounts/{accountId}/users/{userId}/cloud_storage/{serviceId}/folders
- "Get folder details?" -> GET /v2.1/accounts/{accountId}/users/{userId}/cloud_storage/{serviceId}/folders/{folderId}
- "List all custom_settings?" -> GET /v2.1/accounts/{accountId}/users/{userId}/custom_settings
- "List all profile?" -> GET /v2.1/accounts/{accountId}/users/{userId}/profile
- "List all image?" -> GET /v2.1/accounts/{accountId}/users/{userId}/profile/image
- "List all settings?" -> GET /v2.1/accounts/{accountId}/users/{userId}/settings
- "List all signatures?" -> GET /v2.1/accounts/{accountId}/users/{userId}/signatures
- "Create a signature?" -> POST /v2.1/accounts/{accountId}/users/{userId}/signatures
- "Get signature details?" -> GET /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId}
- "Update a signature?" -> PUT /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId}
- "Delete a signature?" -> DELETE /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId}
- "Get signature details?" -> GET /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId}/{imageType}
- "Update a signature?" -> PUT /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId}/{imageType}
- "Delete a signature?" -> DELETE /v2.1/accounts/{accountId}/users/{userId}/signatures/{signatureId}/{imageType}
- "Create a console?" -> POST /v2.1/accounts/{accountId}/views/console
- "List all watermark?" -> GET /v2.1/accounts/{accountId}/watermark
- "List all workspaces?" -> GET /v2.1/accounts/{accountId}/workspaces
- "Create a workspace?" -> POST /v2.1/accounts/{accountId}/workspaces
- "Get workspace details?" -> GET /v2.1/accounts/{accountId}/workspaces/{workspaceId}
- "Update a workspace?" -> PUT /v2.1/accounts/{accountId}/workspaces/{workspaceId}
- "Delete a workspace?" -> DELETE /v2.1/accounts/{accountId}/workspaces/{workspaceId}
- "Get folder details?" -> GET /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}
- "Delete a folder?" -> DELETE /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}
- "Create a file?" -> POST /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}/files
- "Get file details?" -> GET /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}/files/{fileId}
- "Update a file?" -> PUT /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}/files/{fileId}
- "List all pages?" -> GET /v2.1/accounts/{accountId}/workspaces/{workspaceId}/folders/{folderId}/files/{fileId}/pages
- "List all provisioning?" -> GET /v2.1/accounts/provisioning
- "List all billing_plans?" -> GET /v2.1/billing_plans
- "Get billing_plan details?" -> GET /v2.1/billing_plans/{billingPlanId}
- "List all notary?" -> GET /v2.1/current_user/notary
- "Create a notary?" -> POST /v2.1/current_user/notary
- "List all journals?" -> GET /v2.1/current_user/notary/journals
- "List all jurisdictions?" -> GET /v2.1/current_user/notary/jurisdictions
- "Create a jurisdiction?" -> POST /v2.1/current_user/notary/jurisdictions
- "Get jurisdiction details?" -> GET /v2.1/current_user/notary/jurisdictions/{jurisdictionId}
- "Update a jurisdiction?" -> PUT /v2.1/current_user/notary/jurisdictions/{jurisdictionId}
- "Delete a jurisdiction?" -> DELETE /v2.1/current_user/notary/jurisdictions/{jurisdictionId}
- "List all password_rules?" -> GET /v2.1/current_user/password_rules
- "List all request_logs?" -> GET /v2.1/diagnostics/request_logs
- "Get request_log details?" -> GET /v2.1/diagnostics/request_logs/{requestLogId}
- "List all settings?" -> GET /v2.1/diagnostics/settings
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
