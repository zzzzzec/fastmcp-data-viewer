# FastMCP Stdio 调试踩坑记录

本文档记录了在通过标准输入/输出（Stdio）模式直接与 FastMCP 服务进行命令行交互时遇到的常见问题和正确步骤。

## 关键步骤与常见错误

### 1. 激活虚拟环境

**问题**: 在项目根目录直接运行 `data-viewer` 命令时，提示 `bash: data-viewer: command not found`。

**原因**: 项目通过 `pip install -e .` 安装的可执行文件位于 `.venv/bin/` 目录下，而系统默认的 `PATH` 并不包含这个路径。

**解决方案**: 必须先激活项目的 Python 虚拟环境，才能让 Shell 找到正确的命令。

```bash
# 在项目根目录下执行
source .venv/bin/activate
```

### 2. 发送 `initialize` 初始化请求

**问题**: 激活环境后，直接发送 `tools/list` 或 `tools/call` 请求，服务器返回 `Received request before initialization was complete` 错误。

**原因**: 根据 MCP 协议，客户端连接到服务器后，**必须**发送的第一条消息是 `initialize` 请求，用于建立会话。在初始化成功之前，服务器会拒绝所有其他业务请求。

**解决方案**: 建立连接后，务必先发送一个完整的 `initialize` 请求。

一个最小化且正确的 `initialize` 请求如下（**注意：必须为单行 JSON**）：
```json
{"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "clientInfo": {"name": "test-console-client", "version": "0.1.0"}, "capabilities": {}}}
```

### 3. 使用正确的请求方法 (Method)

**问题**: `initialize` 成功后，发送 `{"method": "tool_list"}` 这样的请求，服务器返回 `Invalid request parameters` 错误。

**原因**: MCP 协议为各类操作定义了标准的、带前缀的方法名。例如，列出工具的方法是 `tools/list` 而不是 `tool_list`。

**解决方案**: 使用文档规定的正确方法名。

*   **列出工具**:
    ```json
    {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    ```

*   **调用工具**:
    ```json
    {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "your_tool_name", "args": {"arg1": "value1"}}}
    ```

## 正确的交互流程总结

1.  **启动服务**:
    ```bash
    source .venv/bin/activate
    data-viewer
    ```
2.  **初始化 (粘贴并回车)**:
    ```json
    {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "clientInfo": {"name": "test-console-client", "version": "0.1.0"}, "capabilities": {}}}
    ```
3.  **（收到成功响应后）列出工具**:
    ```json
    {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    ```
4.  **（收到成功响应后）调用工具**:
    ```json
    {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_summary", "args": {"path": "test.parquet"}}}
    ```
