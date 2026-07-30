import sqlite3


def save_log(data):

    print("进入save_log:", data)

    conn = sqlite3.connect("logs.db")

    cursor = conn.cursor()


    cursor.execute("""

    INSERT INTO logs (

        container,

        container_id,

        ip,

        time,

        method,

        path,

        status,

        size,

        message,

        log_type

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        data.get("container"),

        data.get("container_id"),

        data.get("ip"),

        data.get("time"),

        data.get("method"),

        data.get("path"),

        data.get("status"),

        data.get("size"),

        data.get("message"),

        data.get("log_type")

    ))

    log_id = cursor.lastrowid

    conn.commit()

    print("日志已保存:", data.get("log_type"))

    conn.close()

    return log_id

def save_error(error):

    conn = sqlite3.connect("logs.db")

    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO error_logs
    (
        log_id,
        reason,
        level
    )

    VALUES (?, ?, ?)

    """,
    (
        error.get("log_id"),
        error.get("reason"),
        error.get("level")
    ))

    conn.commit()

    conn.close()
