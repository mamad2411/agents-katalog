# Adding a New MCP Tool

Follow this exact pattern when adding a new tool. Do not invent new registration patterns or file structures.

## Steps

1. **Implement in `src/tools/<category>.ts`**
   - Define a Zod schema for the tool's parameters using validators from `src/utils/validators.ts`
   - Add the handler inside the existing `register*Tools(server, exchangeManager)` function
   - Return `{ content: [{ type: 'text', text: JSON.stringify(...) }] }`

2. **Register in `src/tools/index.ts`**
   - If you created a new category file, import and call its `register*Tools()` function here
   - Existing categories (market-data, account, trading, cardano, strategy) are already wired up

3. **Update README.md**
   - Add the tool to the tools table with name, description, and parameters
   - Assign a pricing tier: free (`list_exchanges` only), read ($0.001), or write ($0.01)

4. **Add pricing in `src/payment/index.ts`**
   - Add the tool name to the appropriate tier in `TOOL_PRICING`

5. **Add unit test in `src/tests/`**
   - Mock the exchange connector via `getConnectorSafe()`
   - Test parameter validation and expected output shape

## Do NOT
- Create new files under `src/` for a single tool — add to the matching category file
- Use `require()` — this project is ESM (NodeNext)
- Skip `npm run typecheck` after changes
