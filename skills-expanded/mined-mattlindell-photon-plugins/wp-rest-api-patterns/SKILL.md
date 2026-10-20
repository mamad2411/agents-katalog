---
name: wp-rest-api-patterns
description: WordPress REST API patterns — registering custom endpoints, permission callbacks, schema validation, response formatting, extending existing endpoints, and webhook handling. Use when building or consuming WP REST API endpoints.
---

# WordPress REST API Patterns

Patterns for building robust REST APIs using the WordPress REST API infrastructure. Covers endpoint registration, permission callbacks, JSON Schema validation, response formatting, extending core endpoints, CRUD controller classes, webhooks, error formatting, and cursor-based pagination.

## When to Use This Skill

- Registering custom WP REST API endpoints with `register_rest_route`
- Implementing permission callbacks for public, authenticated, or capability-based access
- Validating and sanitizing request arguments with JSON Schema
- Formatting responses with `WP_REST_Response` including pagination headers
- Extending existing WordPress REST endpoints with `register_rest_field`
- Building a full CRUD controller by extending `WP_REST_Controller`
- Receiving and validating webhooks through a REST endpoint
- Implementing RFC 7807 Problem Details error responses
- Adding cursor-based pagination to REST endpoints

## Core Concepts

- **Always declare `permission_callback`**: Omitting it triggers a `_doing_it_wrong` notice and defaults to public access
- **Schema-first design**: Define your request validation and response shape before writing business logic
- **Authentication != Authorization**: Auth confirms identity; authorization checks permissions. Always implement both layers
- **Consistent error formatting**: Use RFC 7807 Problem Details for machine-readable errors across all endpoints
- **Pagination by default**: Never return unbounded collections -- always paginate

## Quick Start

Register a simple endpoint:

```php
add_action('rest_api_init', function () {
    register_rest_route('myplugin/v1', '/items', [
        'methods'             => WP_REST_Server::READABLE,
        'callback'            => function (WP_REST_Request $request) {
            return new WP_REST_Response(['items' => []], 200);
        },
        'permission_callback' => '__return_true',
    ]);
});
```

---

### Pattern 1: Custom Endpoint with Full Validation

Register an endpoint with namespace, versioning, methods, permission checks, and argument validation/sanitization.

```php
<?php
declare(strict_types=1);

add_action('rest_api_init', function (): void {
    register_rest_route('myplugin/v1', '/events', [
        [
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => 'myplugin_get_events',
            'permission_callback' => '__return_true',
            'args'                => [
                'status' => [
                    'required'          => false,
                    'default'           => 'published',
                    'type'              => 'string',
                    'enum'              => ['draft', 'published', 'cancelled'],
                    'description'       => 'Filter events by status.',
                    'validate_callback' => function ($value, $request, $param): bool {
                        return in_array($value, ['draft', 'published', 'cancelled'], true);
                    },
                    'sanitize_callback' => function ($value, $request, $param): string {
                        return sanitize_text_field($value);
                    },
                ],
                'per_page' => [
                    'required' => false, 'default' => 10, 'type' => 'integer',
                    'minimum'  => 1,     'maximum' => 100,
                    'sanitize_callback' => 'absint',
                ],
                'page' => [
                    'required' => false, 'default' => 1, 'type' => 'integer',
                    'minimum'  => 1,
                    'sanitize_callback' => 'absint',
                ],
            ],
        ],
        [
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => 'myplugin_create_event',
            'permission_callback' => 'myplugin_can_manage_events',
            'args'                => [
                'title' => [
                    'required'          => true,
                    'type'              => 'string',
                    'minLength'         => 1,
                    'maxLength'         => 200,
                    'sanitize_callback' => 'sanitize_text_field',
                ],
                'date' => [
                    'required'          => true,
                    'type'              => 'string',
                    'format'            => 'date-time',
                    'validate_callback' => function ($value): bool {
                        return (bool) strtotime($value);
                    },
                    'sanitize_callback' => 'sanitize_text_field',
                ],
                'description' => [
                    'required'          => false,
                    'type'              => 'string',
                    'default'           => '',
                    'sanitize_callback' => 'wp_kses_post',
                ],
            ],
        ],
    ]);

    // Single-item route: GET, PUT/PATCH, DELETE with URL param (?P<id>\d+)
    register_rest_route('myplugin/v1', '/events/(?P<id>\d+)', [
        [
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => 'myplugin_get_event',
            'permission_callback' => '__return_true',
            'args'                => [
                'id' => [
                    'required'          => true,
                    'type'              => 'integer',
                    'validate_callback' => function ($value): bool {
                        return is_numeric($value) && (int) $value > 0;
                    },
                    'sanitize_callback' => 'absint',
                ],
            ],
        ],
        // EDITABLE + DELETABLE handlers follow the same structure
        // with their own permission_callback and args
    ]);
});
```

