from chalice import Blueprint
from treys import Card, Deck, Evaluator
import json

noauth = Blueprint(__name__)


@noauth.route('/treys')
def index():
    evaluator = Evaluator()
    deck = Deck()
    card = Card.new('Qh')
    board = deck.draw(5)
    player_names = ("player 1", "player 2", "player 3", "player 4", "player 5", "player 6", "player 7", "player 8")
    players = {}
    output = {}
    # this is procedural programming, not functional programming :(
    for p in player_names:
        hand = deck.draw(2)
        score = evaluator.evaluate(board, hand)
        text = evaluator.class_to_string(evaluator.get_rank_class(score))
        players[p] = score
        output[p] = {'score': score, 'text': text}
    # What about a tie?
    tie = (len(players.values()) == len(set(players.values())))
    winner = min(players, key=players.get)  # always 1 result :( Don't forget to fix the TEST!
    # does the tie involve the winning hand though?
    # TODO https://stackoverflow.com/questions/17821079/how-to-check-if-two-keys-in-dictionary-hold-the-same-value
    output["winners"] = winner
    output["tie"] = tie
    output["card"] = Card.int_to_str(card)
    j = json.dumps(output)
    return j


# This is a basic health check used by test_hello.py
@noauth.route('/hello/world')
def index():
    return {'hello': 'world'}
