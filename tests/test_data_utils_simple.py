"""
简化版数据工具测试
只测试实际存在的功能
"""

import pytest
from xiao_long_xia import DataUtils, validate_email, clean_phone_number, normalize_text, validate_json


def test_validate_email():
    """测试邮箱验证"""
    assert validate_email("test@example.com") is True
    assert validate_email("invalid") is False


def test_clean_phone_number():
    """测试手机号清洗"""
    # 测试中国手机号
    result = clean_phone_number("135-1062-8257", country_code='CN')
    assert result == "13510628257"
    
    # 测试带国际区号
    result = clean_phone_number("+86 138-0013-8000", country_code='CN')
    assert result == "13800138000"


def test_normalize_text():
    """测试文本标准化"""
    text = "  Hello  World  "
    result = normalize_text(text)
    assert result == "Hello World"
    
    # 测试基本功能
    result = normalize_text("TEST")
    assert result == "TEST"  # 没有转换为小写


def test_validate_json():
    """测试JSON验证"""
    assert validate_json('{"name": "Alice", "age": 25}') is True
    assert validate_json('invalid json') is False


def test_extract_emails():
    """测试提取邮箱"""
    text = "Contact alice@example.com and bob@test.org"
    emails = DataUtils.extract_emails(text)
    assert len(emails) == 2
    assert "alice@example.com" in emails
    assert "bob@test.org" in emails


def test_extract_urls():
    """测试提取URL"""
    text = "Visit https://example.com and http://test.org"
    urls = DataUtils.extract_urls(text)
    assert len(urls) == 2
    assert "https://example.com" in urls
    assert "http://test.org" in urls


def test_remove_duplicates():
    """测试移除重复项"""
    data = [1, 2, 2, 3, 3, 3]
    result = DataUtils.remove_duplicates(data)
    assert result == [1, 2, 3]


def test_remove_special_characters():
    """测试移除特殊字符"""
    text = "Hello@World#123"
    result = DataUtils.remove_special_characters(text)
    assert "@" not in result
    assert "#" not in result
    assert "HelloWorld123" in result


def test_format_date():
    """测试日期格式化"""
    result = DataUtils.format_date("2024-03-09", input_format="%Y-%m-%d", output_format="%Y/%m/%d")
    assert result == "2024/03/09"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])