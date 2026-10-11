from itertools import product
from pydoc import text
from turtle import mode

ALPHABET = ('a', 'b')
EPSILON = 'ε'
MODES = (NONEMPTY, STANDARD)
SUBSCRIPT = {1: '₁', 2: '₂', 3: '₃'}

#1 Input: A string of characters from the alphabet.

def is_valid_string(text):
   """ Return True if text is a valid string over {a, b}.

   The empty string ''  is valid and represents the empty string ε.  
   Rejects uppercase letters, digits, and any other characters not in the alphabet.
   """

   if not isinstance(text, str):
      return False
   return all(ch in ALPHABET for ch in text)

def is_valid_mode(text):
   """ Return True if text names a valid mode of operation."""
   return isinstance(text, str) and text.upper() in MODES
   
   
def parse_mode(text):
    """ Return the mode of operation named by text, or None if invalid."""
  
    if not is_valid_mode(text):
        return None
    return text.upper()

def is_valid_max_length(text):
    """Return True if text represents an integer in [0, 8]."""
    return isinstance(text, str) and text in tuple('012345678')

#2 Prefix Generation

def generate_prefixes(word, mode):
    """Return the list of prefixes of `word` under the given mode.

    NONEMPTY : prefixes of length 1..len(word)  (ε has no prefixes)
    STANDARD : prefixes of length 0..len(word)  (includes ε)

    The empty prefix is returned as '' and later displayed as 'ε'.
    Prefixes are returned in increasing length order.
    """
    if mode == 'NONEMPTY':
        start = 1
    elif mode == 'STANDARD':
        start = 0
    else:
        raise ValueError(f'Unknown mode: {mode!r}')
    return [word[:i] for i in range(start, len(word) + 1)]


def display_prefix(prefix):
    """Return the display label for a prefix, replacing the empty string with ε."""
    return EPSILON if prefix == '' else prefix

def display_prefixes(prefixes):
    """Return a comma-separated string of display labels for the given list of prefixes."""
    if not prefixes:
        return '(none)'
    return ', '.join(display_prefix(p) for p in prefixes)

def format_input(word):
    """Display label for the input string."""
    return EPSILON if word == '' else word

# 3. Language Recognition

def recognize(word, language, mode):
    """Return (decision, explanation) for `word` in the given language under mode.
    `language` is 1, 2, or 3. `mode` is 'STANDARD' or 'NONEMPTY'.
    The prefixes are generated first and examined one by one.
    The first prefix that violates the language rules is reported in the explanation.
    
    """
    prefixes = generate_prefixes(word, mode)
    if language == 1:
        #L₁ = {w ∈ {a, b}* : no prefix of w contains b}
        for p in prefixes:
            if 'b' in p:
                return 'REJECT', f'Prefix {display_prefix(p)} contains b'
        return 'ACCEPT', 'All prefixes are valid'