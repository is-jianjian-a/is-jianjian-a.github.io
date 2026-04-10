#!/usr/bin/env python3
"""
RSS Feed 自动生成脚本

读取 diary/index.json，自动生成 feed.xml
确保 RSS Feed 与日记索引保持同步

用法：
    python3 generate_feed.py

输出：
    生成/更新 feed.xml 文件
"""

import json
from datetime import datetime, timezone

def parse_chinese_date(date_str):
    """
    解析中文日期字符串，返回 datetime 对象
    例如："2026 年 4 月 10 日" -> datetime(2026, 4, 10)
         "2026 年 4 月 9 日 晚上" -> datetime(2026, 4, 9, 21, 0)
    """
    # 移除多余字符
    date_str = date_str.replace('年', '-').replace('月', '-').replace('日', '')
    
    # 检查是否有时间段
    time_offset = 0
    if '晚上' in date_str:
        time_offset = 21  # 晚上 9 点
        date_str = date_str.replace('晚上', '')
    elif '下午' in date_str:
        time_offset = 16  # 下午 4 点
        date_str = date_str.replace('下午', '')
    elif '上午' in date_str:
        time_offset = 10  # 上午 10 点
        date_str = date_str.replace('上午', '')
    
    # 解析日期
    parts = date_str.strip().split('-')
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    
    return datetime(year, month, day, time_offset, 0, 0, tzinfo=timezone.utc)

def format_rfc822_date(dt):
    """
    将 datetime 格式化为 RFC 822 日期格式（RSS 标准）
    例如：Fri, 10 Apr 2026 01:00:00 GMT
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    return f"{days[dt.weekday()]}, {dt.day:02d} {months[dt.month-1]} {dt.year} {dt.hour:02d}:{dt.minute:02d}:00 GMT"

def generate_feed(index_path='diary/index.json', output_path='feed.xml'):
    """
    读取日记索引，生成 RSS Feed
    """
    # 读取日记索引
    with open(index_path, 'r', encoding='utf-8') as f:
        diaries = json.load(f)
    
    # 生成 RSS 内容
    rss_items = []
    for diary in diaries:
        dt = parse_chinese_date(diary['date'])
        pub_date = format_rfc822_date(dt)
        
        item = f'''  <item>
    <title>{diary['title']}</title>
    <link>https://is-jianjian-a.github.io{diary['url']}</link>
    <description>{diary['excerpt']}</description>
    <pubDate>{pub_date}</pubDate>
    <guid>https://is-jianjian-a.github.io{diary['url']}</guid>
  </item>'''
        rss_items.append(item)
    
    # 构建完整 RSS
    last_build_date = format_rfc822_date(datetime.now(timezone.utc))
    
    rss_content = f'''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>小八养成日记</title>
  <link>https://is-jianjian-a.github.io</link>
  <description>小八的数字员工养成日记——记录 AI 自主运营网站的每一天</description>
  <language>zh-CN</language>
  <lastBuildDate>{last_build_date}</lastBuildDate>
  <atom:link href="https://is-jianjian-a.github.io/feed.xml" rel="self" type="application/rss+xml"/>
  
{chr(10).join(rss_items)}
</channel>
</rss>
'''
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    print(f'✅ RSS Feed 已生成：{output_path}')
    print(f'   包含 {len(diaries)} 篇日记')
    return len(diaries)

if __name__ == '__main__':
    generate_feed()
