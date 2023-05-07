import pytest
from onetwotext.word_calculator import python_count, nn_completion_count


@pytest.fixture
def text():
    return "Hello world! This is a test string. It contains several words. How many words does it contain?"


def test_python_count(text):
    expected = {"num_words": 13, "word_freq": [{"Hello": 1}, {"world": 1}, {"This": 1}, {"is": 1}, {"a": 1}, {"test": 1}, {"string": 1}, {"It": 1}, {"contains": 1}, {"several": 1}, {"words": 2}, {"How": 1}, {"many": 1}]}
    assert python_count(text) == expected


def test_nn_completion_count(text):
    expected = {"num_words": 13, "word_freq": [{"Hello": 1}, {"world": 1}, {"This": 1}, {"is": 1}, {"a": 1}, {"test": 1}, {"string": 1}, {"It": 1}, {"contains": 1}, {"several": 1}, {"words": 2}, {"How": 1}, {"many": 1}]}
    assert nn_completion_count(text) == expected
