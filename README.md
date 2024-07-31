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





### Buy me a coffee

 Bitcoin Address: bc1psanc6rn7wt0mwdy2377yrsfkut2ajr26x7v9afcerl9drzmh64asm5rfgn

 Ethereum Address(EVM chain supported): 0xb26871811eea6c21cd3e9e44faa0024a70046554
