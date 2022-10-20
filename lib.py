# Year 8 Math thingo (much harder than Year 9 for some reason)
# Lodinu Kalugalage

import math


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

TRI_LENGTH_AB = 0
TRI_LENGTH_AC = 1
TRI_LENGTH_BC = 2

TRI_ANGLE_BAC = 0
TRI_ANGLE_ABC = 1
TRI_ANGLE_ACB = 2

# triangle shape
#
#          A
#         /\
#        /  \
#       /    \ AC
# AB   /      \
#     /        \
#    /          \
#    B-----------C
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
        return "The longest side is longer than the sum of the other two sides"
    return True


def validate_triangle_angles(angles):
    # Check if the angles are valid
    if TRI_NAN in angles:
        return True
    s = sum(filter(lambda x: x != TRI_NAN, angles))
    nan_count = angles.count(TRI_NAN)
    if nan_count == 0:
        if s != 180:
            return "The sum of the angles is not 180"
    if s > 180:
        return "The sum of the angles is greater than 180"
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
    rvalue = tri.angles.copy()
    nan_locations = []
    for i in range(3):
        if rvalue[i] == TRI_NAN:
            nan_locations.append(i)
    nan_count = len(nan_locations)
    if nan_count == 0:
        pass
    elif nan_count == 1:
        rvalue[nan_locations[0]] = 180 - \
            sum(filter(lambda x: x != TRI_NAN, rvalue))
    elif len(list(filter(lambda x: x != TRI_NAN, tri.lengths))) == 3:
        # (a^2 + c^2 - b^2) / 2ac
        cos_1 = ((float(tri.lengths[TRI_LENGTH_AC]) ** 2) +
                 (float(tri.lengths[TRI_LENGTH_AB]) ** 2) - (float(tri.lengths[TRI_LENGTH_BC]) ** 2)) \
            / (2 * float(tri.lengths[TRI_LENGTH_AC]) * float(tri.lengths[TRI_LENGTH_AB]))

        # (b^2 + c^2 - a^2) / 2bc
        cos_2 = ((float(tri.lengths[TRI_LENGTH_BC]) ** 2) +
                 (float(tri.lengths[TRI_LENGTH_AB]) ** 2) - (float(tri.lengths[TRI_LENGTH_AC]) ** 2)) \
            / (2 * float(tri.lengths[TRI_LENGTH_BC]) * float(tri.lengths[TRI_LENGTH_AB]))

        # (a^2 + b^2 - c^2) / 2ab
        cos_3 = (float(tri.lengths[TRI_LENGTH_AC] ** 2) +
                 (float(tri.lengths[TRI_LENGTH_BC]) ** 2) - (float(tri.lengths[TRI_LENGTH_AB]) ** 2)) \
            / (2 * float(tri.lengths[TRI_LENGTH_AC]) * float(tri.lengths[TRI_LENGTH_BC]))

        rvalue = [round(math.degrees(math.acos(cos_1))), round(math.degrees(
            math.acos(cos_2))), round(math.degrees(math.acos(cos_3)))]

    tri.angles = rvalue
    return


def __sin_rule(C, D):
    if C == TRI_NAN or D == TRI_NAN:
        return (False, TRI_NAN)
    return (True, D / (math.sin(math.radians(C))))


def compute_unknown_side(tri: Triangle):
    rvalue = tri.lengths.copy()
    nan_locations = []
    for i in range(3):
        if rvalue[i] == TRI_NAN:
            nan_locations.append(i)
    nan_count = len(nan_locations)
    if nan_count == 0:
        return

    # use the cosine rules to get side lengths from angles
    # using this because we need angles
    compute_unknown_angle(tri)
    sine_rule = {TRI_ANGLE_BAC: __sin_rule(
        tri.angles[TRI_ANGLE_BAC], tri.lengths[TRI_LENGTH_BC]),
        TRI_ANGLE_ABC: __sin_rule(
        tri.angles[TRI_ANGLE_ABC], tri.lengths[TRI_LENGTH_AC]),
        TRI_ANGLE_ACB: __sin_rule(
        tri.angles[TRI_ANGLE_ACB], tri.lengths[TRI_LENGTH_AB])}
    # get the first occurence with a valid value
    sine_rule_value = TRI_NAN
    for i in range(3):
        if sine_rule[i][0]:
            sine_rule_value = sine_rule[i][1]
            break
    if sine_rule_value == TRI_NAN:
        return

    for i in range(3):
        if rvalue[i] == TRI_NAN:
            rvalue[i] = int(sine_rule_value *
                            (math.sin(math.radians(tri.angles[i]))))

    tri.lengths = rvalue
    return


if __name__ == "__main__":
    # t = get_triangles()
    tri_1 = Triangle([6, TRI_NAN, 6], [60, TRI_NAN, TRI_NAN])
    # tri_2 = Triangle(t[2], t[3])
    compute_unknown_side(tri_1)
    print(tri_1)
