---
name: systems-formats
description: "Binary formats and serialisation: choosing a format, endianness, alignment and padding, versioning with backward and forward compatibility, parsing untrusted input with bounds and limits, zero-copy parsing, checksums, compression, magic numbers and headers, fuzzing parsers, and writing the spec down. Read before designing, parsing or changing a file format or a wire protocol."
---

# Binary formats and serialisation

The default format is a `memcpy` of an in-memory struct: host byte order,
compiler padding written to disk, no magic number, no version, and no way
to add a field next year. The default parser reads a `u32` length, calls
`Vec::with_capacity(len)` and falls over on the first corrupt or hostile
file. This skill: pick an existing format first; when you must design
one, make it explicit, versioned, bounded and written down; parse every
input as if an attacker wrote it, because sometimes one did.

## 1. Choose before inventing

| Need | Format | Rust crates |
|---|---|---|
| Human-readable interchange | JSON (integers above 2^53 lose precision in JavaScript: send big ids as strings) | `serde_json` |
| JSON's data model, compact | CBOR (RFC 8949), MessagePack | `ciborium`, `minicbor`, `rmp-serde` |
| Evolving schemas across languages, RPC | Protocol Buffers | `prost` (with `buf` for lint and breaking checks) |
| Read in place without parsing | FlatBuffers, Cap'n Proto | `flatbuffers`, `capnp` |
| Rust to Rust, compact | postcard | `postcard` |
| Rust to Rust, zero-copy | rkyv | `rkyv` (validated access) |
| Pipelines with schema evolution | Avro | `apache-avro` |
| Columnar analytics | Parquet on disk, Arrow in memory and IPC | `parquet`, `arrow` |

- bincode is unmaintained (RUSTSEC-2025-0141): new code uses postcard.
- Invent a format only when none fits (a log, an index, a container with
  random access), and then with a written spec (section 11).

## 2. A custom header

Every file or message starts with a fixed header, all integers
little-endian:

