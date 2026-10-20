---
name: on-prem-infrastructure-patterns
description: >
  Guides designing and operating on-premises, private-cloud, and hybrid
  infrastructure — VMware vSphere as the virtualization baseline,
  automated bare-metal provisioning (PXE/MAAS/Redfish), inventory-as-code
  (IPAM/DCIM), and hybrid connectivity back to public cloud (VPN, dedicated
  interconnect equivalents of Direct Connect/ExpressRoute/FastConnect).
  Use when a user asks to "design a private cloud", "provision bare-metal
  servers", "set up a vSphere cluster", "connect our data center to AWS/
  Azure/GCP/OCI", "decide whether to migrate to the cloud or stay
  on-prem", "plan hybrid connectivity", or "build a data center network
  for a new site".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# On-Prem Infrastructure Patterns

## Purpose

Not every workload belongs in the public cloud, and not every
organization can (or should) migrate everything at once — data residency
law, sub-millisecond latency requirements, existing capital investment in
depreciating hardware, or genuinely predictable steady-state capacity all
make on-premises or private-cloud infrastructure the correct choice for at
least part of most large estates. But on-prem infrastructure without the
same engineering discipline applied to cloud — inventory as code, IaC-
driven provisioning, redundant hybrid connectivity, deliberate workload
placement — degenerates into hand-built snowflake servers, spreadsheet
inventories that drift from physical reality, and a single point of
failure between the data center and everything the business has since
moved to the cloud. This skill covers the common virtualization baseline
(VMware vSphere), automated bare-metal provisioning, inventory-as-code
discipline, and the hybrid connectivity patterns that let on-prem and
cloud infrastructure operate as one coherent estate rather than two
disconnected islands.

## When to use

- Designing or expanding a private-cloud/data-center footprint: a new
  vSphere cluster, a bare-metal fleet, or a colocation build-out.
- Automating bare-metal server provisioning (OS install, firmware
  baseline, network configuration) instead of manual per-server setup.
- Planning or troubleshooting hybrid connectivity between an on-premises
  data center and a public cloud (VPN, dedicated circuit, DNS/IP
  integration).
- Deciding whether a specific workload should stay on-premises, burst to
  cloud, or migrate fully — using a documented framework rather than
  defaulting to "cloud, always."
- Building or auditing an infrastructure-as-code pipeline for on-prem
  resources (Terraform against vSphere/bare-metal providers, Ansible
  configuration baselines).
- Establishing or fixing an IPAM/DCIM inventory that has drifted from
  what's physically racked and cabled.
- Planning capacity ahead of a hardware refresh cycle, given that
  procurement lead times (weeks to months) are nothing like cloud
  elasticity.

## Prerequisites & environment

- Physical facility prerequisites already in place: rack space, power
  (with A/B redundant feeds for anything production-critical), cooling
  capacity, and physical access control — infrastructure-as-code cannot
  fix a data center that's out of power or cooling headroom.
- An **out-of-band management network** physically or logically separate
  from the production network, reachable to every server's BMC (iLO,
  iDRAC, IPMI, or Redfish-capable equivalent) — this is a prerequisite for
  automated provisioning and remote recovery, not an optional extra.
- VMware vSphere ≥ 8.0 (ESXi + vCenter Server) if using VMware as the
  virtualization baseline, or the equivalent for an alternative platform
  (Nutanix AHV, Proxmox VE, Microsoft Hyper-V) — pick one platform as the
  default and treat others as deliberate exceptions, not a mixed fleet by
  accident.
- Terraform ≥ 1.5 with the `vsphere` provider (or the relevant
  bare-metal/private-cloud provider) and Ansible ≥ 2.15 for OS/config
  management if managing on-prem infrastructure as code — strongly
  recommended over console/CLI click-ops past a handful of hosts.
- A single source of truth for IP address space and physical inventory
  before provisioning anything — NetBox or an equivalent DCIM/IPAM tool,
  version-controlled or API-driven, not a spreadsheet nobody updates after
  the first month.
- For hybrid connectivity: an account/subscription/project already
  provisioned in the target public cloud(s), with the relevant
  landing-zone guardrails in place (see the `*-landing-zone-setup`
  skills) and a central IP address plan that includes the on-prem CIDR
  ranges, not just cloud VPC/VNet ranges.
