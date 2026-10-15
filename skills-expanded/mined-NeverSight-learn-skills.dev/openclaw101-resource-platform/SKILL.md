---
name: openclaw101-resource-platform
description: Build and contribute to OpenClaw 101, a Chinese-language resource aggregation platform for OpenClaw AI assistant tutorials and guides
triggers:
  - how do I add resources to openclaw101
  - set up the openclaw101 development environment
  - contribute a new tutorial to openclaw 101
  - customize the openclaw101 resource categories
  - deploy openclaw101 to cloudflare pages
  - structure resources in the openclaw101 platform
  - add new skill recommendations to openclaw101
  - translate openclaw101 content to english
---

# OpenClaw 101 Resource Platform Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## What is OpenClaw 101?

OpenClaw 101 is an open-source resource aggregation platform built with Next.js 14 and TypeScript. It serves as a comprehensive Chinese-language guide for [OpenClaw](https://github.com/openclaw/openclaw), collecting 35+ tutorials from platforms like Alibaba Cloud, Tencent Cloud, DigitalOcean, and Bilibili. The platform features:

- **Resource aggregation** with search and filtering
- **7-day learning path** (linked to Feishu knowledge base)
- **AI skill recommendations** by use case
- **Bilingual support** (Chinese and English)
- Category-based organization and tagging system

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/mengjian-github/openclaw101.git
cd openclaw101

# Install dependencies
npm install

# Start development server
npm run dev
```

Access at `http://localhost:3000`

## Build & Deploy

```bash
# Production build
npm run build

# Start production server
npm start

# Deploy to Cloudflare Pages
# (Typically automated via Git integration)
npm run build
```

## Project Structure

```
src/
├── app/
│   ├── page.tsx                    # Homepage
│   ├── resources/page.tsx          # Resources listing page
│   ├── layout.tsx                  # Root layout
│   └── globals.css                 # Global styles
├── components/
│   ├── Hero.tsx                    # Hero section
│   ├── WhatIs.tsx                  # Introduction section
│   ├── LearningPath.tsx            # 7-day learning path
│   ├── Skills.tsx                  # Skill recommendations
│   ├── ResourcesSection.tsx        # Featured resources
│   ├── Community.tsx               # Community section
│   ├── Navbar.tsx                  # Navigation
│   └── Footer.tsx                  # Footer
└── data/
    └── resources.ts                # Resource database
```

## Adding New Resources

The core of the platform is the resource database in `src/data/resources.ts`:

```typescript
// src/data/resources.ts
export interface Resource {
  title: string;
  desc: string;
  url: string;
  source: string;
  lang: 'zh' | 'en';
  category: 'official' | 'getting-started' | 'channel-integration' | 
            'skill-dev' | 'video' | 'deep-dive' | 'tools' | 'cloud-deploy';
  featured?: boolean;
  tags?: string[];
}

export const resources: Resource[] = [
  {
    title: 'OpenClaw 飞书接入完整指南',
    desc: '详细介绍如何将 OpenClaw 接入飞书平台的步骤',
    url: 'https://cloud.tencent.com/developer/article/2505478',
    source: '腾讯云',
    lang: 'zh',
    category: 'channel-integration',
    featured: true,
    tags: ['飞书', 'Lark', '接入'],
  },
  {
    title: 'Deploy OpenClaw on DigitalOcean',
    desc: 'One-click deployment guide for DigitalOcean platform',
    url: 'https://www.digitalocean.com/community/tutorials/how-to-deploy-openclaw',
    source: 'DigitalOcean',
    lang: 'en',
    category: 'cloud-deploy',
    featured: false,
    tags: ['deployment', 'cloud', 'VPS'],
  },
  // Add more resources...
];
```

### Resource Categories

| Category | Description |
|----------|-------------|
| `official` | Official OpenClaw documentation |
| `getting-started` | Installation and deployment tutorials |
| `channel-integration` | Platform integrations (Feishu, DingTalk, Telegram) |
| `skill-dev` | AI skill development guides |
| `video` | Video tutorials |
| `deep-dive` | In-depth analysis articles |
| `tools` | Tools and plugins |
| `cloud-deploy` | Cloud platform deployment guides |

## Component Development Patterns

### Creating a New Component

```typescript
// src/components/NewSection.tsx
import React from 'react';

export default function NewSection() {
  return (
    <section className="py-20 px-4">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
          Section Title
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Content grid */}
        </div>
      </div>
    </section>
  );
}
```

### Using Resources Data

```typescript
// Example: Filtering resources in a component
import { resources } from '@/data/resources';

export default function FeaturedResources() {
  const featured = resources.filter(r => r.featured);
  const chineseResources = resources.filter(r => r.lang === 'zh');
  const videoTutorials = resources.filter(r => r.category === 'video');

  return (
    <div>
      {featured.map((resource, idx) => (
        <div key={idx} className="border rounded-lg p-4 hover:shadow-lg transition">
          <h3 className="font-bold text-lg mb-2">{resource.title}</h3>
          <p className="text-gray-600 mb-3">{resource.desc}</p>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500">{resource.source}</span>
            <a 
              href={resource.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              阅读 →
            </a>
          </div>
        </div>
      ))}
    </div>
  );
}
```

## Resources Page Implementation

The resources page includes search and filtering:

```typescript
// src/app/resources/page.tsx
'use client';

import { useState, useMemo } from 'react';
import { resources } from '@/data/resources';

export default function ResourcesPage() {
  const [search, setSearch] = useState('');
  const [langFilter, setLangFilter] = useState<'all' | 'zh' | 'en'>('all');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');

  const filtered = useMemo(() => {
    return resources.filter(r => {
      const matchesSearch = r.title.toLowerCase().includes(search.toLowerCase()) ||
                           r.desc.toLowerCase().includes(search.toLowerCase());
      const matchesLang = langFilter === 'all' || r.lang === langFilter;
      const matchesCategory = categoryFilter === 'all' || r.category === categoryFilter;
      
      return matchesSearch && matchesLang && matchesCategory;
    });
  }, [search, langFilter, categoryFilter]);

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">资源库</h1>
      
      {/* Filters */}
      <div className="mb-8 flex flex-wrap gap-4">
        <input
          type="text"
          placeholder="搜索资源..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="px-4 py-2 border rounded-lg flex-1 min-w-[200px]"
        />
        
        <select 
          value={langFilter} 
          onChange={(e) => setLangFilter(e.target.value as any)}
          className="px-4 py-2 border rounded-lg"
        >
          <option value="all">全部语言</option>
          <option value="zh">中文</option>
          <option value="en">English</option>
        </select>
        
        <select 
          value={categoryFilter} 
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="px-4 py-2 border rounded-lg"
        >
          <option value="all">全部分类</option>
          <option value="getting-started">入门部署</option>
          <option value="channel-integration">平台接入</option>
          <option value="skill-dev">技能开发</option>
          {/* More categories */}
        </select>
      </div>

      {/* Results */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((resource, idx) => (
          <ResourceCard key={idx} resource={resource} />
        ))}
      </div>
    </div>
  );
}
```

## Styling with Tailwind CSS

Common utility patterns used in the project:

```typescript
// Container pattern
<div className="max-w-6xl mx-auto px-4">

// Responsive grid
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

// Card with hover effect
<div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">

// Button styles
<button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">

// Text gradients
<h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
```

## Configuration

### Next.js Configuration

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // For static export to Cloudflare Pages
  images: {
    unoptimized: true, // Required for static export
  },
};

