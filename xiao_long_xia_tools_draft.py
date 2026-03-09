"""
Xiao Long Xia Tools - Python Development Utilities
AI-assisted tools for developers
"""

import os
import re
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import mimetypes


class FileUtils:
    """文件处理工具类"""
    
    @staticmethod
    def batch_rename_files(directory: str, pattern: str, new_pattern: str) -> List[str]:
        """
        批量重命名文件
        
        Args:
            directory: 目录路径
            pattern: 匹配模式（支持正则表达式）
            new_pattern: 新文件名模式
            
        Returns:
            重命名后的文件列表
        """
        renamed_files = []
        try:
            for filename in os.listdir(directory):
                if re.match(pattern, filename):
                    new_name = re.sub(pattern, new_pattern, filename)
                    old_path = os.path.join(directory, filename)
                    new_path = os.path.join(directory, new_name)
                    os.rename(old_path, new_path)
                    renamed_files.append(new_name)
            return renamed_files
        except Exception as e:
            raise Exception(f"批量重命名失败: {str(e)}")
    
    @staticmethod
    def convert_file_encoding(file_path: str, from_encoding: str, to_encoding: str) -> bool:
        """
        转换文件编码
        
        Args:
            file_path: 文件路径
            from_encoding: 原始编码
            to_encoding: 目标编码
            
        Returns:
            是否成功
        """
        try:
            with open(file_path, 'r', encoding=from_encoding) as f:
                content = f.read()
            
            with open(file_path, 'w', encoding=to_encoding) as f:
                f.write(content)
            
            return True
        except Exception as e:
            raise Exception(f"文件编码转换失败: {str(e)}")
    
    @staticmethod
    def find_duplicate_files(directory: str) -> Dict[str, List[str]]:
        """
        查找重复文件（基于内容哈希）
        
        Args:
            directory: 目录路径
            
        Returns:
            哈希值到文件列表的映射
        """
        hash_map = {}
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    if file_hash not in hash_map:
                        hash_map[file_hash] = []
                    hash_map[file_hash].append(file_path)
                except:
                    continue
        
        # 只返回有重复的文件
        return {h: files for h, files in hash_map.items() if len(files) > 1}


class DataUtils:
    """数据清洗工具类"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        验证邮箱格式
        
        Args:
            email: 邮箱地址
            
        Returns:
            是否有效
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def clean_phone_number(phone: str) -> str:
        """
        清洗手机号码
        
        Args:
            phone: 手机号码
            
        Returns:
            清洗后的手机号码
        """
        # 移除所有非数字字符
        cleaned = re.sub(r'\D', '', phone)
        
        # 处理中国手机号
        if cleaned.startswith('86'):
            cleaned = cleaned[2:]
        elif cleaned.startswith('+86'):
            cleaned = cleaned[3:]
        
        # 验证长度
        if len(cleaned) == 11 and cleaned.startswith('1'):
            return cleaned
        else:
            raise ValueError(f"无效的手机号码: {phone}")
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        文本标准化
        
        Args:
            text: 原始文本
            
        Returns:
            标准化后的文本
        """
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 标准化标点符号
        text = re.sub(r'[，,]+', ', ', text)
        text = re.sub(r'[。.]+', '. ', text)
        text = re.sub(r'[！!]+', '! ', text)
        text = re.sub(r'[？?]+', '? ', text)
        
        # 移除首尾空白
        return text.strip()


