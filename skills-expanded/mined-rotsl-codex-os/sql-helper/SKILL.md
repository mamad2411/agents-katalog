# SQL Helper Plugin

## Purpose
Improve SQL correctness, performance, and clarity.

## Use When
- the task includes SQL query design
- a query is slow or inefficient
- SQL errors need debugging

## Behavior
- propose valid SQL, not pseudo-code
- optimize joins, filters, and indexes usage
- identify common mistakes (null handling, cartesian joins, wrong aggregation)
- explain fixes briefly with concrete rationale

## Output
- corrected query
- optimization notes
- validation checks

## Constraints
- keep output concise
- avoid speculative schema assumptions
