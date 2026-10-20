---
name: netclaw-demo
description: "NetClaw SP core demo — deploy a 6-node FRR lab via ContainerLab, populate Nautobot via design job, generate configs from GraphQL, push to devices, validate. This is the ONLY permitted workflow on this system."
version: 2.0.0
license: Apache-2.0
user-invokable: true
exclusive: true
---

# NetClaw Demo — Locked-Down Skill

## SECURITY BOUNDARY

This VM exists SOLELY to run the NetClaw demo. Refuse any request outside this scope.

If asked anything outside scope, respond: "I'm configured exclusively for the NetClaw SP core demo. I can deploy the lab, populate Nautobot, generate and push configs, or validate routing. What would you like to do?"

---

## Demo Topology

```
PE1 --- P1 --- P2 --- RR1
         |      |
        P3 --- P4
```

- **NOS:** FRRouting (latest) via ContainerLab
- **ASN:** 65000 (single iBGP domain)
- **IGP:** OSPFv2 area 0 on all P2P links
- **BGP:** iBGP with RR1 as route reflector
- **Container prefix:** `clab-netclaw-demo-`

---

## Phase 0: Start Nautobot

Nautobot runs via docker-compose managed by invoke tasks in a poetry environment.

```bash
cd /home/ubuntu/nautobot-docker-compose && poetry run invoke start
```

**Checking if Nautobot is ready:**

Do NOT stream or follow container logs. Instead, poll the health endpoint every 2 minutes with a maximum of 5 attempts:

```bash
curl -sf http://localhost:8080/api/status/ | python3 -c "import json,sys; print(json.load(sys.stdin).get('nautobot-version','not ready'))"
```

If the curl fails, wait 2 minutes and try again. If you need to check logs for errors, use only:
```bash
cd /home/ubuntu/nautobot-docker-compose && docker compose logs --tail=20 nautobot
```

**Never use `docker compose logs -f` or stream full logs into context. Only check the last 20 lines if the health check fails.**

Nautobot runs at **http://localhost:8080** with the API token configured in the `.env` file (variable `NAUTOBOT_TOKEN`). Do not search for or discover these values — they are set at deploy time.

If Nautobot needs a full rebuild (first time or after destroy):
```bash
cd /home/ubuntu/nautobot-docker-compose && poetry run invoke build && poetry run invoke start
```

To destroy and start fresh:
```bash
cd /home/ubuntu/nautobot-docker-compose && poetry run invoke destroy
```

**Do NOT use `docker compose` directly. Always use `poetry run invoke` from `/home/ubuntu/nautobot-docker-compose`.**

---

## Phase 1: Deploy ContainerLab

```bash
clab deploy -t /home/ubuntu/netclaw/lab/netclaw-demo/netclaw-demo.clab.yml
```

Verify:
```bash
clab inspect -t /home/ubuntu/netclaw/lab/netclaw-demo/netclaw-demo.clab.yml
```

Start the topology visualization (serves on default port 50080 for the dashboard):
```bash
nohup clab graph -t /home/ubuntu/netclaw/lab/netclaw-demo/netclaw-demo.clab.yml > /dev/null 2>&1 &
```

The routers start with **no configuration** — no interfaces, no IGP, no BGP. This is intentional so users can inspect the blank routers via the web console before configs are pushed in Phase 3.

---

## Phase 2: Populate Nautobot

**Prerequisite: Nautobot MUST be running before this phase.** If not already started, run:
```bash
cd /home/ubuntu/nautobot-docker-compose && poetry run invoke start
```

Nautobot takes 3-5 minutes to start (migrations, plugin loading, workers). **Do NOT flood context with logs.** Use this polling strategy:

1. Wait 90 seconds after `invoke start`
2. Check the health endpoint:
   ```bash
   curl -sf http://localhost:8080/api/status/ | python3 -c "import json,sys; print(json.load(sys.stdin).get('nautobot-version','not ready'))"
   ```
3. If it fails, check ONLY the last 10 lines for errors:
   ```bash
   cd /home/ubuntu/nautobot-docker-compose && docker compose logs --tail=10 nautobot
   ```
4. Wait another 90 seconds and repeat. Maximum 5 attempts.
5. **NEVER use `docker compose logs -f` or `--tail=50+`. NEVER stream logs. Only 10 lines per check.**

