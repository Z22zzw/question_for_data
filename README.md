# QQ Doc MCP Server 配置指南

## 快速开始

1. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env，填入你的腾讯文档 API Token
   ```

2. **构建项目**
   ```bash
   npm run build
   ```

3. **在 Claude Code 中启用 MCP**
   - 使用 `/update-config` 命令配置 MCP 服务器
   - 或手动编辑 `.claude/mcp.json`

## MCP 工具列表

- `create_document`: 创建新文档
- `get_document`: 获取文档内容
- `update_document`: 更新文档
- `delete_document`: 删除文档
- `list_documents`: 列出文档

## 获取腾讯文档 API Token

访问 [腾讯文档开放平台](https://docs.qq.com/openapi) 获取 API 凭证。
