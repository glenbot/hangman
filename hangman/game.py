import os
import logging
import random
import base64

import zmq

from . import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')


class Game:
    """Game loop"""
    def __init__(self):
        self.logger = logger

        self.words_file = os.path.join(DATA_PATH, 'usa.txt')
        self.words = []
        with open(self.words_file, 'r') as f:
            self.words = f.readlines()

        # game states
        self.started = False
        self.finished = False
        self.max_guesses = 7
        self.state = 0
        self.help = False
        self.won = False

        # Computed propeties
        self._intro = None
        self._winner = None
        self._loser = None
        self._banner = None

        # word selection
        self.word = None
        self.letters = []
        self.partial_word = ''
        self.correctly_guessed_letters = []
        self.incorrectly_guessed_letters = []
        self.incorrectly_guessed_words = []

        # hangman states
        self.hang_states = []
        self.load_hang_states()

    @property
    def clear_code(self):
        return b'\033[2J'

    @property
    def prompt(self):
        return b'\r>> '

    @property
    def banner(self):
        """Load winner screen"""
        if self._banner is None:
            with open(os.path.join(DATA_PATH, 'banner.txt'), 'rb') as f:
                self._banner = f.read()
        return self._banner

    @property
    def winner(self):
        """Load winner screen"""
        if self._winner is None:
            with open(os.path.join(DATA_PATH, 'winner.txt'), 'rb') as f:
                self._winner = f.read()
        return self._winner

    @property
    def loser(self):
        """Load loser screen"""
        if self._loser is None:
            with open(os.path.join(DATA_PATH, 'gameover.txt'), 'rb') as f:
                self._loser = f.read()
        return self._loser

    @property
    def intro(self):
        """Load intro screen"""
        if self._intro is None:
            with open(os.path.join(DATA_PATH, 'intro.txt'), 'rb') as f:
                self._intro = f.read()
        return self._intro

    def load_hang_states(self):
        """Load all the hangmans states"""
        state_files = [
            os.path.join(DATA_PATH, 'manstate1.txt'),
            os.path.join(DATA_PATH, 'manstate2.txt'),
            os.path.join(DATA_PATH, 'manstate3.txt'),
            os.path.join(DATA_PATH, 'manstate4.txt'),
            os.path.join(DATA_PATH, 'manstate5.txt'),
            os.path.join(DATA_PATH, 'manstate6.txt'),
            os.path.join(DATA_PATH, 'manstate7.txt'),
            os.path.join(DATA_PATH, 'manstate8.txt')
        ]
        for sf in state_files:
            with open(sf, 'rb') as f:
                self.hang_states.append(f.read())

    def get_win_statement(self):
        """Get the final win statement"""
        return bytes("""
The word you guessed was: {}

Type 'n' and hit enter to start a new game
        """.format(self.word), 'utf-8')

    def get_lose_statement(self):
        """Get the final lose statement"""
        return bytes("""
The word you tried to guess was: {}

Type 'n' and hit enter to start a new game
        """.format(self.word), 'utf-8')

    def get_hint(self):
        """Get the initial line"""
        return bytes("""
A word that is {} characters long
        """.format(len(self.letters)), 'utf-8')

    def get_word_state(self):
        """Get the state of the word"""
        letter_holder = []

        if len(self.correctly_guessed_letters) == 0:
            for l in self.letters:
                letter_holder.append('_')
        else:
            for l in self.letters:
                if l in self.correctly_guessed_letters:
                    letter_holder.append(l)
                    continue
                letter_holder.append('_')

        # check for a winning word by guessing only letters
        self.partial_word = ''.join(letter_holder)
        if self.partial_word == self.word:
            self.win()

        # check for losing game
        if self.state == self.max_guesses:
            self.lose()

        return bytes("""

{}

Correctly guessed: {}
Incorrectly guessed: {}
Incorrectly guessed words: {}

g <letter> - guess letter
gw <word> - guess word
        """.format(
            ''.join(letter_holder),
            ','.join(self.correctly_guessed_letters),
            ','.join(self.incorrectly_guessed_letters),
            ','.join(self.incorrectly_guessed_words)
        ), 'utf-8')

    def get_hang_state(self):
        """Get the state of the hang man"""
        try:
            return self.hang_states[self.state]
        except IndexError:
            return self.hang_states[self.max_guesses]

    def print_screen(self):
        # clear the screen
        output = self.clear_code + self.banner

        # the game just started to print the intro screen
        if self.finished and self.won:
            output += self.winner + self.get_win_statement()
        elif self.finished and not self.won:
            output += self.loser + self.get_lose_statement()
        elif not self.started and self.state == 0:
            output += self.intro
        elif self.help:
            self.help = False
            output += self.intro
        else:
            output += \
                self.get_hang_state() + \
                self.get_word_state() + \
                self.get_hint() + \
                b'\033[8D'

        # check for a finished letter game
        if self.finished and self.won:
            output = self.clear_code + \
                self.banner + \
                self.winner + \
                self.get_win_statement()
        elif self.finished and not self.won:
            output = self.clear_code + \
                self.banner + \
                self.loser + \
                self.get_lose_statement()

        # add the prompt
        output += self.prompt

        return output

    def guess_word(self, word):
        """Guess a letter"""
        if self.state == self.max_guesses:
            self.lose()

        if word != self.word:
            self.incorrectly_guessed_words.append(word)
            self.state += 1
        else:
            self.win()

    def guess(self, letter):
        """Guess a letter"""
        if self.state == self.max_guesses:
            self.lose()

        letter = letter.lower()
        if letter in self.letters:
            if letter in self.correctly_guessed_letters or letter in self.incorrectly_guessed_letters:
                return  # letter was already guessed
            self.correctly_guessed_letters.append(letter)
            return
        if letter in self.incorrectly_guessed_letters:
            return
        self.incorrectly_guessed_letters.append(letter)
        self.state += 1

    def win(self):
        self.started = False
        self.finished = True
        self.won = True

    def lose(self):
        self.started = False
        self.finished = True
        self.won = False

    def new(self):
        """Configure a new game"""
        if not self.started:
            self.help = False
            self.started = True
            self.finished = False
            self.won = False
            self.state = 0
            self.partial_word = ''
            self.correctly_guessed_letters = []
            self.incorrectly_guessed_letters = []
            self.incorrectly_guessed_words = []
            self.word = random.choice(self.words).strip()
            logger.info('Game word is: %s', self.word)
            self.letters = [l for l in self.word]


