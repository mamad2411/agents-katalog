---
name: wordpress-abilities-ai
description: WordPress 6.9+ Abilities API and 7.0+ AI Client API. Use when registering or invoking "abilities" (wp_register_ability, wp_get_ability, wp_abilities_api_init), building AI prompts via wp_ai_client_prompt() / WP_AI_Client_Prompt_Builder, doing function calling with WP_AI_Client_Ability_Function_Resolver, or building AI features inside WordPress. These APIs are very new (WP 7.1-alpha in this repo) and may not be in older training data — read the source files in wp-includes/abilities-api/ and wp-includes/ai-client/ as the authoritative reference.
---

# Abilities API and AI Client (WP 6.9 / 7.0+)

These two APIs are new in WordPress and work together. The **Abilities API** is a registry of discoverable, schema-described functions (much like MCP tools or OpenAI function-calling tools). The **AI Client API** is a fluent builder for calling generative AI models, with optional integration where registered abilities are exposed to the model as tools.

This repository is WordPress 7.1-alpha. The Abilities API landed in 6.9, the AI Client in 7.0.

## When to reach for which

- **Abilities API alone**: when you want to expose a discrete capability of your plugin in a uniform way — to other plugins, to the REST API, or to AI tooling. Think "register `my-plugin/export-users` so anything can find it and run it."
- **AI Client alone**: when you want to generate text, images, speech, video, or embeddings from inside WordPress against any compatible provider.
- **Both together**: when you want the AI model to be able to call your registered abilities as tools (function calling).

## Abilities API basics

### Two action hooks, two registries

```php
// 1. Register categories on this hook.
add_action( 'wp_abilities_api_categories_init', function () {
    wp_register_ability_category( 'content-management', array(
        'label'       => __( 'Content Management', 'my-plugin' ),
        'description' => __( 'Abilities for managing and organizing content.', 'my-plugin' ),
    ) );
} );

// 2. Register abilities on this hook (and only this hook — calling elsewhere triggers _doing_it_wrong).
add_action( 'wp_abilities_api_init', function () {
    wp_register_ability( 'my-plugin/export-users', array(
        'label'               => __( 'Export Users', 'my-plugin' ),
        'description'         => __( 'Exports user data to CSV format.', 'my-plugin' ),
        'category'            => 'content-management',
        'execute_callback'    => 'my_plugin_export_users',
        'permission_callback' => fn() => current_user_can( 'export' ),
        'input_schema'        => array(
            'type'        => 'string',
            'enum'        => array( 'subscriber', 'editor', 'administrator' ),
            'description' => __( 'Role to filter exported users by.', 'my-plugin' ),
            'required'    => false,
        ),
        'output_schema'       => array(
            'type'        => 'string',
            'description' => __( 'User data in CSV format.', 'my-plugin' ),
            'required'    => true,
        ),
        'meta' => array(
            'annotations'  => array(
                'readonly'    => true,    // Doesn't modify environment.
                'destructive' => false,
                'idempotent'  => true,
            ),
            'show_in_rest' => true,       // Exposes via /wp-json/wp/v2/abilities/.
        ),
    ) );
} );
```

### Naming rules

Ability names must be `namespace/slug`, lowercase, with only alphanumerics, dashes, and forward slashes. Example: `acme-crm/sync-contacts`. Use descriptive action-verb slugs (`process-payment`, not `payment`).

### Input/output schemas (subset of JSON Schema draft 4)

WordPress's validator implements a subset of JSON Schema. Use the same vocabulary as the REST API schema:

```php
'input_schema' => array(
    'type'       => 'object',
    'properties' => array(
        'role'   => array( 'type' => 'string', 'enum' => array( 'editor', 'author' ) ),
        'limit'  => array( 'type' => 'integer', 'minimum' => 1, 'maximum' => 1000 ),
        'fields' => array( 'type' => 'array', 'items' => array( 'type' => 'string' ) ),
    ),
    'required' => array( 'role' ),
),
```

Schemas serve double duty: input validation at runtime, and self-documenting contracts for AI/REST consumers.

### Callbacks

```php
function my_plugin_export_users( $input ) {
    // $input is whatever shape input_schema declared (already validated).
    if ( ! is_string( $input ) ) {
        return new WP_Error( 'bad_input', 'Expected string role' );
    }
    $csv = build_csv_for_role( $input );
    return $csv;          // Return the value, OR a WP_Error on failure.
}

// Permission callback receives the same input. Return bool or WP_Error.
function my_plugin_can_export( $input ): bool|WP_Error {
    return current_user_can( 'export' );
}
```

Always return `WP_Error` for failures — never throw exceptions. The Abilities runner expects this.

