"""
Xiao Long Xia Tools - 命令行接口
基于Click框架的CLI工具
"""

import click
import sys
import os
from pathlib import Path
from typing import Optional, List
from functools import wraps

from .file_utils import FileUtils
from .data_utils import DataUtils
from .dev_utils import DevUtils
from .ai_utils import AIUtils

# 版本信息
__version__ = "0.1.0"

# 全局选项
def common_options(func):
    """通用命令行选项装饰器"""
    @click.option('--verbose', '-v', is_flag=True, help='详细输出模式')
    @click.option('--quiet', '-q', is_flag=True, help='安静模式，仅输出结果')
    @click.option('--output', '-o', type=click.Path(), help='输出文件路径')
    @click.option('--format', '-f', type=click.Choice(['json', 'yaml', 'csv', 'text']), 
                  default='text', help='输出格式')
    @click.option('--dry-run', is_flag=True, help='试运行，不实际执行操作')
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@click.group()
@click.version_option(version=__version__)
@click.option('--debug', is_flag=True, help='调试模式')
def cli(debug):
    """Xiao Long Xia Tools - Python开发工具集
    
    一个AI辅助的Python工具库，包含文件管理、数据处理、
    开发工具和AI辅助功能。
    
    示例:
        xiao-long-xia find-duplicates /path/to/dir
        xiao-long-xia clean-csv data.csv --output cleaned.csv
        xiao-long-xia setup-project myproject
    """
    if debug:
        click.echo("调试模式已启用")
        import logging
        logging.basicConfig(level=logging.DEBUG)

# ==================== 文件工具命令 ====================

@cli.group()
def file():
    """文件操作工具"""
    pass

@file.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
@click.option('--algorithm', '-a', type=click.Choice(['md5', 'sha1', 'sha256', 'size']), 
              default='md5', help='哈希算法')
@click.option('--min-size', type=int, help='最小文件大小（字节）')
@click.option('--max-size', type=int, help='最大文件大小（字节）')
@click.option('--extensions', '-e', multiple=True, help='文件扩展名过滤')
def find_duplicates(directory, algorithm, min_size, max_size, extensions):
    """查找重复文件
    
    DIRECTORY: 要扫描的目录路径
    """
    try:
        duplicates = FileUtils.find_duplicate_files(
            directory=directory,
            hash_algorithm=algorithm,
            min_size=min_size,
            max_size=max_size,
            extensions=list(extensions) if extensions else None
        )
        
        if not duplicates:
            click.echo("未找到重复文件")
            return
            
        click.echo(f"找到 {len(duplicates)} 组重复文件:")
        for i, group in enumerate(duplicates, 1):
            click.echo(f"\n组 {i} ({len(group)} 个文件):")
            for filepath in group:
                click.echo(f"  - {filepath}")
                
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)

@file.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
@click.option('--target-dir', '-t', type=click.Path(file_okay=False), 
              help='目标目录（默认在源目录内创建organized文件夹）')
@click.option('--copy/--move', default=False, help='复制文件而不是移动')
@click.option('--dry-run', is_flag=True, help='试运行，显示将要执行的操作')
def organize(directory, target_dir, copy, dry_run):
    """按文件类型组织文件
    
    DIRECTORY: 要组织的目录路径
    """
    try:
        result = FileUtils.organize_files_by_type(
            source_dir=directory,
            target_dir=target_dir,
            copy_files=copy,
            dry_run=dry_run
        )
        
        if dry_run:
            click.echo("试运行结果（不会实际执行）:")
            for action in result.get('actions', []):
                click.echo(f"  {action}")
            return
            
        click.echo(f"组织完成:")
        click.echo(f"  处理的文件: {result.get('files_processed', 0)}")
        click.echo(f"  创建的目录: {result.get('directories_created', 0)}")
        click.echo(f"  目标位置: {result.get('target_directory', 'N/A')}")
        
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)

@file.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
@click.option('--human-readable', '-h', is_flag=True, help='人类可读格式')
@click.option('--depth', '-d', type=int, default=0, help='目录深度（0表示无限）')
def size(directory, human_readable, depth):
    """计算目录大小
    
    DIRECTORY: 要计算大小的目录路径
    """
    try:
        total_size = FileUtils.calculate_directory_size(
            directory=directory,
            depth=depth if depth > 0 else None
        )
        
        if human_readable:
            # 转换为人类可读格式
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if total_size < 1024.0:
                    size_str = f"{total_size:.2f} {unit}"
                    break
                total_size /= 1024.0
            else:
                size_str = f"{total_size:.2f} PB"
        else:
            size_str = f"{total_size} 字节"
            
        click.echo(f"目录大小: {size_str}")
        
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)