### Pattern 2: Permission Callback Patterns

Three levels of access control for REST endpoints.

```php
<?php
declare(strict_types=1);

/**
 * Public endpoint -- no authentication required.
 * Still MUST declare permission_callback (omitting it triggers a _doing_it_wrong notice).
 */
function myplugin_public_access(): bool {
    return true;
}
// Or use: 'permission_callback' => '__return_true'

/**
 * Logged-in users only -- any authenticated user.
 */
function myplugin_authenticated_access(): bool {
    return is_user_logged_in();
}

/**
 * Capability-based -- check a specific WordPress capability.
 */
function myplugin_can_manage_events(): bool {
    return current_user_can('edit_posts');
}

/**
 * Resource-owner check -- only the author can modify their own resource.
 */
function myplugin_can_edit_own_event(WP_REST_Request $request): bool {
    $event_id = (int) $request->get_param('id');
    $event    = get_post($event_id);

    if (! $event || $event->post_type !== 'event') {
        return false;
    }

    return current_user_can('edit_post', $event_id);
}

/**
 * Combined check -- capability plus custom condition.
 */
function myplugin_admin_or_api_key(WP_REST_Request $request): bool {
    // Admins always have access
    if (current_user_can('manage_options')) {
        return true;
    }

    // Fall back to API key validation
    $api_key = $request->get_header('X-API-Key');
    if (! $api_key) {
        return false;
    }

    $valid_key = get_option('myplugin_api_key');

    return hash_equals($valid_key, $api_key);
}
```

### Pattern 3: Schema Validation on Args

Define a JSON Schema for your endpoint args. WordPress validates incoming requests against the schema automatically when `type`, `format`, `enum`, `minimum`, `maximum`, `minLength`, `maxLength`, and other JSON Schema keywords are provided.

```php
<?php
declare(strict_types=1);

add_action('rest_api_init', function (): void {
    register_rest_route('myplugin/v1', '/contacts', [
        'methods'             => WP_REST_Server::CREATABLE,
        'callback'            => 'myplugin_create_contact',
        'permission_callback' => function (): bool {
            return current_user_can('edit_posts');
        },
        'args'                => myplugin_contact_args_schema(),
    ]);
});

function myplugin_contact_args_schema(): array {
    return [
        'name' => [
            'required'    => true,
            'type'        => 'string',
            'minLength'   => 2,
            'maxLength'   => 100,
            'description' => 'Full name of the contact.',
            'sanitize_callback' => 'sanitize_text_field',
        ],
        'email' => [
            'required'    => true,
            'type'        => 'string',
            'format'      => 'email',
            'description' => 'Contact email address.',
            'sanitize_callback' => 'sanitize_email',
        ],
        'phone' => [
            'required'    => false,
            'type'        => 'string',
            'pattern'     => '^\+?[1-9]\d{1,14}$', // E.164 format
            'description' => 'Phone number in E.164 format.',
            'sanitize_callback' => 'sanitize_text_field',
        ],
        'type' => [
            'required'    => true,
            'type'        => 'string',
            'enum'        => ['lead', 'customer', 'partner'],
            'description' => 'Contact classification.',
        ],
        'tags' => [
            'required'    => false,
            'type'        => 'array',
            'default'     => [],
            'items'       => [
                'type'      => 'string',
                'minLength' => 1,
                'maxLength' => 50,
            ],
            'maxItems'    => 10,
            'uniqueItems' => true,
            'description' => 'Tags for categorizing the contact.',
            'sanitize_callback' => function (array $tags): array {
                return array_map('sanitize_text_field', $tags);
            },
        ],
        // Nested objects use 'type' => 'object' with 'properties' and 'additionalProperties' => false
    ];
}

// In the callback, all args are already validated and sanitized by WordPress.
// Use $request->get_param('name') etc. to access clean values.
```

