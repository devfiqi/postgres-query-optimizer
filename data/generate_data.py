import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Connect to database (uses your Mac username by default)
print("Connecting to database...")
conn = psycopg2.connect("dbname=ecommerce_benchmark")
cur = conn.cursor()

# Generate 100k users
print("Generating 100,000 users...")
batch_size = 1000
for batch in range(100):
    users_batch = []
    for i in range(batch_size):
        username = (fake.user_name() + str(batch * batch_size + i))[:50]
        users_batch.append((
            username,
            fake.email()[:100],
            fake.country()[:50],
            random.choice([True, False])
        ))
    
    cur.executemany("""
        INSERT INTO users (username, email, country, is_premium)
        VALUES (%s, %s, %s, %s)
    """, users_batch)
    
    conn.commit()
    print(f"  Users: {(batch + 1) * batch_size} / 100,000")

print("✓ Users complete")

# Generate 10k products
print("\nGenerating 10,000 products...")
categories = ['Electronics', 'Books', 'Clothing', 'Home', 'Sports']
batch_size = 500
for batch in range(20):
    products_batch = []
    for i in range(batch_size):
        products_batch.append((
            fake.catch_phrase(),
            random.choice(categories),
            round(random.uniform(10, 1000), 2)
        ))
    
    cur.executemany("""
        INSERT INTO products (name, category, price)
        VALUES (%s, %s, %s)
    """, products_batch)
    
    conn.commit()
    print(f"  Products: {(batch + 1) * batch_size} / 10,000")

print("✓ Products complete")

# Get actual ID ranges from the database
cur.execute("SELECT MIN(user_id), MAX(user_id) FROM users")
min_user_id, max_user_id = cur.fetchone()
cur.execute("SELECT MIN(product_id), MAX(product_id) FROM products")
min_product_id, max_product_id = cur.fetchone()
print(f"\nUser IDs: {min_user_id}-{max_user_id}, Product IDs: {min_product_id}-{max_product_id}")

# Generate 1M orders + 5M order items
print("Generating 1,000,000 orders (this will take 30-60 min)...")
print("(You can let this run overnight)")

for i in range(1000000):
    # Create order
    user_id = random.randint(min_user_id, max_user_id)
    order_date = fake.date_time_between(start_date='-2y', end_date='now')

    cur.execute("""
        INSERT INTO orders (user_id, order_date, total_amount, status)
        VALUES (%s, %s, %s, %s)
        RETURNING order_id
    """, (
        user_id,
        order_date,
        round(random.uniform(20, 500), 2),
        random.choice(['pending', 'shipped', 'delivered', 'cancelled'])
    ))

    order_id = cur.fetchone()[0]

    # Create 3-7 order items
    num_items = random.randint(3, 7)
    items_batch = []
    for _ in range(num_items):
        items_batch.append((
            order_id,
            random.randint(min_product_id, max_product_id),
            random.randint(1, 5),
            round(random.uniform(10, 200), 2)
        ))
    
    cur.executemany("""
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s)
    """, items_batch)
    
    if (i + 1) % 10000 == 0:
        conn.commit()
        print(f"  Orders: {i + 1} / 1,000,000")

conn.commit()
print("\n✓ Orders complete")
print("\n=== DATA GENERATION COMPLETE ===")
print("Database ready for benchmarking!")

cur.close()
conn.close()