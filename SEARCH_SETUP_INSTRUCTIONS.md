# 搜索API配置说明

## 如何设置Brave Search API密钥

要使web_search功能正常工作，请按照以下步骤操作：

1. 访问 https://brave.com/search/api/
2. 注册并获取免费的API密钥（每天2000次查询限制）
3. 获取API密钥后，有几种方式设置：

### 方法1：通过环境变量
```bash
# 设置环境变量
export BRAVE_API_KEY="your_actual_brave_api_key_here"
# 然后重启OpenClaw
openclaw gateway restart
```

### 方法2：直接编辑配置文件
1. 编辑 `C:\Users\89198\.openclaw\openclaw.json`
2. 将 `"apiKey": "YOUR_BRAVE_API_KEY_HERE"` 替换为实际的API密钥
3. 重启OpenClaw服务

### 方法3：使用configure命令
```bash
openclaw configure --section web
```
然后按照交互式提示输入API密钥。

## 验证配置

设置完成后，您可以通过以下方式验证：
- 在聊天中输入 "搜索最新的AI新闻"
- 或者直接使用web_search工具

注意：Brave Search API提供免费层级，每月5000次查询，足以满足大多数个人使用需求。