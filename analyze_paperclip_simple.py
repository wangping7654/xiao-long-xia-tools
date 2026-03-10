import requests
import json
import datetime
import base64

def analyze_paperclip():
    print("=== 分析 Paperclip AI 项目 ===")
    print("=" * 60)
    
    # GitHub API 地址
    repo_url = "https://api.github.com/repos/paperclipai/paperclip"
    
    try:
        # 获取仓库信息
        print("1. 获取项目基本信息...")
        repo_response = requests.get(repo_url, headers={'Accept': 'application/vnd.github.v3+json'})
        repo_data = repo_response.json()
        
        if 'message' in repo_data and repo_data['message'] == 'Not Found':
            print("ERROR: 项目不存在或无法访问")
            return
        
        # 基本信息
        print(f"项目名称: {repo_data.get('full_name', 'N/A')}")
        print(f"描述: {repo_data.get('description', 'N/A')}")
        print(f"Stars: {repo_data.get('stargazers_count', 'N/A')}")
        print(f"Forks: {repo_data.get('forks_count', 'N/A')}")
        print(f"创建时间: {repo_data.get('created_at', 'N/A')}")
        print(f"更新时间: {repo_data.get('updated_at', 'N/A')}")
        print(f"语言: {repo_data.get('language', 'N/A')}")
        
        topics = repo_data.get('topics', [])
        if topics:
            print(f"Topics: {', '.join(topics)}")
        
        # 计算创建天数
        created_at = repo_data.get('created_at', '')
        if created_at:
            created_date = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            days_ago = (datetime.datetime.now(datetime.timezone.utc) - created_date).days
            print(f"创建于 {days_ago} 天前")
            
            # 检查是否3天内
            if days_ago <= 3:
                print("INFO: 项目在3天内创建，符合文章描述")
            else:
                print(f"INFO: 项目创建超过3天 ({days_ago}天)")
        
        # 检查stars数量
        stars = repo_data.get('stargazers_count', 0)
        if 12000 <= stars <= 15000:
            print(f"INFO: Stars数量 {stars} 接近12.8k，符合文章描述")
        else:
            print(f"INFO: Stars数量 {stars}，与12.8k有差异")
        
        # 分析项目描述
        description = repo_data.get('description', '').lower()
        print(f"\n2. 项目描述分析: {description}")
        
        # 关键词匹配
        keywords = {
            'ai': ['ai', 'artificial intelligence', 'machine learning', 'llm'],
            'automation': ['automation', 'autonomous', 'auto'],
            'company': ['company', 'business', 'enterprise', 'startup'],
            'agent': ['agent', 'multi-agent', 'crew', 'autogen'],
            'revenue': ['revenue', 'income', 'profit', 'money']
        }
        
        matches = {}
        for category, words in keywords.items():
            matches[category] = sum(1 for word in words if word in description)
        
        print("\n3. 关键词匹配结果:")
        for category, count in matches.items():
            print(f"  {category}: {count}个关键词匹配")
        
        # 总体评估
        total_matches = sum(matches.values())
        print(f"\n4. 总体匹配度: {total_matches}个关键词匹配")
        
        if total_matches >= 3:
            print("结论: 很可能是文章提到的项目")
        elif total_matches >= 1:
            print("结论: 可能是相关项目，需要进一步确认")
        else:
            print("结论: 可能不是目标项目")
            
        # 获取README简要内容
        print("\n5. 尝试获取README...")
        readme_url = "https://api.github.com/repos/paperclipai/paperclip/readme"
        readme_response = requests.get(readme_url, headers={'Accept': 'application/vnd.github.v3+json'})
        
        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            readme_content = readme_data.get('content', '')
            if readme_content:
                decoded_content = base64.b64decode(readme_content).decode('utf-8')
                # 提取前几行
                lines = decoded_content.split('\n')[:10]
                print("README前10行:")
                for line in lines:
                    if line.strip():
                        print(f"  {line}")
        
        print("\n" + "=" * 60)
        print("分析完成")
            
    except Exception as e:
        print(f"ERROR: 分析过程中出错: {e}")

if __name__ == "__main__":
    analyze_paperclip()