| Offset | Size | Field | Rule |
|---|---|---|---|
| 0 | 8 | magic `89 4D 59 46 0D 0A 1A 0A` | non-ASCII first byte, then CR LF, Ctrl-Z, LF: catches text-mode and 7-bit damage (PNG's trick) |
| 8 | 2 | major version | a reader refuses a major it does not know |
| 10 | 2 | minor version | adds optional content; older readers skip it |
| 12 | 4 | header length | lets a newer header grow; readers skip to its end |
| 16 | 8 | flags | bits 0 to 31 optional, bits 32 to 63 required: an unknown required bit means refuse |
| 24 | 4 | CRC32C of bytes 0 to 23 | header integrity |

The body is records of `type u32, length u32, payload, crc32c u32`
(type-length-value), so a reader skips what it does not understand. A
byte for the compression algorithm (section 9) lets it change later.

## 3. Endianness, explicit

- The spec fixes the byte order (little-endian unless a standard says
  network order) and code converts on every access, even on a match.
- Rust: `u32::from_le_bytes`, `to_le_bytes`; `zerocopy` byte-order types
  for struct views. C: assemble from bytes (compilers emit one load):

```c
static inline uint32_t load_le32(const uint8_t *p) {
    return (uint32_t)p[0] | (uint32_t)p[1] << 8 | (uint32_t)p[2] << 16 | (uint32_t)p[3] << 24;
}
```

  C++20 has `std::endian`, C++23 `std::byteswap`; `le32toh` and friends
  are not portable across Linux, macOS and Windows.

## 4. Alignment and padding stay in memory

- Never `memcpy`, `fwrite(&s, sizeof s, ...)` or `transmute` a struct to
  or from bytes: padding leaks memory contents, layout changes with the
  compiler and target, and a `bool` or enum from arbitrary bytes is UB.
- Encode field by field, or use a view type proven to have no padding and
  to accept any bytes: `zerocopy` derives or `bytemuck::Pod`.

```rust
use zerocopy::byteorder::little_endian::{U16, U32};
use zerocopy::{FromBytes, Immutable, IntoBytes, KnownLayout, Unaligned};

#[derive(FromBytes, IntoBytes, KnownLayout, Immutable, Unaligned)]
#[repr(C)]
struct RecordHeader { kind: U16, flags: U16, len: U32 }

let (header, rest) = RecordHeader::ref_from_prefix(input).map_err(|_| Error::ShortHeader)?;
let len = header.len.get() as usize;
```

- `#[repr(packed)]` and `__attribute__((packed))`: a reference to a
  misaligned field is undefined; copy the field out or use
  `ptr::read_unaligned`.

## 5. Versioning and compatibility

- Plan both directions: new readers read old data (backward), old readers
  read new data and skip what they do not know (forward). Everything that
  may be added later is tagged (a record type, a field number); unknown
  fields are preserved on rewrite when other writers may need them.
- Safe changes: a new optional field with a default, a new skippable
  record type. Breaking: changing a field's type or meaning, reusing a tag,
  reordering positional fields, making an optional field required.
- Protocol Buffers: never reuse a field number (`reserved 4, 7;` and
  `reserved "old_name";` for removed ones); numbers 1 to 15 take one byte,
  so give them to frequent fields; first enum value `*_UNSPECIFIED = 0`;
  `optional` where presence matters; `buf breaking --against
  '.git#branch=main'` in CI.
- Every version the reader still supports has a sample file in the tests.

## 6. Parsing untrusted input

Everything from outside the process is untrusted, including your own
format read back from disk.

- Every length and count is checked against the bytes remaining and a
  maximum before it is used, and never trusted for allocation: reserve
  `min(count, remaining / min_item_size)` and grow as items arrive.
- Limits in one place and in the spec: total size (16 MiB per message,
  say), element count, nesting depth (64), string length, decompressed
  size. No recursion without a depth counter; offset and length arithmetic
  with `checked_add` and `checked_mul`.
- Strict by default: reject trailing bytes, overlong varints,
  non-canonical encodings and duplicate keys (two parsers disagreeing on
  one input is a security bug).
- Errors carry the offset and the expectation (`truncated record at
  offset 1024: need 16 bytes, have 5`).

```rust
pub struct Reader<'a> { rest: &'a [u8], offset: usize }

impl<'a> Reader<'a> {
    pub fn take(&mut self, n: usize) -> Result<&'a [u8], Error> {
        let (head, tail) = self.rest.split_at_checked(n).ok_or(Error::Truncated {
            offset: self.offset, need: n, have: self.rest.len(),
        })?;
        self.rest = tail;
        self.offset += n;
        Ok(head)
    }

    pub fn u32_le(&mut self) -> Result<u32, Error> {
        let (bytes, tail) = self.rest.split_first_chunk::<4>().ok_or(Error::Truncated {
            offset: self.offset, need: 4, have: self.rest.len(),
        })?;
        self.rest = tail;
        self.offset += 4;
        Ok(u32::from_le_bytes(*bytes))
    }

    /// A u32 length prefix, checked against `max` before any byte is taken.
    pub fn bytes_with_len(&mut self, max: usize) -> Result<&'a [u8], Error> {
        let len = self.u32_le()? as usize;
        if len > max {
            return Err(Error::TooLarge { offset: self.offset, len, max });
        }
        self.take(len)
    }

    /// Strict formats end here: bytes left over are an error.
    pub fn finish(self) -> Result<(), Error> {
        if self.rest.is_empty() { Ok(()) } else { Err(Error::Trailing { offset: self.offset }) }
    }
}
```

## 7. Varints and framing

- LEB128 varints (protobuf, WebAssembly): 7 bits per byte, at most 10
  bytes for a u64 and 5 for a u32; reject longer, and in strict mode
  reject overlong forms (`80 00` for zero). ZigZag for signed values.
- Streams need framing: a u32 length prefix checked against a maximum
  frame before the body is read. `tokio_util::codec::LengthDelimitedCodec::builder()
  .max_frame_length(16 * 1024 * 1024).new_framed(io)` does it (default
  8 MiB, a 4-byte big-endian length).
- Append-only logs: each record `magic, length, crc, payload`, so a reader
  detects a torn last write and resynchronises by scanning for the magic.
  Reads are partial: accumulate until the frame is complete.

## 8. Zero-copy and integrity

- Parsed values borrow the input (`&'a [u8]`, `&'a str`) while the owner
  (a `Vec`, an `Mmap`, `bytes::Bytes`) keeps it alive. Views built from
  byte-order types are `Unaligned` and accept any offset; an aligned view
  needs an aligned buffer, and `ref_from_bytes` refuses otherwise.
- FlatBuffers, Cap'n Proto and rkyv read in place: run their verifier on
  untrusted bytes (`flatbuffers::root::<T>`, rkyv's validated `access`);
  the unchecked accessors are for bytes this process wrote.
- `#[serde(borrow)] name: Cow<'a, str>` borrows when the JSON string has
  no escapes and allocates when it does.

| Need | Use | Rust |
|---|---|---|
| Catch accidental corruption | CRC32C (hardware on x86 SSE4.2 and Arm) | `crc32c` |
| Interop with zip, gzip, PNG | CRC-32 (IEEE) | `crc32fast` |
| Fast content hash, no adversary | XXH3 | `xxhash-rust` |
| Content address, tamper evidence | BLAKE3, SHA-256 | `blake3`, `sha2` |
| Tamper evidence with a shared key | HMAC-SHA256, or an AEAD | `hmac`, `chacha20poly1305`, `aes-gcm` |

A CRC catches accidents, not attackers: anyone can recompute it. Checksum
each record or block so damage is local, verify before parsing the
payload, and compare MACs in constant time (`verify_slice`).

## 9. Compression

- zstd by default (level 3; 19 for archives written once); lz4 where
  speed matters more than ratio; gzip or deflate only for interop; brotli
  for web assets.
- Messages under a few KiB compress poorly alone: train a dictionary
  (`zstd --train samples/* -o dict`) and version it with the format.
- Cap the output, whatever the header claims (decompression bombs):

```rust
use std::io::Read;
let mut out = Vec::new();
zstd::stream::read::Decoder::new(input)?
    .take(MAX_DECOMPRESSED as u64 + 1)
    .read_to_end(&mut out)?;
if out.len() > MAX_DECOMPRESSED {
    return Err(Error::DecompressedTooLarge { max: MAX_DECOMPRESSED });
}
```

## 10. Fuzz and test the parser

A fuzz target per entry point; the corpus seeded with test vectors and
real samples; every crash kept as a regression test.

```rust
// fuzz/fuzz_targets/decode.rs (cargo install cargo-fuzz; cargo fuzz init)
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Ok(msg) = myformat::decode(data) {
        let bytes = myformat::encode(&msg);
        assert_eq!(myformat::decode(&bytes).ok(), Some(msg), "round trip changed the value");
    }
});
```

```sh
cargo +nightly fuzz run decode -- -max_total_time=600 -max_len=1048576
cargo +nightly fuzz cmin decode            # shrink the corpus
cargo +nightly fuzz tmin decode <crash>    # shrink a crashing input
```

- `proptest` for `decode(encode(x)) == x` over generated values; C and C++
  parsers with libFuzzer or AFL++ (`systems-c-cpp`, section 10). Time the
  parser on hostile shapes too: a million empty records, maximum depth.

## 11. Write the spec down

A format without a spec is whatever the current code does. Keep
`docs/format.md` (or the schema plus notes) with: purpose and byte order;
the header table (offset, size, type, meaning, allowed values); each
record type; checksums and compression; the limits and what a reader does
on each error; what a reader does with an unknown version, flag, record or
field; and test vectors (small files with a hex dump and the decoded
value) in `tests/vectors/`, decoded by a test so other implementations can
check against them. A Kaitai Struct (`.ksy`) description or an ImHex
pattern helps people inspect files by hand.

## Check it

- `xxd file | head` (or `hexdump -C`) of a written file matches the spec
  table byte for byte.
- Tests decode every vector and every old-version fixture; each limit is
  tested at the limit and one past it; every prefix of a valid message
  (a loop over `0..len`) fails cleanly as truncated, never panics.
- The fuzz target ran at least 10 minutes on this change without a
  finding; say so if it could not run here (cargo-fuzz needs nightly).

## Avoid

Structs written with `memcpy` or `transmute`; host byte order on disk; no
magic number or version; lengths used before they are checked against
what remains and a maximum; `with_capacity` from an input count;
recursion without a depth limit; trailing garbage accepted in a strict
format; reused protobuf field numbers; CRCs trusted against tampering;
decompression without an output cap; bincode in new code; a format with
no spec and no test vectors.
