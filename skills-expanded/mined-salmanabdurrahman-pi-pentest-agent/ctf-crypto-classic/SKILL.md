---
name: ctf-crypto-classic
description: Classic cipher CTF workflow — Vigenere key recovery, Kasiski examination, XOR frequency analysis, multi-byte XOR key recovery, OTP key reuse (many-time pad), cascade XOR, book cipher, homophonic substitution, Atbash, Caesar/ROT, and historical cipher attacks for authorized lab/competition material.
disable-model-invocation: true
risk: passive
allowed-modes: [ctf]
authorization-required: yes
evidence-outputs: [artifact-hash, analysis-notes, key-recovery-notes, redacted-decryption]
---

# Classic cipher CTF — identification, analysis, and key recovery

Use this skill for cryptanalysis of classic and historical cipher challenges in authorized CTF competitions, lab exercises, or educational environments. Every technique assumes the ciphertext is provided as a challenge artifact. Never apply these techniques to real communications, intercepted traffic, production secrets, or any material outside explicit competition scope. All analysis should be performed offline on local challenge files. Remote interaction is only permitted when the challenge explicitly provides a service endpoint within competition infrastructure.

This skill covers: cipher-type fingerprinting through statistical profiling, monoalphabetic and polyalphabetic substitution attacks, transposition analysis, XOR-family key recovery, historical cipher emulation, and multi-layer cascade unwrapping. The workflow emphasizes methodical hypothesis-testing cycles: form a hypothesis about the cipher family and key structure, design a discriminating test, execute through gated tooling, record the result, and refine.

## Required inputs

- Challenge artifact file (ciphertext, encoded blob, or encrypted archive) with its SHA-256 hash recorded before any transformation.
- Written scope confirming the artifact belongs to an authorized CTF competition, lab exercise, or educational environment. Include: competition name, challenge name, allowed tooling, any rate limits or service constraints, and the challenge provider's rules on collaboration and writeup sharing.
- If the challenge includes a remote service: host, port, protocol, and the exact interaction contract described in the challenge statement. Never interact with a service without first validating it against the competition scope.
- Valid authorization cache for the CTF engagement. Separate authorization is required if the challenge spans multiple service endpoints or requires credentials beyond the initial challenge file.
- For challenges with password-protected archives, encrypted ZIP files, or encoded layers: the challenge description or hints, plus any known plaintext, key fragment, or structural constraint disclosed by the challenge author.
- Known constraints from the challenge: alphabet size, character set (printable ASCII, hex, base64 alphabet, alphanumeric, custom), expected plaintext language (English, numeric, JSON, XML, flag format), and any structural hints (key length range, cipher era, historical context).

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before any planning or analysis.
2. Use `pentest_agent_parse_scope` for the competition rules, lab targets, challenge files, accounts, and time limits. Confirm that the challenge artifact hash is recorded in scope.
3. Use `pentest_agent_validate_target` before any service contact, even within the CTF infrastructure. For offline-only challenges, validate that no remote contact is needed.
4. Use `pentest_agent_check_authorization` before active service interaction. Re-check if analysis reveals a new endpoint, if the challenge scope expands, or if the engagement time window changes.
5. Use `pentest_agent_build_command` for dry-run argument preview when catalog tools (hashcat, john, Python cryptanalysis libraries, CyberChef, dCode, quipqiup, RsaCtfTool, SageMath) are needed. Review the argument list for correctness and safety before execution.
6. Use `pentest_agent_execute_tool` for all tool execution — never raw shell. This enforces rate limiting, approval gates, timeout boundaries, disabled-category policy, and output redaction.
7. Use `pentest_agent_append_evidence` to record each analysis step, `pentest_agent_record_finding` for recovered keys or flags, and report tools for final handoff.

## Workflow

### Phase 1 — artifact intake and encoding normalization

Begin with thorough intake before any cryptanalysis. Every cipher challenge has at least one encoding layer (base64, hex, base32, decimal, binary) wrapping the raw ciphertext. This phase strips encodings and establishes the working byte representation.

