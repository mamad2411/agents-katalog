---
name: happy-ota
description: Publishes or rolls back a happy-app OTA update (JS only) through our own update server — checks which installed builds the update can reach, confirms one plan, publishes with `yarn ota`, then tells the user how to verify on the phone. Command-only — invoked via /happy-ota.
disable-model-invocation: true
---

# happy-app OTA 发布与回滚

App 的 JS 和资源可以不经过商店直接更新：`yarn ota`（`packages/happy-app/sources/scripts/ota.ts`）把更新上传到 happy-server（`/v1/ota/*`），App 里的 expo-updates 从 `https://api.happy-next.com/v1/ota/manifest` 拉取。

- **runtime version 就是原生 fingerprint**（`fingerprint.config.js`）。一个更新只会发给 fingerprint 相同的安装包。改了原生依赖、插件或 `app.config.js` 中影响原生的部分以后，fingerprint 会变，旧包就收不到这次更新，要先打新的原生包。
- **App 什么时候收到更新：**
  - 冷启动时，原生层会在后台下载更新，到下一次冷启动才换上。
  - App 从后台回到前台时，也会检查并下载（`hooks/useUpdates.ts`，在根布局里启动）。下载好后，收件箱顶部会出现「有可用更新」横幅，点一下立即重载。不点的话，下一次冷启动时生效。
- **渠道：** production、preview、development 各对应同名 channel，默认用 production。

调用本技能，就是授权执行下面「流程」第一、三、四段的操作。第二段的计划要用户确认后才能执行。由 `happy-next-release` 照本文件执行时，以它的发布计划为准，不再单独确认。

## 一、检查（不询问用户）

在 `packages/happy-app` 下：

1. **工作区：** 运行 `git status --porcelain --untracked-files=no`。有未提交的已跟踪改动时停下，让用户选「先提交」还是「不发布」。不要把未提交的改动发出去，`ota.ts` 遇到这种情况只会警告，不会拦。
2. **算出这次的 runtime：** 和发布时一样，要在 EAS 环境里算：
   ```bash
   T=$(mktemp -d); npx eas-cli env:pull production --path $T/p.env --non-interactive >/dev/null
   for p in ios android; do ( set -a; . $T/p.env; set +a; export APP_ENV=production NODE_ENV=production CI=1
     npx expo-updates runtimeversion:resolve --platform $p 2>/dev/null | tail -1 ); done; rm -rf $T
   ```
3. **哪些安装包收得到：** 把上一步的 runtime 和已经装在用户手机上的包的 fingerprint 对一下（工具：`.claude/skills/happy-ota/scripts/embedded-fingerprint.sh <ipa|apk>`）：
   - **最近一次 GitHub Release**（App Store 和 Android 用户用的就是它）：
     ```bash
     D=$(mktemp -d); gh release download <tag> -p '*-ios.ipa' -p '*-android.apk' -D $D
     ```
     解出 fingerprint 后删除目录。输出「no embedded fingerprint」，说明这个包打在自建 OTA 之前，收不到任何 OTA。
   - **Mac mini 测试包：** `~/wwwroot/appdown/builds/` 里最新的 `HappyNext-*.ipa`，用 orchestrator_exec 在 Mac mini 上执行 `unzip -p <ipa> 'Payload/*.app/EXUpdates.bundle/fingerprint'`。
   - **历史更新：** `yarn ota list --platform ios` 和 `--platform android`，列出之前的更新发到了哪些 runtime。

   哪个平台都对不上，就说明没有设备能收到这次更新。这时停下，告诉用户要先打原生包（测试包用 happy-ios-build，正式版走 happy-next-release）。
4. **这次包含哪些改动：** 从 `yarn ota list` 里取同平台最近一次更新的 gitCommit，执行 `git log --oneline <gitCommit>..HEAD -- packages/happy-app packages/happy-wire`。如果其中有原生相关的改动（`package.json` 里的依赖、`plugins/`、`modules/`、`targets/`、`patches/`、`app.config.js`），第 2 步算出的 runtime 应该已经变了，要和第 3 步的结论一起核对。

## 二、确认计划

一次性给用户看：

- 平台（ios、android 或 all）和 channel；
- runtime，以及能收到这次更新的包，比如「v2.22.0 App Store 版、Mac mini 192 号测试包」；
- 包含的提交（第 4 步），以及准备写的 `--message`；
- 「发布后用户的 App 会自动下载」。

用户确认后进入第三段。

