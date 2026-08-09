# Reflective Journal Review

`reflective-journal-review` 是一个开源 Codex Skill，用于基于证据生成单日或连续七个自然日的反思总结。它可以分析用户明确提供的文本、文件，或按需配置的本地 Markdown 日记目录。

这个 Skill 会总结原始记录、识别反复出现的主题和想法变化，并追踪没有完成证据的主意。它不负责写入原始日记，也不创建定时任务。

## 两种模式

- `daily-review`：分析一个指定日期。
- `weekly-review`：分析截止日及此前六天，截止日包含在内。

两种模式都会区分原文事实、作者自己的判断、谨慎的分析观察和可选建议。没有内容的栏目会被省略；没有有效输入时不会创建空总结。

## 安装

克隆仓库，然后把 Skill 目录复制或链接到个人 Codex Skill 目录：

```bash
git clone https://github.com/konsyuukun-maker/reflective-journal-review.git
mkdir -p ~/.codex/skills
cp -R reflective-journal-review/skills/reflective-journal-review ~/.codex/skills/
```

如果只希望在某个代码仓库内使用，可将 Skill 放入该仓库代理配置所使用的 Skill 目录。

## 使用

```text
使用 $reflective-journal-review 总结我在 2026-03-14 的日记。

使用 $reflective-journal-review 分析我提供的文件，生成截止到
2026-03-15 的七日总结。
```

用户明确提供的文本或文件优先于自动目录扫描。如果需要自动读取本地日记，可以复制并修改 [`examples/AGENTS.example.md`](examples/AGENTS.example.md)，填写自己的 `journal_root`。默认输出是对话中的 Markdown；只有用户明确要求或本地规则定义了输出目录时才保存文件。

## 文件命名

- 每日总结：`YYYY-MM-DD-SUM.md`
- 七日总结：`YYYY-MM-DD～MM-DD-7dSUM.md`

保存脚本只允许创建新文件，会拒绝覆盖、符号链接、非法日期、空白来源以及不是七个自然日的日期范围。

## 开发与迭代

```bash
python3 tests/validate_structure.py
bash tests/test_save_review.sh
```

发布前还应使用 OpenAI Skill Creator 的 `quick_validate.py` 验证 `skills/reflective-journal-review`。版本管理和贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

MIT
