# unscrembler.py

import json
import os
import dotenv
from typing import List, Dict

dotenv.load_dotenv()

# words_path = os.getenv("WORDLIST_FILE_PATH", None)
# if words_path is None:
#     raise ValueError("WORDLIST_FILE_PATH is not set in .env!")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create the full path to words.json
words_path = os.path.join(BASE_DIR, "words.json")

class PyScramble:
    """
    PyScramble unscrambles a string of characters into valid words, 
    using a preloaded dictionary from words.json.
    """

    def __init__(self, words_file_path = words_path) -> None:
        """
        Initialize PyScramble by loading words from a JSON file and building an index for unscrambling.

        :param words_file_path: path to the JSON file containing the list of words.
        """
        self.words_file_path = words_file_path
        self._words_index: Dict[str, List[str]] = {}

        # Load and index words
        self._load_and_index_words()

    def _load_and_index_words(self) -> None:
        """
        Private method to load words from the JSON file and build an in-memory index
        mapping sorted letters -> list of matching words.
        """
        file_path = self.words_file_path

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Words JSON file not found at: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                words = data.get("word_list", [])
        except (json.JSONDecodeError, OSError) as e:
            raise ValueError(f"Error reading {file_path}: {e}")

        # Build an index so we can unscramble quickly
        # Key: sorted letters, Value: list of words that match those letters
        for word in words:
            sorted_key = self._sort_string(word)
            if sorted_key not in self._words_index:
                self._words_index[sorted_key] = []
            self._words_index[sorted_key].append(word)

        # Sort each list of anagrams alphabetically for consistent ranking
        for key in self._words_index:
            self._words_index[key].sort()

    @staticmethod
    def _sort_string(s: str) -> str:
        """
        Sort the letters of a string to produce a canonical form (key).
        Example: 'cat' -> 'act'
        """
        return "".join(sorted(s.lower()))

    def unscramble(self, scrambled_string: str) -> List[str]:
        """
        Unscramble a given string into a ranked list of possible words from the dictionary.
        
        :param scrambled_string: The scrambled input to unscramble
        :return: A list of valid words (anagrams). The first item is the most likely 
                 if you are using alphabetical or alternative heuristic.
                 If no matches exist, returns an empty list.
        """
        # Basic sanitization remove spaces, ensure letters only, etc. if needed
        scrambled_string = scrambled_string.strip()
        if not scrambled_string:
            return []

        # Build the key for lookup
        key = self._sort_string(scrambled_string)
        # Return the pre-computed anagrams or an empty list
        return self._words_index.get(key, [])

if __name__ == "__main__":
    unscrambler = PyScramble()

    samples = ["sirpa"]
    for sample in samples:
        result = unscrambler.unscramble(sample)
        print(f"Scrambled: {sample}, Unscrambled: {result}")