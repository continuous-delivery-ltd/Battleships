from python.orientation import Horizontal, Vertical
from python.ships import AircraftCarrier, Battleship, Cruiser, Destroyer, Submarine


class BattleShips(object):

    def __init__(self, game_sheet_factory, player1, player2):
        self.game_sheet_factory = game_sheet_factory
        self.players = {player1: None, player2: None}

    def new_game(self):
        for player in self.players:
            self.players[player] = self.game_sheet_factory.create_game_sheet()

    def place_ship(self, player, ship_details):
        ship = self._create_ship(ship_details)
        self.players[player].add_ship(ship)

    def place_ships(self, player):
        self.players[player].position_ships()

    def fire(self, player, location):
        self._other_players_sheet(player).fire(location)

    def show_defense(self, player):
        return str(self.players[player])

    def _create_ship(self, ship_details):
        ship_class, location, orientation = parse_ship_details(ship_details)
        return ship_class(location, orientation)

    def _other_players_sheet(self, player):
        return self.players[self._other_player(player)]

    def _other_player(self, player):
        for key in self.players.keys():
            if key is not player:
                return key


def parse_ship_details(ship_details):
    return _ship_type(ship_details[0:1]), ship_details[1:3], _orientation(ship_details[-1:])


def _ship_type(type):
    if type is 'A':
        return AircraftCarrier
    elif type is 'B':
        return Battleship
    elif type is 'C':
        return Cruiser
    elif type is 'D':
        return Destroyer
    elif type is 'S':
        return Submarine


def _orientation(orientation):
    if orientation is 'H':
        return Horizontal
    else:
        return Vertical




