---
name: sage-patterns
description: Sage/Roots theme patterns — Acorn service providers, Bud asset configuration, Blade components in WordPress, view composers, and common Sage gotchas with solutions. Use when working with Sage themes or the Roots ecosystem.
---

# Sage/Roots Implementation Patterns

Production-ready implementation patterns for the Roots ecosystem (Sage, Acorn, Bud, Bedrock). Sage brings Laravel's tooling into WordPress: Acorn boots a Laravel container, Bud compiles assets, and Blade replaces the PHP template hierarchy. Every pattern targets Sage 10+ with Acorn and is copy-pasteable PHP/JS.

## When to Use This Skill

- Building Sage themes with Acorn service providers
- Configuring Bud for Tailwind CSS asset compilation
- Creating Blade components that render WordPress data
- Passing WordPress data into Blade templates via view composers
- Writing custom Blade directives for WordPress functions
- Troubleshooting Sage-specific issues (autoloading timing, template hierarchy, asset versioning)

## Core Concepts

1. **Sage is Laravel inside WordPress.** Acorn boots a Laravel application container during `after_setup_theme`. Everything you know about Laravel works, but the lifecycle and entry point are WordPress-controlled.
2. **Convention over configuration.** Sage follows strict directory conventions. Place files where the framework expects them (`app/Providers/`, `app/View/Composers/`, `resources/views/components/`) and auto-discovery handles the rest.
3. **Blade replaces the template hierarchy.** Views live in `resources/views/`. Use `@include` and `<x-component>` syntax, not `get_template_part()`.
4. **View composers centralize data.** Never scatter `get_the_title()` calls across Blade files. Composers pass clean, typed variables to views.
5. **Bud is the build tool.** It compiles JS, CSS (PostCSS/Tailwind), images, and fonts. Use `bundle()->enqueue()` in PHP to load hashed production assets.

## Quick Start

A minimal Sage view composer passing WordPress data to a Blade view:

```php
<?php

declare(strict_types=1);

namespace App\View\Composers;

use Roots\Acorn\View\Composer;

class HeroComposer extends Composer
{
    protected static $views = ['partials.hero'];

    public function with(): array
    {
        return [
            'title' => get_the_title(),
            'image' => get_the_post_thumbnail_url(null, 'full'),
            'excerpt' => get_the_excerpt(),
        ];
    }
}
```

---

## Pattern 1: Acorn Service Provider in Sage

Acorn service providers work like Laravel service providers but boot inside WordPress. Place them in `app/Providers/` and register them in `config/app.php`. Use the `boot()` method to hook into WordPress actions.

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use App\Services\MenuService;
use App\Services\SeoService;
use App\Contracts\SeoServiceInterface;
use Illuminate\Support\ServiceProvider;

class ThemeServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(MenuService::class, function ($app) {
            return new MenuService(
                cacheDriver: $app->make('cache.store'),
                cacheTtl: (int) $app->make('config')->get('theme.menu_cache_ttl', 3600),
            );
        });

        $this->app->bind(SeoServiceInterface::class, SeoService::class);
    }

    public function boot(): void
    {
        // Register WordPress hooks inside the provider boot
        add_action('after_setup_theme', [$this, 'registerThemeSupport']);
        add_action('widgets_init', [$this, 'registerSidebars']);
        add_action('init', [$this, 'registerNavigationMenus']);
    }

    public function registerThemeSupport(): void
    {
        add_theme_support('title-tag');
        add_theme_support('post-thumbnails');
        add_theme_support('responsive-embeds');
        add_theme_support('html5', [
            'caption', 'comment-form', 'comment-list',
            'gallery', 'search-form', 'script', 'style',
        ]);
        add_theme_support('custom-logo', [
            'height' => 100, 'width' => 400,
            'flex-height' => true, 'flex-width' => true,
        ]);
    }

    public function registerSidebars(): void
    {
        register_sidebar([
            'name' => __('Primary Sidebar', 'theme'),
            'id' => 'sidebar-primary',
            'before_widget' => '<section class="widget %2$s" id="%1$s">',
            'after_widget' => '</section>',
            'before_title' => '<h3 class="widget-title">',
            'after_title' => '</h3>',
        ]);
    }

    public function registerNavigationMenus(): void
    {
        register_nav_menus([
            'primary_navigation' => __('Primary Navigation', 'theme'),
            'footer_navigation' => __('Footer Navigation', 'theme'),
        ]);
    }
}
```

Register in `config/app.php` within Sage:

```php
'providers' => [
    // ...existing providers...
    App\Providers\ThemeServiceProvider::class,
],
```

---

## Pattern 2: Bud Configuration for Tailwind CSS

Bud is the asset build tool for Sage 10+. This configuration sets up Tailwind CSS with PostCSS, entry points, dev server proxy, and production optimization.

**`bud.config.js`** (project root of Sage theme):

```javascript
/** @param {import('@roots/bud').Bud} bud */
export default async (bud) => {
  bud
    // Entrypoints -- assets matching the key are bundled together
    .entry({
      app: ['@scripts/app', '@styles/app'],
      editor: ['@scripts/editor', '@styles/editor'],
    })
    .assets(['images'])

    // Dev server: proxy your local WordPress URL for hot reloading
    .setUrl('http://localhost:3000')
    .setProxyUrl('https://mysite.test')
    .watch(['resources/views/**/*.blade.php', 'app/**/*.php'])

    // MUST match the URL path to your theme's public/ directory
    .setPublicPath('/app/themes/theme-name/public/')

    // Tailwind CSS via PostCSS
    .use(['@roots/bud-tailwindcss'])

    // Production: minify + hash for cache busting
    .when(bud.isProduction, () => bud.minimize().hash())
    .when(!bud.isProduction, () => bud.devtool('cheap-module-source-map'));
};
```

**`tailwind.config.js`:**

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './app/**/*.php',
    './resources/**/*.{php,vue,js,blade.php}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```

**`resources/styles/app.css`** -- standard Tailwind entry point:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## Pattern 3: Anonymous Blade Component in Sage

Sage stores anonymous Blade components in `resources/views/components/`. They receive props via `@props` and render with `<x-component-name>` syntax. Use WordPress escaping (`esc_url`, `esc_attr`, `esc_html`) -- Blade's `{{ }}` uses `htmlspecialchars`, not WordPress's context-aware escaping.

**`resources/views/components/card.blade.php`:**

```blade
@props([
    'title' => '',
    'image' => null,
    'url' => '#',
    'badge' => null,
    'excerpt' => '',
])

<article {{ $attributes->merge(['class' => 'bg-white rounded-lg shadow-md overflow-hidden']) }}>
  @if ($image)
    <a href="{{ esc_url($url) }}">
      <img
        src="{{ esc_url($image) }}"
        alt="{{ esc_attr($title) }}"
        class="w-full h-48 object-cover"
        loading="lazy"
      />
    </a>
  @endif

  <div class="p-6">
    @if ($badge)
      <span class="inline-block px-2 py-1 text-xs font-semibold bg-brand-50 text-brand-900 rounded mb-2">
        {{ esc_html($badge) }}
      </span>
    @endif

    <h3 class="text-lg font-bold mb-2">
      <a href="{{ esc_url($url) }}" class="hover:text-brand-500 transition-colors">
        {{ esc_html($title) }}
      </a>
    </h3>

    @if ($excerpt)
      <p class="text-gray-600 text-sm mb-4">{{ $excerpt }}</p>
    @endif

    @if ($slot->isNotEmpty())
      <div class="mt-4 pt-4 border-t border-gray-100">{{ $slot }}</div>
    @endif
  </div>
</article>
```

**Usage in a Blade view:**

```blade
<x-card
  :title="get_the_title()"
  :image="get_the_post_thumbnail_url(null, 'medium_large')"
  :url="get_permalink()"
  :excerpt="wp_trim_words(get_the_excerpt(), 20)"
>
  <time datetime="{{ get_the_date('c') }}" class="text-sm text-gray-500">
    {{ get_the_date() }}
  </time>
</x-card>
```

