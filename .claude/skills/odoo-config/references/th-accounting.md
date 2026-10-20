# Thai accounting configuration decisions

| Topic | Decide | Typical choice / note |
|---|---|---|
| Localization | Install Thailand fiscal localization before posting anything | Thai CoA + VAT taxes from `l10n_th`; check which taxes/accounts it creates in your version |
| VAT 7% | Sales & purchase taxes, included/excluded in price | Excluded for B2B; POS often included |
| VAT 0% / exempt | Export (0%) vs exempt goods/services | Separate taxes + fiscal positions |
| Undue VAT (services) | Cash-basis taxes | VAT recognized on payment; needs transition (undue) accounts |
| Withholding tax | Standard negative taxes on bill / at payment, OCA `l10n_thailand` modules, or custom | Decide output: 50 Tawi certificate, PND 3 / PND 53 lists; WHT at payment is the legal point |
| Tax invoice | Full tax invoice fields: seller/buyer name, address, Tax ID, branch, "ต้นฉบับ/สำเนา" | Usually a custom QWeb report; abbreviated tax invoice for POS |
| Branch | Company branch code and customer branch | No standard field in many setups → custom field [CONFIG] |
| Numbering | Per document type, monthly/yearly reset | Odoo default `INV/2026/00001`; Thai formats like `IV2610-0001` may need sequence customization (verify per version) |
| Receipt / billing note | Separate documents after payment / for collection | Often custom reports/modules |
| Currency rates | Bank of Thailand or manual | Manual monthly for small companies |
| Fiscal year / lock dates | Year end, period lock policy | Lock after monthly close |
| Assets | Depreciation method, start (in-use date) | Straight-line common; EE Assets or OCA |

Record each decision in the workbook "Accounting" sheet and the Taxes/Journals/Sequences sheets; validate with the accountant/auditor before go-live.
