---
name: gsmtasks-project-api
description: "GSMTasks Project API skill. Use when working with GSMTasks Project for account_roles, accounts, addons. Covers 261 endpoints."
version: 1.0.0
generator: lapsh
---

# GSMTasks Project API
API version: 2.4.13

## Auth
ApiKey Authorization in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /account_roles/ -- verify access
3. POST /account_roles/ -- create first account_roles

## Endpoints

261 endpoints across 55 groups. See references/api-spec.lap for full details.

### account_roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /account_roles/ |  |
| POST | /account_roles/ |  |
| GET | /account_roles/{id}/ |  |
| PUT | /account_roles/{id}/ |  |
| PATCH | /account_roles/{id}/ |  |
| DELETE | /account_roles/{id}/ |  |
| POST | /account_roles/{id}/activate/ |  |
| POST | /account_roles/{id}/notify/ |  |
| GET | /account_roles/{id}/token/ |  |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts/ |  |
| GET | /accounts/{id}/ |  |
| PUT | /accounts/{id}/ |  |
| PATCH | /accounts/{id}/ |  |
| GET | /accounts/{id}/braintree_customer/ |  |
| POST | /accounts/{id}/change_owner/ |  |
| GET | /accounts/{id}/managers/ |  |
| POST | /accounts/{id}/managers/ |  |
| DELETE | /accounts/{id}/managers/ |  |
| PUT | /accounts/{id}/stripe_attach_payment_method/ | Action to (re)set the account stripe customer and payment method to new values. |
| POST | /accounts/{id}/stripe_create_setup_intent/ | Action to start a new setup intent. |
| PUT | /accounts/{id}/stripe_create_setup_intent/ | Action to start a new setup intent. |
| PUT | /accounts/{id}/stripe_detach_payment_method/ | Detached payment method from the customer. |
| GET | /accounts/{id}/stripe_get_payment_method/ | Fetch a single payment method from stripe. |
| GET | /accounts/{id}/stripe_get_setup_attempt/ | Fetch a single setup intent |
| GET | /accounts/{id}/stripe_get_setup_intent/ | Fetch a single setup intent |
| GET | /accounts/{id}/stripe_payment_methods/ | Fetch all customer payment methods. |
| PUT | /accounts/{id}/stripe_set_default_payment_method/ | Action to set a payment method to default. |
| GET | /accounts/{id}/stripe_setup_intents/ | Fetch existing setup intents |
| GET | /accounts/{id}/workers/ |  |
| POST | /accounts/{id}/workers/ |  |
| DELETE | /accounts/{id}/workers/ |  |

### addons
| Method | Path | Description |
|--------|------|-------------|
| GET | /addons/ |  |
| GET | /addons/{id}/ |  |

### authenticate
| Method | Path | Description |
|--------|------|-------------|
| POST | /authenticate/ |  |

### billing
| Method | Path | Description |
|--------|------|-------------|
| GET | /billing/customers/ |  |
| POST | /billing/customers/ |  |
| GET | /billing/customers/{id}/ |  |
| PUT | /billing/customers/{id}/ |  |
| PATCH | /billing/customers/{id}/ |  |
| GET | /billing/customers/{id}/client_token/ |  |
| GET | /billing/invoices/ |  |
| GET | /billing/invoices/{id}/ |  |
| PUT | /billing/invoices/{id}/ |  |
| PATCH | /billing/invoices/{id}/ |  |
| POST | /billing/invoices/{id}/mark_as_paid/ |  |
| GET | /billing/stripe_payments/ |  |
| GET | /billing/stripe_payments/{id}/ |  |
| GET | /billing/transactions/ |  |
| GET | /billing/transactions/{id}/ |  |

### client_roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /client_roles/ |  |
| POST | /client_roles/ |  |
| GET | /client_roles/{id}/ |  |
| PUT | /client_roles/{id}/ |  |
| PATCH | /client_roles/{id}/ |  |
| POST | /client_roles/{id}/notify/ |  |

