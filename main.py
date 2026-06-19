import sys

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


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        return

    filename = sys.argv[1]

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