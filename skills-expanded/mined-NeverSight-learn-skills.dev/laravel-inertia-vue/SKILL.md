---
name: laravel-inertia-vue
description: Laravel + Inertia.js + Vue 3 integration patterns. Use when building Inertia page components, handling forms with useForm composable, managing shared data, or implementing persistent layouts. Triggers on tasks involving Inertia.js, page props, form handling, or Laravel Vue integration.
license: MIT
metadata:
  author: Jasim K
  version: "1.0.0"
  laravelVersion: "12.x"
  phpVersion: "8.3+"
---

# Laravel + Inertia.js + Vue 3

Comprehensive patterns for building modern monolithic applications with Laravel, Inertia.js, and Vue 3. Contains 30+ rules for seamless full-stack development.

## When to Apply

Reference these guidelines when:
- Creating Inertia page components with Vue 3
- Handling forms with useForm composable
- Managing shared data and authentication
- Implementing persistent layouts
- Navigating between pages

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Page Components | CRITICAL | `page-` |
| 2 | Forms & Validation | CRITICAL | `form-` |
| 3 | Navigation & Links | HIGH | `nav-` |
| 4 | Shared Data | HIGH | `shared-` |
| 5 | Layouts | MEDIUM | `layout-` |
| 6 | File Uploads | MEDIUM | `upload-` |
| 7 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Page Components (CRITICAL)

- `page-props-typing` - Type page props from Laravel
- `page-component-structure` - Standard page component pattern
- `page-head-management` - Title and meta tags with Head
- `page-default-layout` - Assign layouts to pages

### 2. Forms & Validation (CRITICAL)

- `form-useform-basic` - Basic useForm usage
- `form-validation-errors` - Display Laravel validation errors
- `form-processing-state` - Handle form submission state
- `form-reset-preserve` - Reset vs preserve form data
- `form-transform` - Transform data before submit

### 3. Navigation & Links (HIGH)

- `nav-link-component` - Use Link for navigation
- `nav-preserve-state` - Preserve scroll and state
- `nav-partial-reloads` - Reload only what changed
- `nav-replace-history` - Replace vs push history

### 4. Shared Data (HIGH)

- `shared-auth-user` - Access authenticated user
- `shared-flash-messages` - Handle flash messages
- `shared-global-props` - Access global props
- `shared-typescript` - Type shared data

### 5. Layouts (MEDIUM)

- `layout-persistent` - Persistent layouts pattern
- `layout-nested` - Nested layouts
- `layout-default` - Default layout assignment
- `layout-conditional` - Conditional layouts

### 6. File Uploads (MEDIUM)

- `upload-basic` - Basic file upload
- `upload-progress` - Upload progress tracking
- `upload-multiple` - Multiple file uploads

### 7. Advanced Patterns (LOW)

- `advanced-polling` - Real-time polling
- `advanced-prefetch` - Prefetch pages
- `advanced-modal-pages` - Modal as pages
- `advanced-infinite-scroll` - Infinite scrolling

## Essential Patterns

### Page Component with TypeScript

```vue
<!-- resources/js/Pages/Posts/Index.vue -->
<script setup lang="ts">
import { Head, Link } from '@inertiajs/vue3'

interface Post {
  id: number
  title: string
  excerpt: string
  created_at: string
  author: {
    id: number
    name: string
  }
}

interface Props {
  posts: {
    data: Post[]
    links: { url: string | null; label: string; active: boolean }[]
  }
  filters: {
    search?: string
  }
}

const props = defineProps<Props>()
</script>

<template>
  <Head title="Posts" />

  <div class="container mx-auto py-8">
    <h1 class="text-2xl font-bold mb-6">Posts</h1>

    <div class="space-y-4">
      <article
        v-for="post in props.posts.data"
        :key="post.id"
        class="p-4 bg-white rounded-lg shadow"
      >
        <Link :href="route('posts.show', post.id)">
          <h2 class="text-xl font-semibold hover:text-blue-600">
            {{ post.title }}
          </h2>
        </Link>
        <p class="text-gray-600 mt-2">{{ post.excerpt }}</p>
        <p class="text-sm text-gray-400 mt-2">By {{ post.author.name }}</p>
      </article>
    </div>
  </div>
</template>
```

### Form with useForm

```vue
<!-- resources/js/Pages/Posts/Create.vue -->
<script setup lang="ts">
import { Head, Link, useForm } from '@inertiajs/vue3'

interface Category {
  id: number
  name: string
}

interface Props {
  categories: Category[]
}

const props = defineProps<Props>()

const form = useForm({
  title: '',
  body: '',
  category_id: '',
})

function submit() {
  form.post(route('posts.store'), {
    onSuccess: () => form.reset(),
  })
}
</script>

<template>
  <Head title="Create Post" />

  <form @submit.prevent="submit" class="max-w-2xl mx-auto py-8">
    <div class="mb-4">
      <label for="title" class="block font-medium mb-1">Title</label>
      <input
        id="title"
        v-model="form.title"
        type="text"
        class="w-full border rounded px-3 py-2"
      />
      <p v-if="form.errors.title" class="text-red-500 text-sm mt-1">
        {{ form.errors.title }}
      </p>
    </div>

    <div class="mb-4">
      <label for="category" class="block font-medium mb-1">Category</label>
      <select
        id="category"
        v-model="form.category_id"
        class="w-full border rounded px-3 py-2"
      >
        <option value="">Select a category</option>
        <option v-for="cat in props.categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>
      <p v-if="form.errors.category_id" class="text-red-500 text-sm mt-1">
        {{ form.errors.category_id }}
      </p>
    </div>

    <div class="mb-4">
      <label for="body" class="block font-medium mb-1">Content</label>
      <textarea
        id="body"
        v-model="form.body"
        rows="10"
        class="w-full border rounded px-3 py-2"
      />
      <p v-if="form.errors.body" class="text-red-500 text-sm mt-1">
        {{ form.errors.body }}
      </p>
    </div>

    <div class="flex gap-4">
      <button
        type="submit"
        :disabled="form.processing"
        class="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {{ form.processing ? 'Creating...' : 'Create Post' }}
      </button>

      <Link :href="route('posts.index')" class="px-4 py-2 border rounded">
        Cancel
      </Link>
    </div>
  </form>
</template>
```

