---
name: amazon-cloudsearch-domain
description: "Amazon CloudSearch Domain API skill. Use when working with Amazon CloudSearch Domain for 2013-01-01. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon CloudSearch Domain
API version: 2013-01-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /2013-01-01/search?format=sdk&pretty=true -- verify access
3. POST /2013-01-01/documents/batch?format=sdk -- create first batch?format=sdk

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### 2013-01-01
| Method | Path | Description |
|--------|------|-------------|
| GET | /2013-01-01/search?format=sdk&pretty=true | Retrieves a list of documents that match the specified search criteria. How you specify the search criteria depends on which query parser you use. Amazon CloudSearch supports four query parsers:  simple: search all text and text-array fields for the specified string. Search for phrases, individual terms, and prefixes.  structured: search specific fields, construct compound queries using Boolean operators, and use advanced features such as term boosting and proximity searching. lucene: specify search criteria using the Apache Lucene query parser syntax. dismax: specify search criteria using the simplified subset of the Apache Lucene query parser syntax defined by the DisMax query parser.  For more information, see Searching Your Data in the Amazon CloudSearch Developer Guide. The endpoint for submitting Search requests is domain-specific. You submit search requests to a domain's search endpoint. To get the search endpoint for your domain, use the Amazon CloudSearch configuration service DescribeDomains action. A domain's endpoints are also displayed on the domain dashboard in the Amazon CloudSearch console. |
| GET | /2013-01-01/suggest?format=sdk&pretty=true | Retrieves autocomplete suggestions for a partial query string. You can use suggestions enable you to display likely matches before users finish typing. In Amazon CloudSearch, suggestions are based on the contents of a particular text field. When you request suggestions, Amazon CloudSearch finds all of the documents whose values in the suggester field start with the specified query string. The beginning of the field must match the query string to be considered a match.  For more information about configuring suggesters and retrieving suggestions, see Getting Suggestions in the Amazon CloudSearch Developer Guide.  The endpoint for submitting Suggest requests is domain-specific. You submit suggest requests to a domain's search endpoint. To get the search endpoint for your domain, use the Amazon CloudSearch configuration service DescribeDomains action. A domain's endpoints are also displayed on the domain dashboard in the Amazon CloudSearch console. |
| POST | /2013-01-01/documents/batch?format=sdk | Posts a batch of documents to a search domain for indexing. A document batch is a collection of add and delete operations that represent the documents you want to add, update, or delete from your domain. Batches can be described in either JSON or XML. Each item that you want Amazon CloudSearch to return as a search result (such as a product) is represented as a document. Every document has a unique ID and one or more fields that contain the data that you want to search and return in results. Individual documents cannot contain more than 1 MB of data. The entire batch cannot exceed 5 MB. To get the best possible upload performance, group add and delete operations in batches that are close the 5 MB limit. Submitting a large volume of single-document batches can overload a domain's document service.  The endpoint for submitting UploadDocuments requests is domain-specific. To get the document endpoint for your domain, use the Amazon CloudSearch configuration service DescribeDomains action. A domain's endpoints are also displayed on the domain dashboard in the Amazon CloudSearch console.  For more information about formatting your data for Amazon CloudSearch, see Preparing Your Data in the Amazon CloudSearch Developer Guide. For more information about uploading data for indexing, see Uploading Data in the Amazon CloudSearch Developer Guide. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?format=sdk&pretty=true?" -> GET /2013-01-01/search?format=sdk&pretty=true
- "Search suggest?format=sdk&pretty=true?" -> GET /2013-01-01/suggest?format=sdk&pretty=true
- "Create a batch?format=sdk?" -> POST /2013-01-01/documents/batch?format=sdk
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object
- Error responses use types: DocumentServiceException, SearchException

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
