# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Ansible playbook that provisions a Raspberry Pi to gather Nature Remo (smart meter power) and SwitchBot Hub 2 (temperature/humidity/light) data via their cloud APIs and visualize it with Prometheus + InfluxDB + Grafana. The project originally read Inkbird IBS-TH1/TH2 sensors over Bluetooth (based on [this Qiita article](https://qiita.com/revsystem/items/4097d0ff447913e2675a)); that Bluetooth/Inkbird support has since been fully retired (see README "Licensing" section for history).

## Commands

Dry run (check mode) before applying:

```bash
ansible-playbook -i hosts -b iot.yml --diff --check
```

Apply for real:

```bash
ansible-playbook -i hosts -b iot.yml --diff
```

Limit to specific roles/tasks via tags (see "Tags" below), e.g.:

```bash
ansible-playbook -i hosts -b iot.yml --diff --tags influxdb_configure
```

Lint (config in `.ansible-lint`, rules `106`, `208`, `602` are skipped):

```bash
ansible-lint
```

Install Python dependencies (pinned in `requirements.txt`; installs `ansible`/`ansible-core` themselves, not project runtime deps):

```bash
pip install -r requirements.txt
```

There is no test suite; validation is `--check` dry-runs against a real or staging Raspberry Pi host plus `ansible-lint`.

## Architecture

`iot.yml` is the single playbook entrypoint. It targets the `[IoT]` group defined in `hosts` (edit `ansible_host`/`ansible_user` there before running) and applies roles in this fixed order:

1. `common` — hostname/`/etc/hosts` setup, rsyslog cron logging, enables `rsyslog`/`cron` services. `apt.yml` (OS package upgrade) exists but is currently commented out of `tasks/main.yml`.
2. `python3` — installs `python3-dev`/`python3-pip` only. The sensor script's own dependencies are managed separately by `uv` (see role 3), not system-wide pip.
3. `sensor_collector` — deploys the sensor-polling application to `{{ sensor_collector_home }}` (default `/home/pi/raspberry-sensor-collector`): copies `sensors_to_prometheus.py`, `remo.py` (Nature Remo client), `switchbot.py` (SwitchBot client), `test_switchbot.py`, `pyproject.toml`/`uv.lock`, templates `config.ini`, copies `DeviceList.csv` (device inventory incl. API tokens — `force: false` so a real production file is never clobbered by the repo's placeholder), installs `uv` for the `pi` user and runs `uv sync` to build `{{ sensor_collector_home }}/.venv`, and installs a cron job running `sensors_to_prometheus.py` via that venv every minute (with a `|| rm -f .../sensors.prom` fallback so a crashed run doesn't leave stale metrics visible in Prometheus).
4. `prometheus` — installs `prometheus` + `prometheus-node-exporter` via apt, templates their systemd unit files (both bound to `127.0.0.1` only) and `/etc/prometheus/prometheus.yml` — the template itself includes the `remote_write` block pointing at InfluxDB (`{{ influxdb_hostname }}`, a default from the `influxdb` role's `defaults/main.yml`; cross-role default references like this work because Ansible loads all roles' defaults at play start, not lazily per-role). node-exporter is pointed at `{{ sensor_collector_home }}/Data` as its textfile collector directory — this is how sensor readings reach Prometheus.
5. `grafana` — installs `grafana` via apt (dashboards must then be configured manually through the web UI: add the InfluxDB datasource, build dashboards/panels — this is not automated).
6. `influxdb` — installs `influxdb` and creates the `prometheus` database (no `remote_read`: Grafana talks to InfluxDB directly as its datasource).

### Data flow

