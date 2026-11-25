---
name: webpack-vite
description: Frontend bundler configuration for Webpack and Vite. Use when user mentions "webpack", "vite", "bundler", "vite config", "webpack config", "code splitting", "tree shaking", "hot module replacement", "HMR", "build optimization", "bundle size", "chunk splitting", "loader", "plugin", "esbuild", "rollup", "dev server", or configuring JavaScript build tools.
---

# Webpack and Vite Reference

## Vite Configuration

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
    },
  },
  server: { port: 3000, open: true, strictPort: true },
  build: {
    outDir: 'dist',
    sourcemap: true,
    target: 'esnext',
    minify: 'esbuild',               // or 'terser' for drop_console
    rollupOptions: {
      output: {
        manualChunks: { vendor: ['react', 'react-dom'], router: ['react-router-dom'] },
      },
    },
  },
  optimizeDeps: {
    include: ['lodash-es', 'axios'],  // force pre-bundling
    exclude: ['your-local-package'],
  },
  css: {
    modules: { localsConvention: 'camelCaseOnly' },
    preprocessorOptions: { scss: { additionalData: `@use "@/styles/variables" as *;` } },
  },
});
```

## Vite Environment Variables

```bash
# .env / .env.local / .env.development / .env.production / .env.[mode]
# Only VITE_ prefixed vars are exposed to client code
VITE_API_URL=https://api.example.com
DB_PASSWORD=secret                     # NOT exposed to client
```

```ts
const apiUrl = import.meta.env.VITE_API_URL;
const isDev = import.meta.env.DEV;       // boolean
const mode = import.meta.env.MODE;       // 'development' | 'production' | custom

// Type declarations (env.d.ts)
/// <reference types="vite/client" />
interface ImportMetaEnv { readonly VITE_API_URL: string }
```

## Vite Plugins

```ts
import react from '@vitejs/plugin-react';           // Babel-based
import reactSWC from '@vitejs/plugin-react-swc';    // SWC-based (faster)
import vue from '@vitejs/plugin-vue';
import svgr from 'vite-plugin-svgr';                // SVG as React components
import { VitePWA } from 'vite-plugin-pwa';
import legacy from '@vitejs/plugin-legacy';          // IE11 / older browser support
import { visualizer } from 'rollup-plugin-visualizer'; // bundle analysis

export default defineConfig({
  plugins: [
    reactSWC(),
    svgr(),
    VitePWA({ registerType: 'autoUpdate', workbox: { globPatterns: ['**/*.{js,css,html,ico,png,svg}'] } }),
    legacy({ targets: ['defaults', 'not IE 11'] }),
    visualizer({ open: true, gzipSize: true, brotliSize: true }),
  ],
});
```

## Vite Dev Server and Proxy

```ts
export default defineConfig({
  server: {
    proxy: {
      '/api': { target: 'http://localhost:4000', changeOrigin: true, rewrite: (p) => p.replace(/^\/api/, '') },
      '/ws': { target: 'ws://localhost:4000', ws: true },
    },
    https: { key: './certs/key.pem', cert: './certs/cert.pem' },
    cors: true,
    fs: { allow: ['../..'] },            // monorepo: serve files outside root
  },
});
```

## Webpack 5 Configuration

```js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  mode: 'production',
  entry: { main: './src/index.tsx', admin: './src/admin.tsx' },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    chunkFilename: '[name].[contenthash].chunk.js',
    clean: true,
    publicPath: '/',
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js', '.jsx'],
    alias: { '@': path.resolve(__dirname, 'src') },
  },
  module: {
    rules: [
      { test: /\.(ts|tsx|js|jsx)$/, exclude: /node_modules/, use: { loader: 'babel-loader',
          options: { presets: ['@babel/preset-env', '@babel/preset-react', '@babel/preset-typescript'] } } },
      { test: /\.css$/, use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader'] },
      { test: /\.module\.css$/, use: [MiniCssExtractPlugin.loader,
          { loader: 'css-loader', options: { modules: true } }, 'postcss-loader'] },
      { test: /\.s[ac]ss$/, use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader'] },
      { test: /\.(png|jpg|gif|svg|webp)$/, type: 'asset', parser: { dataUrlCondition: { maxSize: 8 * 1024 } } },
      { test: /\.(woff|woff2|eot|ttf|otf)$/, type: 'asset/resource' },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({ template: './public/index.html', minify: { collapseWhitespace: true } }),
    new MiniCssExtractPlugin({ filename: 'css/[name].[contenthash].css' }),
  ],
};
// Note: Webpack 5 asset modules replace file-loader, url-loader, and raw-loader.
```

## Webpack Plugins

```js
const { DefinePlugin, ProvidePlugin } = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new DefinePlugin({
      'process.env.API_URL': JSON.stringify(process.env.API_URL),
      __DEV__: JSON.stringify(process.env.NODE_ENV === 'development'),
    }),
    new ProvidePlugin({ React: 'react' }),
    new CopyWebpackPlugin({ patterns: [{ from: 'public/assets', to: 'assets' }] }),
    new BundleAnalyzerPlugin({ analyzerMode: 'static', openAnalyzer: false }),
  ],
};
```

## Code Splitting

```js
// Dynamic import -- creates a separate chunk loaded on demand
const LazyComponent = React.lazy(() => import('./HeavyComponent'));
const Admin = React.lazy(() => import(/* webpackChunkName: "admin" */ './AdminPanel'));

