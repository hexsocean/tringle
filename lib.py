# Year 8 Math thingo (much harder than Year 9 for some reason)
# Lodinu Kalugalage
# ethan xu drool

from symtable import Symbol


INPUT_QUERIES = [
    "Enter lengths AB, AC and BC in that order, separated by spaces: ",
    "Enter angles BAC, ABC and ACB in that order, separated by spaces: ",
    "Enter lengths PQ, PR and QR in that order, separated by spaces: ",
    "Enter angles QPR, PQR and PRQ in that order, separated by spaces: ",
]

IQ_TRI_1_LEN = 0
IQ_TRI_1_ANG = 1
IQ_TRI_2_LEN = 2
IQ_TRI_2_ANG = 3

TRI_NAN = "NA"

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


def err(error):
    print(f"ERROR: {error}")


def input_base(q, validate, ealt="Unknown Error"):
    # Get input from the user
    while True:
        try:
            inp = input(q)
            inp = inp.split()
            inp = [TRI_NAN if i == TRI_NAN else int(i) for i in inp]
            if len(inp) != 3:
                err("Three values are required.")
                continue
            res = validate(inp)
            if res == True:
                return inp
            else:
                if res == False:
                    res = ealt
                err(f"Invalid input: {res}")
        except ValueError:
            err("Invalid input")


def validate_triangle_lengths(lengths):
    # Check if the lengths are valid
    if TRI_NAN in lengths:
        return True
    longest_side = max(lengths)
    if longest_side >= sum(lengths) - longest_side:
        return False
    return True


def validate_triangle_angles(angles):
    # Check if the angles are valid
    if TRI_NAN in angles:
        return True
    if sum(angles) != 180:
        return False
    return True


def get_triangles():
    # Get the triangle from the user
    tri_1_lens = input_base(
        INPUT_QUERIES[IQ_TRI_1_LEN],
        validate_triangle_lengths, "Those lengths will not result in a valid triangle, try again.")
    tri_1_angs = input_base(
        INPUT_QUERIES[IQ_TRI_1_ANG],
        validate_triangle_angles, "Those angles will not result in a valid triangle, try again.")

    tri_2_lens = input_base(
        INPUT_QUERIES[IQ_TRI_2_LEN],
        validate_triangle_lengths, "Those lengths will not result in a valid triangle, try again.")
    tri_2_angs = input_base(
        INPUT_QUERIES[IQ_TRI_2_ANG],
        validate_triangle_angles, "Those angles will not result in a valid triangle, try again.")

    return [tri_1_lens, tri_1_angs, tri_2_lens, tri_2_angs]


class Triangle:
    # Triangle class
    def __init__(self, lengths, angles):
        self.lengths = lengths
        self.angles = angles

    def __str__(self):
        return f"<triangle;Lengths: {self.lengths}, Angles: {self.angles}>"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.lengths == other.lengths and self.angles == other.angles

    def __ne__(self, other):
        return not self.__eq__(other)


def compute_unknown_angle(tri: Triangle):
    nan_count = tri.angles.count(TRI_NAN)
    if nan_count == 0:
        return tri.angles.copy()
    elif nan_count == 1:
        rvalue = tri.angles.copy()
        sum_wo_nan = sum([i for i in tri.angles if i != TRI_NAN])
        rvalue[rvalue.index(TRI_NAN)] = 180 - sum_wo_nan
        return rvalue


if __name__ == "__main__":
    print(get_triangles())