- Decide the hybrid connectivity budget and lead time up front — a
  dedicated circuit (AWS Direct Connect, Azure ExpressRoute, GCP Cloud
  Interconnect, OCI FastConnect) typically takes weeks to provision,
  unlike a VPN which can be stood up same-day.

## Step-by-step guidance

1. **Establish inventory-as-code before touching hardware.** Model racks,
   power circuits, IP subnets, VLANs, and device records in a DCIM/IPAM
   system (NetBox is the common open-source choice) so physical reality
   and its digital record never diverge. A minimal NetBox-style device
   record as data:
   ```yaml
   device:
     name: esx-host-042
     site: dc1-rack-14
     device_role: virtualization-host
     device_type: dell-poweredge-r760
     status: active
     primary_ip4: 10.20.4.42/24
     oob_ip: 10.20.250.42/24   # separate management VLAN
   ```
   Treat this record as the source of truth that IaC pipelines read from
   — not a description written after the fact.

2. **Choose a virtualization platform baseline and standardize on it.**
   VMware vSphere (ESXi hosts clustered under vCenter, with vSphere HA for
   failover and DRS for load balancing) is the common enterprise default;
   Nutanix AHV, Proxmox VE, or Hyper-V are valid alternatives when
   licensing cost, hyperconverged-infrastructure preference, or existing
   Microsoft investment drives the decision. Whichever is chosen, manage
   cluster configuration as code:
   ```hcl
   resource "vsphere_compute_cluster" "prod" {
     name            = "cluster-prod-dc1"
     datacenter_id   = data.vsphere_datacenter.dc1.id
     host_managed    = true

     drs_enabled          = true
     drs_automation_level = "fullyAutomated"
     ha_enabled           = true
     ha_admission_control_policy = "resourcePercentage"
   }
   ```

3. **Automate bare-metal provisioning** rather than hand-installing OS
   images per server. Two common patterns:
   - **PXE + kickstart/preseed**: a DHCP/TFTP-served PXE boot chain that
     hands each new host an automated OS install (Kickstart for RHEL/
     Rocky, preseed/cloud-init for Debian/Ubuntu), driven by the
     inventory record's MAC address.
   - **MAAS (Metal-as-a-Service) or Ironic (OpenStack bare-metal)**: a
     dedicated bare-metal provisioning service that commissions, images,
     and hands off servers as a managed pool — closer to "cloud-like"
     self-service for physical hardware.
   Either way, drive the initial power-on and OS install through the
   BMC's **Redfish API** (the vendor-neutral successor to proprietary
   IPMI extensions) so provisioning is scriptable end to end:
   ```bash
   curl -k -u "<BMC_USER>:<BMC_PASSWORD>" \
     -X POST -H "Content-Type: application/json" \
     -d '{"ResetType": "On"}' \
     https://<BMC_IP>/redfish/v1/Systems/1/Actions/ComputerSystem.Reset
   ```

4. **Configure the OS and baseline agents with Ansible immediately after
   provisioning** — firmware/BIOS version check, NTP, monitoring agent,
   security baseline (CIS benchmark), and hypervisor join-to-cluster —
   so every host reaches a known-good state before carrying workloads:
   ```yaml
   - hosts: new_esx_hosts
     tasks:
       - name: Verify BIOS/firmware baseline
         assert:
           that: "ansible_facts['bios_version'] == expected_bios_version"
       - name: Join host to vSphere cluster
         community.vmware.vmware_host:
           cluster: cluster-prod-dc1
           esxi_hostname: "{{ inventory_hostname }}"
           state: present
   ```

5. **Design the network as core/distribution/access or spine-leaf**,
   matching scale: a small single-site data center is well served by a
   traditional three-tier core/distribution/access design; a larger
   private cloud or multiple co-located clusters benefit from a
   non-blocking spine-leaf fabric. Segment with VLANs at minimum:
   production workload, storage/vMotion, out-of-band management, and a
   DMZ/edge segment — never share the management VLAN with production
   workload traffic.

6. **Reserve IP address space centrally, including on-prem ranges, before
   connecting to any cloud.** The same IPAM discipline covered in
   `multi-cloud-networking-patterns` applies here in reverse: on-prem
   CIDR blocks must be reserved and known before a cloud VPC/VNet/VCN is
   peered to them, or the connection will fail on first overlap.

