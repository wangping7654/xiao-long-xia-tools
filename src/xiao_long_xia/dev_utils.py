"""
开发效率工具模块
提供项目模板生成、代码片段提取等功能
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import shutil


class DevUtils:
    """开发效率工具类"""
    
    @staticmethod
    def generate_project_template(
        template_name: str, 
        output_dir: str, 
        **kwargs
    ) -> bool:
        """
        生成项目模板
        
        Args:
            template_name: 模板名称 ('python', 'flask', 'fastapi', 'cli')
            output_dir: 输出目录
            **kwargs: 模板参数
            
        Returns:
            是否成功
            
        Example:
            >>> DevUtils.generate_project_template(
            ...     'python', 
            ...     './my_project',
            ...     project_name='MyApp',
            ...     description='A new Python project',
            ...     author='Your Name'
            ... )
            True
        """
        templates = {
            'python': {
                'files': {
                    'README.md': """# {project_name}

{description}

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
pip install -e .
```

## Usage

```python
from {package_name} import main

main()
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run code quality checks
black src/
isort src/
flake8 src/
```

## License

MIT
""",
                    'pyproject.toml': """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{package_name}"
version = "0.1.0"
description = "{description}"
authors = [
    {{name = "{author}", email = ""}}
]
license = {{text = "MIT"}}
requires-python = ">=3.8"

[project.urls]
Homepage = ""

[tool.setuptools]
packages = ["{package_name}"]
""",
                    'src/{package_name}/__init__.py': """\"\"\"
{project_name}

{description}
\"\"\"

__version__ = "0.1.0"
__author__ = "{author}"

def main():
    \"\"\"Main entry point\"\"\"
    print("Hello from {project_name}!")
""",
                    'tests/test_basic.py': """\"\"\"Basic tests\"\"\"

from {package_name} import __version__, main

def test_version():
    \"\"\"Test version\"\"\"
    assert __version__ == "0.1.0"

def test_main(capsys):
    \"\"\"Test main function\"\"\"
    main()
    captured = capsys.readouterr()
    assert "Hello from {project_name}!" in captured.out
""",
                }
            },
            'flask': {
                'files': {
                    'app.py': """from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
""",
                    'requirements.txt': """Flask>=2.0.0
""",
                }
            },
            'cli': {
                'files': {
                    'src/{package_name}/cli.py': """\"\"\"Command-line interface\"\"\"

import click

@click.group()
def cli():
    \"\"\"{project_name} CLI\"\"\"
    pass

@cli.command()
def hello():
    \"\"\"Say hello\"\"\"
    click.echo("Hello from {project_name}!")

if __name__ == '__main__':
    cli()
""",
                }
            }
        }
        
        if template_name not in templates:
            raise ValueError(f"不支持的模板: {template_name}")
        
        try:
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 获取模板
            template = templates[template_name]
            
            # 默认参数
            default_params = {
                'project_name': 'MyProject',
                'package_name': 'myproject',
                'description': 'A new project',
                'author': 'Developer',
            }
            
            # 合并参数
            params = {**default_params, **kwargs}
            
            # 生成文件
            for filepath, content_template in template['files'].items():
                # 替换路径中的变量
                filepath = filepath.format(**params)
                full_path = os.path.join(output_dir, filepath)
                
                # 确保目录存在
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # 替换内容中的变量
                content = content_template.format(**params)
                
                # 写入文件
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return True
        except Exception as e:
            raise Exception(f"生成模板失败: {str(e)}")
    
    @staticmethod
    def extract_code_snippets(
        file_path: str, 
        language: str = "python"
    ) -> List[Dict[str, Any]]:
        """
        提取代码片段
        
        Args:
            file_path: 文件路径
            language: 编程语言
            
        Returns:
            代码片段列表
            
        Example:
            >>> snippets = DevUtils.extract_code_snippets('example.py')
            >>> for snippet in snippets:
            ...     print(f"{snippet['type']}: {snippet['name']}")
        """
        snippets = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if language == "python":
                # 提取函数定义
                function_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*(?:->\s*[^:]+)?\s*:\s*(?:\"[^\"]*\"\s*)?\n?(.*?)(?=\n\s*def|\n\s*class|\n\s*@|\Z)'
                functions = re.findall(function_pattern, content, re.DOTALL)
                
                for func_name, func_body in functions:
                    # 清理函数体
                    func_body = func_body.rstrip()
                    
                    snippets.append({
                        'type': 'function',
                        'name': func_name,
                        'code': f'def {func_name}(...):\n{func_body}',
                        'language': language,
                        'line_count': func_body.count('\n') + 1,
                    })
                
                # 提取类定义
                class_pattern = r'class\s+(\w+)\s*(?:\([^)]*\))?\s*:\s*(?:\"[^\"]*\"\s*)?\n?(.*?)(?=\n\s*class|\n\s*def|\n\s*@|\Z)'
                classes = re.findall(class_pattern, content, re.DOTALL)
                
                for class_name, class_body in classes:
                    # 清理类体
                    class_body = class_body.rstrip()
                    
                    snippets.append({
                        'type': 'class',
                        'name': class_name,
                        'code': f'class {class_name}:\n{class_body}',
                        'language': language,
                        'line_count': class_body.count('\n') + 1,
                    })
                
                # 提取装饰器定义
                decorator_pattern = r'@(\w+(?:\.\w+)*)\s*\n?(?:def|class)'
                decorators = re.findall(decorator_pattern, content)
                
                for decorator in decorators:
                    snippets.append({
                        'type': 'decorator',
                        'name': decorator,
                        'code': f'@{decorator}',
                        'language': language,
                    })
            
            return snippets
        except Exception as e:
            raise Exception(f"提取代码片段失败: {str(e)}")
    
    @staticmethod
    def create_package_structure(
        package_name: str,
        output_dir: str,
        include_tests: bool = True,
        include_docs: bool = True,
        include_examples: bool = True
    ) -> bool:
        """
        创建标准的Python包结构
        
        Args:
            package_name: 包名称
            output_dir: 输出目录
            include_tests: 是否包含测试
            include_docs: 是否包含文档
            include_examples: 是否包含示例
            
        Returns:
            是否成功
        """
        try:
            base_dir = os.path.join(output_dir, package_name)
            
            # 创建目录结构
            dirs = [
                os.path.join(base_dir, 'src', package_name),
                os.path.join(base_dir, 'tests') if include_tests else None,
                os.path.join(base_dir, 'docs') if include_docs else None,
                os.path.join(base_dir, 'examples') if include_examples else None,
            ]
            
            for dir_path in dirs:
                if dir_path:
                    os.makedirs(dir_path, exist_ok=True)
            
            # 创建基本文件
            files = {
                'README.md': f"""# {package_name}

A Python package.

## Installation

```bash
pip install {package_name}
```

## Usage

```python
import {package_name}

