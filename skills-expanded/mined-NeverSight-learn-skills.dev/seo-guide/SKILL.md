---
name: seo-guide
description: SaaS SEO 최적화 가이드 - 검색엔진 상위 노출을 위한 완벽 가이드
triggers:
  - SEO
  - 검색
  - 메타태그
  - sitemap
  - 구글
---

# SaaS SEO 최적화 가이드

> SaaS 프로젝트의 검색엔진 최적화(SEO)를 위한 완벽 가이드

---

## 1. 메타태그 설정

### Next.js App Router (권장)

```typescript
// src/app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  // 기본 메타데이터
  title: {
    default: 'MySaaS - 서비스 설명',
    template: '%s | MySaaS',
  },
  description: '서비스에 대한 150-160자 설명. 핵심 키워드 포함.',
  keywords: ['SaaS', '키워드1', '키워드2', '키워드3'],
  authors: [{ name: 'Your Name' }],
  creator: 'Your Company',
  publisher: 'Your Company',

  // 로봇 설정
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },

  // Open Graph (소셜 공유)
  openGraph: {
    type: 'website',
    locale: 'ko_KR',
    url: 'https://mysaas.com',
    siteName: 'MySaaS',
    title: 'MySaaS - 서비스 설명',
    description: '서비스에 대한 설명',
    images: [
      {
        url: 'https://mysaas.com/og-image.png',
        width: 1200,
        height: 630,
        alt: 'MySaaS',
      },
    ],
  },

  // Twitter Card
  twitter: {
    card: 'summary_large_image',
    title: 'MySaaS - 서비스 설명',
    description: '서비스에 대한 설명',
    images: ['https://mysaas.com/twitter-image.png'],
    creator: '@yourhandle',
  },

  // 아이콘
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },

  // 기타
  manifest: '/manifest.json',
  alternates: {
    canonical: 'https://mysaas.com',
    languages: {
      'ko-KR': 'https://mysaas.com/ko',
      'en-US': 'https://mysaas.com/en',
    },
  },

  // 검증
  verification: {
    google: 'google-site-verification-code',
    naver: 'naver-site-verification-code',
  },
};
```

### 동적 페이지 메타데이터

```typescript
// src/app/blog/[slug]/page.tsx
import { Metadata } from 'next';

type Props = {
  params: { slug: string };
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
      type: 'article',
      publishedTime: post.publishedAt,
      authors: [post.author.name],
    },
  };
}
```

---

## 2. Sitemap 생성

### 정적 Sitemap

```typescript
// src/app/sitemap.ts
import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://mysaas.com';

  // 정적 페이지
  const staticPages = [
    '',
    '/features',
    '/pricing',
    '/about',
    '/contact',
    '/blog',
  ].map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: route === '' ? 1 : 0.8,
  }));

  return staticPages;
}
```

### 동적 Sitemap (블로그 포함)