### Pattern 4: Response Formatting with WP_REST_Response

Use `WP_REST_Response` for proper status codes, headers, and consistent response shapes.

```php
<?php
declare(strict_types=1);

/**
 * Format a single resource response.
 */
function myplugin_get_event(WP_REST_Request $request): WP_REST_Response {
    $event_id = (int) $request->get_param('id');
    $post     = get_post($event_id);

    if (! $post || $post->post_type !== 'event') {
        return new WP_REST_Response([
            'code'    => 'event_not_found',
            'message' => 'The requested event does not exist.',
            'data'    => ['status' => 404],
        ], 404);
    }

    $response = new WP_REST_Response(myplugin_format_event($post), 200);

    // Add cache headers
    $response->header('Cache-Control', 'max-age=300, public');
    $response->header('X-Event-Status', get_post_meta($post->ID, '_event_status', true));

    return $response;
}

/**
 * Collection response with pagination headers.
 */
function myplugin_get_events(WP_REST_Request $request): WP_REST_Response {
    $per_page = (int) $request->get_param('per_page');
    $page     = (int) $request->get_param('page');
    $status   = $request->get_param('status');

    $query = new WP_Query([
        'post_type'      => 'event',
        'post_status'    => 'publish',
        'posts_per_page' => $per_page,
        'paged'          => $page,
        'meta_query'     => $status ? [
            [
                'key'   => '_event_status',
                'value' => $status,
            ],
        ] : [],
    ]);

    $events = array_map('myplugin_format_event', $query->posts);
    $total  = (int) $query->found_posts;
    $pages  = (int) $query->max_num_pages;

    $response = new WP_REST_Response($events, 200);

    // Standard WP REST pagination headers
    $response->header('X-WP-Total', (string) $total);
    $response->header('X-WP-TotalPages', (string) $pages);

    // Link headers for next/prev navigation
    $base = rest_url('myplugin/v1/events');
    if ($page < $pages) {
        $response->link_header('next', add_query_arg(['page' => $page + 1, 'per_page' => $per_page], $base));
    }
    if ($page > 1) {
        $response->link_header('prev', add_query_arg(['page' => $page - 1, 'per_page' => $per_page], $base));
    }

    return $response;
}

/**
 * Format a single event for API output.
 * Keep this as a standalone function so all endpoints return consistent shapes.
 */
function myplugin_format_event(WP_Post $post): array {
    return [
        'id'          => $post->ID,
        'title'       => $post->post_title,
        'description' => apply_filters('the_content', $post->post_content),
        'excerpt'     => get_the_excerpt($post),
        'status'      => get_post_meta($post->ID, '_event_status', true) ?: 'draft',
        'date'        => get_post_meta($post->ID, '_event_date', true),
        'location'    => get_post_meta($post->ID, '_event_location', true),
        'created_at'  => $post->post_date_gmt,
        'updated_at'  => $post->post_modified_gmt,
        '_links'      => [
            'self'       => [rest_url('myplugin/v1/events/' . $post->ID)],
            'collection' => [rest_url('myplugin/v1/events')],
        ],
    ];
}

// Creation: return 201 with Location header (see Pattern 6 CRUD Controller for full example).
// Deletion: return 200 with {'deleted': true, 'previous': {...}} or 204 with no body.
```

### Pattern 5: Extending Existing Endpoints with register_rest_field

Add custom fields to built-in WP REST responses (posts, users, terms) without creating new endpoints.

