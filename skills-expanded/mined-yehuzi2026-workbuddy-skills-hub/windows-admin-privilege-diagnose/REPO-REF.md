# Repo Ref
- source: https://github.com/yehuzi2026/workbuddy-skills-hub (path: categories/09-windows-ops/windows-admin-privilege-diagnose/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 诊断 Windows 本地账户的"管理员权限"并给出提权方案。当用户说「把某用户改成管理员」「我不是管理员吗」「为什么提示拒绝访问」「关掉 UAC」「让程序默认以管理员运行」「以管理员身份运行脚本」时使用。区分三种完全不同的"没权限"：①账户不在管理员组 ②账户在组但 UAC 筛选令牌降级 ③第三方软件（如 WorkBuddy 命令安全策略）程序黑名单拦截。核心判据：令牌组的「只用于拒绝的组」标记
