---
name: legal-practice
description: 中国大陆民商事诉讼与执行实务主技能，用于案件材料分类审阅、证据评价、金额计算、诉讼请求和抗辩方案确定、知识库检索与说理、起诉状、答辩状、代理词、上诉状、质证意见、法律意见、申请书、证据目录和证据册的起草、修改与重构。法律关系明确时不重复作抽象定性分析；正式文书形成前必须完成证据和金额审查及诉讼方案确定。修改既有文书时以用户最新版本为唯一底稿，局部修改优先，修改后必须通读全文消除重复、矛盾和衔接问题。完整中文文本自动适用 chinese-writing-style，正式文件自动适用 chinese-document-output-style；凡通过读取案件文件夹或成组案件材料完成分析、计算或文书时必须联动 obsidian-case-workspace-sync；后续单独形成材料时，属于已同步案件的继续增量登记。
---

# 民商事法律实务

## 一、核心定位

本技能处理具体民商事案件和执行事项。核心关系是：

`证据和金额审查决定事实基础 → 诉讼方案决定请求与抗辩 → 知识库增强法律说理 → 文书只是最终表达载体`

合同文本本身的起草和审查使用 `china-contract-practice`；刑事辩护使用 `criminal-defense-practice`；法律专题研究使用 `obsidian-legal-kb-sync`；具体案件材料和进展持续同步使用 `obsidian-case-workspace-sync`。

## 二、固定办案顺序

1. 确认程序阶段、代理立场、用户目标、交付成果和材料范围；
2. 区分法院材料、对方材料、委托人材料、我方证据、工作材料和参考资料；
3. 法律关系明确时只作简要确认；不明确、存在竞合或咨询方案任务时才深入识别；
4. 根据诉请、抗辩或可能请求权拆解要件事实；
5. 按要件审阅证据，区分已证明、初步支持、仅有陈述、证据冲突、需要补证和无法确认；
6. 对每份关键材料评价证明事项、来源、真实性风险、与其他证据的印证关系、替代解释和缺少的连接证据；
7. 涉及款项、赔偿或待遇时形成独立金额底稿，核对每项金额的事实、证据、规则和公式；
8. 根据证据和计算结果确定最终诉请、主备位关系、否认、反证、真正抗辩、时效抗辩和金额抗辩；
9. 围绕具体争点按需检索本地知识库，将规则转化为本案说理；
10. 起草文书并自动适用中文表达规则；
11. 通读全文，复核事实、证据、金额、逻辑、重复、矛盾、指代、标题和结论；
12. 需要正式文件时按格式技能生成或修改 Word、PDF；
13. 凡通过读取案件文件夹或成组案件材料完成分析、计算或文书时，同步案件工作台；后续单独形成材料时，先匹配既有工作台，属于已同步案件的继续增量登记。

## 三、文书起草前置门槛

正式起诉状、答辩状、代理词、上诉状、法律意见和证据目录形成前，原则上应确认：

- 代理立场和诉讼目标明确；
- 每项主要诉请或抗辩已经识别；
- 关键要件事实及证明责任已经拆解；
- 关键材料已经实际读取，不只依据文件名或当事人概述；
- 主体、签章、经办人、付款收款路径、履行和时效已经核对；
- 金额已经独立计算或说明暂无法计算的原因；
- 主要不利证据、证据冲突和补证缺口已经识别；
- 文书中的核心事实能够定位到具体材料。

材料不足但用户要求先形成初稿时，使用“根据现有材料”“暂按”等限定表述，并列明关键待核事项，不把未核实事实写成确定事实。

## 四、修改和重构硬规则

1. 用户最新文件或最新文本是唯一底稿；不得恢复旧稿或模型此前版本。
2. 默认区分语言润色、具体错误纠正、局部重构和整体重构；哪里有问题先修哪里。
3. 修改事实、金额、请求、证据编号或法律观点时，必须检查其对全文其他位置的影响并同步修改。
4. 修改后必须重新通读全文，检查重复、啰嗦、前后矛盾、逻辑断裂、称谓不一致、金额日期冲突、证据错位和交叉引用失效。
5. 全文复核只处理必要的关联问题，不借机改写已确认且与本次修改无关的内容。
6. 只有用户明确要求重写、重构，或者原方案的法律关系、核心事实、请求权、证据评价、金额或结构无法局部修复时，才整体重构。
7. 整体重构先冻结已确认事实、金额、证据、用户观点和原格式，再回退到产生错误的分析阶段重新处理。

