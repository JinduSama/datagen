import random
import string

def generate_german_id():
    """
    Generates a German ID (Personalausweis) number with a valid check digit.
    The format is 9 alphanumeric characters followed by 1 check digit.
    Allowed characters: 0-9 and C, F, G, H, J, K, L, M, N, P, Q, R, T, V, W, X, Y, Z.
    """
    chars = "0123456789CFGHJKLMNPRTVWXYZ"
    id_base = "".join(random.choice(chars) for _ in range(9))
    
    weights = [7, 3, 1, 7, 3, 1, 7, 3, 1]
    total = 0
    
    for i, char in enumerate(id_base):
        if char.isdigit():
            val = int(char)
        else:
            # Alphanumeric values: A=10, B=11, ... but some are excluded.
            # The standard mapping for German ID is:
            # 0-9 = 0-9
            # A=10, B=11, C=12, D=13, E=14, F=15, G=16, H=17, I=18, J=19, K=20, L=21, M=22, N=23, O=24, P=25, Q=26, R=27, S=28, T=29, U=30, V=31, W=32, X=33, Y=34, Z=35
            val = ord(char) - ord('A') + 10
            
        total += val * weights[i]
    
    check_digit = total % 10
    return f"{id_base}{check_digit}"

def generate_german_tax_id():
    """
    Generates a German Tax ID (Steuer-Identifikationsnummer) with a valid check digit.
    11 digits total.
    - First digit 1-9.
    - Digits 1-10: One digit appears 2 or 3 times, others 0 or 1 time.
    - Digit 11: Check digit.
    """
    while True:
        # Decide if one digit appears 2 or 3 times
        if random.random() < 0.9: # 90% chance for 2 times
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
        remainder = 10
        for d in id_digits:
            sum_val = (d + remainder) % 10
            if sum_val == 0:
                sum_val = 10
            remainder = (sum_val * 2) % 11
            
        check_digit = 11 - remainder
        if check_digit == 10:
            check_digit = 0
            
        return "".join(map(str, id_digits)) + str(check_digit)

if __name__ == "__main__":
    # Quick test
    print(f"ID: {generate_german_id()}")
    print(f"Tax ID: {generate_german_tax_id()}")