### Persistent Layout

```vue
<!-- resources/js/Layouts/AppLayout.vue -->
<script setup lang="ts">
import { Link, usePage } from '@inertiajs/vue3'
import { computed } from 'vue'

const page = usePage()
const auth = computed(() => page.props.auth as { user: { name: string } })
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow">
      <div class="container mx-auto px-4 py-3 flex justify-between">
        <Link href="/" class="font-bold">My App</Link>
        <span>Welcome, {{ auth.user.name }}</span>
      </div>
    </nav>

    <main class="container mx-auto px-4 py-8">
      <slot />
    </main>
  </div>
</template>
```

```vue
<!-- resources/js/Pages/Dashboard.vue -->
<script setup lang="ts">
import AppLayout from '@/Layouts/AppLayout.vue'

defineOptions({ layout: AppLayout })
</script>

<template>
  <h1>Dashboard</h1>
</template>
```

### Laravel Controller

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\StorePostRequest;
use App\Models\Post;
use App\Models\Category;
use Illuminate\Http\RedirectResponse;
use Inertia\Inertia;
use Inertia\Response;

class PostController extends Controller
{
    public function index(): Response
    {
        return Inertia::render('Posts/Index', [
            'posts' => Post::with('author:id,name')
                ->latest()
                ->paginate(10),
            'filters' => request()->only('search'),
        ]);
    }

    public function create(): Response
    {
        return Inertia::render('Posts/Create', [
            'categories' => Category::all(['id', 'name']),
        ]);
    }

    public function store(StorePostRequest $request): RedirectResponse
    {
        $post = Post::create([
            ...$request->validated(),
            'user_id' => auth()->id(),
        ]);

        return redirect()
            ->route('posts.show', $post)
            ->with('success', 'Post created successfully.');
    }

    public function show(Post $post): Response
    {
        return Inertia::render('Posts/Show', [
            'post' => $post->load('author', 'category'),
        ]);
    }
}
```

### Shared Data (HandleInertiaRequests)

```php
<?php

namespace App\Http\Middleware;

use Illuminate\Http\Request;
use Inertia\Middleware;

class HandleInertiaRequests extends Middleware
{
    public function share(Request $request): array
    {
        return array_merge(parent::share($request), [
            'auth' => [
                'user' => $request->user() ? [
                    'id' => $request->user()->id,
                    'name' => $request->user()->name,
                    'email' => $request->user()->email,
                ] : null,
            ],
            'flash' => [
                'success' => $request->session()->get('success'),
                'error' => $request->session()->get('error'),
            ],
        ]);
    }
}
```

### Flash Messages Component

```vue
<!-- resources/js/Components/FlashMessages.vue -->
<script setup lang="ts">
import { usePage } from '@inertiajs/vue3'
import { computed, ref, watch } from 'vue'

const page = usePage()
const flash = computed(() => page.props.flash as { success?: string; error?: string })
const visible = ref(false)
let timer: ReturnType<typeof setTimeout> | null = null

watch(flash, (newFlash) => {
  if (newFlash.success || newFlash.error) {
    visible.value = true
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      visible.value = false
    }, 3000)
  }
}, { deep: true })
</script>

<template>
  <div v-if="visible" class="fixed top-4 right-4 z-50">
    <div
      v-if="flash.success"
      class="bg-green-500 text-white px-4 py-2 rounded shadow"
    >
      {{ flash.success }}
    </div>
    <div
      v-if="flash.error"
      class="bg-red-500 text-white px-4 py-2 rounded shadow"
    >
      {{ flash.error }}
    </div>
  </div>
</template>
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/form-useform-basic.md
rules/page-props-typing.md
rules/layout-persistent.md
```

## Project Structure

```
laravel-inertia-vue/
├── SKILL.md                 # This file - overview and examples
├── README.md                # Quick reference guide
├── AGENTS.md                # Integration guide for AI agents
├── metadata.json            # Skill metadata and references
└── rules/
    ├── _sections.md         # Rule categories and priorities
    ├── _template.md         # Template for new rules
    ├── page-*.md            # Page component patterns (6 rules)
    ├── form-*.md            # Form handling patterns (8 rules)
    ├── nav-*.md             # Navigation patterns (5 rules)
    ├── shared-*.md          # Shared data patterns (4 rules)
    └── layout-*.md          # Layout patterns (1 rule)
```

## References

- [Inertia.js Documentation](https://inertiajs.com/) - Official Inertia.js docs
- [Laravel Documentation](https://laravel.com/docs) - Laravel framework docs
- [Vue 3 Documentation](https://vuejs.org/) - Official Vue 3 docs
- [Ziggy](https://github.com/tighten/ziggy) - Laravel route helper for JavaScript

## License

MIT License. This skill is provided as-is for educational and development purposes.

## Metadata

- **Version**: 1.0.0
- **Last Updated**: 2026-03-17
- **Maintainer**: Jasim K
- **Rule Count**: 24 rules across 6 categories
- **Tech Stack**: Laravel 12+, Inertia.js 2.0+, Vue 3.3+, TypeScript 5+