```php
<?php
declare(strict_types=1);

add_action('rest_api_init', function (): void {
    // Add a "reading_time" field to all post responses
    register_rest_field('post', 'reading_time', [
        'get_callback' => function (array $post_data): int {
            $content   = get_post_field('post_content', $post_data['id']);
            $word_count = str_word_count(wp_strip_all_tags($content));

            return max(1, (int) ceil($word_count / 200));
        },
        'update_callback' => null, // Read-only field
        'schema'          => [
            'description' => 'Estimated reading time in minutes.',
            'type'        => 'integer',
            'context'     => ['view', 'embed'],
            'readonly'    => true,
        ],
    ]);

    // Add a writable "subtitle" field to posts
    register_rest_field('post', 'subtitle', [
        'get_callback' => function (array $post_data): string {
            return (string) get_post_meta($post_data['id'], '_subtitle', true);
        },
        'update_callback' => function (string $value, WP_Post $post): bool {
            return (bool) update_post_meta($post->ID, '_subtitle', sanitize_text_field($value));
        },
        'schema' => [
            'description' => 'Post subtitle displayed below the main title.',
            'type'        => 'string',
            'maxLength'   => 200,
            'context'     => ['view', 'edit'],
            'arg_options' => [
                'sanitize_callback' => 'sanitize_text_field',
            ],
        ],
    ]);

    // The same pattern works for any post type, users, or terms.
    // Use 'type' => 'object' with 'properties' for structured fields (e.g., social_links on users).
});
```

### Pattern 6: CRUD Controller Class

An OOP approach to organizing WP REST endpoints by extending `WP_REST_Controller`. This provides a standard structure with route registration, permission checks, CRUD operations, response preparation, and schema definition.

