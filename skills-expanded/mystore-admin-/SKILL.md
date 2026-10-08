# Lessons

- Supabase Storage public URL must include the bucket name. Prefer using `getPublicUrl()` rather than manual string building.
- Supabase Storage requires RLS policies on `storage.objects` per-bucket; authenticated users need explicit `insert` policy and public read needs `select` policy for the bucket.
- Keep debug info in API JSON minimal but include HTTP status codes for clarity.
- On client, clear Zod field error immediately on input change, including file inputs.
- For optimistic creates, if upstream fails, best-effort delete uploaded file using API DELETE with object path.
- Avoid hydration mismatches: render client-only dynamic UI after mount using a guard.

# Scratchpad

[ ] Add storage RLS policies for `products` bucket in Supabase
[ ] Ensure bucket `products` is set to public if using public URLs
[X] Fix API to generate correct public URL and unique file path
[X] Add DELETE handler to remove files from `products` bucket
[X] Clear image field validation error on file selection
[X] Add mount guard to Breadcrumbs to avoid hydration mismatch

Task: Enable image uploads to Supabase `products` bucket with correct URL
Plan:
- Create per-bucket `insert` policy for authenticated users
- Create per-bucket `select` policy for public reads (or mark bucket public)
- Use `getPublicUrl()` in API and generate unique file paths
- Verify upload succeeds without RLS error and URL loads
 - Add DELETE route to clean up orphaned files on failure
