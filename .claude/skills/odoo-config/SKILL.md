---
name: odoo-config
description: Odoo functional configuration for implementation projects, any version (16, 17, 18, 19, 20+) — generates a Configuration Workbook (settings decisions per module, taxes, journals, sequences, warehouses, approval matrix, roles, sign-off) as Excel, guides configuration decisions with Thai accounting specifics (VAT 7%, cash-basis VAT, withholding tax, document numbering, tax invoice), and takes a read-only snapshot of a live database to verify configuration against the workbook. Use when the user asks for config workbook, setup checklist, configuration design, ตั้งค่าระบบ, system setup, or to verify/compare a database's configuration.
---

# Odoo Config (version-aware, token-efficient)

## Token rules
1. Workbooks come from `scripts/make_workbook.py`; never type the settings list in chat.
2. Live checks come from `scripts/snapshot.py` (read-only) or an Odoo MCP tool if connected; compare the two Excel files and report only differences.
3. Load `references/th-accounting.md` only for accounting/tax/numbering decisions.
4. Answers = decisions/differences tables, no Odoo feature explanations unless asked.

## Workflow
1. **Generate** — `python3 $S/make_workbook.py out/Config_Workbook_v18.xlsx --version 18 --modules general,accounting,sales,purchase,inventory[,mrp,pos,crm] --project "<name>"`
2. **Workshop** — fill "Customer decision", "Owner", Status per row; fill master sheets (Taxes, Journals, Sequences, Warehouses, Approval Matrix, Roles). When asked, propose a recommendation per row with a one-line reason.
3. **Configure** — status Decided → Configured. Items needing development go to odoo-dev / odoo-pm (Change Request), not hacked via settings.
4. **Verify** — `ODOO_URL=… ODOO_DB=… ODOO_USER=… ODOO_KEY=… python3 $S/snapshot.py out/Snapshot.xlsx`, compare with the workbook, mark Verified or list gaps.
5. **Sign-off** — sheet "Sign-off" before UAT.

`S=.claude/skills/odoo-config/scripts` (or `~/.claude/skills/odoo-config/scripts`). Needs `openpyxl`.

## Rules
- Setting names follow Odoo 18 UI; for other versions tag unconfirmed names `(verify)` and update `scripts/items.py` once confirmed.
- Never write to a live database from this skill; `snapshot.py` uses `search_read`/`fields_get` only. Prefer an API key over a password; never print credentials.
- Configure in a test database first; production only after sign-off.
- Add project-specific rows to `items.py` (one tuple per setting) instead of editing generated files by hand.