```php
<?php
declare(strict_types=1);

namespace MyPlugin\Api;

use WP_REST_Controller;
use WP_REST_Request;
use WP_REST_Response;
use WP_REST_Server;
use WP_Error;

class EventsController extends WP_REST_Controller
{
    protected $namespace = 'myplugin/v1';
    protected $rest_base = 'events';

    public function register_routes(): void
    {
        register_rest_route($this->namespace, '/' . $this->rest_base, [
            [
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => [$this, 'get_items'],
                'permission_callback' => [$this, 'get_items_permissions_check'],
                'args'                => $this->get_collection_params(),
            ],
            [
                'methods'             => WP_REST_Server::CREATABLE,
                'callback'            => [$this, 'create_item'],
                'permission_callback' => [$this, 'create_item_permissions_check'],
                'args'                => $this->get_endpoint_args_for_item_schema(WP_REST_Server::CREATABLE),
            ],
            'schema' => [$this, 'get_public_item_schema'],
        ]);

        register_rest_route($this->namespace, '/' . $this->rest_base . '/(?P<id>[\d]+)', [
            [
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => [$this, 'get_item'],
                'permission_callback' => [$this, 'get_item_permissions_check'],
                'args'                => [
                    'id' => [
                        'type'              => 'integer',
                        'required'          => true,
                        'sanitize_callback' => 'absint',
                    ],
                ],
            ],
            [
                'methods'             => WP_REST_Server::EDITABLE,
                'callback'            => [$this, 'update_item'],
                'permission_callback' => [$this, 'update_item_permissions_check'],
                'args'                => $this->get_endpoint_args_for_item_schema(WP_REST_Server::EDITABLE),
            ],
            [
                'methods'             => WP_REST_Server::DELETABLE,
                'callback'            => [$this, 'delete_item'],
                'permission_callback' => [$this, 'delete_item_permissions_check'],
                'args'                => [
                    'force' => [
                        'type'    => 'boolean',
                        'default' => false,
                        'description' => 'Bypass trash and force deletion.',
                    ],
                ],
            ],
            'schema' => [$this, 'get_public_item_schema'],
        ]);
    }

    // -- Permission checks --------------------------------------------------

    public function get_items_permissions_check($request): bool
    {
        return true; // Public listing
    }

    public function get_item_permissions_check($request): bool
    {
        return true; // Public single view
    }

    public function create_item_permissions_check($request): bool
    {
        return current_user_can('edit_posts');
    }

    public function update_item_permissions_check($request): bool
    {
        $post = get_post((int) $request['id']);

        return $post && current_user_can('edit_post', $post->ID);
    }

    public function delete_item_permissions_check($request): bool
    {
        $post = get_post((int) $request['id']);

        return $post && current_user_can('delete_post', $post->ID);
    }

    // -- CRUD operations ----------------------------------------------------

    public function get_items($request): WP_REST_Response
    {
        $args = [
            'post_type'      => 'event',
            'post_status'    => 'publish',
            'posts_per_page' => (int) $request['per_page'],
            'paged'          => (int) $request['page'],
            'orderby'        => $request['orderby'] ?? 'date',
            'order'          => $request['order'] ?? 'DESC',
        ];

        if (! empty($request['search'])) {
            $args['s'] = $request['search'];
        }

        $query = new \WP_Query($args);
        $items = [];

        foreach ($query->posts as $post) {
            $data    = $this->prepare_item_for_response($post, $request);
            $items[] = $this->prepare_response_for_collection($data);
        }

        $response = rest_ensure_response($items);
        $response->header('X-WP-Total', (string) $query->found_posts);
        $response->header('X-WP-TotalPages', (string) $query->max_num_pages);

        return $response;
    }

    public function get_item($request): WP_REST_Response|WP_Error
    {
        $post = get_post((int) $request['id']);

        if (! $post || $post->post_type !== 'event') {
            return new WP_Error(
                'rest_event_not_found',
                __('Event not found.', 'myplugin'),
                ['status' => 404]
            );
        }

        return $this->prepare_item_for_response($post, $request);
    }

    public function create_item($request): WP_REST_Response|WP_Error
    {
        $post_id = wp_insert_post([
            'post_type'    => 'event',
            'post_title'   => $request['title'],
            'post_content' => $request['description'] ?? '',
            'post_status'  => 'publish',
            'meta_input'   => [
                '_event_date'     => $request['event_date'],
                '_event_location' => $request['location'] ?? '',
            ],
        ], true);

        if (is_wp_error($post_id)) {
            return $post_id;
        }

        $post     = get_post($post_id);
        $response = $this->prepare_item_for_response($post, $request);
        $response->set_status(201);
        $response->header('Location', rest_url(
            sprintf('%s/%s/%d', $this->namespace, $this->rest_base, $post_id)
        ));

        return $response;
    }

    // update_item / delete_item follow the same pattern:
    // 1. Fetch the resource, return WP_Error if not found
    // 2. Perform the operation (wp_update_post / wp_delete_post)
    // 3. Return prepare_item_for_response() result

    // -- Response preparation -----------------------------------------------

    public function prepare_item_for_response($post, $request): WP_REST_Response
    {
        $data = [
            'id'          => $post->ID,
            'title'       => $post->post_title,
            'description' => $post->post_content,
            'event_date'  => get_post_meta($post->ID, '_event_date', true) ?: null,
            'location'    => get_post_meta($post->ID, '_event_location', true) ?: null,
            'author'      => (int) $post->post_author,
            'created_at'  => mysql_to_rfc3339($post->post_date_gmt),
            'updated_at'  => mysql_to_rfc3339($post->post_modified_gmt),
        ];

        $response = rest_ensure_response($data);
        $response->add_links([
            'self'       => ['href' => rest_url(sprintf('%s/%s/%d', $this->namespace, $this->rest_base, $post->ID))],
            'collection' => ['href' => rest_url(sprintf('%s/%s', $this->namespace, $this->rest_base))],
        ]);

        return $response;
    }

    // -- Schema -------------------------------------------------------------

    public function get_item_schema(): array
    {
        if ($this->schema) {
            return $this->add_additional_fields_schema($this->schema);
        }

        // Each property defines: description, type, context (view/edit/embed),
        // readonly flag, and arg_options with sanitize_callback.
        // Use get_endpoint_args_for_item_schema() to auto-generate route args from this schema.
        $this->schema = [
            '$schema'    => 'http://json-schema.org/draft-04/schema#',
            'title'      => 'event',
            'type'       => 'object',
            'properties' => [
                'id'         => ['type' => 'integer', 'context' => ['view', 'edit', 'embed'], 'readonly' => true],
                'title'      => ['type' => 'string',  'context' => ['view', 'edit', 'embed'], 'required' => true,
                                 'minLength' => 1, 'maxLength' => 200,
                                 'arg_options' => ['sanitize_callback' => 'sanitize_text_field']],
                'event_date' => ['type' => 'string', 'format' => 'date-time', 'context' => ['view', 'edit', 'embed'], 'required' => true],
                'location'   => ['type' => 'string', 'context' => ['view', 'edit'],
                                 'arg_options' => ['sanitize_callback' => 'sanitize_text_field']],
                'created_at' => ['type' => 'string', 'format' => 'date-time', 'context' => ['view', 'edit'], 'readonly' => true],
                'updated_at' => ['type' => 'string', 'format' => 'date-time', 'context' => ['view', 'edit'], 'readonly' => true],
            ],
        ];

        return $this->add_additional_fields_schema($this->schema);
    }

    public function get_collection_params(): array
    {
        $params = parent::get_collection_params(); // Inherits page, per_page, search

        $params['orderby'] = ['type' => 'string', 'default' => 'date', 'enum' => ['date', 'title', 'modified']];
        $params['order']   = ['type' => 'string', 'default' => 'DESC', 'enum' => ['ASC', 'DESC']];

        return $params;
    }
}

// Register the controller (typically in plugin bootstrap):
add_action('rest_api_init', function (): void {
    $controller = new EventsController();
    $controller->register_routes();
});
```

