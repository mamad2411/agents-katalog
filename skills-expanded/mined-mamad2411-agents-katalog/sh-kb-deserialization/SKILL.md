---
name: sh-kb-deserialization
description: "Knowledge base for finding insecure deserialization - untrusted data fed to object-deserialization APIs that can trigger RCE or object injection via gadget chains. Use when hunting deserialization issues. CWE-502, OWASP A08:2021-Software and Data Integrity Failures."
---

# Insecure Deserialization - Hunter Knowledge Base

Deserializing attacker-controlled bytes into live objects can execute code during reconstruction (magic
methods / gadget chains) or corrupt application state. Confirmed native-object deserialization of untrusted
input is typically critical (RCE).

## Sinks by ecosystem (grep targets)
- **Python**: `pickle.load(s)`, `cPickle`, `yaml.load(` without `SafeLoader`, `jsonpickle.decode`,
  `shelve`, `dill`, `marshal.loads`, `pandas.read_pickle`, `numpy.load(allow_pickle=True)`.
- **Java**: `ObjectInputStream.readObject(`, `readUnshared`, XMLDecoder, XStream (default), Kryo,
  SnakeYAML `new Yaml().load(`, Jackson polymorphic typing (`enableDefaultTyping`/`@JsonTypeInfo`),
  Fastjson `parseObject` with autotype.
- **PHP**: `unserialize(` on user input (POP chains via `__wakeup`/`__destruct`).
- **Ruby**: `Marshal.load(`, `YAML.load(` (Psych, pre-safe), `Oj` in object mode.
- **.NET**: `BinaryFormatter.Deserialize`, `LosFormatter`, `NetDataContractSerializer`, `TypeNameHandling` in JSON.
- **Node**: `node-serialize` `unserialize(`, `funcster`, `serialize-javascript` misuse, `vm` on decoded input.

## Detection recipe
1. `graft grep "pickle.load|yaml.load\(|readObject|unserialize\(|Marshal.load|BinaryFormatter|TypeNameHandling|enableDefaultTyping" --json`.
2. Trace the input to the deserializer: request body/cookie/header, cache, queue message, uploaded file,
   or a signed token whose signature isn't verified before deserialization.
3. Check for a safe variant (see filters). If the raw/native deserializer processes untrusted bytes, flag.

## Payloads / PoC
- Python pickle: a class with `__reduce__` returning `(os.system, ('id',))` - describe the gadget; do not
  ship a live malicious blob.
- Java: reference `ysoserial` gadget families (CommonsCollections, etc.) conceptually - the PoC is that the
  endpoint deserializes attacker bytes with vulnerable classpath gadgets present.
- PHP: craft a serialized object of a class with a dangerous `__destruct`/`__wakeup` (POP chain).
- Detection without RCE: send a malformed/DoS payload or an object of an unexpected type and observe
  type-confusion behavior.

## False-positive filters
- **Safe loaders**: `yaml.safe_load`, `SafeLoader`; JSON (`json.loads`, `JSON.parse` of plain data) with no
  polymorphic typing; protobuf/avro/thrift schema-bound decoders; `pickle` of a **trusted, integrity-checked**
  source only (e.g. a file the app itself wrote, signature-verified before load).
- Deserializer restricted by an allowlist of classes / `ObjectInputFilter` (Java) / custom `find_class`.
- Data is signed+verified (HMAC) *before* deserialization and the key is secret.

## CWE / OWASP / severity
CWE-502. OWASP A08:2021. Untrusted native deserialization with reachable gadgets -> **critical**;
object injection with limited impact -> high.

## Chaining hints
Deserialization RCE -> read `secrets`, pivot; often reachable via `access-control` gaps (an endpoint that
accepts serialized state); cache/queue poisoning feeds it a stored payload (second-order).

## Mitigation
Never deserialize untrusted data with native/polymorphic deserializers. Prefer schema-bound formats (JSON
without type info, protobuf). If unavoidable, sign+verify integrity with a secret key and restrict to an
allowlist of expected classes; disable polymorphic typing (Jackson `TypeNameHandling.None`, remove XStream
default). Keep gadget-prone libraries patched.
