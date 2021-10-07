import pandas as pd
from pandas import Series
from numpy.random import choice


class Arena:

    def __init__(self, csv_list: list, num_rounds=5):
        self.csv_list = csv_list
        self.num_rounds = num_rounds
        self.stick_df = self.build_stick_dataframe()

    def build_stick_dataframe(self):
        types = {"hash": str,
                 "s_num": str,
                 "rarity": float,
                 "bg": str,
                 "body": str,
                 "misc": str,
                 "hand": str}
        df = pd.read_csv(self.csv_list[0], dtype=types).dropna()
        if len(self.csv_list) > 1:
            for csv in self.csv_list[1:]:
                tmp_df = pd.read_csv(csv, dtype=types).dropna()
                df = pd.concat([df, tmp_df])

        def parse_rarity(s):
            s = s[1:-1]
            rarity = s.split(",")[-1]
            return float(rarity)

        for col in ["bg", "body", "misc", "hand"]:
            df[col] = df[col].apply(parse_rarity)
        return df.set_index("s_num")

    def verify_stick(self, stick_number: str) -> bool:
        try:
            self.get_stick(stick_number)
            return True
        except KeyError:
            return False

    def get_stick(self, stick_number: str) -> Series:
        num_str = f"CryptoStykz {stick_number}"
        try:
            return self.stick_df.loc[num_str]
        except KeyError:
            num_str = f"CryptoStykz #{stick_number}"
            return self.stick_df.loc[num_str]

    def calc_odds(self, stick: Series) -> float:
        return (abs(stick.rarity) / 3) / 2 + 0.5

    def fight_round(self, snum1: str, snum2: str) -> str:
        s1 = self.get_stick(snum1)
        s2 = self.get_stick(snum2)
        rarer = [snum1, snum2] if s1.rarity < s2.rarity else [snum2, snum1]
        winning_odds = self.calc_odds(self.get_stick(rarer[0]))
        losing_odds = 1 - winning_odds
        winner = choice(rarer, p=[winning_odds, losing_odds])
        return winner

    def fight_sticks(self, snum1: str, snum2: str) -> list:
        rounds = list()
        for _ in range(self.num_rounds):
            rounds.append(self.fight_round(snum1, snum2))
        return rounds

    def match_winner(self, rounds: list) -> str:
        fighters = set(rounds)
        if len(fighters) == 1:
            return fighters.pop()
        else:
            results = [(rounds.count(fighter), fighter) for fighter in fighters]
            return max(results)[1]

    # Randomly select 2 different stick numbers
    def random_fighers(self):
        fighters = choice(self.stick_df.index, size=2, replace=False)
        return list(map(lambda x: x.split(" ")[-1], fighters))


if __name__ == "__main__":
    arena = Arena(["cryptostykz_v3.csv"])
    stick_df = arena.build_stick_dataframe()
    print(stick_df)
    for _ in range(10):
        print(arena.random_fighers())