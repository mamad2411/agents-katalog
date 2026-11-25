# Repo Ref
- source: https://github.com/kao273183/qa-claude-skill (path: skills/property-based-test-gen/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 從 TC 的邊界欄位（前置 / 預期）+ 既有 pytest，產生 hypothesis 的 @given strategies，把 example-based test 升級成 fuzz test。每條 property test 跑 100+ input 自動探邊界 bug，跟 mutation-testing 互補（mutation 找漏點 / property 用 fuzz 封死）。當使用
