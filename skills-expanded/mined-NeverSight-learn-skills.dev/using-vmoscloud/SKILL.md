---
name: using-vmoscloud
description: Use when 需要通过 VMOSCloud OpenAPI、SSH 隧道和 ADB 连接云手机，或排查签名正确但 `/padApi/adb` / `infos` 等接口返回 `System is busy` 的情况。
---

### vmoscloud文档

- [**快速参考**](https://cloud.vmoscloud.com/vmoscloud/doc/zh/server/llms.html) (推荐)(重要)(必读)
- [完整文档](https://cloud.vmoscloud.com/vmoscloud/doc/zh/server/OpenAPI.html)

## ADB 正确链路

1. 先请求 `/vcpcloud/api/padApi/adb`，body 形如 `{"padCode":"<pad>","enable":true}`
2. 若返回 `code=200` 且 `data.command`、`data.key` 完整，直接使用返回值建 SSH 隧道
3. 若 `/adb` 返回 `command/key/adb` 不全，或文档明确提示需要先开启 ADB，则调用 `/vcpcloud/api/padApi/openOnlineAdb`
4. `/openOnlineAdb` 成功后再重试 `/adb` 获取 `command` 和 `key`
5. 用 `sshpass -p "$KEY"` 启动 SSH 隧道
6. 再执行 `adb connect localhost:<本地映射端口>`
7. 连接后立刻跑：
   - `adb devices -l`
   - `adb -s <serial> get-state`
   - `adb -s <serial> shell getprop ro.product.model`

示例：

```bash
sshpass -p "$KEY" ssh -oHostKeyAlgorithms=+ssh-rsa -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user@host -p 1824 -L 6280:adb-proxy:43206 -Nf
adb connect localhost:6280
adb -s localhost:6280 get-state
```

## 遇到 `System is busy`

- 先检查签名是否正确：紧凑 JSON、`x-content-sha256`、`authorization`, 只有在“签名正确 + 接口参数正确 + 历史 SSH 隧道也失败”时，才进一步怀疑设备状态或供应商侧问题

## 仓内库入口

生成客户端命令：

```bash
bash /workspace/mtm-vmossdk/scripts/generate_client.sh
```

高层示例：

```python
from mtm_vmos_sdk import VMOSClient

client = VMOSClient(
    access_key="${VMOSCLOUD_API_KEY}",
    secret_key="${VMOSCLOUD_SECRET_KEY}",
    api_base="https://api.vmoscloud.com",
    api_host="api.vmoscloud.com",
    service="armcloud-paas",
)

sts = client.sts_token_by_pad_code("${VMOSCLOUD_TESTING_DRIVER_ID}")
adb = client.adb_info("${VMOSCLOUD_TESTING_DRIVER_ID}")
```

低层示例：

```python
from mtm_vmos_sdk import SignedVMOSApiClient, VMOSAuthConfig
from mtm_vmos_sdk.generated.api.sdk_token_api import SDKTokenApi
from mtm_vmos_sdk.generated.models.vcpcloud_api_pad_api_pad_properties_post_request import (
    VcpcloudApiPadApiPadPropertiesPostRequest,
)

api_client = SignedVMOSApiClient(
    VMOSAuthConfig(
        access_key="${VMOSCLOUD_API_KEY}",
        secret_key="${VMOSCLOUD_SECRET_KEY}",
        api_base="https://api.vmoscloud.com",
        api_host="api.vmoscloud.com",
        service="armcloud-paas",
    )
)

sdk_api = SDKTokenApi(api_client)
result = sdk_api.vcpcloud_api_pad_api_sts_token_by_pad_code_post(
    VcpcloudApiPadApiPadPropertiesPostRequest(
        padCode="${VMOSCLOUD_TESTING_DRIVER_ID}",
    )
)
```

## 参考

- 官方文档：`https://cloud.vmoscloud.com/vmoscloud/doc/zh/server/OpenAPI.html`
- 官方签名说明：`https://cloud.vmoscloud.com/vmoscloud/doc/zh/server/example.html`
