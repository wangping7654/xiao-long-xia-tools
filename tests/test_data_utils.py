"""
测试数据工具模块
"""

import os
import tempfile
import shutil
import json
from pathlib import Path
import pytest

from xiao_long_xia import DataUtils, validate_email, clean_phone_number, normalize_text, validate_json


class TestDataUtils:
    """测试DataUtils类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.test_dir = tempfile.mkdtemp(prefix="test_data_utils_")
        print(f"测试目录: {self.test_dir}")
    
    def teardown_method(self):
        """每个测试方法后的清理"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_validate_email_valid(self):
        """测试有效的邮箱地址验证"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "user123@sub.domain.com",
            "a@b.cd",  # 最短有效邮箱
        ]
        
        for email in valid_emails:
            result = DataUtils.validate_email(email)
            assert result is True, f"邮箱 {email} 应该有效"
    
    def test_validate_email_invalid(self):
        """测试无效的邮箱地址验证"""
        invalid_emails = [
            "",  # 空字符串
            "invalid",  # 无@符号
            "invalid@",  # 无域名
            "@domain.com",  # 无用户名
            "user@.com",  # 无域名部分
            "user@domain.",  # 无顶级域名
            "user@domain..com",  # 双点
            "user name@domain.com",  # 空格
            "user@domain_com",  # 下划线
            "user@-domain.com",  # 以连字符开头
            "user@domain-.com",  # 以连字符结尾
            "user@domain.c",  # 顶级域名太短
            "user@domain.123",  # 数字顶级域名
        ]
        
        for email in invalid_emails:
            result = DataUtils.validate_email(email)
            assert result is False, f"邮箱 {email} 应该无效"
    
    def test_clean_phone_number_china(self):
        """测试中国手机号清洗"""
        test_cases = [
            ("13510628257", "13510628257"),  # 你的手机号，已干净
            ("138-0013-8000", "13800138000"),  # 带分隔符
            ("(139)12345678", "13912345678"),  # 带括号
            (" 15098765432 ", "15098765432"),  # 带空格
            ("+8618812345678", "18812345678"),  # 带国际区号
            ("199-1234-5678", "19912345678"),  # 新号段带分隔符
        ]
        
        for input_phone, expected in test_cases:
            result = DataUtils.clean_phone_number(input_phone, country='CN')
            assert result == expected, f"手机号 {input_phone} 应该清洗为 {expected}"
    
    def test_clean_phone_number_invalid(self):
        """测试无效手机号清洗"""
        invalid_phones = [
            "",  # 空字符串
            "1234567890",  # 长度不够
            "123456789012",  # 长度太长
            "1351062825a",  # 包含字母
            "invalid",  # 完全无效
        ]
        
        for phone in invalid_phones:
            result = DataUtils.clean_phone_number(phone, country='CN')
            # 无效手机号应该返回None或空字符串
            assert result is None or result == "", f"无效手机号 {phone} 应该返回None或空字符串"
    
    def test_clean_phone_number_us(self):
        """测试美国手机号清洗"""
        test_cases = [
            ("+1-555-123-4567", "5551234567"),
            ("5551234567", "5551234567"),
            ("(555) 123-4567", "5551234567"),
            ("555-123-4567", "5551234567"),
            (" 555 123 4567 ", "5551234567"),
        ]
        
        for input_phone, expected in test_cases:
            result = DataUtils.clean_phone_number(input_phone, country='US')
            assert result == expected, f"美国手机号 {input_phone} 应该清洗为 {expected}"
    
    def test_clean_text_data_basic(self):
        """测试基本文本数据清洗"""
        dirty_text = "  Hello,  World!  \n\t  This is a test.  "
        cleaned = DataUtils.clean_text_data(dirty_text)
        
        expected = "Hello, World! This is a test."
        assert cleaned == expected
    
    def test_clean_text_data_remove_html(self):
        """测试移除HTML标签"""
        html_text = "<p>Hello <b>World</b>!</p>"
        cleaned = DataUtils.clean_text_data(html_text, remove_html=True)
        
        assert "<" not in cleaned
        assert ">" not in cleaned
        assert "Hello World!" in cleaned
    
    def test_clean_text_data_lowercase(self):
        """测试转换为小写"""
        text = "Hello WORLD"
        cleaned = DataUtils.clean_text_data(text, lowercase=True)
        
        assert cleaned == "hello world"
    
    def test_clean_text_data_remove_punctuation(self):
        """测试移除标点符号"""
        text = "Hello, World! How are you?"
        cleaned = DataUtils.clean_text_data(text, remove_punctuation=True)
        
        # 标点符号应该被移除或替换为空格
        assert "," not in cleaned
        assert "!" not in cleaned
        assert "?" not in cleaned
    
    def test_remove_duplicates(self):
        """测试移除重复项"""
        data = [1, 2, 2, 3, 3, 3, 4, 5]
        unique = DataUtils.remove_duplicates(data)
        
        # 验证结果
        assert len(unique) == 5
        assert set(unique) == {1, 2, 3, 4, 5}
        # 保持顺序
        assert unique == [1, 2, 3, 4, 5]
    
    def test_remove_special_characters(self):
        """测试移除特殊字符"""
        text = "Hello@World#123$测试%"
        cleaned = DataUtils.remove_special_characters(text)
        
        # 验证结果
        assert "@" not in cleaned
        assert "#" not in cleaned
        assert "$" not in cleaned
        assert "%" not in cleaned
        assert "HelloWorld123测试" in cleaned
    
    def test_format_date(self):
        """测试日期格式化"""
        date_str = "2024-03-09"
        formatted = DataUtils.format_date(date_str, input_format="%Y-%m-%d", output_format="%Y年%m月%d日")
        
        # 验证结果
        assert formatted == "2024年03月09日"
    
    def test_validate_json(self):
        """测试验证JSON格式"""
        valid_json = '{"name": "Alice", "age": 25}'
        invalid_json = '{"name": "Alice", age: 25}'  # 缺少引号
        
        assert DataUtils.validate_json(valid_json) is True
        assert DataUtils.validate_json(invalid_json) is False
    
    def test_clean_json(self):
        """测试清洗JSON数据"""
        dirty_json = '{"name": "Alice", "age": 25, "city": "Beijing", "extra": null}'
        cleaned = DataUtils.clean_json(dirty_json, remove_null=True)
        
        # 验证结果
        assert "extra" not in cleaned
        assert '"name": "Alice"' in cleaned
        assert '"age": 25' in cleaned
        assert '"city": "Beijing"' in cleaned
    
    def test_extract_emails(self):
        """测试提取邮箱地址"""
        text = "Contact us at alice@example.com or bob@test.org for more info."
        emails = DataUtils.extract_emails(text)
        
        # 验证结果
        assert len(emails) == 2
        assert "alice@example.com" in emails
        assert "bob@test.org" in emails
    
    def test_extract_urls(self):
        """测试提取URL"""
        text = "Visit https://example.com or http://test.org for details."
        urls = DataUtils.extract_urls(text)
        
        # 验证结果
        assert len(urls) == 2
        assert "https://example.com" in urls
        assert "http://test.org" in urls


class TestConvenienceFunctions:
    """测试便捷函数"""
    
    def test_validate_email_function(self):
        """测试validate_email便捷函数"""
        assert validate_email("test@example.com") is True
        assert validate_email("invalid") is False
    
    def test_clean_phone_number_function(self):
        """测试clean_phone_number便捷函数"""
        result = clean_phone_number("135-1062-8257", country='CN')
        assert result == "13510628257"
    
    def test_normalize_text_function(self):
        """测试normalize_text便捷函数"""
        text = "  Hello  World  "
        normalized = normalize_text(text)
        assert normalized == "Hello World"
    
    def test_validate_json_function(self):
        """测试validate_json便捷函数"""
        assert validate_json('{"test": "data"}') is True
        assert validate_json('invalid json') is False


if __name__ == "__main__":
    # 直接运行测试
    pytest.main([__file__, "-v"])