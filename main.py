
import os, sys
import time
import argparse

from yolo_interact import YOLO,Games

def main():
    parser = argparse.ArgumentParser(description="main.py for the YOLO project.")

    parser.add_argument("--private-key",'-p', default='', type=str, dest='pri_key', help="Input your Private Key to import the wallet.")
    parser.add_argument("--game-name",'-gn', default='laserblast', type=str, dest='game', help="Input Game Name to start a game. Keep letter lowercase. flipper/laserblast/quantum")
    parser.add_argument("--num-rounds", default= 1, type = int, dest='num_rounds', help="Input number of rounds. Numbers over 10 will be split.")
    parser.add_argument("--amount-perround",'-ap', default=0, type=float, dest='amount_1round', help="Input amount per round. Default unit of currency is yolo.")
    parser.add_argument("--amount_currency",'-ac', default='yolo', type = str, dest='currency', help="Name of currency. Must be eth or yolo")

    parser.add_argument("--is_gold", type = bool, dest='is_gold', help="Flipper Extra Keyword: is_gold : 0/1 -> False/True")
    parser.add_argument("--is_above", type = bool, dest='is_above', help="Quantum Extra Keyword: is_gold : 0/1 -> False/True")
    parser.add_argument("--multiplier", type = float, dest='multiplier', help="Quantum Extra Keyword: multiplier : from 1.05 to 100")
    parser.add_argument("--risk_level", type = int, dest='risk_level', help="LaserBlast Extra Keyword: risk_level : int [1,2,3]")
    parser.add_argument("--row_count", type = int, dest='row_count', help="LaserBlast Extra Keyword: row_count : int [8..16]")

    args = parser.parse_args()

    private_key = args.pri_key
    game_name = args.game
    amount_1r = args.amount_1round
    number_r = args.num_rounds
    currency = args.currency

    YL = YOLO()

    num_list = []
    while number_r > 0:
        if number_r > 10:
            num_list.append(10)
            number_r -= 10
        else:
            num_list.append(number_r)
            number_r = 0

    args_dict = {key: value for key, value in vars(args).items() if value is not None}

    game_class = getattr(YL, game_name, None)
    game_class.show_args()
    game_class.set_account(private_key)
    game_class.set_args( **args_dict )

    for i in num_list:
        game_class.play(i, amount_1r, currency)

if __name__ == "__main__":
    main()
