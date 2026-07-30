from storage import save_log

data = {
    "container": "test",
    "container_id": "123",
    "ip": "127.0.0.1",
    "time": "now",
    "method": "GET",
    "path": "/test",
    "status": 404,
    "size": 100,
    "message": "test error",
    "log_type": "access"
}

save_log(data)

print("测试完成")
