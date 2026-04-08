def boyer_moore_search(text, pattern):
    if not pattern or not text:
        return pattern in text
    
    bad_char_table = build_bad_character_table(pattern)
    good_suffix_shift, prefix_suffix_match = build_good_suffix_tables(pattern)
    
    return perform_search(text, pattern, bad_char_table, good_suffix_shift, prefix_suffix_match)


def build_bad_character_table(pattern):
    ALPHABET_SIZE = 26
    bad_char_shift = [len(pattern)] * ALPHABET_SIZE
    
    chars_in_pattern = set()
    for char in pattern:
        chars_in_pattern.add(ord(char) - ord('a'))
    
    for char_code in range(ALPHABET_SIZE):
        if char_code in chars_in_pattern:
            for position in range(len(pattern) - 1, -1, -1):
                if pattern[position] == chr(char_code + ord('a')):
                    bad_char_shift[char_code] = position + 1
                    break
    
    return bad_char_shift


def build_good_suffix_tables(pattern):
    pattern_length = len(pattern)
    good_suffix_shift = [-1] * pattern_length
    prefix_suffix_match = [0] * pattern_length
    
    for suffix_start in range(1, pattern_length):
        suffix = pattern[suffix_start + 1:]
        suffix_length = len(suffix)
        
        for position in range(pattern_length - suffix_length - 1):
            if (pattern[position:position + suffix_length] == suffix and 
                pattern[position - 1] != pattern[suffix_start]):
                good_suffix_shift[suffix_start] = position
                break
        
        if pattern[:suffix_length] == suffix:
            prefix_suffix_match[suffix_start] = suffix_length
    
    prefix_suffix_match[pattern_length - 1] = pattern_length
    
    return good_suffix_shift, prefix_suffix_match


def perform_search(text, pattern, bad_char_table, good_suffix_shift, prefix_suffix_match):
    text_length = len(text)
    pattern_length = len(pattern)
    current_position = 0
    pattern_found = False
    
    while current_position <= (text_length - pattern_length) and not pattern_found:
        pattern_found = True
        
        for pattern_index in range(pattern_length - 1, -1, -1):
            if pattern[pattern_index] != text[current_position + pattern_index]:
                text_char = text[current_position + pattern_index]
                bad_char_shift = bad_char_table[ord(text_char) - ord('a')]
                
                if good_suffix_shift[pattern_index] != -1:
                    good_suffix_value = pattern_length - 1 - good_suffix_shift[pattern_index]
                else:
                    good_suffix_value = pattern_length - prefix_suffix_match[pattern_index]
                
                current_position += max(bad_char_shift, good_suffix_value)
                pattern_found = False
                break
    
    return pattern_found


def main():
    test_cases = [
        ("abcd", "abcd", True),
        ("zzabcdzz", "abcd", True),
        ("abxabc", "abcd", False),
        ("hello world", "world", True),
        ("pattern matching", "match", True),
        ("boyer moore algorithm", "moore", True),
        ("no match here", "xyz", False),
    ]
    
    print("Boyer-Moore Algorithm Tests:")
    print("-" * 40)
    
    for text, pattern, expected in test_cases:
        text_cleaned = text.replace(" ", "")
        pattern_cleaned = pattern.replace(" ", "")
        result = boyer_moore_search(text_cleaned, pattern_cleaned)
        status = "✓" if result == expected else "✗"
        print(f"{status} boyer_moore('{text}', '{pattern}') = {result}")


if __name__ == "__main__":
    main()