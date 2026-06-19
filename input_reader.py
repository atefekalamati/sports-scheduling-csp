def read_input(filename):
    with open(filename, "r") as file:
        stadium_count = int(file.readline().strip())

        stadiums = file.readline().split()

        days = int(file.readline().strip())
        hours = int(file.readline().strip())

        match_count = int(file.readline().strip())

        matches = []

        for _ in range(match_count):
            team1, team2 = file.readline().split()
            matches.append((team1, team2))

        sensitive_count = int(file.readline().strip())

        sensitive_names = []

        for _ in range(sensitive_count):
            team1, team2 = file.readline().split()
            sensitive_names.append(tuple(sorted((team1, team2))))

    sensitive_matches = set()

    for index, match in enumerate(matches):
        normalized_match = tuple(sorted(match))

        if normalized_match in sensitive_names:
            sensitive_matches.add(index)

    return stadiums, days, hours, matches, sensitive_matches