class GameServer:
    def __init__(self):
        self.client_dict = {}
        self.logger = logger
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.STREAM)

    def ready(self):
        """Readiness probe for k8s"""
        with open(settings.READINESS_PROBE_FILE, 'w') as f:
            f.write('1')

    def liveness(self, remove=False):
        """Liveness probe for k8s"""
        if not remove:
            with open(settings.LIVENESS_PROBE_FILE, 'w') as f:
                f.write('1')
        else:
            os.unlink(settings.LIVENESS_PROBE_FILE)

    def start(self):
        bind_uri = 'tcp://{}:{}'.format(
            settings.SERVER_ADDRESS,
            settings.SERVER_PORT
        )
        self.logger.info('Initializing game server: %s', bind_uri)
        self.socket.bind(bind_uri)

        # set the application as ready and live
        self.ready()
        self.liveness()

        while True:
            client_id, message = self.socket.recv_multipart()

            try:
                message = message.decode('utf-8').strip()
            except UnicodeDecodeError:
                logger.info('Unicode decode error')
                continue

            logger.info('client_id: %s message(%s): %s', base64.b64encode(client_id), len(message), message)

            client_state = None
            game = None
            if client_id not in self.client_dict.keys():
                self.client_dict[client_id] = {
                    'game': Game()
                }
                client_state = self.client_dict[client_id]
                game = client_state['game']
            else:
                client_state = self.client_dict[client_id]
                game = client_state['game']

            if message.startswith('n') and len(message) == 1:
                game.new()

            if message.startswith('h') and len(message) == 1:
                game.help = True

            if message.startswith('g '):
                if game.started:
                    try:
                        _, letter = message.split()
                    except ValueError:
                        continue
                    game.guess(letter.strip())

            if message.startswith('gw '):
                if game.started:
                    try:
                        _, word = message.split()
                    except ValueError:
                        continue
                    game.guess_word(word.strip())

            try:
                self.socket.send_multipart([client_id, game.print_screen()], zmq.NOBLOCK)
            except zmq.error.Again:
                continue