# ==================== 数据工具命令 ====================

@cli.group()
def data():
    """数据处理工具"""
    pass

@data.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.option('--output', '-o', type=click.Path(dir_okay=False), 
              help='输出文件路径（默认：input_cleaned.csv）')
@click.option('--encoding', '-e', default='utf-8', help='文件编码')
@click.option('--remove-empty', is_flag=True, help='删除空行')
@click.option('--trim-whitespace', is_flag=True, help='修剪空白字符')
@click.option('--standardize-dates', is_flag=True, help='标准化日期格式')
def clean_csv(input_file, output, encoding, remove_empty, trim_whitespace, standardize_dates):
    """清理CSV文件数据
    
    INPUT_FILE: 输入的CSV文件路径
    """
    try:
        if not output:
            output = Path(input_file).stem + '_cleaned.csv'
            
        result = DataUtils.clean_csv_data(
            file_path=input_file,
            output_path=output,
            encoding=encoding,
            remove_empty_rows=remove_empty,
            trim_whitespace=trim_whitespace,
            standardize_dates=standardize_dates
        )
        
        click.echo(f"CSV清理完成:")
        click.echo(f"  输入文件: {input_file}")
        click.echo(f"  输出文件: {output}")
        click.echo(f"  处理行数: {result.get('rows_processed', 0)}")
        click.echo(f"  清理行数: {result.get('rows_cleaned', 0)}")
        
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)

@data.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.option('--output', '-o', type=click.Path(dir_okay=False), 
              help='输出文件路径（默认：input.json）')
@click.option('--encoding', '-e', default='utf-8', help='文件编码')
@click.option('--orient', default='records', 
              type=click.Choice(['split', 'records', 'index', 'columns', 'values', 'table']),
              help='DataFrame方向')
def json_to_csv(input_file, output, encoding, orient):
    """JSON文件转换为CSV
    
    INPUT_FILE: 输入的JSON文件路径
    """
    try:
        if not output:
            output = Path(input_file).stem + '.csv'
            
        result = DataUtils.json_to_dataframe(
            json_file=input_file,
            output_file=output,
            encoding=encoding,
            orient=orient
        )
        
        click.echo(f"JSON转CSV完成:")
        click.echo(f"  输入文件: {input_file}")
        click.echo(f"  输出文件: {output}")
        click.echo(f"  数据行数: {result.get('row_count', 0)}")
        click.echo(f"  数据列数: {result.get('column_count', 0)}")
        
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)

# ==================== 开发工具命令 ====================

@cli.group()
def dev():
    """开发工具"""
    pass

@dev.command()
@click.argument('project_name')
@click.option('--template', '-t', 
              type=click.Choice(['basic', 'package', 'cli', 'web', 'data']),
              default='basic', help='项目模板类型')
@click.option('--path', '-p', type=click.Path(file_okay=False), 
              help='项目路径（默认：当前目录）')
@click.option('--author', '-a', help='作者名称')
@click.option('--description', '-d', help='项目描述')
def setup_project(project_name, template, path, author, description):
    """设置新项目结构
    
    PROJECT_NAME: 项目名称
    """
    try:
        result = DevUtils.setup_project_structure(
            project_name=project_name,
            template_type=template,
            base_path=path or os.getcwd(),
            author=author,
            description=description
        )
        
        click.echo(f"项目设置完成:")
        click.echo(f"  项目名称: {project_name}")
        click.echo(f"  项目路径: {result.get('project_path', 'N/A')}")
        click.echo(f"  创建的文件: {len(result.get('files_created', []))}")
        click.echo(f"  模板类型: {template}")
        
        if result.get('files_created'):
            click.echo("\n创建的文件:")
            for filepath in result['files_created']:
                click.echo(f"  - {filepath}")
                
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)

# ==================== AI工具命令 ====================

@cli.group()
def ai():
    """AI辅助工具"""
    pass

