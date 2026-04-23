"""
One-time script to create the TruthScan database on TiDB Cloud.
Run this locally with the production .env values.
"""

import pymysql

# Production TiDB credentials (same ones used on Render)
HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
PORT = 4000
USER = "3i16FS6z5WGQ5wQ.root"
PASSWORD = "IlgwoltS6sSlZIZd"

# Connect WITHOUT a database first
conn = pymysql.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASSWORD,
    ssl={"ssl": {}},
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS truthscan_ai;")
cursor.execute("SHOW DATABASES;")
print("Databases visible to Render user:")
for db in cursor.fetchall():
    print("  -", db[0])

conn.close()
print("\nDone. 'truthscan_ai' should be in the list above.")
