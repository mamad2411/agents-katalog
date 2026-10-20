---
name: postcss-plugins-reference
description: PostCSS plugins reference - essential plugins, configuration, and optimization strategies
searchable: true
tags: [postcss, build-tools, css-processing, autoprefixer, cssnano, purgecss]
---

# PostCSS Plugins Reference

Quick reference for essential PostCSS plugins, configuration patterns, and build optimization.

## Essential Plugins

### 1. postcss-preset-env
Transform modern CSS to browser-compatible CSS.

```javascript
require('postcss-preset-env')({
  stage: 2, // CSS features at stage 2+
  features: {
    'nesting-rules': true,
    'custom-properties': true,
    'custom-media-queries': true,
  },
  browsers: 'last 2 versions',
})
```

### 2. autoprefixer
Add vendor prefixes automatically.

```javascript
require('autoprefixer')({
  grid: 'autoplace',
  flexbox: 'no-2009',
  overrideBrowserslist: ['> 1%', 'last 2 versions'],
})
```

### 3. cssnano
Minify and optimize CSS.

```javascript
require('cssnano')({
  preset: ['advanced', {
    discardComments: { removeAll: true },
    reduceIdents: true,
    zindex: false,
  }],
})
```

### 4. postcss-import
Resolve `@import` statements.

```javascript
require('postcss-import')({
  path: ['src/styles', 'node_modules'],
})
```

### 5. @fullhuman/postcss-purgecss
Remove unused CSS.

```javascript
require('@fullhuman/postcss-purgecss')({
  content: ['./src/**/*.{html,ts,tsx,jsx}'],
  safelist: [/^mat-/, /^cdk-/],
})
```

## Plugin Categories

### Modern CSS Features
- **postcss-preset-env** - Future CSS features
- **postcss-nesting** - CSS nesting
- **postcss-custom-properties** - CSS variables fallback

### Optimization
- **cssnano** - Minification
- **postcss-purgecss** - Remove unused CSS
- **css-mqpacker** - Combine media queries

### Tools
- **autoprefixer** - Vendor prefixes
- **postcss-import** - Import resolution
- **postcss-reporter** - Error reporting

## Production Config

```javascript
module.exports = {
  plugins: [
    require('postcss-import')(),
    require('postcss-preset-env')({
      stage: 2,
      features: { 'nesting-rules': true },
    }),
    process.env.NODE_ENV === 'production' && require('@fullhuman/postcss-purgecss')({
      content: ['./src/**/*.{html,ts,tsx}'],
    }),
    process.env.NODE_ENV === 'production' && require('cssnano')({
      preset: 'advanced',
    }),
  ].filter(Boolean),
};
```

## Framework Integration

### Vite
```javascript
// vite.config.js
import postcssPresetEnv from 'postcss-preset-env';

export default {
  css: {
    postcss: {
      plugins: [postcssPresetEnv({ stage: 2 })],
    },
  },
};
```

### Webpack
```javascript
{
  test: /\.css$/,
  use: ['style-loader', 'css-loader', 'postcss-loader'],
}
```

### Angular
```json
{
  "architect": {
    "build": {
      "options": {
        "postcssOptions": {
          "config": "./postcss.config.js"
        }
      }
    }
  }
}
```

## Best Practices

✅ **DO:**
- Use postcss-preset-env for future CSS
- Enable PurgeCSS in production
- Configure autoprefixer with browserslist
- Use cssnano for minification

❌ **DON'T:**
- Run heavy plugins in development
- Skip source maps
- Ignore plugin order
- Use conflicting plugins

Use this reference for quick PostCSS configuration lookups.
