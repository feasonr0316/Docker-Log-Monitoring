from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3


router = APIRouter()


class StatsResponse(BaseModel):
    total_logs: int
    total_errors: int
    containers: int

@router.get(
    "/stats",
    response_model=StatsResponse,
    tags=["系统统计"],
    summary="获取系统统计信息"
)
def get_stats():

    conn = sqlite3.connect("../collector/logs.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) FROM logs
        """
    )

    total_logs = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT COUNT(*) FROM error_logs
        """
    )

    total_errors = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT COUNT(DISTINCT container) FROM logs
        """
    )

    containers = cursor.fetchone()[0]


    conn.close()


    return {
        "total_logs": total_logs,
        "total_errors": total_errors,
        "containers": containers
    }


@router.get(
    "/stats/trend",
    tags=["系统统计"],
    summary="日志趋势"
)
def get_trend():

    conn = sqlite3.connect("../collector/logs.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            substr(time,1,14) as hour,
            COUNT(*)
        FROM logs
        WHERE time IS NOT NULL
        GROUP BY hour
        ORDER BY hour
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "time": row[0],
            "count": row[1]
        }
        for row in rows
    ]
