INPUT_QUERIES = [
    "Enter lengths AB, AC and BC in that order, separated by spaces: 5 5 5",
    "Enter angles BAC, ABC and ACB in that order, separated by spaces: 60 60 60",
    "Enter lengths PQ, PR and QR in that order, separated by spaces: 5 5 5",
    "Enter angles QPR, PQR and PRQ in that order, separated by spaces: 60 60 60",
]


# triangle shape
#
#    A
#    / \\
#    /   \\
#    /     \\ AC
# AB /       \\
#    /         \\
#    /           \\
#    B-------------C
#        BC


class Triangle():
    def __init__(self, lengths, angles):
        self.lengths = lengths
        self.angles = angles

    def __str__(self):
        return f"Triangle with lengths {self.lengths} and angles {self.angles}"

    def __repr__(self):
        return f"Triangle({self.lengths}, {self.angles})"


def validate_triangle(lengths, angles):
    # Check if the lengths and angles are valid
    longest_side = max(lengths)
    if longest_side >= sum(lengths) - longest_side:
        return False
    if any(angle <= 0 for angle in angles):
        return False
    if any(angle >= 180 for angle in angles):
        return False
    return True


if __name__ == "__main__":
    print(validate_triangle([5, 5, 5], [60, 60, 50]))
