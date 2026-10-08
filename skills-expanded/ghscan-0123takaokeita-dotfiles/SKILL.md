---
name: laravel-lint
description: Fixes or suggests fixes to match Laravel coding standards. Use when the user asks to fix Laravel code style, apply Laravel conventions, or /laravel-lint.
disable-model-invocation: true
created: 2026-03-01T12:23
updated: 2026-03-01T12:23
---

# Laravel 規約に沿った修正

このスキルは **Laravel プロジェクト** でだけ実行すること。まず `composer.json` に `laravel/framework` が含まれるか確認し、Laravel プロジェクトでない場合は「このプロジェクトは Laravel ではありません」とだけ返す。

Laravel プロジェクトの場合、次の手順で規約に沿った修正を行う。

1. **規約を参照する**: `~/dotfiles/cursor/laravel-standards.md`（またはこの設定ディレクトリ内の `laravel-standards.md`）を読み、Laravel コーディング規約を確認する。
2. ユーザが指定したファイル、または現在のコンテキストで対象となる PHP ファイルについて、規約に沿うか確認する。
3. 規約違反があれば、修正案を提示する。可能な範囲で **Laravel Pint** の自動修正（`./vendor/bin/pint`）を提案し、それで対応できない部分は手動修正案を出す。
4. UseCase の配置・Controller の薄さ・Form Request / Policy / Resource の使い方など、規約で定めている構成にも従うよう提案する。

出力は「何を直すか」「どう直すか」が分かるようにする。
