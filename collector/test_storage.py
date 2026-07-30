from storage import save_log


data = {

    "container":"test-nginx",

    "container_id":"123",

    "ip":"127.0.0.1",

    "time":"now",

    "method":"GET",

    "path":"/",

    "status":500,

    "size":100,

    "message":"error"

}


log_id = save_log(data)


print("新日志id:", log_id)
