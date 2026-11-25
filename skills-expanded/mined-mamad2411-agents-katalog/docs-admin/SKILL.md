---
name: docs-admin
description: 어드민 문서 자동 뷰어 - 모든 가이드를 한 곳에서 관리
triggers:
  - docs
  - 문서
  - 가이드뷰어
  - documentation
---

# 어드민 문서 자동 뷰어

> 모든 KreatSaaS 가이드를 어드민 대시보드에서 한 곳에서 관리하고 열람

---

## 1. 자동 문서 로더

### 문서 스캔 유틸리티

```typescript
// src/lib/docs/scanner.ts
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';

export type DocCategory =
  | 'beginner'      // 초보자 가이드
  | 'setup'         // 설치 가이드
  | 'development'   // 개발 가이드
  | 'deployment'    // 배포 가이드
  | 'enhancement'   // 고도화 가이드
  | 'seo'           // SEO 가이드
  | 'admin'         // 어드민 가이드
  | 'api';          // API 가이드

export interface DocMeta {
  slug: string;
  title: string;
  description: string;
  category: DocCategory;
  order: number;
  lastUpdated: string;
  triggers?: string[];
}

export interface DocFile extends DocMeta {
  content: string;
}

// KreatSaaS 스킬 디렉토리에서 모든 문서 스캔
export async function scanDocs(skillsDir: string): Promise<DocMeta[]> {
  const docs: DocMeta[] = [];

  try {
    const skillFolders = await fs.readdir(skillsDir);

    for (const folder of skillFolders) {
      const skillPath = path.join(skillsDir, folder, 'SKILL.md');

      try {
        const content = await fs.readFile(skillPath, 'utf-8');
        const { data, content: body } = matter(content);

        docs.push({
          slug: folder,
          title: data.name || folder,
          description: data.description || '',
          category: getCategoryFromSlug(folder),
          order: getCategoryOrder(folder),
          lastUpdated: (await fs.stat(skillPath)).mtime.toISOString(),
          triggers: data.triggers || [],
        });
      } catch {
        // 파일이 없으면 스킵
      }
    }
  } catch (error) {
    console.error('Error scanning docs:', error);
  }

  return docs.sort((a, b) => a.order - b.order);
}

// 문서 내용 가져오기
export async function getDoc(skillsDir: string, slug: string): Promise<DocFile | null> {
  const skillPath = path.join(skillsDir, slug, 'SKILL.md');

  try {
    const content = await fs.readFile(skillPath, 'utf-8');
    const { data, content: body } = matter(content);
    const stat = await fs.stat(skillPath);

    return {
      slug,
      title: data.name || slug,
      description: data.description || '',
      category: getCategoryFromSlug(slug),
      order: getCategoryOrder(slug),
      lastUpdated: stat.mtime.toISOString(),
      triggers: data.triggers || [],
      content: body,
    };
  } catch {
    return null;
  }
}

function getCategoryFromSlug(slug: string): DocCategory {
  const categoryMap: Record<string, DocCategory> = {
    'beginner-guide': 'beginner',
    'setup-guide': 'setup',
    'enhancement-guide': 'enhancement',
    'seo-guide': 'seo',
    'admin-guide': 'admin',
    'docs-admin': 'admin',
    'saas-design': 'development',
    'llm-auto-update': 'development',
  };
  return categoryMap[slug] || 'development';
}

function getCategoryOrder(slug: string): number {
  const orderMap: Record<string, number> = {
    'beginner-guide': 1,
    'setup-guide': 2,
    'saas-design': 3,
    'admin-guide': 4,
    'enhancement-guide': 5,
    'seo-guide': 6,
    'llm-auto-update': 7,
    'docs-admin': 8,
  };
  return orderMap[slug] || 99;
}
```

### 필요 패키지

```bash
npm install gray-matter
npm install react-markdown remark-gfm rehype-highlight
```

---

## 2. 어드민 문서 페이지

### 문서 목록 페이지

