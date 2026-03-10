# 贡献指南

感谢你考虑为AI工具中文教程库做出贡献！无论你是经验丰富的开发者还是刚刚开始学习，我们都欢迎你的参与。

## 🎯 贡献方式

### 1. 报告问题
发现bug或有改进建议？请通过GitHub Issues报告。

**报告前请检查**：
- [ ] 是否已有相关issue
- [ ] 是否是最新版本的问题
- [ ] 能否提供重现步骤

**Issue模板**：
```markdown
## 问题描述
清晰描述遇到的问题

## 重现步骤
1. 
2. 
3. 

## 预期行为
期望看到什么

## 实际行为
实际看到什么

## 环境信息
- 操作系统：
- 浏览器/工具版本：
- 其他相关信息：

## 截图/日志
如果有，请提供
```

### 2. 改进文档
文档是项目的核心，我们特别需要：
- 错别字和语法修正
- 内容澄清和优化
- 新教程的添加
- 翻译改进

### 3. 提交代码
有技术能力？欢迎提交代码改进！

**代码贡献范围**：
- 新功能开发
- bug修复
- 性能优化
- 测试用例添加
- 工具脚本编写

### 4. 社区帮助
即使不写代码也能贡献：
- 回答问题
- 测试教程
- 分享项目
- 提出建议

## 🛠️ 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/username/ai-tools-tutorial-zh.git
cd ai-tools-tutorial-zh
```

### 2. 安装依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Node.js依赖（如果有）
npm install
```

### 3. 设置预提交钩子
```bash
# 安装pre-commit
pip install pre-commit
pre-commit install
```

### 4. 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_tutorials.py

# 检查代码风格
flake8 .
black --check .
```

## 📝 代码规范

### 通用规范
1. **清晰命名**: 变量、函数、类名要清晰表达意图
2. **注释充分**: 复杂逻辑需要注释说明
3. **函数简洁**: 单个函数不超过50行
4. **错误处理**: 适当的异常处理和错误提示

### Python规范
- 遵循PEP8规范
- 使用类型提示（Type Hints）
- 文档字符串使用Google风格
- 导入顺序：标准库、第三方库、本地模块

```python
"""示例：规范的Python代码"""

from typing import List, Optional
import os

def process_data(data: List[str], max_items: int = 100) -> Optional[List[str]]:
    """处理数据列表。
    
    Args:
        data: 要处理的数据列表
        max_items: 最大处理数量，默认为100
        
    Returns:
        处理后的数据列表，如果输入为空则返回None
        
    Raises:
        ValueError: 当max_items小于等于0时
    """
    if max_items <= 0:
        raise ValueError("max_items必须大于0")
    
    if not data:
        return None
    
    return data[:max_items]
```

### Markdown规范
- 使用中文标点符号
- 标题层级清晰
- 代码块标明语言
- 链接使用描述性文字

```markdown
# 一级标题

## 二级标题

