"""Module that expose functions to calculate words in a text."""

from typing import Dict
import json
import string
import re
from collections import Counter

from onetwotext.llm_neural_network_conn import Completion


def python_count(text: str) -> Dict:
    """
    Simple python function to count words in a pythonic way
    make statistics and return dictionary results.

    Input:
    ------
     - text: str
       a string variable that represent text input to be elaborated by function.
    """

    no_punctuation_text = text.translate(str.maketrans("", "", string.punctuation))
    space_stripped_text = (re.sub("\s+", " ", no_punctuation_text)).replace("\n", "")
    words = space_stripped_text.split()
    num_words = len(words)

    word_freq = Counter(words)
    freq_list = [{w: c} for w, c in word_freq.items()]

    response = {"num_words": num_words, "word_freq": freq_list}
    return response


def nn_completion_count(text: str) -> Dict:
    """
    function to invoke LLM neural network to count words, make statistics
    and return results dictionary.
    Input:
    ------
     - text: str
       a string variable that represent text input to be elaborated by function.
    """

    no_punctuation_text = text.translate(str.maketrans("", "", string.punctuation))
    space_stripped_text = (re.sub("\s+", " ", no_punctuation_text)).replace("\n", "")
    prompt = f"""mi scrivi il numero di quante parole sono contenute in questa frase: "{space_stripped_text}".  mi scrivi anche un json che mi conteggi le occorrenze di ogni parola"""
    res = ""
    word_count = None
    words_dict = {}
    try:
        for token in Completion.create(prompt):
            res += token
        res_list = res.split("```")
        try:
            response_count = res_list[0].split('"')
            response_sentence = "".join(response_count[0] + response_count[2])
        except:
            response_sentence = res_list[0]
        match = re.search("\d+", response_sentence)
        if match is not None:
            word_count = int(match.group(0))
        try:
            words_dict = json.loads(
                res_list[1].replace("json", "").strip().replace("\n", "")
            )
        except:
            pass
    except:
        print("could not get a response from the neural network")
    if word_count and words_dict:
        freq_list = [{w: c} for w, c in words_dict.items()]
    else:
        freq_list = []
    response = {"num_words": word_count, "word_freq": freq_list}

    return response
