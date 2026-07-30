import sqlite3


conn = sqlite3.connect("logs.db")


cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    container TEXT,

    container_id TEXT,

    ip TEXT,

    time TEXT,

    method TEXT,

    path TEXT,

    status INTEGER,

    size INTEGER,

    message TEXT,

    log_type TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS error_logs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    log_id INTEGER,

    reason TEXT,

    level TEXT

)
""")

conn.commit()

conn.close()


print("数据库初始化完成")