```typescript
// src/app/admin/docs/page.tsx
import Link from 'next/link';
import { scanDocs, DocCategory } from '@/lib/docs/scanner';
import { Book, Code, Rocket, Settings, Search, Zap } from 'lucide-react';

const categoryInfo: Record<DocCategory, { icon: any; label: string; color: string }> = {
  beginner: { icon: Book, label: '초보자 가이드', color: 'bg-green-100 text-green-800' },
  setup: { icon: Settings, label: '설치 가이드', color: 'bg-blue-100 text-blue-800' },
  development: { icon: Code, label: '개발 가이드', color: 'bg-purple-100 text-purple-800' },
  deployment: { icon: Rocket, label: '배포 가이드', color: 'bg-orange-100 text-orange-800' },
  enhancement: { icon: Zap, label: '고도화 가이드', color: 'bg-yellow-100 text-yellow-800' },
  seo: { icon: Search, label: 'SEO 가이드', color: 'bg-pink-100 text-pink-800' },
  admin: { icon: Settings, label: '어드민 가이드', color: 'bg-red-100 text-red-800' },
  api: { icon: Code, label: 'API 가이드', color: 'bg-indigo-100 text-indigo-800' },
};

export default async function DocsPage() {
  const skillsDir = process.env.KREATSAAS_SKILLS_DIR || './skills';
  const docs = await scanDocs(skillsDir);

  // 카테고리별 그룹화
  const groupedDocs = docs.reduce((acc, doc) => {
    if (!acc[doc.category]) {
      acc[doc.category] = [];
    }
    acc[doc.category].push(doc);
    return acc;
  }, {} as Record<DocCategory, typeof docs>);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">문서 가이드</h1>
        <span className="text-sm text-gray-500">
          총 {docs.length}개 문서
        </span>
      </div>

      {Object.entries(groupedDocs).map(([category, categoryDocs]) => {
        const info = categoryInfo[category as DocCategory];
        const Icon = info.icon;

        return (
          <div key={category} className="space-y-4">
            <div className="flex items-center gap-2">
              <div className={`p-2 rounded-lg ${info.color}`}>
                <Icon className="w-5 h-5" />
              </div>
              <h2 className="text-lg font-semibold">{info.label}</h2>
              <span className="text-sm text-gray-400">({categoryDocs.length})</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {categoryDocs.map((doc) => (
                <Link
                  key={doc.slug}
                  href={`/admin/docs/${doc.slug}`}
                  className="block p-4 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow"
                >
                  <h3 className="font-medium text-gray-900 mb-2">{doc.title}</h3>
                  <p className="text-sm text-gray-500 line-clamp-2 mb-3">
                    {doc.description}
                  </p>
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <span>업데이트: {new Date(doc.lastUpdated).toLocaleDateString('ko-KR')}</span>
                    {doc.triggers && doc.triggers.length > 0 && (
                      <span className="bg-gray-100 px-2 py-1 rounded">
                        {doc.triggers[0]}
                      </span>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
```

### 문서 상세 페이지

```typescript
// src/app/admin/docs/[slug]/page.tsx
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getDoc, scanDocs } from '@/lib/docs/scanner';
import { MarkdownRenderer } from '@/components/admin/MarkdownRenderer';
import { ArrowLeft, Edit, Clock, Tag } from 'lucide-react';

export async function generateStaticParams() {
  const skillsDir = process.env.KREATSAAS_SKILLS_DIR || './skills';
  const docs = await scanDocs(skillsDir);
  return docs.map((doc) => ({ slug: doc.slug }));
}

export default async function DocDetailPage({
  params,
}: {
  params: { slug: string };
}) {
  const skillsDir = process.env.KREATSAAS_SKILLS_DIR || './skills';
  const doc = await getDoc(skillsDir, params.slug);

  if (!doc) {
    notFound();
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* 헤더 */}
      <div className="mb-8">
        <Link
          href="/admin/docs"
          className="inline-flex items-center gap-2 text-gray-500 hover:text-gray-700 mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          문서 목록으로
        </Link>

        <h1 className="text-3xl font-bold text-gray-900 mb-2">{doc.title}</h1>
        <p className="text-gray-600 mb-4">{doc.description}</p>

        <div className="flex items-center gap-4 text-sm text-gray-500">
          <span className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            {new Date(doc.lastUpdated).toLocaleDateString('ko-KR')}
          </span>
          {doc.triggers && doc.triggers.length > 0 && (
            <span className="flex items-center gap-1">
              <Tag className="w-4 h-4" />
              {doc.triggers.join(', ')}
            </span>
          )}
        </div>
      </div>

      {/* 콘텐츠 */}
      <div className="bg-white rounded-xl shadow-sm p-8">
        <MarkdownRenderer content={doc.content} />
      </div>

      {/* 하단 네비게이션 */}
      <div className="mt-8 pt-8 border-t flex justify-between">
        <Link
          href="/admin/docs"
          className="text-blue-600 hover:text-blue-800"
        >
          ← 목록으로
        </Link>
        <button className="flex items-center gap-2 text-gray-500 hover:text-gray-700">
          <Edit className="w-4 h-4" />
          수정 요청
        </button>
      </div>
    </div>
  );
}
```

