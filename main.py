from bs4 import BeautifulSoup
from typing import TypedDict, List
from collections import defaultdict
import requests


class OddsFiveThirtyEight(TypedDict):
    teams: List[str]
    odds: List[float]


def main() -> None:

    games = parse_games_538()
    print(games)


def parse_games_538() -> List[OddsFiveThirtyEight]:
    raw_html = requests.get("https://projects.fivethirtyeight.com/2022-nba-predictions/games/").text
    soup = BeautifulSoup(raw_html, 'html.parser')

    res = list()

    for game in soup.find_all("table", "game-body"):

        game_dict = defaultdict(list)

        for team in game.find_all("tr", "team"):
            game_dict['teams'].append(team['data-team'])
            text = team.find('td', "spread").getText()

            odd = float("+inf")

            if not len(text) == 0:
                if text == "PK":
                    odd = 0
                else:
                    odd = float(text)

            game_dict['odds'].append(odd)

        if game_dict['odds'][0] == float("+inf"):
            game_dict['odds'][0] = 0 - game_dict['odds'][1]
        elif game_dict['odds'][1] == float("+inf"):
            game_dict['odds'][1] = 0 - game_dict['odds'][0]

        res.append(game_dict)

    return res


if __name__ == '__main__':
    main()

