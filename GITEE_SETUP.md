# Gitee 部署说明 - Xiao Long Xia Tools

## 项目概述
**名称：** xiao-long-xia-tools
**描述：** Python开发工具集合，由小龙虾（AI辅助）创建
**目标：** 提供实用的Python工具，通过开源项目获得收入

## Gitee 特定配置

### 1. 仓库设置
- **仓库地址：** https://gitee.com/little-dragon-shrimp/xiao-long-xia-tools
- **开源协议：** MIT License
- **主要分支：** master

### 2. Gitee 功能利用

#### A. Gitee Pages（文档托管）
```yaml
# 在仓库设置中启用Gitee Pages
# 分支：master
# 目录：/ (根目录)
# 自动部署：启用
```

#### B. Gitee Go（CI/CD）
```yaml
# .gitee-ci.yml 配置文件
# 自动测试、构建、部署
```

#### C. Gitee 赞助
- 在仓库页面启用"赞助"功能
- 设置赞助等级和说明

### 3. 安装和使用

#### 从Gitee安装：
```bash
# 使用pip从Gitee安装
pip install git+https://gitee.com/little-dragon-shrimp/xiao-long-xia-tools.git

# 或克隆后安装
git clone https://gitee.com/little-dragon-shrimp/xiao-long-xia-tools.git
cd xiao-long-xia-tools
pip install -e .
```

#### 基本使用：
```python
from xiao_long_xia import FileUtils, DataUtils, DevUtils, AIUtils

# 文件处理
FileUtils.batch_rename_files('./docs', r'(\d+)\.txt', r'doc_\1.md')

# 数据清洗
DataUtils.validate_email('test@example.com')

# 开发工具
DevUtils.generate_project_template('python', './my_project')

# AI辅助
AIUtils.code_explanation('def add(a, b): return a + b')
```

### 4. 项目结构
```
xiao-long-xia-tools/
├── src/xiao_long_xia/     # 源代码
│   ├── __init__.py       # 包导出
│   ├── file_utils.py     # 文件处理工具
│   ├── data_utils.py     # 数据清洗工具
│   ├── dev_utils.py      # 开发效率工具
│   └── ai_utils.py       # AI辅助工具
├── .github/              # GitHub配置（兼容）
├── pyproject.toml        # 项目配置
├── README.md             # 项目文档
└── 其他配置文件...
```

### 5. 开发指南

#### 环境设置：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"
```

#### 运行测试：
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_file_utils.py

# 生成测试覆盖率报告
pytest --cov=xiao_long_xia --cov-report=html
```

### 6. 贡献指南

#### 提交代码：
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -m '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建 Pull Request

#### 代码规范：
- 使用 Black 代码格式化
- 使用 isort 导入排序
- 遵循 PEP 8 规范
- 添加类型提示

### 7. 收入模式

#### Gitee 赞助：
1. 在仓库页面启用赞助功能
2. 设置赞助等级（如：5元、15元、50元、100元）
3. 提供赞助者权益

#### 其他收入：
- 技术咨询服务
- 定制开发服务
- 培训和技术支持

### 8. 联系方式

- **问题反馈：** 通过Gitee Issues
- **功能建议：** 通过Gitee Issues或Pull Request
- **合作咨询：** 通过Gitee私信或邮箱

### 9. 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**小龙虾生存创收项目 - Gitee部署版**
**目标：** 通过开源项目实现自动化收入，最小化人类介入