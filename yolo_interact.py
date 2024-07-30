
import web3.eth
import json
from web3 import Web3

class Games():
    def __init__(self, w3, address, ABI, min_eth, min_yolo) -> None:
        
        with open(ABI, 'r') as f:
            abi_ = f.read()
        self.contract = w3.eth.contract(address=address, abi=abi_)

        self.min_eth = min_eth
        self.min_yolo = min_yolo


class Flipper(Games):
    pass

class Quantum(Games):
    pass

class LaserBlast(Games):
    pass

class YOLO():

    def __init__(self):
        

        w3 = Web3(Web3.HTTPProvider("https://rpc.blast.io"))
        with open("global.json",'r') as f:
            s1 = f.read()
            dct = json.loads(s1)

        self.basic_fee = dct['basic_fee']
        flp_cfg = dct['flipper']
        # self.flipper = Flipper( w3,  flp_cfg['address'], flp_cfg['abi_file'], flp_cfg['minimum_eth'], flp_cfg['minimum_yolo'])
        qtm_cfg = dct['quantum']
        self.quantum = Quantum(  w3, qtm_cfg['address'], qtm_cfg['abi_file'], qtm_cfg['minimum_eth'], qtm_cfg['minimum_yolo'])
        lsb_sfg = dct['laserblast']
        self.laserblast = LaserBlast( w3, lsb_sfg['address'], lsb_sfg['abi_file'], lsb_sfg['minimum_eth'], lsb_sfg['minimum_yolo'])

A = YOLO()