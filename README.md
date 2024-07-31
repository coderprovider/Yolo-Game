# YOLO_Games-EasyUse

 A tool to help interact with yolo games on Blast Blockchain
 Base on Python web.py

## Usage

 For example, this program gives wrapped API to interact with YOLO Games automatically

```python

from yolo_interact import YOLO
A = YOLO()
A.set_account( YOUR_PRIVATEKEY )
# Another method:
# w3 = Web3(Web3.HTTPProvider("https://rpc.blast.io"))
# A.account = w3.eth.account.from_key(YOUR_PRIVATEKEY)
A.show_balance()
A.account.address
A.laserblast.show_args()
A.laserblast.play(1, 0.0003, 'eth')
A.laserblast.set_args(row_count = 9)
A.laserblast.play(1, 200, 'yolo')

```
or use command line:
```
python main.py -p PRIVATEKEY -gn flipper -ap 0.001 -ac eth
```

## Main.py Arguments

    --private-key,      '-p',  help="Input your Private Key to import the wallet."
    --game-name,        '-gn', help="Input Game Name to start a game. Keep letter lowercase. flipper/laserblast/quantum"
    --num-rounds,              help="Input number of rounds. Numbers over 10 will be split."
    --amount-perround, '-ap',  help="Input amount per round. Default unit of currency is yolo."
    --amount_currency, '-ac',  help="Name of currency. Must be eth or yolo"

    Extra Arguments for games:
    --is_gold,                 help="Flipper Extra Keyword: is_gold : 0/1 -> False/True"
    --is_above,                help="Quantum Extra Keyword: is_gold : 0/1 -> False/True"
    --multiplier, float,       help="Quantum Extra Keyword: multiplier : from 1.05 to 100"
    --risk_level, int,         help="LaserBlast Extra Keyword: risk_level : int [1,2,3]"
    --row_count, int,          help="LaserBlast Extra Keyword: row_count : int [8..16]"


### Buy me a coffee

 Bitcoin Address: bc1psanc6rn7wt0mwdy2377yrsfkut2ajr26x7v9afcerl9drzmh64asm5rfgn

 Ethereum Address(EVM chain supported): 0xb26871811eea6c21cd3e9e44faa0024a70046554
