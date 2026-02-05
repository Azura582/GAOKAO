# 教师AI评分系统使用说明

## 功能概述

这个程序会遍历 `Results/deepseek` 下的所有 JSON 文件，使用教师AI对模型输出进行评分。

### 评分依据
- **question**: 题目内容
- **answer**: 标准答案
- **analysis**: 题目解析
- **score**: 满分分值
- **model_output**: AI模型的输出

### 评分输出
每个问题会新增两个字段：
- **teacher_analysis**: 详细的评分分析
- **teacher_score**: 最终得分（0到满分之间的数值）

---

## 快速开始

### 1. 基本用法

```bash
cd /home/azura/code/python/GAOKAO-Bench-main\ \(Copy\)

python3 AIRun/teacher_grading.py \
    --api-url "https://api.openai.com/v1/chat/completions" \
    --api-key "your-api-key-here" \
    --model "gpt-4"
```

### 2. 只评分特定策略

```bash
python3 AIRun/teacher_grading.py \
    --api-url "YOUR_API_URL" \
    --api-key "YOUR_API_KEY" \
    --strategy "Strategy_0_CoT"
```

### 3. 不备份原文件（谨慎使用）

```bash
python3 AIRun/teacher_grading.py \
    --api-url "YOUR_API_URL" \
    --api-key "YOUR_API_KEY" \
    --no-backup
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--api-url` | 教师AI的API地址 | `https://api.openai.com/v1/chat/completions` |
| `--api-key` | API密钥 | `your-api-key-here` |
| `--model` | 使用的模型名称 | `gpt-4` |
| `--results-dir` | 结果目录路径 | `../Results/deepseek` |
| `--no-backup` | 不备份原文件 | False（默认会备份） |
| `--strategy` | 只处理特定策略 | None（处理所有策略） |

---

## 输出示例

### 原始数据结构
```json
{
    "index": 0,
    "year": "2023",
    "question": "题目内容...",
    "answer": "标准答案",
    "analysis": "题目解析...",
    "score": 10,
    "model_output": "AI模型的回答..."
}
```

### 评分后的数据结构
```json
{
    "index": 0,
    "year": "2023",
    "question": "题目内容...",
    "answer": "标准答案",
    "analysis": "题目解析...",
    "score": 10,
    "model_output": "AI模型的回答...",
    "teacher_analysis": "该答案基本正确，涵盖了主要知识点...",
    "teacher_score": 8.5,
    "grading_timestamp": "2024-01-15 10:30:00"
}
```

---

## 特性说明

### 1. 断点续评
- 程序会自动跳过已评分的题目
- 中断后重新运行会从未评分的题目继续
- 每评分5道题自动保存一次，防止数据丢失

### 2. 自动备份
- 首次处理文件时会自动创建 `.json.backup` 备份文件
- 备份只创建一次，不会覆盖已有备份
- 使用 `--no-backup` 可关闭备份功能

### 3. 智能解析
- 自动解析教师AI返回的JSON格式
- 支持markdown代码块中的JSON
- 解析失败时会给出0分并记录原始返回

### 4. 错误处理
- API调用失败会自动重试（最多3次）
- 单个文件处理失败不影响其他文件
- 详细的错误日志便于排查问题

---

## 运行示例

### 示例1：评分所有策略
```bash
python3 AIRun/teacher_grading.py \
    --api-url "https://api.modelarts-maas.com/v2/chat/completions" \
    --api-key "sk-xxxxxxxxxxxx" \
    --model "deepseek-v3"
```

输出：
```
======================================================================
教师AI评分系统 - 初始化完成
======================================================================
模型: deepseek-v3
结果目录: ../Results/deepseek
备份原文件: True
======================================================================

找到 10 个策略文件夹

======================================================================
策略: Strategy_0_CoT
======================================================================

处理文件: Commonsense&WorldKnowledge.json
  总题目数: 50, 已评分: 0, 待评分: 50
  评分进度: 100%|████████████████████| 50/50 [02:30<00:00, 0.33it/s]
  ✓ 完成评分: 50 道题

...

======================================================================
评分完成！
======================================================================
处理文件数: 80
总题目数: 4000
已评分数: 4000
评分率: 100.0%
======================================================================
```

### 示例2：只评分特定策略
```bash
python3 AIRun/teacher_grading.py \
    --api-key "sk-xxxxxxxxxxxx" \
    --strategy "Strategy_0_CoT"
```

### 示例3：从中断处恢复
如果程序中断，直接重新运行相同命令即可：
```bash
python3 AIRun/teacher_grading.py --api-key "sk-xxxxxxxxxxxx"
```
程序会自动跳过已评分的题目。

---

## 估算时间和成本

### 时间估算
假设：
- 8个分类文件 × 10个策略 = 80个文件
- 每个文件平均50道题
- 每次评分耗时约3秒（包括API调用和处理）

**总时间**: 80 × 50 × 3秒 = 12000秒 ≈ **3.3小时**

### 成本估算（GPT-4）
- 每次评分约1500 tokens（输入） + 300 tokens（输出）
- 总计：4000题 × 1800 tokens = 7,200,000 tokens
- **预计成本**: $100-200（取决于具体定价）

建议使用更便宜的模型如 `gpt-3.5-turbo` 或 `deepseek-v3` 来降低成本。

---

## 常见问题

### 1. API调用失败
**原因**: API密钥错误、网络问题、API配额用完
**解决**: 
- 检查API密钥是否正确
- 检查网络连接
- 查看API配额

### 2. 评分不合理
**原因**: 提示词不够详细、模型理解偏差
**解决**: 
- 修改 `_build_grading_prompt()` 中的提示词模板
- 调整温度参数（temperature）
- 使用更强大的模型

### 3. 程序运行缓慢
**解决**: 
- 使用更快的API
- 减少 `time.sleep()` 的延迟
- 只处理特定策略（使用 `--strategy`）

### 4. 内存不足
**解决**: 
- 程序会每5题保存一次，内存占用较小
- 如果仍有问题，可以分批处理不同策略

---

## 进阶配置

### 修改评分提示词
编辑 `teacher_grading.py` 中的 `_build_grading_prompt()` 方法。

### 修改评分标准
可以在提示词中添加更详细的评分规则：
- 完全正确：满分
- 部分正确：70%-90%
- 思路正确但结果错误：40%-60%
- 完全错误：0分

### 批量处理
如果需要处理多个不同的results目录，可以写一个shell脚本循环调用。

---

## 注意事项

1. **API密钥安全**: 不要将API密钥提交到代码仓库
2. **备份重要**: 首次运行建议保留备份功能
3. **成本控制**: 大规模评分前先测试少量数据
4. **评分一致性**: 同一批数据建议使用相同的模型和提示词
5. **结果验证**: 评分完成后建议抽查部分结果验证合理性

---

## 技术支持

如有问题或需要定制功能，请联系开发者。