```typescript
// src/app/sitemap.ts
import { MetadataRoute } from 'next';
import { getAllPosts } from '@/lib/blog';
import { getAllProducts } from '@/lib/products';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://mysaas.com';

  // 정적 페이지
  const staticPages = [
    { url: baseUrl, priority: 1 },
    { url: `${baseUrl}/features`, priority: 0.9 },
    { url: `${baseUrl}/pricing`, priority: 0.9 },
    { url: `${baseUrl}/blog`, priority: 0.8 },
  ].map((page) => ({
    ...page,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
  }));

  // 블로그 포스트
  const posts = await getAllPosts();
  const blogPages = posts.map((post) => ({
    url: `${baseUrl}/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'monthly' as const,
    priority: 0.6,
  }));

  // 제품 페이지
  const products = await getAllProducts();
  const productPages = products.map((product) => ({
    url: `${baseUrl}/products/${product.slug}`,
    lastModified: new Date(product.updatedAt),
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  return [...staticPages, ...blogPages, ...productPages];
}
```

---

## 3. Robots.txt

```typescript
// src/app/robots.ts
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const baseUrl = 'https://mysaas.com';

  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: [
          '/api/',
          '/admin/',
          '/dashboard/',
          '/private/',
          '/*.json$',
        ],
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  };
}
```

---

## 4. 구조화된 데이터 (JSON-LD)

### 조직 정보

```typescript
// src/components/JsonLd.tsx
export function OrganizationJsonLd() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'MySaaS',
    url: 'https://mysaas.com',
    logo: 'https://mysaas.com/logo.png',
    sameAs: [
      'https://twitter.com/mysaas',
      'https://linkedin.com/company/mysaas',
      'https://github.com/mysaas',
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: '+82-2-1234-5678',
      contactType: 'customer service',
      availableLanguage: ['Korean', 'English'],
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

### SaaS 제품

```typescript
// src/components/ProductJsonLd.tsx
export function SoftwareApplicationJsonLd() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'MySaaS',
    operatingSystem: 'Web',
    applicationCategory: 'BusinessApplication',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'KRW',
      priceValidUntil: '2026-12-31',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: '4.8',
      ratingCount: '150',
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

### 블로그 포스트

```typescript
// src/components/ArticleJsonLd.tsx
type Props = {
  title: string;
  description: string;
  publishedAt: string;
  author: string;
  image: string;
  url: string;
};

export function ArticleJsonLd({ title, description, publishedAt, author, image, url }: Props) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: title,
    description: description,
    image: image,
    datePublished: publishedAt,
    author: {
      '@type': 'Person',
      name: author,
    },
    publisher: {
      '@type': 'Organization',
      name: 'MySaaS',
      logo: {
        '@type': 'ImageObject',
        url: 'https://mysaas.com/logo.png',
      },
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': url,
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

### FAQ

```typescript
// src/components/FaqJsonLd.tsx
type FaqItem = {
  question: string;
  answer: string;
};

export function FaqJsonLd({ faqs }: { faqs: FaqItem[] }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer,
      },
    })),
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

---

## 5. 이미지 최적화

### Next.js Image 컴포넌트

```typescript
// src/components/OptimizedImage.tsx
import Image from 'next/image';

type Props = {
  src: string;
  alt: string;
  width: number;
  height: number;
  priority?: boolean;
};

export function OptimizedImage({ src, alt, width, height, priority = false }: Props) {
  return (
    <Image
      src={src}
      alt={alt}  // SEO: 반드시 의미있는 alt 텍스트
      width={width}
      height={height}
      priority={priority}  // LCP 이미지는 priority 설정
      loading={priority ? 'eager' : 'lazy'}
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    />
  );
}
```

### next.config.js 이미지 설정

```javascript
// next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.mysaas.com',
      },
    ],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
};
```

---

## 6. 성능 최적화 (Core Web Vitals)

### LCP (Largest Contentful Paint)

```typescript
// 중요 이미지에 priority 추가
<Image src="/hero.jpg" alt="Hero" priority />

// 폰트 최적화
import { Inter } from 'next/font/google';
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // 폰트 로딩 중 텍스트 표시
});
```

### CLS (Cumulative Layout Shift)

```typescript
// 이미지 크기 명시
<Image src="/image.jpg" width={800} height={600} alt="..." />

// 스켈레톤 로더
function Skeleton({ className }: { className?: string }) {
  return (
    <div className={`animate-pulse bg-gray-200 ${className}`} />
  );
}

// 광고/동적 콘텐츠 공간 예약
<div style={{ minHeight: '250px' }}>
  <AdComponent />
</div>
```

### INP (Interaction to Next Paint)

```typescript
// React.memo로 불필요한 리렌더링 방지
const ExpensiveComponent = React.memo(function ExpensiveComponent() {
  // ...
});

// useTransition으로 비동기 상태 업데이트
const [isPending, startTransition] = useTransition();

