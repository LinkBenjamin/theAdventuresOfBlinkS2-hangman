# The first thing we do is import pytest, and 
# then we grab the Hangman class that we anticipate
# writing in game.py.
import pytest
from hangman.game import Hangman

# Annotating a method as a fixture allows you to 
# create shared setup and teardown code that all 
# of your tests can use.
@pytest.fixture
def new_game():
    # Our new_game fixture creates a hangman board with 
    # the word "PYTHON" as its content.
    return Hangman("PYTHON")  # Example game phrase

@pytest.fixture
def new_phrase_game():
    return Hangman("TWO WORDS")

# Our first test defines the initial state of the game.
# We list our expectations here and verify that the new
# object meets those expectations.
def test_initial_game_state(new_game, new_phrase_game):
    """Test the initial state of the game."""
    # Create a new game
    game = new_game
    game2 = new_phrase_game
    # Check the values we expect the game to have for these values
    assert game.remaining_lives == 6  # Assuming 6 lives to start
    assert game.get_display_word == "______"  # Hidden word
    assert game.guessed_letters == []  # No guesses yet
    assert game.game_over is False  # Game isn't over
    assert game2.get_display_word == "___ _____"

# Our next test validates what happens when you select
# a letter that DOES appear in the puzzle.
def test_correct_guess(new_game):
    """Test guessing a correct letter."""
    game = new_game
    # Use the game's "guess" method to pick the letter 'P'
    result = game.guess("P")
    # Validate that the method returns the right value and
    # also that it updates the game appropriately.
    assert result is True
    assert game.get_display_word == "P_____"  # 'P' revealed
    assert game.guessed_letters == ["P"]

# Next we should validate what happens if the letter is NOT
# present in the puzzle
def test_incorrect_guess(new_game):
    """Test guessing an incorrect letter."""
    game = new_game
    result = game.guess("X")
    assert result is False
    assert game.remaining_lives == 5  # Lose a life
    assert game.guessed_letters == ["X"]

# Testing a single incorrect guess is a start, but we 
# should ensure that multiple incorrect guesses update the game
# correctly, too
def test_multiple_incorrect_guesses(new_game):
    """Test multiple incorrect guesses."""
    game = new_game
    game.guess("X")
    game.guess("Z")
    assert game.remaining_lives == 4  # Lost two lives
    assert "X" in game.guessed_letters
    assert "Z" in game.guessed_letters

# We should validate that the "game is won" behavior
def test_game_won(new_game):
    """Test the game is won after correct guesses."""
    game = new_game
    game.guess("P")
    game.guess("Y")
    game.guess("T")
    game.guess("H")
    game.guess("O")
    game.guess("N")
    assert game.game_won is True
    assert game.game_over is True

# And of course, we should validate that you can lose the game too!
def test_game_lost(new_game):
    """Test the game is lost after too many incorrect guesses."""
    game = new_game
    for guess in ["A", "B", "C", "D", "E", "F"]:
        game.guess(guess)
    assert game.remaining_lives == 0
    assert game.game_over is True
    assert game.game_won is False

# Finally, we need to ensure that duplicate guesses of a letter
# are ignored by the game state.
def test_duplicate_guess(new_game):
    """Test that duplicate guesses do not affect lives or state."""
    game = new_game
    game.guess("P")
    game.guess("P")  # Duplicate guess
    assert game.remaining_lives == 6  # Lives shouldn't change
    assert game.guessed_letters == ["P"]  # No duplicate in guessed letters