---

## Pattern 4: View Composer Passing WordPress Data to Blade

View composers bind data to specific Blade views automatically. Place them in `app/View/Composers/`. Sage auto-discovers composers extending `Roots\Acorn\View\Composer`.

```php
<?php

declare(strict_types=1);

namespace App\View\Composers;

use Roots\Acorn\View\Composer;

class NavigationComposer extends Composer
{
    /**
     * Views this composer is attached to.
     * Supports wildcards: 'partials.*' matches all partials.
     *
     * @var array<int, string>
     */
    protected static $views = [
        'sections.header',
        'sections.footer',
    ];

    /**
     * Data passed to every matched view.
     *
     * @return array<string, mixed>
     */
    public function with(): array
    {
        return [
            'primaryMenu' => $this->getMenu('primary_navigation'),
            'footerMenu' => $this->getMenu('footer_navigation'),
            'siteName' => get_bloginfo('name'),
            'siteUrl' => home_url('/'),
        ];
    }

    /**
     * @return array<int, object>|false
     */
    private function getMenu(string $location): array|false
    {
        $locations = get_nav_menu_locations();

        if (empty($locations[$location])) {
            return false;
        }

        $menu = wp_get_nav_menu_items($locations[$location]);

        if (! $menu) {
            return false;
        }

        return array_map(fn ($item) => (object) [
            'id' => $item->ID,
            'title' => $item->title,
            'url' => $item->url,
            'target' => $item->target ?: '_self',
            'classes' => implode(' ', array_filter($item->classes)),
            'isCurrent' => $item->current,
        ], $menu);
    }
}
```

**Using the data in `resources/views/sections/header.blade.php`:**

```blade
<header class="site-header bg-white shadow-sm">
  <div class="container mx-auto px-4 flex items-center justify-between h-16">
    <a href="{{ esc_url($siteUrl) }}">
      <span class="text-xl font-bold">{{ esc_html($siteName) }}</span>
    </a>

    @if ($primaryMenu)
      <nav>
        <ul class="flex space-x-6">
          @foreach ($primaryMenu as $item)
            <li>
              <a
                href="{{ esc_url($item->url) }}"
                @class([
                  'text-sm font-medium hover:text-brand-500',
                  'text-brand-500' => $item->isCurrent,
                  'text-gray-700' => ! $item->isCurrent,
                ])
              >
                {{ esc_html($item->title) }}
              </a>
            </li>
          @endforeach
        </ul>
      </nav>
    @endif
  </div>
</header>
```

---

## Pattern 5: Custom Blade Directive Registration

Register custom Blade directives in a Sage service provider to wrap common WordPress functions in clean Blade syntax. Place the provider in `app/Providers/`.

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class BladeDirectivesServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        $this->registerWordPressDirectives();
        $this->registerConditionalDirectives();
    }

    private function registerWordPressDirectives(): void
    {
        // @wphead -- outputs wp_head()
        Blade::directive('wphead', function () {
            return '<?php wp_head(); ?>';
        });

        // @wpfooter -- outputs wp_footer()
        Blade::directive('wpfooter', function () {
            return '<?php wp_footer(); ?>';
        });

        // @bodyclasses -- outputs body_class()
        Blade::directive('bodyclasses', function ($expression) {
            $classes = $expression ?: "''";

            return "<?php body_class({$classes}); ?>";
        });

        // @postmeta('field_name') -- escaped output of post meta
        Blade::directive('postmeta', function (string $expression) {
            return "<?php echo esc_html(get_post_meta(get_the_ID(), {$expression}, true)); ?>";
        });

        // @acf('field_name') -- output ACF field (if ACF is installed)
        Blade::directive('acf', function (string $expression) {
            return "<?php echo esc_html(function_exists('get_field') ? get_field({$expression}) : ''); ?>";
        });

        // @shortcode('[shortcode_here]')
        Blade::directive('shortcode', function (string $expression) {
            return "<?php echo do_shortcode({$expression}); ?>";
        });
    }

    private function registerConditionalDirectives(): void
    {
        // @role('administrator') ... @endrole
        Blade::if('role', function (string $role) {
            return is_user_logged_in() && current_user_can($role);
        });

        // @logged ... @endlogged
        Blade::if('logged', function () {
            return is_user_logged_in();
        });

        // @production ... @endproduction
        Blade::if('production', function () {
            return wp_get_environment_type() === 'production';
        });

        // @posttype('product') ... @endposttype
        Blade::if('posttype', function (string $type) {
            return get_post_type() === $type;
        });

        // @hasposts ... @endhasposts (check if current query has posts)
        Blade::if('hasposts', function () {
            global $wp_query;

            return $wp_query->have_posts();
        });
    }
}
```

**Usage in Blade templates:**

```blade
<html {!! get_language_attributes() !!}>
<head>@wphead</head>
<body @bodyclasses('custom-class')>

  @logged
    Welcome, {{ esc_html(wp_get_current_user()->display_name) }}
  @endlogged

  @role('administrator')
    <a href="{{ esc_url(admin_url()) }}">Dashboard</a>
  @endrole

  @posttype('product')
    @acf('product_subtitle')
  @endposttype

  @shortcode('[contact-form-7 id="123" title="Contact"]')

  @wpfooter
