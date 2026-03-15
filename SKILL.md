---
name: xiaohongshu-auto-operation
description: 小红书账号全自动运营系统。每日自动选题、内容生成、封面制作、定时发布、数据分析。适用于：(1) 需要每日更新小红书账号；(2) 希望自动化内容生产流程；(3) 需要数据驱动的运营优化；(4) 想要批量管理多个小红书账号。支持完全自动化或半自动化模式。
---

# 小红书自动化运营 Skill

这个 Skill 提供完整的小红书账号自动化运营解决方案，从选题策划到数据分析全流程自动化。

## 核心功能

### 1. 每日自动选题（18:00）
- 搜索最新爆款笔记和热门话题
- 分析历史数据表现
- 生成 3 个差异化选题方向
- 每个选题包含：标题、创新点、互动设计

### 2. 内容自动生成
- 根据选题生成完整正文（≤1000字）
- 自动优化标题（≤20字）
- 生成话题标签（≤10个）
- 违规词自动检测和替换

### 3. 封面自动制作
- AI 生成高质量封面图
- 尺寸：1080x1440（3:4）
- 无留白，填满画布
- 高对比度设计

### 4. 定时自动发布（20:30）
- 通过 MCP 服务自动发布
- 发布前预检查（19:45）
- 发布日志记录

### 5. 数据自动分析（22:00）
- 抓取所有笔记数据
- 生成数据报告
- 趋势分析和优化建议

## 运营模式

### 模式 1：完全自动化
- 自动选择最优选题
- 自动生成内容和封面
- 自动发布
- 无需人工干预

### 模式 2：半自动化（推荐）
- AI 准备 3 个选题
- 人工确认选择
- 自动生成和发布
- 保持内容质量控制

## 安装配置

### 前置要求

1. **小红书 MCP 服务**
   - 安装：参考 `references/mcp-setup.md`
   - 端口：`http://localhost:18060`
   - 需要 Chrome 浏览器

2. **Python 环境**
   - Python 3.8+
   - 依赖：`playwright`, `requests`

3. **Obsidian（可选）**
   - 用于内容管理和数据存储
   - 路径：`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/JerryHunag WorkSpace/Obsidian Vault/小红书/`

### 快速开始

1. **安装依赖**
```bash
pip install playwright requests
playwright install chromium
```

2. **配置定时任务**
```bash
# 在 OpenClaw 中运行
claw cron add --name "小红书选题准备" \
  --schedule "0 18 * * *" \
  --task "执行小红书选题准备任务"

claw cron add --name "小红书发布预检查" \
  --schedule "45 19 * * *" \
  --task "检查小红书 MCP 服务状态"

claw cron add --name "小红书自动发布" \
  --schedule "30 20 * * *" \
  --task "执行小红书自动发布任务"

claw cron add --name "小红书数据报告" \
  --schedule "0 22 * * *" \
  --task "执行小红书数据抓取和分析"
```

3. **启动 MCP 服务**
```bash
cd ~/.openclaw/workspace/xiaohongshu-skill
npm start
```

4. **首次登录**
- 访问 `http://localhost:18060`
- 扫码登录小红书账号
- 保持登录状态

## 使用指南

### 日常工作流程

**18:00 - 选题准备**
- AI 自动搜索热点和爆款
- 生成 3 个选题方向
- 发送消息通知

**你的操作**（半自动模式）
- 回复选择哪个选题（1/2/3）
- 或回复"自动选择"让 AI 决定

**AI 自动执行**
- 生成完整正文
- 制作封面图
- 保存到待发布文件夹

**19:45 - 发布预检查**
- 检查 MCP 服务状态
- 检查登录状态
- 如有问题，发送提醒

**20:30 - 自动发布**
- 读取待发布内容
- 自动发布到小红书
- 记录发布日志

**22:00 - 数据报告**
- 抓取所有笔记数据
- 生成数据报告
- 发送分析结果

### 内容规范

**标题要求**
- 长度：≤20 个字
- 格式：数字法/对比法/痛点法
- 禁止：绝对化用语（最、第一、100%等）

**正文要求**
- 长度：≤1000 个字
- 结构：痛点开头 + 效果对比 + 3步教程 + 互动引导
- 禁止：绝对化用语、诱导互动、拉踩行为

**封面要求**
- 尺寸：1080x1440（3:4）
- 设计：高对比度、无留白
- 文字：大字标题 + 简洁副标题

**标签要求**
- 数量：≤10 个
- 格式：`#标签名`
- 位置：正文最后一行

### 违规词检测

系统自动检测和替换以下违规词：
- 绝对化用语：最、第一、100%、必须、一定
- 诱导互动：评论区回复、点赞关注、转发抽奖
- 拉踩行为：品牌对比、贬低竞品

详细列表见：`references/violation-words.md`

## 文件结构

```
xiaohongshu-auto-operation/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── topic_generator.py      # 选题生成脚本
│   ├── content_generator.py    # 内容生成脚本
│   ├── cover_generator.py      # 封面生成脚本
│   ├── publisher.py            # 发布脚本
│   └── data_analyzer.py        # 数据分析脚本
└── references/
    ├── mcp-setup.md            # MCP 服务安装指南
    ├── content-rules.md        # 内容规范详解
    ├── violation-words.md      # 违规词列表
    └── optimization-guide.md   # 运营优化指南
```

## 高级功能

### 多账号管理
- 支持同时管理多个小红书账号
- 每个账号独立配置
- 统一数据看板

### 数据驱动优化
- 自动分析爆款内容特征
- 推荐最佳发布时间
- 标签效果分析
- 封面 A/B 测试

### 内容素材库
- 爆款标题模板库
- 封面设计模板库
- 互动话术库
- 自动学习和更新

## 故障排查

### MCP 服务无法启动
- 检查端口 18060 是否被占用
- 检查 Chrome 浏览器是否安装
- 查看服务日志：`~/.openclaw/workspace/xiaohongshu-skill/logs/`

### 登录状态失效
- 重新访问 `http://localhost:18060`
- 扫码重新登录
- 检查 Cookie 是否过期

### 发布失败
- 检查内容是否符合规范（字数、格式）
- 检查是否有违规词
- 检查封面图是否存在
- 查看发布日志：`~/.openclaw/workspace/memory/xiaohongshu_log.md`

### 数据抓取失败
- 检查网络连接
- 检查账号是否被限流
- 检查脚本是否需要更新

## 最佳实践

1. **保持登录状态**：每周至少检查一次 MCP 服务登录状态
2. **定期备份**：每周备份发布日志和数据报告
3. **内容多样化**：避免重复相似选题，保持内容新鲜度
4. **数据分析**：每周查看数据报告，优化内容方向
5. **违规预防**：发布前仔细检查违规词

## 更新日志

- **v1.0.0** (2026-03-15)
  - 初始版本
  - 支持完全自动化运营流程
  - 包含选题、生成、发布、分析全流程

## 支持

- GitHub: https://github.com/your-username/xiaohongshu-auto-operation
- Issues: https://github.com/your-username/xiaohongshu-auto-operation/issues
- 文档: https://github.com/your-username/xiaohongshu-auto-operation/wiki