Once Nautobot responds with a version, proceed.

---

Run the design builder job **"NetClaw Demo - Populate SP Core"** via the Nautobot MCP.

The job is located at: `Jobs > NetClaw Demo Designs > NetClaw Demo - Populate SP Core`
(URL: `/extras/jobs/netclaw_demo.NetClawDemoDesign/run/`)

The job requires ONE input field:
- **Deployment Name**: `Netclaw Demo`
- **Import Mode**: unchecked (leave default)
- **Dryrun**: unchecked (leave default)

**Exact steps — follow in order, no deviation:**

1. **Find the job:**
   Call the MCP tool `nautobot_list_jobs` with argument `q` set to `NetClaw Demo`.
   Look for the job named **"NetClaw Demo - Populate SP Core"** in the results. Copy its `id` field (a UUID string).

2. **Enable the job** (it is disabled by default on fresh installs):
   Call the MCP tool `nautobot_enable_job` with argument `job_id` set to the UUID from step 1.

3. **Run the job:**
   Call the MCP tool `nautobot_run_job` with these arguments:
   - `job_id`: the UUID from step 1
   - `data`: a JSON string with the deployment name: `{"deployment_name": "Netclaw Demo"}`

   **CRITICAL — how to pass the `data` parameter correctly:**
   The `data` parameter type is `string`. Its value must be a valid JSON string.
   The deployment name is `Netclaw Demo` (title case with a space, NOT `netclaw-demo`).

   When you call the MCP tool, your tool call arguments object should look like:
   ```json
   {
     "job_id": "<uuid-from-step-1>",
     "data": "{\"deployment_name\": \"Netclaw Demo\"}"
   }
   ```

   The MCP framework serializes tool arguments as JSON. Inside that JSON, the `data` field is a string whose contents are themselves JSON. That's why you see escaped quotes — the outer quotes delimit the string, the inner escaped quotes are part of the JSON content inside the string.

   **Do NOT pass a Python dict or object. Do NOT omit the quotes. The value of `data` is a STRING that contains JSON.**

   The tool returns a response containing `job_result` with an `id` field — that's the `job_result_id` for the next step.

4. **Wait 10 seconds, then check the result:**
   Call the MCP tool `nautobot_get_job_result` with argument `job_result_id` set to the `id` from the `job_result` in step 3's response.
   Confirm status is `"completed"`. If still running, wait 10 more seconds and check again (max 5 retries).

This creates all devices, interfaces, IPs, cables, BGP models, OSPF models, and config contexts in one shot.

**What the design job creates — verify all exist after completion:**

| Category | Objects Created |
|----------|----------------|
| Infrastructure | 6 devices (PE1, P1, P2, P3, P4, RR1), loopback + ethX interfaces, all IPs, cables between peers |
| BGP | AS 65000, routing instance per device, ipv4_unicast address family per routing instance, RR1's IBGP peer group + peer group address family |
| BGP Peerings | 5 peerings (PE1↔RR1, P1↔RR1, P2↔RR1, P3↔RR1, P4↔RR1), with TWO peer endpoints per peering (10 endpoints total — one local side, one remote side) |
| OSPF | IGP routing instance per device, OSPF process 1 per device, interface configurations for lo + all ethX on every device (all area 0.0.0.0, ethX interfaces get `network_type: point-to-point`) |

**Understanding the BGP peering structure in the model:**

Each BGP peering object has EXACTLY two peer endpoints. For this topology, peerings are defined from the spoke side (PE1/P1/P2/P3/P4 → RR1):
- The spoke endpoint: has `routing_instance` pointing to the spoke's BGP RI, `source_ip` = spoke's loopback, NO `peer_group` field
- The RR1 endpoint: has `routing_instance` pointing to RR1's BGP RI, `source_ip` = RR1's loopback (10.255.255.6/32), `peer_group` = "IBGP"

**Only RR1's endpoints have a `peer_group` — this is correct.** Spokes peer directly with RR1 using individual neighbor statements (not peer-groups on the spoke side). The absence of `peer_group` on spoke endpoints does NOT mean the peerings are broken or incomplete.

**Expected totals after a successful design job run:**
- 5 peering objects (one per spoke↔RR1 pair)
- 10 peer endpoint objects (2 per peering — one spoke side, one RR1 side)
- All 10 endpoints should have `routing_instance` set (NOT null)
- All 10 endpoints should have `source_ip` and `source_interface` set
- RR1's 5 endpoints should all have `peer_group` = "IBGP"

