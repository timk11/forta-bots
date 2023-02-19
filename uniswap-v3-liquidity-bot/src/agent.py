from forta_agent import Finding, FindingType, FindingSeverity, get_transaction_receipt
from web3 import Web3

UniV3_CONTRACT_EVENT = '{"name":"Transfer","type":"event","anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":true,"name":"tokenId","type":"uint256"}]}'

CONTRACT_ADDRESS = '0xC36442b4a4522E871399CD717aBDD847Ab11FE88' # Uniswap V3 liquidity contract address

transfer_event_sig = Web3.keccak(text="Transfer(address,address,uint256)").hex() # Transfer
collect_event_sig = Web3.keccak(text="Collect(uint256,address,uint256,uint256)").hex() # Collect
burn_event_sig = Web3.keccak(text="Burn(address,int24,int24,uint128,uint256,uint256)").hex() # Burn
inc_liq_event_sig = Web3.keccak(text="IncreaseLiquidity(uint256,uint128,uint256,uint256)").hex() # IncreaseLiquidity
dec_liq_event_sig = Web3.keccak(text="DecreaseLiquidity(uint256,uint128,uint256,uint256)").hex() # DecreaseLiquidity
approval_event_sig = Web3.keccak(text="Approval(address,address,uint256)").hex() # Approval
approval_for_all_event_sig = Web3.keccak(text="ApprovalForAll(address,address,bool)").hex() # ApprovalForAll

event_dict = {transfer_event_sig: "Transfer (or Mint)", collect_event_sig: "Collect", burn_event_sig: "Burn",
              inc_liq_event_sig: "Increase Liquidity", dec_liq_event_sig: "Decrease Liquidity",
              approval_event_sig: "Approval", approval_for_all_event_sig: "Approval For All"}

def handle_transaction(transaction_event):
    findings = []

    # filter the transaction logs for any Uniswap V3 liquidity transactions
    uniV3_contract_events = transaction_event.filter_log(
        UniV3_CONTRACT_EVENT, CONTRACT_ADDRESS)

    for contract_event in uniV3_contract_events:
        # extract contract event arguments
        to = contract_event['args']['to']
        from_ = contract_event['args']['from']
        token_id = contract_event['args']['tokenId']
        tx_hash = contract_event['transactionHash']
        receipt = get_transaction_receipt(tx_hash)
        topic = receipt.logs[0].__dict__['topics'][0]
        if topic in event_dict.keys():
            event_type = event_dict[topic]
        else:
            event_type = "Other"

        # report transaction
        findings.append(Finding({
            'name': 'Uniswap V3 Liquidity Transaction',
            'description': 'Uniswap V3 liquidity transaction',
            'alert_id': 'FORTA-1',
            'severity': FindingSeverity.Low,
            'type': FindingType.Info,
            'metadata': {
                'to': to,
                'from': from_,
                'event_type': event_type,
                'token_ID': token_id
            }
        }))

    return findings