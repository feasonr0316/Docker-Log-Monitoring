# Docker Compose 一键启动

先停止手动启动的 collector、FastAPI 和 Vite 服务，避免占用 `8000`、`5173` 端口。

在项目根目录执行：

```bash
docker compose up -d --build
```

查看服务状态：

```bash
docker compose ps
```

查看采集器实时日志：

```bash
docker compose logs -f collector
```

停止全部项目服务：

```bash
docker compose down
```

前端地址仍为 `http://<Ubuntu-IP>:5173`，后端 Swagger 地址为
`http://<Ubuntu-IP>:8000/docs`。
