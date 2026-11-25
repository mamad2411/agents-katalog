---
name: file-access-scan
description: File upload and file read surface — type by magic bytes, size caps, storage outside webroot, served content-type, SVG/HTML/polyglot, archive extraction (zip-slip), path traversal and LFI on every read/download, symlinks, and download IDOR.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: file-access-scan

## Premise

Files cross the trust boundary in two directions, and both are attacker-steered. **Inbound**, a user chooses the bytes, the name, the declared type and the size of something the server will store, process, unpack and serve back. **Outbound**, a user chooses — through a path, a name or an id — *which* file the server reads. One wrong line on either side is code execution (an executable upload, an unpacked archive overwriting a loaded file), arbitrary file read (`../../.env`), stored XSS on the app's own origin, or another user's documents.

This skill is the **executor** behind contracts that otherwise stay prose: the file-upload MUST and the path-canonicalization MUST in `rules/security-principles.md`, `@security-auditor`'s A01 path-traversal bullet, the "security-specific upload risks" that `ssrf-scan § Upload egress note` names (SVG, polyglot, native-parser CVEs), and — when the backend pack is installed — the eight detectors of `backend/ai-patterns/file-upload.md § Detectors (cite-or-halt)`. Their mapping here: its 1 + 3 → §2, 2 → §1, 4 → §4, 5 → §3, 6 → §8, 8 → §9. Its 7 (orphaned presigned objects) is a cost and operations defect, not a hole, and stays with that pattern. Without the backend pack, the BAD/GOOD blocks below are the whole contract and the run says so in its header.

**Every finding cites the sink at `<file:line>` + the tainted source or the failing condition + the concrete fix + a severity.** A grep hit is never a finding by itself: it becomes one after a read of the enclosing function establishes the path from the untrusted input to the sink, and the absence of a guard on that path.

## Adapt to the codebase

Detect the upload parser, the read sinks and the path primitive in use, and phrase every fix in them. **Print the lanes you ran in the output header**; a stack present in the repo whose lane was not run is a `blocked` row in the class coverage block, never a silent pass.

**Upload lane** — where the caps live, what the client controls, what sniffs the bytes:

| Stack | Parser + where its caps live | Client-controlled (never the decision) | Magic-byte sniff |
|---|---|---|---|
| **Node/TS** (Express, NestJS, Fastify) | `multer({ limits: { fileSize, files, fields, parts } })`; `busboy` / `formidable` `limits` / `maxFileSize` / `maxFiles`; `@fastify/multipart` `limits: { fileSize, files, fields, fieldSize, parts, headerPairs }` — busboy's defaults leave `fields` / `parts` effectively uncapped; NestJS `FileInterceptor(…, { limits })` + `ParseFilePipe` `MaxFileSizeValidator`; body-parser `limit`. NestJS on Fastify has no `@nestjs/platform-express` `FileInterceptor`, so apps hand-roll one: find the project's interceptor and read its `req.file()` / `req.parts()` call | `file.mimetype`, `file.originalname` | `file-type` (`fileTypeFromBuffer`); a hand-written signature table (`0x89 0x50 0x4E 0x47`, `%PDF-`) is a sniff too — read it; NestJS `FileTypeValidator` only where the installed `@nestjs/common` sniffs bytes — older majors compare `file.mimetype`, the client header |
| **Python** (Django, FastAPI/Starlette, Flask) | Django `DATA_UPLOAD_MAX_NUMBER_FILES` (count) — no per-file byte cap, check `f.size` in the form/serializer; `FILE_UPLOAD_MAX_MEMORY_SIZE` is a spill-to-disk threshold, **not** a cap; Starlette `request.form(max_files=, max_fields=)`, no byte cap — edge or a counted stream; Flask `MAX_CONTENT_LENGTH` | `f.content_type`, `UploadFile.filename`, `FileStorage.filename` | `python-magic` (`magic.from_buffer`), `filetype`, `puremagic` |
| **Go** (net/http, Gin, Echo, chi) | `http.MaxBytesReader(w, r.Body, N)`; `ParseMultipartForm(maxMemory)` is a memory threshold, **not** a cap — the rest spills to temp files | `FileHeader.Header.Get("Content-Type")`, `FileHeader.Filename` | `http.DetectContentType(first512)` |
| **Java/Kotlin** (Spring) | `spring.servlet.multipart.max-file-size` / `max-request-size` (defaults 1MB / 10MB — the finding is `-1` or an unexplained raise); `@MultipartConfig` | `getContentType()`, `getOriginalFilename()` | Apache Tika `tika.detect(stream)` |
| **Ruby/Rails** | Rack has no body cap — edge; `Rack::Utils.multipart_part_limit` (parts); CarrierWave `size_range`; Shrine `validate_max_size`; Active Storage ships no validation — a model validator or `active_storage_validations` | form `content_type`, `original_filename` | `Marcel::MimeType.for(io)`; Shrine `determine_mime_type` |
| **PHP/Laravel** | php.ini `upload_max_filesize`, `post_max_size`, `max_file_uploads`; Laravel `'file' => 'max:<KB>'` | `$_FILES[…]['type']`, `getClientMimeType()`, `getClientOriginalExtension()`, `getClientOriginalName()` | `finfo_file(finfo_open(FILEINFO_MIME_TYPE), $tmp)`; Laravel `mimes:` / `mimetypes:` rules read the content |
| **.NET** (ASP.NET Core) | Kestrel `MaxRequestBodySize`, `FormOptions.MultipartBodyLengthLimit`, `[RequestSizeLimit]`, `[RequestFormLimits]`; IIS `maxAllowedContentLength` | `IFormFile.ContentType`, `IFormFile.FileName` | a signature table on the first bytes (no built-in sniffer) |
| **Edge** (any stack) | nginx `client_max_body_size`, ingress `proxy-body-size`, API-gateway payload limit — the outer cap; the rest of that config is `iac-scan`'s | — | — |

**Read lane** — the sinks, the one primitive that makes a user path safe, and the archive APIs:

| Stack | Read / serve sinks | Safe-path primitive (resolve, then assert inside root) | Archive extraction |
|---|---|---|---|
| **Node/TS** | `res.sendFile`, `res.download`, `fs.readFile` / `createReadStream` / `open`, `reply.sendFile`, Fastify `reply.send(stream)` / `res.type(t).send(object.stream)`, NestJS `StreamableFile(createReadStream(p))`, an object-store wrapper's `open(key)` | `abs = path.resolve(ROOT, p)`; `abs.startsWith(ROOT + path.sep)`; `fs.realpath` + re-assert for links. `res.sendFile(name, { root: ROOT })` rejects `..` itself | `adm-zip`, `unzipper`, `yauzl`, `extract-zip`, `decompress`, `tar` / `tar-fs` |
| **Python** | `open`, `send_file`, `FileResponse`, `Path.read_bytes` / `read_text`, `StaticFiles` | `(ROOT / p).resolve().is_relative_to(ROOT)` (ROOT pre-resolved, 3.9+); `werkzeug.utils.safe_join`; `flask.send_from_directory`. `secure_filename` is for names, not paths | `zipfile.extractall`, `tarfile.extractall` (`filter="data"`: 3.12+, backported to 3.8.17 / 3.9.17 / 3.10.12 / 3.11.4), `shutil.unpack_archive` |
| **Go** | `os.Open`, `os.ReadFile`, `http.ServeFile(w, r, name)` (guards `r.URL.Path`, **not** `name`), Gin `c.File` / `c.FileAttachment` | `os.OpenRoot(ROOT)` + `root.Open(p)` (Go 1.24+, also refuses link escapes); else `filepath.IsLocal(p)` before `filepath.Join` | `archive/zip`, `archive/tar` — manual loops; guard each name with `filepath.IsLocal` |
| **Java/Kotlin** | `Files.readAllBytes` / `newInputStream` / `copy`, `new File(base, p)`, `FileSystemResource`, `UrlResource` | `p = base.resolve(user).normalize(); p.startsWith(base)`; then `toRealPath()` re-check | `ZipInputStream`, `ZipFile`, Commons Compress `ArchiveInputStream` |
| **Ruby/Rails** | `send_file`, `File.read` / `open` / `binread`, `IO.read`, `render file:` | `abs = File.expand_path(p, ROOT); abs.start_with?(ROOT + File::SEPARATOR)`; `File.realpath` for links | `Zip::File` (rubyzip), `Gem::Package::TarReader`, `minitar` |
| **PHP/Laravel** | `include` / `require` (LFI → RCE), `file_get_contents`, `readfile`, `fopen`, `Storage::download`, `response()->download` / `->file` | `$real = realpath($root.'/'.$p); $real !== false && str_starts_with($real, $rootReal . DIRECTORY_SEPARATOR)` | `ZipArchive::extractTo`, `PharData` |
| **.NET** | `PhysicalFile`, `File.ReadAllBytes` / `OpenRead`, `new FileStream` | `full = Path.GetFullPath(Path.Combine(root, p)); full.StartsWith(rootFull + Path.DirectorySeparatorChar, StringComparison.Ordinal)` | `ZipFile.ExtractToDirectory` (guards); a manual `entry.ExtractToFile(Path.Combine(dest, entry.FullName))` loop (does not) |

