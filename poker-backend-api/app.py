from chalice import Chalice
from treys import Card, Deck, Evaluator
import json

app = Chalice(app_name='poker-backend-api')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/treys')
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
    output["card"] = card
    j = json.dumps(output)
    return j


# This is a basic health check used by test_hello.py
@app.route('/hello/world')
def index():
    return {'hello': 'world'}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