</body>
</html>
```

---

## Common Sage Gotchas

### Gotcha 1: Autoloading Timing with Acorn Boot Lifecycle

**Problem:** Code depends on the Acorn container but runs before it boots. WordPress fires hooks before `after_setup_theme`, but Acorn is not available yet. Calling `app()` before boot causes fatal errors.

```php
// BROKEN: This runs at file parse time, before Acorn boots
namespace App;

// Fatal: "app() is not defined" or "Container has not been bootstrapped"
$config = app('config')->get('theme.feature_flag');

class MyClass
{
    // BROKEN: Property initializers run at class load time
    private string $setting = app('config')->get('theme.setting');
}
```

**Solution:** Always access the container inside hook callbacks, method bodies, or service provider `boot()` / `register()` methods. These are guaranteed to run after Acorn has bootstrapped.

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class FeatureFlagServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // Safe: register() runs after the container is available
        $this->app->singleton('feature.flags', function ($app) {
            return $app->make('config')->get('theme.features', []);
        });
    }

    public function boot(): void
    {
        // Safe: boot() runs after all providers are registered
        $flags = $this->app->make('feature.flags');

        if ($flags['dark_mode'] ?? false) {
            add_action('wp_enqueue_scripts', function () {
                // Safe: this closure runs during a WP hook, well after boot
                wp_enqueue_style('dark-mode', asset('css/dark-mode.css')->uri());
            });
        }
    }
}
```

**Rule of thumb:** If you find yourself calling `app()` at the top level of a file, outside of any function, method, or closure, refactor it into a service provider or a hook callback.

### Gotcha 2: Mixing WordPress Template Hierarchy with Blade

**Problem:** Sage replaces `get_template_part()` with Blade views in `resources/views/`. Developers from classic WordPress create `single-product.php` in the theme root or call `get_template_part()` inside Blade, and it does not work.

```php
// BROKEN: Creating resources/views/single-product.blade.php expecting
// WordPress template hierarchy to find it automatically.
// Sage maps template hierarchy differently.

// BROKEN: Using get_template_part() inside Blade
@php
  get_template_part('template-parts/content', get_post_type());
@endphp
```

**Solution:** Use Blade includes and components, not `get_template_part()`. Template hierarchy mapping is configured in `app/filters.php` or a service provider.

Sage's template resolution:

```text
WordPress requests "single-product" template
  -> Sage maps to resources/views/single-product.blade.php
  -> Falls back to resources/views/single.blade.php
  -> Falls back to resources/views/index.blade.php
```

To add a custom template mapping, use the `template_include` filter:

```php
// In a service provider's boot() method or app/filters.php:
add_filter('template_include', function (string $template) {
    if (is_singular('portfolio')) {
        return get_theme_file_path('views/portfolio-single.blade.php') ?: $template;
    }

    return $template;
});
```

