# DEPOSIT ACCOUNT PRODUCT
### deposit_account.py: the smart contract file using for implementing the behavior of the deposit account product
### Product features:
#### Currency:
    - Using parameter: denomination
    - Default currency is VND
#### Interest Accrual:
    - Using parameter: accrue_interest_schedule_hour,minute,second to define schedule time
    - Using parameter: annual_interest_rate to define the annual interest rate
    - The schedule will run daily
    - The accrued interest is truncated to 5 decimal places before being added to the accrual pot
    - The accrued interest address is ACCRUAL_INCOMING
#### Interest Application:
    - Using parameter: apply_interest_schedule_hour,minute,second to define schedule time
    - Using parameter: apply_interest_type to define apply interest type (daily or monthly)
    - The accrued interest is applied to the account balance at 2 decimal places by default
#### Rebalance
    - The post_posting_code will rebalance address AVAILABLE_BALANCE and AUTH based on the instruction type
    - With posting instruction type HARD_SETTLEMENT and TRANSFER: rebalance address AVAILABLE_BALANCE
    - With posting instruction type AUTHORISATION: rebalance address AUTH
    - With posting instruction type SETTLEMENT: rebalance address AVAILABLE_BALANCE and AUTH
    - With posting instruction type RELEASE: rebalance AUTH
    - With posting instruction type AUTHORISATION_ADJUSTMENT: rebalance AUTH


