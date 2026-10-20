# ai-build-support Rules

## xcodegen の直接呼び出し禁止

**`xcodegen` を直接実行してはならない。**

このルールは `ai-build-support/` サブモジュールを持つすべてのプロジェクトに適用される。

`xcodegen generate` は必ず `gen_build_install.zsh` 経由で実行すること:

```bash
./ai-build-support/gen_build_install.zsh --build-check
./ai-build-support/gen_build_install.zsh --sim
./ai-build-support/gen_build_install.zsh -n "iPhone"
# など
```

`gen_build_install.zsh` が内部で `xcodegen generate` を適切なタイミングで呼ぶ。
Claude が直接 `xcodegen generate` や `xcodegen` を実行することは **いかなる理由があっても禁止**。
