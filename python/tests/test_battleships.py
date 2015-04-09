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

    def test_should_show_my_hits(self):
        self.battleships.new_game()
        self.battleships.place_ship("Player2", "AB1H")

        self.battleships.fire("Player1", "B3")

        offense = self.battleships.show_offense("Player1")

        self.assertEquals("B..X.....", offense[ROW_B_START:ROW_B_END])

    def test_should_show_my_misses(self):
        self.battleships.new_game()
        self.battleships.place_ship("Player2", "AB1H")

        self.battleships.fire("Player1", "A2")

        offense = self.battleships.show_offense("Player1")

        self.assertEquals("A.x......", offense[ROW_A_START:ROW_A_END])

    def test_should_report_when_a_ship_is_sunk(self):
        self.battleships.new_game()
        self.battleships.place_ship("Player2", "DB1H")
        self.battleships.place_ship("Player2", "SC1H")

        self.battleships.fire("Player1", "B1")
        self.assertIsInstance(self.battleships.fire("Player1", "B2"), Sunk)

    def test_should_show_my_opponents_hits_misses(self):
        self.battleships.new_game()
        self.battleships.place_ship("Player1", "AB1H")

        self.battleships.fire("Player2", "A2")

        defense = self.battleships.show_defense("Player1")

        self.assertEquals("A.x......", defense[ROW_A_START:ROW_A_END])

    def test_should_show_my_opponents_hits(self):
        self.battleships.new_game()
        self.battleships.place_ship("Player1", "AB1H")

        self.battleships.fire("Player2", "B3")

        defense = self.battleships.show_defense("Player1")

        self.assertEquals("BAAXAA...", defense[ROW_B_START:ROW_B_END])

    def test_should_return_fire_after_each_move_when_playing_against_the_computer(self):
        self.battleships = BattleShips(GameSheetFactory(), "Player1", "Computer")
        self.battleships.new_game()
        self.battleships.place_ship("Player1", "AB1H")

        self.assertEquals(0, count_hits_and_misses(self.battleships.show_defense("Player1")))

        self.battleships.fire("Player1", "A2")

        self.assertEquals(1, count_hits_and_misses(self.battleships.show_defense("Player1")))

    def test_should_report_winner_when_there_are_no_more_ships_to_sink(self):
        self.battleships.new_game()

        self.battleships.place_ship("Player1", "SG1H")
        self.battleships.place_ship("Player1", "DB1H")

        self.battleships.fire("Player2", "B1")
        self.battleships.fire("Player2", "G1")

        self.assertRaisesWithMessage("Game Over - Player2 Wins!", self.battleships.fire, "Player2", "B2")

    def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.fail()
        except Exception as inst:
            self.assertEqual(inst.message, msg)

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


def count_hits_and_misses(sheet):
    return sheet.count('x') + sheet.count('X')

