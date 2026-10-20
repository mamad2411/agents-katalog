# 買いたいものリストアプリ - 開発ルール

## 必須セキュリティルール
以下のファイルは絶対に触らない：
- `.env` ファイル
- Supabase関連の認証情報
- Auth0関連の認証情報
- JWT関連の鍵やシークレット
- APIキー、トークン、認証情報を含むファイル全般

機密ファイルの編集が必要な場合は、必ず指示を仰ぐ。

## 開発ルール
- `/domain`以下と`/infrastructure`以下のファイルは無視する
- 連続で修正に失敗した場合は、作業を止めて現状を報告する
- エラーが発生した場合は自律的に解決を試み、失敗したら報告する

## 技術スタック
- TypeScript + Remix v2 + Vite
- Supabase (PostgreSQL)
- Auth0 (認証)
- TailwindCSS + DaisyUI

## ファイル構成
```
/app
  /models          # データアクセス（*.server.ts）
  /routes          # Remixルート
  /components      # UIコンポーネント
```

## コーディング原則と実装例

### データフロー図
```
ユーザー → Routes (loader/action) → Models → Database
         ↘ Components (props経由でデータ渡し)
```

### 1. データフロー（正しい例）
```typescript
// ❌ NG: コンポーネントが直接modelsにアクセス
export default function WishItemList() {
  const items = await getWishItems(); // NG!
}

// ✅ OK: routesのloaderでデータ取得 → componentsにprops渡し
// app/routes/wish-items/_index.tsx
export const loader = async ({ request }: LoaderArgs) => {
  const items = await getWishItems(request); // Models層呼び出し
  return json({ items });
};

export default function WishItemsIndex() {
  const { items } = useLoaderData<typeof loader>();
  return <WishItemList items={items} />; // propsでデータ渡し
}
```

### 2. modelsファイル（Database層との接続）
```typescript
// app/models/wishItem.server.ts
export async function getWishItems(request: Request) {
  const session = await getSession(request);
  const { data, error } = await supabase // Database操作
    .from('wish_items')
    .select('*')
    .eq('user_id', session.get('userId'));
  
  if (error) throw new Error(error.message);
  return data;
}
```

### 3. コンポーネント（UI表示のみ）
```typescript
// app/components/features/wish-item/WishItemList.tsx
interface Props {
  items: WishItem[]; // routesからpropsで受け取る
}

export default function WishItemList({ items }: Props) {
  // DBアクセスなし、UI表示のみ
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

### 4. 重要なルール
- Routes: loader/actionでModels呼び出し、ComponentsにDATAを渡す
- Models: Database操作とビジネスロジック（.server.tsファイル）
- Components: propsを受け取ってUI表示するのみ

// ❌ Biomeエラーが出る
import { ActionArgs, LoaderArgs } from '@remix-run/node';

// ✅ 修正版
import type { ActionArgs, LoaderArgs } from '@remix-run/node';