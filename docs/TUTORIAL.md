# 使用教程

## 快速开始

### 1. 安装

```bash
# 从GitHub安装最新版本
pip install git+https://github.com/wangping7654/xiao-long-xia-tools.git

# 或克隆后安装
git clone https://github.com/wangping7654/xiao-long-xia-tools.git
cd xiao-long-xia-tools
pip install -e .
```

### 2. 基本使用

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

## 详细教程

### 文件处理示例

#### 批量重命名文件

```python
from xiao_long_xia import batch_rename_files

# 重命名所有.txt文件为.md
result = batch_rename_files(
    './documents',
    r'\.txt$',
    '.md'
)
print(f"重命名了 {len(result)} 个文件")
```

#### 查找重复文件

```python
from xiao_long_xia import find_duplicate_files

# 查找照片目录中的重复文件
duplicates = find_duplicate_files(
    './photos',
    min_size=1024 * 1024  # 只查找大于1MB的文件
)

for hash_val, files in duplicates.items():
    print(f"重复文件组 ({len(files)} 个文件):")
    for file in files:
        print(f"  - {file}")
```

### 数据清洗示例

#### 验证和清洗数据

```python
from xiao_long_xia import validate_email, clean_phone_number, normalize_text

# 验证邮箱
emails = [
    'alice@example.com',
    'invalid-email',
    'bob@test.org'
]

for email in emails:
    if validate_email(email):
        print(f"✅ 有效邮箱: {email}")
    else:
        print(f"❌ 无效邮箱: {email}")

# 清洗手机号
phone_numbers = [
    '135-1062-8257',
    '+86 138-0013-8000',
    'invalid'
]

for phone in phone_numbers:
    cleaned = clean_phone_number(phone, country_code='CN')
    if cleaned:
        print(f"✅ 清洗后: {cleaned}")
    else:
        print(f"❌ 无效手机号: {phone}")

# 标准化文本
texts = [
    '  Hello  World  ',
    '<p>Test HTML</p>',
    'MIXED CASE text'
]

for text in texts:
    normalized = normalize_text(text, lowercase=True)
    print(f"标准化: '{text}' -> '{normalized}'")
```

### 开发工具示例

#### 生成项目模板

```python
from xiao_long_xia import generate_project_template

# 生成Python项目模板
success = generate_project_template(
    'python',
    './my_python_project',
    project_name='MyPythonProject',
    author='Your Name',
    version='1.0.0',
    description='A Python project'
)

if success:
    print("✅ 项目模板生成成功")
else:
    print("❌ 项目模板生成失败")
```

#### 提取代码片段

```python
from xiao_long_xia import extract_code_snippets

# 从Python文件中提取代码片段
snippets = extract_code_snippets(
    './src',
    language='python'
)

for snippet in snippets[:3]:  # 显示前3个片段
    print(f"文件: {snippet['file']}")
    print(f"代码:\n{snippet['code'][:100]}...")
    print("-" * 50)
```

### AI辅助示例

#### 代码解释

```python
from xiao_long_xia import code_explanation

code = '''
def fibonacci(n):
    """计算斐波那契数列"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
'''

result = code_explanation(
    code,
    language='python',
    detail_level='detailed'
)

print("📝 代码解释:")
print(result['explanation'])
print("\n🔍 复杂度分析:")
print(result.get('complexity', 'N/A'))
```

#### Bug诊断

```python
from xiao_long_xia import bug_diagnosis

buggy_code = '''
def divide_numbers(a, b):
    return a / b

result = divide_numbers(10, 0)
print(result)
'''

result = bug_diagnosis(
    buggy_code,
    error_message='ZeroDivisionError: division by zero',
    language='python'
)

print("🐛 Bug诊断结果:")
print(f"问题: {result['problem']}")
print(f"解决方案: {result['solution']}")
print(f"修复后的代码:\n{result['fixed_code']}")
```

## 实际应用场景

### 场景1：批量处理下载的文件

```python
from xiao_long_xia import organize_files_by_extension

# 整理下载目录
result = organize_files_by_extension(
    '~/Downloads',
    extensions_map={
        'pdf': 'documents',
        'doc': 'documents',
        'docx': 'documents',
        'jpg': 'images',
        'png': 'images',
        'mp4': 'videos',
        'mp3': 'music',
        'zip': 'archives',
        'rar': 'archives'
    }
)

for folder, files in result.items():
    print(f"📁 {folder}: {len(files)} 个文件")
```