function handleClick() {
  startTransition(() => {
    setItems(computeExpensiveList());
  });
}
```

---

## 7. 국제화 SEO (다국어)

### hreflang 설정

```typescript
// src/app/layout.tsx
export const metadata: Metadata = {
  alternates: {
    canonical: 'https://mysaas.com',
    languages: {
      'ko-KR': 'https://mysaas.com/ko',
      'en-US': 'https://mysaas.com/en',
      'ja-JP': 'https://mysaas.com/ja',
      'x-default': 'https://mysaas.com',
    },
  },
};
```

### 언어별 Sitemap

```typescript
// src/app/sitemap.ts
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const languages = ['ko', 'en', 'ja'];
  const baseUrl = 'https://mysaas.com';

  const pages = ['', '/features', '/pricing'];

  return pages.flatMap((page) =>
    languages.map((lang) => ({
      url: `${baseUrl}/${lang}${page}`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: page === '' ? 1 : 0.8,
    }))
  );
}
```

---

## 8. 검색엔진 등록

### Google Search Console

1. https://search.google.com/search-console 접속
2. 속성 추가 → URL 접두어 또는 도메인
3. 소유권 확인 (HTML 태그, DNS, 파일 업로드 중 선택)
4. sitemap.xml 제출

### Naver Search Advisor

1. https://searchadvisor.naver.com 접속
2. 사이트 등록
3. 소유확인 (HTML 태그)
4. 사이트맵 제출

### Bing Webmaster Tools

1. https://www.bing.com/webmasters 접속
2. 사이트 추가
3. 소유권 확인
4. 사이트맵 제출

---

## 9. SEO 체크리스트

```
┌─────────────────────────────────────────────────────────────┐
│ ✅ SEO 체크리스트                                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 📝 메타 태그                                                 │
│ □ title 태그 (50-60자)                                      │
│ □ description 메타 태그 (150-160자)                         │
│ □ Open Graph 태그                                           │
│ □ Twitter Card 태그                                         │
│ □ canonical URL                                             │
│                                                              │
│ 🗺️ 사이트맵 & 로봇                                          │
│ □ sitemap.xml 생성                                          │
│ □ robots.txt 설정                                           │
│ □ Google Search Console 등록                                │
│ □ Naver Search Advisor 등록                                 │
│                                                              │
│ 📊 구조화된 데이터                                           │
│ □ Organization JSON-LD                                      │
│ □ Product/Service JSON-LD                                   │
│ □ Article JSON-LD (블로그)                                  │
│ □ FAQ JSON-LD                                               │
│ □ BreadcrumbList JSON-LD                                    │
│                                                              │
│ 🖼️ 이미지 최적화                                            │
│ □ alt 텍스트                                                │
│ □ WebP/AVIF 포맷                                            │
│ □ 적절한 크기                                               │
│ □ lazy loading                                              │
│                                                              │
│ ⚡ 성능 (Core Web Vitals)                                   │
│ □ LCP < 2.5초                                               │
│ □ INP < 200ms                                               │
│ □ CLS < 0.1                                                 │
│                                                              │
│ 🌐 기타                                                      │
│ □ HTTPS 사용                                                │
│ □ 모바일 친화적                                             │
│ □ 빠른 로딩 속도                                            │
│ □ 명확한 URL 구조                                           │
│ □ 내부 링크 최적화                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. SEO 모니터링 도구

### 무료 도구

- **Google Search Console**: 검색 성능, 인덱싱 상태
- **Google PageSpeed Insights**: Core Web Vitals 측정
- **Lighthouse**: 종합 SEO 점수
- **Screaming Frog SEO Spider**: 사이트 크롤링 (500 URL 무료)

### 유료 도구

- **Ahrefs**: 백링크, 키워드 분석
- **SEMrush**: 종합 SEO 도구
- **Moz Pro**: 도메인 권위, 키워드 추적

### 코드로 SEO 점수 확인

```bash
# Lighthouse CLI
npm install -g lighthouse
lighthouse https://mysaas.com --output html --output-path ./report.html

# PageSpeed Insights API
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://mysaas.com&strategy=mobile"
```

---

## 11. 파비콘 자동 생성

### 방법 1: AI 이미지 생성 + 자동 변환

