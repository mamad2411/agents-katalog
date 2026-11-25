---
name: amazon-managed-blockchain
description: "Amazon Managed Blockchain API skill. Use when working with Amazon Managed Blockchain for accessors, networks, invitations. Covers 27 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Managed Blockchain
API version: 2018-09-24

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /accessors -- verify access
3. POST /accessors -- create first accessors

## Endpoints

27 endpoints across 4 groups. See references/api-spec.lap for full details.

### accessors
| Method | Path | Description |
|--------|------|-------------|
| POST | /accessors | Creates a new accessor for use with Amazon Managed Blockchain service that supports token based access. The accessor contains information required for token based access. |
| DELETE | /accessors/{AccessorId} | Deletes an accessor that your Amazon Web Services account owns. An accessor object is a container that has the information required for token based access to your Ethereum nodes including, the BILLING_TOKEN. After an accessor is deleted, the status of the accessor changes from AVAILABLE to PENDING_DELETION. An accessor in the PENDING_DELETION state can’t be used for new WebSocket requests or HTTP requests. However, WebSocket connections that were initiated while the accessor was in the AVAILABLE state remain open until they expire (up to 2 hours). |
| GET | /accessors/{AccessorId} | Returns detailed information about an accessor. An accessor object is a container that has the information required for token based access to your Ethereum nodes. |
| GET | /accessors | Returns a list of the accessors and their properties. Accessor objects are containers that have the information required for token based access to your Ethereum nodes. |

### networks
| Method | Path | Description |
|--------|------|-------------|
| POST | /networks/{networkId}/members | Creates a member within a Managed Blockchain network. Applies only to Hyperledger Fabric. |
| POST | /networks | Creates a new blockchain network using Amazon Managed Blockchain. Applies only to Hyperledger Fabric. |
| POST | /networks/{networkId}/nodes | Creates a node on the specified blockchain network. Applies to Hyperledger Fabric and Ethereum. |
| POST | /networks/{networkId}/proposals | Creates a proposal for a change to the network that other members of the network can vote on, for example, a proposal to add a new member to the network. Any member can create a proposal. Applies only to Hyperledger Fabric. |
| DELETE | /networks/{networkId}/members/{memberId} | Deletes a member. Deleting a member removes the member and all associated resources from the network. DeleteMember can only be called for a specified MemberId if the principal performing the action is associated with the Amazon Web Services account that owns the member. In all other cases, the DeleteMember action is carried out as the result of an approved proposal to remove a member. If MemberId is the last member in a network specified by the last Amazon Web Services account, the network is deleted also. Applies only to Hyperledger Fabric. |
| DELETE | /networks/{networkId}/nodes/{nodeId} | Deletes a node that your Amazon Web Services account owns. All data on the node is lost and cannot be recovered. Applies to Hyperledger Fabric and Ethereum. |
| GET | /networks/{networkId}/members/{memberId} | Returns detailed information about a member. Applies only to Hyperledger Fabric. |
| GET | /networks/{networkId} | Returns detailed information about a network. Applies to Hyperledger Fabric and Ethereum. |
| GET | /networks/{networkId}/nodes/{nodeId} | Returns detailed information about a node. Applies to Hyperledger Fabric and Ethereum. |
| GET | /networks/{networkId}/proposals/{proposalId} | Returns detailed information about a proposal. Applies only to Hyperledger Fabric. |
| GET | /networks/{networkId}/members | Returns a list of the members in a network and properties of their configurations. Applies only to Hyperledger Fabric. |
| GET | /networks | Returns information about the networks in which the current Amazon Web Services account participates. Applies to Hyperledger Fabric and Ethereum. |
| GET | /networks/{networkId}/nodes | Returns information about the nodes within a network. Applies to Hyperledger Fabric and Ethereum. |
| GET | /networks/{networkId}/proposals/{proposalId}/votes | Returns the list of votes for a specified proposal, including the value of each vote and the unique identifier of the member that cast the vote. Applies only to Hyperledger Fabric. |
| GET | /networks/{networkId}/proposals | Returns a list of proposals for the network. Applies only to Hyperledger Fabric. |
| PATCH | /networks/{networkId}/members/{memberId} | Updates a member configuration with new parameters. Applies only to Hyperledger Fabric. |
| PATCH | /networks/{networkId}/nodes/{nodeId} | Updates a node configuration with new parameters. Applies only to Hyperledger Fabric. |
| POST | /networks/{networkId}/proposals/{proposalId}/votes | Casts a vote for a specified ProposalId on behalf of a member. The member to vote as, specified by VoterMemberId, must be in the same Amazon Web Services account as the principal that calls the action. Applies only to Hyperledger Fabric. |

