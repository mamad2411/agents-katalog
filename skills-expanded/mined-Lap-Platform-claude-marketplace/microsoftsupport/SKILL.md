---
name: microsoftsupport
description: "Microsoft.Support API skill. Use when working with Microsoft.Support for providers, subscriptions. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# Microsoft.Support
API version: 2019-05-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Support/operations -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.Support/checkNameAvailability -- create first checkNameAvailability

## Endpoints

14 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Support/operations | This lists all the available Microsoft Support REST API operations. |
| GET | /providers/Microsoft.Support/services | Lists all the Azure services available for support ticket creation. Here are the Service Ids for **Billing**, **Subscription Management**, and **Service and subscription limits (Quotas)** issues: <br/><table><tr><td><u>Issue type</u></td><td><u>Service Id</u></td></tr><tr><td>Billing</td><td>'/providers/Microsoft.Support/services/517f2da6-78fd-0498-4e22-ad26996b1dfc'</td></tr><tr><td>Subscription Management</td><td>'/providers/Microsoft.Support/services/f3dc5421-79ef-1efa-41a5-42bf3cbb52c6'</td></tr><tr><td>Quota</td><td>'/providers/Microsoft.Support/services/06bfd9d3-516b-d5c6-5802-169c800dec89'</td></tr></table> <br/><br/> For **Technical** issues, select the Service Id that maps to the Azure service/product as displayed in the **Services** drop-down list on the Azure portal's <a target='_blank' href='https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/overview'>New support request</a> page. <br/><br/> Always use the service and it's corresponding problem classification(s) obtained programmatically for support ticket creation. This practice ensures that you always have the most recent set of service and problem classification Ids. |
| GET | /providers/Microsoft.Support/services/{serviceName} | Gets a specific Azure service for support ticket creation. |
| GET | /providers/Microsoft.Support/services/{serviceName}/problemClassifications | Lists all the problem classifications (categories) available for a specific Azure service.<br/><br/> Always use the service and problem classifications obtained programmatically. This practice ensures that you always have the most recent set of service and problem classification Ids. |
| GET | /providers/Microsoft.Support/services/{serviceName}/problemClassifications/{problemClassificationName} | Gets the details of a specific problem classification for a specific Azure service. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Support/checkNameAvailability | Check the availability of a resource name. This API should to be used to check the uniqueness of the name for support ticket creation for the selected subscription. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets | Lists all the support tickets for an Azure subscription. <br/><br/>You can also filter the support tickets by <i>Status</i> or <i>CreatedDate</i> using the $filter parameter. Output will be a paged result with <i>nextLink</i>, using which you can retrieve the next set of support tickets. <br/><br/>Support ticket data is available for 18 months after ticket creation. If a ticket was created more than 18 months ago, a request for data might cause an error. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName} | Gets details for a specific support ticket in an Azure subscription. <br/><br/>Support ticket data is available for 18 months after ticket creation. If a ticket was created more than 18 months ago, a request for data might cause an error. |
| PATCH | /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName} | This API allows you to update the severity level or your contact information in the support ticket. <br/><br/> Note: The severity levels cannot be changed if a support ticket is actively being worked upon by an Azure support engineer. In such a case, contact your support engineer to request severity update by adding a new communication using the Communications API. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName} | Creates a new support ticket for Quota increase, Technical, Billing, and Subscription Management issues for the specified subscription. <br/><br/>A paid technical support plan is required to create a support ticket using this API. <a href='https://aka.ms/supportticketAPI'>Learn more</a> <br/><br/> Use the Services API to map the right Service Id to the issue type. For example: For billing tickets set *serviceId* to *'/providers/Microsoft.Support/services/517f2da6-78fd-0498-4e22-ad26996b1dfc'*. <br/> For Technical issues, the Service id will map to the Azure service you want to raise a support ticket for. <br/><br/>Always call the Services and ProblemClassifications API to get the most recent set of services and problem categories required for support ticket creation. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}/checkNameAvailability | Check the availability of a resource name. This API should to be used to check the uniqueness of the name for adding a new communication to the support ticket. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}/communications | Lists all communications (attachments not included) for a support ticket. <br/></br> You can also filter support ticket communications by <i>CreatedDate</i>�or <i>CommunicationType</i> using the $filter parameter. The only type of communication supported today is <i>Web</i>. Output will be a paged result with <i>nextLink</i>, using which you can retrieve the next set of Communication results. <br/><br/> Support ticket data is available for 18 months after ticket creation. If a ticket was created more than 18 months ago, a request for data might cause an error. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}/communications/{communicationName} | Returns details of a specific communication in a support ticket. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}/communications/{communicationName} | Adds a new customer communication to an Azure support ticket. Adding attachments are not currently supported via the API. <br/>To add a file to a support ticket, visit the <a target='_blank' href='https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/managesupportrequest'>Manage support ticket</a> page in the Azure portal, select the support ticket, and use the file upload control to add a new file. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.Support/operations
- "List all services?" -> GET /providers/Microsoft.Support/services
- "Get service details?" -> GET /providers/Microsoft.Support/services/{serviceName}
- "List all problemClassifications?" -> GET /providers/Microsoft.Support/services/{serviceName}/problemClassifications
- "Get problemClassification details?" -> GET /providers/Microsoft.Support/services/{serviceName}/problemClassifications/{problemClassificationName}
- "Create a checkNameAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Support/checkNameAvailability
- "List all supportTickets?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets
- "Get supportTicket details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}
- "Partially update a supportTicket?" -> PATCH /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}
- "Update a supportTicket?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}
- "Create a checkNameAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}/checkNameAvailability
- "List all communications?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}/communications
- "Get communication details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}/communications/{communicationName}
- "Update a communication?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.Support/supportTickets/{supportTicketName}/communications/{communicationName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
