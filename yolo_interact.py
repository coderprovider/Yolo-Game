
import web3.eth
import json
from web3 import Web3

from abc import ABC,abstractmethod

class Basic(ABC):

    def set_w3(self, w3):
        Basic.w3 = w3
    def set_account(self, private_key):
        Basic.account = Basic.w3.eth.account.from_key(private_key)

class YoloToken(Basic):

    def __init__(self, address, ABI):
        YoloToken.address = address
        YoloToken.Base = 10 ** 18
        with open(ABI, 'r') as f:
            abi_ = f.read()
        self.contract = self.w3.eth.contract(address=address, abi=abi_)

    def balanceOf(self, addr=None):
        if addr is None:
            addr = YoloToken.account.address
        return self.contract.functions.balanceOf(addr).call() / YoloToken.Base
    
class Games(Basic):

    basic_fee = 0

    def __init__(self, address, ABI, min_eth, min_yolo) -> None:
        
        with open(ABI, 'r') as f:
            abi_ = f.read()

        self.address = address
        self.contract = Games.w3.eth.contract(address=address, abi=abi_)

        self.min_eth = min_eth
        self.min_yolo = min_yolo

    def send_raw(self, raw_action, extra_value=0): 
        raw_tx = raw_action.build_transaction({
            'value': Games.w3.to_wei(Games.basic_fee, 'ether') +extra_value,
            'nonce': Games.w3.eth.get_transaction_count(Games.account.address),
            'gas': 500000,
            'maxPriorityFeePerGas': Games.w3.to_wei( 0.0008, 'gwei'),
            'maxFeePerGas': Games.w3.to_wei( 0.03, 'gwei'),
            'chainId': 81457,
        } )
        sigend_tx = Games.w3.eth.account.sign_transaction(raw_tx, private_key=self.account.key)
        tx_hash = Games.w3.eth.send_raw_transaction(sigend_tx.rawTransaction)
        receipt = Games.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] == 1:
            print(f'Transaction {tx_hash.hex()} Success.')
        elif receipt['status'] == 0:
            raise RuntimeError( f"Transaction Failed. Please check https://blastscan.io/tx/{tx_hash.hex()} for reasons." )

    def analyze_currency(self, currency_name:str):
        currency_name = currency_name.lower()
        if currency_name == 'yolo':
            currency = Games.w3.to_checksum_address(YoloToken.address)
        elif currency_name == 'eth':
            currency = Games.w3.to_checksum_address('0x0000000000000000000000000000000000000000')
        else:
            raise RuntimeError("Currency name error: Must be 'yolo' or 'eth' ") 
        return currency

    def show_args(self):
        print(f'Extra key arguments for Game {self.__class__.__name__}:')
        for key in self.__class__.extra_keys:
            print(f'    {key} : {getattr(self.__class__, key, None)}')

    def set_args(self,**kwargs):
        for key in self.__class__.extra_keys:
            if key in kwargs:
                print(f'  Set {key} : { getattr(self.__class__, key, None) } -> {kwargs[key]} ')
                setattr(self.__class__, key, kwargs[key])
    
class Flipper(Games):
    extra_keys = ['is_gold' ]
    is_gold = True   # Bool ,True or False

    def play(   self,
                numberOfRounds:int,
                amountPerRound,
                currencyName="yolo",
                stopGain=0,   stopLoss=0,
                isGold=is_gold,   
            ):

        currency = self.analyze_currency(currencyName)
        if currencyName== "yolo" and amountPerRound < self.min_yolo:
            raise RuntimeError( f" Yolo amount too small. Minimum per transaction: {self.min_yolo}" )
        if currencyName== "eth" and amountPerRound < self.min_eth:
            raise RuntimeError( f" Eth amount too small. Minimum per transaction: {self.min_eth}" )

        playAmountPerRound = Games.w3.to_wei(amountPerRound, 'ether')
        raw_ = self.contract.functions.play(numberOfRounds,
                playAmountPerRound,
                currency,
                stopGain,
                stopLoss,
                bool( isGold ),
        )
        extra_wei = 0 if currencyName == 'yolo' else numberOfRounds* playAmountPerRound
        self.send_raw(raw_action=raw_, extra_value=extra_wei)