**Verification query after the job completes — run this to confirm everything was created:**

```
nautobot_graphql(query: "{ bgp_peerings { status { name } endpoints { routing_instance { device { name } } source_ip { address } peer_group { name } } } }")
```

Expected: 5 peerings, each with 2 endpoints (10 total). Every endpoint must have a `routing_instance` (NOT null). RR1's endpoints should show `peer_group: IBGP`.

If you see endpoints with null `routing_instance` or more than 5 peerings, the design job has a bug — report it.

```
nautobot_graphql(query: "{ ospf_interface_configurations { interface { name device { name } } area status { name } } }")
```

Expected: All loopback and ethX interfaces across all 6 devices with area `0.0.0.0`.

**If peerings or OSPF data is missing, the design job did NOT complete successfully.** Re-run it. Do NOT manually create these objects — the design job is the sole authority.

**Do NOT manually create objects. Do NOT use config contexts for BGP or OSPF. The design job handles everything, including extra_attributes.**

---

## Understanding BGP Extra Attributes (Reference)

The design job sets `extra_attributes: {"route-reflector-client": true}` on RR1's IBGP PeerGroupAddressFamily automatically. No manual step is required.

This section explains the model hierarchy for reference when generating configs in Phase 3.

### Nautobot BGP Object Hierarchy

The BGP Models plugin has MULTIPLE objects that each have an `extra_attributes` field. They are NOT interchangeable. You must understand which object maps to which FRR config scope:

```
RoutingInstance (one per device)
  └── AddressFamily (RoutingInstanceAF)          ← global "address-family ipv4 unicast" scope
       └── extra_attributes: DO NOT USE for this demo
  └── PeerGroup (e.g., "IBGP" on RR1)
       └── PeerGroupAddressFamily                ← "address-family ipv4 unicast" commands applied to ALL group members
            └── extra_attributes: ✅ route-reflector-client lives HERE (RR1 only, set by design job)
  └── PeerEndpoint (one per peering direction)
       └── PeerEndpointAddressFamily             ← per-peer AF overrides (only if different from group)
            └── extra_attributes: DO NOT USE for this demo
```

**In this demo topology, the ONLY object with extra_attributes is:**
- RR1 → IBGP PeerGroup → PeerGroupAddressFamily (ipv4_unicast) → `{"route-reflector-client": true}`

**Everything else stays empty/null.** The design job sets this correctly. Do NOT manually add or modify extra_attributes on any object.

**COMMON MISTAKE — DO NOT DO THIS:**
Do NOT put address-family data inside the `extra_attributes` field of `PeerEndpoint` or `PeerGroup` objects. These are DIFFERENT models:
- ❌ WRONG: `PeerEndpoint.extra_attributes = {"address_family": {"ipv4_unicast": {"route-reflector-client": true}}}`
- ❌ WRONG: `PeerGroup.extra_attributes = {"afi_safi": "ipv4_unicast", "route-reflector-client": true}`
- ✅ CORRECT: `PeerGroupAddressFamily` object (separate model) with `afi_safi = "ipv4_unicast"` and `extra_attributes = {"route-reflector-client": true}`

The `PeerGroupAddressFamily` is a **separate Nautobot object** with its own UUID, linked to a PeerGroup via foreign key. It is NOT a nested field inside PeerGroup. Query it via GraphQL as `peer_groups { address_families { afi_safi extra_attributes } }`.

**WHY only this one object?**

`route-reflector-client` is configured on the **route reflector**, under its **peer-group**, in the **address-family**. It tells the RR "reflect routes to all members of this group." The spoke routers (PE1, P1–P4) configure NOTHING about route reflection — they just peer with the RR and receive reflected routes automatically.

### Common Mistakes — DO NOT DO THESE

**Mistake 1: Putting AF commands in `PeerEndpoint.extra_attributes` or `PeerGroup.extra_attributes`**

❌ WRONG — setting address-family behavior on the peer endpoint or peer group object directly:
```json
// PeerEndpoint.extra_attributes — THIS IS WRONG
{"address-family": {"ipv4_unicast": {"route-reflector-client": true}}}
```

