from test_solver import matches, domains, neighbors, is_consistent
from solver import solve_csp


solution, backtracks, elapsed_time = solve_csp(
    matches,
    domains,
    neighbors,
    is_consistent
)

if solution is None:
    print("No Solution")
else:
    for match_id in range(len(matches)):
        team1, team2 = matches[match_id]
        day, hour, stadium = solution[match_id]
        print(team1, team2, day, hour, stadium)

print("Backtracks:", backtracks)
print("Time:", format(elapsed_time, ".6f"), "seconds")