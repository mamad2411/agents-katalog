---
name: aws-service-catalog
description: "AWS Service Catalog API skill. Use when working with AWS Service Catalog for root. Covers 90 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Service Catalog
API version: 2015-12-10

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

90 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Accepts an offer to share the specified portfolio. |
| POST | / | Associates the specified budget with the specified resource. |
| POST | / | Associates the specified principal ARN with the specified portfolio. If you share the portfolio with principal name sharing enabled, the PrincipalARN association is included in the share.  The PortfolioID, PrincipalARN, and PrincipalType parameters are required.  You can associate a maximum of 10 Principals with a portfolio using PrincipalType as IAM_PATTERN.   When you associate a principal with portfolio, a potential privilege escalation path may occur when that portfolio is then shared with other accounts. For a user in a recipient account who is not an Service Catalog Admin, but still has the ability to create Principals (Users/Groups/Roles), that user could create a role that matches a principal name association for the portfolio. Although this user may not know which principal names are associated through Service Catalog, they may be able to guess the user. If this potential escalation path is a concern, then Service Catalog recommends using PrincipalType as IAM. With this configuration, the PrincipalARN must already exist in the recipient account before it can be associated. |
| POST | / | Associates the specified product with the specified portfolio. A delegated admin is authorized to invoke this command. |
| POST | / | Associates a self-service action with a provisioning artifact. |
| POST | / | Associate the specified TagOption with the specified portfolio or product. |
| POST | / | Associates multiple self-service actions with provisioning artifacts. |
| POST | / | Disassociates a batch of self-service actions from the specified provisioning artifact. |
| POST | / | Copies the specified source product to the specified target product or a new product. You can copy a product to the same account or another account. You can copy a product to the same Region or another Region. If you copy a product to another account, you must first share the product in a portfolio using CreatePortfolioShare. This operation is performed asynchronously. To track the progress of the operation, use DescribeCopyProductStatus. |
| POST | / | Creates a constraint. A delegated admin is authorized to invoke this command. |
| POST | / | Creates a portfolio. A delegated admin is authorized to invoke this command. |
| POST | / | Shares the specified portfolio with the specified account or organization node. Shares to an organization node can only be created by the management account of an organization or by a delegated administrator. You can share portfolios to an organization, an organizational unit, or a specific account. Note that if a delegated admin is de-registered, they can no longer create portfolio shares.  AWSOrganizationsAccess must be enabled in order to create a portfolio share to an organization node. You can't share a shared resource, including portfolios that contain a shared product. If the portfolio share with the specified account or organization node already exists, this action will have no effect and will not return an error. To update an existing share, you must use the  UpdatePortfolioShare API instead.   When you associate a principal with portfolio, a potential privilege escalation path may occur when that portfolio is then shared with other accounts. For a user in a recipient account who is not an Service Catalog Admin, but still has the ability to create Principals (Users/Groups/Roles), that user could create a role that matches a principal name association for the portfolio. Although this user may not know which principal names are associated through Service Catalog, they may be able to guess the user. If this potential escalation path is a concern, then Service Catalog recommends using PrincipalType as IAM. With this configuration, the PrincipalARN must already exist in the recipient account before it can be associated. |
| POST | / | Creates a product. A delegated admin is authorized to invoke this command. The user or role that performs this operation must have the cloudformation:GetTemplate IAM policy permission. This policy permission is required when using the ImportFromPhysicalId template source in the information data section. |
| POST | / | Creates a plan. A plan includes the list of resources to be created (when provisioning a new product) or modified (when updating a provisioned product) when the plan is executed. You can create one plan for each provisioned product. To create a plan for an existing provisioned product, the product status must be AVAILABLE or TAINTED. To view the resource changes in the change set, use DescribeProvisionedProductPlan. To create or modify the provisioned product, use ExecuteProvisionedProductPlan. |
| POST | / | Creates a provisioning artifact (also known as a version) for the specified product. You cannot create a provisioning artifact for a product that was shared with you. The user or role that performs this operation must have the cloudformation:GetTemplate IAM policy permission. This policy permission is required when using the ImportFromPhysicalId template source in the information data section. |
| POST | / | Creates a self-service action. |
| POST | / | Creates a TagOption. |
| POST | / | Deletes the specified constraint. A delegated admin is authorized to invoke this command. |
| POST | / | Deletes the specified portfolio. You cannot delete a portfolio if it was shared with you or if it has associated products, users, constraints, or shared accounts. A delegated admin is authorized to invoke this command. |
| POST | / | Stops sharing the specified portfolio with the specified account or organization node. Shares to an organization node can only be deleted by the management account of an organization or by a delegated administrator. Note that if a delegated admin is de-registered, portfolio shares created from that account are removed. |
| POST | / | Deletes the specified product. You cannot delete a product if it was shared with you or is associated with a portfolio. A delegated admin is authorized to invoke this command. |
| POST | / | Deletes the specified plan. |
| POST | / | Deletes the specified provisioning artifact (also known as a version) for the specified product. You cannot delete a provisioning artifact associated with a product that was shared with you. You cannot delete the last provisioning artifact for a product, because a product must have at least one provisioning artifact. |
| POST | / | Deletes a self-service action. |
| POST | / | Deletes the specified TagOption. You cannot delete a TagOption if it is associated with a product or portfolio. |
| POST | / | Gets information about the specified constraint. |
| POST | / | Gets the status of the specified copy product operation. |
| POST | / | Gets information about the specified portfolio. A delegated admin is authorized to invoke this command. |
| POST | / | Gets the status of the specified portfolio share operation. This API can only be called by the management account in the organization or by a delegated admin. |
| POST | / | Returns a summary of each of the portfolio shares that were created for the specified portfolio. You can use this API to determine which accounts or organizational nodes this portfolio have been shared, whether the recipient entity has imported the share, and whether TagOptions are included with the share. The PortfolioId and Type parameters are both required. |
| POST | / | Gets information about the specified product.   Running this operation with administrator access results in a failure. DescribeProductAsAdmin should be used instead. |
| POST | / | Gets information about the specified product. This operation is run with administrator access. |
| POST | / | Gets information about the specified product. |
| POST | / | Gets information about the specified provisioned product. |
| POST | / | Gets information about the resource changes for the specified plan. |
| POST | / | Gets information about the specified provisioning artifact (also known as a version) for the specified product. |
| POST | / | Gets information about the configuration required to provision the specified product using the specified provisioning artifact. If the output contains a TagOption key with an empty list of values, there is a TagOption conflict for that key. The end user cannot take action to fix the conflict, and launch is not blocked. In subsequent calls to ProvisionProduct, do not include conflicted TagOption keys as tags, or this causes the error "Parameter validation failed: Missing required parameter in Tags[N]:Value". Tag the provisioned product with the value sc-tagoption-conflict-portfolioId-productId. |
| POST | / | Gets information about the specified request operation. Use this operation after calling a request operation (for example, ProvisionProduct, TerminateProvisionedProduct, or UpdateProvisionedProduct).   If a provisioned product was transferred to a new owner using UpdateProvisionedProductProperties, the new owner will be able to describe all past records for that product. The previous owner will no longer be able to describe the records, but will be able to use ListRecordHistory to see the product's history from when he was the owner. |
| POST | / | Describes a self-service action. |
| POST | / | Finds the default parameters for a specific self-service action on a specific provisioned product and returns a map of the results to the user. |
| POST | / | Gets information about the specified TagOption. |
| POST | / | Disable portfolio sharing through the Organizations service. This command will not delete your current shares, but prevents you from creating new shares throughout your organization. Current shares are not kept in sync with your organization structure if the structure changes after calling this API. Only the management account in the organization can call this API. You cannot call this API if there are active delegated administrators in the organization. Note that a delegated administrator is not authorized to invoke DisableAWSOrganizationsAccess.  If you share an Service Catalog portfolio in an organization within Organizations, and then disable Organizations access for Service Catalog, the portfolio access permissions will not sync with the latest changes to the organization structure. Specifically, accounts that you removed from the organization after disabling Service Catalog access will retain access to the previously shared portfolio. |
| POST | / | Disassociates the specified budget from the specified resource. |
| POST | / | Disassociates a previously associated principal ARN from a specified portfolio. The PrincipalType and PrincipalARN must match the AssociatePrincipalWithPortfolio call request details. For example, to disassociate an association created with a PrincipalARN of PrincipalType IAM you must use the PrincipalType IAM when calling DisassociatePrincipalFromPortfolio.  For portfolios that have been shared with principal name sharing enabled: after disassociating a principal, share recipient accounts will no longer be able to provision products in this portfolio using a role matching the name of the associated principal.  For more information, review associate-principal-with-portfolio in the Amazon Web Services CLI Command Reference.   If you disassociate a principal from a portfolio, with PrincipalType as IAM, the same principal will still have access to the portfolio if it matches one of the associated principals of type IAM_PATTERN. To fully remove access for a principal, verify all the associated Principals of type IAM_PATTERN, and then ensure you disassociate any IAM_PATTERN principals that match the principal whose access you are removing. |
| POST | / | Disassociates the specified product from the specified portfolio.  A delegated admin is authorized to invoke this command. |
| POST | / | Disassociates the specified self-service action association from the specified provisioning artifact. |
| POST | / | Disassociates the specified TagOption from the specified resource. |
| POST | / | Enable portfolio sharing feature through Organizations. This API will allow Service Catalog to receive updates on your organization in order to sync your shares with the current structure. This API can only be called by the management account in the organization. When you call this API, Service Catalog calls organizations:EnableAWSServiceAccess on your behalf so that your shares stay in sync with any changes in your Organizations structure. Note that a delegated administrator is not authorized to invoke EnableAWSOrganizationsAccess.  If you have previously disabled Organizations access for Service Catalog, and then enable access again, the portfolio access permissions might not sync with the latest changes to the organization structure. Specifically, accounts that you removed from the organization after disabling Service Catalog access, and before you enabled access again, can retain access to the previously shared portfolio. As a result, an account that has been removed from the organization might still be able to create or manage Amazon Web Services resources when it is no longer authorized to do so. Amazon Web Services is working to resolve this issue. |
| POST | / | Provisions or modifies a product based on the resource changes for the specified plan. |
| POST | / | Executes a self-service action against a provisioned product. |
| POST | / | Get the Access Status for Organizations portfolio share feature. This API can only be called by the management account in the organization or by a delegated admin. |
| POST | / | This API takes either a ProvisonedProductId or a ProvisionedProductName, along with a list of one or more output keys, and responds with the key/value pairs of those outputs. |
| POST | / | Requests the import of a resource as an Service Catalog provisioned product that is associated to an Service Catalog product and provisioning artifact. Once imported, all supported governance actions are supported on the provisioned product.   Resource import only supports CloudFormation stack ARNs. CloudFormation StackSets, and non-root nested stacks, are not supported.   The CloudFormation stack must have one of the following statuses to be imported: CREATE_COMPLETE, UPDATE_COMPLETE, UPDATE_ROLLBACK_COMPLETE, IMPORT_COMPLETE, and IMPORT_ROLLBACK_COMPLETE.   Import of the resource requires that the CloudFormation stack template matches the associated Service Catalog product provisioning artifact.    When you import an existing CloudFormation stack into a portfolio, Service Catalog does not apply the product's associated constraints during the import process. Service Catalog applies the constraints after you call UpdateProvisionedProduct for the provisioned product.    The user or role that performs this operation must have the cloudformation:GetTemplate and cloudformation:DescribeStacks IAM policy permissions.  You can only import one provisioned product at a time. The product's CloudFormation stack must have the IMPORT_COMPLETE status before you import another. |
| POST | / | Lists all imported portfolios for which account-to-account shares were accepted by this account. By specifying the PortfolioShareType, you can list portfolios for which organizational shares were accepted by this account. |
| POST | / | Lists all the budgets associated to the specified resource. |
| POST | / | Lists the constraints for the specified portfolio and product. |
| POST | / | Lists the paths to the specified product. A path describes how the user gets access to a specified product and is necessary when provisioning a product. A path also determines the constraints that are put on a product. A path is dependent on a specific product, porfolio, and principal.    When provisioning a product that's been added to a portfolio, you must grant your user, group, or role access to the portfolio. For more information, see Granting users access in the Service Catalog User Guide. |
| POST | / | Lists the organization nodes that have access to the specified portfolio. This API can only be called by the management account in the organization or by a delegated admin. If a delegated admin is de-registered, they can no longer perform this operation. |
| POST | / | Lists the account IDs that have access to the specified portfolio. A delegated admin can list the accounts that have access to the shared portfolio. Note that if a delegated admin is de-registered, they can no longer perform this operation. |
| POST | / | Lists all portfolios in the catalog. |
| POST | / | Lists all portfolios that the specified product is associated with. |
| POST | / | Lists all PrincipalARNs and corresponding PrincipalTypes associated with the specified portfolio. |
| POST | / | Lists the plans for the specified provisioned product or all plans to which the user has access. |
| POST | / | Lists all provisioning artifacts (also known as versions) for the specified product. |
| POST | / | Lists all provisioning artifacts (also known as versions) for the specified self-service action. |
| POST | / | Lists the specified requests or all performed requests. |
| POST | / | Lists the resources associated with the specified TagOption. |
| POST | / | Lists all self-service actions. |
| POST | / | Returns a paginated list of self-service actions associated with the specified Product ID and Provisioning Artifact ID. |
| POST | / | Returns summary information about stack instances that are associated with the specified CFN_STACKSET type provisioned product. You can filter for stack instances that are associated with a specific Amazon Web Services account name or Region. |
| POST | / | Lists the specified TagOptions or all TagOptions. |
| POST | / | Notifies the result of the provisioning engine execution. |
| POST | / | Notifies the result of the terminate engine execution. |
| POST | / | Notifies the result of the update engine execution. |
| POST | / | Provisions the specified product.   A provisioned product is a resourced instance of a product. For example, provisioning a product that's based on an CloudFormation template launches an CloudFormation stack and its underlying resources. You can check the status of this request using DescribeRecord.   If the request contains a tag key with an empty list of values, there's a tag conflict for that key. Don't include conflicted keys as tags, or this will cause the error "Parameter validation failed: Missing required parameter in Tags[N]:Value".    When provisioning a product that's been added to a portfolio, you must grant your user, group, or role access to the portfolio. For more information, see Granting users access in the Service Catalog User Guide. |
| POST | / | Rejects an offer to share the specified portfolio. |
| POST | / | Lists the provisioned products that are available (not terminated). To use additional filtering, see SearchProvisionedProducts. |
| POST | / | Gets information about the products to which the caller has access. |
| POST | / | Gets information about the products for the specified portfolio or all products. |
| POST | / | Gets information about the provisioned products that meet the specified criteria. |
| POST | / | Terminates the specified provisioned product. This operation does not delete any records associated with the provisioned product. You can check the status of this request using DescribeRecord. |
| POST | / | Updates the specified constraint. |
| POST | / | Updates the specified portfolio. You cannot update a product that was shared with you. |
| POST | / | Updates the specified portfolio share. You can use this API to enable or disable TagOptions sharing or Principal sharing for an existing portfolio share.  The portfolio share cannot be updated if the CreatePortfolioShare operation is IN_PROGRESS, as the share is not available to recipient entities. In this case, you must wait for the portfolio share to be completed. You must provide the accountId or organization node in the input, but not both. If the portfolio is shared to both an external account and an organization node, and both shares need to be updated, you must invoke UpdatePortfolioShare separately for each share type.  This API cannot be used for removing the portfolio share. You must use DeletePortfolioShare API for that action.   When you associate a principal with portfolio, a potential privilege escalation path may occur when that portfolio is then shared with other accounts. For a user in a recipient account who is not an Service Catalog Admin, but still has the ability to create Principals (Users/Groups/Roles), that user could create a role that matches a principal name association for the portfolio. Although this user may not know which principal names are associated through Service Catalog, they may be able to guess the user. If this potential escalation path is a concern, then Service Catalog recommends using PrincipalType as IAM. With this configuration, the PrincipalARN must already exist in the recipient account before it can be associated. |
| POST | / | Updates the specified product. |
| POST | / | Requests updates to the configuration of the specified provisioned product. If there are tags associated with the object, they cannot be updated or added. Depending on the specific updates requested, this operation can update with no interruption, with some interruption, or replace the provisioned product entirely. You can check the status of this request using DescribeRecord. |
| POST | / | Requests updates to the properties of the specified provisioned product. |
| POST | / | Updates the specified provisioning artifact (also known as a version) for the specified product. You cannot update a provisioning artifact for a product that was shared with you. |
| POST | / | Updates a self-service action. |
| POST | / | Updates the specified TagOption. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