# Your code here
```

## Development

See CONTRIBUTING.md for development instructions.
""",
                'pyproject.toml': f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{package_name}"
version = "0.1.0"
description = "A Python package"
authors = [
    {{name = "Developer", email = ""}}
]
license = {{text = "MIT"}}
requires-python = ">=3.8"

[project.urls]
Homepage = ""

[tool.setuptools]
packages = ["{package_name}"]
package-dir = {{"" = "src"}}
""",
                'LICENSE': """MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
                f'src/{package_name}/__init__.py': f"""\"\"\"
{package_name}

A Python package.
\"\"\"

__version__ = "0.1.0"
__author__ = "Developer"

def hello():
    \"\"\"Say hello\"\"\"
    return "Hello from {package_name}!"
""",
            }
            
            if include_tests:
                files['tests/test_basic.py'] = f"""\"\"\"Basic tests\"\"\"

import pytest
from {package_name} import __version__, hello

def test_version():
    \"\"\"Test version\"\"\"
    assert __version__ == "0.1.0"

def test_hello():
    \"\"\"Test hello function\"\"\"
    result = hello()
    assert "Hello from {package_name}!" in result
"""
            
            # 写入文件
            for filepath, content in files.items():
                full_path = os.path.join(base_dir, filepath)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return True
        except Exception as e:
            raise Exception(f"创建包结构失败: {str(e)}")


# 便捷函数
def generate_project_template(template_name: str, output_dir: str, **kwargs) -> bool:
    """生成项目模板（便捷函数）"""
    return DevUtils.generate_project_template(template_name, output_dir, **kwargs)

def extract_code_snippets(file_path: str, language: str = "python") -> List[Dict[str, Any]]:
    """提取代码片段（便捷函数）"""
    return DevUtils.extract_code_snippets(file_path, language)

def create_package_structure(
    package_name: str,
    output_dir: str,
    include_tests: bool = True,
    include_docs: bool = True,
    include_examples: bool = True
) -> bool:
    """创建包结构（便捷函数）"""
    return DevUtils.create_package_structure(
        package_name, output_dir, include_tests, include_docs, include_examples
    )