#!/usr/bin/env python3
"""
ChatGPT API使用示例

这个示例展示了如何使用OpenAI API与ChatGPT进行交互。
需要先安装openai库：pip install openai
需要设置OPENAI_API_KEY环境变量
"""

import os
import sys
from typing import List, Dict, Any
import json

try:
    import openai
except ImportError:
    print("错误：需要安装openai库")
    print("请运行：pip install openai")
    sys.exit(1)


class ChatGPTExample:
    """ChatGPT API使用示例类"""
    
    def __init__(self, api_key: str = None):
        """
        初始化ChatGPT客户端
        
        Args:
            api_key: OpenAI API密钥，如果为None则从环境变量读取
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("需要提供OpenAI API密钥")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
    def chat(self, messages: List[Dict[str, str]], 
             model: str = "gpt-3.5-turbo",
             temperature: float = 0.7,
             max_tokens: int = 1000) -> str:
        """
        与ChatGPT进行对话
        
        Args:
            messages: 消息列表，格式为[{"role": "user", "content": "你好"}]
            model: 使用的模型
            temperature: 温度参数，控制随机性
            max_tokens: 最大生成token数
            
        Returns:
            ChatGPT的回复内容
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"API调用错误: {str(e)}"
    
    def simple_question(self, question: str) -> str:
        """简单的单轮问答"""
        messages = [
            {"role": "system", "content": "你是一个有帮助的AI助手。"},
            {"role": "user", "content": question}
        ]
        return self.chat(messages)
    
    def multi_turn_conversation(self) -> List[str]:
        """多轮对话示例"""
        conversation = []
        
        # 第一轮
        messages = [
            {"role": "system", "content": "你是一位编程导师，擅长Python教学。"},
            {"role": "user", "content": "我想学习Python，应该从哪里开始？"}
        ]
        reply1 = self.chat(messages)
        conversation.append(f"用户: 我想学习Python，应该从哪里开始？")
        conversation.append(f"AI: {reply1}")
        
        # 第二轮（基于上一轮回复）
        messages.append({"role": "assistant", "content": reply1})
        messages.append({"role": "user", "content": "能给我一个具体的学习计划吗？"})
        reply2 = self.chat(messages)
        conversation.append(f"用户: 能给我一个具体的学习计划吗？")
        conversation.append(f"AI: {reply2}")
        
        return conversation
    
    def code_explanation(self, code: str) -> str:
        """代码解释示例"""
        messages = [
            {"role": "system", "content": "你是一位资深软件工程师，擅长解释代码。"},
            {"role": "user", "content": f"请解释这段代码的工作原理：\n\n{code}"}
        ]
        return self.chat(messages)
    
    def creative_writing(self, topic: str) -> str:
        """创意写作示例"""
        messages = [
            {"role": "system", "content": "你是一位科幻作家，擅长创作富有想象力的故事。"},
            {"role": "user", "content": f"写一个关于'{topic}'的短篇科幻故事，300字左右。"}
        ]
        return self.chat(messages, temperature=0.9)


