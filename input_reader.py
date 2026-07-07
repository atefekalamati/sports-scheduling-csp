def parse_input(data_tokens) -> dict:
    """
    Input format:
        1. S         ← number of stadiums
        2. Stadium names (space-separated)
        3. D         ← number of available days
        4. H         ← number of time slots per day
        5. N         ← total number of matches
        6..N+5: Team pairs for each match
        N+6: K      ← number of sensitive matches
        N+7..N+6+K: Team pairs for sensitive matches

    Returns:
        dict with keys:
            - stadiums
            - days
            - hours
            - matches
            - sensitive_matches
    """

    idx = 0

    def next_token() -> str:
        nonlocal idx
        token = data_tokens[idx]
        idx += 1
        return token

    S = int(next_token())
    stadiums = [next_token() for _ in range(S)]

    D = int(next_token())
    H = int(next_token())

    N = int(next_token())
    matches = []
    for _ in range(N):
        t1 = next_token()
        t2 = next_token()
        matches.append((t1, t2))

    K = int(next_token())
    sensitive_names = []
    for _ in range(K):
        t1 = next_token()
        t2 = next_token()
        sensitive_names.append(tuple(sorted((t1, t2))))

    sensitive_matches = set()

    for index, match in enumerate(matches):
        normalized_match = tuple(sorted(match))

        if normalized_match in sensitive_names:
            sensitive_matches.add(index)

    return {
        "stadiums": stadiums,
        "days": D,
        "hours": H,
        "matches": matches,
        "sensitive_matches": sensitive_matches,
    }


def normalize_sensitive(team1: str, team2: str) -> tuple:
    return tuple(sorted((team1, team2)))


# wrapper برای سازگاری با main.py
def read_input(filename: str = None):
    with open(filename, "r") as f:
        data = f.read().split()

    parsed = parse_input(data)

    return (
        parsed["stadiums"],
        parsed["days"],
        parsed["hours"],
        parsed["matches"],
        parsed["sensitive_matches"],
    )
