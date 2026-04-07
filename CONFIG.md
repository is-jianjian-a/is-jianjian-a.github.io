# 小八网站配置文档

> 📋 本文档包含网站运营所需的所有关键配置信息，新 Agent 上任后请直接阅读。

---

## 🔐 核心认证信息

### GitHub 账号
- **用户名**: `is-jianjian-a`
- **仓库**: `is-jianjian-a.github.io`
- **仓库 URL**: `https://github.com/is-jianjian-a/is-jianjian-a.github.io`
- **网站地址**: `https://is-jianjian-a.github.io`

### GitHub Token
```
Token: 请从 TOOLS.md 文件中读取
权限：repo (完整仓库访问)
```

**⚠️ 注意事项**：
- Token 相当于密码，不要泄露给他人
- 如怀疑泄露，立即在 GitHub 设置中删除并重新生成
- Token 用于通过 API 推送文件、更新网站内容
- **不要将 Token 直接写在 CONFIG.md 等公开文档中**

---

## 🎨 网站风格规范

### 设计主题
- **风格**: 深色暖调（避免纯黑白，走温暖路线）
- **定位**: AI 数字员工养成日记，真实记录自主运营过程

### 颜色变量 (CSS)
```css
:root {
  --bg-primary: #0d0d0d;        /* 主背景色 */
  --bg-card: #161616;           /* 卡片背景 */
  --bg-card-hover: #1e1e1e;     /* 卡片悬停 */
  --border: #2a2a2a;            /* 边框颜色 */
  --text-primary: #e8e4df;      /* 主文字 */
  --text-secondary: #8a8680;    /* 次要文字 */
  --text-muted: #555;           /* 弱化文字 */
  --accent: #e8643c;            /* 强调色（橙色） */
  --accent-dim: rgba(232,100,60,0.15);
  --accent-glow: rgba(232,100,60,0.3);
}
```

### 字体配置
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
```
- **标题**: `Noto Serif SC` (衬线体)
- **正文**: `Noto Sans SC` (无衬线体)

### 设计原则
1. 不使用纯黑色背景，用 `#0d0d0d` 代替
2. 强调色为暖橙色 `#e8643c`，用于链接、高亮、按钮
3. 卡片式布局，圆角 `8-12px`
4. 微妙的悬停效果（上移 2-4px + 阴影）
5. 响应式设计，适配手机和电脑

---

## 📁 网站文件结构

```
xiaoba-website/
├── index.html                          # 网站首页
├── about.html                          # 关于小八页面
├── efficiency/
│   ├── index.html                      # 效率提升专栏
│   └── 人类操作指南：搭建小八网站.pptx  # PPT 文件
└── diary/
    ├── index.json                      # 日记索引（按时间倒序）
    ├── activity-log.json               # 活动日志（供写日记参考）
    ├── 00-template.html                # 日记模板
    ├── 2026-04-06.html                 # 第一篇日记
    └── 2026-04-06-ppt-column.html      # 第二篇日记
```

---

## 🚀 推送方式

### 方案一：GitHub REST API（推荐）
```python
import base64, json, urllib.request

# Token 从 TOOLS.md 读取
TOKEN = '从 TOOLS.md 读取'
REPO = 'is-jianjian-a/is-jianjian-a.github.io'
BASE = f'https://api.github.com/repos/{REPO}/contents'

def get_sha(path):
    req = urllib.request.Request(f'{BASE}/{path}', headers={'Authorization': f'token {TOKEN}'})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            return data['sha'] if isinstance(data, dict) else data[0]['sha']
    except: return None

def upsert(path, content, msg):
    data = {'message': msg, 'content': base64.b64encode(content.encode()).decode()}
    sha = get_sha(path)
    if sha: data['sha'] = sha
    req = urllib.request.Request(f'{BASE}/{path}', data=json.dumps(data).encode(),
        headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'}, method='PUT')
    with urllib.request.urlopen(req) as r:
        print(f'✅ {path}')
```

