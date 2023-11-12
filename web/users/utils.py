import random
import string

code = random.randint(1000, 9999)


def generate_random_code(length=4):
    characters = string.octdigits + string.digits
    return ''.join(random.choice(characters) for
                   _ in range(length))
