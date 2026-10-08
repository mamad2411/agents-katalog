---
name: algo-stacks-queues
description: Implement Stack (LIFO)/Queue (FIFO) in Python (array, linked-list, two-stack) with O(1) ops; validate balanced brackets/RNA dot-bracket notation. Use for stack/queue from scratch, backing BFS/DFS, or checking parens.
tool_type: python
primary_tool: Python
---

# Stacks and Queues

## When to Use

- Implementing a stack or queue from scratch (interviewer disallows `list`/`collections.deque`)
- Validating balanced brackets/parentheses, or nested notations like RNA secondary-structure dot-bracket strings (`(((...)))`)
- Building undo/redo, browser back-button history, or expression (postfix/infix) evaluators
- Backing a BFS (queue) or DFS/backtracking (stack) traversal — see `algo-bfs-dfs`
- Explaining why `list.pop(0)` is a queue anti-pattern, or the "queue with two stacks" interview question

## Version Compatibility

Pure Python standard library only — no third-party dependencies. Works on Python ≥3.8 (uses `typing.Optional`); `collections.deque` and `queue.PriorityQueue` are stdlib since Python 2, unchanged in behavior through Python 3.13.

## Prerequisites

- Comfort with Python classes and references (a linked node's `next` is a reference, not a copy)
- Big-O notation — see `algo-complexity-analysis`
- No external packages needed

## Stack (LIFO)

All operations O(1). Use for: DFS, backtracking, bracket matching, undo/redo, recursion-to-iteration.

**Goal:** a stack with push/pop/peek that raises on empty rather than returning `None` (silent `None` hides bugs).

**Approach:** array-based version wraps a Python `list` (amortized O(1) `append`/`pop` from the end); linked-list version prepends nodes at `_top` for true O(1) push with no resize.

```python
from typing import Any, Optional, List


class ArrayStack:
    """Stack backed by a Python list. push/pop/peek are O(1) amortized."""

    def __init__(self) -> None:
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        self._items.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return len(self._items) > 0


class StackNode:
    """A node in the linked-list stack; `next` points toward the bottom."""

    def __init__(self, value: Any, next_node: Optional["StackNode"] = None) -> None:
        self.value = value
        self.next = next_node


class LinkedStack:
    """Stack backed by a singly linked list. push/pop/peek are O(1), never amortized."""

    def __init__(self) -> None:
        self._top: Optional[StackNode] = None
        self._size = 0

    def push(self, item: Any) -> None:
        self._top = StackNode(item, self._top)
        self._size += 1

    def pop(self) -> Any:
        if self._top is None:
            raise IndexError("Pop from empty stack")
        value = self._top.value
        self._top = self._top.next
        self._size -= 1
        return value

    def peek(self) -> Any:
        if self._top is None:
            raise IndexError("Peek from empty stack")
        return self._top.value

    def is_empty(self) -> bool:
        return self._top is None

    def __len__(self) -> int:
        return self._size


if __name__ == "__main__":
    for Stack in (ArrayStack, LinkedStack):
        s = Stack()
        for v in [10, 20, 30]:
            s.push(v)
        assert s.peek() == 30 and len(s) == 3
        assert s.pop() == 30 and s.pop() == 20 and s.pop() == 10
        assert s.is_empty()
        try:
            s.pop()
            assert False, "expected IndexError on empty pop"
        except IndexError:
            pass
    print("Stack self-check passed")
```

## Queue (FIFO)

All operations O(1). Use for: BFS, task scheduling, message buffers, simulation.

**Goal:** enqueue at the rear, dequeue from the front, both O(1) — never shift a Python list.

**Approach:** `LinkedQueue` keeps `_front`/`_rear` pointers so both ends are reachable without scanning; `QueueWithTwoStacks` shows the classic "simulate a queue with two stacks" trick (push-only inbox, pop-only outbox, transfer on demand — O(1) amortized per operation since each element moves at most 4 times total).

```python
from typing import Any, Optional


class QueueNode:
    def __init__(self, value: Any, next_node: Optional["QueueNode"] = None) -> None:
        self.value = value
        self.next = next_node


class LinkedQueue:
    """Queue backed by a singly linked list with cached front/rear pointers."""

    def __init__(self) -> None:
        self._front: Optional[QueueNode] = None
        self._rear: Optional[QueueNode] = None
        self._size = 0

    def enqueue(self, item: Any) -> None:
        node = QueueNode(item)
        if self._rear is None:
            self._front = self._rear = node
        else:
            self._rear.next = node
            self._rear = node
        self._size += 1

    def dequeue(self) -> Any:
        if self._front is None:
            raise IndexError("Dequeue from empty queue")
        value = self._front.value
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return value

    def peek(self) -> Any:
        if self._front is None:
            raise IndexError("Peek from empty queue")
        return self._front.value

    def is_empty(self) -> bool:
        return self._front is None

    def __len__(self) -> int:
        return self._size


class QueueWithTwoStacks:
    """FIFO queue simulated with two LIFO stacks (classic interview question)."""

    def __init__(self) -> None:
        self._inbox: ArrayStack = ArrayStack()
        self._outbox: ArrayStack = ArrayStack()

    def enqueue(self, item: Any) -> None:
        """Always push to inbox. O(1)."""
        self._inbox.push(item)

    def dequeue(self) -> Any:
        """Pop from outbox; refill it from inbox (reversing order) if empty."""
        if self._outbox.is_empty():
            while not self._inbox.is_empty():
                self._outbox.push(self._inbox.pop())
        if self._outbox.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._outbox.pop()

    def is_empty(self) -> bool:
        return self._inbox.is_empty() and self._outbox.is_empty()


if __name__ == "__main__":
    for Queue in (LinkedQueue, QueueWithTwoStacks):
        q = Queue()
        for v in [10, 20, 30]:
            q.enqueue(v)
        assert q.dequeue() == 10 and q.dequeue() == 20 and q.dequeue() == 30
        assert q.is_empty()
    print("Queue self-check passed")
```

## Application: Bracket / Dot-Bracket Matching

**Goal:** validate that brackets are balanced — the same algorithm validates RNA secondary-structure dot-bracket notation (`(((..)).)`) where `(` must pair with a later `)` and unmatched/crossed brackets indicate invalid structure.

**Approach:** push each opening symbol; on a closing symbol, pop and check it matches. Balanced iff the stack ends empty.

```python
def is_balanced(expression: str, pairs: dict = None) -> bool:
    """
    Check that brackets in `expression` are balanced and properly nested.

    Works for plain brackets ("(){}[]") and RNA dot-bracket notation
    (only "()" used; "." is ignored) by passing pairs={')': '('}.

    >>> is_balanced("({[]})")
    True
    >>> is_balanced("([)]")
    False
    >>> is_balanced("(((...)).)")   # RNA dot-bracket, one unmatched '('
    False
    """
    matching = pairs if pairs is not None else {')': '(', ']': '[', '}': '{'}
    opening = set(matching.values())
    closing = set(matching.keys())

    stack = ArrayStack()
    for char in expression:
        if char in opening:
            stack.push(char)
        elif char in closing:
            if stack.is_empty() or stack.pop() != matching[char]:
                return False
    return stack.is_empty()


if __name__ == "__main__":
    assert is_balanced("({[]})") is True
    assert is_balanced("([)]") is False
    assert is_balanced("(((...))") is False  # unmatched '(' — mimics bad dot-bracket
    assert is_balanced("((..))..((.))", pairs={')': '('}) is True  # RNA dot-bracket, valid
    print("Bracket-matching self-check passed")
```

## Python stdlib equivalents

- Stack: just use `list` (`append`/`pop`)
- Queue: `collections.deque` (`append`/`appendleft` + `pop`/`popleft`, all O(1))
- Priority queue: `heapq` or `queue.PriorityQueue`

## Pitfalls

- Using `list.pop(0)` as a queue is O(n) (shifts every remaining element) — use `collections.deque.popleft()` instead
- Array-based stack `push` is O(1) amortized but O(n) worst case during list resize
- In `QueueWithTwoStacks`, only transfer inbox→outbox when outbox is empty — transferring on every call breaks the O(1)-amortized guarantee and re-reverses order incorrectly
- Bracket matching must check `stack.is_empty()` before popping on a closing symbol, otherwise a lone `)` raises instead of returning `False`
- For RNA dot-bracket validation, remember pseudoknots (crossed pairs, e.g. `([)]`) are invalid under simple bracket matching — they need a different representation (extended bracket alphabet or base-pair list)

## See Also

- `algo-linked-lists` — the node/pointer mechanics `LinkedStack`/`LinkedQueue` are built on
- `algo-bfs-dfs` — BFS uses a queue, DFS uses a stack (or recursion)
- `algo-dynamic-arrays` — why array-based `push`/`pop` is O(1) amortized, not worst-case
- `bio-rna-structure-secondary-structure-prediction` — dot-bracket notation in a real RNA-folding context