```typescript
// scripts/generate-favicon.ts
import sharp from 'sharp';
import { toIco } from 'ico-endec';
import fs from 'fs/promises';
import path from 'path';

interface FaviconConfig {
  inputImage: string;  // AI 생성 이미지 또는 로고
  outputDir: string;
  siteName: string;
  themeColor: string;
}

async function generateFavicons(config: FaviconConfig) {
  const { inputImage, outputDir, siteName, themeColor } = config;

  // 필요한 사이즈 정의
  const sizes = [
    { name: 'favicon-16x16.png', size: 16 },
    { name: 'favicon-32x32.png', size: 32 },
    { name: 'favicon-48x48.png', size: 48 },
    { name: 'apple-touch-icon.png', size: 180 },
    { name: 'android-chrome-192x192.png', size: 192 },
    { name: 'android-chrome-512x512.png', size: 512 },
    { name: 'mstile-150x150.png', size: 150 },
  ];

  // 디렉토리 생성
  await fs.mkdir(outputDir, { recursive: true });

  // 각 사이즈로 변환
  for (const { name, size } of sizes) {
    await sharp(inputImage)
      .resize(size, size, { fit: 'contain', background: { r: 255, g: 255, b: 255, alpha: 0 } })
      .png()
      .toFile(path.join(outputDir, name));

    console.log(`✅ Generated: ${name}`);
  }

  // favicon.ico 생성 (16x16, 32x32, 48x48 포함)
  const ico16 = await sharp(inputImage).resize(16, 16).png().toBuffer();
  const ico32 = await sharp(inputImage).resize(32, 32).png().toBuffer();
  const ico48 = await sharp(inputImage).resize(48, 48).png().toBuffer();

  const icoBuffer = toIco([ico16, ico32, ico48]);
  await fs.writeFile(path.join(outputDir, 'favicon.ico'), icoBuffer);
  console.log('✅ Generated: favicon.ico');

  // manifest.json 생성
  const manifest = {
    name: siteName,
    short_name: siteName,
    icons: [
      { src: '/android-chrome-192x192.png', sizes: '192x192', type: 'image/png' },
      { src: '/android-chrome-512x512.png', sizes: '512x512', type: 'image/png' },
    ],
    theme_color: themeColor,
    background_color: '#ffffff',
    display: 'standalone',
  };
  await fs.writeFile(
    path.join(outputDir, 'manifest.json'),
    JSON.stringify(manifest, null, 2)
  );
  console.log('✅ Generated: manifest.json');

  // browserconfig.xml 생성 (Microsoft)
  const browserconfig = `<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
  <msapplication>
    <tile>
      <square150x150logo src="/mstile-150x150.png"/>
      <TileColor>${themeColor}</TileColor>
    </tile>
  </msapplication>
</browserconfig>`;
  await fs.writeFile(path.join(outputDir, 'browserconfig.xml'), browserconfig);
  console.log('✅ Generated: browserconfig.xml');

  console.log('\n🎉 All favicons generated successfully!');
}

// 실행
generateFavicons({
  inputImage: './logo.png',  // AI로 생성한 로고 또는 기존 로고
  outputDir: './public',
  siteName: 'MySaaS',
  themeColor: '#3B82F6',
});
```

### 방법 2: AI 로고 생성 스크립트

```typescript
// scripts/generate-logo-and-favicon.ts
import OpenAI from 'openai';
import sharp from 'sharp';
import fs from 'fs/promises';

const openai = new OpenAI();

interface LogoConfig {
  serviceName: string;
  style: 'minimal' | 'modern' | 'playful' | 'corporate';
  primaryColor: string;
  description: string;
}

async function generateLogoWithAI(config: LogoConfig): Promise<Buffer> {
  const prompt = `
    Create a simple, modern logo icon for "${config.serviceName}".
    Style: ${config.style}
    Primary color: ${config.primaryColor}
    Description: ${config.description}
    Requirements:
    - Square format, centered
    - Works well at small sizes (16x16 to 512x512)
    - Clean, minimal design
    - No text, icon only
    - Flat design, no gradients
    - White or transparent background
  `;

  const response = await openai.images.generate({
    model: 'dall-e-3',
    prompt,
    n: 1,
    size: '1024x1024',
    quality: 'hd',
    response_format: 'b64_json',
  });

  const imageData = response.data[0].b64_json!;
  return Buffer.from(imageData, 'base64');
}

async function main() {
  console.log('🎨 Generating logo with AI...');

  const logoBuffer = await generateLogoWithAI({
    serviceName: 'MySaaS',
    style: 'modern',
    primaryColor: '#3B82F6',
    description: 'A productivity SaaS for teams',
  });

  // 원본 로고 저장
  await fs.writeFile('./logo-original.png', logoBuffer);
  console.log('✅ Saved: logo-original.png');

  // 배경 제거 및 정사각형으로 크롭
  await sharp(logoBuffer)
    .resize(1024, 1024, { fit: 'contain', background: { r: 255, g: 255, b: 255, alpha: 0 } })
    .png()
    .toFile('./logo.png');
  console.log('✅ Saved: logo.png');

  console.log('\n🚀 Now run: npx ts-node scripts/generate-favicon.ts');
}

main().catch(console.error);
```

