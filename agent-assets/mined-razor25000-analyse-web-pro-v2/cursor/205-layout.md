---
description: EXPLAIN how to use Layout to have consistant UI
globs: page.tsx, layout.tsx
---
We have utilities named `layout` to handle the layout of Dashboard page.

```tsx
import {
  Layout,
  LayoutContent,
  LayoutDescription,
  LayoutHeader,
  LayoutTitle,
  LayoutActions,
} from "@/features/page/layout";

export default async function SubscribersPage() {
  return (
    <Layout>
      <LayoutHeader>
        <LayoutTitle>Title</LayoutTitle>
        <LayoutDescription>Description</LayoutDescription>
      </LayoutHeader>
      <LayoutActions>
        <Button>Action</Button>
      </LayoutActions>
      <LayoutContent>// Content...</LayoutContent>
    </Layout>
  );
}
```