from input_reader import read_input
from csp_model import (
    create_domains,
    create_neighbors,
    create_consistency_function,
    is_feasible
)


stadiums, days, hours, matches, sensitive_matches = read_input(
    "tests/sample_bonus.txt"
)

print("Feasible:", is_feasible(stadiums, days, hours, matches, sensitive_matches))

domains = create_domains(matches, stadiums, days, hours)
neighbors = create_neighbors(matches)
is_consistent = create_consistency_function(matches, sensitive_matches)

print("Domain size for match 0:", len(domains[0]))
print("Neighbors of match 0:", neighbors[0])

value1 = (1, 1, "Azadi")
value2 = (1, 1, "Azadi")

print("Same stadium same time:", is_consistent(0, value1, 1, value2))

value3 = (1, 1, "Azadi")
value4 = (1, 2, "Takhti")

print("Sensitive same day:", is_consistent(0, value3, 1, value4))

value5 = (1, 1, "Azadi")
value6 = (2, 1, "Azadi")

print("Sensitive different day:", is_consistent(0, value5, 1, value6))