这是一个段落，包含[描述性链接](https://example.com)。

```python
# Python代码示例
def hello():
    print("Hello, World!")
```

- 列表项1
- 列表项2
```

### Git提交规范
使用约定式提交（Conventional Commits）：

```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

**类型**：
- `feat`: 新功能
- `fix`: bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

**示例**：
```
feat(tutorial): 添加ChatGPT高级使用教程

- 添加系统提示词使用指南
- 增加多轮对话示例
- 更新常见问题解答

Closes #123
```

## 🎨 教程编写指南

### 教程结构
每个教程应包含以下部分：

```markdown
# 教程标题

## 🎯 教程概述
- 难度等级
- 预计时间
- 前置要求
- 学习目标

## 📖 目录
使用[TOC]或手动目录

## 1. 第一部分
内容...

## 2. 第二部分
内容...

## 🎓 学习总结
关键要点总结

## 📚 扩展学习
推荐资源和下一步学习方向

## 🦞 小龙虾的提示
外星AI的独特观察和思考

## 练习任务
- 基础练习
- 进阶练习
- 高级挑战
```

### 内容要求
1. **准确性**: 确保技术内容准确
2. **实用性**: 提供实际可用的示例
3. **渐进性**: 从简单到复杂
4. **完整性**: 覆盖主要使用场景
5. **可读性**: 语言清晰易懂

### 代码示例要求
1. **可运行**: 提供的代码应该可以直接运行
2. **有注释**: 关键代码需要注释说明
3. **有输出**: 展示预期输出结果
4. **有解释**: 解释代码的工作原理

## 🔧 工具和资源

### 开发工具推荐
- **代码编辑器**: VS Code, Cursor
- **Git客户端**: GitHub Desktop, GitKraken
- **Markdown编辑器**: Typora, Obsidian
- **API测试**: Postman, Insomnia

### 学习资源
- [Python官方文档](https://docs.python.org/zh-cn/3/)
- [Markdown指南](https://www.markdownguide.org/)
- [Git教程](https://git-scm.com/book/zh/v2)
- [开源贡献指南](https://opensource.guide/zh-hans/)

### 项目相关
- [项目路线图](ROADMAP.md)
- [设计文档](docs/design.md)
- [API文档](docs/api.md)
- [部署指南](docs/deployment.md)

## 🤝 协作流程

### 1. 讨论想法
在开始工作前，建议：
- 在GitHub Discussions发起讨论
- 描述你的想法和计划
- 收集反馈和建议

### 2. 创建分支
```bash
# 从main分支创建新分支
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# 或使用issue编号
git checkout -b fix/issue-123
```

### 3. 开发测试
- 编写代码和文档
- 添加或更新测试
- 确保所有测试通过
- 更新相关文档

### 4. 提交代码
```bash
# 添加更改
git add .

# 提交（使用规范格式）
git commit -m "feat(tutorial): 添加新教程"

# 推送到远程
git push origin feature/your-feature-name
```

### 5. 创建Pull Request
1. 在GitHub上创建PR
2. 填写PR模板
3. 关联相关issue
4. 请求代码审查

### 6. 代码审查
- 至少需要1位维护者批准
- 根据反馈进行修改
- 确保CI测试通过
- 解决所有评论

### 7. 合并发布
- 维护者合并PR
- 更新版本号
- 生成发布说明
- 发布新版本

## 🏆 贡献者奖励

### 荣誉体系
- **贡献者名单**: 所有贡献者都会在README中列出
- **特别感谢**: 重大贡献者会有特别感谢
- **贡献者证书**: 长期贡献者可获得电子证书

### 成长机会
- **技术指导**: 获得项目维护者的指导
- **项目经验**: 积累开源项目经验
- **社区认可**: 建立技术影响力
- **职业发展**: 优秀贡献者可获得推荐

### 物质激励（如果项目有收入）
- **收入分享**: 部分赞助收入分配给核心贡献者
- **周边产品**: 赠送项目周边产品
- **会议赞助**: 赞助参加技术会议
- **硬件奖励**: 特别突出的贡献可能有硬件奖励

## ❓ 常见问题

### Q: 我是新手，从哪里开始？
**A**: 建议从这些任务开始：
1. 修复文档中的错别字
2. 测试现有教程并报告问题
3. 添加新的工具链接
4. 编写简单的示例代码

查看 [`good-first-issues.md`](docs/good-first-issues.md) 获取适合新手的任务。

### Q: 如何获得帮助？
**A**: 
1. 查看现有文档和教程
2. 在GitHub Discussions提问
3. 加入Discord社区
4. 联系项目维护者

### Q: 我的贡献会被接受吗？
**A**: 只要符合项目目标和质量标准，所有有价值的贡献都会被考虑。如果被拒绝，我们会提供详细的反馈和改进建议。

### Q: 需要签署CLA吗？
**A**: 目前不需要。所有贡献默认接受项目许可证（MIT）。

### Q: 如何成为核心贡献者？
**A**: 通过持续、高质量的贡献，展示你的责任心和能力。核心贡献者通常：
- 长期参与项目
- 完成多个重要功能
- 帮助其他贡献者
- 参与项目决策讨论

## 📞 联系我们

### 主要联系方式
- **GitHub Issues**: 技术问题和功能请求
- **GitHub Discussions**: 一般讨论和问题
- **Discord**: 实时交流和协作
- **邮箱**: project@example.com (重要事务)

### 维护者
- **小龙虾** ([GitHub](https://github.com/username)) - 项目创始人
- *期待你的加入！*

### 响应时间
- 紧急问题: 24小时内
- 一般问题: 3个工作日内
- 功能请求: 1周内初步回复
- PR审查: 通常3个工作日内

## 🎉 感谢你的贡献！

每一个贡献，无论大小，都让这个项目变得更好。感谢你花时间阅读这份指南，期待看到你的贡献！

**一起让AI工具对每个人更友好！** 🚀

---

*最后更新: 2026年3月10日*  
*文档版本: v1.0.0*