#!/usr/bin/env python3
import requests
import json
import sys
from typing import Dict, Any, Optional
from pathlib import Path

def load_webhook_url() -> str:
    """从 .env 文件加载 webhook URL"""
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() == 'POWER_AUTOMATE_WEBHOOK_URL':
                        return value.strip()
    raise FileNotFoundError(
        "未找到 .env 文件或 POWER_AUTOMATE_WEBHOOK_URL 配置。\n"
        "请复制 .env.example 为 .env 并配置 webhook URL。"
    )

class PowerAutomateWebhook:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_message(self, message: str, title: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        headers = {
            'Content-Type': 'application/json'
        }
        
        adaptive_card: Dict[str, Any] = {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.4",
            "body": []
        }
        
        body_list = adaptive_card["body"]
        
        if title:
            body_list.append({
                "type": "TextBlock",
                "text": title,
                "size": "Large",
                "weight": "Bolder"
            })
        
        body_list.append({
            "type": "TextBlock",
            "text": message,
            "wrap": True
        })
        
        payload = adaptive_card
        
        if data:
            payload.update(data)
        
        try:
            response = requests.post(self.webhook_url, headers=headers, json=payload)
            response.raise_for_status()
            return {
                'success': True,
                'status_code': response.status_code,
                'response': response.json() if response.content else None
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }

def main():
    try:
        webhook_url = load_webhook_url()
    except FileNotFoundError as e:
        print(f"错误: {e}")
        sys.exit(1)

    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = """## 📋 任务通知

**项目名称**: 自动化工作流
**状态**: ✅ 已完成
**优先级**: 🔴 高

### 任务详情
- **开始时间**: 2026-01-09 09:00
- **结束时间**: 2026-01-09 12:00
- **负责人**: @Robert

### 完成内容
1. 配置 Power Automate webhook
2. 测试消息发送功能
3. 验证 Markdown 格式支持

> 💡 **提示**: 支持多种 Markdown 格式，包括标题、列表、链接、代码块等。

[查看详情](https://example.com)"""
    
    webhook = PowerAutomateWebhook(webhook_url)
    result = webhook.send_message(message, title="🚀 工作流通知")
    
    if result['success']:
        print(f"消息发送成功！状态码: {result['status_code']}")
        if result['response']:
            print(f"响应: {json.dumps(result['response'], indent=2, ensure_ascii=False)}")
    else:
        print(f"消息发送失败: {result['error']}")
        if result['status_code']:
            print(f"状态码: {result['status_code']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
