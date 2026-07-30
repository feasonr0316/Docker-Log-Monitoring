import docker
import threading
import json
import time

from parser import parse_nginx_log
from storage import save_log, save_error
from detector import detect_error


client = docker.from_env()


def collect_logs(container):
    print("启动日志监听:", container.name)

    logs = container.logs(
        stream=True,
        follow=True,
        stdout=True,
        stderr=True,
        tail=0
    )

    for log in logs:
        print("收到日志:", log)

        log = log.decode("utf-8").strip()

        data = parse_nginx_log(
            container.name,
            container.short_id,
            log
        )

        print("解析结果:", data)

        log_id = save_log(data)

        print("保存完成:", log_id)

        result = detect_error(data)

        print("检测结果:", result)

        if result["is_error"]:
            result["log_id"] = log_id
            save_error(result)

            print("异常记录已保存")

        print(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            )
        )

listening_containers = set()

while True:
    containers = client.containers.list()

    for container in containers:
        if container.labels.get("monitor.exclude") == "true":
            continue

        if container.id in listening_containers:
            continue

        print("发现新容器:", container.name)

        thread = threading.Thread(
            target=collect_logs,
            args=(container,),
            daemon=True
        )

        thread.start()
        listening_containers.add(container.id)

    time.sleep(5)
