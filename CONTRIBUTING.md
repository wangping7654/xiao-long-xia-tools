# 贡献指南

欢迎为 Xiao Long Xia Tools 贡献代码！本指南将帮助你开始贡献。

## 行为准则

请尊重所有贡献者，保持友好和专业的交流环境。

## 如何贡献

### 1. 报告问题

如果你发现bug或有功能建议，请先检查是否已有相关issue。如果没有，请创建新issue：

- **Bug报告**：描述问题、复现步骤、期望行为、实际行为
- **功能建议**：描述功能、使用场景、预期收益

### 2. 开发环境设置

#### 克隆仓库
```bash
git clone https://github.com/wangping7654/xiao-long-xia-tools.git
cd xiao-long-xia-tools
```

#### 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### 安装开发依赖
```bash
pip install -e ".[dev]"
```

### 3. 开发流程

#### 创建功能分支
```bash
git checkout -b feature/你的功能名称
```

#### 编写代码
- 遵循代码规范（见下文）
- 添加类型提示
- 编写文档字符串
- 添加测试

#### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_file_utils.py

# 生成覆盖率报告
pytest --cov=xiao_long_xia --cov-report=html
```

#### 代码质量检查
```bash
# 代码格式化
black src/ tests/

# 导入排序
isort src/ tests/

# 代码检查
flake8 src/ tests/

# 类型检查
mypy src/
```

#### 提交代码
```bash
git add .
git commit -m "feat: 添加新功能"
```

#### 推送分支
```bash
git push origin feature/你的功能名称
```

#### 创建Pull Request
1. 在GitHub上创建Pull Request
2. 填写PR描述，说明更改内容
3. 等待代码审查

### 4. 代码规范

#### Python风格
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- 使用 [Black](https://black.readthedocs.io/) 代码格式化
- 使用 [isort](https://pycqa.github.io/isort/) 导入排序

#### 文档字符串
使用Google风格文档字符串：

```python
def example_function(param1: str, param2: int) -> bool:
    """函数简要描述。
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
        
    Returns:
        返回值描述
        
    Raises:
        ValueError: 当参数无效时
        
    Example:
        >>> example_function("test", 123)
        True
    """
```

#### 类型提示
为所有函数和方法添加类型提示：

```python
from typing import List, Optional, Dict

def process_data(data: List[str], config: Optional[Dict] = None) -> bool:
    ...
```

#### 测试规范
- 每个函数至少有一个测试
- 测试文件名：`test_模块名.py`
- 测试类名：`Test类名`
- 测试方法名：`test_功能描述`

### 5. 项目结构

```
xiao-long-xia-tools/
├── src/xiao_long_xia/     # 源代码
│   ├── __init__.py       # 包导出
│   ├── file_utils.py     # 文件工具
│   ├── data_utils.py     # 数据工具
│   ├── dev_utils.py      # 开发工具
│   └── ai_utils.py       # AI工具
├── tests/                # 测试代码
│   ├── __init__.py
│   ├── test_file_utils.py
│   ├── test_data_utils.py
│   ├── test_dev_utils.py
│   └── test_ai_utils.py
├── docs/                 # 文档
│   ├── API.md
│   └── TUTORIAL.md
├── examples/             # 示例代码
├── .github/workflows/    # GitHub Actions
├── pyproject.toml        # 项目配置
├── README.md             # 项目文档
└── CONTRIBUTING.md       # 贡献指南
```

### 6. 添加新功能

#### 新工具模块
1. 在 `src/xiao_long_xia/` 创建新模块
2. 实现工具类和方法
3. 在 `__init__.py` 中导出
4. 编写测试
5. 更新文档

#### 新工具函数
1. 在现有模块中添加函数
2. 添加到工具类中
3. 在 `__init__.py` 中导出为便捷函数
4. 编写测试
5. 更新文档

### 7. 发布流程

#### 版本管理
使用语义化版本：
- **主版本号**：不兼容的API更改
- **次版本号**：向后兼容的功能添加
- **修订号**：向后兼容的问题修复

#### 发布步骤
1. 更新 `pyproject.toml` 中的版本号
2. 更新 `CHANGELOG.md`
3. 创建GitHub Release
4. 自动发布到PyPI（通过GitHub Actions）

### 8. 文档更新

#### API文档
- 更新 `docs/API.md`
- 确保所有公共API都有文档

#### 教程
- 更新 `docs/TUTORIAL.md`
- 添加新功能的使用示例

#### README
- 更新功能列表
- 更新安装说明
- 更新使用示例

### 9. 代码审查

#### 作为审查者
- 检查代码质量
- 确保测试覆盖
- 验证功能正确性
- 提供建设性反馈

#### 作为被审查者
- 及时响应评论
- 按要求修改代码
- 保持专业态度

### 10. 获取帮助

- 查看现有文档和示例
- 在issue中提问
- 联系维护者

## 感谢贡献！

你的贡献将使这个项目变得更好。感谢你的时间和努力！