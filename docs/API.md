# API 文档

## 概述

Xiao Long Xia Tools 是一个Python开发工具集合，提供文件处理、数据清洗、开发效率和AI辅助等功能。

## 安装

```bash
pip install git+https://github.com/wangping7654/xiao-long-xia-tools.git
```

## 模块

### 1. FileUtils - 文件工具

#### 类：`FileUtils`

##### 方法：

**`batch_rename_files(directory, pattern, replacement, dry_run=False)`**
批量重命名文件。

- **参数**:
  - `directory` (str): 目录路径
  - `pattern` (str): 正则表达式模式
  - `replacement` (str): 替换字符串
  - `dry_run` (bool): 试运行模式，默认False
- **返回**: List[str] - 重命名的文件列表
- **示例**:
  ```python
  from xiao_long_xia import FileUtils
  
  # 批量重命名
  result = FileUtils.batch_rename_files(
      './docs',
      r'(\d+)\.txt',
      r'doc_\1.md'
  )
  # 返回: ['doc_1.md', 'doc_2.md']
  ```

**`convert_file_encoding(filepath, from_encoding, to_encoding, backup=True)`**
转换文件编码。

- **参数**:
  - `filepath` (str): 文件路径
  - `from_encoding` (str): 原始编码
  - `to_encoding` (str): 目标编码
  - `backup` (bool): 是否创建备份，默认True
- **返回**: bool - 是否成功
- **示例**:
  ```python
  success = FileUtils.convert_file_encoding(
      'file.txt',
      'gbk',
      'utf-8'
  )
  ```

**`find_duplicate_files(directory, min_size=1024)`**
查找重复文件。

- **参数**:
  - `directory` (str): 目录路径
  - `min_size` (int): 最小文件大小（字节），默认1024
- **返回**: Dict[str, List[str]] - 哈希值到文件列表的映射
- **示例**:
  ```python
  duplicates = FileUtils.find_duplicate_files('./photos')
  ```

**`organize_files_by_extension(directory, extensions_map=None)`**
按扩展名整理文件。

- **参数**:
  - `directory` (str): 目录路径
  - `extensions_map` (Dict[str, str]): 扩展名到文件夹的映射
- **返回**: Dict[str, List[str]] - 整理结果
- **示例**:
  ```python
  result = FileUtils.organize_files_by_extension('./downloads')
  ```

#### 便捷函数：

**`batch_rename_files(directory, pattern, replacement, dry_run=False)`**
同FileUtils.batch_rename_files。

**`convert_file_encoding(filepath, from_encoding, to_encoding, backup=True)`**
同FileUtils.convert_file_encoding。

**`find_duplicate_files(directory, min_size=1024)`**
同FileUtils.find_duplicate_files。

**`organize_files_by_extension(directory, extensions_map=None)`**
同FileUtils.organize_files_by_extension。

### 2. DataUtils - 数据工具

#### 类：`DataUtils`

##### 方法：

**`validate_email(email)`**
验证邮箱格式。

- **参数**: `email` (str): 邮箱地址
- **返回**: bool - 是否有效
- **示例**:
  ```python
  is_valid = DataUtils.validate_email('test@example.com')
  ```

**`clean_phone_number(phone, country_code='CN')`**
清洗手机号码。

- **参数**:
  - `phone` (str): 手机号码
  - `country_code` (str): 国家代码，默认'CN'
- **返回**: str - 清洗后的手机号码
- **示例**:
  ```python
  cleaned = DataUtils.clean_phone_number('+86 138-0013-8000')
  # 返回: '13800138000'
  ```

**`normalize_text(text, lowercase=True, remove_punctuation=False)`**
标准化文本。

- **参数**:
  - `text` (str): 原始文本
  - `lowercase` (bool): 是否转换为小写，默认True
  - `remove_punctuation` (bool): 是否移除标点，默认False
- **返回**: str - 标准化后的文本
- **示例**:
  ```python
  normalized = DataUtils.normalize_text('  Hello, World!  ')
  # 返回: 'hello, world!'
  ```

**`validate_json(json_str)`**
验证JSON格式。

- **参数**: `json_str` (str): JSON字符串
- **返回**: bool - 是否有效
- **示例**:
  ```python
  is_valid = DataUtils.validate_json('{"name": "Alice"}')
  ```

**`extract_emails(text)`**
提取邮箱地址。

- **参数**: `text` (str): 文本
- **返回**: List[str] - 邮箱地址列表
- **示例**:
  ```python
  emails = DataUtils.extract_emails('Contact: alice@example.com')
  ```

**`extract_urls(text)`**
提取URL。

- **参数**: `text` (str): 文本
- **返回**: List[str] - URL列表
- **示例**:
  ```python
  urls = DataUtils.extract_urls('Visit https://example.com')
  ```

**`remove_duplicates(data)`**
移除重复项。

- **参数**: `data` (List[Any]): 数据列表
- **返回**: List[Any] - 去重后的列表
- **示例**:
  ```python
  unique = DataUtils.remove_duplicates([1, 2, 2, 3])
  # 返回: [1, 2, 3]
  ```

**`remove_special_characters(text)`**
移除特殊字符。

- **参数**: `text` (str): 文本
- **返回**: str - 清理后的文本
- **示例**:
  ```python
  cleaned = DataUtils.remove_special_characters('Hello@World#123')
  # 返回: 'HelloWorld123'
  ```

