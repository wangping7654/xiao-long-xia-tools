"""
测试文件工具模块
"""

import os
import tempfile
import shutil
from pathlib import Path
import pytest

from xiao_long_xia import FileUtils, batch_rename_files, convert_file_encoding, find_duplicate_files


class TestFileUtils:
    """测试FileUtils类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.test_dir = tempfile.mkdtemp(prefix="test_file_utils_")
        print(f"测试目录: {self.test_dir}")
    
    def teardown_method(self):
        """每个测试方法后的清理"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_batch_rename_files_basic(self):
        """测试基本批量重命名"""
        # 创建测试文件
        test_files = ["file1.txt", "file2.txt", "file3.txt", "image.jpg"]
        for filename in test_files:
            filepath = os.path.join(self.test_dir, filename)
            with open(filepath, 'w') as f:
                f.write(f"Content of {filename}")
        
        # 执行重命名
        result = FileUtils.batch_rename_files(
            self.test_dir,
            r'file(\d+)\.txt',
            r'document_\1.md'
        )
        
        # 验证结果
        assert len(result) == 3  # 3个txt文件被重命名
        assert "document_1.md" in result
        assert "document_2.md" in result
        assert "document_3.md" in result
        
        # 验证文件存在
        for new_name in result:
            assert os.path.exists(os.path.join(self.test_dir, new_name))
        
        # 验证原始文件不存在
        assert not os.path.exists(os.path.join(self.test_dir, "file1.txt"))
    
    def test_batch_rename_files_dry_run(self):
        """测试试运行模式"""
        # 创建测试文件
        filepath = os.path.join(self.test_dir, "test.txt")
        with open(filepath, 'w') as f:
            f.write("Test content")
        
        # 执行试运行
        result = FileUtils.batch_rename_files(
            self.test_dir,
            r'test\.txt',
            r'renamed.txt',
            dry_run=True
        )
        
        # 验证结果
        assert result == ["renamed.txt"]
        
        # 验证文件未被实际重命名
        assert os.path.exists(filepath)
        assert not os.path.exists(os.path.join(self.test_dir, "renamed.txt"))
    
    def test_batch_rename_files_no_match(self):
        """测试无匹配文件的情况"""
        # 创建不匹配的文件
        filepath = os.path.join(self.test_dir, "image.jpg")
        with open(filepath, 'w') as f:
            f.write("Image content")
        
        # 执行重命名
        result = FileUtils.batch_rename_files(
            self.test_dir,
            r'\.txt$',
            r'.md'
        )
        
        # 验证无文件被重命名
        assert result == []
        assert os.path.exists(filepath)
    
    def test_convert_file_encoding(self):
        """测试文件编码转换"""
        # 创建测试文件（UTF-8编码）
        filepath = os.path.join(self.test_dir, "test.txt")
        content = "测试内容 - Test content - テストコンテンツ"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 执行编码转换
        result = FileUtils.convert_file_encoding(
            filepath,
            'utf-8',
            'utf-8',  # 相同编码，测试功能
            backup=False
        )
        
        # 验证成功
        assert result is True
        
        # 验证文件内容不变
        with open(filepath, 'r', encoding='utf-8') as f:
            assert f.read() == content
    
    def test_convert_file_encoding_with_backup(self):
        """测试带备份的文件编码转换"""
        # 创建测试文件
        filepath = os.path.join(self.test_dir, "test.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("Test content")
        
        # 执行带备份的编码转换
        result = FileUtils.convert_file_encoding(
            filepath,
            'utf-8',
            'utf-8',
            backup=True
        )
        
        # 验证成功
        assert result is True
        
        # 验证备份文件存在
        backup_path = filepath + ".bak"
        assert os.path.exists(backup_path)
        
        # 清理备份文件
        os.remove(backup_path)
    
    def test_find_duplicate_files(self):
        """测试查找重复文件"""
        # 创建重复文件
        content1 = "相同的文件内容"
        content2 = "不同的文件内容"
        
        # 文件1和文件3内容相同
        with open(os.path.join(self.test_dir, "file1.txt"), 'w') as f:
            f.write(content1)
        with open(os.path.join(self.test_dir, "file2.txt"), 'w') as f:
            f.write(content2)
        with open(os.path.join(self.test_dir, "file3.txt"), 'w') as f:
            f.write(content1)
        
        # 查找重复文件
        duplicates = FileUtils.find_duplicate_files(self.test_dir, min_size=1)
        
        # 验证结果
        assert len(duplicates) == 1  # 应该有一组重复文件
        
        for hash_val, files in duplicates.items():
            assert len(files) == 2  # file1.txt 和 file3.txt
            filenames = [os.path.basename(f) for f in files]
            assert "file1.txt" in filenames
            assert "file3.txt" in filenames
            assert "file2.txt" not in filenames
    
    def test_find_duplicate_files_no_duplicates(self):
        """测试无重复文件的情况"""
        # 创建不同内容的文件
        for i in range(3):
            filepath = os.path.join(self.test_dir, f"file{i}.txt")
            with open(filepath, 'w') as f:
                f.write(f"Unique content {i}")
        
        # 查找重复文件
        duplicates = FileUtils.find_duplicate_files(self.test_dir)
        
        # 验证无重复文件
        assert duplicates == {}
    
    def test_find_duplicate_files_min_size(self):
        """测试最小文件大小过滤"""
        # 创建小文件
        small_file = os.path.join(self.test_dir, "small.txt")
        with open(small_file, 'w') as f:
            f.write("x")  # 1字节
        
        # 创建大文件（相同内容）
        large_file = os.path.join(self.test_dir, "large.txt")
        with open(large_file, 'w') as f:
            f.write("x" * 1024)  # 1KB
        
        # 查找重复文件，设置最小大小
        duplicates = FileUtils.find_duplicate_files(self.test_dir, min_size=1024)
        
        # 验证小文件被过滤
        assert duplicates == {}
    
    def test_organize_files_by_extension(self):
        """测试按扩展名整理文件"""
        # 创建各种类型的文件
        files = {
            "doc1.txt": "Text document",
            "doc2.txt": "Another text",
            "image1.jpg": "JPEG image",
            "image2.png": "PNG image",
            "data.csv": "CSV data",
            "archive.zip": "ZIP archive",
        }
        
        for filename, content in files.items():
            filepath = os.path.join(self.test_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
        
        # 执行文件整理
        result = FileUtils.organize_files_by_extension(self.test_dir)
        
        # 验证结果
        assert "documents" in result
        assert "images" in result
        assert "archives" in result
        
        # 验证文件被移动到正确目录
        assert os.path.exists(os.path.join(self.test_dir, "documents", "doc1.txt"))
        assert os.path.exists(os.path.join(self.test_dir, "images", "image1.jpg"))
        assert os.path.exists(os.path.join(self.test_dir, "archives", "archive.zip"))
        
        # 验证其他目录（未指定扩展名）
        assert os.path.exists(os.path.join(self.test_dir, "others", "data.csv"))


class TestConvenienceFunctions:
    """测试便捷函数"""
    
    def setup_method(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_convenience_")
    
    def teardown_method(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_batch_rename_files_function(self):
        """测试batch_rename_files便捷函数"""
        # 创建测试文件
        filepath = os.path.join(self.test_dir, "test.txt")
        with open(filepath, 'w') as f:
            f.write("Test")
        
        # 使用便捷函数
        result = batch_rename_files(self.test_dir, r'test\.txt', r'renamed.txt')
        
        # 验证结果
        assert result == ["renamed.txt"]
        assert os.path.exists(os.path.join(self.test_dir, "renamed.txt"))
    
    def test_convert_file_encoding_function(self):
        """测试convert_file_encoding便捷函数"""
        # 创建测试文件
        filepath = os.path.join(self.test_dir, "test.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("Test")
        
        # 使用便捷函数
        result = convert_file_encoding(filepath, 'utf-8', 'utf-8', backup=False)
        
        # 验证结果
        assert result is True
    
    def test_find_duplicate_files_function(self):
        """测试find_duplicate_files便捷函数"""
        # 创建重复文件（确保内容足够长）
        file1 = os.path.join(self.test_dir, "file1.txt")
        file2 = os.path.join(self.test_dir, "file2.txt")
        
        content = "Same content " * 100  # 确保内容足够长
        
        with open(file1, 'w') as f:
            f.write(content)
        with open(file2, 'w') as f:
            f.write(content)
        
        # 使用便捷函数
        result = find_duplicate_files(self.test_dir, min_size=1)
        
        # 验证结果
        assert len(result) == 1
        for files in result.values():
            assert len(files) == 2


if __name__ == "__main__":
    # 直接运行测试
    pytest.main([__file__, "-v"])