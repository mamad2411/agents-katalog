# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/topic-qualixar-superlocalmemory-slm-cache/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: KV cache for repeated reads — call slm_cache_get(key) first; on a miss do the expensive operation then slm_cache_set(key, value, ttl_seconds) to store it; on a hit use the returned value directly; alw