1. Record the challenge file hash with `pentest_agent_append_evidence`. Include filename, file size in bytes, and the first 64 hex characters of the SHA-256 digest. This creates an immutable anchor for the analysis chain.
2. Inspect the raw artifact visually. Determine the character set: does it contain only hex digits (0-9, a-f), base64 alphabet (A-Z, a-z, 0-9, +, /, =), base32 alphabet (A-Z, 2-7, =), decimal numbers separated by spaces or commas, binary digits, or printable ASCII? The character set constrains the encoding hypothesis.
3. Detect multi-layer encoding by applying encoding recognition in sequence. Common patterns: base64 → hex → raw bytes, or base64 → base32 → hex, or decimal → ASCII → base64. Each decoding step should narrow the character set. If a decode produces printable text that looks like another encoded layer, apply recognition again. Stop when you reach either: raw unreadable bytes (entropy analysis begins), or readable plaintext (challenge may already be solved).
4. Check for compression. If the decoded output has high entropy but a recognizable archive signature (PK for ZIP, 1f8b for gzip, BZh for bzip2), the challenge may require decompression before cryptanalysis. Record the compression format in evidence.
5. Check for steganographic embedding. If the challenge file is an image, audio file, or PDF, and decoding the visible text yields nothing, suspect steganography. Use the `ctf-stego` skill for embedded-data extraction, then return to this skill with the extracted payload.
6. Once the raw ciphertext bytes are isolated, compute entropy using Shannon entropy over byte values (0-255). Record the entropy value:
   - Entropy near 8.0 bits per byte: likely random or properly encrypted (modern cipher, OTP, or compressed data). Proceed to Phase 2 with XOR and modern-cipher hypotheses.
   - Entropy between 4.0-7.0 bits per byte: likely classic cipher (substitution, transposition, Vigenere). The ciphertext alphabet may be restricted.
   - Entropy below 4.0 bits per byte: likely simple substitution, Caesar, or plaintext encoding.
7. Determine the effective alphabet size. Count unique byte values in the ciphertext. If only 26 distinct bytes appear (or 52 with case), suspect a monoalphabetic substitution on English letters. If the set size is exactly 64, suspect base64-alphabet ciphertext. An alphabet size of 256 with high entropy suggests XOR with an unknown key or a modern stream cipher.

### Phase 2 — cipher-type fingerprinting via statistical profiling

Once raw ciphertext bytes are isolated, run statistical tests to discriminate between cipher families. Each test provides evidence for or against a specific cipher type. Combine multiple tests for a confidence-weighted hypothesis.

1. **Index of Coincidence (IC)**. Compute IC over the full ciphertext. IC measures the probability that two randomly selected characters are identical. For English plaintext, IC ≈ 0.0667 (1/26 * 1.065). For random text over 26 letters, IC ≈ 0.0385 (1/26). For a monoalphabetic substitution cipher, IC matches the plaintext language IC because letter frequencies are preserved (only symbols change). For polyalphabetic ciphers (Vigenere, running key), IC drops toward random as the key length increases. For a one-time pad, IC is exactly random.
   - IC > 0.060: strongly suggests monoalphabetic substitution or plaintext.
   - IC between 0.045-0.055: suggests short-key polyalphabetic cipher (Vigenere with key length 3-10).
   - IC near 0.038: suggests long-key polyalphabetic cipher, XOR with random-looking key, or modern encryption.
   - IC < 0.030: suggests non-alphabetic data, heavily compressed data, or a very long key.

2. **Chi-squared against English letter frequency**. Compute the chi-squared statistic comparing the ciphertext character frequency distribution to expected English letter frequencies (ETAOIN SHRDLU). A low chi-squared value means the distribution matches English — this happens with transposition ciphers (which rearrange letters) and monoalphabetic substitutions (which remap but preserve distribution shape). A high chi-squared value means the distribution is flattened, suggesting polyalphabetic or XOR ciphers.

3. **Autocorrelation / Kasiski examination for period detection**. Compute the autocorrelation of the ciphertext at lags from 1 to 20 (or up to ciphertext length / 3). For each lag distance, count positions where the ciphertext character equals the character at position + lag. A significant spike at lag K suggests a repeating key of length K. Additionally, search for repeated trigrams, tetragrams, or longer n-grams. For each repeated sequence, compute the distance between occurrences and factor it. The most common factor across all repeated sequences is likely the key length. This is the classical Kasiski examination. Use a Python cryptanalysis library or CyberChef's "Kasiski Examination" operation for automated factoring.

4. **Friedman test for key length estimation**. Apply the Friedman test to estimate the most probable key length. The formula uses the observed IC and the expected IC values for the plaintext language. The estimate may not be exact but narrows the key-length range for subsequent brute-force or column-attack phases.

5. **Byte-value distribution plot for XOR detection**. For decoded raw bytes (values 0-255), plot a histogram of byte frequencies. If the distribution is flat (all 256 values appear with roughly equal frequency), the data is either random (OTP key material) or XOR-encrypted with a random-looking key. If the distribution has spikes at specific byte values, the underlying plaintext structure is bleeding through — a short XOR key or a classic cipher on bytes.

6. **File signature / magic byte check**. XOR the first few ciphertext bytes against known file-format magic bytes. If the plaintext is a known file type (PNG: 89 50 4E 47, PDF: 25 50 44 46, ZIP: 50 4B 03 04, JPEG: FF D8 FF E0), XOR the ciphertext prefix against each candidate magic sequence. If a candidate produces a plausible repeating pattern, you have recovered part of the XOR key. This is a specialized crib-drag for structured plaintext.

Based on the combined evidence from IC, chi-squared, Kasiski, and distribution analysis, assign a primary hypothesis and one or two secondary hypotheses. Record the hypothesis, supporting evidence, and confidence level in the evidence log before proceeding to the targeted attack phase.

