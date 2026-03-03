# Microsoft Webhook 发送工具

这是一个用于向 Microsoft Teams 和 Power Automate 发送 webhook 消息的 Python 工具。

## 功能特性

- 🔄 **同时支持** Microsoft Teams Webhook 和 Power Automate Webhook
- 📝 支持 Adaptive Card 格式的富文本消息
- 🎯 支持自定义标题和消息内容
- 💻 支持命令行参数输入消息
- 🔒 环境变量配置管理，保护敏感信息
- 🤖 自动检测 Webhook 类型并使用正确的消息格式

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 文件为 `.env`：

```bash
cp .env.example .env
```

2. 在 `.env` 文件中配置您的 webhook URL：

```
# Microsoft Teams Webhook（直接在 Teams 中创建的连接器）
POWER_AUTOMATE_WEBHOOK_URL=https://yourtenant.webhook.office.com/webhookb2/...

# 或 Power Automate Webhook（通过 Power Automate 创建的 HTTP 触发器）
POWER_AUTOMATE_WEBHOOK_URL=https://prod-xx.region.logic.azure.com/workflows/...
```

### Webhook 类型说明

本工具会自动检测 Webhook 类型并使用正确的格式：

| Webhook 类型 | URL 特征 | 创建方式 |
|-------------|---------|---------|
| **Teams Webhook** | 包含 `webhook.office.com` | 在 Teams 频道中添加"传入 Webhook"连接器 |
| **Power Automate Webhook** | 包含 `logic.azure.com` | 在 Power Automate 中创建带 HTTP 触发器的流 |

## 使用方法

### 基本使用

直接运行脚本，将发送默认的测试消息：

```bash
python send_webhook.py
```

### 自定义消息

通过命令行参数发送自定义消息：

```bash
python send_webhook.py "您的自定义消息内容"
```

### 代码中使用

```python
from send_webhook import PowerAutomateWebhook

webhook_url = "your_webhook_url"
webhook = PowerAutomateWebhook(webhook_url)

result = webhook.send_message(
    message="消息内容",
    title="消息标题"
)

if result['success']:
    print("消息发送成功")
else:
    print(f"发送失败: {result['error']}")
```

## 项目结构

```
.
├── .env.example          # 环境变量示例文件
├── .gitignore           # Git 忽略文件配置
├── requirements.txt     # Python 依赖列表
├── send_webhook.py      # 主程序文件
└── README.md            # 项目说明文档
```

## 依赖项

- `requests>=2.31.0` - HTTP 请求库

## 注意事项

- 请确保 `.env` 文件不会被提交到版本控制系统（已在 `.gitignore` 中配置）
- webhook URL 应该保密，不要泄露
- 确保网络连接正常，能够访问 Power Automate 服务