7. **Connect to public cloud with a redundant hybrid path**, following
   the same "dedicated connection with VPN failover" pattern used for
   cross-cloud connectivity:
   - AWS: Direct Connect + Site-to-Site VPN failover.
   - Azure: ExpressRoute + VPN Gateway failover.
   - GCP: Cloud Interconnect (Dedicated or Partner) + Cloud VPN failover.
   - OCI: FastConnect + Site-to-Site VPN failover.
   A minimal vendor-neutral IPsec VPN failover tunnel (strongSwan-style
   config, illustrative):
   ```
   conn onprem-to-cloud
     left=<ON_PREM_GATEWAY_PUBLIC_IP>
     leftsubnet=10.20.0.0/16
     right=<CLOUD_VPN_GATEWAY_PUBLIC_IP>
     rightsubnet=10.50.0.0/16
     ike=aes256-sha256-modp2048
     esp=aes256-sha256-modp2048
     keyexchange=ikev2
     auto=start
   ```
   Confirm both sides agree on IKE/IPsec parameters explicitly rather than
   relying on auto-negotiation defaults, which differ by vendor.

8. **Decide workload placement with a documented framework, not
   instinct.** For each workload, score against: data residency/
   sovereignty requirements, latency tolerance (sub-10ms plant-floor
   control loops behave very differently from a nightly batch job),
   existing capex/depreciation runway on already-owned hardware, data
   gravity (cost/time to move large existing datasets), and whether the
   workload's demand is genuinely elastic/bursty (cloud's core advantage)
   or flat and predictable (where owned steady-state capacity is often
   cheaper). Document the decision and revisit it — it is not permanent.

9. **Capacity-plan with real lead-time headroom.** Unlike cloud
   autoscaling, a bare-metal or vSphere cluster capacity shortfall means
   weeks-to-months of hardware procurement, not minutes. Track
   utilization trends and trigger procurement well before a cluster
   reaches the threshold where DRS/HA admission control starts rejecting
   placements.

10. **Validate hybrid failover and provisioning automation before relying
    on them.** Run a controlled VPN-failover test (drop the primary
    dedicated circuit deliberately, confirm traffic reroutes), and
    provision one canary bare-metal host end to end through the
    PXE/MAAS + Ansible pipeline to confirm it reaches the expected
    baseline before trusting the pipeline for a full fleet rollout.

## Best practices

- **Manage on-prem infrastructure as code** (Terraform for
  vSphere/bare-metal provisioning, Ansible for OS/config baselines) with
  the same PR review rigor as cloud IaC — a hand-built ESXi host is a
  future outage nobody can explain.
- **Keep the out-of-band management network physically or logically
  isolated** from production traffic, with no default BMC credentials
  left in place and no route to the public internet.
- **Standardize on one virtualization platform** as the default and treat
  every additional platform as a deliberate, documented exception —
  mixed fleets multiply operational tooling and staffing cost.
- **Version and stage firmware/BIOS baselines** before fleet-wide
  rollout; firmware drift across a bare-metal fleet is one of the most
  common causes of "it works on some hosts but not others" incidents.
- **Design hybrid connectivity redundant from day one** — a dedicated
  circuit with VPN failover, not a single link, for anything
  production-critical crossing the data-center boundary.
- **Keep a single, continuously reconciled inventory** (DCIM/IPAM) —
  automation that reads a stale inventory record will provision against
  the wrong rack, subnet, or already-decommissioned host.
- **Re-evaluate workload placement periodically**, not just at initial
  build time — a workload's latency/data-residency/elasticity profile can
  change as the business does, and "we built it here five years ago" is
  not a durable placement justification.
- **Plan power, cooling, and rack capacity alongside compute capacity** —
  a cluster can be compute/memory-healthy and still be unable to grow
  because the rack is out of power headroom.

## Common pitfalls

- **Symptom:** A new vSphere host or bare-metal server takes days to
  bring into service even though procurement delivered it on schedule.
  **Fix:** Provisioning was still a manual, per-host process (rack it,
  console in, click through an OS installer). Automate the PXE/MAAS +
  Ansible pipeline described above so bringing a racked, cabled, and
  BMC-reachable host into service is a single pipeline run, not a
  multi-day manual checklist.

