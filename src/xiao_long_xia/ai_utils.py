"""
AI辅助工具模块
提供代码解释、Bug诊断、优化建议等功能
"""

import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class AIUtils:
    """AI辅助工具类"""
    
    @staticmethod
    def code_explanation(
        code: str, 
        language: str = "python",
        detail_level: str = "medium"
    ) -> Dict[str, Any]:
        """
        代码解释
        
        Args:
            code: 代码字符串
            language: 编程语言
            detail_level: 详细程度 ('brief', 'medium', 'detailed')
            
        Returns:
            解释结果
            
        Example:
            >>> explanation = AIUtils.code_explanation(
            ...     'def add(a, b): return a + b',
            ...     language='python'
            ... )
            >>> print(explanation['summary'])
        """
        # 这里可以集成DeepSeek API
        # 目前返回基于规则的分析结果
        
        # 基础分析
        lines = code.strip().split('\n')
        line_count = len(lines)
        
        # 检测代码类型
        code_type = "unknown"
        if re.search(r'def\s+\w+\s*\(', code):
            code_type = "function"
        elif re.search(r'class\s+\w+', code):
            code_type = "class"
        elif re.search(r'import\s+|from\s+', code):
            code_type = "import"
        elif re.search(r'=\s*\[|\{', code):
            code_type = "data_structure"
        
        # 复杂度估算
        complexity = "low"
        if line_count > 50:
            complexity = "high"
        elif line_count > 20:
            complexity = "medium"
        
        # 根据详细程度生成解释
        explanations = {
            'brief': f"This is a {code_type} in {language} with {line_count} lines.",
            'medium': f"This {code_type} in {language} contains {line_count} lines. "
                     f"It appears to have {complexity} complexity.",
            'detailed': f"""
Code Analysis:
- Type: {code_type}
- Language: {language}
- Lines: {line_count}
- Complexity: {complexity}
- Structure: {'Well-structured' if line_count < 100 else 'Could be refactored'}

Key Observations:
1. The code appears to be a {code_type}
2. Written in {language}
3. {complexity.capitalize()} complexity level
4. Consider adding comments for clarity
"""
        }
        
        explanation = explanations.get(detail_level, explanations['medium'])
        
        # 生成建议
        suggestions = []
        if line_count > 30:
            suggestions.append("Consider breaking down into smaller functions")
        if not re.search(r'\"\"\"|\'\'\'|#', code):
            suggestions.append("Add documentation comments")
        if complexity == "high":
            suggestions.append("Consider performance optimization")
        
        return {
            'code': code,
            'language': language,
            'type': code_type,
            'line_count': line_count,
            'complexity': complexity,
            'explanation': explanation.strip(),
            'suggestions': suggestions,
            'analysis_time': datetime.now().isoformat(),
        }
    
    @staticmethod
    def bug_diagnosis(
        error_message: str, 
        code_context: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Bug诊断
        
        Args:
            error_message: 错误信息
            code_context: 代码上下文
            language: 编程语言
            
        Returns:
            诊断结果
            
        Example:
            >>> diagnosis = AIUtils.bug_diagnosis(
            ...     "NameError: name 'x' is not defined",
            ...     "print(x)"
            ... )
            >>> print(diagnosis['solution'])
        """
        # 常见错误模式匹配
        error_patterns = {
            'python': {
                r'NameError: name \'(\w+)\' is not defined': {
                    'cause': '变量未定义',
                    'solution': '检查变量名拼写或确保变量已定义',
                    'prevention': '使用前先定义变量，检查作用域'
                },
                r'TypeError:': {
                    'cause': '类型错误',
                    'solution': '检查函数参数类型或操作数类型',
                    'prevention': '添加类型检查或使用类型提示'
                },
                r'SyntaxError:': {
                    'cause': '语法错误',
                    'solution': '检查代码语法，如括号、引号匹配',
                    'prevention': '使用代码编辑器或linter检查语法'
                },
                r'IndexError:': {
                    'cause': '索引错误',
                    'solution': '检查列表/字符串索引是否越界',
                    'prevention': '访问前检查长度'
                },
                r'KeyError:': {
                    'cause': '键错误',
                    'solution': '检查字典键是否存在',
                    'prevention': '使用get()方法或先检查键是否存在'
                },
                r'AttributeError:': {
                    'cause': '属性错误',
                    'solution': '检查对象是否有该属性或方法',
                    'prevention': '使用hasattr()检查属性'
                },
                r'ImportError:': {
                    'cause': '导入错误',
                    'solution': '检查模块名拼写或是否已安装',
                    'prevention': '确保依赖已安装，检查PYTHONPATH'
                },
                r'IndentationError:': {
                    'cause': '缩进错误',
                    'solution': '检查代码缩进是否一致',
                    'prevention': '使用一致的缩进（推荐4个空格）'
                },
            }
        }
        
        # 匹配错误模式
        diagnosis = {
            'cause': '未知错误',
            'solution': '检查代码逻辑和错误信息',
            'prevention': '添加错误处理和日志'
        }
        
        patterns = error_patterns.get(language, {}).items()
        for pattern, info in patterns:
            if re.search(pattern, error_message):
                diagnosis = info
                break
        
        # 提取错误详情
        error_details = {
            'raw_error': error_message,
            'error_type': error_message.split(':')[0] if ':' in error_message else 'Unknown',
            'context_lines': len(code_context.strip().split('\n')),
            'diagnosis_time': datetime.now().isoformat(),
        }
        
        return {
            **error_details,
            **diagnosis,
            'recommended_actions': [
                '仔细阅读错误信息',
                '检查相关代码行',
                '搜索类似错误解决方案',
                '添加调试打印语句',
                '简化代码复现问题'
            ]
        }
    
    @staticmethod
    def code_optimization_suggestions(
        code: str,
        language: str = "python",
        focus_areas: List[str] = None
    ) -> Dict[str, Any]:
        """
        代码优化建议
        
        Args:
            code: 代码字符串
            language: 编程语言
            focus_areas: 关注领域 ('performance', 'readability', 'memory', 'all')
            
        Returns:
            优化建议
            
        Example:
            >>> suggestions = AIUtils.code_optimization_suggestions(
            ...     'for i in range(1000000): x = i * 2',
            ...     focus_areas=['performance']
            ... )
        """
        if focus_areas is None:
            focus_areas = ['all']
        
        suggestions = []
        improvements = []
        
        # 性能优化建议
        if 'performance' in focus_areas or 'all' in focus_areas:
            # 检测大循环
            if re.search(r'for\s+\w+\s+in\s+range\(\d{5,}\)', code):
                suggestions.append("大循环考虑使用向量化操作或并行处理")
                improvements.append("性能提升潜力: 高")
            
            # 检测重复计算
            if len(re.findall(r'len\(', code)) > 3:
                suggestions.append("重复调用len()，考虑缓存结果")
                improvements.append("性能提升潜力: 中")
            
            # 检测字符串拼接
            if code.count('+') > 5 and '"' in code:
                suggestions.append("大量字符串拼接，考虑使用join()")
                improvements.append("性能提升潜力: 中")
        
        # 可读性优化建议
        if 'readability' in focus_areas or 'all' in focus_areas:
            lines = code.split('\n')
            avg_length = sum(len(line.strip()) for line in lines) / max(len(lines), 1)
            
            if avg_length > 80:
                suggestions.append("行过长，考虑拆分或换行")
                improvements.append("可读性提升: 高")
            
            if not re.search(r'\"\"\"|\'\'\'|#\s+', code):
                suggestions.append("缺少文档字符串和注释")
                improvements.append("可读性提升: 高")
            
            # 检查魔法数字
            magic_numbers = re.findall(r'\b\d{2,}\b', code)
            if magic_numbers:
                suggestions.append(f"发现魔法数字: {magic_numbers}，考虑定义为常量")
                improvements.append("可读性提升: 中")
        
        # 内存优化建议
        if 'memory' in focus_areas or 'all' in focus_areas:
            if re.search(r'\[\s*\]\s*\*\s*\d+', code):
                suggestions.append("列表乘法可能创建多个引用，考虑使用列表推导式")
                improvements.append("内存优化潜力: 中")
            
            if 'yield' in code:
                suggestions.append("使用生成器良好，有助于内存优化")
                improvements.append("内存优化: 已优化")
        
        # 如果没有具体建议，提供通用建议
        if not suggestions:
            suggestions = [
                "代码结构良好，继续保持",
                "考虑添加单元测试",
                "确保错误处理完善",
                "文档化公共接口"
            ]
            improvements = ["维护性: 良好"]
        
        return {
            'code_snippet': code[:100] + ('...' if len(code) > 100 else ''),
            'language': language,
            'focus_areas': focus_areas,
            'suggestions': suggestions,
            'improvements': improvements,
            'complexity_score': len(code.split('\n')) / 10,  # 简单复杂度评分
            'optimization_time': datetime.now().isoformat(),
        }
    
    @staticmethod
    def generate_documentation(
        code: str,
        language: str = "python",
        style: str = "google"
    ) -> Dict[str, Any]:
        """
        生成代码文档
        
        Args:
            code: 代码字符串
            language: 编程语言
            style: 文档风格 ('google', 'numpy', 'sphinx')
            
        Returns:
            生成的文档
            
        Example:
            >>> docs = AIUtils.generate_documentation(
            ...     'def add(a, b): return a + b',
            ...     style='google'
            ... )
            >>> print(docs['documentation'])
        """
        # 提取函数信息
        function_match = re.search(r'def\s+(\w+)\s*\((.*?)\)', code, re.DOTALL)
        
        if function_match:
            func_name = function_match.group(1)
            params = function_match.group(2).strip()
            
            # 解析参数
            param_list = []
            if params:
                for param in params.split(','):
                    param = param.strip()
                    if '=' in param:
                        name, default = param.split('=', 1)
                        param_list.append({
                            'name': name.strip(),
                            'default': default.strip(),
                            'type': 'any'
                        })
                    else:
                        param_list.append({
                            'name': param,
                            'default': None,
                            'type': 'any'
                        })
            
            # 根据风格生成文档
            if style == 'google':
                docstring = f'\"\"\"{func_name}.\n\n'
                if param_list:
                    docstring += 'Args:\n'
                    for param in param_list:
                        default_str = f' (default: {param["default"]})' if param['default'] else ''
                        docstring += f'    {param["name"]}: Description{default_str}\n'
                docstring += '\nReturns:\n    Description\n\"\"\"'
            
            elif style == 'numpy':
                docstring = f'\"\"\"\n{func_name}\n\nParameters\n----------\n'
                if param_list:
                    for param in param_list:
                        default_str = f', default {param["default"]}' if param['default'] else ''
                        docstring += f'{param["name"]} : type{default_str}\n    Description\n'
                docstring += '\nReturns\n-------\ntype\n    Description\n\"\"\"'
            
            else:  # sphinx style
                docstring = f'\"\"\"{func_name}\n\n:param param: Description\n:type param: type\n:return: Description\n:rtype: type\n\"\"\"'
        
        else:
            # 非函数代码的通用文档
            docstring = '\"\"\"\nCode documentation\n\nOverview:\n    Brief description of the code\n\nNotes:\n    Additional information\n\"\"\"'
        
        return {
            'code': code,
            'language': language,
            'style': style,
            'documentation': docstring,
            'suggested_improvements': [
                '添加具体参数类型',
                '描述返回值含义',
                '添加示例用法',
                '说明可能抛出的异常'
            ],
            'generation_time': datetime.now().isoformat(),
        }


# 便捷函数
def code_explanation(code: str, language: str = "python", detail_level: str = "medium") -> Dict[str, Any]:
    """代码解释（便捷函数）"""
    return AIUtils.code_explanation(code, language, detail_level)

def bug_diagnosis(error_message: str, code_context: str, language: str = "python") -> Dict[str, Any]:
    """Bug诊断（便捷函数）"""
    return AIUtils.bug_diagnosis(error_message, code_context, language)

def code_optimization_suggestions(code: str, language: str = "python", focus_areas: List[str] = None) -> Dict[str, Any]:
    """代码优化建议（便捷函数）"""
    return AIUtils.code_optimization_suggestions(code, language, focus_areas)

def generate_documentation(code: str, language: str = "python", style: str = "google") -> Dict[str, Any]:
    """生成代码文档（便捷函数）"""
    return AIUtils.generate_documentation(code, language, style)