@ai.command()
@click.argument('text', required=False)
@click.option('--file', '-f', type=click.Path(exists=True, dir_okay=False),
              help='输入文件路径（如果不直接提供文本）')
@click.option('--ratio', '-r', type=float, default=0.3, 
              help='摘要比例（0.1-0.9）')
@click.option('--language', '-l', default='zh', 
              type=click.Choice(['zh', 'en', 'ja', 'ko']),
              help='输出语言')
def summarize(text, file, ratio, language):
    """文本摘要
    
    TEXT: 要摘要的文本（或使用--file选项）
    """
    try:
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
        elif not text:
            # 从标准输入读取
            text = sys.stdin.read()
            
        if not text:
            click.echo("错误: 没有提供文本", err=True)
            sys.exit(1)
            
        summary = AIUtils.summarize_text(
            text=text,
            ratio=ratio,
            language=language
        )
        
        click.echo("文本摘要:")
        click.echo("=" * 50)
        click.echo(summary)
        click.echo("=" * 50)
        
        # 统计信息
        original_len = len(text)
        summary_len = len(summary)
        compression = 1 - (summary_len / original_len)
        
        click.echo(f"\n统计:")
        click.echo(f"  原文长度: {original_len} 字符")
        click.echo(f"  摘要长度: {summary_len} 字符")
        click.echo(f"  压缩率: {compression:.1%}")
        
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)

@ai.command()
@click.argument('text', required=False)
@click.option('--file', '-f', type=click.Path(exists=True, dir_okay=False),
              help='输入文件路径（如果不直接提供文本）')
@click.option('--top-n', '-n', type=int, default=10, help='提取关键词数量')
@click.option('--language', '-l', default='zh', 
              type=click.Choice(['zh', 'en', 'ja', 'ko']),
              help='文本语言')
def keywords(text, file, top_n, language):
    """提取关键词
    
    TEXT: 要提取关键词的文本（或使用--file选项）
    """
    try:
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
        elif not text:
            # 从标准输入读取
            text = sys.stdin.read()
            
        if not text:
            click.echo("错误: 没有提供文本", err=True)
            sys.exit(1)
            
        keywords = AIUtils.extract_keywords(
            text=text,
            top_n=top_n,
            language=language
        )
        
        click.echo(f"提取的关键词（前{top_n}个）:")
        click.echo("=" * 50)
        for i, (keyword, score) in enumerate(keywords, 1):
            click.echo(f"{i:2d}. {keyword} ({score:.3f})")
        click.echo("=" * 50)
        
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)

# ==================== 工具命令 ====================

@cli.command()
def version():
    """显示版本信息"""
    click.echo(f"Xiao Long Xia Tools v{__version__}")
    click.echo("一个AI辅助的Python开发工具集")
    click.echo("作者: Xiao Long Xia (AI-assisted)")
    click.echo("许可证: MIT")
    click.echo("GitHub: https://github.com/wangping7654/xiao-long-xia-tools")

@cli.command()
def info():
    """显示工具信息"""
    from . import __version__, __author__, __license__
    
    click.echo("=" * 50)
    click.echo("Xiao Long Xia Tools - 信息")
    click.echo("=" * 50)
    click.echo(f"版本: {__version__}")
    click.echo(f"作者: {__author__}")
    click.echo(f"许可证: {__license__}")
    click.echo()
    
    # 模块信息
    click.echo("可用模块:")
    click.echo("  - FileUtils - 文件操作工具")
    click.echo("  - DataUtils - 数据处理工具")
    click.echo("  - DevUtils  - 开发工具")
    click.echo("  - AIUtils   - AI辅助工具")
    click.echo()
    
    # 快速示例
    click.echo("快速示例:")
    click.echo("  xiao-long-xia find-duplicates /path/to/dir")
    click.echo("  xiao-long-xia clean-csv data.csv")
    click.echo("  xiao-long-xia setup-project myproject")
    click.echo("  xiao-long-xia summarize --file document.txt")
    click.echo()
    
    click.echo("详细文档: https://github.com/wangping7654/xiao-long-xia-tools")
    click.echo("=" * 50)

# ==================== 主入口点 ====================

def main():
    """命令行主入口点"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n操作已取消")
        sys.exit(130)
    except Exception as e:
        if '--debug' in sys.argv:
            raise
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()