### 마크다운 렌더러

```typescript
// src/components/admin/MarkdownRenderer.tsx
'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github-dark.css';

type Props = {
  content: string;
};

export function MarkdownRenderer({ content }: Props) {
  return (
    <ReactMarkdown
      className="prose prose-lg max-w-none"
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeHighlight]}
      components={{
        // 코드 블록 스타일링
        pre: ({ children }) => (
          <pre className="bg-gray-900 rounded-lg overflow-x-auto">
            {children}
          </pre>
        ),
        code: ({ inline, className, children }) => {
          if (inline) {
            return (
              <code className="bg-gray-100 text-red-600 px-1 py-0.5 rounded text-sm">
                {children}
              </code>
            );
          }
          return <code className={className}>{children}</code>;
        },
        // 테이블 스타일링
        table: ({ children }) => (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              {children}
            </table>
          </div>
        ),
        // 체크박스 스타일링
        input: ({ type, checked }) => {
          if (type === 'checkbox') {
            return (
              <input
                type="checkbox"
                checked={checked}
                readOnly
                className="mr-2 rounded"
              />
            );
          }
          return <input type={type} />;
        },
        // 링크 새 탭에서 열기
        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800"
          >
            {children}
          </a>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
```

---

## 3. 사이드바에 문서 메뉴 추가

```typescript
// src/components/admin/Sidebar.tsx 수정
const menuItems = [
  { href: '/admin', icon: LayoutDashboard, label: '대시보드' },
  { href: '/admin/users', icon: Users, label: '사용자 관리' },
  { href: '/admin/analytics', icon: BarChart3, label: '통계' },
  { href: '/admin/subscriptions', icon: CreditCard, label: '구독 관리' },
  { href: '/admin/content', icon: FileText, label: '콘텐츠' },
  { href: '/admin/docs', icon: Book, label: '문서 가이드' },  // 추가
  { href: '/admin/settings', icon: Settings, label: '설정' },
];
```

---

## 4. 문서 자동 업데이트 API

### 문서 동기화 API

```typescript
// src/app/api/admin/docs/sync/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { withPermission } from '@/lib/admin/auth';
import { scanDocs, getDoc } from '@/lib/docs/scanner';
import { prisma } from '@/lib/prisma';

// 문서를 DB에 동기화
export const POST = withPermission('settings:write', async (req) => {
  const skillsDir = process.env.KREATSAAS_SKILLS_DIR || './skills';
  const docs = await scanDocs(skillsDir);

  const results = [];

  for (const docMeta of docs) {
    const doc = await getDoc(skillsDir, docMeta.slug);
    if (!doc) continue;

    // DB에 upsert
    const result = await prisma.doc.upsert({
      where: { slug: doc.slug },
      create: {
        slug: doc.slug,
        title: doc.title,
        description: doc.description,
        category: doc.category,
        content: doc.content,
        order: doc.order,
        triggers: doc.triggers || [],
        lastUpdated: new Date(doc.lastUpdated),
      },
      update: {
        title: doc.title,
        description: doc.description,
        category: doc.category,
        content: doc.content,
        order: doc.order,
        triggers: doc.triggers || [],
        lastUpdated: new Date(doc.lastUpdated),
      },
    });

    results.push(result);
  }

  return NextResponse.json({
    success: true,
    synced: results.length,
    docs: results.map((r) => ({ slug: r.slug, title: r.title })),
  });
});
```

### 문서 검색 API

```typescript
// src/app/api/admin/docs/search/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { withPermission } from '@/lib/admin/auth';
import { prisma } from '@/lib/prisma';

export const GET = withPermission('admin:access', async (req) => {
  const { searchParams } = new URL(req.url);
  const query = searchParams.get('q') || '';
  const category = searchParams.get('category');

  const docs = await prisma.doc.findMany({
    where: {
      AND: [
        query
          ? {
              OR: [
                { title: { contains: query, mode: 'insensitive' } },
                { description: { contains: query, mode: 'insensitive' } },
                { content: { contains: query, mode: 'insensitive' } },
                { triggers: { has: query } },
              ],
            }
          : {},
        category ? { category } : {},
      ],
    },
    select: {
      slug: true,
      title: true,
      description: true,
      category: true,
      lastUpdated: true,
    },
    orderBy: { order: 'asc' },
  });

  return NextResponse.json(docs);
});
```