Use Blade includes and components instead of `get_template_part()`:

```blade
{{-- Instead of get_template_part('template-parts/content', 'post') --}}
@include('partials.content-' . get_post_type())

{{-- Or use a component for more structured data passing --}}
<x-post-card :post="$post" />

{{-- For WP loop iteration within Blade --}}
@while (have_posts())
  @php(the_post())
  @include('partials.content-' . get_post_type())
@endwhile
```

### Gotcha 3: Asset Versioning with Bud in Production

**Problem:** Bud generates hashed filenames in production and writes `public/entrypoints.json` to map them. If `setPublicPath()` is misconfigured, assets return 404 in production but work fine in development. Symptoms: assets load with `bud dev` but break after `bud build`, manifest points to wrong paths, stale hashes after re-deploy.

```javascript
// BROKEN: Missing or incorrect publicPath
export default async (bud) => {
  bud
    .entry({ app: ['@scripts/app', '@styles/app'] })
    // publicPath never set -- defaults to '/' which is wrong for WP themes
    .hash();
};
```

**Solution:** Always set `setPublicPath()` to match your theme's `public/` directory URL. Use `bundle()` from Acorn to resolve hashed filenames automatically.

```javascript
export default async (bud) => {
  bud
    .entry({
      app: ['@scripts/app', '@styles/app'],
      editor: ['@scripts/editor', '@styles/editor'],
    })
    // This MUST match the URL path to your theme's public/ directory
    .setPublicPath('/app/themes/your-theme/public/')
    // Enable hashing in production for cache busting
    .when(bud.isProduction, () => bud.hash().minimize());
};
```

**Enqueue assets in a service provider using Acorn's asset helper:**

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use function Roots\bundle;

class AssetServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        add_action('wp_enqueue_scripts', [$this, 'enqueueAssets']);
        add_action('enqueue_block_editor_assets', [$this, 'enqueueEditorAssets']);
    }

    public function enqueueAssets(): void
    {
        // bundle() reads entrypoints.json and resolves hashed filenames automatically
        bundle('app')->enqueue();
    }

    public function enqueueEditorAssets(): void
    {
        bundle('editor')->enqueue();
    }
}
```

**Deployment checklist:** Run `pnpm run build`, verify `public/entrypoints.json` exists with correct `publicPath`, and ensure `public/` is not gitignored in production. With Bedrock the theme path is typically `/app/themes/your-theme/public/` (not `/wp-content/themes/`).

---

## Best Practices Summary

1. **In Sage, never access `app()` at file top level.** The Acorn container is only available after `after_setup_theme`. Use service provider methods or WordPress hook callbacks.

2. **Use Blade components and `@include`, not `get_template_part()`.** Sage replaces the WordPress template part system. Embrace Blade's component model for reusable UI.

3. **Always set `setPublicPath()` in Bud config.** It must match the URL path to your theme's `public/` directory on the production server. Omitting it is the most common cause of broken production assets.

4. **Use view composers for WordPress data.** Never sprinkle `get_the_title()` and `get_field()` calls throughout Blade templates. Centralize WordPress data access in composers so templates receive clean, typed variables.

5. **Use `bundle()->enqueue()` for asset loading.** Acorn's bundle helper reads the Bud manifest and handles hashed filenames, dependencies, and script/style registration in one call.

6. **Register custom Blade directives for repeated WordPress patterns.** Wrapping `wp_head()`, `body_class()`, capability checks, and environment checks in directives keeps Blade templates clean and readable.

7. **Keep service providers focused.** One provider for theme support, one for assets, one for Blade directives. Small providers are easier to debug and disable selectively.

8. **Use WordPress escaping in Blade templates.** Blade's `{{ }}` uses `htmlspecialchars()`, but WordPress has context-aware escaping (`esc_url`, `esc_attr`, `esc_html`). Use the WordPress functions for URLs, attributes, and output that may contain WordPress-specific content.