### Discovery and inspection

```php
if ( wp_has_ability( 'my-plugin/export-users' ) ) {
    $ability = wp_get_ability( 'my-plugin/export-users' );
    echo $ability->get_label();
    echo $ability->get_description();
}

$all = wp_get_abilities();                    // WP_Ability[]
$cats = wp_get_ability_categories();          // WP_Ability_Category[]
```

### Annotations — hint behavior to tooling

The `meta.annotations` block describes side-effects so callers (AI, automation, admin UI) can reason about safety:

- `readonly: true` — doesn't modify state at all. Safe to call speculatively.
- `destructive: true` — may delete or overwrite. AI should ask before calling.
- `idempotent: true` — same input always produces same effect; safe to retry.

### REST exposure

Setting `meta.show_in_rest => true` exposes the ability through new REST controllers (see `wp-includes/rest-api/endpoints/class-wp-rest-abilities-v1-*.php`):

- `GET /wp-json/wp/v2/abilities` — list registered abilities.
- `GET /wp-json/wp/v2/abilities/categories` — list categories.
- `POST /wp-json/wp/v2/abilities/<name>/run` — invoke an ability.

The `permission_callback` is enforced for the run endpoint.

### Unregistering and overriding

```php
// Override an ability another plugin registered:
add_action( 'wp_abilities_api_init', function () {
    if ( wp_has_ability( 'other-plugin/some-ability' ) ) {
        wp_unregister_ability( 'other-plugin/some-ability' );
    }
    wp_register_ability( 'other-plugin/some-ability', array( /* your version */ ) );
}, 20 );   // Higher priority so it runs after the original registration.
```

## AI Client API basics

The AI Client wraps a PHP AI SDK behind a fluent, WordPress-idiomatic builder. It supports multiple providers (selected via a registry), multi-modal inputs/outputs, and structured (JSON-schema) responses.

### Hello, world

```php
if ( ! wp_supports_ai() ) {
    return new WP_Error( 'ai_unavailable', 'AI is not enabled.' );
}

$result = wp_ai_client_prompt( 'Write a haiku about WordPress.' )
    ->using_system_instruction( 'You are a poet.' )
    ->using_temperature( 0.8 )
    ->using_max_tokens( 200 )
    ->generate_text();

if ( is_wp_error( $result ) ) {
    error_log( $result->get_error_message() );
} else {
    echo esc_html( $result );      // $result is a string.
}
```

### The fluent builder pattern

Every `with_*` / `using_*` / `as_*` returns the same builder so you can chain. The chain enters an "error state" if any step throws — subsequent calls are no-ops, and `generate_*` returns the captured `WP_Error`. This means you never have to check between every link.

Most-used methods:

| Method | Purpose |
| --- | --- |
| `with_text(string)` | Append text to the current message. |
| `with_file(file, mime?)` | Attach a file (image, audio, video, document). |
| `with_history(...Message)` | Provide multi-turn conversation history. |
| `using_model_preference(...$models)` | Try these models in order. |
| `using_provider(string)` | Force a specific provider. |
| `using_system_instruction(string)` | System / persona prompt. |
| `using_temperature(float)`, `using_top_p(float)`, `using_top_k(int)` | Sampling controls. |
| `using_max_tokens(int)` | Generation cap. |
| `using_stop_sequences(...string)` | Halt on tokens. |
| `using_function_declarations(...FunctionDeclaration)` | Tool/function calling. |
| `as_output_mime_type(string)` | e.g., `application/json`. |
| `as_json_response(?array $schema)` | Shortcut for JSON output with optional schema. |
| `as_output_modalities(...ModalityEnum)` | Image, audio, video, etc. |

Generating methods (these return the result OR a `WP_Error`):

```php
->generate_text()                       // -> string
->generate_texts(?int $count = null)    // -> list<string>
->generate_image()                      // -> File
->generate_images(?int $count = null)   // -> list<File>
->convert_text_to_speech()              // -> File
->generate_video_result()               // -> GenerativeAiResult
->generate_result(?CapabilityEnum)      // -> GenerativeAiResult (raw)
```

### Capability checks

Different providers/models support different modalities. Always probe:

```php
$builder = wp_ai_client_prompt( 'A red sunset over a forest.' )
    ->as_output_modalities( ModalityEnum::IMAGE() );

if ( ! $builder->is_supported_for_image_generation() ) {
    return new WP_Error( 'unsupported', 'No image-capable model is configured.' );
}

$image = $builder->generate_image();    // WordPress\AiClient\Files\DTO\File
```

### Structured (JSON) output

