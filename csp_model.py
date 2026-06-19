def create_domains(matches, stadiums, days, hours):
    values = []

    for day in range(1, days + 1):
        for hour in range(1, hours + 1):
            for stadium in stadiums:
                values.append((day, hour, stadium))

    domains = {}

    for match_id in range(len(matches)):
        domains[match_id] = values.copy()

    return domains


def create_neighbors(matches):
    neighbors = {}

    for match_id in range(len(matches)):
        neighbors[match_id] = set()

        for other_id in range(len(matches)):
            if match_id != other_id:
                neighbors[match_id].add(other_id)

    return neighbors


def has_common_team(match1, match2):
    return match1[0] in match2 or match1[1] in match2


def create_consistency_function(matches, sensitive_matches):
    def is_consistent(variable1, value1, variable2, value2):
        day1, hour1, stadium1 = value1
        day2, hour2, stadium2 = value2

        match1 = matches[variable1]
        match2 = matches[variable2]

        if day1 == day2 and hour1 == hour2 and stadium1 == stadium2:
            return False

        if has_common_team(match1, match2) and day1 == day2:
            return False

        both_sensitive = (
            variable1 in sensitive_matches
            and variable2 in sensitive_matches
        )

        if both_sensitive and day1 == day2:
            return False

        return True

    return is_consistent


def is_feasible(stadiums, days, hours, matches, sensitive_matches):
    total_slots = len(stadiums) * days * hours

    if len(matches) > total_slots:
        return False

    if len(sensitive_matches) > days:
        return False

    return True