### clients
| Method | Path | Description |
|--------|------|-------------|
| GET | /clients/ |  |
| POST | /clients/ |  |
| GET | /clients/{id}/ |  |
| PUT | /clients/{id}/ |  |
| PATCH | /clients/{id}/ |  |

### configurations
| Method | Path | Description |
|--------|------|-------------|
| GET | /configurations/ |  |

### contact_address_exports
| Method | Path | Description |
|--------|------|-------------|
| GET | /contact_address_exports/ | This view has multiple renderer classes available: `json` and `xlsx`. In order to export the data as an excel file, just set query argument `format` to `xlsx`.When downloading `xlsx` format, use Accept header `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; version=...` |

### contact_address_import
| Method | Path | Description |
|--------|------|-------------|
| GET | /contact_address_import/ |  |
| POST | /contact_address_import/ |  |
| GET | /contact_address_import/{id}/ |  |

### contact_addresses
| Method | Path | Description |
|--------|------|-------------|
| GET | /contact_addresses/ |  |
| POST | /contact_addresses/ |  |
| GET | /contact_addresses/{id}/ |  |
| PUT | /contact_addresses/{id}/ |  |
| PATCH | /contact_addresses/{id}/ |  |

### devices
| Method | Path | Description |
|--------|------|-------------|
| GET | /devices/ |  |
| POST | /devices/ |  |
| GET | /devices/{id}/ |  |

### docs
| Method | Path | Description |
|--------|------|-------------|
| GET | /docs/schema/ | OpenApi3 schema for this API. Format can be selected via content negotiation. |

### documents
| Method | Path | Description |
|--------|------|-------------|
| GET | /documents/ |  |
| POST | /documents/ |  |
| GET | /documents/{id}/ |  |
| DELETE | /documents/{id}/ |  |
| POST | /documents/batch_delete/ | Available from version 2.4.2 |

### emails
| Method | Path | Description |
|--------|------|-------------|
| GET | /emails/ |  |
| POST | /emails/ |  |
| GET | /emails/{id}/ |  |
| PUT | /emails/{id}/ |  |
| PATCH | /emails/{id}/ |  |
| DELETE | /emails/{id}/ |  |
| POST | /emails/{id}/resend/ |  |

### exports
| Method | Path | Description |
|--------|------|-------------|
| GET | /exports/ |  |
| POST | /exports/ |  |
| GET | /exports/{id}/ |  |
| PUT | /exports/{id}/ |  |
| PATCH | /exports/{id}/ |  |
| DELETE | /exports/{id}/ |  |

### file_uploads
| Method | Path | Description |
|--------|------|-------------|
| GET | /file_uploads/ |  |
| POST | /file_uploads/ |  |
| GET | /file_uploads/{id}/ |  |

### formrules
| Method | Path | Description |
|--------|------|-------------|
| GET | /formrules/ |  |
| POST | /formrules/ |  |
| GET | /formrules/{id}/ |  |
| PUT | /formrules/{id}/ |  |
| PATCH | /formrules/{id}/ |  |
| DELETE | /formrules/{id}/ |  |

### integrations
| Method | Path | Description |
|--------|------|-------------|
| POST | /integrations/ |  |

### metafields
| Method | Path | Description |
|--------|------|-------------|
| GET | /metafields/ |  |
| POST | /metafields/ |  |
| GET | /metafields/{id}/ |  |
| PUT | /metafields/{id}/ |  |
| PATCH | /metafields/{id}/ |  |
| DELETE | /metafields/{id}/ |  |

### notification_templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /notification_templates/ |  |
| POST | /notification_templates/ |  |
| GET | /notification_templates/{id}/ |  |
| PUT | /notification_templates/{id}/ |  |
| PATCH | /notification_templates/{id}/ |  |
| DELETE | /notification_templates/{id}/ |  |
| POST | /notification_templates/{id}/render/ |  |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /notifications/ |  |
| POST | /notifications/ |  |
| GET | /notifications/{id}/ |  |

### orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /orders/ |  |
| POST | /orders/ |  |
| GET | /orders/{id}/ |  |
| PUT | /orders/{id}/ |  |
| PATCH | /orders/{id}/ |  |

### password_change
| Method | Path | Description |
|--------|------|-------------|
| POST | /password_change/ |  |

### password_reset
| Method | Path | Description |
|--------|------|-------------|
| POST | /password_reset/ |  |

### password_reset_confirm
| Method | Path | Description |
|--------|------|-------------|
| POST | /password_reset_confirm/ |  |

### push_notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /push_notifications/ |  |
| POST | /push_notifications/ |  |
| GET | /push_notifications/{id}/ |  |
| PUT | /push_notifications/{id}/ |  |
| PATCH | /push_notifications/{id}/ |  |
| DELETE | /push_notifications/{id}/ |  |
| POST | /push_notifications/{id}/resend/ |  |

### recurrences
| Method | Path | Description |
|--------|------|-------------|
| GET | /recurrences/ |  |
| POST | /recurrences/ |  |
| GET | /recurrences/{id}/ |  |
| PUT | /recurrences/{id}/ |  |
| PATCH | /recurrences/{id}/ |  |

### register
| Method | Path | Description |
|--------|------|-------------|
| POST | /register/ |  |

### reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /reports/tasks/states_count/ |  |

### reviews
| Method | Path | Description |
|--------|------|-------------|
| GET | /reviews/ |  |
| POST | /reviews/ |  |
| GET | /reviews/{id}/ |  |

### route_optimizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /route_optimizations/ |  |
| POST | /route_optimizations/ |  |
| GET | /route_optimizations/{id}/ |  |
| POST | /route_optimizations/{id}/commit/ |  |
| GET | /route_optimizations/{id}/results/ |  |
| GET | /route_optimizations/{id}/routes/ |  |
| POST | /route_optimizations/{id}/routes/ |  |
| POST | /route_optimizations/{id}/schedule/ |  |

### routes
| Method | Path | Description |
|--------|------|-------------|
| GET | /routes/ |  |
| POST | /routes/ |  |
| GET | /routes/{id}/ |  |
| PUT | /routes/{id}/ |  |
| PATCH | /routes/{id}/ |  |
| DELETE | /routes/{id}/ |  |

### scenes
| Method | Path | Description |
|--------|------|-------------|
| GET | /scenes/dashboard/ |  |
| GET | /scenes/order_list/ |  |
| GET | /scenes/recurrence_list/ |  |
| GET | /scenes/task_list/ |  |

### signatures
| Method | Path | Description |
|--------|------|-------------|
| GET | /signatures/ |  |
| POST | /signatures/ |  |
| GET | /signatures/{id}/ |  |
| DELETE | /signatures/{id}/ |  |
| POST | /signatures/batch_delete/ | Available from version 2.4.2 |

### sms
| Method | Path | Description |
|--------|------|-------------|
| GET | /sms/ |  |
| POST | /sms/ |  |
| GET | /sms/{id}/ |  |
| PUT | /sms/{id}/ |  |
| PATCH | /sms/{id}/ |  |
| DELETE | /sms/{id}/ |  |
| POST | /sms/{id}/resend/ |  |

### task_address_features
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_address_features/ |  |
| GET | /task_address_features/{id}/ |  |

### task_commands
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_commands/ |  |
| POST | /task_commands/ |  |
| GET | /task_commands/{id}/ |  |
| PUT | /task_commands/{id}/ |  |

### task_event_tracks
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_event_tracks/ |  |
| GET | /task_event_tracks/{id}/ |  |

### task_events
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_events/ | Mixin which allows the override of the filename being |
| GET | /task_events/{id}/ | Mixin which allows the override of the filename being |

### task_exports
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_exports/ | This view has multiple renderer classes available: `json` and `xlsx`. In order to export the data as an excel file, just set query argument `format` to `xlsx`.When downloading `xlsx` format, use Accept header `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; version=...` |

