---
name: performance-optimization
description: Optimize application performance including caching, lazy loading, bundle optimization, and database query optimization. Use when optimizing code, improving performance, or when the user asks about performance, caching, optimization, or speed.
---

# Performance Optimization Best Practices

Optimize applications for speed, efficiency, and scalability.

## Frontend Performance

### Code Splitting & Lazy Loading

```typescript
// ✅ Good - Lazy load routes
const routes = [
  {
    path: "/users",
    component: () => import("@/views/Users/index.vue"),
  },
];

// ✅ Good - Lazy load components
const HeavyComponent = defineAsyncComponent(
  () => import("@/components/HeavyComponent.vue"),
);

// ✅ Good - Dynamic imports
async function loadModule() {
  const module = await import("./heavy-module.js");
  module.doSomething();
}
```

### Bundle Optimization

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["vue", "vue-router", "pinia"],
          ui: ["vuetify"],
          utils: ["axios", "lodash"],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },
});
```

### Image Optimization

```vue
<!-- ✅ Good - Lazy load images -->
<img :src="imageSrc" loading="lazy" :alt="imageAlt" />

<!-- ✅ Good - Use modern formats -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description">
</picture>
```

### Virtual Scrolling

```vue
<!-- For large lists -->
<template>
  <VirtualList
    :data-key="'id'"
    :data-sources="items"
    :data-component="itemComponent"
    :keeps="20"
  />
</template>
```

## Backend Performance

### Database Query Optimization

```typescript
// ✅ Good - Select only needed columns
const users = await User.findAll({
  attributes: ["id", "name", "email"],
});

// ✅ Good - Use indexes
await User.findAll({
  where: { status: "active" }, // Indexed column
  order: [["createdAt", "DESC"]], // Indexed column
});

// ✅ Good - Eager load to avoid N+1
const orders = await Order.findAll({
  include: [{ model: User }, { model: OrderItem }],
});

// ✅ Good - Use pagination
const users = await User.findAll({
  limit: 20,
  offset: 0,
});
```

### Caching Strategies

**In-Memory Caching:**

```typescript
import NodeCache from "node-cache";

const cache = new NodeCache({ stdTTL: 600 }); // 10 minutes

async function getUser(id: number) {
  const cacheKey = `user:${id}`;
  const cached = cache.get(cacheKey);

  if (cached) {
    return cached;
  }

  const user = await User.findByPk(id);
  cache.set(cacheKey, user);
  return user;
}
```

**Redis Caching:**

```typescript
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL);

async function getUser(id: number) {
  const cacheKey = `user:${id}`;
  const cached = await redis.get(cacheKey);

  if (cached) {
    return JSON.parse(cached);
  }

  const user = await User.findByPk(id);
  await redis.setex(cacheKey, 600, JSON.stringify(user)); // 10 min TTL
  return user;
}
```

**API Response Caching:**

```typescript
import express from "express";
import apicache from "apicache";

const cache = apicache.middleware;

// Cache for 5 minutes
router.get("/users", cache("5 minutes"), getUsers);

// Cache with custom key
router.get(
  "/users/:id",
  cache("10 minutes", (req) => `user:${req.params.id}`),
  getUser,
);
```

### Connection Pooling

```typescript
// Sequelize connection pool
const sequelize = new Sequelize(database, username, password, {
  pool: {
    max: 10, // Maximum connections
    min: 2, // Minimum connections
    acquire: 30000, // Max time to wait for connection
    idle: 10000, // Max time connection can be idle
  },
});
```

## API Performance

### Response Compression

```typescript
import compression from "compression";

app.use(
  compression({
    filter: (req, res) => {
      if (req.headers["x-no-compression"]) {
        return false;
      }
      return compression.filter(req, res);
    },
    level: 6,
  }),
);
```

### Request Batching

```typescript
// Batch multiple requests
async function batchGetUsers(userIds: number[]) {
  const users = await User.findAll({
    where: { id: { [Op.in]: userIds } },
  });
  return users;
}

// Instead of
// for (const id of userIds) {
//   await User.findByPk(id); // N queries
// }
```

### Pagination

```typescript
// ✅ Good - Offset pagination
async function getUsers(page: number = 1, limit: number = 20) {
  const offset = (page - 1) * limit;
  return User.findAll({
    limit,
    offset,
    order: [["createdAt", "DESC"]],
  });
}

// ✅ Better - Cursor pagination for large datasets
async function getUsers(cursor?: string, limit: number = 20) {
  const where = cursor ? { id: { [Op.gt]: cursor } } : {};
  return User.findAll({
    where,
    limit,
    order: [["id", "ASC"]],
  });
}
```

## Frontend Caching

### HTTP Caching Headers

```typescript
// Set cache headers
app.use((req, res, next) => {
  if (req.path.startsWith("/static/")) {
    res.setHeader("Cache-Control", "public, max-age=31536000"); // 1 year
  } else if (req.path.startsWith("/api/")) {
    res.setHeader("Cache-Control", "no-cache");
  }
  next();
});
```

### Service Worker Caching

```typescript
// service-worker.ts
self.addEventListener("fetch", (event) => {
  if (event.request.url.includes("/api/")) {
    event.respondWith(
      caches.open("api-cache").then((cache) => {
        return fetch(event.request).then((response) => {
          cache.put(event.request, response.clone());
          return response;
        });
      }),
    );
  }
});
```

## Monitoring & Profiling

### Performance Monitoring

```typescript
// Add performance middleware
app.use((req, res, next) => {
  const start = Date.now();

  res.on("finish", () => {
    const duration = Date.now() - start;
    logger.info("Request duration", {
      method: req.method,
      path: req.path,
      duration: `${duration}ms`,
      statusCode: res.statusCode,
    });
  });

  next();
});
```

### Database Query Logging

```typescript
// Log slow queries
sequelize.addHook("afterQuery", (options, query) => {
  if (query.duration > 1000) {
    // Log queries > 1s
    logger.warn("Slow query detected", {
      sql: query.sql,
      duration: `${query.duration}ms`,
    });
  }
});
```

## Best Practices

1. **Lazy load routes** - Code splitting
2. **Cache frequently accessed data** - Reduce database queries
3. **Optimize database queries** - Use indexes, avoid N+1
4. **Compress responses** - Reduce bandwidth
5. **Use pagination** - Don't load all data at once
6. **Optimize images** - Use modern formats, lazy loading
7. **Minify and bundle** - Reduce file sizes
8. **Use CDN** - Serve static assets from edge
9. **Monitor performance** - Track slow operations
10. **Profile before optimizing** - Measure first

## When Optimizing Performance

1. **Measure first** - Use profiling tools
2. **Identify bottlenecks** - Database, network, rendering
3. **Cache appropriately** - Frequently accessed data
4. **Lazy load** - Code and data on demand
5. **Optimize queries** - Use indexes, avoid N+1
6. **Compress responses** - Reduce payload size
7. **Use pagination** - Limit data transfer
8. **Monitor continuously** - Track performance metrics
9. **Test optimizations** - Verify improvements
10. **Document changes** - Explain performance decisions
