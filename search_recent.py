import requests
import json
import datetime

# 搜索最近3天创建的项目
three_days_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
url = f'https://api.github.com/search/repositories?q=created:>{three_days_ago}+stars:>10000&sort=stars&order=desc&per_page=10'

try:
    r = requests.get(url, headers={'Accept': 'application/vnd.github.v3+json'})
    data = r.json()
    print('最近3天创建且stars>10k的项目:')
    for item in data.get('items', []):
        print(f'  {item["full_name"]}: {item["stargazers_count"]} stars, 创建于: {item["created_at"]}')
        print(f'    描述: {item.get("description", "无描述")}')
        print(f'    URL: {item["html_url"]}')
        print()
except Exception as e:
    print(f'错误: {e}')