### task_forms
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_forms/ |  |
| POST | /task_forms/ |  |
| GET | /task_forms/{id}/ |  |
| PUT | /task_forms/{id}/ |  |
| PATCH | /task_forms/{id}/ |  |
| DELETE | /task_forms/{id}/ |  |

### task_import
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_import/ |  |
| POST | /task_import/ |  |
| GET | /task_import/{id}/ |  |

### task_import_mapping
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_import_mapping/ |  |
| POST | /task_import_mapping/ |  |
| GET | /task_import_mapping/{id}/ |  |

### task_metadatas
| Method | Path | Description |
|--------|------|-------------|
| GET | /task_metadatas/ |  |
| GET | /task_metadatas/{id}/ |  |

### tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks/ |  |
| POST | /tasks/ |  |
| GET | /tasks/{id}/ |  |
| PUT | /tasks/{id}/ |  |
| PATCH | /tasks/{id}/ |  |
| POST | /tasks/{id}/accept/ |  |
| POST | /tasks/{id}/account_change/ |  |
| POST | /tasks/{id}/activate/ |  |
| POST | /tasks/{id}/assign/ |  |
| POST | /tasks/{id}/cancel/ |  |
| POST | /tasks/{id}/complete/ |  |
| GET | /tasks/{id}/documents/ |  |
| GET | /tasks/{id}/events/ |  |
| POST | /tasks/{id}/fail/ |  |
| POST | /tasks/{id}/reject/ |  |
| GET | /tasks/{id}/signatures/ |  |
| POST | /tasks/{id}/transit/ |  |
| POST | /tasks/{id}/unaccept/ |  |
| POST | /tasks/{id}/unassign/ |  |
| POST | /tasks/reorder/ |  |
| POST | /tasks/reposition/ |  |

### time_location_features
| Method | Path | Description |
|--------|------|-------------|
| GET | /time_location_features/ |  |
| POST | /time_location_features/ |  |
| GET | /time_location_features/{id}/ |  |
| PUT | /time_location_features/{id}/ |  |
| PATCH | /time_location_features/{id}/ |  |
| DELETE | /time_location_features/{id}/ |  |

### time_locations
| Method | Path | Description |
|--------|------|-------------|
| GET | /time_locations/ |  |
| POST | /time_locations/ |  |
| GET | /time_locations/{id}/ |  |

### trackers
| Method | Path | Description |
|--------|------|-------------|
| GET | /trackers/ |  |
| POST | /trackers/ |  |
| GET | /trackers/{id}/ |  |
| PUT | /trackers/{id}/ |  |
| PATCH | /trackers/{id}/ |  |
| GET | /trackers/{id}/public/ |  |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/ |  |
| POST | /users/ |  |
| GET | /users/{id}/ |  |
| PUT | /users/{id}/ |  |
| PATCH | /users/{id}/ |  |
| DELETE | /users/{id}/ |  |
| POST | /users/{id}/activate/ |  |
| GET | /users/{id}/on_duty/ |  |
| PUT | /users/{id}/on_duty/ |  |
| DELETE | /users/{id}/on_duty/ |  |

### users_on_duty_log
| Method | Path | Description |
|--------|------|-------------|
| GET | /users_on_duty_log/ |  |
| POST | /users_on_duty_log/ |  |
| GET | /users_on_duty_log/{id}/ |  |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks/ |  |
| POST | /webhooks/ |  |
| GET | /webhooks/{id}/ |  |
| PUT | /webhooks/{id}/ |  |
| PATCH | /webhooks/{id}/ |  |
| DELETE | /webhooks/{id}/ |  |
| POST | /webhooks/{id}/active/ |  |
| POST | /webhooks/{id}/inactive/ |  |

### worker_features
| Method | Path | Description |
|--------|------|-------------|
| GET | /worker_features/ |  |
| GET | /worker_features/{user_id}/ |  |

### worker_tracks
| Method | Path | Description |
|--------|------|-------------|
| GET | /worker_tracks/ |  |