module.exports = nextConfig;
```

### Tailwind Configuration

```javascript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // Custom theme extensions
    },
  },
  plugins: [],
};

export default config;
```

## Common Patterns

### Adding a New Learning Path Item

```typescript
// In src/components/LearningPath.tsx
const pathItems = [
  {
    day: 1,
    title: '认识 OpenClaw',
    desc: '了解基本概念、架构和使用场景',
  },
  {
    day: 2,
    title: '快速部署',
    desc: '选择云平台，完成首次部署',
  },
  // Add more days...
];
```

### Adding Skill Recommendations

```typescript
// In src/components/Skills.tsx
const skills = [
  {
    icon: '💬',
    title: 'Chat Integration',
    desc: '接入微信、飞书、Telegram 等聊天平台',
    tags: ['WeChat', 'Feishu', 'Telegram'],
  },
  {
    icon: '🤖',
    title: 'Custom AI Skills',
    desc: '开发专属的 AI 助手技能',
    tags: ['Python', 'JavaScript', 'API'],
  },
  // Add more skills...
];
```

### Creating External Links

```typescript
// Safe external link pattern
<a 
  href={resource.url}
  target="_blank"
  rel="noopener noreferrer"
  className="text-blue-600 hover:underline"
>
  {resource.title}
</a>
```

## Troubleshooting

### Build Errors

**Issue**: `Type error: Property does not exist on type`

**Solution**: Ensure resource types match the interface:

```typescript
// Check src/data/resources.ts
const newResource: Resource = {
  title: string,
  desc: string,
  url: string,
  source: string,
  lang: 'zh' | 'en',
  category: /* valid category */,
  // Optional fields
  featured: boolean,
  tags: string[],
};
```

### Deployment Issues

**Issue**: Static export fails with image optimization

**Solution**: Set `images.unoptimized: true` in `next.config.js`

**Issue**: 404 on client-side navigation

**Solution**: Ensure proper routing in `app/` directory structure

### Development Server Issues

**Issue**: Changes not reflecting

**Solution**: 
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

## Testing Locally

```bash
# Development mode
npm run dev

# Production build test
npm run build
npm start

# Type checking
npx tsc --noEmit

# Lint
npm run lint
```

## Contributing Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-resources`
3. Add resources to `src/data/resources.ts`
4. Test locally: `npm run dev`
5. Commit changes: `git commit -m "Add 5 new OpenClaw tutorials"`
6. Push and create PR

## Key Files to Modify

- **Add resources**: `src/data/resources.ts`
- **Edit homepage**: `src/app/page.tsx`
- **Edit resources page**: `src/app/resources/page.tsx`
- **Add components**: `src/components/`
- **Global styles**: `src/app/globals.css`
- **Site metadata**: `src/app/layout.tsx`
