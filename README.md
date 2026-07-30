# 基于 Docker 的容器日志监控系统

## 项目介绍

本项目设计并实现了一套基于 Docker 的容器日志监控系统。

系统面向单机 Docker 实验环境，通过自动发现运行中的容器，持续采集容器标准输出和标准错误日志，对 Nginx 访问日志进行结构化解析，并根据 HTTP 状态码和关键词规则进行异常检测。

采集后的日志数据保存至 SQLite 数据库，后端通过 FastAPI 提供查询和统计接口，前端使用 Vue 3 和 ECharts 实现日志展示、数据统计以及趋势可视化。

项目主要用于学习和实践：

- Docker 容器管理
- 容器日志采集
- Python 后端开发
- 前后端接口设计
- 数据库存储
- Web 可视化展示
- Docker Compose 部署


---

# 项目目标

在 Docker 多容器运行环境中，解决以下问题：

- 多个容器日志分散，不方便统一查看；
- 使用 docker logs 命令逐个查看效率较低；
- 原始日志文本难以快速筛选和统计；
- 异常日志不容易被及时发现；
- 缺少简单直观的日志趋势展示。


本系统实现：

- 自动发现 Docker 容器；
- 持续采集容器日志；
- 日志结构化解析；
- 异常日志检测；
- 日志数据持久化；
- 日志查询与筛选；
- 统计信息展示；
- 日志趋势分析；
- Docker Compose 一键部署。


---

# 系统架构

整体数据流程如下：

```
Docker 容器
     |
     |
     v
日志采集模块 collector
     |
     |
     v
日志解析与异常检测
     |
     |
     v
SQLite 数据库存储
     |
     |
     v
FastAPI 后端接口
     |
     |
     v
Vue 3 + ECharts 前端展示
```


系统主要组成：

```
docker-log-monitor-system

├── collector
│   └── Docker日志采集服务
│
├── backend
│   └── FastAPI后端接口服务
│
├── frontend
│   └── Vue3前端展示系统
│
├── docker-compose.yml
│   └── 一键部署配置
│
└── docs
    └── 项目文档
```


---

# 技术栈

## 后端

| 技术 | 用途 |
|---|---|
| Python | 后端开发语言 |
| FastAPI | Web接口框架 |
| Docker SDK for Python | Docker容器管理 |
| SQLite | 数据持久化存储 |


## 前端

| 技术 | 用途 |
|---|---|
| Vue 3 | 前端页面开发 |
| Axios | 前后端通信 |
| ECharts | 数据可视化 |


## 部署

| 技术 | 用途 |
|---|---|
| Docker | 容器运行环境 |
| Docker Compose | 多服务编排部署 |
| Nginx | 测试日志来源容器 |


---

# 功能模块

## 1. Docker 容器发现模块

功能：

- 获取当前运行中的 Docker 容器；
- 周期性扫描新启动容器；
- 建立日志监听。


实现：

使用 Docker SDK for Python：

```python
docker.from_env()
```

连接本机 Docker 服务。


---

## 2. 容器日志采集模块

功能：

- 持续读取容器 stdout/stderr 日志；
- 获取容器运行日志；
- 传递日志进行后续处理。


支持：

- 多容器日志采集；
- 动态发现后的日志监听。


---

## 3. Nginx 日志解析模块

功能：

将原始 Nginx 访问日志解析为结构化数据。


提取信息：

- 客户端地址；
- 请求时间；
- 请求方法；
- 请求路径；
- HTTP状态码；
- 响应大小。


无法匹配格式的日志：

保留原始内容。


---

## 4. 异常检测模块

功能：

根据规则检测异常日志。


检测条件：

### HTTP状态码

例如：

```
404
403
500
```

### 关键词

例如：

```
error
failed
exception
```


说明：

当前系统采用规则检测方式，
不包含机器学习模型和自动告警功能。


---

## 5. 日志存储模块

数据库：

SQLite


主要数据表：

## logs

保存全部日志信息。


## error_logs

保存异常日志记录。


数据关系：

通过日志 ID 建立程序逻辑关联。


---

## 6. 日志查询模块

提供：

- 日志分页查询；
- 容器名称筛选；
- HTTP状态码筛选；
- 异常日志查询。


---

## 7. 系统统计模块

统计内容：

- 日志总数量；
- 异常日志数量；
- 当前监控容器数量。


---

## 8. 日志趋势可视化模块

功能：

按照时间统计日志数量。


展示：

- 小时级日志趋势；
- ECharts折线图。


---

# 后端接口

主要接口：

| 接口 | 功能 |
|-|-|
| GET /logs | 查询日志 |
| GET /errors | 查询异常日志 |
| GET /stats | 获取系统统计 |
| GET /stats/trend | 获取日志趋势 |


---

# 部署方式

## 环境要求

建议环境：

- Ubuntu 22.04
- Docker
- Docker Compose
- Python 3
- Node.js


---

## 一键启动


进入项目目录：

```bash
cd docker-log-monitor-system
```


启动：

```bash
docker compose up -d --build
```


查看运行状态：

```bash
docker compose ps
```


停止：

```bash
docker compose down
```


---

# 项目运行流程


启动系统：

```
docker compose up
```

↓

collector启动

↓

自动发现Docker容器

↓

读取容器日志

↓

解析Nginx访问日志

↓

检测异常日志

↓

保存SQLite

↓

FastAPI提供接口

↓

Vue页面展示


---

# 项目截图

## 前端页面

包括：

- 日志列表；
- 异常日志展示；
- 数据统计；
- 趋势图。


## API接口

提供：

- Swagger接口文档；
- 日志查询接口；
- 统计接口。


---

# 项目目录说明

```
backend
│
├── main.py
├── routers
└── 数据接口相关代码


collector
│
├── 日志采集代码
├── 日志解析代码
└── 异常检测代码


frontend
│
├── Vue页面
├── Axios请求
└── ECharts图表


docker-compose.yml
│
└── 服务部署配置
```


---

# 项目特点

- 基于真实 Docker 环境开发；
- 支持容器动态发现；
- 实现日志采集到展示完整链路；
- 前后端分离设计；
- 支持 Docker Compose 一键部署；
- 适合作为 Docker 日志监控学习项目。


---

# 项目限制

当前系统定位为学习和实验环境：

不包含：

- 用户登录；
- 权限管理；
- 自动告警；
- 分布式日志采集；
- Elasticsearch；
- ELK完整平台；
- Kubernetes集群管理。


后续可以扩展：

- 增加用户权限；
- 接入 Elasticsearch；
- 增加消息通知；
- 支持多主机日志采集。


---

# 作者

姓名：
feasonr
项目：
《基于 Docker 的容器日志监控系统设计与实现》
更新时间：
2026 7/30
