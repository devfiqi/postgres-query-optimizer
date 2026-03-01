# PostgreSQL Query Optimizer

Understanding database performance through hands-on query optimization.

## Learning Goals

- How B-tree indexes improve query performance
- When to use indexes vs when they hurt performance
- How to profile and optimize slow queries
- The trade-offs between read performance and write performance

### B-tree Indexes
PostgreSQL uses B-trees for indexing, which provide O(log n) lookup vs O(n) sequential scan.

### Optimization Techniques
1. **Single-column indexes** - For simple filters
2. **Composite indexes** - For multi-column filters
3. **Query rewriting** - JOIN instead of subquery
4. **EXPLAIN ANALYZE** - Understanding query execution plans

## Performance Results

| Query | Before | After | Improvement | Technique |
|-------|--------|-------|-------------|-----------|
| User Orders | 245ms | 8ms | 30x | Single-column index |
| High-Value Orders | 1200ms | 45ms | 27x | Composite index |
| Product Sales | 2100ms | 180ms | 12x | Query rewrite + index |

## Resources

**Designing Data-Intensive Applications** by Martin Kleppmann
- Chapter 3: Storage and Retrieval (B-trees, LSM-trees, indexes)

**PostgreSQL Documentation**
- EXPLAIN and query planning
- Index types and usage

## Running
```bash
# Setup database
createdb ecommerce_benchmark
psql ecommerce_benchmark < schema/01_create_tables.sql

# Generate data
python data/generate_data.py

# Run benchmarks
python benchmark.py
```

## Goal?

Built to understand how production databases optimize queries - the same techniques used by LinkedIn's Venice, Espresso, and other distributed data systems. Understanding B-tree indexes prepares me for working on storage systems at scale.
