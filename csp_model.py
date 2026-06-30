from input_reader import normalize_sensitive

# Global context so that create_neighbors can access sensitive_matches
_SENSITIVE_MATCHES_CONTEXT = set()


# 1. Variable Definition
def build_variables(matches: list) -> list:
    """
    Each match is treated as a CSP variable.

    Returns:
        A list of variable IDs corresponding to match indices:
        [0, 1, 2, ..., N-1]
    """
    return list(range(len(matches)))


# 2. Domain Construction
def build_domains(variables: list, days: int, hours: int, stadiums: list) -> dict:
    """
    Each variable (match) can be assigned any combination of:
        (day, hour, stadium)
    Returns:
        Dictionary mapping each variable to its possible assignments.
    """
    full_domain = [
        (d, h, stadium)
        for d in range(1, days + 1)
        for h in range(1, hours + 1)
        for stadium in stadiums
    ]
    return {var: list(full_domain) for var in variables}


# 3. Constraint Graph Construction (Neighbors)
def build_neighbors(
    variables: list,
    matches: list,
    sensitive_matches: set
) -> dict:
    """
    Two matches are neighbors if:
        - They share at least one team
        - OR both matches are sensitive matches
    """
    neighbors = {var: [] for var in variables}

    for i in variables:
        for j in variables:
            if i == j:
                continue

            teams_i = set(matches[i])
            teams_j = set(matches[j])

            has_common_team = bool(teams_i & teams_j)

            norm_i = normalize_sensitive(*matches[i])
            norm_j = normalize_sensitive(*matches[j])
            both_sensitive = (
                norm_i in sensitive_matches and
                norm_j in sensitive_matches
            )

            # If the matches share a team or both are sensitive,
            # they must be considered neighbors
            if has_common_team or both_sensitive:
                neighbors[i].append(j)

    return neighbors


# 4. Consistency Check
def is_consistent(
    var_i: int,
    val_i: tuple,
    var_j: int,
    val_j: tuple,
    matches: list,
    sensitive_matches: set
) -> bool:
    """
    Constraints:
        1) If two matches share a team, they cannot be scheduled on the same day.
        2) Only one match can occupy a specific (day, hour, stadium).
        3) If both matches are sensitive matches, they cannot be scheduled on the same day.
    """
    day_i, hour_i, stadium_i = val_i
    day_j, hour_j, stadium_j = val_j

    teams_i = set(matches[var_i])
    teams_j = set(matches[var_j])

    # Constraint 1: matches sharing a team must be on different days
    if teams_i & teams_j and day_i == day_j:
        return False

    # Constraint 2: no two matches can use the same stadium at the same time
    if day_i == day_j and hour_i == hour_j and stadium_i == stadium_j:
        return False

    # Constraint 3: sensitive matches must be scheduled on different days
    norm_i = normalize_sensitive(*matches[var_i])
    norm_j = normalize_sensitive(*matches[var_j])
    if norm_i in sensitive_matches and norm_j in sensitive_matches and day_i == day_j:
        return False

    return True


# 5. Wrappers compatible with main.py
def create_domains(matches, stadiums, days, hours):
    variables = build_variables(matches)
    return build_domains(variables, days, hours, stadiums)


def create_neighbors(matches):
    variables = build_variables(matches)
    return build_neighbors(variables, matches, _SENSITIVE_MATCHES_CONTEXT)


def create_consistency_function(matches, sensitive_matches):
    global _SENSITIVE_MATCHES_CONTEXT
    _SENSITIVE_MATCHES_CONTEXT = set(sensitive_matches)

    def consistency_fn(var_i, val_i, var_j, val_j):
        return is_consistent(var_i, val_i, var_j, val_j, matches, sensitive_matches)

    return consistency_fn


def is_feasible(stadiums, days, hours, matches, sensitive_matches):
    """
    Ensures that the total number of matches does not exceed
    the total number of available time slots.
    """
    total_slots = len(stadiums) * days * hours
    return len(matches) <= total_slots
