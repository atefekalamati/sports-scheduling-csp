# Intelligent Sports Match Scheduling (CSP)

Python implementation of a weekly sports match scheduler, modeled and solved as a Constraint Satisfaction Problem (CSP). Each match is assigned a (day, time slot, stadium) triple using Backtracking Search with Forward Checking, plus the MRV and LCV heuristics.

**Course:** Artificial Intelligence &nbsp;·&nbsp; **Language:** Python &nbsp;·&nbsp; no external dependencies (standard library only)

## Table of Contents

1. [Overview](#overview)
2. [Usage](#usage)
3. [Input Format](#input-format)
4. [Project Structure](#project-structure)
5. [CSP Formulation](#csp-formulation)
6. [Search Algorithm](#search-algorithm)
7. [Heuristics: MRV and LCV](#heuristics-mrv-and-lcv)
8. [Feasibility Pre-checks](#feasibility-pre-checks)
9. [Results](#results)
10. [Function Reference](#function-reference)
11. [Team](#team)

## Overview

Constraints enforced on every schedule:

- No team plays more than one match on the same day.
- No stadium hosts more than one match at the same time.
- No two sensitive matches are scheduled on the same day.

The goal is any valid complete assignment, not necessarily an optimal one.

## Usage

```bash
python main.py <input_file>
```

Example:

```bash
python main.py tests/sample_bonus.txt
```
```
Team_A Team_B 1 1 Azadi
Team_C Team_D 2 1 Azadi
Team_A Team_C 3 1 Azadi
Team_B Team_D 3 1 Takhti
Team_E Team_F 1 1 Takhti
Backtracks: 0
Time: 0.000506 seconds
```

## Input Format

| Section | Meaning |
|---|---|
| `S` + names | Number of stadiums and their names |
| `D` | Number of days |
| `H` | Time slots per day |
| `N` + `N` lines | Number of matches and each team pair |
| `K` + `K` lines | Number of sensitive matches and each team pair |

## Project Structure

```
.
├── main.py
├── input_reader.py
├── csp_model.py
├── solver.py
├── tests/*.txt
├── Documentation.pdf
└── .gitignore
```

| File | Purpose |
|---|---|
| `main.py` | Entry point; runs the full pipeline |
| `input_reader.py` | Parses the input file into data structures |
| `csp_model.py` | Builds variables, domains, neighborhood, consistency, feasibility |
| `solver.py` | Backtracking Search + Forward Checking + MRV/LCV |
| `tests/*.txt` | Sample input files |
| `Documentation.pdf` | Full project documentation |

## CSP Formulation

| Property | Description | Function |
|---|---|---|
| Variable | Each match | `build_variables` |
| Domain | All (day, time, stadium) triples; size `S×D×H` | `build_domains` |
| Neighborhood | Complete graph — all matches are neighbors | `build_neighbors` |
| Consistency | Team rest, stadium conflict, sensitive matches same day | `is_consistent` |

Simple and correct since all matches share the same initial domain, at the cost of a few unnecessary checks between unrelated matches.

## Search Algorithm

Depth-first Backtracking Search; after each assignment, Forward Checking prunes the domains of unassigned neighbors and triggers an immediate backtrack if any domain becomes empty.

**Flow:** select variable (MRV) → order values (LCV) → check consistency → assign → Forward Check → recurse or undo.

Still exponential in the worst case (CSP is NP-complete), but Forward Checking detects dead ends early and reduces backtracks.

## Heuristics: MRV and LCV

| Heuristic | Description | Function |
|---|---|---|
| MRV | Picks the variable with the smallest remaining domain | `select_unassigned_variable` |
| LCV | Orders values by least constraint on neighbors | `order_values_lcv` |

Both are already active in the example above (`Backtracks: 0`); their effect is more visible on larger, harder inputs.

## Feasibility Pre-checks

Two O(1) checks run before the search starts, in `is_feasible` (called from `main.py`):

- **Capacity:** if matches exceed available slots (`S×D×H`), infeasible.
- **Pigeonhole:** if sensitive matches exceed available days, infeasible.

```bash
python main.py tests/no_solution_capacity.txt
```
```
No Solution
Backtracks: 0
Time: 0.000000 seconds
```

## Results

| Input File | Result |
|---|---|
| `sample_bonus.txt` | Valid solution; `Backtracks: 0` |
| `no_solution_capacity.txt` | `No Solution` (capacity check) |
| `no_solution_sensitive.txt` | `No Solution` (pigeonhole check) |

Output on the official assignment example (2 stadiums, 2 days, 2 time slots, 4 matches) matches one of the valid solutions given in the assignment, confirming the constraint logic is correct.

## Function Reference

| File | Functions | Purpose |
|---|---|---|
| `input_reader.py` | `parse_input`, `read_input`, `normalize_sensitive` | Parse input and build data structures |
| `csp_model.py` | `build_variables`, `build_domains`, `build_neighbors` | Build the CSP model |
| `csp_model.py` | `is_consistent`, `is_feasible` | Constraint and feasibility checks |
| `solver.py` | `select_unassigned_variable`, `order_values_lcv` | MRV / LCV heuristics |
| `solver.py` | `forward_check`, `search_backtracking`, `solve_csp` | Core search |
| `main.py` | `print_solution`, `main` | Output and pipeline entry point |

## Team

| Member | Files | Responsibility |
|---|---|---|
| Team Member 1 | `input_reader.py`, `csp_model.py` | Input parsing, CSP modeling, feasibility checks |
| Team Member 2 | `solver.py`, `main.py` | Search, Forward Checking, MRV/LCV, entry point |
