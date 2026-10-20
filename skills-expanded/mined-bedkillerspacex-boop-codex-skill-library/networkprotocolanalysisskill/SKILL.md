---
name: NetworkProtocolAnalysisSkill
description: >
  Capture and analyze network traffic with PCAP, tshark/Wireshark, Lua dissectors,
  Scapy crafting, state-machine recovery, debugging, and authorized fuzzing. Use for
  pcap triage, custom dissectors, packet reproduction, and controlled protocol testing
  on owned or authorized targets — not for unsolicited interception of third-party traffic.
---

# Network Protocol Analysis

## Scope And Authorization

- **In scope:** traffic you own, lab captures, CTF PCAPs, or systems under written authorization.
- **Out of scope:** unauthorized wiretaps, attacking third-party services, or fuzzing production without approval.
- Prefer offline PCAP analysis first; gate live capture, replay, and fuzzing behind ownership.
- Keep original PCAPs immutable; store derived slices, keys, and parsers separately.
- Redact credentials, cookies, tokens, and PII from reports and example packets.

## When To Use

- Triaging PCAPs for unknown binary protocols or mixed TCP/UDP flows.
- Writing Wireshark/tshark display filters and **Lua dissectors**.
- Reproducing packets with **Scapy** for debugging or authorized interoperability tests.
- Recovering message framing, opcodes, length prefixes, and simple state machines.
- Controlled mutation/fuzzing against **owned** services after baseline capture.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| PCAP forensics / CTF stream focus | `traffic-analysis-pcap` |
| TLS plaintext acquisition method choice | `tls-plaintext-acquisition` |
| Protobuf / gRPC schema recovery | `protobuf-grpc-reverse-engineering` |
| Binary WebSocket payloads | `websocket-binary-reverse-engineering` |
| QUIC / HTTP/3 | `quic-http3-analysis` |
| General custom protocol documentation | `protocol-reverse-engineering` |
| WebSocket CSWSH-style auth testing | `websocket-security` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Layer | Questions | Tools |
| --- | --- | --- |
| Capture | Full duplex? Snaplen? Offload artifacts? | tcpdump, dumpcap, Wireshark |
| Transport | TCP reassembly, UDP loss, ports, TLS? | tshark, follow stream |
| Framing | Length-prefix, delimiter, fixed size? | Hex dump, Scapy |
| Semantics | Opcodes, flags, endianness, checksums | Custom dissector, notes |
| State | Who speaks first? Auth then data? | Timeline, sequence diagrams |
| Validation | Replay accepted? Mutation crashes? | Scapy, boofuzz (authorized) |

## Workflow

### 1. Confirm scope and success criteria

1. Record authorization, capture point (host/NIC/span), environment, and data-sensitivity class.
2. Success examples: filter isolates app protocol; Lua dissector shows fields; Scapy replay elicits valid response; state diagram covers login→command→teardown.
3. Decide offline-only vs live; never fuzz prod by default.

### 2. Capture or ingest PCAP

```bash
# Owned host capture (example)
sudo tcpdump -i eth0 -s 0 -w capture.pcap host 10.0.0.5 and port 9000

# Quick metadata
capinfos capture.pcap
tshark -r capture.pcap -q -z conv,tcp
tshark -r capture.pcap -q -z io,phs
```

1. Hash originals: `sha256sum capture.pcap`.
2. If TLS, obtain keys via `tls-plaintext-acquisition` or use pre-master secrets; do not assume PCAP alone yields HTTP bodies.
3. Slice interesting flows to working copies.

### 3. Triage streams and framing

```bash
# List TCP streams and endpoints
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.stream | sort -u

# Follow one stream (stream index N)
tshark -r capture.pcap -q -z follow,tcp,raw,0
tshark -r capture.pcap -Y 'tcp.stream eq 0' -T fields -e data.data | head
```

1. Identify **length-prefix** (common: 2/4-byte BE/LE size + payload) vs delimiter (`\n`, `0x00`) vs fixed records.
2. Note handshake banners and magic bytes.
3. Align multiple samples; mark fields that change with controlled inputs (username length, sequence).