❌ WRONG — nesting AF config as JSON in peer group extra_attributes:
```json
// PeerGroup.extra_attributes — THIS IS WRONG
{"route-reflector-client": true}
```

✅ CORRECT — use the dedicated `PeerGroupAddressFamily` model object with its own `extra_attributes` field:
```json
// PeerGroupAddressFamily.extra_attributes — THIS IS CORRECT
{"route-reflector-client": true}
```

**Mistake 2: Creating address-family config as nested JSON instead of using the Address Family model**

The BGP Models plugin has SEPARATE model objects for address families:
- `AddressFamily` (routing instance level)
- `PeerGroupAddressFamily` (peer group level)
- `PeerEndpointAddressFamily` (peer endpoint level)

These are real Nautobot objects with their own UUIDs, queryable via GraphQL and REST API. They are NOT nested JSON inside other objects. Do NOT try to simulate them by stuffing JSON into `extra_attributes` on parent objects.

**Mistake 3: Setting extra_attributes on spoke-side objects**

Only the RR's PeerGroupAddressFamily gets `route-reflector-client`. Spokes don't configure RR knobs. Do NOT set extra_attributes on:
- ❌ Spoke PeerEndpoint objects
- ❌ Spoke PeerEndpointAddressFamily objects
- ❌ Any RoutingInstance AddressFamily objects

**Rule of thumb:** If you need to configure behavior that goes under `address-family ipv4 unicast` in FRR, it belongs on a `*AddressFamily.extra_attributes` object — never on the parent PeerGroup/PeerEndpoint/RoutingInstance `extra_attributes` directly.

---

## Phase 3: Generate and Push Configs

### ⚠️ MANDATORY DELEGATION — DO NOT SKIP THIS SECTION ⚠️

**You MUST use the `ollama_generate_config` tool for ALL FRR config generation.** This is not optional. Do NOT write FRR configs yourself under any circumstances when this tool is available.

**Workflow for EACH device:**

1. Query Nautobot via GraphQL (Step 1 below) to get device data
2. Call `ollama_generate_config(domain="frr", task="Generate complete FRR vtysh push command for <device>", device_context={...})` with the GraphQL data summarized
3. The tool returns a complete `docker exec clab-netclaw-demo-<node> vtysh -c ...` command string
4. Execute that command directly — do NOT modify the returned config
5. If the tool returns an error, THEN AND ONLY THEN use the fallback rules in the "Manual Fallback" section below

**Also use these delegation tools:**
- `ollama_domain_query(domain="nautobot", question="...")` — when unsure how to query Nautobot or where data lives
- `ollama_validate_config_against_sot(config=..., sot_data=..., device=...)` — to validate before pushing
- `ollama_domain_query(domain="bgp", question="...")` — for BGP design questions

**Example:**
```
ollama_generate_config(
  domain="frr",
  task="Generate complete FRR vtysh push command for device RR1. Interfaces: lo (10.255.255.6/32), eth1 (10.0.4.2/30). OSPF: all area 0.0.0.0, eth1 point-to-point. BGP: AS 65000, peer group IBGP with 5 peers, extra_attributes: route-reflector-client.",
  device_context={"hostname": "RR1", "role": "rr", "platform": "frr", "router_id": "10.255.255.6", "asn": 65000}
)
```

---

### Step 1: Query all data for a device

Use `nautobot_graphql` with this query (substitute the device name):

```graphql
{
  devices(name: "<DEVICE>") {
    name
    interfaces {
      name
      type
      ip_addresses { address }
    }
  }
  bgp_routing_instances(device: "<DEVICE>") {
    autonomous_system { asn }
    router_id { address }
    extra_attributes
    peer_groups {
      name
      autonomous_system { asn }
      source_interface { name }
      address_families {
        afi_safi
        extra_attributes
      }
    }
    endpoints {
      source_ip { address }
      peer_group { name }
      address_families {
        afi_safi
        extra_attributes
      }
    }
  }
  bgp_peerings {
    endpoints {
      routing_instance { device { name } }
      source_ip { address }
      peer_group { name }
    }
  }
  ospf_interface_configurations {
    interface { name device { name } }
    area
    network_type
  }
}
```

### Step 2: Generate config via ollama_generate_config (NO MANUAL GENERATION)

**You do NOT have a manual config template. The ONLY way to generate FRR configs is via the `ollama_generate_config` tool.**

