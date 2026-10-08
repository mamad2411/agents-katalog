---
name: algo-binary-search-trees
description: "Implement/debug a binary search tree in Python: insert, search, delete (3 cases), successor/predecessor, inorder/level-order traversal. Use for BST coding, O(log n) vs O(n) degenerate cases, or choosing AVL/Red-Black."
tool_type: python
primary_tool: Python
---

# Binary Search Trees (BST)

## When to Use

- Implementing a BST from scratch for an interview, assignment, or as a building block for another data structure.
- Explaining or reasoning about BST time complexity (search/insert/delete/traversal) and why sorted input is a worst case.
- Debugging a broken `delete` (especially the two-children case) or successor/predecessor logic.
- Deciding whether a plain BST is sufficient or whether you need a self-balancing variant (AVL, Red-Black) for guaranteed O(log n).
- Needing inorder (sorted-order) or level-order (BFS) traversal of a tree of ordered values.

## Version Compatibility

Pure Python standard library only — `collections.deque`, `typing`. Works on Python ≥3.10 (uses `X | None` union syntax); for 3.8/3.9 replace with `Optional[X]`.

## Prerequisites

- No external packages required.
- Helpful prior concepts: `algo-complexity-analysis` (Big-O basics), `algo-linear-binary-search` (binary search on sorted arrays, for contrast).
- For guaranteed O(log n) instead of amortized/average behavior, see `algo-avl-trees` or `algo-red-black-trees`.

**Invariant**: for every node, all values in the left subtree < node value < all values in the right subtree (no duplicates stored; duplicates are treated as no-ops on insert).

## Complexity

| Operation | Average | Worst (degenerate) |
|-----------|---------|-------------------|
| Search / Insert / Delete | O(log n) | O(n) |
| Min / Max | O(log n) | O(n) |
| Successor / Predecessor | O(log n) | O(n) |
| Inorder traversal | O(n) | O(n) |

Worst case occurs on sorted (or reverse-sorted) input, which degenerates the tree into a linked list — use AVL or Red-Black tree to guarantee O(log n).

**Goal:** a correct, iterative BST supporting search/insert/delete plus ordering queries (min, max, successor, predecessor) and two traversal orders.

**Approach:** store `left`/`right`/`parent` pointers per node; keep insert/search iterative (O(height) stack-free); implement delete via the classic three-case rule, using `_transplant` to splice a subtree in place of a node.

```python
from collections import deque
from typing import Any


class Node:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.left = self.right = self.parent = None


class BST:
    def __init__(self) -> None:
        self.root: Node | None = None

    # --- Insert (iterative) ---
    def insert(self, value: Any) -> Node:
        """Insert value, returning the new (or existing, if duplicate) node."""
        if not self.root:
            self.root = Node(value)
            return self.root
        node = self.root
        while True:
            if value < node.value:
                if node.left is None:
                    node.left = Node(value)
                    node.left.parent = node
                    return node.left
                node = node.left
            elif value > node.value:
                if node.right is None:
                    node.right = Node(value)
                    node.right.parent = node
                    return node.right
                node = node.right
            else:
                return node  # duplicate: no-op

    # --- Search (iterative) ---
    def search(self, value: Any) -> Node | None:
        node = self.root
        while node:
            if value == node.value:
                return node
            node = node.left if value < node.value else node.right
        return None

    # --- Min / Max ---
    def find_min(self, node: Node | None = None) -> Node | None:
        node = node or self.root
        if not node:
            return None
        while node.left:
            node = node.left
        return node

    def find_max(self, node: Node | None = None) -> Node | None:
        node = node or self.root
        if not node:
            return None
        while node.right:
            node = node.right
        return node

    # --- Successor / Predecessor ---
    def successor(self, node: Node) -> Node | None:
        if node.right:
            return self.find_min(node.right)
        p = node.parent
        while p and node == p.right:
            node, p = p, p.parent
        return p

    def predecessor(self, node: Node) -> Node | None:
        if node.left:
            return self.find_max(node.left)
        p = node.parent
        while p and node == p.left:
            node, p = p, p.parent
        return p

    # --- Delete ---
    def delete(self, value: Any) -> bool:
        """Delete value if present. Returns True if a node was removed."""
        node = self.search(value)
        if not node:
            return False
        self._delete_node(node)
        return True

    def _delete_node(self, node: Node) -> None:
        if node.left and node.right:
            succ = self.find_min(node.right)
            node.value = succ.value
            self._delete_node(succ)  # succ has at most one child (its right)
        else:
            child = node.left or node.right
            self._transplant(node, child)

    def _transplant(self, u: Node, v: Node | None) -> None:
        """Replace subtree rooted at u with subtree rooted at v."""
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # --- Traversals ---
    def inorder(self) -> list[Any]:
        """Return values in sorted order."""
        result: list[Any] = []

        def _rec(n):
            if n:
                _rec(n.left)
                result.append(n.value)
                _rec(n.right)

        _rec(self.root)
        return result

    def level_order(self) -> list[Any]:
        """Return values in BFS (level-by-level) order."""
        if not self.root:
            return []
        result, q = [], deque([self.root])
        while q:
            n = q.popleft()
            result.append(n.value)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        return result

    def __contains__(self, value: Any) -> bool:
        return self.search(value) is not None


def demo() -> None:
    """Self-check: build a tree, verify invariants hold after insert/delete."""
    bst = BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(v)
    assert bst.inorder() == [20, 30, 40, 50, 60, 70, 80]
    assert 40 in bst and 999 not in bst

    n40 = bst.search(40)
    assert bst.successor(n40).value == 50
    assert bst.predecessor(n40).value == 30

    assert bst.delete(30) is True   # two children (20 has none, but 30 has left=20)
    assert 30 not in bst
    assert bst.inorder() == [20, 40, 50, 60, 70, 80]
    assert bst.delete(999) is False

    print("All BST checks passed.")


if __name__ == "__main__":
    demo()
```

## Delete: Three Cases

| Node type | Action |
|-----------|--------|
| Leaf | Remove directly (transplant with `None`) |
| One child | Replace node with that child |
| Two children | Copy inorder successor's value into the node, then delete the successor (which has at most one child) |

## Pitfalls

- **Sorted input degenerates to O(n)**: inserting `[1,2,3,4,5]` creates a linked list; use a self-balancing tree (AVL, Red-Black) for production use where input order isn't controlled.
- **Inorder successor during deletion**: after copying the successor's value to the deleted node, you must delete the successor node — not the original node again (recursing on `succ`, not `node`, avoids this).
- **Parent pointer consistency**: when implementing with parent pointers, only set `v.parent` in `_transplant` if `v` is not `None`, or you'll crash on leaf deletion.
- **Recursive height/traversal on deep trees**: Python's default recursion limit (~1000) is hit on degenerate (near-linear) trees; use iterative traversal (e.g. an explicit stack, like `level_order`'s BFS) for untrusted input sizes.
- **Duplicates**: this implementation silently ignores inserting a value already present; decide explicitly whether your use case needs a count/multiset instead.

## See Also

- `algo-avl-trees` — self-balancing BST guaranteeing O(log n) via rotations.
- `algo-red-black-trees` — another self-balancing BST, used by many standard library map/set implementations.
- `algo-linear-binary-search` — binary search over a sorted array (no explicit tree structure).
- `algo-complexity-analysis` — Big-O fundamentals referenced throughout this skill.
