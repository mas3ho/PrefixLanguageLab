from itertools import product

ALPHABET = ('a', 'b')
EPSILON = 'ε'
NONEMPTY = 'NONEMPTY'
STANDARD = 'STANDARD'
MODES = (NONEMPTY, STANDARD)
SUBSCRIPT = {1: '₁', 2: '₂', 3: '₃'}


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def is_valid_string(text):
    """Return True if text is a valid string over {a, b}."""
    if not isinstance(text, str):
        return False
    return all(ch in ALPHABET for ch in text)


def is_valid_mode(text):
    """Return True if text names a valid mode."""
    return isinstance(text, str) and text.upper() in MODES


def parse_mode(text):
    """Return the mode named by text, or None if invalid."""
    if not is_valid_mode(text):
        return None
    return text.upper()


def is_valid_max_length(text):
    """Return True if text represents an integer in [0, 8]."""
    return isinstance(text, str) and text in tuple('012345678')


# ---------------------------------------------------------------------------
# Prefix generation
# ---------------------------------------------------------------------------

def generate_prefixes(word, mode):
    """Return the list of prefixes of `word` under the given mode."""
    if mode == NONEMPTY:
        start = 1
    elif mode == STANDARD:
        start = 0
    else:
        raise ValueError(f'Unknown mode: {mode!r}')

    return [word[:i] for i in range(start, len(word) + 1)]


def display_prefix(prefix):
    """Display the empty string as ε."""
    return EPSILON if prefix == '' else prefix


def display_prefixes(prefixes):
    """Return a comma-separated string of display labels."""
    if not prefixes:
        return '(none)'
    return ', '.join(display_prefix(p) for p in prefixes)


def format_input(word):
    """Display label for the input string."""
    return EPSILON if word == '' else word


# ---------------------------------------------------------------------------
# Language recognition
# ---------------------------------------------------------------------------

def recognize(word, language, mode):
    """Return (decision, explanation) for `word` in the given language."""
    prefixes = generate_prefixes(word, mode)

    if language == 1:
        for p in prefixes:
            if 'b' in p:
                return 'REJECT', f'Prefix {display_prefix(p)} contains b'
        return 'ACCEPT', 'No prefix contains b'

    if language == 2:
        for p in prefixes:
            if p.startswith('a'):
                return 'REJECT', f'Prefix {display_prefix(p)} starts with a'
        return 'ACCEPT', 'No prefix starts with a'

    if language == 3:
        for p in prefixes:
            if not p.startswith('a'):
                return 'REJECT', f'Prefix {display_prefix(p)} does not start with a'
        return 'ACCEPT', 'Every prefix starts with a'

    raise ValueError(f'Unknown language: {language!r}')


# ---------------------------------------------------------------------------
# Enumeration
# ---------------------------------------------------------------------------

def generate_strings(max_length):
    """Yield all strings over {a,b} of length 0..max_length in shortlex order."""
    for length in range(max_length + 1):
        for chars in product(ALPHABET, repeat=length):
            yield ''.join(chars)


def enumerate_language(language, mode, max_length):
    """Return the list of words of length <= max_length accepted by language."""
    accepted = []
    for word in generate_strings(max_length):
        decision, _ = recognize(word, language, mode)
        if decision == 'ACCEPT':
            accepted.append(word)
    return accepted


# ---------------------------------------------------------------------------
# Presentation helpers
# ---------------------------------------------------------------------------

def print_decision(word, mode):
    """Print the prefixes and the three decisions for one input and mode."""
    print(f'Input: {format_input(word)}')
    print(f'Mode: {mode}')
    print(f'Prefixes: {display_prefixes(generate_prefixes(word, mode))}')
    for language in (1, 2, 3):
        decision, reason = recognize(word, language, mode)
        print(f'L{SUBSCRIPT[language]}: {decision} - {reason}')


def prompt_for_string():
    """Prompt the user for a string over {a, b}; return it, or None if invalid."""
    raw = input('Enter a string over {a, b} (or empty for ε): ')
    if not is_valid_string(raw):
        print(f'Invalid input: {raw!r}. Only lowercase letters a and b are allowed.')
        return None
    return raw


def prompt_for_mode():
    """Prompt the user for a mode; return it, or None if invalid."""
    raw = input(f'Enter a mode of operation {MODES}: ')
    if not is_valid_mode(raw):
        print(f'Invalid mode: {raw!r}. Must be one of {MODES}.')
        return None
    return parse_mode(raw)


def pause():
    """Wait for the user to press Enter so results stay readable."""
    input('Press Enter to return to the menu...')


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------

def action_recognize():
    """Menu option 1: recognise one string in one mode."""
    word = prompt_for_string()
    if word is None:
        pause()
        return

    mode = prompt_for_mode()
    if mode is None:
        pause()
        return

    print()
    print_decision(word, mode)
    pause()


def action_enumerate():
    """Menu option 2: enumerate accepted strings up to N for all three languages."""
    mode = prompt_for_mode()
    if mode is None:
        pause()
        return

    raw = input('Enter a maximum length N (0..8): ')
    if not is_valid_max_length(raw):
        print(f'Invalid maximum length: {raw!r}. Must be an integer in [0, 8].')
        pause()
        return

    max_length = int(raw)
    total = 2 ** (max_length + 1) - 1

    print()
    print(f'Mode: {mode}, N = {max_length}')
    print(f'Total candidates: {total}')
    for language in (1, 2, 3):
        accepted = enumerate_language(language, mode, max_length)
        labels = ', '.join(format_input(w) for w in accepted) if accepted else '(none)'
        print(f'L{SUBSCRIPT[language]} accepted ({len(accepted)}): {labels}')
    pause()


def action_compare():
    """Menu option 3: compare NONEMPTY and STANDARD for the same input."""
    word = prompt_for_string()
    if word is None:
        pause()
        return

    print()
    for mode in MODES:
        print_decision(word, mode)
        print()
    pause()


# ---------------------------------------------------------------------------
# Menu and help
# ---------------------------------------------------------------------------

def show_menu():
    print()
    print('=' * 50)
    print('PrefixLanguageLab')
    print('=' * 50)
    print('1. Recognise one string')
    print('2. Enumerate up to N')
    print('3. Compare modes')
    print('4. Exit')
    print('=' * 50)


def explain_options():
    print()
    print('1. Recognise one string')
    print('2. Enumerate up to N')
    print('3. Compare modes')
    print('4. Exit')


def main():
    while True:
        show_menu()
        choice = input('Choose an option (1-4, or ? for help): ').strip().lower()

        if choice == '1':
            action_recognize()
        elif choice == '2':
            action_enumerate()
        elif choice == '3':
            action_compare()
        elif choice == '4':
            print('Goodbye.')
            break
        elif choice in ('?', 'help', 'h'):
            explain_options()
        else:
            print(f'INVALID CHOICE: {choice!r}. Enter 1, 2, 3, 4 or ?.')


if __name__ == '__main__':
    main()