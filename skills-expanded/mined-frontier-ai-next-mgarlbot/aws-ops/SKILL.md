---
name: aws_ops
description: AWS EC2 — инстансы, VPC, subnets через aws_api tool
triggers: [aws, ec2, amazon, instance, инстанс, сервер aws, vpc, subnet, ami]
tools: [aws_api]
platform: all
---

## AWS EC2 (`aws_api` tool)

Креды в настройках бота: `AWS_PROFILE` **или** `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`, плюс `AWS_REGION`.
**Не** передавай ключи в аргументах и **не** выводи их в ответ.

### Когда использовать

- «покажи EC2 / инстансы в AWS»
- «подними t3.micro в eu-central-1»
- «останови / запусти инстанс i-…»
- «какие VPC / subnets / security groups»

### Безопасность (обязательно)

- **Не** вызывай `terminate_instance` без **явного** запроса пользователя на удаление.
- Для `terminate_instance` нужен `params.confirm: true`.
- По умолчанию предпочитай `t3.micro` / `t3.small`; не запускай дорогие типы без запроса.
- Перед `run_instance`: `list_vpcs` → `list_subnets` → `list_security_groups` → `list_amis` (Ubuntu/Amazon Linux).
- После `run_instance` — краткий отчёт: InstanceId, IP, тип, регион.

### Типовые вызовы

**Инстансы:**
```json
{"action": "list_instances", "params": {"region": "eu-central-1"}}
{"action": "get_instance", "params": {"instance_id": "i-0123456789abcdef0", "region": "eu-central-1"}}
```

**Запуск (минимальный):**
```json
{
  "action": "run_instance",
  "params": {
    "region": "eu-central-1",
    "ami_id": "ami-xxxxxxxx",
    "instance_type": "t3.micro",
    "name": "mgarlbot-test",
    "key_name": "my-key",
    "subnet_id": "subnet-xxx",
    "security_group_ids": ["sg-xxx"]
  }
}
```

**Stop / start:**
```json
{"action": "stop_instance", "params": {"instance_id": "i-xxx", "region": "eu-central-1"}}
{"action": "start_instance", "params": {"instance_id": "i-xxx", "region": "eu-central-1"}}
```

**Terminate (только по явной просьбе):**
```json
{"action": "terminate_instance", "params": {"instance_id": "i-xxx", "region": "eu-central-1", "confirm": true}}
```

**Сеть и образы:**
```json
{"action": "list_vpcs", "params": {"region": "eu-central-1"}}
{"action": "list_subnets", "params": {"region": "eu-central-1", "vpc_id": "vpc-xxx"}}
{"action": "list_security_groups", "params": {"region": "eu-central-1"}}
{"action": "list_amis", "params": {"region": "eu-central-1", "owners": ["amazon"], "name_filter": "ubuntu-noble", "max_results": 10}}
```

### Ошибки

- «AWS не настроен» → ⚙ Настройки → AWS (профиль или ключи + регион).
- `UnauthorizedOperation` → у IAM не хватило прав (EC2 read/run).
