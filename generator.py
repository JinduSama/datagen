import random

# Constants for German ID generation
GERMAN_ID_CHARS = "0123456789CFGHJKLMNPRTVWXYZ"
GERMAN_ID_WEIGHTS = [7, 3, 1, 7, 3, 1, 7, 3, 1]
GERMAN_ID_LENGTH = 9

# Constants for German Tax ID generation
TAX_ID_DUPLICATE_PROBABILITY = 0.9
MODULUS_11 = 11
MODULUS_10 = 10


def _char_to_value(char: str) -> int:
    """
    Convert a character to its numeric value for German ID check digit calculation.
    
    Args:
        char: A single character (digit or letter)
        
    Returns:
        Numeric value (0-9 for digits, 10-35 for letters A-Z)
    """
    if char.isdigit():
        return int(char)
    else:
        # Alphanumeric values: A=10, B=11, C=12, ... Z=35
        return ord(char) - ord('A') + 10


def _calculate_german_id_check_digit(id_base: str) -> int:
    """
    Calculate the check digit for a German ID using the 7-3-1 weighting method.
    
    Args:
        id_base: The base ID string (9 characters)
        
    Returns:
        Check digit (0-9)
    """
    total = 0
    for i, char in enumerate(id_base):
        val = _char_to_value(char)
        total += val * GERMAN_ID_WEIGHTS[i]
    
    return total % MODULUS_10


def generate_german_id() -> str:
    """
    Generates a German ID (Personalausweis) number with a valid check digit.
    The format is 9 alphanumeric characters followed by 1 check digit.
    Allowed characters: 0-9 and C, F, G, H, J, K, L, M, N, P, Q, R, T, V, W, X, Y, Z.
    
    Returns:
        A 10-character German ID string with valid check digit
    """
    id_base = "".join(random.choice(GERMAN_ID_CHARS) for _ in range(GERMAN_ID_LENGTH))
    check_digit = _calculate_german_id_check_digit(id_base)
    return f"{id_base}{check_digit}"

def generate_german_tax_id() -> str:
    """
    Generates a German Tax ID (Steuer-Identifikationsnummer) with a valid check digit.
    11 digits total.
    - First digit 1-9.
    - Digits 1-10: One digit appears 2 or 3 times, others 0 or 1 time.
    - Digit 11: Check digit.
    
    Returns:
        An 11-digit German Tax ID string with valid check digit
    """
    while True:
        # Decide if one digit appears 2 or 3 times
        if random.random() < TAX_ID_DUPLICATE_PROBABILITY:  # 90% chance for 2 times
            # 9 unique digits, one repeated
            base_digits = random.sample(range(10), 9)
            duplicate_digit = random.choice(base_digits)
            id_digits = base_digits + [duplicate_digit]
        else:
            # 8 unique digits, one repeated 3 times
            base_digits = random.sample(range(10), 8)
            triplicate_digit = random.choice(base_digits)
            id_digits = base_digits + [triplicate_digit, triplicate_digit]
            
        random.shuffle(id_digits)
        
        # First digit cannot be 0
        if id_digits[0] == 0:
            continue
            
        # Rule: If a digit appears 3 times, no three in a row
        has_three_in_row = False
        for i in range(len(id_digits) - 2):
            if id_digits[i] == id_digits[i+1] == id_digits[i+2]:
                has_three_in_row = True
                break
        if has_three_in_row:
            continue

        # Calculate check digit (ISO 7064, MOD 11, 10)
        remainder = MODULUS_10
        for d in id_digits:
            sum_val = (d + remainder) % MODULUS_10
            if sum_val == 0:
                sum_val = MODULUS_10
            remainder = (sum_val * 2) % MODULUS_11
            
        check_digit = MODULUS_11 - remainder
        if check_digit == MODULUS_10:
            check_digit = 0
            
        return "".join(map(str, id_digits)) + str(check_digit)

if __name__ == "__main__":
    # Quick test
    print(f"ID: {generate_german_id()}")
    print(f"Tax ID: {generate_german_tax_id()}")