### 场景2：数据清洗管道

```python
from xiao_long_xia import (
    validate_email,
    clean_phone_number,
    remove_duplicates,
    extract_emails,
    extract_urls
)

def clean_contact_data(raw_data):
    """清洗联系人数据"""
    cleaned_data = []
    
    for contact in raw_data:
        # 清洗邮箱
        if 'email' in contact:
            if not validate_email(contact['email']):
                continue  # 跳过无效邮箱
        
        # 清洗手机号
        if 'phone' in contact:
            cleaned_phone = clean_phone_number(contact['phone'])
            if not cleaned_phone:
                continue  # 跳过无效手机号
            contact['phone'] = cleaned_phone
        
        # 提取额外信息
        if 'notes' in contact:
            contact['extracted_emails'] = extract_emails(contact['notes'])
            contact['extracted_urls'] = extract_urls(contact['notes'])
        
        cleaned_data.append(contact)
    
    # 移除重复联系人（基于邮箱）
    return remove_duplicates(cleaned_data, key=lambda x: x.get('email', ''))
```

### 场景3：自动化代码审查

```python
from xiao_long_xia import (
    code_explanation,
    bug_diagnosis,
    code_optimization_suggestions,
    generate_documentation
)

def code_review_pipeline(code_file):
    """自动化代码审查管道"""
    with open(code_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    review_report = {
        'file': code_file,
        'explanations': [],
        'optimizations': [],
        'documentation': None
    }
    
    # 代码解释
    explanation = code_explanation(code)
    review_report['explanations'].append(explanation)
    
    # 优化建议
    optimizations = code_optimization_suggestions(code, focus='performance')
    review_report['optimizations'].append(optimizations)
    
    # 生成文档
    docs = generate_documentation(code, style='google')
    review_report['documentation'] = docs
    
    return review_report
```

## 最佳实践

### 1. 错误处理

```python
from xiao_long_xia import FileUtils
import traceback

try:
    result = FileUtils.batch_rename_files(
        '/nonexistent/directory',
        r'\.txt$',
        '.md'
    )
except Exception as e:
    print(f"❌ 错误: {e}")
    # 记录错误但不中断程序
    traceback.print_exc()
```

### 2. 性能优化

```python
from xiao_long_xia import find_duplicate_files
import time

# 测量性能
start_time = time.time()

duplicates = find_duplicate_files(
    './large_directory',
    min_size=1024 * 1024  # 只处理大文件
)

elapsed_time = time.time() - start_time
print(f"⏱️ 处理时间: {elapsed_time:.2f}秒")
print(f"📊 找到 {len(duplicates)} 组重复文件")
```

### 3. 批量处理

```python
from xiao_long_xia import DataUtils
from concurrent.futures import ThreadPoolExecutor

def batch_validate_emails(emails):
    """批量验证邮箱"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(DataUtils.validate_email, emails))
    
    valid_count = sum(results)
    invalid_count = len(emails) - valid_count
    
    return {
        'total': len(emails),
        'valid': valid_count,
        'invalid': invalid_count,
        'valid_emails': [email for email, valid in zip(emails, results) if valid]
    }
```

## 故障排除

### 常见问题

#### Q1: 导入模块时出现 `ModuleNotFoundError`
**A:** 确保已正确安装包：
```bash
pip install -e .
```

#### Q2: 文件操作权限错误
**A:** 检查文件权限：
```python
import os
print(os.access('/path/to/file', os.R_OK))  # 检查读权限
print(os.access('/path/to/file', os.W_OK))  # 检查写权限
```

#### Q3: 正则表达式不匹配
**A:** 使用原始字符串并测试正则表达式：
```python
import re
pattern = r'\.txt$'
test_string = 'document.txt'
print(bool(re.match(pattern, test_string)))  # 应该返回True
```

#### Q4: AI工具返回空结果
**A:** 检查网络连接和API配置：
```python
# 确保有网络连接
import requests
try:
    response = requests.get('https://api.deepseek.com', timeout=5)
    print("✅ 网络连接正常")
except:
    print("❌ 网络连接问题")
```

## 下一步

- 查看 [API文档](API.md) 获取完整功能列表
- 查看 [贡献指南](../CONTRIBUTING.md) 参与开发
- 查看 [示例项目](../examples/) 获取更多使用示例

## 获取帮助

- 提交 [Issue](https://github.com/wangping7654/xiao-long-xia-tools/issues)
- 查看 [常见问题](../FAQ.md)
- 加入讨论