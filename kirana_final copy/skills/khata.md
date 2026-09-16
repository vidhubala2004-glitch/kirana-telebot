# Khata Skill

Khata is a prepaid customer wallet.

Rules:

1. Deposits (credit) increase a customer's wallet balance.
2. A customer is created automatically when a deposit is made.
3. Purchases paid via the KHATA payment mode consume wallet balance.
4. A KHATA purchase must fail if the wallet balance is insufficient.
5. Money a customer pays in (recorded as a payment) increases their wallet balance.
6. Always calculate the balance from stored transaction records.
7. Never invent customer balances.