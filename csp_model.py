# 1. Variable Definition
def build_variables(matches: list) -> list:
    """
    Returns:
        A list of variable IDs corresponding to match indices:
        [0, 1, 2, ..., N-1]
    """
    return list(range(len(matches)))


# 2. Domain Construction
def build_domains(variables: list, days: int, hours: int, stadiums: list) -> dict:
    full_domain = [
        (d, h, stadium)
        for d in range(1, days + 1)
        for h in range(1, hours + 1)
        for stadium in stadiums
    ]
    return {var: list(full_domain) for var in variables}


# 3. Constraint Graph Construction (Neighbors)
def build_neighbors(variables: list, matches: list) -> dict:
    """
    Two matches are neighbors if:
        1) They share at least one team 
        2) They could compete for the same (day, hour, stadium) slot
        3) Both matches are sensitive matches
    """
    return {i: [j for j in variables if j != i] for i in variables}


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

    sensitive_matches is a set of MATCH INDICES, exactly as returned by
    input_reader.read_input() 
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
    if var_i in sensitive_matches and var_j in sensitive_matches and day_i == day_j:
        return False

    return True


# 5. Wrappers compatible with main.py
def create_domains(matches, stadiums, days, hours):
    variables = build_variables(matches)
    return build_domains(variables, days, hours, stadiums)


def create_neighbors(matches):
    variables = build_variables(matches)
    return build_neighbors(variables, matches)


def create_consistency_function(matches, sensitive_matches):
    def consistency_fn(var_i, val_i, var_j, val_j):
        return is_consistent(var_i, val_i, var_j, val_j, matches, sensitive_matches)

    return consistency_fn


def is_feasible(stadiums, days, hours, matches, sensitive_matches):
    """
    Two necessary pre-checks:
        1) Capacity: total matches must not exceed total available slots
           (S x D x H).
        2) Pigeonhole: number of sensitive matches (K) must not exceed the
           number of available days (D), since at most one sensitive
           match can be hosted per day.
    """
    total_slots = len(stadiums) * days * hours
    if len(matches) > total_slots:
        return False

    if len(sensitive_matches) > days:
        return False

    return True
