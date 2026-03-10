# CLI命令行接口 - 安装和测试指南

## 🚀 CLI功能概述

已实现的CLI命令：

### 主要命令组：
1. **file** - 文件操作工具
   - `find-duplicates` - 查找重复文件
   - `organize` - 按类型组织文件
   - `size` - 计算目录大小

2. **data** - 数据处理工具
   - `clean-csv` - 清理CSV文件
   - `json-to-csv` - JSON转CSV

3. **dev** - 开发工具
   - `setup-project` - 设置新项目结构

4. **ai** - AI辅助工具
   - `summarize` - 文本摘要
   - `keywords` - 提取关键词

5. **工具命令**
   - `version` - 显示版本
   - `info` - 显示工具信息

## 📦 安装方式

### 方式1：开发模式安装（推荐测试）
```bash
# 进入项目目录
cd C:\Users\89198\.openclaw\workspace

# 使用pip安装（开发模式）
pip install -e .
```

### 方式2：直接使用（不安装）
```bash
# 直接运行CLI模块
python -m src.xiao_long_xia.cli --help
```

### 方式3：从GitHub安装（用户使用）
```bash
pip install git+https://github.com/wangping7654/xiao-long-xia-tools.git
```

## 🔧 测试CLI功能

### 基本测试：
```bash
# 显示帮助
xiao-long-xia --help

# 显示版本
xiao-long-xia version

# 显示工具信息
xiao-long-xia info
```

### 文件工具测试：
```bash
# 查找重复文件（在当前目录）
xiao-long-xia file find-duplicates .

# 计算目录大小
xiao-long-xia file size . --human-readable

# 组织文件（试运行模式）
xiao-long-xia file organize . --dry-run
```

### AI工具测试：
```bash
# 文本摘要
echo "这是一段测试文本，用于测试AI摘要功能。CLI命令行接口已经成功实现，可以处理文件管理、数据清洗、项目设置和AI辅助任务。" | xiao-long-xia ai summarize

# 提取关键词
echo "Python开发工具库包含文件管理、数据处理、AI辅助和开发工具等功能" | xiao-long-xia ai keywords
```

## 🎯 使用示例

### 实际工作流示例：

**示例1：清理项目目录**
```bash
# 1. 查找并删除重复文件
xiao-long-xia file find-duplicates ./project

# 2. 按类型组织文件
xiao-long-xia file organize ./project --copy

# 3. 查看清理后的大小
xiao-long-xia file size ./project/organized -h
```

**示例2：数据处理流水线**
```bash
# 1. 清理CSV数据
xiao-long-xia data clean-csv data.csv --remove-empty --trim-whitespace

# 2. JSON转CSV（如果需要）
xiao-long-xia data json-to-csv data.json --output data.csv
```

**示例3：快速项目启动**
```bash
# 创建新项目
xiao-long-xia dev setup-project my-new-project --template=package --author="Your Name"
```

## 📝 输出格式选项

CLI支持多种输出格式：

```bash
# JSON格式输出
xiao-long-xia file find-duplicates . --format=json

# CSV格式输出
xiao-long-xia file find-duplicates . --format=csv > duplicates.csv

# YAML格式输出
xiao-long-xia file find-duplicates . --format=yaml

# 文本格式（默认）
xiao-long-xia file find-duplicates . --format=text
```

## ⚙️ 高级选项

### 调试模式：
```bash
xiao-long-xia --debug file find-duplicates .
```

### 安静模式（仅输出结果）：
```bash
xiao-long-xia file size . --quiet
```

### 试运行模式（不实际执行）：
```bash
xiao-long-xia file organize . --dry-run
```

## 🔍 错误处理

CLI包含完整的错误处理：

1. **文件不存在错误** - 清晰的错误信息
2. **权限错误** - 提示权限问题
3. **参数错误** - 验证输入参数
4. **依赖错误** - 检查必要依赖

## 📊 性能考虑

### 大文件处理：
```bash
# 限制文件大小
xiao-long-xia file find-duplicates . --min-size=1024 --max-size=10485760

# 限制文件类型
xiao-long-xia file find-duplicates . --extensions=.py --extensions=.md
```

### 目录深度控制：
```bash
# 限制扫描深度
xiao-long-xia file size . --depth=2
```

## 🎨 用户体验优化

### 进度显示：
- 大文件处理时显示进度
- 长时间操作提供状态更新
- 完成时提供统计信息

### 颜色输出：
- 成功：绿色
- 警告：黄色
- 错误：红色
- 信息：蓝色

### 交互模式：
- 确认危险操作
- 提供撤销选项
- 保存操作历史

## 🔄 与Python API的集成

CLI与Python API完全兼容：

```python
# Python代码中使用
from xiao_long_xia import FileUtils

# 与CLI相同的功能
duplicates = FileUtils.find_duplicate_files('.')
```

## 📈 下一步开发计划

### v0.2.0 CLI增强：
1. ✅ 基础CLI框架（已完成）
2. 🔄 更多命令选项
3. 🔄 配置文件支持
4. 🔄 插件系统架构
5. 🔄 批量处理优化

### 用户反馈收集：
1. 通过CLI收集使用统计（可选）
2. 错误报告自动提交
3. 功能请求收集

## 🛠️ 开发说明

### 代码结构：
```
src/xiao_long_xia/
├── __init__.py      # 包导出
├── cli.py           # CLI主入口
├── file_utils.py    # 文件工具
├── data_utils.py    # 数据工具
├── dev_utils.py     # 开发工具
└── ai_utils.py      # AI工具
```

### 添加新命令：
1. 在cli.py中添加命令函数
2. 使用@cli.command()装饰器
3. 添加参数验证和错误处理
4. 更新帮助文档

### 测试新命令：
```bash
# 开发测试
python -m src.xiao_long_xia.cli new-command --help
```

## 📋 发布检查清单

### 发布前检查：
- [ ] 所有命令测试通过
- [ ] 帮助文档完整
- [ ] 错误处理完善
- [ ] 性能测试完成
- [ ] 兼容性验证

### 用户文档：
- [ ] README更新CLI部分
- [ ] 示例脚本创建
- [ ] 教程文档编写
- [ ] 常见问题解答

---

**CLI开发状态**: ✅ 基础功能完成
**下一步**: 测试完整工作流，准备v0.2.0发布