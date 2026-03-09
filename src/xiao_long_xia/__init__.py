"""
Xiao Long Xia Tools - Python Development Utilities
AI-assisted tools for developers

Version: 0.1.0
Author: Xiao Long Xia (AI-assisted)
License: MIT
"""

from .file_utils import FileUtils
from .data_utils import DataUtils
from .dev_utils import DevUtils
from .ai_utils import AIUtils

# 便捷函数
from .file_utils import batch_rename_files, convert_file_encoding, find_duplicate_files
from .data_utils import validate_email, clean_phone_number, normalize_text
from .dev_utils import generate_project_template, extract_code_snippets
from .ai_utils import code_explanation, bug_diagnosis

__version__ = "0.1.0"
__author__ = "Xiao Long Xia (AI-assisted)"
__license__ = "MIT"

__all__ = [
    # 类
    'FileUtils',
    'DataUtils',
    'DevUtils',
    'AIUtils',
    
    # 函数
    'batch_rename_files',
    'convert_file_encoding',
    'find_duplicate_files',
    'validate_email',
    'clean_phone_number',
    'normalize_text',
    'generate_project_template',
    'extract_code_snippets',
    'code_explanation',
    'bug_diagnosis',
]