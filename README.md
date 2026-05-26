# XD API CMCC Model Progress

This repository publishes the China Mobile MaaS and XD API model progress report.

Current live status as of 2026-05-18 11:11 CST: the XD API frontend catalog exposes 27 CMCC token-priced models, and public business groups are `1x`, `3x`, and `5x`.

- GitHub Pages entry: `index.html`
- Beginner tutorial page: `docs/cli-ide-setup-tutorial.html`
- Beginner tutorial Markdown: `docs/cli-ide-setup-tutorial.md`
- Business framework: `docs/business-framework.html`
- Group permissions: `docs/group-permissions.html`
- New model test workflow: `docs/model-test-workflow.html`
- Work log: `docs/work-log.html`
- Latency diagnosis: `docs/latency-diagnosis.html`
- Source HTML report: `docs/中国移动 MaaS 与 XD API 模型横向对比进度表.html`
- Markdown report: `docs/中国移动 MaaS 与 XD API 模型横向对比进度表.md`
- Test evidence: `evidence/xdw_model_test_results_20260512.json`
- Latency evidence: `evidence/xdw_latency_diagnosis_20260516_153406.json`
- Group permissions evidence: `evidence/xdw_group_permissions_20260518_1051.json`
- Ratio group evidence: `evidence/xdw_ratio_groups_20260518_1111.json`

Update flow:

1. Regenerate the HTML, Markdown, and evidence JSON locally.
2. Replace the files above.
3. Copy the HTML report to `index.html`.
4. Commit and push to `main`.
