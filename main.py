import sys
import tempfile

from input_reader import read_input
from csp_model import (
    create_domains,
    create_neighbors,
    create_consistency_function,
    is_feasible
)
from solver import solve_csp


def print_solution(matches, solution, backtracks, elapsed_time):
    if solution is None:
        print("No Solution")
    else:
        for match_id in range(len(matches)):
            team1, team2 = matches[match_id]
            day, hour, stadium = solution[match_id]
            print(team1, team2, day, hour, stadium)

    print("Backtracks:", backtracks)
    print("Time:", format(elapsed_time, ".6f"), "seconds")


def read_from_terminal():
    lines = []

    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        encoding="utf-8"
    )

    for line in lines:
        temp_file.write(line + "\n")

    temp_file.close()

    return temp_file.name


def main():
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        filename = read_from_terminal()

    stadiums, days, hours, matches, sensitive_matches = read_input(filename)

    if not is_feasible(stadiums, days, hours, matches, sensitive_matches):
        print("No Solution")
        print("Backtracks:", 0)
        print("Time:", "0.000000 seconds")
        return

    domains = create_domains(matches, stadiums, days, hours)
    neighbors = create_neighbors(matches)
    is_consistent = create_consistency_function(matches, sensitive_matches)

    solution, backtracks, elapsed_time = solve_csp(
        matches,
        domains,
        neighbors,
        is_consistent
    )

    print_solution(matches, solution, backtracks, elapsed_time)


if __name__ == "__main__":
    main()