## Pre-flight greps

Run these first, from the repo root — they produce the candidate set the detectors judge. `rg` is assumed; set the exclusion array once per shell (bash or zsh) and every command carries it. Each command names `.` explicitly because `rg` reads stdin instead of the tree when stdin is not a terminal, as in most agent harnesses. Where a comment says **minus**, the second line lists the guard: files in the first result and absent from the second are the candidates.

```bash
# Not sinks: vendored/built code, docs, lockfiles, tests/mocks/snapshots, tooling scripts, i18n catalogs and
# Refract's own trees (ai/ audits and design canvases, .claude/). Drop a glob only when the app serves or runs from it.
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/.git/**' -g '!**/*.min.js'
   -g '!**/*.{md,mdx,lock,snap}' -g '!**/*-lock.{json,yaml}' -g '!**/{test,tests,__tests__,__mocks__,__snapshots__,e2e,scripts}/**'
   -g '!**/*.{spec,test,mock}.*' -g '!**/*.e2e-spec.*' -g '!**/{i18n,locales}/**' -g '!ai/**' -g '!.claude/**')

# 1. Upload entry points — the upload universe (§1–§10 judge these files). Project-named interceptors
#    (`AppFileInterceptor`), Fastify `req.file()/parts()`, and JSON/base64 bodies (`data:<mime>;base64,`) count.
rg -n --pcre2 '\b(multer|busboy|formidable|fastify/multipart|\w*FileInterceptor|\w*FilesInterceptor|UploadedFiles?|UploadFile|FormFile|MultipartForm|ParseMultipartForm|MultipartFile|IFormFile|has_(one|many)_attached|mount_uploader|Shrine|hasFile|getClientOriginalName)\b|request\.(FILES|files)\b|@RequestPart|\$_FILES|\b(request|req)\.(file|files|parts|saveRequestFiles)\(|Buffer\.from\([^\n]*,\s*["\x27]base64["\x27]|\bb64decode\(|Base64\.getDecoder|\bdata:[^"\x27\s]*;base64' "${X[@]}" .

# 2. Type decided from the client (§1) — minus files that sniff bytes (a library, or a hand-written magic table).
rg -n --pcre2 '\.(mimetype|content_type|ContentType)\b|\b(getContentType|getClientMimeType|getClientOriginalExtension)\s*\(|Header\.Get\("Content-Type"\)|\$_FILES[^\n]*\[["\x27]type["\x27]\]' "${X[@]}" .
rg -l --pcre2 '\b(fileTypeFromBuffer|fileTypeFromFile|fileTypeFromStream|from_buffer|filetype\.guess|puremagic|DetectContentType|Tika|finfo_open|finfo_file|mime_content_type|determine_mime_type)\b|Marcel::MimeType|["\x27](file-type|magic-bytes\.js)["\x27]|0x89\s*,\s*0x50\s*,\s*0x4[eE]\s*,\s*0x47|0x25\s*,\s*0x50\s*,\s*0x44\s*,\s*0x46|0x[fF]{2}\s*,\s*0x[dD]8\s*,\s*0x[fF]{2}|["\x27](%PDF-|GIF8|ftyp)|\\x89PNG|\b(detect|sniff)\w*(Image|Mime|Type|Pdf|Signature)\b' "${X[@]}" .

# 3. Size and count caps (§2) — each upload route in grep 1 needs one on its path. Pagination `limit: 20` is not one.
rg -n --hidden --pcre2 '\b(fileSize|maxFileSize|maxFiles|maxTotalFileSize|MAX_CONTENT_LENGTH|MAX_FORM_MEMORY_SIZE|MAX_FORM_PARTS|DATA_UPLOAD_MAX_MEMORY_SIZE|DATA_UPLOAD_MAX_NUMBER_FILES|FILE_UPLOAD_MAX_MEMORY_SIZE|max_files|max_part_size|MaxBytesReader|ParseMultipartForm|MaxRequestBodySize|MultipartBodyLengthLimit|RequestSizeLimit|RequestFormLimits|maxAllowedContentLength|client_max_body_size|upload_max_filesize|post_max_size|max_file_uploads|multipart_part_limit|size_range|validate_max_size|bodyLimit|MaxFileSizeValidator|fieldSize|headerPairs)\b|\blimits\s*:\s*\{(?!\s*(cpu|memory|ephemeral))|max-(file|request)-size|proxy-body-size|\blimit\s*:\s*["\x27]\d+\s*[kmg]?b\b|["\x27|]max:\d' "${X[@]}" .

# 4. Where uploads land (§3, §4, §10) — every write CALL, wrappers included (`storage.put(`, `stores.public.put(`) —
#    and the client name reaching a path. Read the second line's hits into the first's calls. Browser code is out of
#    the write grep: a client `uploadFile()` hands bytes to the server's door, which is the line to read.
rg -n --pcre2 '\b(new\s+PutObjectCommand|(Put|Upload)Object\w*|put_object|upload_fileobj|upload(Data|Stream|File)|storeAs|storePublicly\w*|putFileAs|move_uploaded_file|transferTo|SaveUploadedFile|CopyToAsync|writeFile|writeFileSync|createWriteStream|os\.Create)\s*\(|\b(upload_to|MEDIA_ROOT|store_dir)\b|->(store|storeAs|storePublicly)\(|\b(dest|destination)\s*:\s*(["\x27\x60]|[^,}\n]*\b(upload|dir|path|tmp|storage|root)\w*)|\b\w*([Ss]torage|[Ss]tores?|[Bb]ucket|[Dd]isk|[Ss]3|[Bb]lob)\w*(\.\w+)?\.(put|upload|save|store|write)(Object|File|Stream|As)?\s*\(' "${X[@]}" -g '!**/*.{tsx,jsx,vue,svelte}' -g '!**/{web,frontend,client}/src/**' .
rg -n --pcre2 '\b(originalname|originalName|original_filename|getOriginalFilename|getClientOriginalName|FileName|Filename)\b|\b(file|f|upload|uploaded_file|image|avatar|attachment)\.filename\b|\$_FILES[^\n]*\[["\x27]name["\x27]\]' "${X[@]}" .

# 5. Uploads under a webroot / app origin (§3) — and the serving headers that would contain them.
rg -n --pcre2 '(public|static|wwwroot|webroot|htdocs|public_html|assets)/(uploads?|files|media|attachments|avatars)\b|["\x27](public|static|wwwroot|webroot|htdocs|public_html)["\x27]\s*,\s*["\x27](uploads?|files|media|attachments|avatars)["\x27]|useStaticAssets\(|static\(\s*settings\.MEDIA_URL|storage:link|\bpublic_path\(|express\.static\([^)]*(upload|media|files)|StaticFiles\([^)]*(upload|media)' "${X[@]}" .
rg -n -i --pcre2 'nosniff|content-disposition|as_attachment|res\.attachment|ResponseContentDisposition|attachment;|sandbox' "${X[@]}" .

# 6. Extension handling (§5) — first-segment / client extension, deny-lists, SVG/HTML accepted, handler re-wiring.
#    6a splits a NAME, never a decimal (`String(v).split('.')[1]`) or a JWT (`token.split('.')[1]`).
rg -n --pcre2 '\b\w*([Nn]ame|[Ff]ile|[Pp]ath|[Uu]pload|[Kk]ey)\w*(\(\))?\.split\(\s*["\x27]\.["\x27]\s*\)\s*(\[\s*1\s*\]|\.pop\(\))|\b(extname|splitext|getExtension|getClientOriginalExtension|pathinfo)\s*\(|filepath\.Ext\(|File\.extname\(' "${X[@]}" .
rg -n -i --pcre2 '\b(black_?list|block_?list|deny_?list|forbidden|disallowed|blocked)\w*\s*[:=][^\n]*\b(php|exe|jsp|sh|bat|js|html?)\b|image/svg\+xml|["\x27]\.?(svg|html?|phtml|phar|php\d?|jspx?|aspx?)["\x27]' "${X[@]}" .
rg -n --hidden 'AddHandler|SetHandler|AddType|php_flag\s+engine' -g '.htaccess' -g '*.conf' -g 'web.config' "${X[@]}" .

# 7. Archive extraction (§6) — minus files that resolve and assert each entry.
rg -n --pcre2 '\b(AdmZip|adm-zip|extractAllTo|extractEntryTo|unzipper|yauzl|extract-zip|decompress|tar-fs|zipfile\.ZipFile|tarfile\.open|extractall|unpack_archive|zip\.OpenReader|zip\.NewReader|tar\.NewReader|ZipInputStream|getNextEntry|ArchiveInputStream|getNextTarEntry|TarReader|Minitar|ZipArchive|extractTo|PharData|ExtractToDirectory|ExtractToFile)\b|Zip::File|\btar\.(x|extract)\s*\(' "${X[@]}" .
rg -l --pcre2 '\b(getCanonicalPath|toRealPath|realpath|IsLocal|is_relative_to|commonpath)\b|filter\s*=\s*["\x27](data|tar)["\x27]|startsWith\([^)]*\b(dest|target|out|root)' "${X[@]}" .

# 8. Image / document / media processors (§7) — imported or shelled out, not the English word — and the guards switched off.
#    A binary name counts as a spawn's first argument or a command string with arguments (`'convert -resize …'`), never a
#    bare `'convert'` tab key.
rg -n --pcre2 '\b(imagemagick|ImageMagick|MiniMagick|mini_magick|image_processing|Imagick|Wand|pyvips|ghostscript|Ghostscript|pdf2image|pdftoppm|pdftocairo|libreoffice|soffice|unoconv|ffmpeg|fluent-ffmpeg|ffprobe|wkhtmltopdf|wkhtmltoimage|exiftool|Thumbnailator|ImageIO|PDFBox|pdf-parse|pypdf|PyPDF2|pdfminer)\b|(\bfrom\s+|require\(\s*)["\x27](sharp|gm|jimp)["\x27]|\b(spawn|execFile|exec|execa|spawnSync|execFileSync|execSync|Popen|run|call|check_output|Command)\w*\(\s*\[?\s*["\x27\x60](convert|magick|identify|mogrify|montage|gs|cwebp|ffmpeg|soffice)["\x27\x60\s]|["\x27\x60](convert|magick|identify|mogrify|montage|gs|cwebp|ffmpeg|soffice)\s+[-\w$"\x27{]|Image\.open\(|Intervention\\Image' "${X[@]}" .
rg -n --hidden --pcre2 'policy domain=|-dNOSAFER|protocol_whitelist|MAX_IMAGE_PIXELS\s*=\s*None|limitInputPixels\s*:\s*(false|0)\b' "${X[@]}" .

# 9. Malware scanning (§8) — zero hits on a repo that re-serves uploads to other users IS the finding. A hand-rolled
#    `quarantined → available` state on the file row counts: read the upload record's status enum, not a keyword.
rg -n -i --pcre2 '\b(clamav|clamd|clamscan|node-clam|clamdjs|pyclamd|virustotal|malware|anti-?virus)\b|["\x27](av|virus|malware)[-_]?scan' "${X[@]}" .

# 10. Presigned URLs, their TTLs and conditions (§9, §15) — read the TTL line only when the first line hits (alone it is
#     every JWT `expiresIn`) — and public object ACLs (§10).
rg -n --pcre2 '\b(getSignedUrl|createPresignedPost|presignedPostPolicy|presignedPutObject|presignedGetObject|generate_presigned_url|generate_presigned_post|PresignPutObject|PresignGetObject|presignPutObject|presignGetObject|generatePresignedUrl|generateSignedUrl|generate_signed_url|generateSasUrl|generateBlobSASQueryParameters|generate_blob_sas|temporaryUrl|temporaryUploadUrl)\b' "${X[@]}" .
rg -n --pcre2 '\b(expiresIn|ExpiresIn|expires_in|signatureDuration|WithPresignExpires)\b[^\n]{0,40}\d|content-length-range|x-goog-content-length-range' "${X[@]}" .
rg -n -i --pcre2 'public-read|PublicRead|PUBLIC_READ|predefinedAcl|makePublic\(|allUsers|PublicAccess\w*\.(Blob|Container)|block_public_acls\s*=\s*false|BlockPublicAcls\s*:\s*false' "${X[@]}" .

# 10b. Public AREAS (§10): a policy granting everyone a prefix, a public bucket, and the app's own registry of public
#      prefixes / served roots. Every grep-4 writer that lands in one is a §10 candidate, whatever its ACL.
rg -n --hidden --pcre2 '"Principal"\s*:\s*(\{\s*"AWS"\s*:\s*)?"\*"|\ballUsers\b|allAuthenticatedUsers|storage\.buckets|\bgetPublicUrl\(|\bPUBLIC_\w*(PREFIX|BUCKET|AREA|ROOT|DIR)\b|\b\w*(area|prefix|folder|scope)\s*:\s*["\x27]public/|\bpublic(Path|BaseUrl|Url|Read)\s*:' "${X[@]}" .

# 10c. App-signed links (§15): an HMAC over a key + an expiry, and the URLs that carry `expires` + `sig`. Then grep
#      the signer's method name for its callers — every caller is a minter whose ownership predicate §14 reads.
rg -n --pcre2 '\b(createHmac|hmac\.new|hash_hmac|OpenSSL::HMAC|Mac\.getInstance|hmac\.New)\b[^\n]*\b(expir|ttl|until)|[?&](expires|exp|expiry|ttl)=[^\n]*[?&](sig|signature|hmac|token)=|[?&](sig|signature|hmac)=[^\n]*[?&](expires|exp|expiry)=' "${X[@]}" .

# 11. Every read sink, per lane — the read universe (§11, §12, §17). One line per stack in the repo. Node includes
#     Fastify's `reply.send(stream)` and object-store reads behind a wrapper (`stores.exports.open(row.filePath)`).
rg -n --pcre2 '\b(readFile|readFileSync|createReadStream|openSync)\s*\(|\bfs\.(promises\.)?open\s*\(|\.(sendFile|download)\s*\(|\bStreamableFile\s*\(|\.send\(\s*[\w.]*\bstream\b|\bnew\s+GetObjectCommand\b|\.(open|download|getObject|readStream|stream)\w*\(\s*[\w.]*\.(filePath|file_path|key|path|storageKey|objectKey)\s*[,)]' -t js -t ts "${X[@]}" .
rg -n --pcre2 '(?<![\w.])open\s*\(|\b(os|io|codecs)\.open\s*\(|\b(send_file|send_from_directory|FileResponse|safe_join)\s*\(|\.(read_text|read_bytes)\s*\(' -t py "${X[@]}" .
rg -n --pcre2 '\b(os\.(Open|OpenFile|ReadFile)|ioutil\.ReadFile|http\.ServeFile|http\.ServeContent|c\.(File|FileAttachment|Attachment|SendFile))\s*\(' -t go "${X[@]}" .
rg -n --pcre2 '\bFiles\.(readAllBytes|readString|newInputStream|newBufferedReader|copy|lines)\s*\(|\bnew\s+(File|FileInputStream|FileReader|FileSystemResource|UrlResource)\s*\(' -t java -t kotlin "${X[@]}" .
rg -n --pcre2 '\b(send_file|File\.(read|open|binread|readlines)|IO\.(read|binread|readlines))\b|\brender\s+file:' -t ruby "${X[@]}" .
rg -n --pcre2 '\b(include|include_once|require|require_once)\b\s*\(?\s*\$|\b(file_get_contents|readfile|fopen|file|fpassthru|highlight_file|parse_ini_file)\s*\(\s*\$|Storage::(get|download|readStream|response)\s*\(|response\(\)->(download|file)\s*\(' -t php "${X[@]}" .
rg -n --pcre2 '\b(PhysicalFile|File\.(ReadAllBytes|ReadAllText|OpenRead|Open))\s*\(|\bnew\s+FileStream\s*\(' -t cs "${X[@]}" .

# 12. Fast track for §11 — a request-derived value on the same line as a sink or a path build. Decorator frameworks
#     (NestJS, FastAPI) have no `req.query`: taint arrives as `@Query('name') name` or `dto.filePath` (second line).
rg -n --pcre2 '\b(sendFile|download|createReadStream|readFile|readFileSync|send_file|send_from_directory|FileResponse|open|ServeFile|ReadFile|readAllBytes|newInputStream|File|file_get_contents|readfile|fopen|include|require|PhysicalFile|ReadAllBytes|join|resolve|Combine|expand_path|get)\b\s*\(?[^\n;]*(\breq\.(params|query|body)|\brequest\.(args|GET|POST|query_params|path_params|form|params|getParameter)|\bparams\[|\$_(GET|POST|REQUEST|COOKIE)|\$request->(input|query|get|route)|\br\.URL\.Query|\bc\.(Param|Query|PostForm)|\bctx\.(params|query|request))' "${X[@]}" .
rg -n --pcre2 '@(Query|Param|Body)\(\s*["\x27](path|file|files|filename|fileName|name|key|filePath|file_path|dir|folder|document|attachment)["\x27]|\b(query|dto|body|params)\.(path|filePath|file_path|key|fileName|filename|dir|folder)\b' "${X[@]}" .

# 13. Safe-path primitives present (set difference against 11/12) — and the ..-stripping anti-pattern (itself a §11 finding).
rg -l --pcre2 '\b(path\.relative|realpath|realpathSync|is_relative_to|commonpath|safe_join|send_from_directory|IsLocal|OpenRoot|OpenInRoot|toRealPath|getCanonicalPath|GetFullPath|expand_path)\b|startsWith\([^)]*\bsep\b|\broot\s*:' "${X[@]}" .
rg -n --pcre2 '\b(replace|replaceAll|str_replace|gsub|sub|Replace|ReplaceAll)\s*\([^\n]*(\.\.[/\\]|\\\.\\\.|["\x27]\.\.["\x27])' "${X[@]}" .

# 14. Static mounts, listing, dotfiles, symlink policy, nginx alias (§12, §13) — and features that materialise a user-controlled tree (§12).
rg -n --hidden --pcre2 'express\.static\(|useStaticAssets\(|serve-static|serveStatic\(|serve-index|serveIndex\(|dotfiles\s*:|fastify/static|ServeStaticModule|StaticFiles\(|static_folder|static_url_path|http\.FileServer|http\.Dir\(|static-locations|addResourceLocations|public_file_server|UseStaticFiles|UseDirectoryBrowser|\bautoindex\s+on|disable_symlinks|FollowSymLinks|Options\s[^\n]*Indexes|follow_symlinks?\s*=\s*True' "${X[@]}" .
rg -n --pcre2 '\bgit\s+clone\b|["\x27]git["\x27]\s*,\s*\[?\s*["\x27]clone["\x27]|simple-git|nodegit|isomorphic-git|Repo\.clone_from|PlainClone|Git\.cloneRepository|Rugged::Repository\.clone' "${X[@]}" .
rg -n --hidden '\balias\s+[^\s;]+;|\bfile_server\b' -g '*.conf' -g '*nginx*' -g '*Caddyfile*' -g '*caddy*' "${X[@]}" .

# 15. File-shaped routes (path-, query- and body-keyed: `files/:id`, `@Get('files/private')?key=&sig=`,
#     `@Post('exports/signed-url') {filePath}`), storage reads keyed from the request or a wrapper, and DTO fields
#     through which the client hands a file key or URL back to be stored on a row (§14). 15c reads REQUEST schemas only
#     (response read models name the same fields) and any value type: a project helper (`trimmedText(512)`) is a string.
rg -n --pcre2 '["\x27`/](files?|attachments?|documents?|docs|downloads?|uploads?|media|exports?|invoices?|reports?|receipts?|avatars?|proofs?)/[:{<]\w*|@(Get|Post)\(\s*["\x27][^"\x27]*\b(files?|proof\w*|downloads?|signed-url|exports?|attachments?|media|documents?)\b[^"\x27]*["\x27]' "${X[@]}" .
rg -n --pcre2 '\b(getObject|GetObjectCommand|get_object|download_file|download_fileobj|GetObject|getBlobClient|download_blob|Storage::download)\b[^\n]*\b(req|request|params|query|body|key|id)\b|\bbucket\.file\([^)]*\b(req|request|params|query|body)\b|\.(open|download|getObject|stream)\w*\(\s*[\w.]*\.(filePath|file_path|key|path|storageKey)\s*[,)]' "${X[@]}" .
rg -n --pcre2 '\b(path|key|filePath|file_path|fileKey|storageKey|objectKey|fileUrl|\w*(Image|File|Receipt|Attachment|Proof|Scan|Document)(Url|Key|Path))\s*[!?]?\s*:\s*(?!(number|boolean|z\.(number|boolean|enum|array|object|literal|coerce\.number)\b|\w+(Int|Number|Bool|Enum|Id|Ids|Uuid)\w*\())[\w.$]' -g '*[dD]to*' -g '*{[Ii]nput,[Rr]equest,[Bb]ody,[Cc]ommand,[Pp]ayload}*' -g '*serializer*' -g '*forms.py' "${X[@]}" -g '!**/*.{tsx,jsx,vue,svelte}' -g '!**/{web,frontend,client}/src/**' .

# 16. Hand-built Content-Disposition (§16) — and file-sink errors echoed to the client (§17).
rg -n -i --pcre2 'content-disposition[^\n]*filename\s*=[^\n]*(\$\{|["\x27`]\s*\+|%s|\{\w+\}|#\{|\.\s*\$|Sprintf|format\()' "${X[@]}" .
rg -l -0 --pcre2 'sendFile|createReadStream|readFile|send_file|FileResponse|os\.Open|ServeFile|readAllBytes|file_get_contents|readfile|PhysicalFile' "${X[@]}" . \
  | xargs -0 -r rg -n --pcre2 '\b(err|error|e|ex|exc)\.(message|getMessage\(\)|Error\(\))|\bstr\(\s*(e|err|exc)\s*\)|ENOENT|FileNotFoundError|NoSuchFileException'
```

A finding is a grep hit **plus** a read of the enclosing function. The greps narrow; they do not decide. Trace each argument backward to its source — a route param, query, body, header, cookie, multipart field, or a **stored** value a user once supplied (the original filename saved at upload, a `path` column). Second-order taint is the shape same-line greps miss, which is why grep 11 is the work list and grep 12 only its fast track. When `llm-trust-scan` ran first, its `completion-sources.txt` (§3s, `<file:line>` of every completion, tool-call argument and model message read) is a source list: trace each one forward to this skill's sinks, and grade the sink here (OH-5, path sinks — a model-chosen file name in a read or write tool); `llm-trust-scan` lists the count only.

Measured on a real repo (a NestJS-on-Fastify monorepo, about 13,000 tracked files) before and after the exclusion array and the call-shape rewrites: grep 4 went from 11,041 lines to 20, grep 3 from 638 to 22, grep 11 (Node) from 608 to 12, grep 8 from 35 to 0 and grep 9 from 24 to 0 — the dropped lines were docs, tests, lockfiles, tooling scripts, pagination `limit:`, the English word "sharp" and webhook "quarantine". Every seeded defect of the benchmark fixture is still hit.

Re-measured 2026-10-15 on a real NestJS + React monorepo: 4a went 19 → 15 (a Redis code store remains, the three browser `uploadFile` lines are gone), 6a 11 → 5 (the decimal-places and JWT-payload splits are gone), 8a 3 → 0 (a `'convert'` tab key), and 15c 41 → 16. The old 15c held 5 of the 10 file-reference request fields: the other 5 used project string helpers (`trimmedText(1024)`, `requiredText(400)`) that `z.string(` never matched, and they are now listed, while the 25 response-schema lines are gone. Fixtures: 4a 14 → 13 (a browser `XLSX.writeFile`), 8a 6 → 6, and the pre-flight output on `vuln-fullstack` is unchanged line for line.

## Scans for

Each detector names its candidate grep, the condition that turns a hit into a finding, its class and a default severity — raise or lower the severity by what the chain actually reaches, and say why in the finding.

**Upload side** — a file entering the system (§1–§10).

### 1. File type trusted from the client, not the bytes

```
BAD:   if (file.mimetype !== 'image/png') return res.status(415).end()     // Content-Type is whatever the client sent
       if (ALLOWED.includes(path.extname(file.originalname))) save(file)    // so is the name
GOOD:  const kind = await fileTypeFromBuffer(head)                          // sniff the leading bytes
       if (!kind || !ALLOWED_MIME.has(kind.mime)) return res.status(415).end()
       const ext = EXT_FOR[kind.mime]                                       // the stored extension comes from the sniff too
```
Candidates: grep 2, first line minus the files its second line lists. A finding when the accept/reject decision, the stored extension, or the `Content-Type` later served derives from the client value with no sniff on that path. A sniffer that runs *after* the file is already stored and reachable is still a finding. A hand-rolled signature table is a sniff: read which types it admits and how many bytes it checks. A sniff proves the leading bytes, not that the file is *only* that type — a GIF header over an HTML body is a polyglot — so §3's serving headers stay required after a correct sniff. **CWE-434 / CWE-646 · A06:2025 · medium** (high when §3 also fires: the type then decides what the browser executes).

### 2. No size cap at the parser, no count cap

```
BAD:   multer({ storage })                                    // no limits: unbounded fileSize, files, fields, parts
       r.ParseMultipartForm(32 << 20)                         // a memory threshold — the remainder spills to disk, uncapped
GOOD:  multer({ storage, limits: { fileSize: 10 * MB, files: 5, fields: 20, parts: 30 } })
       r.Body = http.MaxBytesReader(w, r.Body, 10<<20); r.ParseMultipartForm(1 << 20)
```
Candidates: grep 1 (handlers) against grep 3 (caps). For each upload route find the cap on its path — parser option, route decorator, framework setting, or the edge. A finding when none applies; when the value disables it (`client_max_body_size 0`, `max-file-size=-1`, `fileSize: Infinity`); or when the only "cap" is a threshold that is not one (Django `FILE_UPLOAD_MAX_MEMORY_SIZE`, Go's `ParseMultipartForm` argument). A byte cap with no file / part **count** cap is its own finding — ten thousand one-byte parts exhaust handles and temp files without crossing any byte limit. A size checked after `await file.arrayBuffer()` / `request.body()` / `.read()` has already been paid for: report it as no cap. Text fields count too: busboy accumulates them into the body outside any byte budget the app reserves for files. Severity input: Nest interceptors run after guards, so a multipart parsed in an interceptor is an authenticated-only DoS; a parser registered globally (Fastify `addContentTypeParser`, Express `app.use(multer…)`) is reachable before auth. **CWE-770 · A10:2025 (unbounded input) · API4:2023 · medium** (high when the body is buffered in memory and reachable unauthenticated).

### 3. Uploads stored under the webroot or served inline from the app origin

```
BAD:   multer({ dest: 'public/uploads' }); app.use(express.static('public'))   // /uploads/x.svg runs script on the app origin
       return send_file(path, mimetype=upload.content_type)                     // inline, with the client's type
GOOD:  private bucket / dir outside any static root; serve through a handler or a separate user-content origin with
       Content-Type: <validated type> · Content-Disposition: attachment · X-Content-Type-Options: nosniff
       · Content-Security-Policy: sandbox  (for any type rendered inline)
```
Candidates: grep 4 first line (where uploads land) and grep 5 (webroot paths; the hardening headers). A finding when a user file is reachable from the app's own origin — a static mount over the upload dir, `MEDIA_URL` served by the app or its host, `storage:link`, CarrierWave's default `public/uploads` — **and** the response lacks `nosniff` + `attachment` (or a `sandbox` CSP for inline types). HTML, SVG, XML or PDF there is stored XSS with the app's cookies and origin; under a server that interprets files (PHP-FPM, JSP, CGI, a writable `.htaccess`) it is code execution. A subdomain of the app is **not** a separate origin for cookies scoped to the parent domain — user content needs its own registrable domain. **CWE-434 / CWE-79 · A05:2025 · high** (critical when the server executes the stored file).

### 4. Client filename in the storage path

```
BAD:   filename: (req, file, cb) => cb(null, file.originalname)      // ../../app/server.js, or another user's invoice.pdf
       f.save(os.path.join(UPLOAD_DIR, f.filename))
       $file->storeAs('docs', $file->getClientOriginalName())
GOOD:  key = `${uuid()}.${EXT_FOR[sniffedMime]}`     // generated key; the display name lives in a DB column, never the path
```
Candidates: grep 4 second line (client-name reads) traced into a write or path build from its first line. A finding when any part of the client filename reaches the on-disk path or object key. Traversal is the loud half; **overwrite** is the quiet one — two users uploading `invoice.pdf` to one prefix, or a name chosen to collide with another tenant's object. Several runtimes base-name the client name before the app sees it (multer / busboy unless `preservePath: true`, PHP `$_FILES[…]['name']`, Symfony `UploadedFile`, Go ≥ 1.17 multipart `FileName()`): traversal is then closed, overwrite and the attacker-chosen extension are not — downgrade, do not drop. `secure_filename` / `basename` alone closes traversal and leaves overwrite. **CWE-22 / CWE-73 · A01:2025 · high** (medium where the runtime base-names it).

### 5. Executable or active-content extensions accepted; double-extension tricks

```
BAD:   const ext = file.originalname.split('.')[1]      // "a.jpg.php" → "jpg" passes; the server runs .php
       if (!['exe', 'sh'].includes(ext)) save(file)    // deny-list: .phtml .phar .php5 .jspx .svg .htaccess all pass
GOOD:  ext = EXT_FOR[sniffedMime]                       // allow-list keyed by the sniffed type; the client extension is discarded
```
Candidates: grep 6. A finding when the stored extension comes from the client (first or last segment), when the check is a deny-list, or when the allow-list admits active content without §3's headers: `.php .phtml .phar .php5 .pht .jsp .jspx .asp .aspx .ashx .cer .shtml .cgi .pl .html .htm .xhtml .svg .xml .js .mjs .swf`. Configuration files execute too: an uploaded `.htaccess` or `web.config` re-wires the handler for its whole directory, and grep 6's third line finds the `AddHandler` / `SetHandler` that make `x.php.jpg` run under Apache `mod_mime`. Check case (`.PhP`), a trailing dot or space (`shell.php.` on Windows) and NTFS `::$DATA`. **CWE-434 · A06:2025 · high** (critical when the upload dir is executable).

### 6. Archive extraction without a zip-slip guard or bomb caps

```
BAD:   while ((e = zis.getNextEntry()) != null)
         Files.copy(zis, new File(dest, e.getName()).toPath())     // "../../etc/cron.d/x" lands outside dest
       tarfile.open(upload).extractall(dest)                       // no filter: traversal, absolute paths, links, devices
GOOD:  Path out = destDir.resolve(e.getName()).normalize();
       if (!out.startsWith(destDir)) throw new SecurityException(e.getName());   // per entry, before a byte is written
       tar.extractall(dest, filter="data")                         // Python 3.12+; 3.14 makes it the default
       + caps: entries ≤ N, total uncompressed ≤ M bytes, counted while streaming — never the header's declared size
```
Candidates: grep 7, first line minus the files its second line lists. A finding when an entry name reaches a path with no resolve-and-assert; when symlink or hardlink entries are honoured (a link entry, then a file written *through* it, escapes any name check — reject link types or extract with `filter="data"` / `os.Root`); or when nothing caps entry count and uncompressed bytes (a 42 KB zip expands to petabytes). `adm-zip`, `unzipper`, `node-tar`, `rubyzip` and PHP `ZipArchive` all shipped zip-slip or link-escape fixes in past releases — hand the resolved version to `deps-audit` rather than asserting a CVE here; a manual `path.join(dest, entry.path)` around a patched library reopens the hole at any version. **CWE-22 (zip slip) / CWE-409 (bomb) · A01:2025 / A10:2025 · high** (critical when an overwritten file is later executed or loaded).

### 7. Image, document and media processors fed untrusted files

```
BAD:   sharp(upload, { limitInputPixels: false })       // pixel flood: a 5 KB PNG declaring 100k × 100k
       Image.MAX_IMAGE_PIXELS = None                    // Pillow's decompression-bomb guard switched off
       spawn('convert', [tmp, 'out.png'])               // ImageMagick on every coder it ships, no policy.xml
GOOD:  keep the pixel limits; ImageMagick policy.xml denies MVG, MSL, EPHEMERAL, URL, HTTPS, TEXT, PS, EPS, PDF, XPS
       unless needed and sets width/height/area/memory limits; force the sniffed format (`png:` prefix, ffmpeg `-f mp4`);
       run the processor in a worker with no network, a read-only FS and CPU / memory / time limits
```
Candidates: grep 8. These are large native parsers reading attacker bytes, and the class has a record: ImageTragick (CVE-2016-3714, command execution through MVG / delegates), ImageMagick file read via a PNG text chunk (CVE-2022-44268), Ghostscript pipe-device command execution reachable through ImageMagick's PS / EPS / PDF coders (CVE-2023-36664), ExifTool DjVu metadata RCE (CVE-2021-22204), the libwebp heap overflow exploited in the wild (CVE-2023-4863), and ffmpeg HLS / `concat` playlists embedded in a "video" that pull local files into the output. A finding when a guard is disabled (grep 8 second line); when ImageMagick / GraphicsMagick runs with no `policy.xml` restricting coders and resources; when the input format is auto-detected rather than forced to the sniffed type; or when the processor runs in the web process with network and filesystem reach (`[report-flagged]` — sandboxing is a design call). Boundaries: a filename interpolated into the processor's shell command is `injection-scan`'s; a coder or renderer that fetches URLs (ImageMagick `url:`, HLS segments, HTML-to-PDF) is `ssrf-scan`'s; the installed version against advisories is `deps-audit`'s. **CWE-400 (pixel flood) / CWE-1395 (vulnerable parser) · A02:2025 · high** with a guard off or no policy, medium when only the sandbox is missing.

### 8. No malware scan on files other users receive

Candidates: grep 9 (any scanner) against the share paths — attachments, shared documents, marketplace listings, support tickets: anything uploaded by one principal and downloaded by another, staff included. A finding when a user-supplied file is re-served to someone else and the pipeline holds no scan. The fix is a state, not a call: `quarantined → scanned → available` on the file record, a scan (ClamAV `clamd` over its socket, or the object store's malware-scanning service on object-created) before the transition, nothing served until `available`, and **fail closed** while the scanner is down. Always `[report-flagged]` — the fix is a pipeline and a column. **CWE-434 · A06:2025 · medium** (a design gap, not an exploit).

### 9. Presigned upload with no type / size condition, a client-chosen key, or a long expiry

```
BAD:   getSignedUrl(s3, new PutObjectCommand({ Bucket, Key: req.body.filename }), { expiresIn: 604800 })
GOOD:  createPresignedPost(s3, { Bucket, Key: `pending/${uuid()}`, Expires: 300,
         Conditions: [['content-length-range', 1, 10 * MB], ['eq', '$Content-Type', expectedType]] })
       // then confirm: read the object's first bytes server-side before it leaves pending/
```
Candidates: grep 10, first two lines. A presigned **PUT** cannot carry a size range — bind `ContentType` (and an exact `ContentLength` when known) into the signature, or use a presigned **POST** policy with `content-length-range`; GCS takes `x-goog-content-length-range` as a signed header; an Azure SAS has no size condition, so the confirm step is the only cap. A finding when there is no size condition and no confirm-time check; when `Content-Type` is unbound (the client PUTs `text/html` and the bucket serves it as that); when the key derives from client input (detector 8 of the backend `file-upload` pattern, when that pack is co-installed); or when the TTL outlives one upload (minutes, not the 7-day SigV4 maximum). **CWE-434 / CWE-770 · A06:2025 · medium** (high with a client-chosen key that can overwrite).

### 10. Private documents written where the public can read them — a public ACL, or a public area

```
BAD:   new PutObjectCommand({ Bucket, Key, Body, ACL: 'public-read' })     // every upload world-readable, forever
       this.storage.put(receiptScan, ext)    // `storage` is the PUBLIC store; a bucket policy grants `*` GetObject on public/*
GOOD:  private objects in a private area; access through §15's authorised, short-lived link or an authenticated handler
```
Candidates: grep 10 third line, and grep 10b crossed with grep 4's write calls. Two shapes:
- **(a) Per-object ACL.** Application code sets a public ACL, `makePublic()` or public container access on objects users upload.
- **(b) Public area.** The app sets no ACL. It picks an AREA — a prefix, a bucket, a disk root under a static mount — and a policy or mount makes that area public. The policy is correct as written and no write call says "public", so `iac-scan` and shape (a) both pass it. Resolve every grep-4 write to its store (registry key, DI token, bucket constant). For each one landing public, ask whether the file is a private document: an ID, a receipt, a signed form, an export, a support attachment. When an ADR or a reference system decides visibility (an older system's bucket `public` flag), compare with it. Cite the write call, with the policy line second.

Product intent public (an avatar, a logo) is not a finding — then confirm that area holds nothing else. A public object that outlives its deleted row is the same exposure. Random keys lower severity, never remove the finding: the URL leaks through logs, history, forwards and CDN logs, and a removed member keeps it. The bucket policy itself, Block Public Access and IaC ACLs stay `iac-scan`'s. Measured on a real repo: the one Finding of a whole-repo run was shape (b), a signed receipt scan written through the public store; no grep separated it until 4 + 10b listed the writer and the area. **CWE-732 / CWE-200 · A01:2025 · high** for private documents (medium with random keys and no public listing), low for intentionally public media.

**Read side** — a path, name or key from outside choosing what the server reads (§11–§17).

### 11. Path traversal / LFI on a read sink

```
BAD:   res.sendFile(path.join(FILES, req.query.name))              // ?name=../../.env
       return send_file(os.path.join(BASE, request.args["f"]))     // ?f=/etc/passwd — join discards BASE
       include $_GET['page'] . '.php';                             // LFI → RCE via log poisoning, php://filter, phar://
       safe = name.replace('../', '')                              // "....//" collapses back to "../"
GOOD:  const abs = path.resolve(FILES, name);
       if (!abs.startsWith(FILES + path.sep)) return res.sendStatus(404);
       res.sendFile(abs)                                           // or res.sendFile(name, { root: FILES })
       p = (BASE / name).resolve()                                 # BASE resolved once at startup
       if not p.is_relative_to(BASE): abort(404)
```
Candidates: grep 11 (every read sink, per lane) is the work list; grep 12 is its same-line fast track. A finding when a tainted value — including a stored, user-supplied one — reaches the sink and the path is not resolved and asserted inside the root on that path (grep 13's first line lists files holding a primitive; confirm it guards *this* sink). A hit on grep 13's second line is itself a finding: `....//`, `..%2f`, `..\`, an absolute path and encoded separators all survive `..`-stripping. The fix is always resolve-then-assert from the lane table — better still, take no path at all: map an opaque id to a server-held path. PHP `include` / `require` on a request-derived path is LFI with an RCE upgrade (log poisoning, `php://filter`; `phar://` deserialization is `injection-scan`'s class). **CWE-22 (CWE-98 for PHP include) · A01:2025 · high** (critical when reachable files hold credentials — `.env`, `/proc/self/environ`, key files — or the sink is `include`).

### 12. Symlinks followed out of the root

```
BAD:   const abs = path.resolve(ROOT, name); if (abs.startsWith(ROOT + sep)) fs.createReadStream(abs)
       // ROOT/u/123/link → /etc: the string check passes, open() follows the link
GOOD:  const real = await fs.realpath(abs); if (!real.startsWith(REAL_ROOT + sep)) deny()   // assert the target
       root, _ := os.OpenRoot(ROOT); f, err := root.Open(name)                             // Go 1.24+: refused at open time
```
Candidates: the §11 sinks that pass a lexical assert, plus §6 extraction and anything that materialises a user-controlled tree — grep 14's second line finds the clones (a user's repository installed as a theme or plugin), and a workspace sync is the same shape. A finding when a user can create a link inside a root the app later reads or serves and the read path asserts only the lexical path: a cloned `theme.json` that is a link to the signing key reads the key. `realpath`-then-`open` is still a race where the attacker can swap the link between the two calls — prefer open-time enforcement (`os.Root`, `openat2` with `RESOLVE_BENEATH`, `O_NOFOLLOW`) when the tree is attacker-writable. Static servers follow links by default (Go `http.Dir`, nginx without `disable_symlinks`, Apache `FollowSymLinks`); grep 14 finds them. **CWE-59 / CWE-61 · A01:2025 · high** when users can plant links, low otherwise.

### 13. Static file server mounted too wide

```
BAD:   app.use(express.static(__dirname))                         // serves .env, package.json, src/, .git/
       app.use(express.static('public', { dotfiles: 'allow' }))       // NestJS app.useStaticAssets(…) is the same mount
       http.Handle("/", http.FileServer(http.Dir(".")))            // dotfiles + links + listing
       location /static { alias /srv/app/static/; }                // "/static../" → /srv/app/ (off-by-slash)
GOOD:  mount only a build-output dir that holds nothing else; dotfiles denied; listing off
       location /static/ { alias /srv/app/static/; }               // trailing slash on both
```
Candidates: grep 14. A finding when the mounted dir is the project root, a parent of source / config / `.git`, or the upload dir (then also §3); when dotfiles are allowed, or served by default (Go `http.FileServer`, a bare nginx `root`); when directory listing is on (`serve-index`, `autoindex on`, `Options Indexes`, `UseDirectoryBrowser`); or when an nginx `alias` location lacks the trailing slash its `alias` carries. Django's `static()` / `DEBUG` serving in production and Flask `static_folder='.'` are the same shape. Boundary: `data-exposure-scan` inventories what *is* exposed (a reachable `.git/HEAD`, a `.bak`, a source map); this detector cites the mount that makes it reachable — one finding per `<file:line>`, cited by both. **CWE-538 / CWE-548 · A02:2025 · critical** when `.git` / `.env` / keys are reachable, medium otherwise.

### 14. Download IDOR — a file id or key from the request, no ownership check

```
BAD:   router.get('/files/:id', auth, async (req, res) => {
         const f = await File.findByPk(req.params.id); res.sendFile(f.path) })   // any signed-in user, any file
       s3.getObject({ Bucket, Key: req.query.key })                             // the key IS the authorization
GOOD:  const f = await File.findOne({ where: { id: req.params.id, ownerId: req.user.id } }); if (!f) return res.sendStatus(404)
       // or a policy call (can(user, 'read', f)) before the stream; the storage key is never read from the request
```
Candidates: grep 15 (file-shaped routes; storage reads keyed from the request). A finding when the handler loads a file record or object by a request id or key and streams it with no owner, share-grant or tenant predicate between load and send. An unguessable id is not the check — ids leak through URLs, referrers, logs and forwarded emails.

**Signed-link apps.** Most object-store apps do not load by id. A read that checks ownership MINTS a link (§15, grep 10c), and a public redeem route checks only the signature, so the check lives at the minter: trace every minter's predicate (tenant + owner + scope) and every place the client hands a key back (grep 15 third line). Two sub-shapes:
- **A client-supplied file reference stored on a row**, such as `filePath` in a create DTO, a task `path` or a receipt `imageUrl`. The server must verify it minted that key for this tenant, owner and scope. Otherwise a row points at another tenant's object, or at any URL the client then renders as `<iframe src>` (that half is `xss-scan`'s).
- **A shared queue's download**: exports, reports, dumps. Signing by job kind alone lets a member whose list is confined (assignee-only, one warehouse) download a colleague's whole-book export. Weigh the requester predicate against the list-visibility rules. When an owner decision says exports are shared, report Unconfirmed with that question.

Hand-off, same pack: the per-object ownership model is `@api-security-reviewer`'s (API1); when the boundary is a tenant (a per-tenant prefix or bucket) it is `@tenant-isolation-reviewer`'s. Report the file-shaped instance here with its `<file:line>` and cite the reviewer; do not re-derive the ownership model. **CWE-639 · A01:2025 · high** (critical cross-tenant or unauthenticated).

### 15. Signed GET link (cloud presign or app HMAC) issued without authorization or with a long TTL

```
BAD:   app.get('/download-url', async (req, res) => res.json({ url: await getSignedUrl(s3,
         new GetObjectCommand({ Bucket, Key: req.query.key }), { expiresIn: 7 * 24 * 3600 }) }))
       hmac(secret, `${key}.${exp}`)    // one secret for every link kind: a screen link redeems at the export route
GOOD:  authorise the record first (§14), then sign with a TTL of minutes, a per-kind label in the MAC,
       plus ResponseContentDisposition: 'attachment' and ResponseContentType: <validated type>
```
Candidates: grep 10 (presign calls with a read action, and its TTL line) and grep 10c (app-minted links: an HMAC over a key and an expiry, redeemed by a public route). A signed URL is a bearer token: whoever holds it reads the object until expiry — no session, no revocation, no audit trail. A finding when the minting path performs no §14 check; when the TTL exceeds the use (an inline image needs minutes; days survive a logout, a role change and a forwarded email); or when the URL lands in a log, an analytics event or a long-lived cache — `sig` must be on the log redaction list (`data-exposure-scan` § 6). For app HMAC links also check: a distinct label per link kind, so a signature for one route does not redeem at another. **Two TTLs under one HMAC label** is the same defect in a quieter form: a 2-hour screen link and a 7-day provider link signed with the same label and key are interchangeable, so the long TTL is the real one for every link of that label, and a screen link's reason ("2 h") understates it. Read every mint site of a label and compare their TTLs; a constant-time compare with a length check; and an unambiguous MAC message (`key.expires` splits two ways unless `expires` is validated as an integer). Signing without `ResponseContentDisposition` re-opens §3 on the bucket's origin. **CWE-639 · A01:2025 · high** without authorization; low–medium for the TTL alone (a `LEASTPRIV:` row in `@security-auditor`'s terms).

### 16. Content-Disposition filename built by hand

```
BAD:   res.setHeader('Content-Disposition', `attachment; filename="${doc.originalName}"`)
       // originalName = 'x.pdf"; filename*=UTF-8''evil.html' → saved as evil.html; raw CR/LF splits the header where allowed
GOOD:  res.attachment(doc.originalName)                         // RFC 6266 quoting + filename*
       FileResponse(f, as_attachment=True, filename=name)  ·  ContentDisposition.attachment().filename(name, UTF_8).build()
       send_data(data, filename: name)  ·  response()->download($path, $name)  ·  mime.FormatMediaType("attachment", params)
```
Candidates: grep 16 first line. A finding when a stored or request filename is interpolated into the header value instead of passing through the framework's encoder. The name was attacker-chosen at upload (§4), so this is second-order taint. Boundary: generic CRLF / header injection is `injection-scan`'s; this detector owns the download-header shape because its fix is the file helper. **CWE-113 · A05:2025 · medium** (low on runtimes that reject CR/LF in header values, where the impact is the quote-break and a reflected file download).

### 17. Filesystem paths in error responses

```
BAD:   catch (e) { res.status(500).json({ error: e.message }) }    // "ENOENT: no such file or directory, open '/srv/app/uploads/…'"
GOOD:  catch (e) { log.warn({ err: e, fileId }); res.sendStatus(e.code === 'ENOENT' ? 404 : 500) }
```
Candidates: grep 16 second line (error echo inside files that hold a read sink). A finding when a file sink's exception text reaches the response: it discloses the absolute root (the missing coordinate for a §11 payload), the OS and the deploy layout. A response that tells "exists but forbidden" from "does not exist" (403 vs 404, or measurably different timing) is an existence oracle over arbitrary paths — return one status for both. Boundary: generic stack-trace and error leakage is `data-exposure-scan`'s; this row is the file-sink instance only. **CWE-209 (CWE-204 for the oracle) · A10:2025 · low** (medium when it completes a §11 chain).

## Output

`[report-with-fix]` — the fix is a patch at the cited line. `[report-flagged]` — the fix is a design call (move user content to its own origin, add a scan pipeline, sandbox a processor, change the upload shape) and goes to an ADR.

```
file-access-scan — whole repo · lanes run: Node/TS, Python, edge (nginx) · backend pack: installed

Findings: 5

1. src/files/files.controller.ts:58                    [report-with-fix]  high · CWE-22 · A01:2025
   res.sendFile(path.join(FILES, req.query.name)) — `name` from the query string; no resolve + assert.
   Probe: GET /files?name=../../.env → 200 with the env file.
   Fix: res.sendFile(name, { root: FILES }) — or path.resolve + startsWith(FILES + path.sep), else 404.

2. src/uploads/upload.module.ts:14                     [report-with-fix]  medium · CWE-73 · A01:2025
   diskStorage filename: cb(null, file.originalname) — the client name is the stored name: one user's invoice.pdf
   overwrites another's, and the extension is attacker-chosen (busboy base-names it, so no traversal; §5 folded in).
   Fix: cb(null, `${randomUUID()}.${EXT_FOR[sniffed.mime]}`); keep originalname in the DB row only.

3. src/uploads/upload.module.ts:9 + src/main.ts:31     [report-flagged]   high · CWE-434 / CWE-79 · A05:2025
   dest 'public/uploads' sits under the app's static mount of 'public'; type checked from file.mimetype only (§1). An SVG runs script on the app origin.
   Fix (design): storage off the static root; serve via a handler with nosniff + attachment + CSP sandbox, or a separate user-content domain.

4. workers/import.py:41                                [report-with-fix]  high · CWE-22 / CWE-409 · A01:2025
   tarfile.open(upload).extractall(dest) — no filter, no entry or byte caps.
   Fix: extractall(dest, filter="data") + count entries and uncompressed bytes while iterating; reject over the cap.

5. src/tickets/attachments.service.ts:77               [report-flagged]   medium · CWE-434 · A06:2025
   Ticket attachments re-served to support staff; no malware scan anywhere in the pipeline (grep 9: 0 hits).
   Fix (design): quarantined → available on the attachment row; clamd scan on object-created; serve nothing until available.

Class coverage
  §1  type from client ............ checked (4 hits → 0 findings; folded into #3)
  §2  size / count cap ............ checked (3 handlers → 0 findings; multer limits + client_max_body_size 20m)
  §3  webroot / app-origin serve .. checked (2 hits → 1 finding)
  §4  client filename in path ..... checked (3 hits → 1 finding)
  §5  executable extensions ....... checked (1 hit → 0 findings; extension mapped from the sniffed type)
  §6  archive extraction .......... checked (1 hit → 1 finding)
  §7  file processors ............. checked (2 hits → 0 findings; sharp defaults kept, worker has no egress)
  §8  malware scan ................ checked (0 scanner hits → 1 finding)
  §9  presigned upload ............ N/A (no presign call in repo)
  §10 public ACL / public area .... N/A (no object store, no static mount over uploads)
  §11 traversal / LFI ............. checked (14 sinks → 1 finding)
  §12 symlink escape .............. checked (0 link-planting paths → 0 findings)
  §13 static mount ................ checked (2 mounts → 0 findings)
  §14 download IDOR ............... checked (3 routes → 0 findings; ownerId predicate at files.service.ts:22)
  §15 signed GET link ............. N/A (no presign call; grep 10c: 0 app-signed links)
  §16 Content-Disposition ......... checked (1 hit → 0 findings; res.attachment)
  §17 path in errors .............. blocked (errors shaped by a shared package outside this repo)
```

The class coverage block is required and lists all seventeen detectors — `checked (k hits → m findings)`, `N/A (<no such sink in repo>)` or `blocked (<reason>)` — so "found nothing" and "did not look" stay distinguishable. §10 and §15 cannot be `N/A` on "no ACL call" or "no presign call" alone: when grep 10b or 10c hits, the row reads `checked (public areas: N, writers into them: M → k findings)` or `checked (app-signed links: N → k findings)`. `/security-audit` reads this block into its class coverage ledger.

## False positives / gotchas

- **The safe primitives are not findings**: `res.sendFile(name, { root })`, `send_from_directory`, `safe_join`, `os.Root`, a framework storage that generates the key (Django `FileSystemStorage`, Active Storage, Shrine). Confirm the primitive guards *this* sink, then move on.
- **multer's `file.filename` is the stored name**, generated by default under `diskStorage` — read the `filename:` callback before flagging it as client input; `file.originalname` is the client's.
- **Joins differ on absolute input.** Python `os.path.join(root, "/etc/passwd")`, .NET `Path.Combine`, Java `Path.resolve` and Ruby `Pathname#join` (so `Rails.root.join`) return the absolute argument; Node `path.join` keeps the root but `path.resolve` does not. An assert *after* resolving catches all of them — that is why it is the only accepted fix.
- **A prefix check needs the separator.** `abs.startsWith('/srv/up')` accepts `/srv/upload-evil/x`; assert against `ROOT + sep`, with `ROOT` itself resolved. On Windows and macOS, compare case-insensitively where the filesystem is.
- **Decode once, then resolve, then assert** — the assert must see the exact string the filesystem will open. A check before a second URL-decode (`%252e%252e%252f`) is bypassed.
- **Python's `zipfile.extract*` already strips `..` and absolute parts** — no zip-slip finding there; §6's bomb caps still apply. `tarfile` without `filter=` is the finding on Python < 3.14.
- **Spring's multipart defaults are caps** (1MB / 10MB) — a missing property is not a missing cap; `-1` is.
- **An operator-only import behind admin auth** lowers severity; it removes the finding only when the input is a build-time constant.
- **Overlaps — report once, cite the other**: the same `<file:line>` may surface in `data-exposure-scan` (exposed files, error leakage), `injection-scan` (header injection, `phar://`, a shelled-out processor), `xss-scan` (the client rendering user content) or `ssrf-scan` (a processor that fetches URLs).

## When to run

- On any diff touching an upload handler, a multipart parser config, archive extraction, an image / PDF / media processor, a presign call or an app link signer, a storage-area registry or bucket policy, a static-file mount, or any read / download / `sendFile` sink — the signal `/security-audit` Phase 2 dispatches on. Also on a feature that clones or unpacks a user-supplied tree (theme, plugin, repository import), which that signal does not name.
- On every whole-repo security audit, and before launch on anything that accepts files or serves them back.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). Under `/security-audit` that happens in Phase 4; run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on any finding without the sink `<file:line>` + the tainted source or failing condition + the fix + a severity.
- Do not report a grep hit as a finding. Every row is a hit **plus** a read of the enclosing function that establishes the source-to-sink path and the missing guard.
- Never propose `..`-stripping, an extension deny-list, a client `Content-Type` check, or a `startsWith(root)` without the separator as a fix — each is a §11 / §5 / §1 finding in its own right.
- Do not assert a processor or archive-library CVE without the version resolved against the lockfile — hand that to `deps-audit`.
- Do not emit "no findings" without the full class coverage block; a detector with no `checked` / `N/A` / `blocked` row makes the run incomplete.

## Related

- `/security-audit` — Phase 2 dispatches here on the upload / read-sink signal; its class coverage ledger row for upload validation, stored-file execution, archive extraction, file processors, path traversal / LFI and download IDOR is sourced from this skill's coverage block.
- `/security-fix` — closes these findings and re-runs the same detector on the patched line.
- `/security-live-scan` — the dynamic counterpart: exposed files and headers on the running host confirm §3 / §13 findings.
- `@security-auditor` — its A01 path-traversal bullet is the detector row; this skill is the executor.
- `@api-security-reviewer` — API1 (object ownership, behind §14) and API4 (upload caps, behind §2).
- `@tenant-isolation-reviewer` — §14 when the file boundary is a tenant.
- `ssrf-scan` — its § Upload egress note names the SVG / polyglot / native-parser risks that §3, §1 and §7 now execute; URL-fetching processors stay there.
- `injection-scan` — shelled-out processors, `phar://` deserialization, generic header injection.
- `xss-scan` — client-side rendering of user content; §3 owns the server serving it.
- `data-exposure-scan` — exposed files and generic error leakage; §13 and §17 own the file-sink instances.
- `iac-scan` — bucket policies, Block Public Access, edge body caps and the rest of the reverse-proxy config.
- `deps-audit` — advisory status of the installed processor and archive-library versions.
- `backend/ai-patterns/file-upload.md` *(backend pack, when co-installed)* — the inbound contract: § Rules, § The three upload shapes — and what each one moves, § Detectors (cite-or-halt). Absent that pack, §1–§10 here are the contract.
- `backend/ai-patterns/response-streaming.md` *(backend pack, when co-installed)* — streaming a file out once §11 / §14 have cleared it.
- `rules/security-principles.md` — the file-upload MUST and the path-canonicalization MUST.
