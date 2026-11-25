---
name: get-tweet
description: Fetch a public X/Twitter post as JSON via the get-tweet CLI. Handles photo, video, replies, quote-RTs and link cards.
---

# get-tweet

`get-tweet` CLI で X (Twitter) の公開ポストを Syndication API から JSON で取得する。

## いつ使うか

- ユーザーが X/Twitter の URL または数値のツイート ID を提示したとき
- 本文・投稿者・メディア (画像/動画)・引用元/返信元・リンクカードを構造化データで扱いたいとき

## 基本コマンド

```bash
get-tweet <URL or tweet ID>          # 1 行の raw JSON
get-tweet <URL or tweet ID> --pretty # 整形出力 (人間確認用)
```

## 実行方針 (重要)

1. **最初は素で叩く。パイプで `jq` を挟まない。** 種別 (動画/画像/返信/引用/リンク) ごとにキーが増減するので、フル JSON でスキーマを確認してから絞る。
   ```bash
   get-tweet <url> > /tmp/tw.json
   jq 'keys' /tmp/tw.json
   ```
2. スキーマを確認してから `jq` で必要フィールドだけ抜く。
3. jq が期待通り動かないときは、パイプをやめてフル JSON を取り、キー構造を見てから jq を組み直す。

## スキーマ (種別ごとの差分)

### 常にあるフィールド

- `.id_str`, `.text`, `.created_at`, `.lang`
- `.favorite_count`, `.conversation_count`
- `.user.screen_name` / `.user.name` / `.user.id_str` / `.user.is_blue_verified`
- `.entities.urls[]?` (本文中リンク) / `.entities.media[]?` (メディア短縮 URL)

### メディア (画像・動画・GIF)

- 実データは `.mediaDetails[]`。`.type` は `photo` / `video` / `animated_gif`
- 画像のみのポストは `.photos[]` にも同内容が入る
- 動画はトップレベルに **さらに** `.video` が付き、`.variants[]` に HLS/mp4 URL。MP4 の最高ビットレートは `.mediaDetails[].video_info.variants[]` から `select(.content_type=="video/mp4")` で拾って sort する

### 返信

`.in_reply_to_status_id_str` / `.in_reply_to_screen_name` / `.in_reply_to_user_id_str` と、親ポスト全文が `.parent` に埋まる。

### 引用リツイート

`.quoted_tweet` に引用元がフルで入る (`.quoted_tweet.text`, `.quoted_tweet.user.screen_name` …)。

### リンクカード

`.card.name` (`summary_large_image` など) と `.card.binding_values.<key>.string_value` / `.image_value.url`:

- `.card.binding_values.title.string_value`
- `.card.binding_values.description.string_value`
- `.card.binding_values.domain.string_value`
- `.card.binding_values.thumbnail_image_original.image_value.url`

## 汎用の正規化 jq

全種別で通ることを確認済み (動画のみ / 返信+動画+画像 / 返信+画像複数 / 引用RT / リンクカード)。

```jq
{
  id: .id_str,
  url: ("https://x.com/" + .user.screen_name + "/status/" + .id_str),
  created_at, lang, text,
  favorite_count,
  reply_count: .conversation_count,
  author: {
    id: .user.id_str,
    screen_name: .user.screen_name,
    name: .user.name,
    verified: (.user.is_blue_verified // false)
  },
  reply_to: (
    if .in_reply_to_status_id_str then {
      status_id: .in_reply_to_status_id_str,
      screen_name: .in_reply_to_screen_name,
      user_id: .in_reply_to_user_id_str,
      parent_text: (.parent.text // null)
    } else null end
  ),
  quoted: (
    if .quoted_tweet then {
      id: .quoted_tweet.id_str,
      screen_name: .quoted_tweet.user.screen_name,
      text: .quoted_tweet.text,
      created_at: .quoted_tweet.created_at
    } else null end
  ),
  media: [
    (.mediaDetails // [])[] | {
      type: .type,
      thumbnail: .media_url_https,
      expanded_url: .expanded_url,
      video: (
        if .video_info then {
          duration_ms: .video_info.duration_millis,
          aspect_ratio: .video_info.aspect_ratio,
          variants: [
            .video_info.variants[]
            | select(.content_type == "video/mp4")
            | {bitrate, url}
          ] | sort_by(-(.bitrate // 0))
        } else null end
      )
    }
  ],
  urls: [
    (.entities.urls // [])[] | {url: .expanded_url, t_co: .url, display: .display_url}
  ],
  card: (
    if .card then {
      name: .card.name,
      title: (.card.binding_values.title.string_value // null),
      description: (.card.binding_values.description.string_value // null),
      domain: (.card.binding_values.domain.string_value // null),
      image: (.card.binding_values.thumbnail_image_original.image_value.url
              // .card.binding_values.summary_photo_image_original.image_value.url
              // null),
      url: .card.url
    } else null end
  )
}
```

## ワンライナー

```bash
# 本文と投稿者
get-tweet <url> | jq '{text, user: .user.screen_name, created_at}'

# 動画の最高画質 mp4 URL
get-tweet <url> | jq -r '[.mediaDetails[]?.video_info.variants[]? | select(.content_type=="video/mp4")] | sort_by(-.bitrate) | .[0].url'

# 画像 URL 一覧
get-tweet <url> | jq -r '[.mediaDetails[]? | select(.type=="photo") | .media_url_https][]'

# 返信元
get-tweet <url> | jq '{reply_to: .in_reply_to_status_id_str, parent: .parent.text}'

# 引用元
get-tweet <url> | jq '{quoted_text: .quoted_tweet.text, quoted_user: .quoted_tweet.user.screen_name}'

# リンクカード OGP
get-tweet <url> | jq '{title: .card.binding_values.title.string_value, desc: .card.binding_values.description.string_value, image: .card.binding_values.thumbnail_image_original.image_value.url}'
```

## 終了コード

| code | 意味 |
|------|------|
| 0    | 成功 |
| 1    | 引数エラー・URL 解決失敗 |
| 2    | ツイートが存在しない / 削除済み |
| 3    | Syndication API のエラー |
| 4    | 内部エラー |

## 注意

- 認証不要。非公開・保護アカウントは取得できない。
- スキーマは Twitter 側の都合で変わる。**必ず一度フル JSON を確認してから jq を書く。**