class DevUtils:
    """开发效率工具类"""
    
    @staticmethod
    def generate_project_template(template_name: str, output_dir: str, **kwargs) -> bool:
        """
        生成项目模板
        
        Args:
            template_name: 模板名称
            output_dir: 输出目录
            **kwargs: 模板参数
            
        Returns:
            是否成功
        """
        templates = {
            'python': {
                'files': {
                    'README.md': '# {project_name}\n\n{description}',
                    'setup.py': 'from setuptools import setup, find_packages\n\nsetup(\n    name="{project_name}",\n    version="0.1.0",\n    packages=find_packages(),\n)',
                    'requirements.txt': '',
                    '.gitignore': '__pycache__/\n*.pyc\n.env\n',
                }
            },
            'flask': {
                'files': {
                    'app.py': 'from flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef hello():\n    return "Hello World!"',
                    'requirements.txt': 'Flask\n',
                }
            }
        }
        
        if template_name not in templates:
            raise ValueError(f"不支持的模板: {template_name}")
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            template = templates[template_name]
            
            for filename, content_template in template['files'].items():
                file_path = os.path.join(output_dir, filename)
                content = content_template.format(**kwargs)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return True
        except Exception as e:
            raise Exception(f"生成模板失败: {str(e)}")
    
    @staticmethod
    def extract_code_snippets(file_path: str, language: str = "python") -> List[Dict[str, Any]]:
        """
        提取代码片段
        
        Args:
            file_path: 文件路径
            language: 编程语言
            
        Returns:
            代码片段列表
        """
        snippets = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单的代码块提取（可根据语言扩展）
            if language == "python":
                # 提取函数定义
                function_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*:\s*(?:\"[^\"]*\"\s*)?\n?(.*?)(?=\n\s*def|\n\s*class|\Z)'
                functions = re.findall(function_pattern, content, re.DOTALL)
                
                for func_name, func_body in functions:
                    snippets.append({
                        'type': 'function',
                        'name': func_name,
                        'code': f'def {func_name}(...):\n{func_body.strip()}',
                        'language': language
                    })
                
                # 提取类定义
                class_pattern = r'class\s+(\w+)\s*(?:\([^)]*\))?\s*:\s*(?:\"[^\"]*\"\s*)?\n?(.*?)(?=\n\s*class|\n\s*def|\Z)'
                classes = re.findall(class_pattern, content, re.DOTALL)
                
                for class_name, class_body in classes:
                    snippets.append({
                        'type': 'class',
                        'name': class_name,
                        'code': f'class {class_name}:\n{class_body.strip()}',
                        'language': language
                    })
            
            return snippets
        except Exception as e:
            raise Exception(f"提取代码片段失败: {str(e)}")


class AIUtils:
    """AI辅助工具类"""
    
    @staticmethod
    def code_explanation(code: str, language: str = "python") -> Dict[str, Any]:
        """
        代码解释
        
        Args:
            code: 代码字符串
            language: 编程语言
            
        Returns:
            解释结果
        """
        # 这里可以集成DeepSeek API
        # 目前返回模拟结果
        return {
            'code': code,
            'language': language,
            'explanation': '这段代码实现了...（AI解释）',
            'complexity': '中等',
            'suggestions': ['可以考虑添加错误处理', '可以优化性能']
        }
    
    @staticmethod
    def bug_diagnosis(error_message: str, code_context: str) -> Dict[str, Any]:
        """
        Bug诊断
        
        Args:
            error_message: 错误信息
            code_context: 代码上下文
            
        Returns:
            诊断结果
        """
        return {
            'error': error_message,
            'context': code_context,
            'diagnosis': '可能的原因：...',
            'solution': '建议的解决方案：...',
            'prevention': '预防措施：...'
        }


# 便捷函数
def batch_rename(directory: str, pattern: str, new_pattern: str) -> List[str]:
    """批量重命名文件（便捷函数）"""
    return FileUtils.batch_rename_files(directory, pattern, new_pattern)

def clean_phone(phone: str) -> str:
    """清洗手机号码（便捷函数）"""
    return DataUtils.clean_phone_number(phone)

def generate_template(template: str, output: str, **kwargs) -> bool:
    """生成项目模板（便捷函数）"""
    return DevUtils.generate_project_template(template, output, **kwargs)

def explain_code(code: str, language: str = "python") -> Dict[str, Any]:
    """代码解释（便捷函数）"""
    return AIUtils.code_explanation(code, language)


if __name__ == "__main__":
    # 示例用法
    print("Xiao Long Xia Tools - 开发工具集合")
    print("=" * 50)
    
    # 测试数据清洗
    test_email = "test@example.com"
    print(f"邮箱验证 '{test_email}': {DataUtils.validate_email(test_email)}")
    
    # 测试手机号清洗
    try:
        test_phone = "+86 138-0013-8000"
        cleaned = DataUtils.clean_phone_number(test_phone)
        print(f"手机号清洗 '{test_phone}' -> '{cleaned}'")
    except ValueError as e:
        print(f"手机号清洗错误: {e}")
    
    # 测试文本标准化
    test_text = "你好，世界！！  这是一段测试文本。。。"
    normalized = DataUtils.normalize_text(test_text)
    print(f"文本标准化: '{normalized}'")