### working_state
| Method | Path | Description |
|--------|------|-------------|
| GET | /working_state/ |  |
| POST | /working_state/ |  |
| GET | /working_state/{id}/ |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search account_roles?" -> GET /account_roles/
- "Create a account_role?" -> POST /account_roles/
- "Get account_role details?" -> GET /account_roles/{id}/
- "Update a account_role?" -> PUT /account_roles/{id}/
- "Partially update a account_role?" -> PATCH /account_roles/{id}/
- "Delete a account_role?" -> DELETE /account_roles/{id}/
- "Create a activate?" -> POST /account_roles/{id}/activate/
- "Create a notify?" -> POST /account_roles/{id}/notify/
- "List all token?" -> GET /account_roles/{id}/token/
- "Search accounts?" -> GET /accounts/
- "Get account details?" -> GET /accounts/{id}/
- "Update a account?" -> PUT /accounts/{id}/
- "Partially update a account?" -> PATCH /accounts/{id}/
- "List all braintree_customer?" -> GET /accounts/{id}/braintree_customer/
- "Create a change_owner?" -> POST /accounts/{id}/change_owner/
- "List all managers?" -> GET /accounts/{id}/managers/
- "Create a manager?" -> POST /accounts/{id}/managers/
- "Create a stripe_create_setup_intent?" -> POST /accounts/{id}/stripe_create_setup_intent/
- "List all stripe_get_payment_method?" -> GET /accounts/{id}/stripe_get_payment_method/
- "List all stripe_get_setup_attempt?" -> GET /accounts/{id}/stripe_get_setup_attempt/
- "List all stripe_get_setup_intent?" -> GET /accounts/{id}/stripe_get_setup_intent/
- "List all stripe_payment_methods?" -> GET /accounts/{id}/stripe_payment_methods/
- "List all stripe_setup_intents?" -> GET /accounts/{id}/stripe_setup_intents/
- "List all workers?" -> GET /accounts/{id}/workers/
- "Create a worker?" -> POST /accounts/{id}/workers/
- "List all addons?" -> GET /addons/
- "Get addon details?" -> GET /addons/{id}/
- "Create a authenticate?" -> POST /authenticate/
- "List all customers?" -> GET /billing/customers/
- "Create a customer?" -> POST /billing/customers/
- "Get customer details?" -> GET /billing/customers/{id}/
- "Update a customer?" -> PUT /billing/customers/{id}/
- "Partially update a customer?" -> PATCH /billing/customers/{id}/
- "List all client_token?" -> GET /billing/customers/{id}/client_token/
- "List all invoices?" -> GET /billing/invoices/
- "Get invoice details?" -> GET /billing/invoices/{id}/
- "Update a invoice?" -> PUT /billing/invoices/{id}/
- "Partially update a invoice?" -> PATCH /billing/invoices/{id}/
- "Create a mark_as_paid?" -> POST /billing/invoices/{id}/mark_as_paid/
- "List all stripe_payments?" -> GET /billing/stripe_payments/
- "Get stripe_payment details?" -> GET /billing/stripe_payments/{id}/
- "List all transactions?" -> GET /billing/transactions/
- "Get transaction details?" -> GET /billing/transactions/{id}/
- "Search client_roles?" -> GET /client_roles/
- "Create a client_role?" -> POST /client_roles/
- "Get client_role details?" -> GET /client_roles/{id}/
- "Update a client_role?" -> PUT /client_roles/{id}/
- "Partially update a client_role?" -> PATCH /client_roles/{id}/
- "Create a notify?" -> POST /client_roles/{id}/notify/
- "Search clients?" -> GET /clients/
- "Create a client?" -> POST /clients/
- "Get client details?" -> GET /clients/{id}/
- "Update a client?" -> PUT /clients/{id}/
- "Partially update a client?" -> PATCH /clients/{id}/
- "List all configurations?" -> GET /configurations/
- "Search contact_address_exports?" -> GET /contact_address_exports/
- "List all contact_address_import?" -> GET /contact_address_import/
- "Create a contact_address_import?" -> POST /contact_address_import/
- "Get contact_address_import details?" -> GET /contact_address_import/{id}/
- "Search contact_addresses?" -> GET /contact_addresses/
- "Create a contact_address?" -> POST /contact_addresses/
- "Get contact_address details?" -> GET /contact_addresses/{id}/
- "Update a contact_address?" -> PUT /contact_addresses/{id}/
- "Partially update a contact_address?" -> PATCH /contact_addresses/{id}/
- "Search devices?" -> GET /devices/
- "Create a device?" -> POST /devices/
- "Get device details?" -> GET /devices/{id}/
- "List all schema?" -> GET /docs/schema/
- "Search documents?" -> GET /documents/
- "Create a document?" -> POST /documents/
- "Get document details?" -> GET /documents/{id}/
- "Delete a document?" -> DELETE /documents/{id}/
- "Create a batch_delete?" -> POST /documents/batch_delete/
- "Search emails?" -> GET /emails/
- "Create a email?" -> POST /emails/
- "Get email details?" -> GET /emails/{id}/
- "Update a email?" -> PUT /emails/{id}/
- "Partially update a email?" -> PATCH /emails/{id}/
- "Delete a email?" -> DELETE /emails/{id}/
- "Create a resend?" -> POST /emails/{id}/resend/
- "List all exports?" -> GET /exports/
- "Create a export?" -> POST /exports/
- "Get export details?" -> GET /exports/{id}/
- "Update a export?" -> PUT /exports/{id}/
- "Partially update a export?" -> PATCH /exports/{id}/
- "Delete a export?" -> DELETE /exports/{id}/
- "List all file_uploads?" -> GET /file_uploads/
- "Create a file_upload?" -> POST /file_uploads/
- "Get file_upload details?" -> GET /file_uploads/{id}/
- "Search formrules?" -> GET /formrules/
- "Create a formrule?" -> POST /formrules/
- "Get formrule details?" -> GET /formrules/{id}/
- "Update a formrule?" -> PUT /formrules/{id}/
- "Partially update a formrule?" -> PATCH /formrules/{id}/
- "Delete a formrule?" -> DELETE /formrules/{id}/
- "Create a integration?" -> POST /integrations/
- "Search metafields?" -> GET /metafields/
- "Create a metafield?" -> POST /metafields/
- "Get metafield details?" -> GET /metafields/{id}/
- "Update a metafield?" -> PUT /metafields/{id}/
- "Partially update a metafield?" -> PATCH /metafields/{id}/
- "Delete a metafield?" -> DELETE /metafields/{id}/
- "Search notification_templates?" -> GET /notification_templates/
- "Create a notification_template?" -> POST /notification_templates/
- "Get notification_template details?" -> GET /notification_templates/{id}/
- "Update a notification_template?" -> PUT /notification_templates/{id}/
- "Partially update a notification_template?" -> PATCH /notification_templates/{id}/
- "Delete a notification_template?" -> DELETE /notification_templates/{id}/
- "Create a render?" -> POST /notification_templates/{id}/render/
- "Search notifications?" -> GET /notifications/
- "Create a notification?" -> POST /notifications/
- "Get notification details?" -> GET /notifications/{id}/
- "Search orders?" -> GET /orders/
- "Create a order?" -> POST /orders/
- "Get order details?" -> GET /orders/{id}/
- "Update a order?" -> PUT /orders/{id}/
- "Partially update a order?" -> PATCH /orders/{id}/
- "Create a password_change?" -> POST /password_change/
- "Create a password_reset?" -> POST /password_reset/
- "Create a password_reset_confirm?" -> POST /password_reset_confirm/
- "Search push_notifications?" -> GET /push_notifications/
- "Create a push_notification?" -> POST /push_notifications/
- "Get push_notification details?" -> GET /push_notifications/{id}/
- "Update a push_notification?" -> PUT /push_notifications/{id}/
- "Partially update a push_notification?" -> PATCH /push_notifications/{id}/
- "Delete a push_notification?" -> DELETE /push_notifications/{id}/
- "Create a resend?" -> POST /push_notifications/{id}/resend/
- "Search recurrences?" -> GET /recurrences/
- "Create a recurrence?" -> POST /recurrences/
- "Get recurrence details?" -> GET /recurrences/{id}/
- "Update a recurrence?" -> PUT /recurrences/{id}/
- "Partially update a recurrence?" -> PATCH /recurrences/{id}/
- "Create a register?" -> POST /register/
- "List all states_count?" -> GET /reports/tasks/states_count/
- "List all reviews?" -> GET /reviews/
- "Create a review?" -> POST /reviews/
- "Get review details?" -> GET /reviews/{id}/
- "List all route_optimizations?" -> GET /route_optimizations/
- "Create a route_optimization?" -> POST /route_optimizations/
- "Get route_optimization details?" -> GET /route_optimizations/{id}/
- "Create a commit?" -> POST /route_optimizations/{id}/commit/
- "List all results?" -> GET /route_optimizations/{id}/results/
- "List all routes?" -> GET /route_optimizations/{id}/routes/
- "Create a route?" -> POST /route_optimizations/{id}/routes/
- "Create a schedule?" -> POST /route_optimizations/{id}/schedule/
- "List all routes?" -> GET /routes/
- "Create a route?" -> POST /routes/
- "Get route details?" -> GET /routes/{id}/
- "Update a route?" -> PUT /routes/{id}/
- "Partially update a route?" -> PATCH /routes/{id}/
- "Delete a route?" -> DELETE /routes/{id}/
- "Search dashboard?" -> GET /scenes/dashboard/
- "Search order_list?" -> GET /scenes/order_list/
- "Search recurrence_list?" -> GET /scenes/recurrence_list/
- "Search task_list?" -> GET /scenes/task_list/
- "Search signatures?" -> GET /signatures/
- "Create a signature?" -> POST /signatures/
- "Get signature details?" -> GET /signatures/{id}/
- "Delete a signature?" -> DELETE /signatures/{id}/
- "Create a batch_delete?" -> POST /signatures/batch_delete/
- "Search sms?" -> GET /sms/
- "Create a sm?" -> POST /sms/
- "Get sm details?" -> GET /sms/{id}/
- "Update a sm?" -> PUT /sms/{id}/
- "Partially update a sm?" -> PATCH /sms/{id}/
- "Delete a sm?" -> DELETE /sms/{id}/
- "Create a resend?" -> POST /sms/{id}/resend/
- "List all task_address_features?" -> GET /task_address_features/
- "Get task_address_feature details?" -> GET /task_address_features/{id}/
- "List all task_commands?" -> GET /task_commands/
- "Create a task_command?" -> POST /task_commands/
- "Get task_command details?" -> GET /task_commands/{id}/
- "Update a task_command?" -> PUT /task_commands/{id}/
- "List all task_event_tracks?" -> GET /task_event_tracks/
- "Get task_event_track details?" -> GET /task_event_tracks/{id}/
- "List all task_events?" -> GET /task_events/
- "Get task_event details?" -> GET /task_events/{id}/
- "Search task_exports?" -> GET /task_exports/
- "List all task_forms?" -> GET /task_forms/
- "Create a task_form?" -> POST /task_forms/
- "Get task_form details?" -> GET /task_forms/{id}/
- "Update a task_form?" -> PUT /task_forms/{id}/
- "Partially update a task_form?" -> PATCH /task_forms/{id}/
- "Delete a task_form?" -> DELETE /task_forms/{id}/
- "List all task_import?" -> GET /task_import/
- "Create a task_import?" -> POST /task_import/
- "Get task_import details?" -> GET /task_import/{id}/
- "List all task_import_mapping?" -> GET /task_import_mapping/
- "Create a task_import_mapping?" -> POST /task_import_mapping/
- "Get task_import_mapping details?" -> GET /task_import_mapping/{id}/
- "List all task_metadatas?" -> GET /task_metadatas/
- "Get task_metadata details?" -> GET /task_metadatas/{id}/
- "Search tasks?" -> GET /tasks/
- "Create a task?" -> POST /tasks/
- "Get task details?" -> GET /tasks/{id}/
- "Update a task?" -> PUT /tasks/{id}/
- "Partially update a task?" -> PATCH /tasks/{id}/
- "Create a accept?" -> POST /tasks/{id}/accept/
- "Create a account_change?" -> POST /tasks/{id}/account_change/
- "Create a activate?" -> POST /tasks/{id}/activate/
- "Create a assign?" -> POST /tasks/{id}/assign/
- "Create a cancel?" -> POST /tasks/{id}/cancel/
- "Create a complete?" -> POST /tasks/{id}/complete/
- "List all documents?" -> GET /tasks/{id}/documents/
- "List all events?" -> GET /tasks/{id}/events/
- "Create a fail?" -> POST /tasks/{id}/fail/
- "Create a reject?" -> POST /tasks/{id}/reject/
- "List all signatures?" -> GET /tasks/{id}/signatures/
- "Create a transit?" -> POST /tasks/{id}/transit/
- "Create a unaccept?" -> POST /tasks/{id}/unaccept/
- "Create a unassign?" -> POST /tasks/{id}/unassign/
- "Create a reorder?" -> POST /tasks/reorder/
- "Create a reposition?" -> POST /tasks/reposition/
- "List all time_location_features?" -> GET /time_location_features/
- "Create a time_location_feature?" -> POST /time_location_features/
- "Get time_location_feature details?" -> GET /time_location_features/{id}/
- "Update a time_location_feature?" -> PUT /time_location_features/{id}/
- "Partially update a time_location_feature?" -> PATCH /time_location_features/{id}/
- "Delete a time_location_feature?" -> DELETE /time_location_features/{id}/
- "List all time_locations?" -> GET /time_locations/
- "Create a time_location?" -> POST /time_locations/
- "Get time_location details?" -> GET /time_locations/{id}/
- "List all trackers?" -> GET /trackers/
- "Create a tracker?" -> POST /trackers/
- "Get tracker details?" -> GET /trackers/{id}/
- "Update a tracker?" -> PUT /trackers/{id}/
- "Partially update a tracker?" -> PATCH /trackers/{id}/
- "List all public?" -> GET /trackers/{id}/public/
- "Search users?" -> GET /users/
- "Create a user?" -> POST /users/
- "Get user details?" -> GET /users/{id}/
- "Update a user?" -> PUT /users/{id}/
- "Partially update a user?" -> PATCH /users/{id}/
- "Delete a user?" -> DELETE /users/{id}/
- "Create a activate?" -> POST /users/{id}/activate/
- "List all on_duty?" -> GET /users/{id}/on_duty/
- "List all users_on_duty_log?" -> GET /users_on_duty_log/
- "Create a users_on_duty_log?" -> POST /users_on_duty_log/
- "Get users_on_duty_log details?" -> GET /users_on_duty_log/{id}/
- "Search webhooks?" -> GET /webhooks/
- "Create a webhook?" -> POST /webhooks/
- "Get webhook details?" -> GET /webhooks/{id}/
- "Update a webhook?" -> PUT /webhooks/{id}/
- "Partially update a webhook?" -> PATCH /webhooks/{id}/
- "Delete a webhook?" -> DELETE /webhooks/{id}/
- "Create a active?" -> POST /webhooks/{id}/active/
- "Create a inactive?" -> POST /webhooks/{id}/inactive/
- "List all worker_features?" -> GET /worker_features/
- "Get worker_feature details?" -> GET /worker_features/{user_id}/
- "List all worker_tracks?" -> GET /worker_tracks/
- "List all working_state?" -> GET /working_state/
- "Create a working_state?" -> POST /working_state/
- "Get working_state details?" -> GET /working_state/{id}/
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