## 三、发布

### 1. 取发布凭证（不显示，不落盘到仓库）

`OTA_ADMIN_TOKEN` 只放在 Public 机器的 `/www/ajax/happy-next.com/.env` 里。用一次性密钥对加密后传回本地，做法如下：

```bash
# 本地：生成密钥对，输出公钥的 base64
umask 077; mkdir -p /tmp/ota-key && cd /tmp/ota-key \
&& openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out priv.pem 2>/dev/null \
&& openssl pkey -in priv.pem -pubout | base64 -w0
```

```bash
# Public（orchestrator_exec，机器名 Public）：只返回密文
umask 077; P=$(mktemp); echo '<公钥 base64>' | base64 -d > $P; \
sudo -n grep '^OTA_ADMIN_TOKEN=' /www/ajax/happy-next.com/.env | cut -d= -f2- | tr -d '\r\n' \
| openssl pkeyutl -encrypt -pubin -inkey $P -pkeyopt rsa_padding_mode:oaep | base64 -w0; rm -f $P
```

```bash
# 本地：解密到只有自己可读的文件，删掉私钥，只输出长度（应为 64）
cd /tmp/ota-key && umask 077 && echo '<密文>' | base64 -d \
| openssl pkeyutl -decrypt -inkey priv.pem -pkeyopt rsa_padding_mode:oaep > token && rm priv.pem && wc -c < token
```

不要用 cat、echo 或者 `set -x` 把 token 打印出来，也不要把它写进命令行参数，只能通过 `OTA_ADMIN_TOKEN="$(cat /tmp/ota-key/token)"` 传给命令。

### 2. 发布

```bash
cd packages/happy-app && OTA_ADMIN_TOKEN="$(cat /tmp/ota-key/token)" \
  yarn -s ota publish --platform <ios|android|all> [--channel production] --message "<说明>" 2>&1 | grep -v 'npm warn' | tail -6
```

- 输出里的 `→ <平台>: runtime …` 必须等于第一段第 2 步算出的值；不一致说明环境有问题，停下汇报。
- 以 `✓ <平台> update <id> published` 为准，记下 id。

### 3. 核对服务器

```bash
curl -s -o /dev/null -w '%{http_code}\n' -H 'expo-platform: ios' -H 'expo-runtime-version: <runtime>' \
  -H 'expo-channel-name: production' -H 'expo-protocol-version: 1' https://api.happy-next.com/v1/ota/manifest
```

返回 200 即可。如果返回 204，说明这个 runtime 下没有可发的更新。

### 4. 清理

`rm -rf /tmp/ota-key /tmp/happy-ota-*`。如果接下来马上还要再发一次（比如用户要做真机测试），可以先留着，但要告诉用户凭证还在临时目录里，全部做完后再删。

## 四、汇报

简短说明：哪个平台、更新 id、runtime 对上了哪些包。然后告诉用户怎么在手机上验证：

- 最快的办法：App 切到后台，再切回前台，等几秒，收件箱出现「有可用更新」后点它；
- 或者完全关掉 App 再打开，重复两次（第一次下载，第二次生效）。

要求有可见变化的测试时，改动只放在本地，不提交，测完撤掉。

## 回滚

用户说「回滚 OTA」时：

1. 运行 `yarn ota list --platform <平台> --limit 10`，列出最近的更新。
2. **默认回到上一个正常的更新：** `yarn ota republish <id> --message "<原因>"`。它会把那个更新重新发成最新的一条。
3. **只有最近几个更新都有问题时，才回到包内版本：** `yarn ota rollback-to-embedded --platform <平台>`（默认用当前代码在 EAS 环境下算出的 runtime，也可以用 `--runtime <值>` 指定）。包内的 JS 可能比最近的正常更新还旧，例如会丢掉后来才加的功能，所以选这个之前要先向用户说明。
4. 回滚同样要先确认，凭证的取法同第三段第 1 步。执行后核对服务器，汇报和验证方式同上。回滚到包内版本以后，manifest 返回的 directive 是 `rollBackToEmbedded`。

## 禁止

- 不在未提交、未确认的情况下发布到 production。
- 不在聊天中显示 `OTA_ADMIN_TOKEN`，不把它写进仓库或日志。
- 不直接改 happy-server 的 OtaUpdate 表或 S3 里的文件；回滚只用 `republish` 和 `rollback-to-embedded`。
- runtime 和所有安装包都对不上时不发布，那样只会白白上传。