```php
$schema = array(
    'type' => 'object',
    'properties' => array(
        'title'  => array( 'type' => 'string' ),
        'tags'   => array( 'type' => 'array', 'items' => array( 'type' => 'string' ) ),
        'rating' => array( 'type' => 'integer', 'minimum' => 1, 'maximum' => 5 ),
    ),
    'required' => array( 'title', 'rating' ),
);

$json = wp_ai_client_prompt( 'Suggest a blog post title and tags for an article about caching.' )
    ->as_json_response( $schema )
    ->generate_text();

$data = json_decode( $json, true );
```

### Multi-modal input

```php
use WordPress\AiClient\Files\DTO\File;

$image_file = File::fromPath( '/path/to/screenshot.png' );

$alt = wp_ai_client_prompt()
    ->with_text( 'Write alt text for this screenshot, max 120 chars.' )
    ->with_file( $image_file, 'image/png' )
    ->generate_text();
```

## Function calling: AI Client + Abilities API

This is where the two systems join up: registered abilities become tools the model can call.

```php
use WordPress\AiClient\Tools\DTO\FunctionDeclaration;

// 1. Pick which abilities the model is allowed to use (allowlist — never expose everything).
$allowed = array(
    wp_get_ability( 'my-plugin/search-posts' ),
    wp_get_ability( 'my-plugin/get-post' ),
);

// 2. Build a function resolver that knows about exactly those abilities.
$resolver = new WP_AI_Client_Ability_Function_Resolver( ...$allowed );

// 3. Build the model's tool declarations from the same abilities.
$declarations = array_map(
    fn( WP_Ability $a ) => $resolver->ability_to_function_declaration( $a ),
    $allowed
);

// 4. Run a turn. If the model issues function calls, resolve them, then continue.
$result = wp_ai_client_prompt( 'Find the most recent post about caching and summarize it.' )
    ->using_function_declarations( ...$declarations )
    ->generate_result();

// $result includes any function calls the model made.
// Use $resolver->resolve_function_calls( $result->getFunctionCalls() ) to execute them.
```

The resolver enforces the allowlist: even if the model hallucinates an ability name outside the allowed set, the resolver refuses to invoke it. The mapping uses a `wpab__` prefix on function names internally to namespace them away from any non-ability tools you might also declare.

### Why allowlist?

Never pass `wp_get_abilities()` directly to a model. You don't want the model to discover and call (say) `core/delete-user` because it thought that sounded useful. Construct the allowlist explicitly per use-case.

## Where to look in this codebase

The source is the most up-to-date reference and is heavily commented:

- `wp-includes/abilities-api.php` — `wp_register_ability`, `wp_register_ability_category`, `wp_has_ability`, `wp_get_ability`, `wp_get_abilities`, `wp_get_ability_categories`, `wp_unregister_ability`.
- `wp-includes/abilities-api/class-wp-ability.php` — the `WP_Ability` object (label, description, schemas, execution methods).
- `wp-includes/abilities-api/class-wp-abilities-registry.php` — the registry singleton.
- `wp-includes/abilities-api/class-wp-ability-categories-registry.php` — categories registry.
- `wp-includes/ai-client.php` — `wp_supports_ai`, `wp_ai_client_prompt`, the `WP_AI_SUPPORT` constant and `wp_supports_ai` filter.
- `wp-includes/ai-client/class-wp-ai-client-prompt-builder.php` — the fluent builder; the docblock lists every method with its signature.
- `wp-includes/ai-client/class-wp-ai-client-ability-function-resolver.php` — bridges abilities to AI function calls.
- `wp-includes/ai-client/adapters/` — HTTP client, cache, discovery strategy, event dispatcher.
- `wp-includes/rest-api/endpoints/class-wp-rest-abilities-v1-*.php` — REST controllers for abilities.

## Common pitfalls

- Registering on the wrong hook. Categories on `wp_abilities_api_categories_init`; abilities on `wp_abilities_api_init`. WordPress will warn loudly if you violate this.
- Registering an ability whose `category` isn't registered yet. Categories must come first.
- Returning a thrown exception from `execute_callback`. Return `WP_Error` instead — the rest of the pipeline expects it.
- Forgetting `show_in_rest` and wondering why an ability isn't visible at `/wp-json/wp/v2/abilities`.
- Exposing every registered ability to a model. Allowlist explicitly with `WP_AI_Client_Ability_Function_Resolver`.
- Assuming `wp_supports_ai()` is true. Check first; sites can opt out via the `WP_AI_SUPPORT` constant or the `wp_supports_ai` filter.
- Treating fluent-builder return values as live data instead of as the builder object. Only the `generate_*` methods return content — and they're the only ones that can return `WP_Error`.
- Hardcoding model identifiers. Use `using_model_preference` so the site can route through any compatible provider.
