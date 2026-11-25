---
name: billingmanagementclient
description: "BillingManagementClient API skill. Use when working with BillingManagementClient for providers, subscriptions. Covers 119 endpoints."
version: 1.0.0
generator: lapsh
---

# BillingManagementClient
API version: 2019-10-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Billing/billingAccounts -- verify access
3. POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/listInvoiceSectionsWithCreateSubscriptionPermission -- create first listInvoiceSectionsWithCreateSubscriptionPermission

## Endpoints

119 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Billing/billingAccounts | Lists the billing accounts that a user has access to. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName} | Gets a billing account by its ID. |
| PATCH | /providers/Microsoft.Billing/billingAccounts/{billingAccountName} | Updates the properties of a billing account. Currently, displayName and address can be updated. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/listInvoiceSectionsWithCreateSubscriptionPermission | Lists the invoice sections for which the user has permission to create Azure subscriptions. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/paymentMethods | Lists the payment Methods for a billing account. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/validateAddress | Validates an address. Use the operation to validate an address before using it as a billing account or a billing profile address. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/availableBalance/default | The available credit balance for a billing profile. This is the balance that can be used for pay now to settle due or past due invoices. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/instructions | Lists the instructions by billing profile id. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/instructions/{instructionName} | Get the instruction by name. These are custom billing instructions and are only applicable for certain customers. |
| PUT | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/instructions/{instructionName} | Creates or updates an instruction. These are custom billing instructions and are only applicable for certain customers. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/paymentMethods | Lists the payment Methods for a billing profile. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/validateDetachPaymentMethodEligibility | Validates if the default payment method can be detached from the billing profile. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles | Lists the billing profiles that a user has access to. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName} | Gets a billing profile by its ID. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement. |
| PUT | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName} | Creates a billing profile. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement. |
| PATCH | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName} | Updates the properties of a billing profile. Currently, displayName, poNumber, bill-to address and invoiceEmailOptIn can be updated. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers | Lists the customers that are billed to a billing profile. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections | Lists the invoice sections that a user has access to. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName} | Gets an invoice section by its ID. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| PUT | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName} | Creates an invoice section. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| PATCH | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName} | Updates an invoice section. Currently, only displayName can be updated. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers | Lists the customers that are billed to a billing account. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName} | Gets a customer by its ID. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/billingPermissions | Lists the billing permissions the caller has for a customer. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/billingSubscriptions | Lists the subscriptions for a customer. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/billingSubscriptions/{billingSubscriptionName} | Gets a subscription by its ID. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/products | Lists the products for a customer. These don't include products billed based on usage.The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/products/{productName} | Gets a product by ID. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/transactions | Lists the billed and unbilled transactions by customer id for given start date and end date. Transactions include purchases, refunds and Azure usage charges. Unbilled transactions are listed under pending invoice Id and do not include tax. Tax is added to the amount once an invoice is generated. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments | Lists the departments that a user has access to. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName} | Gets a department by ID. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts | Lists the enrollment accounts for a billing account. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName} | Gets an enrollment account by ID. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/invoices | Lists the invoices for a billing account for a given start date and end date. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement, Microsoft Customer Agreement or Enterprise Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/downloadDocuments | Gets a URL to download multiple invoice documents (invoice pdf, tax receipts, credit notes) as a zip file. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/invoices/{invoiceName} | Gets an invoice by billing account name and ID. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement, Microsoft Customer Agreement or Enterprise Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/default/billingSubscriptions/{subscriptionId}/downloadDocuments | Gets a URL to download multiple invoice documents (invoice pdf, tax receipts, credit notes) as a zip file. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoices/{invoiceName}/pricesheet/default/download | Gets a URL to download the pricesheet for an invoice. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/pricesheet/default/download | Gets a URL to download the current month's pricesheet for a billing profile. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement.This API is hereby deprecated in favor of https://docs.microsoft.com/en-us/rest/api/cost-management/2022-02-01-preview/price-sheet/download-by-billing-profile. We highly recommend you move to the new preview version, as the csv file in the current preview version will have 500k max size that cannot scale with Azure product growth. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoices | Lists the invoices for a billing profile for a given start date and end date. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/downloadDocuments | Gets a URL to download multiple invoice documents (invoice pdf, tax receipts, credit notes) as a zip file. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoices/{invoiceName} | Gets an invoice by ID. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingSubscriptions | Lists the subscriptions for a billing account. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingSubscriptions/{billingSubscriptionName}/invoices | Lists the invoices for a subscription. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingSubscriptions/{billingSubscriptionName}/invoices/{invoiceName} | Gets an invoice by ID. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingSubscriptions | Lists the subscriptions that are billed to a billing profile. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingSubscriptions | Lists the subscriptions that are billed to an invoice section. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingSubscriptions/{billingSubscriptionName} | Gets a subscription by its ID. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingSubscriptions/{billingSubscriptionName}/transfer | Moves a subscription's charges to a new invoice section. The new invoice section must belong to the same billing profile as the existing invoice section. This operation is supported only for products that are purchased with a recurring charge and for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingSubscriptions/{billingSubscriptionName}/validateTransferEligibility | Validates if a subscription's charges can be moved to a new invoice section. This operation is supported only for products that are purchased with a recurring charge and for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/products | Lists the products for a billing account. These don't include products billed based on usage. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products | Lists the products for an invoice section. These don't include products billed based on usage. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products/{productName} | Gets a product by ID. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products/{productName}/transfer | Moves a product's charges to a new invoice section. The new invoice section must belong to the same billing profile as the existing invoice section. This operation is supported only for products that are purchased with a recurring charge and for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products/{productName}/validateTransferEligibility | Validates if a product's charges can be moved to a new invoice section. This operation is supported only for products that are purchased with a recurring charge and for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/transactions | Lists the billed and unbilled transactions by billing account name for given start and end date. Transactions include purchases, refunds and Azure usage charges. Unbilled transactions are listed under pending invoice ID and do not include tax. Tax is added to the amount once an invoice is generated. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/transactions | Lists the billed and unbilled transactions by billing profile name for given start date and end date. Transactions include purchases, refunds and Azure usage charges. Unbilled transactions are listed under pending invoice Id and do not include tax. Tax is added to the amount once an invoice is generated. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/transactions | Lists the billed and unbilled transactions by invoice section name for given start date and end date. Transactions include purchases, refunds and Azure usage charges. Unbilled transactions are listed under pending invoice Id and do not include tax. Tax is added to the amount once an invoice is generated. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoices/{invoiceName}/transactions | Lists the transactions for an invoice. Transactions include purchases, refunds and Azure usage charges. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/transactions/{transactionName} | Gets a transaction by ID. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement or Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/policies/default | Lists the policies for a billing profile. This operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| PUT | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/policies/default | Updates the policies for a billing profile. This operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/policies/default | Lists the policies for a customer. This operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| PUT | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/policies/default | Updates the policies for a customer. This operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products/{productName}/updateAutoRenew | Cancel auto renew for product by product id and invoice section name |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/elevate | Gives the caller permissions on an invoice section based on their billing profile access.  The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/initiateTransfer | Sends a request to a user in another billing account to transfer billing ownership of their subscriptions. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/transfers/{transferName} | Gets a transfer request by ID. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| DELETE | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/transfers/{transferName} | Cancels a transfer request. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/transfers | Lists the transfer requests for an invoice section. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers/{customerName}/initiateTransfer | Sends a request to a user in a customer's billing account to transfer billing ownership of their subscriptions. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers/{customerName}/transfers/{transferName} | Gets a transfer request by ID. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| DELETE | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers/{customerName}/transfers/{transferName} | Cancels a transfer request. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers/{customerName}/transfers | Lists the transfer requests sent to a customer. The operation is supported only for billing accounts with agreement type Microsoft Partner Agreement. |
| POST | /providers/Microsoft.Billing/transfers/{transferName}/acceptTransfer | Accepts a transfer request. |
| POST | /providers/Microsoft.Billing/transfers/{transferName}/validateTransfer | Validates if a subscription or a reservation can be transferred. Use this operation to validate your subscriptions or reservation before using the accept transfer operation. |
| POST | /providers/Microsoft.Billing/transfers/{transferName}/declineTransfer | Declines a transfer request. |
| GET | /providers/Microsoft.Billing/transfers/{transferName} | Gets a transfer request by ID. The caller must be the recipient of the transfer request. |
| GET | /providers/Microsoft.Billing/transfers | Lists the transfer requests received by the caller. |
| GET | /providers/Microsoft.Billing/operations | Lists the available billing REST API operations. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingPermissions | Lists the billing permissions the caller has on a billing account. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingPermissions | Lists the billing permissions the caller has on an invoice section. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingPermissions | Lists the billing permissions the caller has on a billing profile. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingPermissions | Lists the billing permissions the caller has on a department. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingPermissions | Lists the billing permissions the caller has on an enrollment account. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleDefinitions/{billingRoleDefinitionName} | Gets the definition for a role on a billing account. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleDefinitions/{billingRoleDefinitionName} | Gets the definition for a role on an invoice section. The operation is supported only for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleDefinitions/{billingRoleDefinitionName} | Gets the definition for a role on a billing profile. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleDefinitions/{billingRoleDefinitionName} | Gets the definition for a role on a department. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleDefinitions/{billingRoleDefinitionName} | Gets the definition for a role on an enrollment account. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleDefinitions | Lists the role definitions for a billing account. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement, Microsoft Customer Agreement or Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleDefinitions | Lists the role definitions for an invoice section. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleDefinitions | Lists the role definitions for a billing profile. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleDefinitions | Lists the role definitions for a department. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleDefinitions | Lists the role definitions for a enrollmentAccount. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleAssignments/{billingRoleAssignmentName} | Gets a role assignment for the caller on a billing account. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement, Microsoft Customer Agreement or Enterprise Agreement. |
| DELETE | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleAssignments/{billingRoleAssignmentName} | Deletes a role assignment for the caller on a billing account. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| PUT | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleAssignments/{billingRoleAssignmentName} | Create or update a billing role assignment. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleAssignments/{billingRoleAssignmentName} | Gets a role assignment for the caller on an invoice section. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement. |
| DELETE | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleAssignments/{billingRoleAssignmentName} | Deletes a role assignment for the caller on an invoice section. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleAssignments/{billingRoleAssignmentName} | Gets a role assignment for the caller on a billing profile. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| DELETE | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleAssignments/{billingRoleAssignmentName} | Deletes a role assignment for the caller on a billing profile. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement or Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleAssignments/{billingRoleAssignmentName} | Gets a role assignment for the caller on a department. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| DELETE | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleAssignments/{billingRoleAssignmentName} | Deletes a role assignment for the caller on a department. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| PUT | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleAssignments/{billingRoleAssignmentName} | Create or update a billing role assignment. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleAssignments/{billingRoleAssignmentName} | Gets a role assignment for the caller on a enrollment Account. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| DELETE | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleAssignments/{billingRoleAssignmentName} | Deletes a role assignment for the caller on a enrollment Account. The operation is supported only for billing accounts with agreement type Enterprise Agreement. |
| PUT | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleAssignments/{billingRoleAssignmentName} | Create or update a billing role assignment. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleAssignments | Lists the role assignments for the caller on a billing account. The operation is supported for billing accounts with agreement type Microsoft Partner Agreement, Microsoft Customer Agreement or Enterprise Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/createBillingRoleAssignment | Adds a role assignment on a billing account. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleAssignments | Lists the role assignments for the caller on an invoice section. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/createBillingRoleAssignment | Adds a role assignment on an invoice section. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleAssignments | Lists the role assignments for the caller on a billing profile. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement. |
| POST | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/createBillingRoleAssignment | Adds a role assignment on a billing profile. The operation is supported for billing accounts with agreement type Microsoft Customer Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleAssignments | Lists the role assignments for the caller on a billing profile. The operation is supported for billing accounts of type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleAssignments | Lists the role assignments for the caller on a billing profile. The operation is supported for billing accounts of type Enterprise Agreement. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/agreements | Lists the agreements for a billing account. |
| GET | /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/agreements/{agreementName} | Gets an agreement by ID. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Billing/billingProperty/default | Get the billing properties for a subscription. This operation is not supported for billing accounts with agreement type Enterprise Agreement. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all billingAccounts?" -> GET /providers/Microsoft.Billing/billingAccounts
- "Get billingAccount details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}
- "Partially update a billingAccount?" -> PATCH /providers/Microsoft.Billing/billingAccounts/{billingAccountName}
- "Create a listInvoiceSectionsWithCreateSubscriptionPermission?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/listInvoiceSectionsWithCreateSubscriptionPermission
- "List all paymentMethods?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/paymentMethods
- "Create a validateAddress?" -> POST /providers/Microsoft.Billing/validateAddress
- "List all default?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/availableBalance/default
- "List all instructions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/instructions
- "Get instruction details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/instructions/{instructionName}
- "Update a instruction?" -> PUT /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/instructions/{instructionName}
- "List all paymentMethods?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/paymentMethods
- "List all validateDetachPaymentMethodEligibility?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/validateDetachPaymentMethodEligibility
- "List all billingProfiles?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles
- "Get billingProfile details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}
- "Update a billingProfile?" -> PUT /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}
- "Partially update a billingProfile?" -> PATCH /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}
- "List all customers?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers
- "List all invoiceSections?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections
- "Get invoiceSection details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}
- "Update a invoiceSection?" -> PUT /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}
- "Partially update a invoiceSection?" -> PATCH /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}
- "List all customers?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers
- "Get customer details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}
- "List all billingPermissions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/billingPermissions
- "List all billingSubscriptions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/billingSubscriptions
- "Get billingSubscription details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/billingSubscriptions/{billingSubscriptionName}
- "List all products?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/products
- "Get product details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/products/{productName}
- "List all transactions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/transactions
- "List all departments?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments
- "Get department details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}
- "List all enrollmentAccounts?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts
- "Get enrollmentAccount details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}
- "List all invoices?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/invoices
- "Create a downloadDocument?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/downloadDocuments
- "Get invoice details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/invoices/{invoiceName}
- "Create a downloadDocument?" -> POST /providers/Microsoft.Billing/billingAccounts/default/billingSubscriptions/{subscriptionId}/downloadDocuments
- "Create a download?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoices/{invoiceName}/pricesheet/default/download
- "Create a download?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/pricesheet/default/download
- "List all invoices?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoices
- "Create a downloadDocument?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/downloadDocuments
- "Get invoice details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoices/{invoiceName}
- "List all billingSubscriptions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingSubscriptions
- "List all invoices?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingSubscriptions/{billingSubscriptionName}/invoices
- "Get invoice details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingSubscriptions/{billingSubscriptionName}/invoices/{invoiceName}
- "List all billingSubscriptions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingSubscriptions
- "List all billingSubscriptions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingSubscriptions
- "Get billingSubscription details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingSubscriptions/{billingSubscriptionName}
- "Create a transfer?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingSubscriptions/{billingSubscriptionName}/transfer
- "Create a validateTransferEligibility?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingSubscriptions/{billingSubscriptionName}/validateTransferEligibility
- "List all products?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/products
- "List all products?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products
- "Get product details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products/{productName}
- "Create a transfer?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products/{productName}/transfer
- "Create a validateTransferEligibility?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products/{productName}/validateTransferEligibility
- "List all transactions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/transactions
- "List all transactions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/transactions
- "List all transactions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/transactions
- "List all transactions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoices/{invoiceName}/transactions
- "Get transaction details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/transactions/{transactionName}
- "List all default?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/policies/default
- "List all default?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/customers/{customerName}/policies/default
- "List all default?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Billing/billingProperty/default
- "Create a updateAutoRenew?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/products/{productName}/updateAutoRenew
- "Create a elevate?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/elevate
- "Create a initiateTransfer?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/initiateTransfer
- "Get transfer details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/transfers/{transferName}
- "Delete a transfer?" -> DELETE /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/transfers/{transferName}
- "List all transfers?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/transfers
- "Create a initiateTransfer?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers/{customerName}/initiateTransfer
- "Get transfer details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers/{customerName}/transfers/{transferName}
- "Delete a transfer?" -> DELETE /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers/{customerName}/transfers/{transferName}
- "List all transfers?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/customers/{customerName}/transfers
- "Create a acceptTransfer?" -> POST /providers/Microsoft.Billing/transfers/{transferName}/acceptTransfer
- "Create a validateTransfer?" -> POST /providers/Microsoft.Billing/transfers/{transferName}/validateTransfer
- "Create a declineTransfer?" -> POST /providers/Microsoft.Billing/transfers/{transferName}/declineTransfer
- "Get transfer details?" -> GET /providers/Microsoft.Billing/transfers/{transferName}
- "List all transfers?" -> GET /providers/Microsoft.Billing/transfers
- "List all operations?" -> GET /providers/Microsoft.Billing/operations
- "List all billingPermissions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingPermissions
- "List all billingPermissions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingPermissions
- "List all billingPermissions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingPermissions
- "List all billingPermissions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingPermissions
- "List all billingPermissions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingPermissions
- "Get billingRoleDefinition details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleDefinitions/{billingRoleDefinitionName}
- "Get billingRoleDefinition details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleDefinitions/{billingRoleDefinitionName}
- "Get billingRoleDefinition details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleDefinitions/{billingRoleDefinitionName}
- "Get billingRoleDefinition details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleDefinitions/{billingRoleDefinitionName}
- "Get billingRoleDefinition details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleDefinitions/{billingRoleDefinitionName}
- "List all billingRoleDefinitions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleDefinitions
- "List all billingRoleDefinitions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleDefinitions
- "List all billingRoleDefinitions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleDefinitions
- "List all billingRoleDefinitions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleDefinitions
- "List all billingRoleDefinitions?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleDefinitions
- "Get billingRoleAssignment details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Delete a billingRoleAssignment?" -> DELETE /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Update a billingRoleAssignment?" -> PUT /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Get billingRoleAssignment details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Delete a billingRoleAssignment?" -> DELETE /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Get billingRoleAssignment details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Delete a billingRoleAssignment?" -> DELETE /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Get billingRoleAssignment details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Delete a billingRoleAssignment?" -> DELETE /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Update a billingRoleAssignment?" -> PUT /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Get billingRoleAssignment details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Delete a billingRoleAssignment?" -> DELETE /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleAssignments/{billingRoleAssignmentName}
- "Update a billingRoleAssignment?" -> PUT /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleAssignments/{billingRoleAssignmentName}
- "List all billingRoleAssignments?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingRoleAssignments
- "Create a createBillingRoleAssignment?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/createBillingRoleAssignment
- "List all billingRoleAssignments?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/billingRoleAssignments
- "Create a createBillingRoleAssignment?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}/createBillingRoleAssignment
- "List all billingRoleAssignments?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/billingRoleAssignments
- "Create a createBillingRoleAssignment?" -> POST /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/createBillingRoleAssignment
- "List all billingRoleAssignments?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/departments/{departmentName}/billingRoleAssignments
- "List all billingRoleAssignments?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}/billingRoleAssignments
- "List all agreements?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/agreements
- "Get agreement details?" -> GET /providers/Microsoft.Billing/billingAccounts/{billingAccountName}/agreements/{agreementName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