### 4. Wireshark filters and Lua dissectors

**Display filters (examples):**

```text
tcp.port == 9000
tcp.stream eq 3
frame contains 01:02:03:04
http.request.method == "POST"
```

**Minimal Lua dissector skeleton** (lab):

```lua
local p_proto = Proto("labproto", "Lab Protocol")
local f_len = ProtoField.uint32("labproto.len", "Length", base.DEC)
local f_op  = ProtoField.uint8("labproto.op", "Opcode", base.HEX)
p_proto.fields = { f_len, f_op }

function p_proto.dissector(buf, pinfo, tree)
  if buf:len() < 5 then return end
  pinfo.cols.protocol = "LABPROTO"
  local t = tree:add(p_proto, buf())
  t:add(f_len, buf(0,4))
  t:add(f_op, buf(4,1))
end

local tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(9000, p_proto)
```

1. Load via Wireshark personal plugins dir; verify on known PCAP.
2. Prefer expert info for checksum/length mismatches.

### 5. Scapy craft, replay, and authorized mutation

```python
from scapy.all import IP, TCP, Raw, send, sr1, sniff

# Rebuild one application payload (example framing)
payload = b"\x00\x00\x00\x05\x01" + b"hello"
pkt = IP(dst="10.0.0.5") / TCP(dport=9000, sport=40000, flags="PA", seq=1, ack=1) / Raw(load=payload)
# Prefer full TCP session helpers or app-level sockets for reliability:
import socket
s = socket.create_connection(("10.0.0.5", 9000), timeout=3)
s.sendall(payload)
print(s.recv(4096))
```

1. Replay **golden** messages first; confirm service accepts them.
2. Mutate one field at a time (length vs body mismatch, bad opcode, oversized length).
3. Gate crash-finding fuzzing behind explicit authorization; capture cores/logs.

### 6. State-machine recovery

1. Order messages by time and direction (C→S / S→C).
2. Label states: `INIT`, `AUTH`, `READY`, `CLOSE`, error paths.
3. Document mandatory fields per state; note idempotent vs one-shot messages.
4. Validate by driving transitions from a clean client.

### 7. Hand off

1. Deliver: hashed PCAP, filters, dissector script, field notes, state diagram, known-good Scapy/socket client.
2. Keep secrets out of committed PCAPs when possible (use redacted slices).
3. Route gRPC/WebSocket/QUIC-specific work to specialist skills.

## Command Pad

```bash
# Top talkers
tshark -r capture.pcap -q -z endpoints,ip

# Export HTTP objects when decrypted
# Wireshark: File → Export Objects → HTTP

# Hex + ASCII of payload only
tshark -r capture.pcap -Y 'tcp.stream eq 0' -T fields -e tcp.payload | head

# Merge / split
mergecap -w all.pcap a.pcap b.pcap
editcap -c 1000 big.pcap split.pcap
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Owned capture point + ticket | SPAN on neighbor tenant traffic |
| Science | Controlled input delta | Single packet speculation |
| Framing | Length checks vs real sizes | Treating TCP segments as messages |
| Fuzzing | Staging + crash buckets | Unbounded prod fuzz |
| Privacy | Redacted exports | Full auth cookies in gist |

## Output Checklist

- [ ] Authorization and capture conditions recorded
- [ ] Original PCAP hashed and immutable
- [ ] Streams triaged; framing hypothesis written
- [ ] tshark/Wireshark filters saved
- [ ] Dissector or parser produces named fields on samples
- [ ] Replay of golden messages succeeds (if live allowed)
- [ ] State machine covers happy path + at least one error path
- [ ] Mutations/fuzz results (if any) documented with limits
- [ ] Cross-links to TLS/gRPC/WS/QUIC skills when needed
- [ ] PII/secrets redacted

## Rules

- Authorized capture and testing only.
- Prefer offline analysis; escalate invasiveness only with clear ownership.
- Validate protocol hypotheses against multiple samples and one controlled change.
- Do not treat this skill as a license to intercept others’ traffic.
- Keep originals immutable; redact credentials from all shared artifacts.
