---
name: eliteforge-poseidon-cli
description: 通过 poseidon 命令操作波塞冬部署平台。当用户要求操作波塞冬的项目查询、应用创建、应用查询、配置创建、配置查询、配置关联应用构建、应用部署、应用日志查询等相关操作时应使用该包。metadata(search-git,page-apps,page-apps-simple,list-project-entries,list-project-envs,list-project-products,list-app-types,list-app-types-simple,list-build-tools,list-build-tools-simple,list-base-images,list-base-images-simple,get-app,create-app,list-configs,list-configs-simple,create-config,update-config,delete-config),build(trigger,page-builds,page-builds-simple,list-build-params,build-overview,get-log),ops(deploy-app,search-logs,log-context,restart-app),atomic(rebuild-and-deploy,runtime-errors)。
metadata:
  version: 1.0.1
---

# EliteForge Poseidon CLI
## 依赖准备
以下工具不存在，先尝试自动安装：
- python3
- pipx
- jq
上下文或环境变量中的**内部变量**缺失，终止运行，提示用户补全相关变量。  

## 工作流
1. 先确认依赖和变量可用。
2. 每次使用前都检查 `eliteforge-poseidon-cli` 是否已安装。
   - 未安装时执行：`pipx install eliteforge-poseidon-cli`
3. 每次使用前都执行：`pipx upgrade eliteforge-poseidon-cli`
4. 先看帮助再执行具体命令，避免硬编码能力说明。
   - 所有子命令说明 `poseidon -h`
   - 元数据板块：应用与配置元数据管理： `poseidon metadata -h`
     - 注意：创建应用时，依赖gitlab仓库，可使用 `$gitlab-cli-skills` 先在赛迪GitLab平台上创建好项目仓库
   - 构建板块：触发构建、查询构建记录与上下文 `poseidon build -h`
   - 运维板块：发布、日志检索与重启 `poseidon ops -h`
   - 原子命令：`poseidon atomic -h`
     - 构建并发布指定应用：poseidon atomic rebuild-and-deploy 按应用名/ID触发构建并轮询到构建完成，并检测实例是否启动完毕，默认自动部署到开发环境
     - 查看应用实例的错误日志：poseidon atomic runtime-errors  按应用名检索运行时错误日志，并逐条抓取命中时间点的上下文
5. 按用户目标执行命令，可编写脚本自行编排接口.

## Environment Variables

- `ELITEFORGE_SKILL_POSEIDON_BASE_URL` [optional] Platform URL; defaults to `https://poseidon.cisdigital.cn/`.
- `ELITEFORGE_SKILL_POSEIDON_USERNAME` [required] Platform username for account authentication.
- `ELITEFORGE_SKILL_POSEIDON_PASSWD` [required] Platform password for account authentication.
- `ELITEFORGE_SKILL_POSEIDON_AUTH_TYPE` [optional] Authentication mode; supports `ACCOUNT`, `API_TOKEN`, or `BEARER`, and defaults to `ACCOUNT`.
- `ELITEFORGE_SKILL_POSEIDON_PRODUCT_ID` [optional] Product ID; specific commands may override it with command parameters.
- `ELITEFORGE_SKILL_POSEIDON_PROJECT_ID` [optional] Project ID; specific commands may override it with command parameters.
- `ELITEFORGE_SKILL_POSEIDON_AUTH_APP_ID` [conditional] Required when `ELITEFORGE_SKILL_POSEIDON_AUTH_TYPE=API_TOKEN`.
- `ELITEFORGE_SKILL_POSEIDON_AUTH_APP_SECRET` [conditional] Required when `ELITEFORGE_SKILL_POSEIDON_AUTH_TYPE=API_TOKEN`.
- `ELITEFORGE_SKILL_POSEIDON_TOKEN` [conditional] Required when `ELITEFORGE_SKILL_POSEIDON_AUTH_TYPE=BEARER`.

## Output Rules

- 输出保持简洁，必要时可配合 `jq` 等Linux管道工具，处理接口JSON响应。
- 失败时返回实际执行的命令和关键报错
- 需要更多命令说明时，继续引导查看对应 `-h`
