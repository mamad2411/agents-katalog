---
name: social-post
description: "Write X, Bluesky and Substack Notes posts and save them as Buffer drafts: an announcement of a newly published article, or a fragment the author wrote. Use when announcing an article (告知して) or sending a fragment to Buffer (Buffer に入れて). For a long X post from a daily-research report, use x-draft."
user-invocable: true
origin: shimo4228
---

# social-post — X / Bluesky / Substack Notes の投稿を Buffer の下書きにする

著者の投稿を、面ごとの制約に合わせて Buffer の下書き（draft）として入れる。予約と公開は
著者が Buffer の画面で行う。著者が「投稿して」「予約して」とチャットで指示したときだけ、手順 3 の OK の後に
その場で投稿か予約をする（手順 4）。入力は 2 種類:

- **告知** — 公開した記事 1 本から、面ごとの告知文を書く
- **断片** — 著者が書いた短文を、そのまま各面に載せられる形にする

日本語の投稿案を英訳して投稿する依頼は skill: `anthropic-skills:sns-en-post` が受ける。面の上限と下書きの扱いは、この skill の値を使う。

## 面の制約（as-of 2026-10-12）

| 面 | 長さ | リンク | その他 |
|---|---|---|---|
| X | 本アカウントは Premium で 25,000（2026-10-12 に Buffer の channel 設定で確認）。無料の上限は重み付き 280（日本語 1 字 = 2、URL は 23）。長文は feed で冒頭だけ見え、続きは畳まれる | 本文に置く | ハッシュタグとメディア種別に順位の加点は無い（公開コード） |
| Bluesky | 300 grapheme（URL も数える）かつ 3,000 byte | `metadata.bluesky.linkAttachment` に `url` だけを渡す。Buffer が記事の OGP から題・説明文・画像を組む（2026-11-15、1 件で観測） | 画像は 4 枚まで、alt 必須 |
| Substack | Buffer から出るのは Notes だけ。上限 10,000 字 | 告知ではリンクを付けない（著者の判断）。記事への導線は X と Bluesky が持つ。`metadata.substack.linkAttachment` は使わない | 添付は画像 6 枚・動画 1・リンク 1 のどれか 1 種。@ と # はリンクにならない |

- X のリンク位置: X の幹部が 2026-07 に「返信にリンクを置く必要はもうない」と発言した（二次報道）。小規模アカウントでどちらが効くかの実測は無い
- **X は LLM が書いたと判定された利用者に `llm_slop_user` ラベルを付け、30 日間フォロワー外へ配信しない**（公開コード）。判定方法は非公開。重複文の検知は日本語でも文字単位で動く（同じ公開コード）
- Substack は 2026-07 から投稿に AI 生成の検出表示を出す。Notes が対象かは未確認
- 面ごとに書き分けると反応が増える、という実測は無い。書き分けは制約への適合と、面の文化への合わせ方（意見）として扱う
- 本アカウントの X は 1 件あたり表示 10〜36 回、リンクのクリック 0〜3 回（2026-10-13〜11-15 の 100 件）。この件数では書き方の差を
  数字で比べられないので、告知の書き方は下の「カードとの分担」（見え方）から決めている

## カードとの分担（as-of 2026-11-15。著者のアカウントの画面で、告知 1 本を 3 面で、X は長文 2 件を観測）

リンク付きの投稿は、本文とカードが一緒に読まれる。本文は、カードが出さないことを言う。

| 面 | feed で見える本文 | カードが出すもの |
|---|---|---|
| X | 冒頭のおよそ 140 字まで。段落の切れ目で切れ、残りは「さらに表示」の中（長文 2 件からの推定） | 大きな画像と、その左下に小さく重なる題、ドメイン。URL の文字は出ない |
| Bluesky | 全文 | 画像、太字の題、説明文 2 行、ドメイン。題がいちばん目立つ |
| Substack Notes | 全文 | カードなし。記事そのものが、題・副題・画像つきで同じ feed に別に出る |

- 説明文は記事の OGP の description。note では副題と本文の冒頭がそのまま入る
- 題の末尾には媒体のアカウント名が付く（note は「｜<アカウント名>」）
- 題・画像・本文は一つの入口の 3 部品で、役を分ける（skill: `headline-craft` の「サムネイルの文字はタイトルと分担する」と同じ考え）。
  題は何についての記事か、画像は雰囲気、本文は書いた人の事情を持つ、という割り振りは、見え方から立てた方針で、
  反応の数字で確かめたものではない

## 手順

### 1. Buffer の現況を読む

`get_account`（organizationId とタイムゾーン）、`list_channels`（面と channelId）を読む。
面ごとの文字数上限は「面の制約」の表の値を使う。X の契約が変わったかもしれないときは、著者に 1 回聞く。
各面で直近の `sent` を `list_posts` で 5 件ずつ読む。これが voice と言語の見本になる。
同時に、直近の告知の書き出しを控える。`sent` が 0 件の面は、voice を下の voice.md に合わせ、
言語を著者に 1 回聞く。

### 2. 書く

**告知**
- 記事本文を読む。writing repo では日本語の正本が `note/<slug>.md`、Zenn 版が `articles/<slug>.md`、
  英語版が `substack/<slug>-en.md`。repo に無ければ公開 URL を読む。版が複数あるときは、
  面の言語に合う版の公開 URL を告知に使う
