#!/usr/bin/env python3
"""READ-ONLY snapshot of key configuration from a live Odoo DB via XML-RPC,
for comparing against the configuration workbook. Never writes to Odoo.

Usage: ODOO_URL=https://x.odoo.com ODOO_DB=db ODOO_USER=me@x.com ODOO_KEY=<api key or password> \
       snapshot.py OUT.xlsx
Each section is skipped (with a note) if the model/field does not exist or access is denied.
"""
import os
import sys
import xmlrpc.client

SECTIONS = [
    ("Companies", "res.company", [], ["name", "vat", "company_registry", "currency_id", "country_id"]),
    ("Taxes", "account.tax", [], ["name", "type_tax_use", "amount_type", "amount", "tax_exigibility", "active", "company_id"]),
    ("Journals", "account.journal", [], ["name", "type", "code", "company_id"]),
    ("Payment Terms", "account.payment.term", [], ["name"]),
    ("Fiscal Positions", "account.fiscal.position", [], ["name", "auto_apply", "company_id"]),
    ("Currencies", "res.currency", [("active", "=", True)], ["name", "rate"]),
    ("Warehouses", "stock.warehouse", [], ["name", "code", "reception_steps", "delivery_steps", "company_id"]),
    ("Picking Types", "stock.picking.type", [], ["name", "code", "warehouse_id", "sequence_code"]),
    ("Product Categories", "product.category", [], ["complete_name", "property_cost_method", "property_valuation"]),
    ("Installed Modules", "ir.module.module", [("state", "=", "installed")], ["name", "latest_version"]),
]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    env = {k: os.environ.get(k) for k in ("ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_KEY")}
    missing = [k for k, v in env.items() if not v]
    if missing:
        sys.exit(f"missing env vars: {missing}")
    url = env["ODOO_URL"].rstrip("/")
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)
    ver = common.version().get("server_version", "?")
    uid = common.authenticate(env["ODOO_DB"], env["ODOO_USER"], env["ODOO_KEY"], {})
    if not uid:
        sys.exit("authentication failed")
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)

    from openpyxl import Workbook
    wb = Workbook()
    info = wb.active
    info.title = "Info"
    info.append(["Server version", ver])
    info.append(["Database", env["ODOO_DB"]])
    for title, model, domain, fields in SECTIONS:
        try:
            avail = models.execute_kw(env["ODOO_DB"], uid, env["ODOO_KEY"], model, "fields_get", [], {"attributes": ["type"]})
            flds = [f for f in fields if f in avail]
            rows = models.execute_kw(env["ODOO_DB"], uid, env["ODOO_KEY"], model, "search_read", [domain], {"fields": flds})
        except Exception as e:  # missing module / access right
            info.append([title, f"skipped: {str(e)[:120]}"])
            continue
        ws = wb.create_sheet(title[:31])
        ws.append(flds)
        for r in rows:
            ws.append([r[f][1] if isinstance(r.get(f), list) and len(r[f]) == 2 else
                       (", ".join(map(str, r[f])) if isinstance(r.get(f), list) else r.get(f)) for f in flds])
        info.append([title, f"{len(rows)} rows"])
    wb.save(sys.argv[1])
    print(sys.argv[1], f"(server {ver})")


if __name__ == "__main__":
    main()