### 방법 3: 온라인 도구 사용

```bash
# RealFaviconGenerator CLI
npm install -g real-favicon

# favicon 생성 (logo.png 필요)
real-favicon generate ./faviconDescription.json ./faviconData.json ./public
```

```json
// faviconDescription.json
{
  "masterPicture": "./logo.png",
  "iconsPath": "/",
  "design": {
    "ios": {
      "pictureAspect": "backgroundAndMargin",
      "backgroundColor": "#ffffff",
      "margin": "14%"
    },
    "desktopBrowser": {},
    "windows": {
      "pictureAspect": "whiteSilhouette",
      "backgroundColor": "#3B82F6"
    },
    "androidChrome": {
      "pictureAspect": "shadow",
      "themeColor": "#3B82F6",
      "manifest": {
        "name": "MySaaS",
        "display": "standalone"
      }
    }
  },
  "settings": {
    "compression": 2,
    "scalingAlgorithm": "Mitchell"
  }
}
```

### Next.js에서 파비콘 적용

```typescript
// src/app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
    other: [
      { rel: 'mask-icon', url: '/safari-pinned-tab.svg', color: '#3B82F6' },
    ],
  },
  manifest: '/manifest.json',
  themeColor: '#3B82F6',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'MySaaS',
  },
};
```

### 필요한 패키지 설치

```bash
# 파비콘 생성 도구
npm install --save-dev sharp ico-endec

# AI 로고 생성 (선택)
npm install openai

# 타입
npm install --save-dev @types/sharp
```

---

## 12. SEO 개발 워크플로우

### Step 1: 초기 설정

```bash
# 1. SEO 관련 패키지 설치
npm install next-seo next-sitemap

# 2. 파비콘 생성 도구 설치
npm install --save-dev sharp ico-endec

# 3. 로고/파비콘 생성
npx ts-node scripts/generate-logo-and-favicon.ts
npx ts-node scripts/generate-favicon.ts
```

### Step 2: 메타데이터 설정

```typescript
// src/app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL('https://mysaas.com'),
  title: {
    default: 'MySaaS - 서비스 한 줄 설명',
    template: '%s | MySaaS',
  },
  description: '서비스에 대한 150-160자 설명',
  // ... 나머지 설정
};
```

### Step 3: 사이트맵 & robots.txt

```bash
# next-sitemap 설정 파일 생성
touch next-sitemap.config.js
```

```javascript
// next-sitemap.config.js
/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: 'https://mysaas.com',
  generateRobotsTxt: true,
  sitemapSize: 7000,
  changefreq: 'weekly',
  priority: 0.7,
  exclude: ['/api/*', '/admin/*', '/dashboard/*'],
  robotsTxtOptions: {
    additionalSitemaps: [
      'https://mysaas.com/sitemap-blog.xml',
    ],
    policies: [
      { userAgent: '*', allow: '/', disallow: ['/api/', '/admin/'] },
    ],
  },
};
```

```json
// package.json
{
  "scripts": {
    "postbuild": "next-sitemap"
  }
}
```

### Step 4: 구조화된 데이터 추가

