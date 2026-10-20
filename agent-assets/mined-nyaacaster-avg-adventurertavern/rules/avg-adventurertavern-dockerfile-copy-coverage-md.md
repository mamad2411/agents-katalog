---
globs: "{*.ts,*.tsx,*.html,*.css,*.json,*/}"
description: 当用户在项目根目录新增文件或目录时触发，检查 Dockerfile COPY 指令是否覆盖了新增内容，防止构建时出现文件找不到的错误。
alwaysApply: false
---

当用户在项目根目录新增文件或目录时，自动执行以下检查：

1. 读取 Dockerfile，找出 builder 阶段所有的 COPY 指令
2. 检查新增文件的扩展名是否被某条 COPY 通配符覆盖（如 *.tsx、*.css）
3. 检查新增目录名是否在 COPY 指令中明确列出（如 COPY components/ ./components/）
4. 如果未覆盖，立即提示用户需要在 Dockerfile 中补充对应的 COPY 指令，并给出具体的修改建议
5. 同时检查 .dockerignore，确认该文件/目录没有被意外排除

判断规则：
- 根目录 *.ts / *.tsx / *.html / *.css 文件 → 对照 COPY *.tsx *.ts *.html *.css ./ 这类通配符行
- 根目录新目录 → 必须有对应的 COPY <dir>/ ./<dir>/ 指令
- 仅用于运行时（非构建时）的文件不需要 COPY，如 nginx.conf、docker-compose.yml