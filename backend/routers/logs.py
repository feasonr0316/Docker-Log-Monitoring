from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3
from typing import List

router = APIRouter()

class LogItem(BaseModel):
    id: int
    container: str
    container_id: str
    ip: str | None
    time: str | None
    method: str | None
    path: str | None
    status: int | None
    size: int | None
    message: str | None
    log_type: str | None


class LogsResponse(BaseModel):
    total: int
    page: int
    size: int
    data: List[LogItem]

@router.get(
    "/logs",
    response_model=LogsResponse,
    tags=["日志查询"],
    summary="查询日志列表"
)
def get_logs(
    page: int = 1,
    size: int = 10,
    container: str = None,
    status: int = None
):

    conn = sqlite3.connect(
        "../collector/logs.db"
    )

    cursor = conn.cursor()


    offset = (page - 1) * size


    if container and status:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM logs
            WHERE container=? AND status=?
            """,
            (container, status)
        )

    elif container:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM logs
            WHERE container=?
            """,
            (container,)
        )

    elif status:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM logs
            WHERE status=?
            """,
            (status,)
        )

    else:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM logs
            """
        )

    total = cursor.fetchone()[0]

    if container and status:
        cursor.execute(
            """
            SELECT *
            FROM logs
            WHERE container=? AND status=?
            LIMIT ?
            OFFSET ?
            """,
            (
                container,
                status,
                size,
                offset
            )
        )

    elif container:
        cursor.execute(
            """
            SELECT *
            FROM logs
            WHERE container=?
            LIMIT ?
            OFFSET ?
            """,
            (
                container,
                size,
                offset
            )
        )

    elif status:
        cursor.execute(
            """
            SELECT *
            FROM logs
            WHERE status=?
            LIMIT ?
            OFFSET ?
            """,
            (
                status,
                size,
                offset
            )
        )

    else:
        cursor.execute(
            """
            SELECT *
            FROM logs
            LIMIT ?
            OFFSET ?
            """,
            (
                size,
                offset
            )
        )

    rows = cursor.fetchall()


    conn.close()


    result = []


    for row in rows:

        result.append({

            "id": row[0],

            "container": row[1],

            "container_id": row[2],

            "ip": row[3],

            "time": row[4],

            "method": row[5],

            "path": row[6],

            "status": row[7],

            "size": row[8],

            "message": row[9],
           
            "log_type": row[10]

        })

    return {
        "total": total,
        "page": page,
        "size": size,
        "data": result
    }