具体见 [modules/document-revision-and-reconstruction.md](modules/document-revision-and-reconstruction.md)。

## 五、知识库说理规则

- 简单程序文书、事实明确且规则稳定的文书不机械检索；
- 需要实体说理、回应对方观点、处理证明责任、法律适用、责任范围或裁判分歧时，先查 Obsidian 已有专题和来源索引；
- 专题不足时再检索完整本地知识库；正式引用前核验法条、案例、效力和适用时间；
- 检索围绕具体争点，不只搜索案由；
- 同时识别有利观点、不利观点、适用条件和例外；
- 知识库内容必须改写为“规则—本案事实—具体证据或证据缺口—结论”，不得整段堆入文书。

具体见 [modules/knowledge-integration.md](modules/knowledge-integration.md)。

## 六、通用技能自动联动

1. 起草、修改或输出完整中文法律文本，自动适用 `$chinese-writing-style`；
2. 用户要求输出、生成、整理成、形成或制作正式文书，或者明确要求 Word、DOCX、PDF，自动适用 `$chinese-document-output-style`；
3. 修改已有文件时，保留用户最新文件的原格式，优先原位编辑；
4. 凡通过读取案件文件夹或成组案件材料完成分析、计算或文书时，必须调用 `$obsidian-case-workspace-sync`。后续单独形成撤诉申请等材料时，先判断是否属于已建立工作台的案件：属于则只做时间增量登记，不属于且本次未读取案件材料的，不另行建档。单纯标点或轻微润色不重新分析案件。

## 七、模块路由

| 任务 | 读取文件 |
|---|---|
| 材料分类、事实状态、证据价值和连接证据 | [modules/material-and-evidence-review.md](modules/material-and-evidence-review.md) |
| 法律关系不明确、请求权竞合或咨询方案 | [modules/legal-relationship-identification.md](modules/legal-relationship-identification.md) |
| 金额、利息、违约金、工资、工伤、人损、工程款 | [modules/amount-calculation-review.md](modules/amount-calculation-review.md) |
| 原告诉请、主备位请求、被告抗辩层级和排序 | [modules/litigation-position-and-strategy.md](modules/litigation-position-and-strategy.md) |
| 本地知识库检索和观点融入文书 | [modules/knowledge-integration.md](modules/knowledge-integration.md) |
| 根据分析结果形成诉讼文书 | [modules/document-drafting.md](modules/document-drafting.md) |
| 润色、纠错、局部重构和整体重构 | [modules/document-revision-and-reconstruction.md](modules/document-revision-and-reconstruction.md) |
| 证据目录、证据 PDF、连续页码和证据册 | [modules/evidence-production.md](modules/evidence-production.md) |
| 民商事诉讼和仲裁工作流 | [workflows/civil-litigation.md](workflows/civil-litigation.md) |
| 法律意见、咨询和客户汇报 | [workflows/legal-opinion.md](workflows/legal-opinion.md) |
| 执行及少量行政程序事项 | [workflows/administrative-and-enforcement.md](workflows/administrative-and-enforcement.md) |

常见案件只加载一个主要案由包；存在基础关系争议、竞合或主备位请求时，最多再加载一个相邻案由包。见 `case-types/`。

## 八、交付检查

- 核心事实均有材料依据或已标明待核；
- 证据和金额审查结果与诉讼方案一致；
- 每项请求或抗辩均有事实、证据和法律支撑；
- 知识库观点已经转化为本案论证，没有资料堆砌；
- 标题准确概括论点，不使用随意创造或不符合习惯的词语；
- 全文没有重复、矛盾、逻辑断裂、悬空指代和编号错误；
- 主体、案号、日期、金额、证据编号、诉请和结论一致；
- 正式文件可编辑、可打开、可打印，并保留原格式或符合默认格式。
