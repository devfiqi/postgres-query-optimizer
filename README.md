# PostgreSQL Query Optimizer

## Overview

This project benchmarks PostgreSQL query performance before and after adding indexes. It uses a small ecommerce schema, synthetic data, slow query examples, optimized query examples, and a Python benchmark script that captures `EXPLAIN ANALYZE` output.

## Features

- Ecommerce schema with users, products, orders, and order items.
- Synthetic data generator for benchmark data.
- Slow and optimized SQL query examples.
- Index definitions for targeted query optimization.
- Benchmark runner that compares average and minimum execution times.
- JSON result output for later review.

## Architecture / Implementation

- `schema/` contains table definitions.
- `data/` contains the data generation script.
- `queries/slow/` contains baseline queries.
- `queries/optimized/` contains optimized queries.
- `indexes/` contains index definitions.
- `benchmark.py` runs the comparison and writes benchmark results.

The benchmark flow creates a baseline by dropping non-primary-key indexes, runs the slow query set, creates the configured indexes, refreshes PostgreSQL statistics with `ANALYZE`, and runs the optimized query set.

## Tech Stack

- PostgreSQL
- Python
- psycopg2
- Faker

## How to Build/Run

Create the database and schema:

```bash
createdb ecommerce_benchmark
psql ecommerce_benchmark < schema/01_create_tables.sql
```

Install Python dependencies:

```bash
pip install psycopg2-binary Faker
```

Generate benchmark data:

```bash
python data/generate_data.py
```

Run the benchmark:

```bash
python benchmark.py
```

## Tests/Benchmarks

The benchmark runner executes each query multiple times with `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`, prints a comparison table, and writes timestamped JSON results to `results/`.

## What I Learned

- How PostgreSQL query plans change when indexes are added.
- How B-tree indexes improve selective lookups.
- How composite index column order affects query support.
- How to use `EXPLAIN ANALYZE` and buffer metrics to evaluate query performance.
- How read performance improvements can add write and storage trade-offs.