```typescript
// src/app/layout.tsx
import { OrganizationJsonLd, SoftwareApplicationJsonLd } from '@/components/JsonLd';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <head>
        <OrganizationJsonLd />
        <SoftwareApplicationJsonLd />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Step 5: OG 이미지 자동 생성

```typescript
// src/app/api/og/route.tsx
import { ImageResponse } from 'next/og';
import { NextRequest } from 'next/server';

export const runtime = 'edge';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') || 'MySaaS';
  const description = searchParams.get('description') || '';

  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#1a1a2e',
          color: 'white',
          padding: '40px',
        }}
      >
        <div style={{ fontSize: 60, fontWeight: 'bold', marginBottom: 20 }}>
          {title}
        </div>
        <div style={{ fontSize: 30, opacity: 0.8, textAlign: 'center' }}>
          {description}
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
```

```typescript
// 사용 예시 - 동적 메타데이터
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    openGraph: {
      images: [`/api/og?title=${encodeURIComponent(post.title)}&description=${encodeURIComponent(post.excerpt)}`],
    },
  };
}
```

### Step 6: 검색엔진 등록

```
┌─────────────────────────────────────────────────────────────┐
│ 🔍 검색엔진 등록 순서                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. 배포 완료 후                                              │
│                                                              │
│ 2. Google Search Console                                    │
│    → https://search.google.com/search-console               │
│    → 속성 추가 → URL 접두어                                  │
│    → HTML 태그로 소유권 확인                                 │
│    → sitemap.xml 제출                                        │
│                                                              │
│ 3. Naver Search Advisor                                      │
│    → https://searchadvisor.naver.com                        │
│    → 사이트 추가                                             │
│    → HTML 태그로 소유확인                                    │
│    → 사이트맵 제출                                           │
│                                                              │
│ 4. Bing Webmaster Tools                                      │
│    → https://www.bing.com/webmasters                        │
│    → Google Search Console에서 가져오기 (간편)              │
│                                                              │
│ 5. 인덱싱 요청                                               │
│    → Google: URL 검사 → 색인 생성 요청                       │
│    → Naver: 웹페이지 수집 요청                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Step 7: SEO 점수 확인

```bash
# Lighthouse로 SEO 점수 측정
npx lighthouse https://mysaas.com --only-categories=seo --output=html --output-path=./seo-report.html

# 또는 Chrome DevTools에서
# F12 → Lighthouse 탭 → SEO 체크 → Analyze
```

### 개발 체크리스트

```
┌─────────────────────────────────────────────────────────────┐
│ 📋 SEO 개발 체크리스트                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ □ 1. 패키지 설치 (next-seo, next-sitemap, sharp)            │
│ □ 2. 로고 생성 (AI 또는 직접 디자인)                         │
│ □ 3. 파비콘 자동 생성 스크립트 실행                          │
│ □ 4. layout.tsx 메타데이터 설정                              │
│ □ 5. next-sitemap.config.js 설정                            │
│ □ 6. JSON-LD 컴포넌트 추가                                   │
│ □ 7. OG 이미지 API 라우트 생성                               │
│ □ 8. 빌드 및 배포                                            │
│ □ 9. Google Search Console 등록                              │
│ □ 10. Naver Search Advisor 등록                              │
│ □ 11. Lighthouse SEO 점수 확인 (목표: 90+)                   │
│ □ 12. Core Web Vitals 확인                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 13. 빠른 적용 템플릿

```bash
# SEO 패키지 설치
npm install next-seo next-sitemap

# next-sitemap 설정
npx next-sitemap
```

### next-seo 사용

```typescript
// src/app/layout.tsx
import { DefaultSeo } from 'next-seo';
import SEO from '../next-seo.config';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <DefaultSeo {...SEO} />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

```typescript
// next-seo.config.ts
export default {
  titleTemplate: '%s | MySaaS',
  defaultTitle: 'MySaaS - 서비스 설명',
  description: '서비스 설명 150-160자',
  openGraph: {
    type: 'website',
    locale: 'ko_KR',
    url: 'https://mysaas.com',
    siteName: 'MySaaS',
  },
  twitter: {
    handle: '@mysaas',
    cardType: 'summary_large_image',
  },
};
```
