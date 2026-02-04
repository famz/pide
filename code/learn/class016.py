# Lesson 16: Text Processing Toolkit
# Create useful text manipulation functions

def reverse_text(text):
    """Reverse a string"""
    return text[::-1]

def count_words(text):
    """Count words in a string"""
    return len(text.split())

def is_palindrome(text):
    """Check if text is a palindrome"""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

def encrypt_caesar(text, shift=3):
    """Simple Caesar cipher encryption"""
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char
    return result

def word_frequency(text):
    """Count frequency of each word"""
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

# Test the functions
test_text = "Hello World Hello"
print(f"Original: {test_text}")
print(f"Reversed: {reverse_text(test_text)}")
print(f"Word count: {count_words(test_text)}")
print(f"Is palindrome: {is_palindrome('racecar')}")
print(f"Encrypted (shift 3): {encrypt_caesar('Hello', 3)}")
print(f"Word frequency: {word_frequency(test_text)}")

# Challenge: Create a function to find the longest word in a sentence
