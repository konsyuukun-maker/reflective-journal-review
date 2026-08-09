# Reflective Journal Review

`reflective-journal-review` 是一个基于开放 [Agent Skills 规范](https://agentskills.io/specification)的跨 Agent Skill，用于从日记记录生成有证据边界的单日或连续七日反思。它可以分析用户明确提供的文本、文件，或按需配置的本地 Markdown 日记目录。

这个 Skill 会总结原始记录、识别反复出现的主题和想法变化，并追踪没有完成证据的主意。它不负责写入原始日记，也不创建定时任务；同一份 Skill 可以安装到 Codex、Claude Code、Cursor、Gemini CLI、GitHub Copilot 和 OpenCode。

## 两种模式

- `daily-review`：分析一个指定日期。
- `weekly-review`：分析截止日及此前六天，截止日包含在内。

两种模式都会区分原文事实、作者自己的判断、谨慎的分析观察和可选建议。没有内容的栏目会被省略；没有有效输入时不会创建空总结。

## 安装

使用开放的 [Skills CLI](https://github.com/vercel-labs/skills) 自动检测本机 Agent 并选择安装目标：

```bash
npx skills add konsyuukun-maker/reflective-journal-review --skill reflective-journal-review
```

一次安装到六个经过 CI 验证的目标：

```bash
npx skills add konsyuukun-maker/reflective-journal-review --skill reflective-journal-review -a codex -a claude-code -a cursor -a gemini-cli -a github-copilot -a opencode
```

加上 `--global` 可以安装到所选 Agent 的个人全局目录。手动安装时，只需把 `skills/reflective-journal-review` 复制到目标 Agent 支持的 Skills 目录，无需为不同 Agent 复制或维护不同版本。

## 兼容范围

| Agent | Skills CLI ID | 验证范围 |
| --- | --- | --- |
| Codex | `codex` | 发现、安装、资源完整性和安全保存 |
| Claude Code | `claude-code` | 发现、安装、资源完整性和安全保存 |
| Cursor | `cursor` | 发现、安装、资源完整性和安全保存 |
| Gemini CLI | `gemini-cli` | 发现、安装、资源完整性和安全保存 |
| GitHub Copilot | `github-copilot` | 发现、安装、资源完整性和安全保存 |
| OpenCode | `opencode` | 发现、安装、资源完整性和安全保存 |

这里的“经过验证”指开放 Skill 包和确定性保存脚本通过 CI，并不表示已经调用或评测六家厂商的付费模型服务。Skills CLI 支持的其他 Agent 也可以尝试安装同一份标准 Skill，但仓库暂不把它们标记为 CI 已验证。

## 使用

```text
使用 reflective-journal-review Skill 总结我在 2026-03-14 的日记。

使用 reflective-journal-review Skill 分析我提供的文件，生成截止到
2026-03-15 的七日总结。
```

Codex 中仍然可以使用 `$reflective-journal-review` 显式调用；其他 Agent 可以直接用自然语言指定 Skill 名称。

用户明确提供的文本或文件优先于自动目录扫描。如果需要自动读取本地日记，可以复制并修改 [`examples/AGENTS.example.md`](examples/AGENTS.example.md)，填写自己的 `journal_root`。默认输出是对话中的 Markdown；只有用户明确要求或本地规则定义了输出目录时才保存文件。

## 文件命名

- 每日总结：`YYYY-MM-DD-SUM.md`
- 七日总结：`YYYY-MM-DD～MM-DD-7dSUM.md`

保存需要 Python 3.11 或更高版本。跨平台脚本只允许创建新文件，会拒绝覆盖、符号链接、非法日期、空文件以及不是七个自然日的日期范围：

```bash
# macOS 或 Linux
python3 skills/reflective-journal-review/scripts/save_review.py daily OUTPUT_DIR YYYY-MM-DD SOURCE_FILE

# Windows
py -3 skills/reflective-journal-review/scripts/save_review.py daily OUTPUT_DIR YYYY-MM-DD SOURCE_FILE
```

原有 `bash .../save_review.sh` 命令继续兼容，并转交给同一个 Python 实现。如果环境没有兼容的 Python，不得绕过防覆盖保护；只在对话中返回总结，并说明未保存文件。

## 开发与迭代

```bash
python3 tests/validate_structure.py
python3 tests/test_save_review.py
bash tests/test_save_review.sh
```

发布前还应使用 Agent Skills 参考验证器和 OpenAI Skill Creator 的 `quick_validate.py` 验证 `skills/reflective-journal-review`。版本管理和贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

MIT
