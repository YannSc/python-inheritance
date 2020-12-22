import unittest

from auction import BlindAuction
from testing_utils import make_auction


class TestAuction():

    def __init__(self, cli=None):
        self.cli = cli

    def play(self):
        val = self.cli.prompt("give me your name")
        self.cli.display(val)


class TestEcho(unittest.TestCase):

    def test_echo(self):
        cli = make_auction(TestAuction)
        self.assertEqual(['give me your name'], cli.get_displayed())
        cli.type("hello")
        self.assertEqual(['hello'], cli.get_displayed())
        self.assertEqual([], cli.get_displayed())


class TestBlind(unittest.TestCase):
    def test_opening_bid(self):
        cli = make_auction(BlindAuction)
        self.assertEqual(
            [
                'Started auction of type: Blind',
                'Please enter the opening bid:'
            ],
            cli.get_displayed()
        )
        cli.type('30')
        self.assertIn('Opening bid is: 30', cli.get_displayed())

    def test_players(self):
        cli = make_auction(BlindAuction)
        cli.type('30')
        self.assertIn('Enter bidder (enter nothing to move on):',
                      cli.get_displayed())
        cli.type('alice')
        self.assertEqual(
            ['Enter bidder (enter nothing to move on):'],
            cli.get_displayed()
        )
        cli.type('bob')
        self.assertEqual(
            ['Enter bidder (enter nothing to move on):'],
            cli.get_displayed()
        )
        cli.type('carol')
        self.assertEqual(
            ['Enter bidder (enter nothing to move on):'],
            cli.get_displayed()
        )
        cli.type(None)
        self.assertIn('Bidders are: alice, bob, carol', cli.get_displayed())

    def test_auction(self):
        cli = make_auction(BlindAuction)
        cli.type('30')
        cli.type('alice')
        cli.type('bob')
        cli.type('carol')
        cli.type(None)
        self.assertEqual(
            [
                'Bidders are: alice, bob, carol',
                'Opening bid is 30. alice bids:'
            ],
            cli.get_displayed()[-2:]
        )
        cli.type(35)  # TODO: assert & bid
        self.assertEqual(
            [
                'Opening bid is 30. bob bids:'
            ],
            cli.get_displayed()
        )
        cli.type(50)
        self.assertEqual(
            [
                'Opening bid is 30. carol bids:'
            ],
            cli.get_displayed()
        )
        cli.type(40)
        self.assertEqual(
            'Winner is bob. Winning bid is 50.',
            cli.get_displayed()[-1]
        )


if __name__ == "__main__":
    unittest.main()