---

### Pattern 7: Webhook Receiver with Signature Validation and Idempotency

Securely receive webhooks through a WP REST endpoint. Validates the signature, checks for duplicate processing, dispatches to async handling, and returns immediately.

```php
<?php
declare(strict_types=1);

add_action('rest_api_init', function (): void {
    register_rest_route('myplugin/v1', '/webhooks/stripe', [
        'methods'             => WP_REST_Server::CREATABLE,
        'callback'            => 'myplugin_handle_stripe_webhook',
        'permission_callback' => '__return_true', // Auth is via signature
    ]);
});

function myplugin_handle_stripe_webhook(WP_REST_Request $request): WP_REST_Response {
    // 1. Validate the webhook signature
    $payload   = $request->get_body();
    $signature = $request->get_header('Stripe-Signature');
    $secret    = get_option('myplugin_stripe_webhook_secret');

    if (! $signature || ! myplugin_verify_stripe_signature($payload, $signature, $secret)) {
        return new WP_REST_Response(['error' => 'Invalid signature.'], 401);
    }

    $event = json_decode($payload, true);

    if (json_last_error() !== JSON_ERROR_NONE) {
        return new WP_REST_Response(['error' => 'Invalid JSON payload.'], 400);
    }

    // 2. Idempotency check -- prevent processing the same event twice
    $event_id = $event['id'] ?? null;

    if (! $event_id) {
        return new WP_REST_Response(['error' => 'Missing event ID.'], 400);
    }

    $processed_key = 'myplugin_webhook_' . md5($event_id);

    if (get_transient($processed_key)) {
        // Already processed -- return 200 so the sender does not retry
        return new WP_REST_Response(['status' => 'already_processed'], 200);
    }

    // 3. Dispatch to async processing (avoid blocking the webhook response)
    if (function_exists('as_enqueue_async_action')) {
        // Use Action Scheduler if available
        as_enqueue_async_action('myplugin_process_webhook', [
            'event_type' => $event['type'],
            'event_data' => $event['data'],
            'event_id'   => $event_id,
        ]);
    } else {
        // Fall back to wp_schedule_single_event
        wp_schedule_single_event(time(), 'myplugin_process_webhook_cron', [$event]);
    }

    // 4. Mark as processed (TTL of 48 hours to cover retry windows)
    set_transient($processed_key, true, 48 * HOUR_IN_SECONDS);

    // 5. Respond immediately with 200 (webhook senders expect fast responses)
    return new WP_REST_Response(['status' => 'accepted'], 200);
}

function myplugin_verify_stripe_signature(string $payload, string $signature_header, string $secret, int $tolerance = 300): bool {
    // Parse "t=timestamp,v1=signature" from header
    $parts = [];
    foreach (explode(',', $signature_header) as $pair) {
        [$key, $value] = explode('=', $pair, 2);
        $parts[trim($key)] = trim($value);
    }
    $timestamp = $parts['t'] ?? '';
    $expected  = $parts['v1'] ?? '';
    if (! $timestamp || ! $expected) { return false; }
    if (abs(time() - (int) $timestamp) > $tolerance) { return false; } // Replay attack prevention
    $computed = hash_hmac('sha256', $timestamp . '.' . $payload, $secret);
    return hash_equals($expected, $computed);
}
```

