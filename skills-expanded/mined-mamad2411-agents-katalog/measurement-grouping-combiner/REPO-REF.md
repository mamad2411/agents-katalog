# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-kjuhwa-skills-hub/measurement-grouping-combiner/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Group rows by `(resourceId, metricId, bucketTs)` into `Map<K, List<T>>`, then a per-granularity pure `combine…ByKey` merges each list into one composite record. One combiner per granularity (raw/1m/5m