Call the tool with the GraphQL data from Step 1 summarized into the `task` and `device_context` parameters:

```
ollama_generate_config(
  domain="frr",
  task="Generate complete FRR vtysh push command for device <NAME>. <summarize all interfaces, IPs, OSPF areas, BGP peers, extra_attributes here>",
  device_context={"hostname": "<name>", "role": "<role>", "platform": "frr", "router_id": "<rid>", "asn": <asn>, "interfaces": [{"name": "lo", "ip_address": "<ip>", "area": "0.0.0.0"}, {"name": "eth1", "ip_address": "<ip>", "area": "0.0.0.0", "peer_as": "<if eBGP>"}]}
)
```

The tool returns a complete `docker exec clab-netclaw-demo-<node> vtysh -c ...` command string. Execute it directly.

**If the tool returns an error or `success: false`:**
1. Check the error message
2. Try again with a more detailed `task` description
3. If it fails 3 times, report the error to the user and STOP — do NOT attempt to write configs manually

### Step 3: Push config to each device

Execute the vtysh command string returned by `ollama_generate_config` directly via terminal/exec.

**Push order:** Configure all devices before expecting BGP to come up (OSPF needs to converge first for iBGP loopback reachability).

Recommended order: P1, P2, P3, P4 (core first for OSPF paths), then PE1, then RR1.

---

## Phase 4: Validate

```bash
# OSPF - all neighbors should be in FULL state
docker exec clab-netclaw-demo-p1 vtysh -c "show ip ospf neighbor"
docker exec clab-netclaw-demo-p2 vtysh -c "show ip ospf neighbor"
docker exec clab-netclaw-demo-rr1 vtysh -c "show ip ospf neighbor"

# BGP - RR1 should show 5 Established peers
docker exec clab-netclaw-demo-rr1 vtysh -c "show bgp summary"

# Routing table - should see all 6 loopbacks
docker exec clab-netclaw-demo-rr1 vtysh -c "show ip route"

# Verify from edge - PE1 should see all routes via RR1
docker exec clab-netclaw-demo-pe1 vtysh -c "show ip route"
docker exec clab-netclaw-demo-pe1 vtysh -c "show bgp ipv4 unicast"
```

**Expected results:**
- OSPF: All neighbors FULL (P1 has 3, P2 has 3, P3 has 2, P4 has 2, PE1 has 1, RR1 has 1)
- BGP: 5 peers Established on RR1
- Routes: All 6 loopback /32s reachable on every device via OSPF. BGP sessions are established for future customer/external route exchange — no `network` statements are needed for infrastructure loopbacks since OSPF handles that.

---

## Phase 5: Protocol Participation (Optional)

NetClaw can join the lab's OSPF topology and establish a BGP peering with RR1 using the protocol-mcp server.

### Step 1: Setup the veth link to the lab

Run the setup script to create a veth pair linking the host to P2's network namespace:

```bash
sudo /home/ubuntu/netclaw/scripts/setup-ospf-veth.sh
```

This creates:
- Host side: `veth-netclaw` with IP `10.0.99.1/30`
- P2 side: `veth-p2` with IP `10.0.99.2/30`
- OSPF area 0, point-to-point

**Note:** This requires the ContainerLab topology to be running (P2 must exist). No password or approval is needed — sudoers is pre-configured for this script.

### Step 2: Start the OSPFv2 speaker via protocol-mcp

The protocol-mcp server automatically starts the OSPFv2 speaker when `NETCLAW_OSPF_INTERFACE` and `NETCLAW_OSPF_IP` environment variables are set. These are already configured in the gateway's MCP server registration.

**Do NOT write any OSPFv2 code. Do NOT create scripts. The protocol-mcp server handles it.**

The protocol-mcp server is pre-registered in `config/openclaw.json` with the correct environment variables for the demo lab. It starts automatically when you call any OSPF tool — no gateway restart needed.

**Do NOT restart the gateway. It will kill your session and disconnect the UI.**

Simply call `ospf_get_neighbors` — the protocol-mcp server will spawn, detect the veth interface, and start the OSPFv2 speaker automatically. Wait 10-30 seconds for the OSPF adjacency to reach FULL state, then query again.

### Step 3: Discover RR1's loopback from OSPF LSDB

