# 小红书 MCP 服务安装指南

## 什么是 MCP 服务？

MCP (Model Context Protocol) 服务是一个本地运行的服务，通过 Chrome DevTools Protocol (CDP) 控制浏览器，实现小红书内容的自动发布。

## 安装步骤

### 1. 克隆仓库

```bash
cd ~/.openclaw/workspace
git clone https://github.com/your-repo/xiaohongshu-mcp.git xiaohongshu-skill
cd xiaohongshu-skill
```

### 2. 安装依赖

```bash
npm install
```

### 3. 启动服务

```bash
npm start
```

服务将在 `http://localhost:18060` 启动。

### 4. 首次登录

1. 打开浏览器访问 `http://localhost:18060`
2. 点击"登录小红书"
3. 扫码登录
4. 登录成功后，Cookie 会自动保存

## 配置说明

### 端口配置

默认端口：`18060`

如需修改，编辑 `config.json`：

```json
{
  "port": 18060,
  "headless": true
}
```

### Cookie 管理

Cookie 保存位置：`~/.openclaw/workspace/xhs_data/xhs_cookies.json`

Cookie 有效期：约 30 天

## 使用方法

### 发布内容

```bash
curl -X POST http://localhost:18060/api/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "标题",
    "content": "正文内容",
    "images": ["/path/to/cover.jpg"],
    "tags": ["#标签1", "#标签2"]
  }'
```

### 检查登录状态

```bash
curl http://localhost:18060/api/status
```

## 故障排查

### 端口被占用

```bash
# 查看占用端口的进程
lsof -i :18060

# 杀死进程
kill -9 <PID>
```

### 登录失效

1. 访问 `http://localhost:18060`
2. 点击"重新登录"
3. 扫码登录

### Chrome 浏览器未找到

确保已安装 Chrome 浏览器：

```bash
# macOS
open -a "Google Chrome"

# 如果未安装，下载安装
# https://www.google.com/chrome/
```

## 安全建议

1. **不要分享 Cookie 文件**：包含登录凭证
2. **定期更新密码**：建议每月更新一次
3. **监控登录设备**：在小红书 App 中查看登录设备
4. **使用独立账号**：建议使用专门的运营账号

## 高级配置

### 无头模式

编辑 `config.json`：

```json
{
  "headless": true  // true: 后台运行, false: 显示浏览器
}
```

### 代理设置

```json
{
  "proxy": {
    "server": "http://proxy.example.com:8080",
    "username": "user",
    "password": "pass"
  }
}
```

### 超时设置

```json
{
  "timeout": {
    "navigation": 30000,  // 页面加载超时（毫秒）
    "action": 5000        // 操作超时（毫秒）
  }
}
```

## 更新服务

```bash
cd ~/.openclaw/workspace/xiaohongshu-skill
git pull
npm install
npm start
```

## 卸载

```bash
rm -rf ~/.openclaw/workspace/xiaohongshu-skill
rm -rf ~/.openclaw/workspace/xhs_data
```