### Phase 3 — monoalphabetic substitution attacks

When IC is high (> 0.060) and chi-squared against English is low (distribution shape preserved), the cipher is likely a monoalphabetic substitution. This includes Caesar/ROT variants, Atbash, keyword-based substitution alphabets, and arbitrary permutation ciphers.

1. **Caesar / ROT variants (shift ciphers)**. If the ciphertext contains only letters with preserved case, test all 25 possible shifts. For each shift, score the resulting plaintext using English n-gram frequency (bigram or trigram log-probability). The shift with the highest score is the most likely. For ROT13 specifically: ROT13 is self-inverse; applying it twice returns the original text. Many CTF challenges use ROT13 as an encoding layer before another cipher. Use CyberChef's "ROT13" operation or a Python script that iterates ROT1-ROT25 with n-gram scoring.

2. **Atbash cipher**. Atbash maps A→Z, B→Y, C→X, etc. — it reverses the alphabet. Testing Atbash requires a single transformation. If the plaintext looks like reversed-alphabet nonsense, Atbash is confirmed. Some challenges apply Atbash after a shift cipher or before base64 encoding. Test Atbash early as a cheap check.

3. **Frequency-based substitution cracking (general monoalphabetic)**. This is the core technique. Compute the frequency of each ciphertext character and map the most frequent ciphertext character to 'E' (the most common English letter), the second most frequent to 'T', and so on. However, letter frequencies in short ciphertexts deviate from the reference distribution, so automated solvers use more robust methods:
   - Use **quipqiup** for automated substitution solving via a web query or local API. quipqiup uses a dictionary-based search with letter-frequency heuristics and performs well on English ciphertexts of 50+ characters. Submit the ciphertext through a controlled, scoped HTTP request if competition rules permit external solver services. Record the service used in evidence.
   - Use **dCode**'s "Mono-alphabetic Substitution" tool for its interactive solver. dCode supports custom alphabets, known-plaintext cribs, and constraint-based solving (lock specific letter mappings). Useful when partial plaintext is known (flag format prefix like `CTF{`).
   - Use **CyberChef**'s "Substitute" operation for manual letter-by-letter mapping. After setting an initial frequency-based mapping, manually adjust mappings based on emerging words. Look for common English patterns: `THE`, `AND`, `THAT`, `ING`, `ION`.
   - Use **Python cryptanalysis libraries** with hill-climbing or simulated-annealing solvers. These evaluate candidate plaintexts using quadgram or quintgram statistics, randomly swap two letter mappings, and keep the swap if the n-gram score improves. This converges to the correct mapping for ciphertexts as short as 100 characters.

4. **Homophonic substitution**. When IC is moderate but frequency distribution is oddly flattened, the cipher may be homophonic: each plaintext letter maps to multiple ciphertext symbols (to flatten the frequency distribution and defeat simple frequency analysis). Common in historical ciphers (Zodiac cipher, Beale ciphers). Homophonic ciphers require a different approach:
   - Count the number of distinct ciphertext symbols. If there are significantly more than 26 (e.g., 50-100 symbols), homophonic substitution is likely.
   - Cluster symbols by the context in which they appear (neighbors, positions). Symbols that appear in similar contexts may map to the same plaintext letter.
   - Apply a hill-climbing solver with an expanded mapping table (multiple ciphertext symbols per plaintext letter). The solver must jointly optimize which symbols map to which letters.
   - Use known cribs (expected words). If the flag format is known, map the crib's letters to likely positions in the ciphertext and eliminate symbol assignments that conflict.

### Phase 4 — Vigenere and polyalphabetic substitution attacks

When IC is moderate (0.045-0.055) and Kasiski examination reveals repeated sequences, the cipher is likely Vigenere or a variant. Vigenere uses a repeating keyword to select different Caesar shifts for each position.

1. **Key length determination**. Use the combined Kasiski and Friedman evidence from Phase 2:
   - Collect all repeated trigrams and longer n-grams. For each, factor the distance between occurrences. Tally the factor counts. The most common factor is the probable key length.
   - Compute the IC for each candidate key length: split the ciphertext into K columns (characters at positions i, i+K, i+2K, ...) and compute IC for each column. If each column has IC ≈ 0.066 (monoalphabetic), K is correct. If columns show IC ≈ 0.038 (random), K is wrong.
   - Start with the most probable K and test IC per column. If all columns have high IC, K is confirmed.

2. **Column-by-column frequency attack**. Once key length K is confirmed, each column is a Caesar cipher (shifted by one key letter). Attack each column independently:
   - For each of the K columns, compute the letter frequency distribution.
   - For each column, find the shift that best aligns the column's frequency distribution with English. The best shift is the one that maximizes the dot product of the column frequency vector with the English frequency vector, or minimizes chi-squared.
   - Alternatively, for each column, try all 26 shifts and score the resulting column plaintext using English n-gram statistics. The shift with the highest score is the correct key letter for that column.
   - Once all K key letters are recovered, decrypt the full ciphertext and verify the plaintext reads as English.