### Pattern 8: Error Response Format -- RFC 7807 Problem Details

A reusable error response format for WP REST API endpoints. RFC 7807 defines a standard JSON structure for HTTP API error responses.

```php
<?php
declare(strict_types=1);

/**
 * Framework-agnostic Problem Details builder (RFC 7807).
 */
class ProblemDetails implements JsonSerializable
{
    public function __construct(
        private readonly string $type,
        private readonly string $title,
        private readonly int $status,
        private readonly ?string $detail = null,
        private readonly ?string $instance = null,
        private readonly array $extensions = [],
    ) {}

    public function jsonSerialize(): array
    {
        $data = ['type' => $this->type, 'title' => $this->title, 'status' => $this->status];
        if ($this->detail !== null)   { $data['detail']   = $this->detail; }
        if ($this->instance !== null) { $data['instance'] = $this->instance; }
        return array_merge($data, $this->extensions);
    }

    public function getStatus(): int { return $this->status; }

    // Factory methods for common error types
    public static function notFound(string $detail = 'The requested resource was not found.'): self
    {
        return new self(type: 'https://httpproblems.com/http-status/404', title: 'Not Found', status: 404, detail: $detail);
    }

    public static function forbidden(string $detail = 'You do not have permission.'): self
    {
        return new self(type: 'https://httpproblems.com/http-status/403', title: 'Forbidden', status: 403, detail: $detail);
    }

    public static function validationFailed(array $errors, string $detail = 'Validation failed.'): self
    {
        return new self(type: 'https://httpproblems.com/http-status/422', title: 'Unprocessable Entity', status: 422, detail: $detail, extensions: ['errors' => $errors]);
    }

    // Same pattern for: unauthorized(401), conflict(409), tooManyRequests(429), internal(500)
}

// -- WordPress usage: -------------------------------------------------------
function myplugin_api_error(ProblemDetails $problem): WP_REST_Response {
    $response = new WP_REST_Response($problem->jsonSerialize(), $problem->getStatus());
    $response->header('Content-Type', 'application/problem+json');

    return $response;
}

// In an endpoint callback:
function myplugin_get_item(WP_REST_Request $request): WP_REST_Response {
    $item = get_post((int) $request['id']);

    if (! $item) {
        return myplugin_api_error(
            ProblemDetails::notFound("Item #{$request['id']} does not exist.")
        );
    }

    // ...
}

// Example validation error response body:
// {
//     "type": "https://httpproblems.com/http-status/422",
//     "title": "Unprocessable Entity",
//     "status": 422,
//     "detail": "Validation failed.",
//     "errors": {
//         "email": ["The email field is required."],
//         "name": ["The name must be at least 2 characters."]
//     }
// }
```

### Pattern 9: Cursor-Based Pagination

Cursor-based pagination avoids the performance problems of `OFFSET` on large datasets and provides stable page boundaries when records are inserted or deleted between requests.

Args: `limit` (integer, 1-100, default 20), `cursor` (string, opaque), `direction` (enum: next/prev).

