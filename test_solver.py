from solver import solve_csp


matches = [
    ("Team_A", "Team_B"),
    ("Team_C", "Team_D"),
    ("Team_A", "Team_E"),
    ("Team_B", "Team_C")
]

sensitive_matches = {0, 1}

stadiums = ["Azadi", "Takhti"]
days = 3
hours = 2

values = []

for day in range(1, days + 1):
    for hour in range(1, hours + 1):
        for stadium in stadiums:
            values.append((day, hour, stadium))

domains = {}

for match_id in range(len(matches)):
    domains[match_id] = values.copy()

neighbors = {}

for match_id in range(len(matches)):
    neighbors[match_id] = set()

    for other_id in range(len(matches)):
        if match_id != other_id:
            neighbors[match_id].add(other_id)


def is_consistent(variable1, value1, variable2, value2):
    day1, hour1, stadium1 = value1
    day2, hour2, stadium2 = value2

    match1 = matches[variable1]
    match2 = matches[variable2]

    if day1 == day2 and hour1 == hour2 and stadium1 == stadium2:
        return False

    common_team = match1[0] in match2 or match1[1] in match2

    if common_team and day1 == day2:
        return False

    both_sensitive = (
        variable1 in sensitive_matches
        and variable2 in sensitive_matches
    )

    if both_sensitive and day1 == day2:
        return False

    return True


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