// Webpack splitChunks
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      maxInitialRequests: 20,
      minSize: 20000,
      cacheGroups: {
        vendor: { test: /[\\/]node_modules[\\/]/, name: 'vendors', priority: -10 },
        commons: { minChunks: 2, priority: -20, reuseExistingChunk: true },
      },
    },
    runtimeChunk: 'single',
  },
};

// Vite manual chunks
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('react')) return 'react-vendor';
            return 'vendor';
          }
        },
      },
    },
  },
});
```

## Tree Shaking

```json
// package.json -- mark as side-effect-free for tree shaking
{ "sideEffects": false }
// Or specify files with side effects:
{ "sideEffects": ["*.css", "*.scss", "./src/polyfills.ts"] }
```

```js
import { debounce } from 'lodash-es';     // tree-shakeable (ESM)
const { debounce } = require('lodash');    // NOT tree-shakeable (CJS), bundles everything
// Webpack: set mode 'production' to enable terser + dead code elimination
// Vite: tree shaking via Rollup is on by default in production
```

## Bundle Analysis

```bash
# Webpack
npx webpack --profile --json > stats.json && npx webpack-bundle-analyzer stats.json
# Or use BundleAnalyzerPlugin (see Webpack Plugins section)

# Vite -- use rollup-plugin-visualizer (see Vite Plugins section)
```

## Webpack Dev Server

```js
module.exports = {
  devServer: {
    port: 3000,
    hot: true,
    historyApiFallback: true,            // SPA routing fallback
    compress: true,
    proxy: [{ context: ['/api'], target: 'http://localhost:4000', changeOrigin: true,
              pathRewrite: { '^/api': '' } }],
    https: true,
    static: { directory: path.join(__dirname, 'public') },
  },
};
```

## Production Optimization

```js
// Webpack
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');

module.exports = {
  mode: 'production',
  devtool: 'source-map',                // 'hidden-source-map' to hide from users
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({ terserOptions: { compress: { drop_console: true, drop_debugger: true } } }),
      new CssMinimizerPlugin(),
    ],
  },
  plugins: [
    new CompressionPlugin({ algorithm: 'gzip', test: /\.(js|css|html|svg)$/, threshold: 10240 }),
  ],
};
```

```ts
// Vite production
export default defineConfig({
  build: {
    sourcemap: 'hidden',
    minify: 'terser',
    terserOptions: { compress: { drop_console: true } },
    cssCodeSplit: true,
    assetsInlineLimit: 4096,             // inline assets < 4KB as base64
    chunkSizeWarningLimit: 500,
  },
});
```

## CSS Handling

```js
// postcss.config.js -- shared by both Webpack and Vite
module.exports = {
  plugins: {
    'tailwindcss': {},
    'autoprefixer': {},
    'cssnano': process.env.NODE_ENV === 'production' ? {} : false,
  },
};
// Vite: install sass and import .scss directly -- no loader config needed
// Webpack: add sass-loader to module.rules (see Webpack 5 Configuration)
```

## Migration from Webpack to Vite

```bash
npm install -D vite @vitejs/plugin-react    # 1. install
# 2. Create vite.config.ts                  # see "Vite Configuration" section
# 3. Move index.html to project root, add: <script type="module" src="/src/main.tsx"></script>
# 4. Update package.json scripts: "dev": "vite", "build": "tsc && vite build", "preview": "vite preview"
```

| Webpack                         | Vite                                      |
|---------------------------------|-------------------------------------------|
| `require()` / `module.exports`  | `import` / `export` (ESM only)            |
| `process.env.X`                 | `import.meta.env.VITE_X`                  |
| `file-loader` / `url-loader`    | Native static asset handling              |
| `webpack.DefinePlugin`          | `define` option in vite.config.ts         |
| `webpackChunkName` comments     | `rollupOptions.output.manualChunks`       |
| `require.context()`             | `import.meta.glob()`                      |
| webpack-dev-server proxy        | `server.proxy` in vite config             |

## Monorepo Bundling

```ts
// Vite monorepo
export default defineConfig({
  resolve: { alias: { '@shared/ui': path.resolve(__dirname, '../../packages/ui/src') } },
  optimizeDeps: { include: ['@shared/ui'] },
  server: { fs: { allow: ['../..'] } },
});

// Webpack monorepo
module.exports = {
  resolve: { alias: { '@shared/ui': path.resolve(__dirname, '../../packages/ui/src') }, symlinks: false },
  module: { rules: [{
    test: /\.(ts|tsx)$/,
    include: [path.resolve(__dirname, 'src'), path.resolve(__dirname, '../../packages')],
    use: 'babel-loader',
  }] },
};
```

## Performance Budgets

```js
// Webpack -- built-in performance hints
module.exports = {
  performance: {
    hints: 'error',                      // 'warning' | 'error' | false
    maxAssetSize: 250000,                // 250KB per asset
    maxEntrypointSize: 400000,           // 400KB per entry point
    assetFilter: (file) => !/\.map$/.test(file),
  },
};
```

```bash
# size-limit -- CI-friendly, works with both Webpack and Vite
npm install -D size-limit @size-limit/preset-app
# package.json: "size-limit": [{ "path": "dist/assets/*.js", "limit": "200 KB", "gzip": true }]
npx size-limit
```
