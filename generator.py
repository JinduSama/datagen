"""
Generator module for synthetic German identification numbers.

This module provides functions to generate valid German ID numbers and tax IDs
with correct check digits for testing and development purposes.
"""

import random


def generate_german_id() -> str:
    """
    Generate a synthetic German ID (Personalausweis) number with valid check digit.

    The German ID number consists of 9 alphanumeric characters followed by a
    check digit calculated using the 7-3-1 weighting method.

    Format: XXXXXXXXX-C
    - X: Alphanumeric character (0-9, C, F, G, H, J, K, L, M, N, P, R, T, V, W, X, Y, Z)
    - C: Check digit (0-9)

    Returns:
        str: A 10-character German ID number with valid check digit.

    Example:
        >>> id_number = generate_german_id()
        >>> len(id_number)
        10
    """
    # Valid characters for German ID (excludes vowels and ambiguous characters)
    valid_chars = "0123456789CFGHJKLMNPRTVWXYZ"
    id_base = "".join(random.choice(valid_chars) for _ in range(9))

    # Calculate check digit using 7-3-1 weighting pattern
    weights = [7, 3, 1, 7, 3, 1, 7, 3, 1]
    total = 0

    for i, char in enumerate(id_base):
        # Convert character to numeric value (0-9 for digits, A=10, B=11, ..., Z=35 for letters)
        value = int(char) if char.isdigit() else ord(char) - ord("A") + 10
        total += value * weights[i]

    check_digit = total % 10
    return f"{id_base}{check_digit}"


def generate_german_tax_id() -> str:
    """
    Generate a synthetic German Tax ID with valid check digit.

    The German Tax ID (Steuer-Identifikationsnummer) consists of 11 digits
    that follow strict structural rules and include a check digit calculated
    using the ISO 7064, MOD 11, 10 algorithm.

    Structural Rules:
        - Total length: 11 digits
        - First digit: Must be 1-9 (cannot be 0)
        - Digits 1-10: Exactly one digit must appear 2 or 3 times
        - Other digits: Appear 0 or 1 time
        - If a digit appears 3 times, they cannot be consecutive
        - Digit 11: Check digit

    Returns:
        str: An 11-digit German Tax ID with valid check digit.

    Example:
        >>> tax_id = generate_german_tax_id()
        >>> len(tax_id)
        11
        >>> tax_id[0] != '0'
        True
    """
    while True:
        # Generate base digits with required frequency rules
        if random.random() < 0.9:  # 90% probability: one digit appears twice
            base_digits = random.sample(range(10), 9)
            duplicate_digit = random.choice(base_digits)
            id_digits = base_digits + [duplicate_digit]
        else:  # 10% probability: one digit appears three times
            base_digits = random.sample(range(10), 8)
            triplicate_digit = random.choice(base_digits)
            id_digits = base_digits + [triplicate_digit, triplicate_digit]

        random.shuffle(id_digits)

        # Validate: first digit cannot be 0
        if id_digits[0] == 0:
            continue

        # Validate: no three consecutive identical digits
        has_consecutive_triplet = any(
            id_digits[i] == id_digits[i + 1] == id_digits[i + 2] for i in range(len(id_digits) - 2)
        )
        if has_consecutive_triplet:
            continue

        # Calculate check digit using ISO 7064, MOD 11, 10 algorithm
        remainder = 10
        for digit in id_digits:
            sum_value = (digit + remainder) % 10
            if sum_value == 0:
                sum_value = 10
            remainder = (sum_value * 2) % 11

        check_digit = 11 - remainder
        if check_digit == 10:
            check_digit = 0

        return "".join(map(str, id_digits)) + str(check_digit)


if __name__ == "__main__":
    # Quick test
    print(f"ID: {generate_german_id()}")
    print(f"Tax ID: {generate_german_tax_id()}")