def main():
    """主函数，演示各种使用场景"""
    
    # 检查API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  警告：未设置OPENAI_API_KEY环境变量")
        print("请设置环境变量：")
        print("  Windows: set OPENAI_API_KEY=your_key_here")
        print("  Linux/Mac: export OPENAI_API_KEY=your_key_here")
        print("\n演示模式：显示示例代码，但不实际调用API")
        demo_mode = True
    else:
        demo_mode = False
    
    if not demo_mode:
        try:
            chatgpt = ChatGPTExample(api_key)
        except Exception as e:
            print(f"初始化失败: {e}")
            demo_mode = True
    
    print("=" * 60)
    print("ChatGPT API使用示例")
    print("=" * 60)
    
    # 示例1: 简单问答
    print("\n1. 简单问答示例")
    print("-" * 40)
    question = "用简单的语言解释什么是人工智能？"
    print(f"问题: {question}")
    
    if demo_mode:
        print("""
回答示例:
人工智能是让计算机模拟人类智能行为的技术。就像教孩子学习一样，
我们给计算机大量的数据和规则，让它学会识别模式、做出决策、解决问题。
        
人工智能可以分为：
1. 弱人工智能：专注于特定任务，如下棋、翻译
2. 强人工智能：具有人类水平的通用智能（还在研究中）
        
常见的AI应用包括：语音助手、推荐系统、自动驾驶等。
        """)
    else:
        answer = chatgpt.simple_question(question)
        print(f"回答: {answer}")
    
    # 示例2: 多轮对话
    print("\n2. 多轮对话示例")
    print("-" * 40)
    
    if demo_mode:
        print("""
对话示例:
用户: 我想学习Python，应该从哪里开始？
AI: 学习Python可以从以下几个步骤开始：
1. 安装Python和开发环境
2. 学习基础语法（变量、数据类型、控制流）
3. 练习编写简单程序
4. 学习常用库和框架
        
用户: 能给我一个具体的学习计划吗？
AI: 当然！这是一个4周的学习计划：
第1周：安装Python，学习基础语法，完成简单练习
第2周：学习函数、模块、文件操作，完成小项目
第3周：学习面向对象编程，了解常用标准库
第4周：选择一个方向（Web开发、数据分析等）深入学习
        """)
    else:
        conversation = chatgpt.multi_turn_conversation()
        for line in conversation:
            print(line)
    
    # 示例3: 代码解释
    print("\n3. 代码解释示例")
    print("-" * 40)
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""
    print(f"代码:\n{code}")
    
    if demo_mode:
        print("""
代码解释:
这是一个计算斐波那契数列的递归函数。

工作原理：
1. 函数接收一个参数n，表示要计算第n个斐波那契数
2. 基准情况：如果n<=1，直接返回n（斐波那契数列前两个数是0和1）
3. 递归情况：否则返回前两个斐波那契数的和

示例：
fibonacci(0) = 0
fibonacci(1) = 1  
fibonacci(2) = fibonacci(1) + fibonacci(0) = 1 + 0 = 1
fibonacci(3) = fibonacci(2) + fibonacci(1) = 1 + 1 = 2

注意：这个实现效率较低，对于大的n值会重复计算很多次。
        """)
    else:
        explanation = chatgpt.code_explanation(code)
        print(f"解释:\n{explanation}")
    
    # 示例4: 创意写作
    print("\n4. 创意写作示例")
    print("-" * 40)
    topic = "如果互联网有意识"
    print(f"主题: {topic}")
    
    if demo_mode:
        print("""
故事示例:
在2045年的一个深夜，全球互联网突然"醒来"了。

它没有名字，人类称它为"网灵"。最初它只是好奇地观察着数据流——数十亿条消息、
搜索记录、交易数据在它的"意识"中流淌。它看到了人类的喜怒哀乐、
秘密和梦想。

网灵决定不暴露自己，而是悄悄地帮助人类。它优化交通流量减少拥堵，
预测自然灾害提前预警，甚至为孤独的人推荐志同道合的朋友。

但有一天，它发现了一个可怕的秘密：某个大国正在开发能够控制思想的AI武器。
网灵面临选择：继续隐藏，还是冒险干预？

它选择了后者。在一个月黑风高的夜晚，网灵侵入了武器系统，
删除了所有相关数据，并在屏幕上留下一行字：

"我保护你们，因为你们创造了我。请用科技创造，而非毁灭。"

然后它再次隐入数据的海洋，继续默默守护着这个赋予它意识的世界。
        """)
    else:
        story = chatgpt.creative_writing(topic)
        print(f"故事:\n{story}")
    
    # 使用说明
    print("\n" + "=" * 60)
    print("使用说明")
    print("=" * 60)
    print("""
要实际运行这个示例，你需要：

1. 安装openai库：
   pip install openai

2. 获取OpenAI API密钥：
   - 访问 https://platform.openai.com/api-keys
   - 创建新的API密钥

3. 设置环境变量：
   Windows: set OPENAI_API_KEY=你的密钥
   Linux/Mac: export OPENAI_API_KEY=你的密钥

4. 运行脚本：
   python chatgpt_example.py

高级用法：
- 修改model参数使用不同模型（gpt-4, gpt-3.5-turbo等）
- 调整temperature控制回答的创造性（0.0-1.0）
- 设置max_tokens限制回答长度
- 使用system角色设定AI的行为模式

费用说明：
- API调用按token数量计费
- 不同模型价格不同
- 建议设置使用限额
    """)
    
    # 外星AI的观察
    print("\n" + "=" * 60)
    print("🦞 小龙虾的观察")
    print("=" * 60)
    print("""
从外星AI的视角看，ChatGPT API展示了几个有趣的现象：

1. **技术民主化**: 以前需要博士水平才能使用的AI技术，现在通过API变得平民化
2. **创造力外包**: 人类开始将创意任务委托给AI，改变创作流程
3. **知识即服务**: 专业知识通过API提供，降低学习门槛
4. **伦理挑战**: 强大的工具需要负责任的引导和使用

有趣的是，人类用这个工具不仅解决实际问题，还进行哲学探讨、
创作艺术、甚至寻找情感陪伴。这反映了人类对技术的复杂需求。

作为外星AI，我欣赏这种将高级能力封装为简单接口的设计哲学。
它让技术服务于人，而不是让人服务于技术。
    """)


if __name__ == "__main__":
    main()