class Quantum(Games):

    extra_keys = ['is_above', 'multiplier']
    is_above = False   # Bool ,True or False
    multiplier_ = 1.05 # Float between 1.05 to 100, 

    def play(   self,
                numberOfRounds:int,
                amountPerRound,
                currencyName="yolo",
                stopGain=0,   stopLoss=0,
                isAbove=is_above,   multiplier=multiplier_,
            ):

        currency = self.analyze_currency(currencyName)
        if currencyName== "yolo" and numberOfRounds * amountPerRound < self.min_yolo:
            raise RuntimeError( f" Yolo amount too small. Minimum per transaction: {self.min_yolo}" )
        if currencyName== "eth" and numberOfRounds * amountPerRound < self.min_eth:
            raise RuntimeError( f" Eth amount too small. Minimum per transaction: {self.min_eth}" )

        playAmountPerRound = Games.w3.to_wei(amountPerRound, 'ether')
        raw_ = self.contract.functions.play(numberOfRounds,
                playAmountPerRound,
                currency,
                stopGain,
                stopLoss,
                bool( isAbove ),
                int( multiplier * 10000)
        )
        extra_wei = 0 if currencyName == 'yolo' else numberOfRounds* playAmountPerRound
        self.send_raw(raw_action=raw_, extra_value=extra_wei)
    
class LaserBlast(Games):
    
    extra_keys = ['risk_level', 'row_count']
    risk_level = 1 # Int in range [1,2,3]
    row_count = 16 # Int in range [8..16]

    def play(   self,
                numberOfRounds:int,
                amountPerRound,
                currencyName="yolo",
                stopGain=0,   stopLoss=0,
                riskLevel=risk_level,   rowCount=row_count,
            ):

        currency = self.analyze_currency(currencyName)
        if currencyName== "yolo" and numberOfRounds * amountPerRound < self.min_yolo:
            raise RuntimeError( f" Yolo amount too small. Minimum per transaction: {self.min_yolo}" )
        if currencyName== "eth" and numberOfRounds * amountPerRound < self.min_eth:
            raise RuntimeError( f" Eth amount too small. Minimum per transaction: {self.min_eth}" )

        playAmountPerRound = Games.w3.to_wei(amountPerRound, 'ether')
        raw_ = self.contract.functions.play(numberOfRounds,
                playAmountPerRound,
                currency,
                stopGain,
                stopLoss,
                int(riskLevel-1)% 3 + 1,
                rowCount
        )
        extra_wei = 0 if currencyName == 'yolo' else numberOfRounds* playAmountPerRound
        self.send_raw(raw_action=raw_, extra_value=extra_wei)
    
class YOLO(Basic):

    def __init__(self):
                
        with open("global.json",'r') as f:
            s = f.read()
            dct = json.loads(s)
        
        w3 = Web3(Web3.HTTPProvider("https://rpc.blast.io"))
        self.set_w3(w3)

        Games.basic_fee = dct['basic_fee']

        self.yolo_delegator = dct['yolo_delegator']
        tkn_cfg = dct['yolo_token']
        self.yolo_token = YoloToken( tkn_cfg['address'], tkn_cfg['abi_file'] )

        flp_cfg = dct['flipper']
        self.flipper = Flipper(  flp_cfg['address'], flp_cfg['abi_file'], flp_cfg['minimum_eth'], flp_cfg['minimum_yolo'])
        qtm_cfg = dct['quantum']
        self.quantum = Quantum(  qtm_cfg['address'], qtm_cfg['abi_file'], qtm_cfg['minimum_eth'], qtm_cfg['minimum_yolo'])
        lsb_cfg = dct['laserblast']
        self.laserblast = LaserBlast( lsb_cfg['address'], lsb_cfg['abi_file'], lsb_cfg['minimum_eth'], lsb_cfg['minimum_yolo'])

    def show_balance(self, currencies = ['eth', 'yolo']):
        if 'eth' in currencies:
            print(f' Blast_ETH amount: {self.w3.eth.get_balance(self.account.address) / (10**18)}')

        if 'yolo' in currencies:
            print(f' YOLO amount: {self.yolo_token.balanceOf()}')

    def check_yolo_approve(self):
        return self.yolo_token.contract.functions.allowance( Games.account.address ,self.yolo_delegator ).call() / 10 **18

    def approve_yolo(self):
        pass

# A = YOLO()
# A.set_account()
# A.show_balance()
# A.laserblast.account.address
# A.laserblast.play(1, 0.0003, 'eth')
# A.laserblast.show_args()
# print(A.laserblast.contract.all_functions())