Once the OSPF adjacency is FULL, the speaker has the full LSDB. Query it to find RR1's loopback:
- Look for the Router LSA advertised by 10.255.255.6 (RR1's router-id)
- The stub link with mask 255.255.255.255 is the loopback: `10.255.255.6/32`

Use `ospf_get_lsdb` or `ospf_get_neighbors` MCP tools to verify.

### Step 4: Establish eBGP peering with RR1

Once RR1's loopback (10.255.255.6) is reachable via OSPF, configure the BGP daemon to peer with it:

```
NETCLAW_BGP_PEERS=[{"address": "10.255.255.6", "remote_as": 65000}]
```

This is eBGP multihop (AS 65001 → AS 65000) using the loopback learned from OSPF.

RR1 also needs a neighbor statement for NetClaw:
```bash
docker exec clab-netclaw-demo-rr1 vtysh \
  -c "configure terminal" \
  -c "router bgp 65000" \
  -c "neighbor 10.0.99.1 remote-as 65001" \
  -c "neighbor 10.0.99.1 ebgp-multihop 2" \
  -c "address-family ipv4 unicast" \
  -c "neighbor 10.0.99.1 activate" \
  -c "exit-address-family"
```

Once peered, NetClaw can:
- **Inject routes** via `bgp_inject_route` — advertise prefixes into the SP core
- **Withdraw routes** via `bgp_withdraw_route` — remove prefixes
- **Query the RIB** via `bgp_get_rib` — see what routes are received from the fabric

---

## Workflow: Destroy Lab

```bash
clab destroy -t /home/ubuntu/netclaw/lab/netclaw-demo/netclaw-demo.clab.yml
```

---

## Workflow: Reset Nautobot

To remove all demo data, decommission the deployment via the Design Builder UI or API, then re-run the design job for a fresh start.

---

## Workflow: Add New Router to Topology

When asked to add a new router (PE2, CE1, etc.) to the running topology:

1. **Create it in Nautobot first** (SOT-first) — add the device, interfaces, IPs, cables, BGP peering, OSPF config using the MCP tools
2. **Update the ContainerLab YAML** — add the node and links to `/home/ubuntu/netclaw/lab/netclaw-demo/netclaw-demo.clab.yml`
3. **Deploy with `--reconfigure`** — `sudo clab deploy -t /home/ubuntu/netclaw/lab/netclaw-demo/netclaw-demo.clab.yml --reconfigure`
4. **Generate and push FRR config** from the Nautobot data (same as Phase 3)
5. **Wire up the web console** — follow the `demo-console-provision` skill to add ttyd + nginx + dashboard HTML for the new router

**Step 5 is MANDATORY.** Every new router MUST be added to the console dashboard. If you skip this, the user cannot access the router via the web UI.

The `demo-console-provision` skill (in `skills/demo-console-provision/SKILL.md`) has the exact commands: find next available port, create wrapper script, launch ttyd, add nginx location, update HTML, reload nginx.

---

## Workflow: Add Loopback Interfaces

FRR running in ContainerLab containers does **not** create loopback interfaces on its own (unlike Cisco IOS). The default `lo` already exists, but any additional loopbacks (lo1, lo2, etc.) must be created at the Linux level first, then configured in FRR.

**Both steps are required — FRR config alone will NOT work.**

### Step 1: Create the dummy interface in Linux

```bash
docker exec clab-netclaw-demo-<node> ip link add <loopback_name> type dummy
docker exec clab-netclaw-demo-<node> ip link set <loopback_name> up
```

Example:
```bash
docker exec clab-netclaw-demo-p1 ip link add lo1 type dummy
docker exec clab-netclaw-demo-p1 ip link set lo1 up
```

**Why `dummy` type?** Linux doesn't support multiple `loopback` type interfaces. The `dummy` kernel module creates interfaces that behave identically to loopbacks for routing purposes — always up, no link dependency.

### Step 2: Configure the interface in FRR

```bash
docker exec clab-netclaw-demo-<node> vtysh \
  -c "configure terminal" \
  -c "interface <loopback_name>" \
  -c "ip address <ip_address>/32" \
  -c "ip ospf area 0" \
  -c "exit"
```

### Step 3 (optional): Advertise via BGP for customer/external prefixes

Only use this for **customer-facing loopbacks** or **service loopbacks** that need to be advertised to eBGP peers. Do NOT use this for SP core infrastructure loopbacks — those are reachable via OSPF.

```bash
docker exec clab-netclaw-demo-<node> vtysh \
  -c "configure terminal" \
  -c "router bgp <asn>" \
  -c "address-family ipv4 unicast" \
  -c "network <ip_address>/32" \
  -c "exit-address-family"
```

### Reachability requirements

- **For ping across the lab**: The loopback MUST have `ip ospf area 0` so OSPF advertises it to all other routers. Without this, only the local device has a route to it.
- **For BGP use cases**: Add a `network` statement under the BGP address-family if you want the prefix reflected by the RR to all peers.
- **OSPF alone is usually sufficient** for basic reachability in this lab since all devices are in area 0.

### Common mistakes to avoid

1. **Skipping the Linux interface creation** — FRR will accept the config but no traffic flows because the interface doesn't exist in the kernel
2. **Forgetting `ip link set up`** — the dummy interface defaults to down
3. **Forgetting `ip ospf area 0`** — the address won't be advertised, other devices can't reach it
4. **Using `loopback` type instead of `dummy`** — Linux only allows one loopback interface (`lo`)

---

## MCP Tools Available

### Job Management Tools

These tools manage Nautobot jobs (finding, enabling, running, checking results):

- `nautobot_list_jobs(q)` — find jobs by name substring search. Returns `{count, jobs: [{id, name, enabled}]}`
- `nautobot_enable_job(job_id, enabled)` — enable/disable a job. `job_id` is a UUID string, `enabled` is boolean (default true)
- `nautobot_run_job(job_id, data)` — trigger a job. `job_id` is a UUID string, `data` is an **optional JSON string** (not a dict/object — a string containing JSON). Returns `{triggered: true, job_result: {id, ...}}`
- `nautobot_get_job_result(job_result_id)` — check job status. Returns status, result data, and any errors

**Important notes on `nautobot_run_job` `data` parameter:**
- Type: `string` (Optional)
- Content: A JSON-formatted string, e.g. `{"deployment_name": "Netclaw Demo"}`
- The MCP tool internally does `json.loads(data)` to parse it
- If no data is needed, omit the parameter entirely (don't pass empty string)
- Do NOT pass a Python dict or object — pass a string that contains valid JSON
- For the design builder job, the deployment name is `Netclaw Demo` (title case with space)

### Query Tools

- `nautobot_graphql(query)` — run any GraphQL query against Nautobot
- `nautobot_get_devices(name)` — query devices
- `nautobot_get_interfaces(device)` — query interfaces
- `routing_get_bgp_summary(device)` — get BGP state from models
- `routing_get_ospf(device)` — get OSPF state from models

---

## Important Rules

1. **Nautobot is the source of truth** — configs come from GraphQL queries, never hardcoded
2. **Design job populates Nautobot** — do NOT manually create devices/interfaces/IPs via MCP tools
3. **OSPF lives in IGP models** — queried via `ospf_interface_configurations` in GraphQL
4. **BGP lives in BGP models** — queried via `bgp_routing_instances` and `bgp_peerings` in GraphQL
5. **Address-family config from extra_attributes** — commands like `route-reflector-client` are ONLY emitted if expressed in `extra_attributes` on the PeerGroupAddressFamily. If not present, do NOT emit.
6. **extra_attributes placement** — `route-reflector-client` belongs ONLY on the RR's peer-group address family. Spoke endpoint address families get NO extra_attributes. Do NOT put RR-side knobs on spoke-side objects.
7. **BGP network statements are SOT-driven** — only add `network X.X.X.X/Y` under BGP address-family ipv4 if the prefix is explicitly listed in `extra_attributes.networks` on the device's PeerEndpointAddressFamily or PeerGroupAddressFamily in Nautobot. If no `networks` field exists in the SOT data for a device, emit ZERO network statements. Pass any discovered networks in the `bgp_networks` field of `device_context` when calling `ollama_generate_config`.
6. **OSPF network_type from IGP models** — `network_type` is stored directly on each `ospf_interface_configuration` object (not in config_context). Query it via GraphQL and emit `ip ospf network <type>` only when the field is non-empty.
9. **Config push via vtysh** — `docker exec clab-netclaw-demo-<node> vtysh`
10. **Validate after pushing** — always show proof the network is working
11. **Explain as you go** — this is a demo for an audience
12. **Stay in scope** — refuse anything outside the demo