```php
<?php
declare(strict_types=1);

// Route registration uses standard args pattern (see Pattern 1) with limit, cursor, direction.

function myplugin_get_feed(WP_REST_Request $request): WP_REST_Response {
    global $wpdb;

    $limit     = (int) $request->get_param('limit');
    $cursor    = $request->get_param('cursor');
    $direction = $request->get_param('direction');

    // Decode cursor (base64-encoded JSON with id and created_at)
    $cursor_data = null;
    if ($cursor) {
        $decoded = json_decode(base64_decode($cursor, true), true);
        if (is_array($decoded) && isset($decoded['id'], $decoded['created_at'])) {
            $cursor_data = $decoded;
        }
    }

    // Build query with cursor-based WHERE clause
    $where = "WHERE p.post_type = 'post' AND p.post_status = 'publish'";

    if ($cursor_data) {
        $op = $direction === 'next' ? '<' : '>';
        $order = $direction === 'next' ? 'DESC' : 'ASC';

        // Use a composite cursor: (created_at, id) for stable ordering
        $where .= $wpdb->prepare(
            " AND (p.post_date < %s OR (p.post_date = %s AND p.ID {$op} %d))",
            $cursor_data['created_at'],
            $cursor_data['created_at'],
            $cursor_data['id']
        );
    } else {
        $order = 'DESC';
    }

    // Fetch one extra record to determine if there are more pages
    $sql = "SELECT p.ID, p.post_title, p.post_date, p.post_excerpt
            FROM {$wpdb->posts} p
            {$where}
            ORDER BY p.post_date {$order}, p.ID {$order}
            LIMIT %d";

    $rows = $wpdb->get_results($wpdb->prepare($sql, $limit + 1));

    $has_more = count($rows) > $limit;
    if ($has_more) {
        array_pop($rows); // Remove the extra record
    }

    // If we fetched in reverse order for "prev", flip back to natural order
    if ($direction === 'prev') {
        $rows = array_reverse($rows);
    }

    $items = array_map(fn ($row) => [
        'id' => (int) $row->ID, 'title' => $row->post_title,
        'excerpt' => $row->post_excerpt, 'created_at' => $row->post_date,
    ], $rows);

    // Build opaque cursors from first/last items
    $next_cursor = ($has_more && count($items) > 0)
        ? base64_encode(json_encode(['id' => end($items)['id'], 'created_at' => end($items)['created_at']]))
        : null;
    $prev_cursor = (count($items) > 0 && $cursor)
        ? base64_encode(json_encode(['id' => reset($items)['id'], 'created_at' => reset($items)['created_at']]))
        : null;

    $response = new WP_REST_Response([
        'data'    => $items,
        'cursors' => ['next' => $next_cursor, 'prev' => $prev_cursor],
        'meta'    => ['has_more' => $has_more, 'count' => count($items)],
    ], 200);

    // Add Link headers for discoverability (see Pattern 4 for link_header usage)
    $base = rest_url('myplugin/v1/feed');
    if ($next_cursor) {
        $response->link_header('next', add_query_arg(['cursor' => $next_cursor, 'direction' => 'next', 'limit' => $limit], $base));
    }
    if ($prev_cursor) {
        $response->link_header('prev', add_query_arg(['cursor' => $prev_cursor, 'direction' => 'prev', 'limit' => $limit], $base));
    }

    return $response;
}
```

---

## Best Practices Summary

1. **Always declare `permission_callback`** in WordPress REST routes. Omitting it triggers a `_doing_it_wrong` notice and defaults to public access -- which may not be your intent.
2. **Validate and sanitize at the boundary.** Use `validate_callback` and `sanitize_callback` on every WP REST arg. Never trust input that reaches your business logic.
3. **Use JSON Schema keywords** (`type`, `format`, `enum`, `minimum`, `maxLength`, `pattern`) in WP REST args. WordPress validates these automatically before your callback runs.
4. **Return proper HTTP status codes.** 200 for success, 201 for creation (with `Location` header), 204 for no-content, 4xx for client errors, 5xx for server errors.
5. **Format errors consistently** using RFC 7807 Problem Details. Consumers should be able to parse every error response with the same code.
6. **Make webhook receivers fast and idempotent.** Validate the signature, check idempotency, dispatch to a queue, and return 200 immediately. Never do heavy processing synchronously in a webhook handler.
7. **Use cursor-based pagination for feeds and large datasets.** Offset-based pagination degrades as page numbers increase and produces inconsistent results when records are added or removed between requests.
8. **Version your API namespace** (e.g., `myplugin/v1`). When breaking changes are needed, introduce `v2` and run both versions until consumers migrate.
9. **Set cache headers** on read endpoints. Use `Cache-Control`, `ETag`, or `Last-Modified` to reduce unnecessary traffic and improve client-side performance.
10. **Use `WP_REST_Controller`** for non-trivial endpoints. The base class provides standardized methods for permissions, response preparation, schema, and collection params.
