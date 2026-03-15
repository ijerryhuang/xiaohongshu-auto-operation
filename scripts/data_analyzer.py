#!/usr/bin/env python3
"""
小红书数据分析脚本
抓取账号所有笔记数据并生成报告
"""

import asyncio
import json
import re
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("⚠️ Playwright not installed. Run: pip install playwright && playwright install chromium")
    exit(1)

# 配置
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "xhs_data"
COOKIES_FILE = DATA_DIR / "xhs_cookies.json"
REPORT_FILE = DATA_DIR / "latest_report.txt"

async def fetch_data():
    """抓取小红书数据"""
    print(f"🚀 开始抓取数据... {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    if not COOKIES_FILE.exists():
        print("❌ Cookie 文件不存在，请先登录")
        return None
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        # 加载 cookies
        with open(COOKIES_FILE, 'r') as f:
            cookies = json.load(f)
            await context.add_cookies(cookies)
        
        page = await context.new_page()
        
        try:
            # 访问创作者中心
            await page.goto('https://creator.xiaohongshu.com/creator/home', timeout=30000)
            await page.wait_for_timeout(3000)
            
            # 抓取数据
            notes_data = await page.evaluate('''() => {
                const notes = [];
                document.querySelectorAll('.note-item').forEach(item => {
                    notes.push({
                        title: item.querySelector('.title')?.textContent || '',
                        views: item.querySelector('.views')?.textContent || '0',
                        likes: item.querySelector('.likes')?.textContent || '0',
                        collects: item.querySelector('.collects')?.textContent || '0',
                        comments: item.querySelector('.comments')?.textContent || '0'
                    });
                });
                return notes;
            }''')
            
            await browser.close()
            return notes_data
            
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            await browser.close()
            return None

def generate_report(data):
    """生成数据报告"""
    if not data:
        return "❌ 无数据"
    
    report = f"""
📊 小红书数据报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

📈 总体数据
- 笔记总数: {len(data)}
- 总阅读: {sum(int(n.get('views', '0').replace(',', '')) for n in data)}
- 总点赞: {sum(int(n.get('likes', '0').replace(',', '')) for n in data)}
- 总收藏: {sum(int(n.get('collects', '0').replace(',', '')) for n in data)}
- 总评论: {sum(int(n.get('comments', '0').replace(',', '')) for n in data)}

📝 最新笔记
"""
    
    for i, note in enumerate(data[:5], 1):
        report += f"\n{i}. {note.get('title', '无标题')}\n"
        report += f"   阅读: {note.get('views', '0')} | 点赞: {note.get('likes', '0')} | 收藏: {note.get('collects', '0')}\n"
    
    return report

async def main():
    """主函数"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    data = await fetch_data()
    report = generate_report(data)
    
    # 保存报告
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    return report

if __name__ == "__main__":
    asyncio.run(main())
