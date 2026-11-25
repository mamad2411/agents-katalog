---
name: docspring-api
description: "DocSpring API skill. Use when working with DocSpring for authentication, combined_submissions, custom_files. Covers 40 endpoints."
version: 1.0.0
generator: lapsh
---

# DocSpring API
API version: v1

## Auth
basic

## Base URL
https://sync.api.docspring.com/api/v1

## Setup
1. Configure auth: basic
2. GET /authentication -- verify access
3. POST /combined_submissions -- create first combined_submissions

## Endpoints

40 endpoints across 10 groups. See references/api-spec.lap for full details.

### authentication
| Method | Path | Description |
|--------|------|-------------|
| GET | /authentication | Test authentication |

### combined_submissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /combined_submissions | Get a list of all combined submissions |
| POST | /combined_submissions | Merge submission PDFs, template PDFs, or custom files |
| GET | /combined_submissions/{combined_submission_id} | Check the status of a combined submission (merged PDFs) |
| DELETE | /combined_submissions/{combined_submission_id} | Expire a combined submission |

### custom_files
| Method | Path | Description |
|--------|------|-------------|
| POST | /custom_files | Create a new custom file from a cached S3 upload |

### uploads
| Method | Path | Description |
|--------|------|-------------|
| GET | /uploads/presign | Get a presigned S3 URL for direct file upload |

### folders
| Method | Path | Description |
|--------|------|-------------|
| GET | /folders/ | Get a list of all folders |
| POST | /folders/ | Create a folder |
| POST | /folders/{folder_id}/move | Move a folder |
| POST | /folders/{folder_id}/rename | Rename a folder |
| DELETE | /folders/{folder_id} | Delete a folder |

### data_requests
| Method | Path | Description |
|--------|------|-------------|
| POST | /data_requests/{data_request_id}/events | Create a new event for emailing a signee a request for signature |
| POST | /data_requests/{data_request_id}/tokens | Create a new data request token for form authentication |
| GET | /data_requests/{data_request_id} | Look up a submission data request |
| PUT | /data_requests/{data_request_id} | Update a submission data request |

### submissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /submissions/batches | Generate multiple PDFs |
| GET | /submissions/batches/{submission_batch_id} | Check the status of a submission batch job |
| GET | /submissions/{submission_id} | Check the status of a PDF |
| DELETE | /submissions/{submission_id} | Expire a PDF submission |
| POST | /submissions/{submission_id}/generate_preview | Generate a preview PDF for partially completed data requests |
| GET | /submissions | List all submissions |

### templates
| Method | Path | Description |
|--------|------|-------------|
| POST | /templates/{template_id}/submissions | Generate a PDF |
| GET | /templates/{template_id}/submissions | List all submissions for a given template |
| GET | /templates | Get a list of all templates |
| POST | /templates | Create a new PDF template with a form POST file upload |
| GET | /templates/{template_id} | Check the status of an uploaded template |
| PUT | /templates/{template_id} | Update a Template |
| DELETE | /templates/{template_id} | Delete a template |
| POST | /templates/{template_id}/publish_version | Publish a template version |
| POST | /templates/{template_id}/restore_version | Restore a template version |
| GET | /templates/{template_id}?full=true | Fetch the full attributes for a PDF template |
| PUT | /templates/{template_id}?endpoint_variant=update_template_pdf_with_form_post | Update a template's document with a form POST file upload |
| PUT | /templates/{template_id}?endpoint_variant=update_template_pdf_with_cached_upload | Update a template's document with a cached S3 file upload |
| PUT | /templates/{template_id}/add_fields | Add new fields to a Template |
| POST | /templates/{template_id}/move | Move Template to folder |
| POST | /templates/{template_id}/copy | Copy a template |
| GET | /templates/{template_id}/schema | Fetch the JSON schema for a template |

### templates?endpoint_variant=create_html_template
| Method | Path | Description |
|--------|------|-------------|
| POST | /templates?endpoint_variant=create_html_template | Create a new HTML template |

### templates?endpoint_variant=create_template_from_cached_upload
| Method | Path | Description |
|--------|------|-------------|
| POST | /templates?endpoint_variant=create_template_from_cached_upload | Create a new PDF template from a cached S3 file upload |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all authentication?" -> GET /authentication
- "List all combined_submissions?" -> GET /combined_submissions
- "Create a combined_submission?" -> POST /combined_submissions
- "Get combined_submission details?" -> GET /combined_submissions/{combined_submission_id}
- "Delete a combined_submission?" -> DELETE /combined_submissions/{combined_submission_id}
- "Create a custom_file?" -> POST /custom_files
- "List all presign?" -> GET /uploads/presign
- "List all folders?" -> GET /folders/
- "Create a folder?" -> POST /folders/
- "Create a move?" -> POST /folders/{folder_id}/move
- "Create a rename?" -> POST /folders/{folder_id}/rename
- "Delete a folder?" -> DELETE /folders/{folder_id}
- "Create a event?" -> POST /data_requests/{data_request_id}/events
- "Create a token?" -> POST /data_requests/{data_request_id}/tokens
- "Get data_request details?" -> GET /data_requests/{data_request_id}
- "Update a data_request?" -> PUT /data_requests/{data_request_id}
- "Create a batche?" -> POST /submissions/batches
- "Get batche details?" -> GET /submissions/batches/{submission_batch_id}
- "Create a submission?" -> POST /templates/{template_id}/submissions
- "List all submissions?" -> GET /templates/{template_id}/submissions
- "Get submission details?" -> GET /submissions/{submission_id}
- "Delete a submission?" -> DELETE /submissions/{submission_id}
- "Create a generate_preview?" -> POST /submissions/{submission_id}/generate_preview
- "List all submissions?" -> GET /submissions
- "Search templates?" -> GET /templates
- "Create a template?" -> POST /templates
- "Create a templates?endpoint_variant=create_html_template?" -> POST /templates?endpoint_variant=create_html_template
- "Create a templates?endpoint_variant=create_template_from_cached_upload?" -> POST /templates?endpoint_variant=create_template_from_cached_upload
- "Get template details?" -> GET /templates/{template_id}
- "Update a template?" -> PUT /templates/{template_id}
- "Delete a template?" -> DELETE /templates/{template_id}
- "Create a publish_version?" -> POST /templates/{template_id}/publish_version
- "Create a restore_version?" -> POST /templates/{template_id}/restore_version
- "Get template details?" -> GET /templates/{template_id}?full=true
- "Update a template?" -> PUT /templates/{template_id}?endpoint_variant=update_template_pdf_with_form_post
- "Update a template?" -> PUT /templates/{template_id}?endpoint_variant=update_template_pdf_with_cached_upload
- "Create a move?" -> POST /templates/{template_id}/move
- "Create a copy?" -> POST /templates/{template_id}/copy
- "List all schema?" -> GET /templates/{template_id}/schema
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
