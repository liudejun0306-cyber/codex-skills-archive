# 组卷计划格式

`build_evidence_bundle.py` 接受 UTF-8 JSON。路径相对于计划文件所在目录解析，也可使用绝对路径。

```json
{
  "case_name": "广利公司诉明勇成买卖合同纠纷",
  "bundle_name": "证据册.pdf",
  "exhibits": [
    {
      "number": 1,
      "name": "原告营业执照及法定代表人身份证明",
      "date": "2026-01-01",
      "purpose": "证明原告主体资格。",
      "sources": [
        {"path": "材料/营业执照.pdf", "pages": "1-2"},
        {"path": "材料/法定代表人身份证明.pdf"}
      ]
    },
    {
      "number": 2,
      "name": "采购合同及订单",
      "date": "2025-03-01",
      "purpose": "证明双方达成买卖合意及主要权利义务。",
      "sources": [
        {"path": "材料/采购合同.pdf"},
        {"path": "材料/订单1.jpg"}
      ]
    }
  ]
}
```

## 字段规则

- `number`：正整数且不得重复；输出按编号排序。
- `name`：用于文件名，脚本会替换文件系统不允许的字符。
- `sources`：至少一项。支持 PDF、PNG、JPG/JPEG、TIFF、BMP、DOCX、DOC、XLSX、XLS、PPTX、PPT、ODT、ODS、ODP。
- `pages`：可选，仅适用于转换后的 PDF；使用 1-based 页码，如 `1-3,5,8-10`。
- `purpose`、`date`：保留在计划中供 AI 生成目录和核验，脚本不据此推断事实。
- 可以增加 `element`、`claim`、`sort_reason`、`notes`、`exclude` 等内部字段；脚本忽略未知字段。

若 `exclude` 为 `true`，脚本跳过该项。任何源文件不存在、页码越界、格式不支持或转换失败，脚本立即报错，不生成“看似成功”的残缺证据册。
