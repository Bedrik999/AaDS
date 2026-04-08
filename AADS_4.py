def knuth_morris_pratt_search(text, pattern):
    if not pattern:
        return True
    
    prefix_function = build_prefix_function(pattern)
    
    return search_with_prefix_function(text, pattern, prefix_function)


def build_prefix_function(pattern):
    pattern_length = len(pattern)
    prefix_function = [0] * pattern_length
    matched_prefix_length = 0

    for current_position in range(1, pattern_length):
        while matched_prefix_length > 0 and pattern[current_position] != pattern[matched_prefix_length]:
            matched_prefix_length = prefix_function[matched_prefix_length - 1]
    
        if pattern[current_position] == pattern[matched_prefix_length]:
            matched_prefix_length += 1
        
        prefix_function[current_position] = matched_prefix_length

    return prefix_function


def search_with_prefix_function(text, pattern, prefix_function):
    pattern_length = len(pattern)
    matched_chars_count = 0

    for current_char in text:
        while matched_chars_count > 0 and pattern[matched_chars_count] != current_char:
            matched_chars_count = prefix_function[matched_chars_count - 1]
        
        if pattern[matched_chars_count] == current_char:
            matched_chars_count += 1
        
        if matched_chars_count == pattern_length:
            return True

    return False


def run_tests():
    test_cases = [
        ("abcd", "abcd", True, "Полное совпадение"),
        ("zzabcdzz", "abcd", True, "Паттерн в середине"),
        ("abxabc", "abcd", False, "Паттерн не найден"),
        ("", "", True, "Пустые строки"),
        ("hello", "", True, "Пустой паттерн"),
        ("", "a", False, "Пустой текст"),
        ("aabaacaadaabaaba", "aaba", True, "Повторяющиеся символы"),
        ("abcabcabc", "abcabcd", False, "Почти совпадает"),
        ("mississippi", "issip", True, "Классический пример"),
    ]
    
    print("Тестирование алгоритма Кнута-Морриса-Пратта:")
    print("=" * 60)
    
    for text, pattern, expected, description in test_cases:
        result = knuth_morris_pratt_search(text, pattern)
        status = "✓" if result == expected else "✗"

        text_display = f"'{text}'" if text else "''"
        pattern_display = f"'{pattern}'" if pattern else "''"
        
        print(f"{status} {description:25} | Текст: {text_display:15} | "
              f"Паттерн: {pattern_display:10} -> {result}")


def main():

    print("Примеры использования алгоритма КМП:")
    print("-" * 40)
    
    examples = [
        ("abcd", "abcd"),
        ("zzabcdzz", "abcd"),
        ("abxabc", "abcd"),
    ]
    
    for text, pattern in examples:
        result = knuth_morris_pratt_search(text, pattern)
        print(f"kmp('{text}', '{pattern}') = {result}")
    
    print("\n")
    
    run_tests()


if __name__ == "__main__":
    main()