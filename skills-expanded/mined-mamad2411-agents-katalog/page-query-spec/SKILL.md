---
name: page-query-spec
description: 当需要分页查询数据时，按本技能规定的规范编码。
---

# 分页查询规范
本技能介绍如何使用封装好的 `withPagination` 进行分页查询。

## 依赖导入
```typescript
import { withPagination } from '/path/to/utils/pagination.js';
```
## 代码模板（以分页查询菜单为例）
```typescript
export async function listMenus(
  db: Db,
  params: { page: number; pageSize: number },
): Promise<PaginatedData<Menu>> {
  const page = Math.max(1, params.page);
  const pageSize = Math.min(100, Math.max(1, params.pageSize));

  const countResult = await db
    .select({ count: sql<number>`count(*)` })
    .from(menusTable);

  const total = Number(countResult[0]?.count ?? 0);

  const items = await withPagination(
    db
      .select({
        id: menusTable.id,
        name: menusTable.name,
        description: menusTable.description,
        createdAt: menusTable.createdAt,
        updatedAt: menusTable.updatedAt,
      })
      .from(menusTable)
      .orderBy(menusTable.id)
      .$dynamic(),
    page,
    pageSize,
  );

  return { items, total, page, pageSize };
}
```