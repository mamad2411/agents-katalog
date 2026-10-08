---
name: algo-linked-lists
description: Implement singly/doubly linked lists in Python (O(1) head/tail insert, delete, reverse) plus pointer problems like Floyd's cycle detection and merge-sorted-lists. Use for linked-list coding-interview questions.
tool_type: python
primary_tool: Python
---

# Linked Lists

## When to Use

- Implementing a singly or doubly linked list from scratch (no built-in Python list allowed)
- Explaining why arrays beat linked lists for random access but lose on head insertion
- Solving classic pointer-manipulation interview problems: cycle detection, find middle, merge two sorted lists, remove n-th from end, palindrome check
- Building a data structure with O(1) insert/delete at known positions (e.g., an LRU cache's backing store, which needs a doubly linked list)
- Teaching/reviewing slow-fast (tortoise-and-hare) pointer technique

## Version Compatibility

Pure Python standard library only — no third-party dependencies. Works on Python ≥3.8 (uses `typing.Optional`); on Python ≥3.10 you can replace `Optional['Node']` with `Node | None`.

## Prerequisites

- Comfort with Python classes and references/aliasing (a node's `next` is a reference, not a copy)
- Big-O notation — see `algo-complexity-analysis`
- No external packages needed

## Array vs Linked List

| Feature | Array | Linked List |
|---------|-------|-------------|
| Memory | Contiguous | Scattered |
| Random access | O(1) | O(n) |
| Insert/delete at head | O(n) | O(1) |
| Insert/delete at tail | O(1) amortized | O(1) with tail ptr (singly), O(1) (doubly) |
| Cache performance | Excellent | Poor |
| Memory overhead | None | 1 pointer/node (singly), 2 (doubly) |

## Singly Linked List: Core Implementation

**Goal:** a singly linked list with head/tail pointers so both head and tail insertion are O(1), plus search, delete, and reverse.

**Approach:** each `Node` holds `data` and `next`; the list tracks `head`, `tail`, and a cached `_length` so `len()` is O(1). Reversing rewires `next` pointers in a single pass and must reset `tail` to the old head.

```python
from typing import Optional, Any, Iterator


class Node:
    """A node in a singly linked list."""

    def __init__(self, data: Any, next_node: Optional["Node"] = None) -> None:
        self.data = data
        self.next = next_node

    def __repr__(self) -> str:
        return f"Node({self.data})"


class SinglyLinkedList:
    """Singly linked list with O(1) head/tail insertion via a cached tail pointer."""

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __str__(self) -> str:
        if self.head is None:
            return "empty list"
        nodes = [f"[{d}]" for d in self]
        nodes.append("null")
        return " -> ".join(nodes)

    def is_empty(self) -> bool:
        return self.head is None

    def add_at_head(self, data: Any) -> None:
        """Insert at the front. O(1)."""
        new_node = Node(data, self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self._length += 1

    def add_at_tail(self, data: Any) -> None:
        """Insert at the back. O(1) because tail is cached."""
        new_node = Node(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._length += 1

    def delete_at_head(self) -> Optional[Any]:
        """Remove and return the first value. O(1)."""
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._length -= 1
        return data

    def delete_by_value(self, data: Any) -> bool:
        """Remove the first node matching `data`. O(n)."""
        if self.head is None:
            return False
        if self.head.data == data:
            self.delete_at_head()
            return True
        current = self.head
        while current.next is not None and current.next.data != data:
            current = current.next
        if current.next is None:
            return False
        if current.next == self.tail:
            self.tail = current
        current.next = current.next.next
        self._length -= 1
        return True

    def search(self, data: Any) -> int:
        """Return the index of the first match, or -1. O(n)."""
        current, index = self.head, 0
        while current is not None:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def reverse(self) -> None:
        """Reverse the list in place. O(n) time, O(1) space."""
        self.tail = self.head  # old head becomes new tail
        prev, current = None, self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev


if __name__ == "__main__":
    sll = SinglyLinkedList()
    for v in [5, 3, 8, 1]:
        sll.add_at_tail(v)
    assert list(sll) == [5, 3, 8, 1]
    assert sll.search(8) == 2 and sll.search(99) == -1
    assert sll.delete_by_value(3) is True and list(sll) == [5, 8, 1]
    sll.reverse()
    assert list(sll) == [1, 8, 5] and sll.tail.data == 5
    print("SinglyLinkedList self-check passed")
```

## Interview Problems: Slow/Fast Pointers

**Goal:** cycle detection, finding the middle node, merging two sorted lists, and removing the n-th node from the end — the problems that come up most in coding interviews.

**Approach:** most of these use two pointers moving at different speeds (Floyd's tortoise-and-hare) or a fixed gap between two pointers, giving O(n) time and O(1) extra space without ever converting to a Python list.

```python
from typing import Optional


def has_cycle(head: Optional[Node]) -> bool:
    """Floyd's cycle detection: slow moves 1 step, fast moves 2. O(n)/O(1)."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def find_middle(head: Optional[Node]) -> Optional[Node]:
    """Return the middle node (second middle for even length). O(n)/O(1)."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


def merge_sorted_lists(head1: Optional[Node], head2: Optional[Node]) -> Optional[Node]:
    """Merge two sorted singly linked lists into one sorted list. O(n+m)/O(1)."""
    dummy = Node(0)
    current = dummy
    while head1 is not None and head2 is not None:
        if head1.data <= head2.data:
            current.next, head1 = head1, head1.next
        else:
            current.next, head2 = head2, head2.next
        current = current.next
    current.next = head1 if head1 is not None else head2
    return dummy.next


def remove_nth_from_end(head: Optional[Node], n: int) -> Optional[Node]:
    """Remove the n-th node from the end in one pass using a dummy head + gap."""
    dummy = Node(0)
    dummy.next = head
    first = second = dummy
    for _ in range(n + 1):
        if first is None:
            return head  # n larger than list length
        first = first.next
    while first is not None:
        first = first.next
        second = second.next
    second.next = second.next.next
    return dummy.next


if __name__ == "__main__":
    a, b, c, d = Node(1), Node(2), Node(3), Node(4)
    a.next, b.next, c.next = b, c, d
    assert has_cycle(a) is False
    d.next = b  # introduce a cycle 4 -> 2
    assert has_cycle(a) is True
    d.next = None  # clean up

    m = find_middle(Node(1, Node(2, Node(3, Node(4, Node(5))))))
    assert m.data == 3

    l1 = Node(1, Node(3, Node(5)))
    l2 = Node(2, Node(4, Node(6)))
    merged = merge_sorted_lists(l1, l2)
    out = []
    while merged:
        out.append(merged.data)
        merged = merged.next
    assert out == [1, 2, 3, 4, 5, 6]

    nodes = [Node(i) for i in range(1, 6)]
    for i in range(4):
        nodes[i].next = nodes[i + 1]
    new_head = remove_nth_from_end(nodes[0], 2)  # drop the 2nd-from-end (value 4)
    out = []
    while new_head:
        out.append(new_head.data)
        new_head = new_head.next
    assert out == [1, 2, 3, 5]
    print("Interview-problem self-checks passed")
```

## Pitfalls

- Forgetting to update `tail` when deleting the last node or when reversing — the classic off-by-reference bug
- Delete at tail is O(n) on a singly linked list (must find the second-to-last node); use a doubly linked list if tail deletion is frequent
- `slow == fast` compares by value for custom `__eq__`; use `is` (identity) for cycle/middle detection so you're comparing node references, not data
- Losing the rest of the list when reversing — always save `next_node = current.next` before rewiring `current.next`
- Off-by-one in `remove_nth_from_end`: advance the lead pointer `n + 1` steps (not `n`) so the trailing pointer lands just before the target node

## See Also

- `algo-stacks-queues` — a doubly linked list backs an O(1) deque
- `algo-dynamic-arrays` — the array-based alternative and its amortized-O(1) append
- `algo-binary-search-trees` — a "linked" structure with two child pointers instead of one `next`
- `algo-complexity-analysis` — Big-O background for the tables above
