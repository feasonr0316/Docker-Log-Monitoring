import re


def parse_nginx_log(container_name, container_id, log):

    pattern = (
        r'(\S+) .* '
        r'\[(.*?)\] '
        r'"(\S+) (\S+) .*?" '
        r'(\d+) '
        r'(\d+)'
    )

    result = re.search(pattern, log)


    if result:

        data = {
            "container": container_name,
            "container_id": container_id,
            "ip": result.group(1),
            "time": result.group(2),
            "method": result.group(3),
            "path": result.group(4),
            "status": int(result.group(5)),
            "size": int(result.group(6)),
            "message": log,
            "log_type": "access"
        }

        return data


    return {
        "container": container_name,
        "container_id": container_id,
        "message": log,
        "log_type": "error"
    }
