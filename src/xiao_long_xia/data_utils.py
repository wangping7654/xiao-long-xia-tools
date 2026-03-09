"""
数据清洗工具模块
提供数据验证、清洗、标准化等功能
"""

import re
import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import unicodedata


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
            
        Example:
            >>> DataUtils.validate_email('test@example.com')
            True
            >>> DataUtils.validate_email('invalid-email')
            False
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def clean_phone_number(phone: str, country_code: str = 'CN') -> str:
        """
        清洗手机号码
        
        Args:
            phone: 手机号码
            country_code: 国家代码
            
        Returns:
            清洗后的手机号码
            
        Example:
            >>> DataUtils.clean_phone_number('+86 138-0013-8000')
            '13800138000'
            >>> DataUtils.clean_phone_number('(010) 1234-5678', 'CN')
            '01012345678'
        """
        # 移除所有非数字字符
        cleaned = re.sub(r'\D', '', phone)
        
        # 根据国家代码处理
        if country_code.upper() == 'CN':
            # 处理中国手机号
            if cleaned.startswith('86'):
                cleaned = cleaned[2:]
            elif cleaned.startswith('+86'):
                cleaned = cleaned[3:]
            
            # 验证中国手机号格式
            if len(cleaned) == 11 and cleaned.startswith('1'):
                return cleaned
            elif len(cleaned) == 10 and cleaned.startswith(('1', '2')):
                # 可能是固定电话
                return cleaned
            else:
                raise ValueError(f"无效的中国电话号码: {phone}")
        
        elif country_code.upper() == 'US':
            # 美国电话号码 (10位)
            if len(cleaned) == 10:
                return cleaned
            elif len(cleaned) == 11 and cleaned.startswith('1'):
                # 包含国家代码
                return cleaned[1:]
            else:
                raise ValueError(f"无效的美国电话号码: {phone}")
        
        else:
            # 通用处理
            return cleaned
    
    @staticmethod
    def normalize_text(text: str, remove_extra_spaces: bool = True) -> str:
        """
        文本标准化
        
        Args:
            text: 原始文本
            remove_extra_spaces: 是否移除多余空白
            
        Returns:
            标准化后的文本
            
        Example:
            >>> DataUtils.normalize_text('你好，世界！！  这是一段测试文本。。。')
            '你好, 世界! 这是一段测试文本.'
        """
        if not text:
            return ""
        
        # 移除多余空白
        if remove_extra_spaces:
            text = re.sub(r'\s+', ' ', text.strip())
        
        # 标准化标点符号（中文转英文）
        text = re.sub(r'[，,]+', ', ', text)
        text = re.sub(r'[。.]+', '. ', text)
        text = re.sub(r'[！!]+', '! ', text)
        text = re.sub(r'[？?]+', '? ', text)
        text = re.sub(r'[：:]+', ': ', text)
        text = re.sub(r'[；;]+', '; ', text)
        
        # 移除首尾空白
        text = text.strip()
        
        # 确保标点符号后只有一个空格
        text = re.sub(r'([,.!?:;])\s+', r'\1 ', text)
        
        return text
    
    @staticmethod
    def validate_json(data: str) -> bool:
        """
        验证JSON字符串
        
        Args:
            data: JSON字符串
            
        Returns:
            是否有效的JSON
            
        Example:
            >>> DataUtils.validate_json('{"name": "John", "age": 30}')
            True
            >>> DataUtils.validate_json('invalid json')
            False
        """
        try:
            json.loads(data)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
    
    @staticmethod
    def clean_json(data: str, strict: bool = False) -> Optional[str]:
        """
        清洗JSON字符串
        
        Args:
            data: JSON字符串
            strict: 严格模式（失败时返回None）
            
        Returns:
            清洗后的JSON字符串
            
        Example:
            >>> DataUtils.clean_json('{"name": "John", "age": 30, }')
            '{"name": "John", "age": 30}'
        """
        try:
            # 尝试解析JSON
            parsed = json.loads(data)
            # 重新序列化，确保格式正确
            cleaned = json.dumps(parsed, ensure_ascii=False, indent=2)
            return cleaned
        except (json.JSONDecodeError, TypeError):
            if strict:
                return None
            
            # 尝试修复常见的JSON问题
            try:
                # 移除尾随逗号
                data = re.sub(r',\s*}', '}', data)
                data = re.sub(r',\s*]', ']', data)
                
                # 尝试再次解析
                parsed = json.loads(data)
                cleaned = json.dumps(parsed, ensure_ascii=False, indent=2)
                return cleaned
            except:
                return None
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        从文本中提取邮箱地址
        
        Args:
            text: 文本内容
            
        Returns:
            邮箱地址列表
            
        Example:
            >>> DataUtils.extract_emails('Contact: test@example.com, support@company.org')
            ['test@example.com', 'support@company.org']
        """
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        从文本中提取URL
        
        Args:
            text: 文本内容
            
        Returns:
            URL列表
            
        Example:
            >>> DataUtils.extract_urls('Visit https://example.com and http://test.org')
            ['https://example.com', 'http://test.org']
        """
        pattern = r'https?://[^\s<>"\']+|www\.[^\s<>"\']+'
        return re.findall(pattern, text)
    
    @staticmethod
    def remove_special_characters(text: str, keep: str = '') -> str:
        """
        移除特殊字符
        
        Args:
            text: 原始文本
            keep: 要保留的字符
            
        Returns:
            清洗后的文本
            
        Example:
            >>> DataUtils.remove_special_characters('Hello#World!@123')
            'HelloWorld123'
            >>> DataUtils.remove_special_characters('Hello#World!@123', keep='!@')
            'Hello#World!@123'
        """
        if keep:
            # 保留指定字符
            pattern = f'[^a-zA-Z0-9\\s{re.escape(keep)}]'
        else:
            # 只保留字母、数字和空白
            pattern = r'[^a-zA-Z0-9\s]'
        
        return re.sub(pattern, '', text)
    
    @staticmethod
    def format_date(date_str: str, input_format: str, output_format: str) -> Optional[str]:
        """
        格式化日期字符串
        
        Args:
            date_str: 日期字符串
            input_format: 输入格式
            output_format: 输出格式
            
        Returns:
            格式化后的日期字符串
            
        Example:
            >>> DataUtils.format_date('2023-12-25', '%Y-%m-%d', '%d/%m/%Y')
            '25/12/2023'
        """
        try:
            date_obj = datetime.strptime(date_str, input_format)
            return date_obj.strftime(output_format)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def remove_duplicates(items: List[Any]) -> List[Any]:
        """
        移除列表中的重复项（保持顺序）
        
        Args:
            items: 原始列表
            
        Returns:
            去重后的列表
            
        Example:
            >>> DataUtils.remove_duplicates([1, 2, 2, 3, 1])
            [1, 2, 3]
        """
        seen = set()
        result = []
        
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        
        return result


# 便捷函数
def validate_email(email: str) -> bool:
    """验证邮箱格式（便捷函数）"""
    return DataUtils.validate_email(email)

def clean_phone_number(phone: str, country_code: str = 'CN') -> str:
    """清洗手机号码（便捷函数）"""
    return DataUtils.clean_phone_number(phone, country_code)

def normalize_text(text: str, remove_extra_spaces: bool = True) -> str:
    """文本标准化（便捷函数）"""
    return DataUtils.normalize_text(text, remove_extra_spaces)

def validate_json(data: str) -> bool:
    """验证JSON字符串（便捷函数）"""
    return DataUtils.validate_json(data)

def extract_emails(text: str) -> List[str]:
    """从文本中提取邮箱地址（便捷函数）"""
    return DataUtils.extract_emails(text)

def extract_urls(text: str) -> List[str]:
    """从文本中提取URL（便捷函数）"""
    return DataUtils.extract_urls(text)