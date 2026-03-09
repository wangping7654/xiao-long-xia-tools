"""
文件处理工具模块
提供批量重命名、编码转换、重复文件查找等功能
"""

import os
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
import shutil


class FileUtils:
    """文件处理工具类"""
    
    @staticmethod
    def batch_rename_files(
        directory: str, 
        pattern: str, 
        new_pattern: str,
        dry_run: bool = False
    ) -> List[str]:
        """
        批量重命名文件
        
        Args:
            directory: 目录路径
            pattern: 匹配模式（支持正则表达式）
            new_pattern: 新文件名模式
            dry_run: 试运行模式，不实际重命名
            
        Returns:
            重命名后的文件列表
            
        Example:
            >>> FileUtils.batch_rename_files('./docs', r'(\\d+)\\.txt', r'doc_\\1.md')
            ['doc_1.md', 'doc_2.md']
        """
        renamed_files = []
        try:
            for filename in os.listdir(directory):
                if re.match(pattern, filename):
                    new_name = re.sub(pattern, new_pattern, filename)
                    old_path = os.path.join(directory, filename)
                    new_path = os.path.join(directory, new_name)
                    
                    if not dry_run:
                        os.rename(old_path, new_path)
                    
                    renamed_files.append(new_name)
            
            return renamed_files
        except Exception as e:
            raise Exception(f"批量重命名失败: {str(e)}")
    
    @staticmethod
    def convert_file_encoding(
        file_path: str, 
        from_encoding: str, 
        to_encoding: str,
        backup: bool = True
    ) -> bool:
        """
        转换文件编码
        
        Args:
            file_path: 文件路径
            from_encoding: 原始编码
            to_encoding: 目标编码
            backup: 是否创建备份
            
        Returns:
            是否成功
            
        Example:
            >>> FileUtils.convert_file_encoding('data.txt', 'gbk', 'utf-8')
            True
        """
        try:
            # 创建备份
            if backup:
                backup_path = f"{file_path}.bak"
                shutil.copy2(file_path, backup_path)
            
            # 读取原始文件
            with open(file_path, 'r', encoding=from_encoding, errors='ignore') as f:
                content = f.read()
            
            # 写入新编码
            with open(file_path, 'w', encoding=to_encoding) as f:
                f.write(content)
            
            return True
        except Exception as e:
            raise Exception(f"文件编码转换失败: {str(e)}")
    
    @staticmethod
    def find_duplicate_files(
        directory: str,
        min_size: int = 1024  # 1KB
    ) -> Dict[str, List[str]]:
        """
        查找重复文件（基于内容哈希）
        
        Args:
            directory: 目录路径
            min_size: 最小文件大小（字节），小于此大小的文件忽略
            
        Returns:
            哈希值到文件列表的映射
            
        Example:
            >>> duplicates = FileUtils.find_duplicate_files('./photos')
            >>> for hash_val, files in duplicates.items():
            ...     print(f"重复文件组 ({len(files)}个文件):")
            ...     for file in files:
            ...         print(f"  - {file}")
        """
        hash_map = {}
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    # 检查文件大小
                    file_size = os.path.getsize(file_path)
                    if file_size < min_size:
                        continue
                    
                    # 计算文件哈希
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    if file_hash not in hash_map:
                        hash_map[file_hash] = []
                    hash_map[file_hash].append(file_path)
                except (OSError, IOError):
                    # 跳过无法访问的文件
                    continue
        
        # 只返回有重复的文件
        return {h: files for h, files in hash_map.items() if len(files) > 1}
    
    @staticmethod
    def organize_files_by_extension(
        directory: str,
        extensions_map: Optional[Dict[str, str]] = None
    ) -> Dict[str, List[str]]:
        """
        按扩展名整理文件
        
        Args:
            directory: 目录路径
            extensions_map: 扩展名到文件夹的映射
            
        Returns:
            整理结果
            
        Example:
            >>> mapping = {
            ...     'jpg': 'images',
            ...     'png': 'images',
            ...     'txt': 'documents',
            ...     'pdf': 'documents'
            ... }
            >>> FileUtils.organize_files_by_extension('./downloads', mapping)
        """
        if extensions_map is None:
            extensions_map = {
                'jpg': 'images',
                'jpeg': 'images',
                'png': 'images',
                'gif': 'images',
                'bmp': 'images',
                'txt': 'documents',
                'pdf': 'documents',
                'doc': 'documents',
                'docx': 'documents',
                'xls': 'documents',
                'xlsx': 'documents',
                'mp3': 'audio',
                'wav': 'audio',
                'mp4': 'video',
                'avi': 'video',
                'mkv': 'video',
                'zip': 'archives',
                'rar': 'archives',
                '7z': 'archives',
            }
        
        result = {}
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                # 获取文件扩展名
                _, ext = os.path.splitext(filename)
                ext = ext.lower().lstrip('.')
                
                # 确定目标文件夹
                target_folder = extensions_map.get(ext, 'others')
                
                # 创建目标文件夹
                target_path = os.path.join(directory, target_folder)
                os.makedirs(target_path, exist_ok=True)
                
                # 移动文件
                new_path = os.path.join(target_path, filename)
                shutil.move(file_path, new_path)
                
                # 记录结果
                if target_folder not in result:
                    result[target_folder] = []
                result[target_folder].append(filename)
        
        return result


# 便捷函数
def batch_rename_files(directory: str, pattern: str, new_pattern: str, dry_run: bool = False) -> List[str]:
    """批量重命名文件（便捷函数）"""
    return FileUtils.batch_rename_files(directory, pattern, new_pattern, dry_run)

def convert_file_encoding(file_path: str, from_encoding: str, to_encoding: str, backup: bool = True) -> bool:
    """转换文件编码（便捷函数）"""
    return FileUtils.convert_file_encoding(file_path, from_encoding, to_encoding, backup)

def find_duplicate_files(directory: str, min_size: int = 1024) -> Dict[str, List[str]]:
    """查找重复文件（便捷函数）"""
    return FileUtils.find_duplicate_files(directory, min_size)

def organize_files_by_extension(directory: str, extensions_map: Optional[Dict[str, str]] = None) -> Dict[str, List[str]]:
    """按扩展名整理文件（便捷函数）"""
    return FileUtils.organize_files_by_extension(directory, extensions_map)