# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/g/gateway-upgrade-local-fork/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: OpenClaw 网关服务本地 fork 升级 skill。覆盖 backup → upgrade → env-merge → verify 全流程。专门处理 OpenClaw systemd service 升级时丢失 user 自定义环境变量（CUDA / LD_LIBRARY_PATH / QMD_EMBED_MODEL）的问题，跑 qmd doctor 检查 RTX 30/40 系 GPU
