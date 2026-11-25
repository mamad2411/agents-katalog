---
name: routeros-containers
description: Containers and apps on MikroTik RouterOS 7. Covers enabling container mode (device mode with physical confirmation), requirements and security risks, veth interfaces with NAT, bridge or LAN DHCP networking and isolated networks, environment lists, mounts, registries and image sources (remote image, tar import from Docker or Podman, build for arm, arm64 or amd64), resource limits, swap, restart policy, saving and committing images, and the /app catalog with its setup wizard, custom apps and app stores, plus guides for Pi-hole, Home Assistant, Mosquitto, Postgres, HAProxy, FreeRADIUS, Matrix and ThingsBoard. Use when running a Docker-style service on a router, building an isolated container network, or deploying a catalog app.
---

# RouterOS containers and apps

Containers run Linux (OCI/Docker) images on arm, arm64 and x86 RouterOS devices with the `container` package. Images come from Docker Hub, GHCR, Quay or
a tar archive. **Security first:** container mode is disabled by default and needs physical access to enable. Once on, containers can be added and
started remotely, and a malicious or exploited image can leave a backdoor even after the container is removed (a compromised bootloader may survive
Netinstall). The router is only as secure as what runs in it: use images you trust, keep the router locked down, and say so to the user before enabling it.

## Prerequisites

- Package `container` installed (`routeros-install-upgrade`), architecture arm, arm64 or x86. hEX Refresh (EN7562CT CPU) can run only `arm32v5` images.
- `/system/device-mode/update container=yes`, then confirm by pressing the reset or mode button (or cold power cycle) within the time limit
  (`routeros-system-utilities`). Without confirmation nothing changes.
- External storage with at least 100 MB/s sequential and 10 K random IOPS is recommended; put `root-dir`, `tmpdir` and volumes on it, not on internal flash
  (`routeros-storage`; `/disk/test` measures speed). 16 MB SPI flash boards should use prebuilt images from USB.
- A DNS server in `/ip/dns` or the container's `dns` setting; **a container without any DNS does not start**.

## Network and first container (Pi-hole pattern)

```ros
/interface/veth/add name=veth1 address=172.17.0.2/24 gateway=172.17.0.1
/interface/bridge/add name=containers
/ip/address/add address=172.17.0.1/24 interface=containers
/interface/bridge/port/add bridge=containers interface=veth1
/ip/firewall/nat/add chain=srcnat action=masquerade src-address=172.17.0.0/24
/container/envs/add list=ENV_PIHOLE key=TZ value="Europe/Riga"
/container/mounts/add list=MOUNT_PIHOLE src=disk1/volumes/pihole/pihole dst=/etc/pihole
/container/config/set registry-url=https://registry-1.docker.io tmpdir=disk1/tmp
/container/add remote-image=pihole/pihole interface=veth1 root-dir=disk1/images/pihole mountlists=MOUNT_PIHOLE envlist=ENV_PIHOLE name=pihole logging=yes start-on-boot=yes
/container/print                         # wait until status=stopped (download and extract finished)
/container/start pihole
/ip/firewall/nat/add action=dst-nat chain=dstnat dst-address=192.168.88.1 dst-port=80 protocol=tcp to-addresses=172.17.0.2 to-ports=80
```

- Adding a container starts the download and extraction only; start it yourself the first time. `/container/shell` opens a shell, `run` starts and enters,
  `stop`, `restart`, `kill`, `update` and `repull` manage the image.
- One veth can serve many containers (bridge-style networking, containers talk freely; publish ports only with dst-nat). Use one veth and bridge per group
  for **isolated** networks (`172.17.0.0/24` and `172.18.0.0/24` with separate masquerade rules).
- Put a container on the LAN instead: `/interface/veth/add name=veth2 dhcp=yes` and make it a port of the LAN bridge; static leases must use the veth `mac-address`, not
  `container-mac-address`. Static IPv4 and IPv6 use `address` (comma separated), `gateway`, `gateway6`.
- `registry-url` defaults to `https://lscr.io/`; `username` and `password` in `/container/config` authenticate to private registries. Per-container
  `check-certificate=no` skips TLS verification of the registry (avoid).
