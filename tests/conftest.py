"""
Pytest 配置和共享fixture
"""

import pytest
import tempfile
import shutil
import os


@pytest.fixture
def temp_directory():
    """创建临时目录的fixture"""
    temp_dir = tempfile.mkdtemp(prefix="xiao_long_xia_test_")
    yield temp_dir
    # 清理
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_text_file(temp_directory):
    """创建示例文本文件的fixture"""
    filepath = os.path.join(temp_directory, "sample.txt")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("这是一段测试文本\n包含多行内容\n用于测试文件工具")
    return filepath


@pytest.fixture
def sample_data_files(temp_directory):
    """创建多个示例数据文件的fixture"""
    files = []
    for i in range(3):
        filepath = os.path.join(temp_directory, f"data_{i}.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"数据文件 {i} 的内容")
        files.append(filepath)
    return files


@pytest.fixture
def duplicate_files(temp_directory):
    """创建重复文件的fixture"""
    # 创建两组重复文件
    files = []
    
    # 第一组重复文件（3个相同）
    for i in range(3):
        filepath = os.path.join(temp_directory, f"dup1_{i}.txt")
        with open(filepath, 'w') as f:
            f.write("相同的文件内容 - 第一组")
        files.append(filepath)
    
    # 第二组重复文件（2个相同）
    for i in range(2):
        filepath = os.path.join(temp_directory, f"dup2_{i}.txt")
        with open(filepath, 'w') as f:
            f.write("相同的文件内容 - 第二组")
        files.append(filepath)
    
    # 一个唯一文件
    unique_file = os.path.join(temp_directory, "unique.txt")
    with open(unique_file, 'w') as f:
        f.write("唯一的内容")
    files.append(unique_file)
    
    return files