3. **Known-plaintext key derivation**. If a crib (known plaintext fragment) is available, derive the key directly:
   - Align the crib with the most probable position in the ciphertext. For each position i where the crib letter is known, compute: key_letter[i mod K] = (ciphertext[i] - crib[i] + 26) mod 26.
   - This directly reveals key letters at each position. If the crib is long enough (longer than K), the entire key is revealed.
   - If only a partial key emerges (some positions not covered by the crib), fill gaps with the column-by-column frequency attack.

4. **Vigenere variants**. Be alert for common Vigenere variants:
   - **Beaufort cipher**: similar to Vigenere but uses a different formula. If Vigenere decryption with the recovered key produces gibberish, try Beaufort with the same key.
   - **Autokey cipher**: the key is the keyword followed by the plaintext itself (or ciphertext). Key recovery is more complex; use a known crib at the beginning and iteratively extend the key.
   - **Running key cipher**: the key is a long English text passage, not a repeating word. The IC will be lower than standard Vigenere and Kasiski will fail. If IC suggests a very long key but the ciphertext is alphabetic, suspect a running key. Attack by shifting the ciphertext against itself and looking for plausible plaintext fragments.

### Phase 5 — XOR-family key recovery

When the ciphertext is raw bytes (all values 0-255) with a distribution that is neither perfectly flat nor strongly spiked, XOR with a short to medium key is likely. XOR is the workhorse of CTF crypto challenges.

1. **Single-byte XOR (fixed key)**. The simplest XOR challenge: every plaintext byte is XORed with the same key byte K.
   - For each candidate key byte (0-255), XOR the entire ciphertext and score the resulting plaintext using a character-frequency model. The scoring model should penalize non-printable characters (bytes < 0x20 or > 0x7E, except common whitespace: 0x0A newline, 0x0D carriage return, 0x09 tab, 0x20 space) and reward English-like letter frequencies.
   - A robust scoring function uses the Bhattacharyya coefficient or log-likelihood against a reference English letter-frequency table (including space, which is the most common character at ~15-20%).
   - Use **CyberChef**'s "XOR Brute Force" operation with the key length set to 1 and crib set to a known plaintext fragment (e.g., "flag{" or "CTF{"). CyberChef filters results to only those containing the crib.
   - Use **Python cryptanalysis libraries** with a character-frequency scorer and iterate all 256 key bytes. The key byte with the highest score is the correct key.

2. **Multi-byte XOR key (repeating-key XOR)**. When the key has length K > 1, the ciphertext is the plaintext XORed with the key repeated to plaintext length.
   - **Key length detection via Hamming distance**. For each candidate key length from 1 to 40 (or up to ciphertext length / 4), compute the normalized Hamming distance between the first K bytes and the second K bytes of the ciphertext. The key length with the smallest normalized Hamming distance is the most probable. This works because XOR of two plaintext bytes (both from the same character distribution) has lower average bit difference than XOR of two random bytes. Normalize by K to avoid bias toward shorter keys.
   - Take the top 3-5 candidate key lengths from the Hamming distance ranking. For each candidate, apply the single-byte XOR attack to each of the K columns (bytes at positions i, i+K, i+2K...). Each column is XORed with the same key byte, so the single-byte XOR attack applies directly.
   - Score the fully decrypted plaintext for each candidate key length. The combination with the highest overall plaintext score is correct.
   - Use **CyberChef**'s "XOR Brute Force" with crib filtering for known plaintext fragments. This is faster than scoring-based approaches when a reliable crib is available.

3. **Crib dragging (known-plaintext attack on XOR)**. When a crib (expected plaintext word or phrase) is known, crib dragging directly reveals key bytes without needing to determine key length first.
   - XOR the crib against every position in the ciphertext. If the crib is at position P, the XOR result at position P is the key (if the crib is correct). Examine the result at each position: if the XOR output looks like a plausible key fragment (readable, structured, or repetitive), the crib position is likely correct.
   - For each candidate position, extend the revealed key fragment forward and backward by assuming the key repeats or continues. If the key is cyclical, the fragment should match at positions offset by the key length.
   - Crib dragging is particularly effective when the plaintext format is partially known (JSON with known field names, XML tags, protocol headers, flag format). For a flag with format `flag{...}` or `CTF{...}`, drag the crib `flag{` or `CTF{` across the ciphertext. The position that reveals a plausible key fragment is the flag start.

4. **Cascade XOR (multiple XOR layers)**. Some challenges apply XOR encryption twice with different keys (cascade). The effective key is the XOR of the two original keys (Key1 XOR Key2). The ciphertext can be treated as single-key XOR and attacked with the multi-byte XOR method above. However, if the cascade uses keys of relatively prime lengths, the effective key length is the least common multiple, which may be too long for the Hamming-distance method. If single-key XOR fails, suspect:
   - XOR with key A of length L1, then XOR with key B of length L2.
   - If L1 and L2 are known or hinted, attempt to strip one layer by guessing key A (or B) and applying the single-byte XOR method to each column of the resulting ciphertext.
   - Cascade XOR is sometimes used with one key known (from a previous challenge step) and one key unknown. Apply the known key first, then attack the remainder.

