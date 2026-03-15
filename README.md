# 小红书自动化运营 Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)

完整的小红书账号自动化运营解决方案，从选题策划到数据分析全流程自动化。

## ✨ 核心功能

- 🎯 **每日自动选题**：AI 分析热点，生成 3 个差异化选题
- ✍️ **内容自动生成**：根据选题生成完整正文、标题、标签
- 🎨 **封面自动制作**：AI 生成高质量封面图（1080x1440）
- ⏰ **定时自动发布**：每天 20:30 自动发布到小红书
- 📊 **数据自动分析**：每天 22:00 抓取数据并生成报告

## 🚀 快速开始

### 1. 安装 Skill

```bash
# 下载 Skill
git clone https://github.com/your-username/xiaohongshu-auto-operation.git
cd xiaohongshu-auto-operation

# 复制到 OpenClaw skills 目录
cp -r . ~/.openclaw/skills/xiaohongshu-auto-operation/
```

### 2. 安装依赖

```bash
pip install playwright requests
playwright install chromium
```

### 3. 配置 MCP 服务

参考 `references/mcp-setup.md` 安装和配置小红书 MCP 服务。

### 4. 配置定时任务

在 OpenClaw 中配置 4 个定时任务：

- **18:00** - 选题准备
- **19:45** - 发布预检查
- **20:30** - 自动发布
- **22:00** - 数据报告

详细配置见 `SKILL.md`。

## 📖 使用文档

- [完整使用指南](SKILL.md)
- [MCP 服务安装](references/mcp-setup.md)
- [内容规范详解](references/content-rules.md)
- [违规词列表](references/violation-words.md)

## 🎯 运营模式

### 完全自动化
- AI 自动选择最优选题
- 自动生成内容和封面
- 自动发布
- 无需人工干预

### 半自动化（推荐）
- AI 准备 3 个选题
- 人工确认选择
- 自动生成和发布
- 保持内容质量控制

## 📊 效果展示

- ✅ 每日稳定更新
- ✅ 内容质量可控
- ✅ 数据驱动优化
- ✅ 节省 90% 运营时间

## 🛠️ 技术栈

- **OpenClaw**: AI Agent 框架
- **Playwright**: 浏览器自动化
- **MCP**: 小红书发布服务
- **Python**: 数据分析脚本

## 📝 更新日志

### v1.0.0 (2026-03-15)
- 🎉 初始版本发布
- ✅ 支持完全自动化运营流程
- ✅ 包含选题、生成、发布、分析全流程

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License

## 🔗 相关链接

- [OpenClaw 官网](https://openclaw.ai)
- [小红书创作者中心](https://creator.xiaohongshu.com)
- [问题反馈](https://github.com/your-username/xiaohongshu-auto-operation/issues)

## ⚠️ 免责声明

本工具仅供学习和研究使用，请遵守小红书平台规则，不要用于违规操作。使用本工具产生的任何后果由使用者自行承担。