- Settings per container: `cmd`, `entrypoint`, `workdir`, `user`, `hostname`, `dns`, `hosts`, `devices`, `cpu-list`, `memory-high`, `memory-max`, `swap-max`, `tmpfs`, `shm-size`,
  `restart-policy` (`no`, `on-failure`, `always`), `restart-interval`, `restart-max-count`, `stop-signal`, `stop-time`, `stop-on-unhealthy`. Global memory limits live in `/container/config`.
  Swap needs the swap setup in `routeros-storage`.
- Volumes: `/container/mounts` lists reused via `mountlists`; a missing `src` directory is created on first use. Environment lists in `/container/envs` via `envlist`.
  Secrets in env values appear in exports.

## Getting images

| Source | How |
| --- | --- |
| Registry | `remote-image=<name>[:tag]` after setting `registry-url` and `tmpdir` (needs plenty of free RAM and disk) |
| Tar from a PC | `podman pull --arch=arm64 docker.io/<image>` (or `arm`, `amd64`), `podman save <image> > image.tar`, upload, then `/container/add file=disk1/image.tar interface=veth1 root-dir=disk1/image` |
| Own build | `podman build --platform linux/arm64 --tag <name> -f Dockerfile`, then `podman save` as above (Docker needs buildx and binfmt for foreign architectures) |
| Backup of a modified container | `/container/save 0 file=out.tar` keeps root-dir content and RouterOS settings; add `commit` to produce a normal OCI image loadable in Podman or Docker |

Choose the image architecture to match `/system/resource/print` `architecture-name`.

## Apps (catalog)

`/app` deploys pre-built, pre-wired applications (one or more containers plus veth, bridge port, NAT and port forwarding) from a MikroTik-maintained catalog. It needs the container
package and container mode, arm64 or x86 (not EN7562CT), and external storage.

```ros
/app/setup                              # wizard: storage disk, LAN bridge, router IP
/app/print
/app/enable pihole                     # downloads, configures and starts; status shows progress (also disable, restart, update, remove)
/app/cleanup pihole                     # stop and DELETE app data and image
/app/settings/print                     # disk, lan-bridge, router-ip, media-path, download-path, registry-mirrors, auto-update, app-store-urls
```

- Per app: `network` (`internal` behind NAT, `lan`, `default`), `environment`, `extra-mounts`, `firewall-redirects`, `devices`, `auto-update`, `use-https`, `pvid`,
  `network-outgoing-access` (no creates a mangle drop), `yaml`. Read-only: `ui-url`, `ip-address`, `interface`, `memory-current`, `default-credential`.
- From 7.22 custom apps are defined with a compose YAML file: `/app/add network=lan` then `/app/edit app yaml` (paste, Ctrl+O), or
  `/app/add yaml=[/file/get alpine-iperf.yml contents]`, then enable it. `app-store-urls` can point to a custom store (a YAML array of apps). Treat third-party stores like third-party images.
- Catalog list with descriptions and suited hardware: `references/guides/containers/apps/available-apps.md`. Thread-enabled Home Assistant on hAP be3 Media is in the Claire guide.

## Where to look

| Need | Open |
| --- | --- |
| Properties, config, save/commit, Pi-hole walkthrough, image sources, bridge/isolated networking, resource limits | `references/guides/containers.md` |
| Veth (NAT, LAN with DHCP, static IPv4/IPv6, VLANs) | `references/guides/containers/veth.md` |
| Apps wizard, settings, custom apps, store | `references/guides/containers/apps.md`, `apps/available-apps.md` |
| Service guides | `references/guides/containers/user-guides/` (Mosquitto, Postgres, HAProxy, FreeRADIUS, Home Assistant, Matrix, ThingsBoard) |
| Properties | `references/cli/container.md` (and `container/`), `references/cli/app.md`, `references/cli/interface/veth.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-storage` (disks, swap), `routeros-system-utilities` (device mode), `routeros-firewall` (NAT, container subnet rules),
`routeros-iot` (Mosquitto broker for MQTT), `routeros-dns` (container DNS), `routeros-users-aaa` (FreeRADIUS container), `routeros-install-upgrade`.