### Phase 6 — many-time pad (OTP key reuse) attacks

The many-time pad is one of the most iconic CTF crypto challenges. Two or more plaintexts are encrypted with the same OTP keystream. Since the key is the same, XORing two ciphertexts cancels the key and yields the XOR of the two plaintexts.

1. **Detecting OTP reuse**. The challenge typically provides two or more ciphertexts of equal (or similar) length. If only one ciphertext is provided, OTP reuse cannot be exploited (unless the keystream itself has structure — see LFSR/stream cipher attacks in the modern crypto skill). The challenge description often hints at key reuse: "we encrypted two messages with the same key," "the same pad was used twice," or "sent two messages using our unbreakable encryption."

2. **Two-ciphertext crib dragging**. With two ciphertexts C1 and C2:
   - Compute D = C1 XOR C2. D is the XOR of P1 and P2 (the key cancels). D is not random — it's the XOR of two English (or structured) plaintexts.
   - Drag cribs through D. Guess a word that might appear in P1 at position i. XOR the crib with D at that position. If the crib position is correct, the result is the corresponding plaintext from P2 at that position. If that result looks like plausible text, the crib guess is confirmed.
   - Extend in both directions. Once one word is confirmed, the surrounding plaintext from both messages emerges. Use the partially revealed P1 to guess the next word, XOR that guess with D to reveal more of P2, and iterate. This technique is called "crib dragging" and is a manual, interactive process.

3. **Automated many-time pad solver**. For more than two ciphertexts, or when manual crib dragging is too slow:
   - Use a statistical approach: at each position, consider all possible pairs of plaintext characters that XOR to the observed D value at that position. Assign probabilities based on character frequency. Use a dynamic-programming or Viterbi-like algorithm to find the most probable pair of plaintexts across all positions, with a language model penalizing improbable character transitions.
   - **Python cryptanalysis libraries** exist that implement probabilistic many-time pad solvers. They combine character n-gram probabilities with the constraint that P1[i] XOR P2[i] = D[i]. The solver iteratively refines probability estimates.
   - An alternative space-based heuristic: space (0x20) XORed with any letter (0x41-0x5A, 0x61-0x7A) flips the letter case. Since spaces are frequent in English text, positions in D where one plaintext has a space produce a readable letter (opposite case) in the XOR output. At each position, if D[i] is a letter (0x41-0x5A or 0x61-0x7A), one of the plaintexts likely has a space at that position. Assign spaces greedily based on this heuristic, then fill in the letters.
   - Use **CyberChef** for visual crib dragging: compute the XOR of C1 and C2, then use the "XOR Brute Force" or "Strings" operations to visually identify when crib placement produces readable output.

4. **More than two ciphertexts**. With N ciphertexts encrypted with the same keystream, the constraint network is denser: for any pair i,j, P_i XOR P_j = C_i XOR C_j. This provides N*(N-1)/2 constraints. The probabilistic solver can use all pairs simultaneously to converge faster. If one plaintext fragment is recovered (e.g., from a known header), it can be XORed with all other ciphertexts to reveal the corresponding plaintext fragments in all messages at once.

### Phase 7 — book cipher and codebook attacks

A book cipher maps plaintext words or letters to positions in a known reference text (the "book"). Without the book, the cipher is unbreakable. In CTF challenges, the "book" is either provided (as a text file), hinted at (a famous text, song lyrics, constitution, religious text, or the challenge description itself), or recoverable from context.

1. **Identifying a book cipher**. The ciphertext typically consists of numbers: either single numbers (word index), number pairs (page, word), or triples (page, line, word). Other formats include: (chapter, paragraph, word), (line, offset), or offsets from a known starting point. If the ciphertext is a sequence of integers and the challenge provides a text file or references a specific document, suspect a book cipher.

2. **Brute-force with a known book**. If the book text is provided, construct the word list: split the book into words, preserving order. For each ciphertext number N, retrieve the Nth word (for 1-indexed) or (N+1)th word (for 0-indexed). Concatenate the retrieved words to form the plaintext. Test both indexing schemes.

3. **Unknown book — dictionary attack**. If the book is not provided but the challenge hints at a category ("the key is the opening of a famous novel"), iterate through a corpus of common texts: the US Constitution, the Declaration of Independence, the Bible (King James), Shakespeare's complete works, Pride and Prejudice, Moby Dick, Alice in Wonderland, or the Universal Declaration of Human Rights. For each candidate text, compute the decoded plaintext and score it. The candidate that produces readable English is the correct book.

4. **Unknown book — challenge-description attack**. Sometimes the challenge description itself is the book. Extract the challenge description text, split into words, and use as the reference. This is common in "meta" challenges where the ciphertext is hidden in the challenge narrative.