`sensors_to_prometheus.py` (deployed by `sensor_collector`, run every minute via cron through its dedicated `uv`-managed venv) reads `DeviceList.csv` and `config.ini`, fetches data per device type via `remo.get_electric_power_data()` (Nature Remo Cloud API) or `switchbot.get_data()` (SwitchBot API v1.1, HMAC-signed), writes readings to per-device daily CSV files under `Data/Sensor/`, and rewrites a Prometheus textfile-collector `.prom` file (`Data/sensors.prom`) every run — including a `sensors_last_run_timestamp_seconds` heartbeat gauge — via a dedicated `CollectorRegistry` (avoids colliding with node_exporter's own `python_*`/`process_*` metric names). Because the file is rewritten unconditionally each run, a failed device's metrics go absent in Prometheus rather than showing frozen stale values. Prometheus' node-exporter scrapes that directory (bound to `127.0.0.1:9100`); Prometheus itself (bound to `127.0.0.1:9090`) remote-writes to InfluxDB; Grafana visualizes via the InfluxDB datasource directly.

Grafana's role source is vendored from [cloudalchemy/ansible-grafana](https://github.com/cloudalchemy/ansible-grafana) (MIT-licensed, see README).

### Tags

Meaningful `--tags`/`--skip-tags` values (grep a role's tasks for the full set): `hostname_setup`, `cron_setup`, `service_setup`, `install_python3`, `sensor_collector_setup`, `prometheus_install`, `prometheus_configure`, `prometheus_run`, `grafana_install`, `grafana_run`, `influxdb_install`, `influxdb_configure`, `influxdb_run`.

### Key variables

Role defaults live in each role's `defaults/main.yml` (see README's Role Variables table for the full list, e.g. `grafana_version`, `influxdb_version`, `influxdb_hostname`, `influxdb_database_name`, `sensor_collector_home`, `prometheus_version`, `prometheus_hostname`). Override at playbook or inventory level rather than editing role defaults directly.

`roles/sensor_collector/files/DeviceList.csv` is the device inventory that seeds the target host on first bootstrap (see the `force: false` note below) — the `MacAddress`/`Offset_Temp`/`Offset_Humid` columns are unused leftovers from the retired Bluetooth/Inkbird schema; only `API_URL`/`Token`/`Secret` matter for Nature Remo/SwitchBot.

## Notes

- `ansible.cfg` sets `host_key_checking = False` and `ask_pass = True` — expect an SSH password prompt on each run unless key-based auth without `ask_pass` is set up locally.
- Several role task files contain commented-out blocks for adding upstream apt repositories (Grafana/InfluxDB GPG keys + repos); the roles currently install from the Ubuntu/Raspberry Pi OS repository instead. Check whether these need re-enabling before assuming package availability/versions on a fresh OS image.
- `roles/sensor_collector/files/DeviceList.csv` in the repo is placeholder-only (real device rows carry live API tokens/secrets in production). The `copy` task uses `force: false` — it seeds the file on first bootstrap but will never overwrite an existing file on a target, so editing the repo's placeholder never clobbers a live deployment.
- `ansible-lint` is referenced in tooling expectations but is **not** in `requirements.txt` / not installed; use `ansible-playbook iot.yml --syntax-check` for a lightweight sanity check instead.
- Raw `ssh`/`scp` to the target often fails in agentic/non-interactive shells here (`ssh_askpass: exec(/usr/bin/ssh-askpass): No such file or directory`, since `ask_pass = True` forces a password prompt with no GUI askpass helper available). `ansible-playbook`'s own password prompt works fine when a human runs it interactively. To pull files off the target, write a throwaway playbook using `fetch`/`command` (+ `delegate_to: localhost` to save output locally) instead of shelling out to raw `ssh`.
- `.venv/` in this repo can go stale if the repo directory is moved (the venv's shebang/paths are absolute). Rebuild with `rm -rf .venv && uv venv .venv && uv pip install -r requirements.txt --python .venv/bin/python` (plain `uv venv` doesn't bootstrap `pip`, so `uv pip install --python` is required, not `.venv/bin/pip install`).
- Because `iot.yml` sets `become: true` at the play level, `{{ ansible_env.HOME }}` (from gathered facts) resolves to the *elevated* user's home even inside a task that locally sets `become: false`. Use `/home/{{ ansible_user }}` for the SSH login user's home directory in such tasks.
- `prometheus.yml` is fully owned by a single `template:` task in the `prometheus` role (the `influxdb` role used to append `remote_write` afterward via `blockinfile`, which made the template task always show `changed` under `--check`; that's been folded into the template directly for full idempotency).
