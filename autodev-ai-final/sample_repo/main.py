from .utils import to_number

def add_numbers(a, b):
    return to_number(a) + to_number(b)

if __name__ == "__main__":
    print(add_numbers(2, "3"))