- **Symptom:** Connecting the data center to a new cloud VPC/VNet/VCN
  fails immediately with an overlapping-CIDR error, or routes silently
  reach the wrong subnet.
  **Fix:** On-prem IP ranges were never centrally reserved alongside
  cloud ranges — each was planned in isolation. Establish one IPAM source
  of truth covering on-prem *and* every cloud account/subscription/
  project's address space before any hybrid connection is provisioned;
  re-IPing a live data-center subnet after the fact is far more
  disruptive than re-IPing a cloud VPC.

- **Symptom:** A subset of hosts in an otherwise-identical cluster behave
  differently under load, or intermittently fail in ways that don't
  reproduce on other hosts.
  **Fix:** Firmware/BIOS versions drifted across the fleet because
  updates were applied ad hoc, host by host, whenever someone happened to
  notice an available update. Track a single firmware/BIOS baseline
  version per hardware model, stage updates through a canary subset, and
  enforce the baseline via the same Ansible assertion shown in step 4.

- **Symptom:** An external audit or incident response finds the BMC/iLO/
  iDRAC management interfaces reachable from the general corporate
  network, several still on default vendor credentials.
  **Fix:** The out-of-band management network was never actually
  isolated — it shared a VLAN (or worse, a flat network) with production
  or corporate traffic. Move BMC interfaces onto a dedicated management
  VLAN with no route to the internet, rotate all default credentials
  immediately, and require the management network to sit behind its own
  access-controlled jump host.

- **Symptom:** A "cloud burst" plan for seasonal capacity turns out to
  cost far more, or perform far worse, than expected once actually
  exercised.
  **Fix:** The workload-placement decision assumed cloud capacity would
  behave like an on-prem extension with negligible cost/latency
  difference — it didn't account for egress cost on data moved back and
  forth, or the added latency of round-tripping to a dependency that
  stayed on-prem. Re-run the placement framework from step 8 honestly for
  the bursty workload specifically, and if cloud bursting stays the
  right pattern, keep the dependent data/services it needs already
  replicated to the cloud side rather than fetched live from on-prem.

## Worked example

**Scenario:** A manufacturing company runs a single on-prem data center
on VMware vSphere. Plant-floor OT systems must stay on-premises for
latency and regulatory reasons, but the company's e-commerce storefront
needs seasonal burst capacity for a holiday sales spike, and inventory
records have drifted badly from what's actually racked.

1. Stand up NetBox and reconcile it against a physical audit of the data
   center — every rack, host, IP subnet, and VLAN gets a real device
   record before any new automation is trusted to act on it.
2. Confirm the vSphere cluster's DRS/HA configuration is managed via the
   Terraform `vsphere` provider going forward, not console click-ops, and
   bring the existing cluster under Terraform management with an
   `import` pass.
3. Apply the workload-placement framework: plant-floor OT systems score
   as "stay on-prem" (sub-10ms latency requirement, regulatory data
   residency), while the storefront's seasonal spike scores as "cloud
   burst" (genuinely elastic, bursty demand with no data-residency
   constraint).
4. Order a dedicated interconnect (e.g. AWS Direct Connect) to the
   storefront's cloud landing zone, with a Site-to-Site VPN configured
   immediately as failover while the physical circuit provisions over the
   following weeks.
5. Reserve on-prem CIDR ranges in the same IPAM system already tracking
   the cloud VPC ranges, confirming no overlap before the hybrid
   connection goes live.
6. Automate provisioning of a small pool of bare-metal hosts reserved for
   OT workloads using PXE + kickstart driven by the NetBox inventory, with
   firmware baseline enforcement via Ansible.
7. Run a controlled failover test: fail the dedicated circuit
   deliberately during a maintenance window, confirm the VPN path takes
   over automatically, then fail back.
8. Result: OT systems stay on-prem with a verified inventory and
   automated bare-metal pipeline; the storefront bursts to cloud through
   a redundant hybrid connection with pre-reserved, non-overlapping IP
   space — and the placement decision is documented for the next review
   cycle rather than assumed permanent.

## Cross-references

- [multi-cloud-networking-patterns](../multi-cloud-networking-patterns/SKILL.md)
- [disaster-recovery-and-backup-strategy](../disaster-recovery-and-backup-strategy/SKILL.md)
