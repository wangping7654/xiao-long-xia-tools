import requests
import json
import datetime

def analyze_paperclip():
    print("=== 分析 Paperclip AI 项目 ===")
    print("=" * 60)
    
    # GitHub API 地址
    repo_url = "https://api.github.com/repos/paperclipai/paperclip"
    readme_url = "https://api.github.com/repos/paperclipai/paperclip/readme"
    
    try:
        # 获取仓库信息
        print("1. 获取项目基本信息...")
        repo_response = requests.get(repo_url, headers={'Accept': 'application/vnd.github.v3+json'})
        repo_data = repo_response.json()
        
        if 'message' in repo_data and repo_data['message'] == 'Not Found':
            print("❌ 项目不存在或无法访问")
            return
        
        # 基本信息
        print(f"✅ 项目名称: {repo_data.get('full_name', 'N/A')}")
        print(f"✅ 描述: {repo_data.get('description', 'N/A')}")
        print(f"✅ Stars: {repo_data.get('stargazers_count', 'N/A')}")
        print(f"✅ Forks: {repo_data.get('forks_count', 'N/A')}")
        print(f"✅ 创建时间: {repo_data.get('created_at', 'N/A')}")
        print(f"✅ 更新时间: {repo_data.get('updated_at', 'N/A')}")
        print(f"✅ 语言: {repo_data.get('language', 'N/A')}")
        print(f"✅ Topics: {', '.join(repo_data.get('topics', []))}")
        
        # 计算创建天数
        created_at = repo_data.get('created_at', '')
        if created_at:
            created_date = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            days_ago = (datetime.datetime.now(datetime.timezone.utc) - created_date).days
            print(f"✅ 创建于 {days_ago} 天前")
        
        # 获取README
        print("\n2. 获取项目README...")
        readme_response = requests.get(readme_url, headers={'Accept': 'application/vnd.github.v3+json'})
        
        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            readme_content = readme_data.get('content', '')
            if readme_content:
                # 简单的base64解码
                import base64
                decoded_content = base64.b64decode(readme_content).decode('utf-8')
                print("✅ README内容（前1000字符）:")
                print("-" * 40)
                print(decoded_content[:1000])
                print("-" * 40)
        
        # 分析项目类型
        print("\n3. 项目类型分析...")
        description = repo_data.get('description', '').lower()
        topics = [t.lower() for t in repo_data.get('topics', [])]
        
        ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt', 'claude']
        automation_keywords = ['automation', 'autonomous', 'auto', 'robot', 'bot']
        company_keywords = ['company', 'business', 'enterprise', 'startup', 'revenue']
        agent_keywords = ['agent', 'multi-agent', 'crew', 'autogen']
        
        ai_score = sum(1 for kw in ai_keywords if kw in description or any(kw in t for t in topics))
        automation_score = sum(1 for kw in automation_keywords if kw in description or any(kw in t for t in topics))
        company_score = sum(1 for kw in company_keywords if kw in description or any(kw in t for t in topics))
        agent_score = sum(1 for kw in agent_keywords if kw in description or any(kw in t for t in topics))
        
        print(f"AI相关度: {ai_score}/6")
        print(f"自动化相关度: {automation_score}/5")
        print(f"公司/业务相关度: {company_score}/5")
        print(f"Agent相关度: {agent_score}/4")
        
        # 总体评估
        total_score = ai_score + automation_score + company_score + agent_score
        max_score = 20
        score_percentage = (total_score / max_score) * 100
        
        print(f"\n4. 总体匹配度: {score_percentage:.1f}%")
        
        if score_percentage >= 70:
            print("✅ 高匹配度 - 很可能就是文章提到的项目")
        elif score_percentage >= 40:
            print("⚠️ 中等匹配度 - 需要进一步确认")
        else:
            print("❌ 低匹配度 - 可能不是目标项目")
            
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")

if __name__ == "__main__":
    analyze_paperclip()