from input_reader import read_input


stadiums, days, hours, matches, sensitive_matches = read_input(
    "tests/sample_bonus.txt"
)

print("Stadiums:", stadiums)
print("Days:", days)
print("Hours:", hours)
print("Matches:", matches)
print("Sensitive matches:", sensitive_matches)