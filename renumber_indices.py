#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本功能：重新编号 fielddata 文件夹中所有JSON文件的 index 参数
使每个文件中的问题 index 从 0 开始递增
"""

import json
from pathlib import Path


def renumber_indices(file_path):
    """
    重新编号指定文件中的 index 参数
    
    Args:
        file_path: JSON文件路径
    
    Returns:
        更新的问题数量
    """
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 重新编号 index
        examples = data.get("example", [])
        for i, example in enumerate(examples):
            example['index'] = i
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return len(examples)
    
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return 0


def main():
    """主函数"""
    fielddata_dir = Path("/home/azura/code/python/GAOKAO-Bench-main (Copy)/fielddata")
    
    print("="*70)
    print("重新编号 fielddata 文件中的 index 参数")
    print("="*70 + "\n")
    
    # 获取所有JSON文件
    json_files = sorted(fielddata_dir.glob("*.json"))
    
    if not json_files:
        print("⚠ 未找到任何JSON文件！")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件\n")
    
    total_questions = 0
    
    # 处理每个文件
    for file_path in json_files:
        print(f"处理: {file_path.name}")
        count = renumber_indices(file_path)
        print(f"  ✓ 重新编号了 {count} 个问题\n")
        total_questions += count
    
    print("="*70)
    print(f"✓ 完成！总共处理了 {total_questions} 个问题")
    print("="*70)


if __name__ == "__main__":
    main()
