from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import sqlite3

router = APIRouter()

class ErrorItem(BaseModel):
    error_id: int
    log_id: int
    reason: str
    level: str
    container: str
    container_id: str
    time: str | None
    status: int | None
    path: str | None
    log_type: str | None
    message: str | None


class ErrorsResponse(BaseModel):
    total: int
    page: int
    size: int
    data: List[ErrorItem]

@router.get(
    "/errors",
    response_model=ErrorsResponse,
    tags=["错误分析"],
    summary="查询错误日志"
)

def get_errors(
    page: int = 1,
    size: int = 10,
    level: str = None,
    container: str = None
):

    conn = sqlite3.connect("../collector/logs.db")

    cursor = conn.cursor()

    offset = (page - 1) * size

    if level and container:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM error_logs e
            JOIN logs l ON e.log_id = l.id
            WHERE e.level=? AND l.container=?
            """,
            (level, container)
        )

    elif level:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM error_logs
            WHERE level=?
            """,
            (level,)
        )

    elif container:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM error_logs e
            JOIN logs l ON e.log_id = l.id
            WHERE l.container=?
            """,
            (container,)
        )

    else:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM error_logs
            """
        )

    total = cursor.fetchone()[0]

    if level:
        cursor.execute(
            """
            SELECT
                e.id,
                e.log_id,
                e.reason,
                e.level,
                l.container,
                l.container_id,
                l.time,
                l.status,
                l.path,
                l.log_type,
                l.message
            FROM error_logs e
            JOIN logs l ON e.log_id = l.id
            WHERE e.level=? AND l.container=?
            ORDER BY e.id DESC
            LIMIT ?
            OFFSET ?
            """,
            (
                level,
                container,
                size,
                offset
            )
         )

    elif level:
        cursor.execute(
            """
            SELECT
                e.id,
                e.log_id,
                e.reason,
                e.level,
                l.container,
                l.container_id,
                l.time,
                l.status,
                l.path,
                l.log_type,
                l.message
            FROM error_logs e
            JOIN logs l ON e.log_id = l.id
            WHERE e.level=?
            ORDER BY e.id DESC
            LIMIT ?
            OFFSET ?
            """,
            (
                level,
                size,
                offset
            )
        )

    elif container:
        cursor.execute(
            """
            SELECT
                e.id,
                e.log_id,
                e.reason,
                e.level,
                l.container,
                l.container_id,
                l.time,
                l.status,
                l.path,
                l.log_type,
                l.message
            FROM error_logs e
            JOIN logs l ON e.log_id = l.id
            WHERE l.container=?
            ORDER BY e.id DESC
            LIMIT ?
            OFFSET ?
            """,
            (
                container,
                size,
                offset
            )
        )

    else:
        cursor.execute(
            """
            SELECT
                e.id,
                e.log_id,
                e.reason,
                e.level,
                l.container,
                l.container_id,
                l.time,
                l.status,
                l.path,
                l.log_type,
                l.message
            FROM error_logs e
            JOIN logs l ON e.log_id = l.id
            ORDER BY e.id DESC
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
            "error_id": row[0],
            "log_id": row[1],
            "reason": row[2],
            "level": row[3],
            "container": row[4],
            "container_id": row[5],
            "time": row[6],
            "status": row[7],
            "path": row[8],
            "log_type": row[9],
            "message": row[10]
        })

    return {
        "total": total,
        "page": page,
        "size": size,
        "data": result
    }
