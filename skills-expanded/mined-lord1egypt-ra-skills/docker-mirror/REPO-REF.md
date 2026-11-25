# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/d/docker-mirror/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Docker 镜像拉取工具，自动切换镜像源。当官方 registry (docker.io) 拉取超时或失败时，自动尝试备用镜像（docker.1ms.run、docker.m.daocloud.io）。适用于网络受限的 Linux 环境。需要 sg (sgdocker group) 和 docker 已安装。触发场景：(1) 用户请求拉取 Docker 镜像，(2) docker pull 失败