5. **Brute-force starting position**. If the book is known but the indexing is ambiguous (does numbering start from word 1, word 0, or some offset?), brute-force a small offset range (0-100) and score each decoded plaintext.

6. **Valid-character-set filter**. For any book cipher candidate, filter the decoded output against the expected character set. If the candidate produces non-printable characters, binary data, or nonsensical symbol sequences, the candidate is wrong. The correct book produces words that form grammatical English sentences.

### Phase 8 — historical and mechanical cipher attacks

Some CTF challenges feature emulated historical cipher machines or period-specific ciphers. These are typically solved with specialized tools or conceptual understanding.

1. **Enigma with known rotor settings**. If the challenge provides Enigma-encrypted ciphertext and the rotor types, ring settings, and plugboard are given (or partially given as a hint), use an Enigma simulator to decrypt. The key parameters are: rotor selection (I through VIII), rotor order (left, middle, right), ring settings (Ringstellung, 01-26 for each rotor), initial rotor positions (Grundstellung), and plugboard pairs (Steckerbrett, up to 10 letter pairs). When all parameters are known, decryption is straightforward via simulation. Use **CyberChef**'s "Enigma" operation or a Python Enigma library.

2. **Enigma with partial settings**. When some settings are unknown but constrained (e.g., only 3 of 5 possible rotors, 10 possible plugboard pairs), brute-force the unknown parameters. The search space for full Enigma settings is too large (10^23 combinations) for exhaustive search, but with constraints (known rotors, small plugboard, known crib), the search is feasible. Use the crib as a known-plaintext discriminator: for each candidate setting, decrypt and check if the crib appears.

3. **Lorenz / Tunny cipher (delta attack concept)**. The Lorenz SZ-40/42 was a German teleprinter cipher machine from WWII. Its cryptanalysis by Bill Tutte and the Bletchley Park team is a landmark. CTF challenges that emulate Lorenz typically require understanding the delta attack conceptually: exploiting the XOR of two adjacent ciphertext bits to cancel the influence of two of the five chi wheels, then using statistical correlation to recover the remaining wheel settings. Implementations exist in Python cryptography libraries. The attack requires iterative bit-level statistical analysis across the ciphertext length.

4. **ADFGVX / ADFGX cipher**. A WWI German field cipher combining a Polybius square substitution with a columnar transposition. The square maps letter pairs (from the alphabet ADFGVX) to plaintext characters. The ciphertext is then transposed by keyword. Attack: first determine the transposition keyword length (by factoring ciphertext length), then reconstruct the columns, and finally solve the Polybius square using frequency analysis. Use **dCode** or **CyberChef** for automated solving.

5. **Playfair cipher**. A digraph substitution cipher using a 5x5 key square (I and J share a cell). Key recovery uses known-plaintext fragments: if a crib is available, the key structure can be partially recovered by tracing digraph mappings. With a full crib, the entire key square can be reconstructed. For ciphertext-only attacks, use a hill-climbing solver that optimizes the key square to maximize English digraph probability. Reference: **dCode** "Playfair Cipher" and **CyberChef** "Playfair" operations.

6. **Bifid cipher**. Uses a Polybius square followed by a transposition of the encoded coordinates. Attack by brute-forcing the key square period (the length of coordinate blocks). For short periods, try all possible squares and check for English output.

7. **Hill cipher (matrix-based polygraphic substitution)**. Encrypts plaintext blocks as vectors multiplied by a key matrix (mod 26). To attack: if the key matrix dimension N is known or guessed, and if N known-plaintext/ciphertext pairs are available, the key matrix can be recovered by solving a system of linear equations (mod 26). The key matrix must be invertible mod 26 for decryption to be possible. Use **SageMath** for matrix operations over Z/26Z (with careful handling of non-coprime elements). If the matrix dimension is unknown but small (2-4), brute-force all possible dimensions and check the determinant for coprimality with 26.

### Phase 9 — transposition and columnar cipher attacks

Transposition ciphers rearrange the plaintext characters without changing them. The character frequencies match the plaintext exactly, so IC remains high.

1. **Identifying a transposition cipher**. High IC, low chi-squared against English, but ciphertext looks like random letters (no obvious word patterns). The letters are all from the plaintext — they are just in the wrong order. This distinguishes transposition from substitution: in substitution, the letters are remapped but in the right order; in transposition, the letters are the original ones but in the wrong order.

2. **Columnar transposition**. The plaintext is written into a grid by rows, then read out by columns in the order determined by a keyword. Attack:
   - Determine the number of columns: factor the ciphertext length. Common factors are candidate column counts.
   - For each candidate column count C, calculate the number of rows R = ceil(length / C). Write the ciphertext into a grid of C columns by R rows (filling columns in keyword order — since the keyword order is unknown, this is the hard part).
   - Use anagramming: try different column permutations and score the resulting plaintext. For small C (2-7), brute-force all C! permutations. For larger C, use a hill-climbing or genetic algorithm that swaps columns and keeps swaps that improve English n-gram probability.
   - Use **CyberChef**'s "Columnar Transposition" operation with a brute-force option for short keys, or use **dCode** for interactive anagramming.

