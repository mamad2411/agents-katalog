---
name: check-ci-result
description: "GitHub PRのCI失敗テスト結果をPlaywrightで取得し、失敗テスト名とエラーメッセージのサマリを返す。"
argument-hint: "[PR URL or number (optional)]"
context: fork
allowed-tools:
  - Bash
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_click
  - mcp__playwright__browser_evaluate
  - mcp__playwright__browser_wait_for
---

# Check CI Result

GitHub Actions の CI 失敗テスト結果を確認し、サマリを返す。

## 入力

- `` が PR URL または PR 番号の場合、それを使う
- 引数がない場合、現在のブランチから PR を特定する:
  `!gh pr view --json number,url -q '.url' 2>/dev/null || echo "NO_PR"`

## 手順

### 1. PR の特定

引数または現在ブランチから PR の URL を決定する。
GitHub の PR URL 形式: `https://github.com/{owner}/{repo}/pull/{number}`

### 2. CI Annotations ページから失敗情報を一括取得

**最も効率的な方法**: Actions run ページの Annotations セクションにエラーサマリがある。
個別ジョブを1つずつ開く必要はない。

1. PR の Checks タブを開く: `{pr_url}/checks`
2. workflow run のリンク (例: `test on: push`) をクリックして Actions run ページへ遷移
3. Actions run ページで以下の JavaScript を実行し、Annotations からエラーを一括抽出:

```javascript
() => {
  // Annotations テーブルからエラー行を取得
  const rows = document.querySelectorAll('table tr');
  const errors = [];
  for (const row of rows) {
    const text = row.textContent.trim();
    if (text.includes('Process completed with exit code') || text.includes('Error')) {
      errors.push(text);
    }
  }
  return errors;
}
```

### 3. 失敗ジョブのログから詳細を取得

Annotations だけでは失敗テスト名が分からない場合が多い。
**失敗ジョブを開いて "Run RSpec" ステップのログ末尾を取得する**。

各失敗ジョブについて:
1. 失敗ジョブのリンクをクリック
2. ページ読み込み後、以下の JavaScript でログ末尾の失敗テスト情報を抽出:

```javascript
() => {
  const details = document.querySelectorAll('details');
  for (const d of details) {
    const summary = d.querySelector('summary');
    if (summary && summary.textContent.includes('Run RSpec')) {
      d.open = true;
      const text = d.innerText;
      // "Failed examples:" 以降を取得
      const failedIdx = text.indexOf('Failed examples:');
      if (failedIdx !== -1) {
        return text.slice(failedIdx, failedIdx + 2000);
      }
      // なければ末尾1500文字を返す
      return text.slice(-1500);
    }
  }
  // RSpec 以外のテストフレームワーク (Jest等) の場合
  for (const d of details) {
    const summary = d.querySelector('summary');
    if (summary && (summary.textContent.includes('test') || summary.textContent.includes('Test'))) {
      d.open = true;
      const text = d.innerText;
      return text.slice(-1500);
    }
  }
  return 'No test step found in this job';
}
```

### 4. 全失敗ジョブを処理する必要はない

CI のマトリクスビルドでは同じテストが複数ジョブに分散される。
**失敗ジョブの結果は重複することが多い**ので:
- まず1つの失敗ジョブからログを取得
- 他のジョブは失敗テスト名だけ確認し、異なるテストが失敗している場合のみ詳細を取得

### 5. 結果のサマリを返す

以下の形式で結果をまとめる:

```
## CI 失敗結果サマリ

**PR**: #番号 (タイトル)
**失敗ジョブ数**: N / M

### 失敗テスト一覧
- `spec/path/to/file_spec.rb:LINE` - テストの説明
- `spec/path/to/file_spec.rb:LINE` - テストの説明

### エラー詳細
(必要に応じてエラーメッセージの要約)
```

## 注意事項

- Playwright で GitHub にアクセスするため、ブラウザでGitHubにログイン済みである必要がある
- ログが大きい場合は `slice` で必要部分のみ取得し、コンテキストを節約する
- lint 系の失敗 (rubocop, eslint等) の場合も同様にログ末尾を確認する
