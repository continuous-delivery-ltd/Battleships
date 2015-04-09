from unittest import TestCase
from mock import MagicMock

from python.battleships import BattleShips
from python.game_sheet_factory import GameSheetFactory


ROW_B_START = 10
ROW_B_END = 19


class BattleShipsTest(TestCase):

    def setUp(self):
        self.battleships = BattleShips(GameSheetFactory())

    def test_should_create_new_game(self):
        mock_factory = MagicMock(GameSheetFactory)
        self.battleships = BattleShips(mock_factory)
        self.battleships.new_game()

        mock_factory.create_game_sheet.assert_called_with()

    def test_should_place_ship(self):
        self.battleships.new_game()
        self.battleships.place_ship("AB1H")

        self.assertEquals("BAAAAA...", str(self.battleships.sheet)[ROW_B_START:ROW_B_END])

    def test_should_place_ships_automatically(self):
        self.battleships.new_game()
        self.battleships.place_ships()

        sheet = str(self.battleships.sheet)

        self.assertHasShipId(sheet, "A", 5)
        self.assertHasShipId(sheet, "B", 4)
        self.assertHasShipId(sheet, "C", 3)
        self.assertHasShipId(sheet, "D", 4)
        self.assertHasShipId(sheet, "S", 2)

    def assertHasShipId(self, sheet, ship_id, count):
        expected = count
        if ship_id is not 'S':
            expected = count + 1

        self.assertEquals(expected, sheet.count(ship_id))

