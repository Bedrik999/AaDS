def finite_state_machine_search(text, pattern):
    text = text.lower()
    pattern = pattern.lower()

    transition_table = build_transition_table(pattern)
    
    return search_pattern(text, pattern, transition_table)


def build_transition_table(pattern):
    ALPHABET_SIZE = 26
    pattern_length = len(pattern)
    
    transition_table = [[0 for _ in range(ALPHABET_SIZE)] 
                        for _ in range(pattern_length)]

    for state in range(pattern_length):
        for char_index in range(ALPHABET_SIZE):
            current_char = chr(char_index + ord('a'))
            prefix = pattern[:state] + current_char
            
            for suffix_start in range(len(prefix)):
                suffix = prefix[suffix_start:]
                pattern_prefix = pattern[:len(suffix)]
                
                if suffix == pattern_prefix:
                    transition_table[state][char_index] = len(suffix)
                    break
    
    final_state = [pattern_length for _ in range(ALPHABET_SIZE)]
    transition_table.append(final_state)
    
    return transition_table


def search_pattern(text, pattern, transition_table):
    current_state = 0
    pattern_length = len(pattern)
    
    for character in text:
        if 'a' <= character <= 'z':
            char_index = ord(character) - ord('a')
            current_state = transition_table[current_state][char_index]
            
            if current_state == pattern_length:
                return True
        else:
            current_state = 0
    
    return False


def main():
    test_cases = [
        ("abcd", "abcd", True),
        ("zzabcdzz", "abcd", True),
        ("abxabc", "abcd", False),
        ("helloworld", "world", True),
        ("patternmatching", "match", True),
        ("nomatchhere", "xyz", False),
    ]
    
    print("Тестирование алгоритма конечного автомата для поиска подстроки:")
    print("-" * 50)
    
    for text, pattern, expected in test_cases:
        result = finite_state_machine_search(text, pattern)
        status = "✓" if result == expected else "✗"
        print(f"{status} Текст: '{text}', Паттерн: '{pattern}' -> {result}")


if __name__ == "__main__":
    main()