#!/usr/bin/env python3
"""
小红书每日数据抓取 - 创作者后台版
直接访问创作者中心获取完整数据
"""

import asyncio
import json
import re
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("⚠️ Playwright not installed")
    exit(1)

DATA_DIR = Path.home() / ".openclaw" / "workspace" / "xhs_data"
COOKIES_FILE = DATA_DIR / "xhs_cookies.json"
REPORT_FILE = DATA_DIR / "latest_report.txt"

async def fetch_creator_data():
    """从创作者中心抓取数据"""
    print(f"🚀 开始抓取创作者数据... {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    if not COOKIES_FILE.exists():
        print("❌ Cookie 文件不存在")
        return None
    
    async with async_playwright() as p:
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        browser = await p.chromium.launch(
            headless=True,
            executable_path=chrome_path if Path(chrome_path).exists() else None
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 加载 cookies
        with open(COOKIES_FILE, 'r') as f:
            cookies = json.load(f)
            await context.add_cookies(cookies)
        
        page = await context.new_page()
        
        try:
            # 直接访问创作者中心首页
            print("📱 访问创作者中心...")
            await page.goto("https://creator.xiaohongshu.com/creator/home", timeout=60000)
            await asyncio.sleep(5)
            
            # 检查是否需要登录
            current_url = page.url
            if "login" in current_url.lower():
                print("⚠️ 需要重新登录")
                await browser.close()
                return {"error": "需要重新登录"}
            
            print("✅ 已进入创作者中心")
            
            # 截图
            screenshot = DATA_DIR / f"creator_{datetime.now().strftime('%H%M%S')}.png"
            await page.screenshot(path=str(screenshot), full_page=True)
            print(f"📸 截图已保存: {screenshot.name}")
            
            # 等待数据加载
            await asyncio.sleep(3)
            
            # 提取数据
            data = {
                "fans": "N/A",
                "notes": "N/A",
                "views_total": "N/A",
                "likes_total": "N/A",
                "collects_total": "N/A",
                "comments_total": "N/A",
                "views_yesterday": "N/A",
                "likes_yesterday": "N/A",
                "fetch_time": datetime.now().isoformat()
            }
            
            # 方法1：从页面元素提取
            print("📊 提取数据...")
            
            try:
                # 提取粉丝数
                fans_elem = await page.query_selector('[class*="fans"], [class*="follower"]')
                if fans_elem:
                    fans_text = await fans_elem.inner_text()
                    fans_match = re.search(r'(\d+)', fans_text)
                    if fans_match:
                        data['fans'] = fans_match.group(1)
                        print(f"   粉丝: {data['fans']}")
            except Exception as e:
                print(f"   ⚠️ 提取粉丝数失败: {e}")
            
            try:
                # 提取笔记数
                notes_elem = await page.query_selector('[class*="note-count"], [class*="post-count"]')
                if notes_elem:
                    notes_text = await notes_elem.inner_text()
                    notes_match = re.search(r'(\d+)', notes_text)
                    if notes_match:
                        data['notes'] = notes_match.group(1)
                        print(f"   笔记: {data['notes']}")
            except Exception as e:
                print(f"   ⚠️ 提取笔记数失败: {e}")
            
            # 方法2：从页面文本提取
            page_text = await page.evaluate('() => document.body.innerText')
            
            # 保存页面文本用于调试
            debug_file = DATA_DIR / f"creator_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(page_text)
            print(f"📝 页面文本已保存: {debug_file.name}")
            
            # 尝试从文本中提取数据
            patterns = {
                'fans': [r'粉丝[：:]\s*(\d+)', r'(\d+)\s*粉丝'],
                'notes': [r'笔记[：:]\s*(\d+)', r'(\d+)\s*笔记'],
                'views_total': [r'总阅读[：:]\s*(\d+)', r'阅读[：:]\s*(\d+)'],
                'likes_total': [r'总点赞[：:]\s*(\d+)', r'点赞[：:]\s*(\d+)'],
                'collects_total': [r'总收藏[：:]\s*(\d+)', r'收藏[：:]\s*(\d+)'],
            }
            
            for key, pattern_list in patterns.items():
                if data[key] == "N/A":
                    for pattern in pattern_list:
                        match = re.search(pattern, page_text)
                        if match:
                            data[key] = match.group(1)
                            print(f"   {key}: {data[key]}")
                            break
            
            # 方法3：尝试从 API 请求中获取数据
            print("🔍 监听网络请求...")
            
            # 刷新页面并监听请求
            api_data = {}
            
            async def handle_response(response):
                if 'api' in response.url and response.status == 200:
                    try:
                        json_data = await response.json()
                        api_data.update(json_data)
                    except:
                        pass
            
            page.on('response', handle_response)
            
            # 刷新页面触发 API 请求
            await page.reload()
            await asyncio.sleep(5)
            
            # 从 API 数据中提取
            if api_data:
                print("✅ 从 API 获取到数据")
                # 根据实际 API 结构提取数据
                # 这里需要根据实际抓到的 API 响应调整
            
            print(f"✅ 数据抓取完成")
            print(f"   粉丝: {data['fans']}")
            print(f"   笔记: {data['notes']}")
            print(f"   总阅读: {data['views_total']}")
            print(f"   总点赞: {data['likes_total']}")
            
            await browser.close()
            return data
            
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 保存错误截图
            try:
                error_screenshot = DATA_DIR / f"error_{datetime.now().strftime('%H%M%S')}.png"
                await page.screenshot(path=str(error_screenshot))
                print(f"📸 错误截图已保存: {error_screenshot.name}")
            except:
                pass
            
            await browser.close()
            return None

def generate_report(data):
    """生成数据报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if not data:
        report = f"""📊 小红书日报 [{today}]
━━━━━━━━━━━━━━━━━━━━━━
❌ 数据抓取失败

⏰ 尝试时间：{datetime.now().strftime("%H:%M")}

💡 可能原因：
- 登录状态过期
- 页面结构变化
- 网络连接问题

🔧 建议：
- 访问 http://localhost:18060 重新登录
- 检查 MCP 服务状态
- 查看错误截图
"""
        return report
    
    if data.get("error"):
        report = f"""📊 小红书日报 [{today}]
━━━━━━━━━━━━━━━━━━━━━━
⚠️ {data['error']}

🔧 解决方法：
1. 访问 http://localhost:18060
2. 点击"重新登录"
3. 扫码登录小红书
4. 等待下次自动抓取（22:00）
"""
        return report
    
    report = f"""📊 小红书日报 [{today}]
━━━━━━━━━━━━━━━━━━━━━━

📈 账号数据
👥 粉丝：{data.get('fans', 'N/A')}
📝 笔记数：{data.get('notes', 'N/A')}

📊 总体数据
👀 总阅读：{data.get('views_total', 'N/A')}
❤️ 总点赞：{data.get('likes_total', 'N/A')}
⭐ 总收藏：{data.get('collects_total', 'N/A')}
💬 总评论：{data.get('comments_total', 'N/A')}

📅 昨日数据
👀 昨日阅读：{data.get('views_yesterday', 'N/A')}
❤️ 昨日点赞：{data.get('likes_yesterday', 'N/A')}

⏰ 数据时间：{datetime.now().strftime("%H:%M")}

💡 提示：数据来自创作者中心
"""
    return report

async def save_to_obsidian(data):
    """保存数据到 Obsidian"""
    try:
        obsidian_path = Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/JerryHunag WorkSpace/Obsidian Vault/小红书/数据运营"
        obsidian_path.mkdir(parents=True, exist_ok=True)
        
        today = datetime.now().strftime("%Y-%m-%d")
        report_file = obsidian_path / f"{today}.md"
        
        report = generate_report(data)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# 小红书数据报告 - {today}\n\n")
            f.write(report)
            f.write("\n\n---\n")
            f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"✅ 报告已保存到 Obsidian: {report_file.name}")
        
    except Exception as e:
        print(f"⚠️ 保存到 Obsidian 失败: {e}")

async def main():
    print("=" * 50)
    print("小红书每日数据抓取 - 创作者后台版")
    print("=" * 50)
    
    # 确保数据目录存在
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    data = await fetch_creator_data()
    
    if data:
        # 保存数据
        today = datetime.now().strftime("%Y-%m-%d")
        stats_file = DATA_DIR / f"stats_{today}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # 生成并保存报告
        report = generate_report(data)
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 保存到 Obsidian
        await save_to_obsidian(data)
        
        print("\n" + report)
        print("\n✅ 报告已保存到:", REPORT_FILE)
    else:
        print("\n❌ 抓取失败")
        report = generate_report(None)
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(report)
        print(report)

if __name__ == "__main__":
    asyncio.run(main())