3. **Rail fence cipher**. A zigzag transposition where plaintext is written along "rails" (diagonal lines) and read off horizontally. The key is the number of rails. Attack: try rail counts from 2 to 10 and score the resulting plaintext. The rail fence leaves a recognizable pattern: if the ciphertext length is L and the rail count is R, the first rail contains characters at positions 0, 2R-2, 4R-4... etc. Use **CyberChef**'s "Rail Fence Cipher Decode" operation.

4. **Scytale cipher**. An ancient Greek transposition using a rod of a specific diameter. The ciphertext is the message wrapped around the rod. In CTF terms, this is equivalent to writing the plaintext in a grid of fixed column width and reading by columns. Brute-force the rod diameter (column width) and score the output.

5. **Route cipher**. A transposition where the plaintext is placed in a grid and read out following a specific path (spiral inward, diagonal, knight's move, etc.). The route may be described in the challenge narrative. Implement a decoder for each candidate route and score the output. Common routes: clockwise spiral, counterclockwise spiral, diagonal-zigzag, and alternating column directions.

### Phase 10 — multi-layer unwrapping and cascade ciphers

Many CTF challenges apply multiple cipher layers in sequence. Each layer must be recognized and reversed in the correct order.

1. **Layer recognition**. After each decryption step, examine the output:
   - Does it look like another encoded layer? (hex, base64, base32 encoding)
   - Does it look like ciphertext for a different cipher family? (e.g., after breaking a Vigenere layer, the output is XOR-looking bytes)
   - Does it contain a recognizable plaintext pattern? (flag format, English prose, JSON structure)
   - Does it contain another challenge artifact? (a URL, a new file hash, instructions for the next step)

2. **Hypothesis tracking**. Maintain an ordered list of layers identified so far. For each layer, record: the layer number, the cipher type, the key (if recovered), the tool used, and the evidence hash. This creates an audit trail that can be unwound if a later hypothesis proves wrong.

3. **Cascade unwinding order**. Decryption must proceed in the reverse of encryption order. If the challenge encrypts as plaintext → Vigenere → base64 → XOR, decryption must proceed as XOR → base64 decode → Vigenere. Identifying the outermost layer correctly is critical. The outer layer is what you see in the challenge file: is it base64 text? Hex? Raw bytes? Start from the outermost encoding and work inward.

4. **Stuck analysis**. If a layer resists all attacks from the current cipher hypothesis, step back and reconsider:
   - Is the effective key length longer than assumed? (cascade with coprime key lengths)
   - Is the ciphertext incomplete or truncated?
   - Is there a compression or encoding step between cipher layers?
   - Is the challenge using an unconventional alphabet or character set?
   - Record the negative results and the hypothesis space already explored. Move to the secondary hypothesis from Phase 2.

## Decision points

- **Stop on readable flag**: when the plaintext contains the competition flag format (e.g., `CTF{...}`, `flag{...}`, `hack{...}`), the challenge is solved. Record the flag hash in evidence (never the raw flag value in unredacted form). Proceed to report handoff.
- **Stop on confirmed plaintext**: even if the flag format is not recognized, if the output is grammatical English (or the expected plaintext language) and conveys coherent meaning, the decryption is correct. Record the plaintext hash and the recovered key.
- **Escalate to modern crypto skill**: if IC is near random, XOR with long key fails, the Hamming distance method returns no clear minimum, and entropy is near 8.0 bits per byte, the cipher is likely modern (AES, RSA, ECC, stream cipher). Hand off to the `ctf-crypto-modern` skill with the working evidence log.
- **Escalate to reverse engineering**: if the challenge provides a binary that performs encryption or a custom algorithm implementation, reverse the binary to extract the algorithm logic and key material. Hand off to the `ctf-reverse` skill.
- **Downgrade to educated guess**: if the ciphertext is very short (fewer than 20 characters), statistical methods are unreliable. Use the challenge title, description, category, and any hints to guess the cipher type. Try common CTF ciphers in order: ROT13, base64, Atbash, Caesar, Vigenere with common keys.
- **Downgrade to dictionary/keyword brute-force**: if the cipher type is confirmed but the key is short and likely a dictionary word, use a wordlist-based brute-force rather than analytical recovery. Use `pentest_agent_build_command` to construct a brute-force invocation through hashcat or john with a dictionary file.
- **Ask for challenge hint**: if three distinct attack approaches fail on a confirmed cipher type, the challenge may have an unconventional twist. Review the challenge description for overlooked constraints, hidden clues, or steganographic elements before continuing.

## Prohibited behavior

- Applying cryptanalysis to real communications, production traffic, intercepted messages, or any material outside authorized CTF competition scope.
- Attacking other teams' challenge instances, scoreboards, or infrastructure.
- Submitting flags or solutions to the competition platform in an automated fashion that bypasses rate limits or manual-verification gates.
- Sharing challenge solutions, flags, or detailed writeups publicly during an active competition (violates most CTF rules and may disqualify the team).
- Using online solver services (quipqiup, dCode, CyberChef web) for challenges where competition rules prohibit external network access or third-party services.
- Submitting challenge ciphertext to external API services that may log, store, or expose challenge material to other competitors.
- Brute-forcing remote challenge services at high rates. Limit interactive queries to rates that do not overload competition infrastructure.
- Using recovered keys, flags, or credentials from one challenge to access other challenges, team accounts, or non-challenge infrastructure.
- Copying challenge material, solutions, or keys into public repositories, chat logs, or shared documents accessible outside the authorized team.

## Stop conditions

- Flag recovered and validated against the competition platform (if interactive submission is allowed and in scope). Stop further cryptanalysis on this challenge artifact.
- Challenge time window expired. Complete any partial evidence logs and hand off to the CTF report skill.
- Competition rules prohibit further online interaction (network isolation phase). Switch to offline-only analysis.
- Ciphertext is provably too short for reliable statistical analysis (fewer than 8 characters) and no crib or hint is available. Record the dead end and the attempted methods.
- Three distinct, well-documented attack approaches have failed, and no secondary hypothesis remains. The skill has exhausted its analytical toolkit for this artifact. Escalate to a broader CTF workflow review or request a challenge hint.
- Challenge server becomes unresponsive or returns error states indicating infrastructure issues beyond the participant's control. Stop interactive queries; preserve the partial evidence log.

## Evidence

Record each step with `pentest_agent_append_evidence` using the following structured format:

```text
Challenge: <competition-name>/<challenge-name>
Artifact hash (SHA-256): <64-char hex digest>
Timestamp: <ISO 8601>

Phase 1 — Intake:
  File size: <bytes>
  Observed character set: <hex | base64 | base32 | decimal | binary | printable ASCII>
  Encoding layers detected: <count, list>
  Raw ciphertext entropy: <Shannon entropy, bits per byte>
  Effective alphabet size: <count distinct bytes>

Phase 2 — Fingerprinting:
  Index of Coincidence: <value, 4 decimal places>
  Chi-squared vs English: <value>
  Kasiski trigram repetitions: <count, list distances>
  Top candidate key length(s): <list, with IC-per-column values>
  Primary hypothesis: <cipher type, confidence 0.0-1.0>
  Secondary hypothesis: <cipher type, confidence 0.0-1.0>

Phase N — Attack:
  Cipher type targeted: <name>
  Method: <description of approach>
  Tool(s) used: <CyberChef operation "XOR Brute Force" | Python cryptanalysis script via pentest_agent_execute_tool | ...>
  Key recovered: <redacted — record SHA-256 of key instead of key value>
  Plaintext hash (SHA-256): <64-char hex digest>
  Flag status: <recovered | not present | partial>

Decision: <stop | escalate to ctf-crypto-modern | escalate to ctf-reverse | downgrade | request hint>
```

Never store in evidence: raw flag values, challenge solutions in plaintext, encryption keys, credentials, team tokens, session cookies, competition platform API keys, unredacted plaintext (beyond hash), or any data from challenges outside the authorized scope.

## Report handoff

When the challenge is solved or the analysis reaches a stopping point:

1. Use `pentest_agent_record_finding` for each recovered key and flag. Record the finding type as `ctf-crypto-classic-key-recovery` or `ctf-crypto-classic-flag-capture`. Include:
   - Challenge identifier (competition, challenge name).
   - Cipher type(s) identified.
   - Attack method summary (3-5 sentences describing the successful technique).
   - Key length (if applicable) and key hash.
   - Flag hash (SHA-256 of the flag value).
   - Confidence: confirmed (flag validated) / likely (plaintext is English but flag format not yet recognized) / partial (key recovered but plaintext has errors).

2. If the challenge requires a writeup submission (common in academic CTF courses or defense challenges), use the `report-ctf` skill to produce a structured writeup. Provide the evidence log as input. The writeup should describe the cipher identification process, the attack methodology, the tools used, and the recovered key/flag (hashed per competition rules).

3. If the analysis failed to recover the key or flag, record a negative finding with:
   - All hypotheses tested and methods attempted.
   - Evidence that rules out each tested hypothesis.
   - Any remaining untested hypotheses and the reason they were not tested (time limit, tooling gap, insufficient crib).
   - Recommendation for next steps (escalate to different skill, request hint, allocate more compute time).

4. For multi-challenge CTF engagements: cross-reference the evidence log with other challenge findings. A recovered key from one challenge may be a hint, crib, or parameter for another. Note any such connections in the evidence.

5. Clean up local working artifacts: delete temporary decoded files, intermediate ciphertext copies, and plaintext outputs from the working directory. Preserve only the evidence log and finding records.