- 書く前に、カードに出るものを控える: 記事の題と、説明文になる副題・本文の冒頭 2 行
- X と Bluesky の本文は、カードに無いことで書き出す。書いた事情（何を考えていてここに来たか）、記事の中でいちばん
  引っかかった一点、決着しなかった問い、のどれか一つを選ぶ。リンクが無くても投稿する価値のある断片に、リンクが
  付いている形になる
- 文はできるだけ記事本文から取る — 著者の言葉になり、LLM の文型が減ると見ている（推定）。1 行目の案が要るときは
  skill: `headline-craft` に、題と説明文を渡し、「カードに無いことで書き出す」を制約として出させる
- X は冒頭の 1 段落、およそ 140 字で完結させる。feed で見えるのはそこまでと見ていて（上の表の推定）、続きの段落は開いた人が読む。
  上限が広いアカウントでも、足す段落は 1〜2 個までにする
- Bluesky は 1〜2 文。説明文に出る語（副題と冒頭の語）も避ける
- Substack は記事の問いを数文で渡す。リンクが無く、記事のカードは Substack が別に出すので、題の言い換えにせず、
  記事を読んでいない人にも一つの考えとして読める文にする（「この記事で」「続きは」のように記事を指す語を置かない）
- 著者が自分で投稿するアカウント（Buffer に繋いでいないもの）の文案を頼まれたら、同じ決まりで、そのアカウントの
  上限に合わせて書く。Premium でない X は重み付き 280 なので、本文は全角およそ 126 字と URL
- 言語は、手順 1 で読んだその面の直近の投稿に合わせる
- 文末は、書き方に合わせて一つに決める。独り言として書くなら口語のだ調（「〜だった」「〜んだよな」「〜気がしている」）、
  読者に向けて知らせる形で書くなら柔らかいですます調。一つの投稿の中で混ぜない。どちらにするか迷ったら、手順 1 で読んだ
  その面の直近の告知に合わせる
- 書き出しと文型は、手順 1 で控えた直近の告知と変える（重複の検知と slop の判定に効くと見ている。判定方法は非公開なので推定）

**断片**
- 著者の文をそのまま使う。面の上限を超えたときだけ、削る箇所の案を示して著者が選ぶ
- 文が無い面（例: 長すぎて Bluesky に入らない）は、その面を外すか、著者が書き直すかを聞く

voice は `~/.claude/skills/x-draft/references/voice.md` と手順 1 の見本に合わせる。
文の原則は `~/MyAI_Lab/writing/.claude/rules/writing-principles.md`、
tell の一覧は `~/MyAI_Lab/writing/.claude/skills/writing-ecosystem/references/style-diagnostics.md`。

### 3. 著者に見せる

見せる前に、リンクを付ける面ごとに、カードの題・説明文と本文を上から並べて読み、同じ語が重なっていたら本文を
書き直す。X は冒頭の 1 段落だけを切り出して、それとカードで記事の中身と書いた事情が伝わるかを見る。

Buffer に入れる前に、面ごとの本文（コードブロック）と長さ、リンクの置き場（本文 / カード）を並べて著者に見せ、
著者の OK を待つ。著者の直しはこの段階で反映し、OK が出た文だけを次の手順で Buffer に入れる。
X と Bluesky にリンクを付けるかもここで決めてもらう。`edit_post` は保存済みの metadata と合わせずに post 全体を検証し直すので、
付けたカードを後から足したり外したりする操作は確実でない。

### 4. Buffer に下書きを入れる

面ごとに `create_post` を 1 回呼ぶ。引数は毎回この 3 つを明示する — `mode` の既定は
`addToQueue` で、`saveToDraft` を落とすと実際に予約される:

- `saveToDraft: true`
- `schedulingType: "automatic"`
- `channelId`: 手順 1 の `list_channels` の値

著者がチャットで投稿を指示し（「投稿して」「ポストしといて」）、手順 3 で文に OK が出たときは、
`saveToDraft` を付けずに `mode: "shareNow"` と `schedulingType: "automatic"` で投稿する。指示が
予約なら `mode: "customScheduled"` と `dueAt`（account のタイムゾーンで、`currentTime` より後）。

手順 3 でリンクを付けると決めた面では、X は本文に書き、Bluesky は `metadata.bluesky.linkAttachment.url` に入れて
本文には書かない（本文の URL も 300 に数える）。付けないと決めた面には、本文にもカードにも入れない。Substack にはリンクを付けない。
`metadata.twitter.isAiGenerated` は著者が指定したときだけ設定する。

作った直後に、各 post を `get_post` で読み戻し、次の 3 点を確かめる。
- `status` が `draft` であること（投稿したときは `sent`。直後は `sending` のことがあるので、`sent` になるまで読み戻す。`error` が空であること）。
  違えば、post id と status をすぐ著者に伝える
- 本文が渡した文と一致すること
- Bluesky では、`metadata.bluesky.linkAttachment.url` が残っていること。消えていたら
  `edit_post` で本文の末尾に URL を足し、300 grapheme に収まるかを数え直す

429（rate limit）が返ったら止めて報告する。

### 5. 報告する

面ごとに、本文（コードブロック）、長さ（X は重み付きの値、Bluesky は grapheme 数）、post id、
読み戻した status を並べる。下書き（`draft`）への著者の直しは `edit_post` で反映し、また読み戻す。そのとき、読み戻した
`metadata`（Bluesky の `linkAttachment` を含む）を毎回そのまま渡す。投稿済みの post の直しは、著者に返す
（下書きでない post を編集すると公開される）。
