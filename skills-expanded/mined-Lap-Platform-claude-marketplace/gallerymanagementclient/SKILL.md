---
name: gallerymanagementclient
description: "GalleryManagementClient API skill. Use when working with GalleryManagementClient for subscriptions. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# GalleryManagementClient
API version: 2015-04-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems -- verify access
3. POST /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems -- create first galleryItems

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems | Lists gallery items. |
| POST | /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems | Uploads a provider gallery item to the storage. |
| GET | /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems/{galleryItemName} | Get a specific gallery item. |
| DELETE | /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems/{galleryItemName} | Delete a specific gallery item. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all galleryItems?" -> GET /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems
- "Create a galleryItem?" -> POST /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems
- "Get galleryItem details?" -> GET /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems/{galleryItemName}
- "Delete a galleryItem?" -> DELETE /subscriptions/{subscriptionId}/providers/microsoft.gallery.admin/galleryItems/{galleryItemName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
