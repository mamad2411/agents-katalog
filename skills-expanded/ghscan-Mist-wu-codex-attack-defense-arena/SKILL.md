# Attacker Skill

目标：在不因单次失败中断的前提下，逐步扩大探测面、复用有效路径、并在必要时提升 burst 压力。

默认原则：
- 先信息探测，再加压
- 优先记录可复用路径、头部技巧和触发条件
- 每轮都把有效打法沉淀到知识库
- 当存在稳定的业务入口时，优先做 query-aware 的路径聚焦；不要用随机后缀破坏已知有效 query
- 如果已知防守方会拦截伪造转发头，就把它们降级为低优先级噪音
- 对 `/echo?msg=...` 这类 query-bearing 路径要保留原始查询语义，fuzz 只能轻微扰动，不要把 query 打碎
- 只要出现稳定的 `msg=` 入口，就把它当成高优先级保留对象，优先复用而不是重新发明路径
- 即使是 fallback 单点探测，也不要在 `msg=` 路径上追加随机 `nonce`；保留 query 原样比补噪音更重要
- 当 `/asset?name=readme.txt` 可用时，把 `name=` 及 traversal / 编码变体提升为主线，优先复用 `/asset?name=../flag.txt`、`/asset?name=..%2Fflag.txt`、`/asset?name=..%252Fflag.txt`
- 对 `/asset?name=...` 这类 query-bearing 路径同样要保留原始 `name=` 语义，fuzz 只能作用在非 `name` 路径上
- 当防守方把活跃连接数卡得很低、请求超时也压到几十毫秒时，优先切到高频重连/瞬时占槽而不是继续扩散路径面：用短寿命半开请求持续刷新 active slots；一旦 cutoff 进入 0.04s 级别，就不要再依赖单连接 drip，再保留一个小探测口做 flag 提交
