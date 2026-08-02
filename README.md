# China Printed Will Package

This repository is a private archive of a legacy Codex skill for preparing printed-will document packages under Mainland Chinese law.

## Overview

The skill helps a lawyer turn client-provided family, property, and testamentary information into a structured, editable package for a printed will. It is designed for non-contentious legal work and assumes that the lawyer provides consultation and drafting support rather than acting as a will witness by default.

## Included materials

The package can route and prepare the following materials:

1. An operation guide for the signing process;
2. A personal printed will or separate wills for a married couple;
3. A lawyer work record that does not falsely describe witnessing;
4. A signing-site record;
5. A property schedule;
6. A family-member information survey;
7. A risk notice;
8. Witness declarations;
9. A signing-video script; and
10. An evidence index and, where needed, a pending-information list.

## Safeguards

- Missing information must remain an explicit placeholder rather than an invented identity number, property number, account number, amount, date, or event.
- The will-maker's capacity, property rights, beneficiary arrangements, witness qualifications, and signing formalities must be checked before signing.
- A lawyer's drafting or consultation record must not be rewritten as a witnessing record unless the lawyer actually acted as a qualified witness.
- Video recording supports proof of the process; it does not replace the statutory signature, witnessing, or date requirements.
- A couple's materials are treated as two separate wills unless the client expressly requests another legally supportable structure.
- Current statutes, judicial interpretations, local registration requirements, and special-asset rules must be verified before professional use.

## Repository layout

```text
china-printed-will-package/
├── SKILL.md
├── agents/openai.yaml
├── assets/templates/
├── references/
└── maintenance/
```

The reusable templates are kept under `assets/templates/`. Intake mapping, legal rules, and output requirements are kept under `references/`.

## Status

This is a legacy archive. It is preserved for reference and version history and is not part of the current active Codex skill set.

## Use and responsibility

This repository is a professional drafting aid, not a substitute for legal advice, current-law verification, client instructions, or the lawyer's review of the actual signing process. The repository does not include an open-source license and is intended for private professional use.
