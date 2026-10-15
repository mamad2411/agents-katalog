# Repo Ref
- source: https://github.com/CharlesHahn/DuIvySkills (path: nonstd-residue/SKILL.md, branch: master)
- mined: 2026-10-15
- desc: 非标残基力场构建的完整流程指南。当 Agent 需要为共价修饰的非标准残基（如 BBO-10203 共价结合 CYS 形成的 CYB）构建 GROMACS 力场定义时必须调用此技能。覆盖场景：从 Sobtop 输出的 itp 文件（RESP2 电荷 + GAFF 拓扑已就绪）开始，生成 rtp/hdb 残基定义、注册 GAFF 参数到本地力场副本、组装 PDB、运行 pdb2gmx 验证。适用于任
