---
description: Run Technical SEO and Social Media Optimization Checks
globs: ["**/app/**/page.tsx", "**/app/layout.tsx", "**/components/seo/**/*.tsx"]
---
# Marketing: SEO & Social Optimization

<audit_rules>
- You MUST ensure every public-facing page exports a `generateMetadata` function or static `metadata` object (in Next.js) with accurate `title` and `description` tags.
- You MUST verify that Canonical URLs are dynamically generated and present on all indexable pages to prevent duplicate content penalties.
- You MUST implement Open Graph (`og:`) and Twitter (`twitter:`) meta tags for social media sharing, including optimized preview images (typically 1200x630px).
- You MUST verify proper HTML heading hierarchy (only one `<h1>` per page, followed sequentially by `<h2>`, `<h3>`).
- You MUST ensure semantic HTML structure and descriptive `alt` tags on all images for both accessibility and SEO.
</audit_rules>

<example_good>
```typescript
// app/blog/[slug]/page.tsx
import { Metadata } from 'next';

export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);
  
  return {
    title: `${post.title} | My Company`,
    description: post.excerpt,
    alternates: {
      canonical: `https://mycompany.com/blog/${post.slug}`,
    },
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.coverImage, width: 1200, height: 630 }],
    },
    twitter: {
      card: 'summary_large_image',
    }
  };
}
```
</example_good>

<example_bad>
```typescript
// BAD: Hardcoded, missing canonical and Open Graph
export const metadata = {
  title: 'Blog Post',
  description: 'Read our blog'
};
```
</example_bad>

