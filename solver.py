import time


def select_unassigned_variable(matches, domains, assignment):
    unassigned = []

    for match_id in range(len(matches)):
        if match_id not in assignment:
            unassigned.append(match_id)

    if len(unassigned) == 0:
        return None

    best_variable = unassigned[0]

    for variable in unassigned:
        if len(domains[variable]) < len(domains[best_variable]):
            best_variable = variable

    return best_variable


def is_value_consistent(
    variable,
    value,
    assignment,
    is_consistent
):
    for assigned_variable in assignment:
        assigned_value = assignment[assigned_variable]

        if not is_consistent(
            variable,
            value,
            assigned_variable,
            assigned_value
        ):
            return False

    return True


def copy_domains(domains):
    new_domains = {}

    for variable in domains:
        new_domains[variable] = domains[variable].copy()

    return new_domains


def forward_check(
    variable,
    value,
    domains,
    assignment,
    neighbors,
    is_consistent
):
    new_domains = copy_domains(domains)

    for other_variable in neighbors[variable]:
        if other_variable in assignment:
            continue

        allowed_values = []

        for other_value in new_domains[other_variable]:
            if is_consistent(
                variable,
                value,
                other_variable,
                other_value
            ):
                allowed_values.append(other_value)

        new_domains[other_variable] = allowed_values

        if len(new_domains[other_variable]) == 0:
            return None

    return new_domains


def backtracking_search(
    matches,
    domains,
    neighbors,
    assignment,
    is_consistent,
    backtrack_counter
):
    if len(assignment) == len(matches):
        return assignment.copy()

    variable = select_unassigned_variable(
    matches,
    domains,
    assignment
    )

    for value in domains[variable]:
        if is_value_consistent(
            variable,
            value,
            assignment,
            is_consistent
        ):
            assignment[variable] = value

            new_domains = forward_check(
                variable,
                value,
                domains,
                assignment,
                neighbors,
                is_consistent
            )

            if new_domains is not None:
                result = backtracking_search(
                    matches,
                    new_domains,
                    neighbors,
                    assignment,
                    is_consistent,
                    backtrack_counter
                )

                if result is not None:
                    return result

            del assignment[variable]
            backtrack_counter[0] += 1

    return None


def solve_csp(
    matches,
    domains,
    neighbors,
    is_consistent
):
    assignment = {}
    backtrack_counter = [0]

    start_time = time.perf_counter()

    result = backtracking_search(
        matches,
        domains,
        neighbors,
        assignment,
        is_consistent,
        backtrack_counter
    )

    elapsed_time = time.perf_counter() - start_time

    return result, backtrack_counter[0], elapsed_time