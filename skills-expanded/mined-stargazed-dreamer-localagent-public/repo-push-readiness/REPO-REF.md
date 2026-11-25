# Repo Ref
- source: https://github.com/stargazed-dreamer/localagent-public (path: .agents/skills/dev/repo-push-readiness/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 把本地仓库推向远端（尤其多机协作）前的就绪体检。当用户说「要推远端/多机合作/开源/首次 push/加 remote/换台机器继续」时使用。逐项检查密钥与凭据泄露、大文件、gitignore 正确性、换行符与二进制声明、协作资产是否入库，并给出可执行的修复动作。核心不是写 .gitignore，而是「先扫真相、再改规则、最后验证」——凭据进了历史就得洗，规则写错只是噪音。