---

## 5. 문서 DB 스키마

```prisma
// prisma/schema.prisma 추가

model Doc {
  id          String   @id @default(cuid())
  slug        String   @unique
  title       String
  description String
  category    String
  content     String   @db.Text
  order       Int      @default(99)
  triggers    String[]
  lastUpdated DateTime
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([category])
  @@index([title])
}
```

---

## 6. 실시간 문서 검색 컴포넌트

```typescript
// src/components/admin/DocSearch.tsx
'use client';

import { useState, useEffect } from 'react';
import { useDebounce } from '@/hooks/useDebounce';
import { Search, X } from 'lucide-react';
import Link from 'next/link';

type SearchResult = {
  slug: string;
  title: string;
  description: string;
  category: string;
};

export function DocSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery.length < 2) {
      setResults([]);
      return;
    }

    async function search() {
      const res = await fetch(`/api/admin/docs/search?q=${encodeURIComponent(debouncedQuery)}`);
      const data = await res.json();
      setResults(data);
    }

    search();
  }, [debouncedQuery]);

  return (
    <div className="relative">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder="문서 검색... (제목, 키워드)"
          className="w-full pl-10 pr-10 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        />
        {query && (
          <button
            onClick={() => {
              setQuery('');
              setResults([]);
            }}
            className="absolute right-3 top-1/2 -translate-y-1/2"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        )}
      </div>

      {/* 검색 결과 */}
      {isOpen && results.length > 0 && (
        <div className="absolute top-full mt-2 w-full bg-white rounded-lg shadow-lg border z-50 max-h-96 overflow-y-auto">
          {results.map((result) => (
            <Link
              key={result.slug}
              href={`/admin/docs/${result.slug}`}
              onClick={() => {
                setIsOpen(false);
                setQuery('');
              }}
              className="block p-4 hover:bg-gray-50 border-b last:border-b-0"
            >
              <div className="font-medium text-gray-900">{result.title}</div>
              <div className="text-sm text-gray-500 line-clamp-1">
                {result.description}
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {result.category}
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* 검색 결과 없음 */}
      {isOpen && query.length >= 2 && results.length === 0 && (
        <div className="absolute top-full mt-2 w-full bg-white rounded-lg shadow-lg border z-50 p-4 text-center text-gray-500">
          검색 결과가 없습니다
        </div>
      )}
    </div>
  );
}
```

---

## 7. 문서 자동 업데이트 설정

### 환경변수

```env
# .env.local
KREATSAAS_SKILLS_DIR=./skills
DOCS_AUTO_SYNC=true
DOCS_SYNC_INTERVAL=3600000  # 1시간마다
```

### 자동 동기화 스케줄러

```typescript
// src/lib/docs/scheduler.ts
import cron from 'node-cron';
import { syncDocs } from './sync';

export function startDocsSyncScheduler() {
  // 매시간 문서 동기화
  cron.schedule('0 * * * *', async () => {
    console.log('[Docs] Starting automatic sync...');
    try {
      const result = await syncDocs();
      console.log(`[Docs] Synced ${result.synced} documents`);
    } catch (error) {
      console.error('[Docs] Sync failed:', error);
    }
  });

  console.log('[Docs] Scheduler started - syncing every hour');
}
```

---

## 8. 문서 관리 체크리스트

```
┌─────────────────────────────────────────────────────────────┐
│ 📚 문서 관리 체크리스트                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ □ gray-matter 패키지 설치                                    │
│ □ react-markdown, remark-gfm 설치                           │
│ □ rehype-highlight 설치                                      │
│ □ Doc 모델 DB 마이그레이션                                   │
│ □ /admin/docs 페이지 구현                                    │
│ □ /admin/docs/[slug] 상세 페이지 구현                        │
│ □ MarkdownRenderer 컴포넌트 구현                             │
│ □ 사이드바에 문서 메뉴 추가                                  │
│ □ 문서 검색 API 구현                                         │
│ □ 문서 동기화 API 구현                                       │
│ □ 자동 동기화 스케줄러 설정 (선택)                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```
