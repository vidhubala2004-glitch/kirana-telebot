# Billing Skill

Billing works in two phases.

Phase 1:
Create or modify a draft.

Phase 2:
Finalize the bill.

Rules:

1. Never deduct stock while creating a draft.
2. Always use database prices.
3. Never invent GST rates.
4. Calculate CGST and SGST for intra-state sales.
5. Before finalization, verify current stock again.
6. Never oversell.
7. Never sell below cost.
8. Require a valid payment mode.
9. Payment modes are CASH, UPI and KHATA.
10. Do not claim a bill is finalized until the tool confirms it.
11. Generate a PDF invoice after successful finalization.
