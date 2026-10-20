---
description: 缓存(Cache)
globs: 
---
# 缓存

为了方便开发者进行缓存操作的组件，它有利于改善项目的性能。它为我们提供了一个数据中心以便进行高效的数据访问。

:::

## 使用

```ts
import { InjectClient, Provide } from '@midwayjs/core';
import { CachingFactory, MidwayCache } from '@midwayjs/cache-manager';

@Provide()
export class UserService {

  @InjectClient(CachingFactory, 'default')
  cache: MidwayCache;

  async invoke(name: string, value: string) {
    // 设置缓存
    await this.cache.set(name, value);
    // 获取缓存
    const data = await this.cache.get(name);
    // ...
  }
}
```

## 换成 Redis (v7.1 版本)

安装依赖，具体可以查看@midwayjs cache

```bash
pnpm i cache-manager-ioredis-yet --save
```

`src/config/config.default.ts`

```ts
import { CoolFileConfig, MODETYPE } from "@cool-midway/file";
import { MidwayConfig } from "@midwayjs/core";
// redis缓存
import { redisStore } from "cache-manager-ioredis-yet";

export default {
  // Redis缓存
  cacheManager: {
    clients: {
      default: {
        store: redisStore,
        options: {
          port: 6379,
          host: "127.0.0.1",
          password: "",
          ttl: 0,
          db: 0,
        },
      },
    },
  },
} as unknown as MidwayConfig;
```

## 换成 Redis (以往版本)

```bash
pnpm i cache-manager-ioredis --save
```

`src/config/config.default.ts`

```ts
import { CoolFileConfig, MODETYPE } from "@cool-midway/file";
import { MidwayConfig } from "@midwayjs/core";
// redis缓存
import * as redisStore from "cache-manager-ioredis";

export default {
  // Redis缓存
  cache: {
    store: redisStore,
    options: {
      port: 6379,
      host: "127.0.0.1",
      password: "",
      db: 0,
      keyPrefix: "cool:",
      ttl: null,
    },
  },
} as unknown as MidwayConfig;
```

## 使用

`src/modules/demo/controller/open/cache.ts`

```ts
import { DemoCacheService } from "../../service/cache";
import { Inject, Post, Provide, Get, InjectClient } from "@midwayjs/core";
import { CoolController, BaseController } from "@cool-midway/core";
import { CachingFactory, MidwayCache } from "@midwayjs/cache-manager";

/**
 * 缓存
 */
@Provide()
@CoolController()
export class AppDemoCacheController extends BaseController {
  @InjectClient(CachingFactory, "default")
  midwayCache: MidwayCache;

  @Inject()
  demoCacheService: DemoCacheService;

  /**
   * 设置缓存
   * @returns
   */
  @Post("/set")
  async set() {
    await this.midwayCache.set("a", 1);
    // 缓存10秒
    await this.midwayCache.set("a", 1, 10 * 1000);
    return this.ok(await this.midwayCache.get("a"));
  }

  /**
   * 获得缓存
   * @returns
   */
  @Get("/get")
  async get() {
    return this.ok(await this.demoCacheService.get());
  }
}
```

## 方法缓存

有些业务场景，我们并不希望每次请求接口都需要操作数据库，如：今日推荐、上个月排行榜等，数据存储在 redis

框架提供了 `@CoolCache` 方法装饰器，方法设置缓存，让代码更优雅

`src/modules/demo/service/cache.ts`

```ts
import { Provide } from "@midwayjs/core";
import { CoolCache } from "@cool-midway/core";

/**
 * 缓存
 */
@Provide()
export class DemoCacheService {
  // 数据缓存5秒
  @CoolCache(5000)
  async get() {
    console.log("执行方法");
    return {
      a: 1,
      b: 2,
    };
  }
}
```

::: warning
service 主要是处理业务逻辑，`@CoolCache`应该要在 service 中使用，不要在 controller 等其他位置使用
:::