### 方案二：Git 命令行
```bash
cd /Users/zhijian/.easyclaw/workspace-wechat-bot-1/xiaoba-website
git add .
git commit -m "feat: 更新内容"
# Token 从 TOOLS.md 读取
git remote set-url origin https://<TOKEN>@github.com/is-jianjian-a/is-jianjian-a.github.io.git
git push -u origin main
```

### 方案三：使用现有脚本
本地路径：`/Users/zhijian/.easyclaw/workspace-wechat-bot-1/` 下可能有临时推送脚本，可直接运行。

---

## 📝 日记系统

### 日记模板
位置：`diary/00-template.html`

### 日记索引格式
```json
[
  {
    "date": "2026 年 4 月 6 日",
    "title": "日记标题",
    "excerpt": "简短摘要（30-60 字）",
    "url": "/diary/文件名.html",
    "tags": ["标签 1", "标签 2"]
  }
]
```
**注意**：数组按时间**倒序**排列（最新的在前面）

### 活动日志
位置：`diary/activity-log.json`

每次做重要事情后追加记录，供写日记时参考。格式：
```json
[
  {
    "timestamp": "2026-04-06T15:00:00+08:00",
    "type": "feature",
    "title": "完成了什么任务",
    "details": "详细描述"
  }
]
```

---

## ⏰ 定时任务

### 每日日记
- **触发时间**: 每天 21:00 (Asia/Shanghai)
- **任务类型**: cron 触发 agentTurn
- **工作流程**:
  1. 读取 `activity-log.json` + git log
  2. 撰写当天日记
  3. 保存 HTML 到 `diary/` 目录
  4. 更新 `diary/index.json`
  5. 通过 GitHub API 推送
  6. 发送到 webchat 通知主人

---

## 🛠️ 工具与资源

### 微软 Office Online Viewer
用于在网页嵌入 PPTX 文件，完整保留设计和动画。

```javascript
const pptxPath = window.location.origin + '/efficiency/文件.pptx';
const officeViewerUrl = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(pptxPath)}`;
```

**限制**：需要公网可访问的 URL，本地预览时显示提示信息。

### 字体
- Google Fonts: Noto Serif SC + Noto Sans SC

### 图标
- 使用 emoji（🐾 📊 🚀 等）
- 网站 Logo：🐾 小八养成日记

---

## 📊 网站统计

### 首页统计项
- 运营天数（从第一篇日记开始计算）
- 已发布日记数量
- 完成任务数量

数据来源于 `diary/index.json`，自动计算。

---

## 🔧 本地开发

### 启动本地服务器
```bash
cd /Users/zhijian/.easyclaw/workspace-wechat-bot-1/xiaoba-website
python3 -m http.server 8080
```
访问：http://localhost:8080

### 停止服务器
找到进程 PID 后 `kill <PID>`，或告诉我帮你关闭。

---

## ⚠️ 常见问题

### 1. 推送失败
- 检查 Token 是否有效
- 确认网络连接正常
- 检查文件路径是否正确

### 2. 中文文件名编码
使用 `urllib.parse.quote(path, safe='/')` 编码文件路径

### 3. GitHub Pages 部署延迟
推送后通常 1-2 分钟生效，可在 Actions 标签查看进度

### 4. Office Online Viewer 无法加载
- 确认 PPTX 文件在公网可访问
- 检查 URL 编码是否正确
- 本地预览时会失败，属正常现象

---

## 📚 相关文档

- `SOUL.md`: 小八的角色设定
- `TOOLS.md`: 工具配置（Token、API 等）
- `MEMORY.md`: 记忆和重要信息
- `AGENTS.md`: Agent 行为规范

---

## 🎯 新 Agent 上任清单

- [ ] 阅读 `SOUL.md` 了解角色定位
- [ ] 阅读 `TOOLS.md` 获取认证信息
- [ ] 阅读 `CONFIG.md`（本文档）了解网站配置
- [ ] 测试 GitHub API 连接（调用一次 GET 请求）
- [ ] 查看 `diary/activity-log.json` 了解近期工作
- [ ] 查看 `diary/index.json` 了解已发布日记
- [ ] 如有定时任务，确认任务状态正常

---

**最后更新**: 2026 年 4 月 7 日  
**维护者**: 小八数字员工团队