### invitations
| Method | Path | Description |
|--------|------|-------------|
| GET | /invitations | Returns a list of all invitations for the current Amazon Web Services account. Applies only to Hyperledger Fabric. |
| DELETE | /invitations/{invitationId} | Rejects an invitation to join a network. This action can be called by a principal in an Amazon Web Services account that has received an invitation to create a member and join a network. Applies only to Hyperledger Fabric. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns a list of tags for the specified resource. Each tag consists of a key and optional value. For more information about tags, see Tagging Resources in the Amazon Managed Blockchain Ethereum Developer Guide, or Tagging Resources in the Amazon Managed Blockchain Hyperledger Fabric Developer Guide. |
| POST | /tags/{resourceArn} | Adds or overwrites the specified tags for the specified Amazon Managed Blockchain resource. Each tag consists of a key and optional value. When you specify a tag key that already exists, the tag value is overwritten with the new value. Use UntagResource to remove tag keys. A resource can have up to 50 tags. If you try to create more than 50 tags for a resource, your request fails and returns an error. For more information about tags, see Tagging Resources in the Amazon Managed Blockchain Ethereum Developer Guide, or Tagging Resources in the Amazon Managed Blockchain Hyperledger Fabric Developer Guide. |
| DELETE | /tags/{resourceArn} | Removes the specified tags from the Amazon Managed Blockchain resource. For more information about tags, see Tagging Resources in the Amazon Managed Blockchain Ethereum Developer Guide, or Tagging Resources in the Amazon Managed Blockchain Hyperledger Fabric Developer Guide. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a accessor?" -> POST /accessors
- "Create a member?" -> POST /networks/{networkId}/members
- "Create a network?" -> POST /networks
- "Create a node?" -> POST /networks/{networkId}/nodes
- "Create a proposal?" -> POST /networks/{networkId}/proposals
- "Delete a accessor?" -> DELETE /accessors/{AccessorId}
- "Delete a member?" -> DELETE /networks/{networkId}/members/{memberId}
- "Delete a node?" -> DELETE /networks/{networkId}/nodes/{nodeId}
- "Get accessor details?" -> GET /accessors/{AccessorId}
- "Get member details?" -> GET /networks/{networkId}/members/{memberId}
- "Get network details?" -> GET /networks/{networkId}
- "Get node details?" -> GET /networks/{networkId}/nodes/{nodeId}
- "Get proposal details?" -> GET /networks/{networkId}/proposals/{proposalId}
- "List all accessors?" -> GET /accessors
- "List all invitations?" -> GET /invitations
- "List all members?" -> GET /networks/{networkId}/members
- "List all networks?" -> GET /networks
- "List all nodes?" -> GET /networks/{networkId}/nodes
- "List all votes?" -> GET /networks/{networkId}/proposals/{proposalId}/votes
- "List all proposals?" -> GET /networks/{networkId}/proposals
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a invitation?" -> DELETE /invitations/{invitationId}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a member?" -> PATCH /networks/{networkId}/members/{memberId}
- "Partially update a node?" -> PATCH /networks/{networkId}/nodes/{nodeId}
- "Create a vote?" -> POST /networks/{networkId}/proposals/{proposalId}/votes
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
