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
#### Localize and Delocalize:
    - Using helper func localize_timestamp and delocalize_timestamp to converse from UTC to +7:00 or from +7:00 to UTC
#### Pre-posting-code:
    - Check denomination (equal to parameter denomination)
    - Check transaction amount (in range of Available Balance)
#### ASSUM that: 
    - Posting instruction will effect to balance of these address: AVAILABLE BALANCE (Phase.COMMITTED & Phase.PENDING_OUT), Earmarked (Phase.PENDING_OUT) and Hold (Phase.PENDING_IN)
    - The post_posting_code will rebalance address based on the instruction type
    - With posting instruction type HARD_SETTLEMENT and TRANSFER: effect to Phase.COMMITTED so we need rebalance address 
    AVAILABLE BALANCE 
    - With posting instruction type AUTHORISATION: effect to Phase.PENDING_OUT and Phase.PENDING_IN so we need rebalance address AVAILABLE BALANCE & EARMARKED (Phase.PENDING_OUT) and HOLD (Phase.PENDING_IN)
    - With posting instruction type SETTLEMENT: effect to Phase.PENDING_OUT / Phase.PENDING_IN and Phase.COMMITTED so we need rebalance address EARMARKED (Phase.PENDING_OUT) / HOLD (Phase.PENDING_IN) and AVAILABLE BALANCE (Phase.COMMITTED)
    - With posting instruction type RELEASE: effect to Phase.PENDING_OUT / Phase.PENDING_IN so we need rebalance address AVAILABLE BALANCE & EARMARKED (Phase.PENDING_OUT) and HOLD (Phase.PENDING_IN)
    - With posting instruction type AUTHORISATION_ADJUSTMENT: we need to provide the phase of the posting we want to AUTHORISATION_ADJUSTMENT in instruction_details (for ex: "instruction_details": {"phase": "POSTING_PHASE_PENDING_OUTGOING"}). the posting instruction will effect to Phase.PENDING_OUT / Phase.PENDING_IN so we need rebalance address AVAILABLE BALANCE & EARMARKED (Phase.PENDING_OUT) and HOLD (Phase.PENDING_IN)


