---
description: 指定したルート/コントローラ/機能の4段階ACL（グループ権限）が正しく実装されているか監査する。
disable-model-invocation: true
---

対象「`$ARGUMENTS`」の認可（4段階ACL）を `security-auditor` エージェントで監査してください。

確認観点:
- 保護対象操作がサーバ側（`check.group.permission` ミドルウェア / Policy / FormRequest）で認可されているか。
- 権限チェックが `user_id` と `group_id` の**両方**でスコープされているか（グループ横断の漏れ）。
- 承認待ち（`is_approved=false`）が弾かれ、必要権限レベルが適切か。
- IDOR：ID 直打ちで他グループ/他人のリソースにアクセスできないか。
- Blade の表示制御だけに依存していないか。

`ファイル:行`・想定攻撃シナリオ・修正案を添えて、深刻度別（Critical/High/Medium/Low）に報告してください。
不足するテスト観点があれば `pest-tester` での追加を提案してください。
