from unittest import TestCase
from mock import MagicMock

from python.battleships import BattleShips
from python.game_sheet_factory import GameSheetFactory
from python.ships import Hit, Miss, Sunk


ROW_A_START = 0
ROW_A_END = 9

ROW_B_START = 10
ROW_B_END = 19


class BattleShipsTest(TestCase):

    def setUp(self):
        self.battleships = BattleShips(GameSheetFactory(), "Player1", "Player2")

    def test_should_create_new_game(self):
        mock_factory = MagicMock(GameSheetFactory)
        self.battleships = BattleShips(mock_factory, "Player1", "Player2")
        self.battleships.new_game()

        mock_factory.create_game_sheet.assert_called_with()

    def test_should_place_ship(self):
        self.battleships.new_game()
        self.battleships.place_ship("Player1", "AB1H")

        self.assertEquals("BAAAAA...", self.battleships.show_defense("Player1")[ROW_B_START:ROW_B_END])

    def test_should_place_ships_automatically(self):
        self.battleships.new_game()
        self.battleships.place_ships("Player1")

        defense = self.battleships.show_defense("Player1")

        self.assertHasShipId(defense, "A", 5)
        self.assertHasShipId(defense, "B", 4)
        self.assertHasShipId(defense, "C", 3)
        self.assertHasShipId(defense, "D", 4)
        self.assertHasShipId(defense, "S", 2)

    def test_should_report_a_hit(self):
        self.battleships.new_game()
        self.battleships.place_ship("Player2", "AB1H")

        self.assertIsInstance(self.battleships.fire("Player1", "B2"), Hit)

    def test_should_report_a_miss(self):
        self.battleships.new_game()
        self.battleships.place_ship("Player2", "AB1H")

        self.assertIsInstance(self.battleships.fire("Player1", "C2"), Miss)

    def test_should_report_when_a_ship_is_sunk(self):
        self.battleships.new_game()
        self.battleships.place_ship("Player2", "DB1H")
        self.battleships.place_ship("Player2", "SC1H")

        self.battleships.fire("Player1", "B1")
        self.assertIsInstance(self.battleships.fire("Player1", "B2"), Sunk)

    def _other_player(self, player):
        if player is "Player1":
            return "Player2"
        else:
            return "Player1"

    def assertHasShipId(self, defense, id, count):
        expected = count
        if id is not 'S':
            expected = count + 1

        self.assertEquals(expected, defense.count(id))