**`format_date(date_str, input_format, output_format)`**
格式化日期。

- **参数**:
  - `date_str` (str): 日期字符串
  - `input_format` (str): 输入格式
  - `output_format` (str): 输出格式
- **返回**: str - 格式化后的日期
- **示例**:
  ```python
  formatted = DataUtils.format_date(
      '2024-03-09',
      '%Y-%m-%d',
      '%Y年%m月%d日'
  )
  # 返回: '2024年03月09日'
  ```

**`clean_json(json_str)`**
清洗JSON数据。

- **参数**: `json_str` (str): JSON字符串
- **返回**: str - 清洗后的JSON
- **示例**:
  ```python
  cleaned = DataUtils.clean_json('{"name": "Alice", "age": null}')
  ```

#### 便捷函数：

**`validate_email(email)`**
同DataUtils.validate_email。

**`clean_phone_number(phone, country_code='CN')`**
同DataUtils.clean_phone_number。

**`normalize_text(text, lowercase=True, remove_punctuation=False)`**
同DataUtils.normalize_text。

**`validate_json(json_str)`**
同DataUtils.validate_json。

**`extract_emails(text)`**
同DataUtils.extract_emails。

**`extract_urls(text)`**
同DataUtils.extract_urls。

### 3. DevUtils - 开发工具

#### 类：`DevUtils`

##### 方法：

**`generate_project_template(project_type, output_dir, **kwargs)`**
生成项目模板。

- **参数**:
  - `project_type` (str): 项目类型（'python', 'web', 'cli'等）
  - `output_dir` (str): 输出目录
  - `**kwargs`: 额外参数
- **返回**: bool - 是否成功
- **示例**:
  ```python
  success = DevUtils.generate_project_template(
      'python',
      './my_project',
      project_name='MyProject'
  )
  ```

**`extract_code_snippets(source_path, language=None)`**
提取代码片段。

- **参数**:
  - `source_path` (str): 源代码路径
  - `language` (str): 编程语言
- **返回**: List[Dict] - 代码片段列表
- **示例**:
  ```python
  snippets = DevUtils.extract_code_snippets('./src', 'python')
  ```

**`create_package_structure(package_name, output_dir, **kwargs)`**
创建包结构。

- **参数**:
  - `package_name` (str): 包名
  - `output_dir` (str): 输出目录
  - `**kwargs`: 额外参数
- **返回**: bool - 是否成功
- **示例**:
  ```python
  success = DevUtils.create_package_structure(
      'mypackage',
      './packages'
  )
  ```

#### 便捷函数：

**`generate_project_template(project_type, output_dir, **kwargs)`**
同DevUtils.generate_project_template。

**`extract_code_snippets(source_path, language=None)`**
同DevUtils.extract_code_snippets。

**`create_package_structure(package_name, output_dir, **kwargs)`**
同DevUtils.create_package_structure。

### 4. AIUtils - AI工具

#### 类：`AIUtils`

##### 方法：

**`code_explanation(code, language='python', detail_level='medium')`**
代码解释。

- **参数**:
  - `code` (str): 代码
  - `language` (str): 编程语言，默认'python'
  - `detail_level` (str): 详细程度（'brief', 'medium', 'detailed'）
- **返回**: Dict - 解释结果
- **示例**:
  ```python
  result = AIUtils.code_explanation('def add(a, b): return a + b')
  ```

**`bug_diagnosis(code, error_message=None, language='python')`**
Bug诊断。

- **参数**:
  - `code` (str): 代码
  - `error_message` (str): 错误信息
  - `language` (str): 编程语言，默认'python'
- **返回**: Dict - 诊断结果
- **示例**:
  ```python
  result = AIUtils.bug_diagnosis(
      'print("Hello"',
      'SyntaxError: unexpected EOF while parsing'
  )
  ```

**`code_optimization_suggestions(code, language='python', focus='performance')`**
代码优化建议。

- **参数**:
  - `code` (str): 代码
  - `language` (str): 编程语言，默认'python'
  - `focus` (str): 优化重点（'performance', 'readability', 'memory'）
- **返回**: Dict - 优化建议
- **示例**:
  ```python
  suggestions = AIUtils.code_optimization_suggestions(
      '[x**2 for x in range(1000)]'
  )
  ```

**`generate_documentation(code, language='python', style='google')`**
生成文档。

- **参数**:
  - `code` (str): 代码
  - `language` (str): 编程语言，默认'python'
  - `style` (str): 文档风格（'google', 'numpy', 'sphinx'）
- **返回**: Dict - 文档内容
- **示例**:
  ```python
  docs = AIUtils.generate_documentation(
      'def calculate_sum(numbers):\n    return sum(numbers)'
  )
  ```

#### 便捷函数：

**`code_explanation(code, language='python', detail_level='medium')`**
同AIUtils.code_explanation。

**`bug_diagnosis(code, error_message=None, language='python')`**
同AIUtils.bug_diagnosis。

**`code_optimization_suggestions(code, language='python', focus='performance')`**
同AIUtils.code_optimization_suggestions。

**`generate_documentation(code, language='python', style='google')`**
同AIUtils.generate_documentation。

## 错误处理

所有方法都包含适当的错误处理，返回有意义的结果或异常。

## 贡献

欢迎贡献！请查看[贡献指南](CONTRIBUTING.md)。

## 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。