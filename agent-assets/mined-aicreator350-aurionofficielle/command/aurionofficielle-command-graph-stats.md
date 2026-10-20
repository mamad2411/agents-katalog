Show graph memory statistics and health.

Steps:
1. Run `node .claude/graph-memory/engine.cjs stats`
2. Format the output as a readable table:
   - Total nodes, edges, density
   - Node types breakdown
   - Top tags
   - Strongest nodes (most reinforced knowledge)
   - Journal days count
3. If graph is sparse (<10 nodes), suggest areas to document
4. If density is low (<0.05), suggest linking related topics
