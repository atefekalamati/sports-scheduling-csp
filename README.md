# Intelligent Sports Match Scheduling (CSP)

A Python implementation of an intelligent weekly sports match scheduler, formulated and solved as a Constraint Satisfaction Problem (CSP). The system assigns a (day, time slot, stadium) triple to every match using Backtracking Search with Forward Checking, extended with the MRV and LCV heuristics.

**Course:** Artificial Intelligence
**Language:** Python

## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Usage](#usage)
4. [Input Format](#input-format)
5. [Project Structure](#project-structure)
6. [CSP Formulation: Variables, Domains, and Neighborhood](#csp-formulation-variables-domains-and-neighborhood)
7. [Search Algorithm: Backtracking with Forward Checking](#search-algorithm-backtracking-with-forward-checking)
8. [Heuristics: MRV and LCV](#heuristics-mrv-and-lcv)
9. [Feasibility Pre-checks](#feasibility-pre-checks)
10. [Results](#results)
11. [Function Reference](#function-reference)
12. [Team and Responsibilities](#team-and-responsibilities)

## Overview

Each match must be assigned a triple of (day, time slot, stadium) such that:

- No team plays more than one match on the same day.
- No stadium hosts more than one match at the same time.
- No two sensitive matches (bonus constraint) are scheduled on the same day.

The problem is modeled as a CSP and solved with Backtracking Search combined with Forward Checking. As a bonus component, the MRV (Minimum Remaining Values) and LCV (Least Constraining Value) heuristics are used to reduce the number of backtracks.

| | |
|---|---|
| **Input** | A text file specifying the number of stadiums, days, time slots, the list of matches, and the list of sensitive matches |
| **Output** | A (day, time slot, stadium) assignment for every match, or `No Solution`, together with the backtrack count and execution time |
| **Computational goal** | Find one complete assignment that satisfies all constraints (not necessarily an optimal one) |

The program takes no arguments beyond the input file path; it performs reading, modeling, and solving in a single run.

## Requirements

- Python 3.x
- No external dependencies. All algorithms — Backtracking Search, Forward Checking, MRV, and LCV — are implemented from scratch using only the Python standard library.

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

The input file is read line by line; each number or name is treated as an independent token.

| Section | Meaning |
|---|---|
| `S` + stadium names | Number of stadiums and the name of each |
| `D` | Number of available days |
| `H` | Number of time slots per day |
| `N` + `N` lines | Number of matches, followed by the team pair for each match (`Team1 Team2`) |
| `K` + `K` lines | Number of sensitive matches, followed by the team pair for each (team order does not matter) |

## Project Structure

```
.
├── main.py
├── input_reader.py
├── csp_model.py
├── solver.py
├── tests/
│   └── *.txt
├── Documentation.pdf
├── .gitignore
└── README.md
```

| File | Purpose |
|---|---|
| `main.py` | Reads the input file path from the command line and runs the complete solving pipeline |
| `input_reader.py` | Reads the input file and converts it into internal data structures (stadiums, days, time slots, matches, sensitive matches) |
| `csp_model.py` | Builds the variables, domains, neighborhood graph, consistency function, and feasibility check |
| `solver.py` | Implements Forward Checking and Backtracking Search, with the MRV/LCV heuristics |
| `tests/*.txt` | Sample input files used to run experiments |
| `Documentation.pdf` | Full project documentation (problem description, CSP modeling, algorithms, results) |
| `.gitignore` | Git ignore rules |

`main.py` is the entry point of the program. The codebase is split into separate modules to improve readability and maintainability.

## CSP Formulation: Variables, Domains, and Neighborhood

The problem is decomposed into three components: variables, domains, and constraints. Each match is a variable, and the initial domain of every variable is the full set of (day, time slot, stadium) triples. Since all matches share the same initial domain, every pair of matches is treated as a neighbor.

| Property | Description | Function |
|---|---|---|
| Variable | Each match (index `0` to `N-1`) | `build_variables` |
| Domain | All (day, time slot, stadium) triples; size = `S × D × H` | `build_domains` |
| Neighborhood | Complete graph — every two matches are neighbors | `build_neighbors` |
| Consistency function | Checks three rules: team rest, stadium conflict, and sensitive matches on the same day | `is_consistent` |

**Advantage:** Simple to implement and provably correct, since the initial domain is identical for all matches.

**Limitation:** Some additional, harmless consistency checks are performed between matches that have no real relationship to each other.

## Search Algorithm: Backtracking with Forward Checking

The core of the solver is a depth-first search over the tree of partial assignments. After every assignment, the domains of the not-yet-assigned matches are immediately pruned (Forward Checking); if any of these domains becomes empty, the search backtracks immediately.

| Property | Description |
|---|---|
| Algorithm | Backtracking Search + Forward Checking |
| Base case | The number of assigned matches equals the total number of matches (`backtracking_search`) |
| Backtrack condition | The domain of an unassigned neighbor becomes empty after `check_forward` |
| Backtrack counter | Incremented each time a value is assigned but does not lead to a complete solution and is later undone |
| Advantage | Early detection of dead ends; a noticeable reduction in backtracks compared to plain Backtracking |
| Limitation | Still exponential in the worst theoretical case, since CSP is NP-complete in general |

**Execution flow:** select the next variable (MRV) → order the domain values (LCV) → check consistency with the current assignment → assign temporarily → run Forward Checking on the neighbors → recurse, or undo the assignment.

## Heuristics: MRV and LCV

As a bonus component, two standard CSP heuristics were added to the solver to reduce the number of backtracks.

| Heuristic | Description | Function(s) |
|---|---|---|
| MRV (Minimum Remaining Values) | Selects the variable with the smallest remaining domain | `select_unassigned_variable` |
| LCV (Least Constraining Value) | Prioritizes the value that removes the fewest options from neighboring variables | `count_removed_values`, `order_values_lcv` |

**MRV advantage:** Harder variables are examined earlier, so a potential failure is discovered closer to the root of the search tree.

**LCV advantage:** The domains of future variables stay as open as possible, increasing the likelihood of finding a solution without backtracking.

Both heuristics were already active in the example run shown above (`Backtracks: 0`). Their benefit over the non-heuristic version becomes more evident on larger and harder inputs, where the difference in reported backtrack counts is more pronounced.

## Feasibility Pre-checks

In addition to the two main constraints (team rest and stadium conflict), a third rule handles sensitive matches. Two simple O(1) pre-checks are also performed before the search starts, so that clearly infeasible inputs are reported as `No Solution` immediately, without running the search.

| Check | Description | Function |
|---|---|---|
| Sensitive match constraint | No two sensitive matches may be scheduled on the same day | `is_consistent` |
| Total capacity check | If the number of matches exceeds the total number of available slots (`S × D × H`), the problem is infeasible | `is_feasible` |
| Pigeonhole check | If the number of sensitive matches exceeds the number of available days, no schedule can satisfy the same-day exclusion constraint | `is_feasible` |

`is_feasible` is called from `main.py` before any search begins.

Examples:

```bash
python main.py tests/no_solution_capacity.txt
```
```
No Solution
Backtracks: 0
Time: 0.000000 seconds
```

```bash
python main.py tests/no_solution_sensitive.txt
```
```
No Solution
Backtracks: 0
Time: 0.000000 seconds
```

## Results

| Input File | Result |
|---|---|
| `sample_bonus.txt` | Valid solution found; `Backtracks: 0` |
| `no_solution_capacity.txt` | `No Solution`, reported immediately by the total capacity check |
| `no_solution_sensitive.txt` | `No Solution`, reported immediately by the pigeonhole check |

Running the program on the official example from the assignment description (2 stadiums, 2 days, 2 time slots, 4 matches) produces output that matches one of the valid solutions listed in the assignment, confirming the correctness of the core constraint implementation. Overall, Forward Checking combined with MRV/LCV finds solutions with zero or very few backtracks, and the two feasibility pre-checks reject clearly unsolvable inputs immediately, without spending any time on search.

## Function Reference

| File | Function / Class | Purpose |
|---|---|---|
| `input_reader.py` | `parse_input` | Parses input tokens and maps sensitive matches to their indices |
| `input_reader.py` | `normalize_sensitive` | Normalizes a sensitive team pair, independent of name order |
| `input_reader.py` | `read_input` | Opens the input file and returns the final structure used by `main.py` |
| `csp_model.py` | `build_variables` | Builds the list of variable IDs (`0` to `N-1`) |
| `csp_model.py` | `build_domains` | Builds the full (day, time slot, stadium) domain for each variable |
| `csp_model.py` | `build_neighbors` | Builds the complete neighborhood graph |
| `csp_model.py` | `is_consistent` | Checks the three main and bonus constraints |
| `csp_model.py` | `is_feasible` | Performs the total capacity and pigeonhole pre-checks |
| `solver.py` | `select_unassigned_variable` | MRV heuristic |
| `solver.py` | `order_values_lcv` | LCV heuristic |
| `solver.py` | `forward_check` | Prunes neighboring domains after each assignment |
| `solver.py` | `search_backtracking` | Recursive core of the search |
| `solver.py` | `solve_csp` | Solver entry point; measures execution time and the backtrack count |
| `main.py` | `print_solution` | Prints the output in the requested format |
| `main.py` | `main` | Wires together all modules and runs the complete solving pipeline |

## Team and Responsibilities

| Team Member | Files | Main Responsibility |
|---|---|---|
| Team Member 1 | `input_reader.py`, `csp_model.py` | Reading and parsing input; CSP modeling (variables, domains, neighborhood, consistency function); feasibility pre-checks |
| Team Member 2 | `solver.py`, `main.py` | Backtracking Search, Forward Checking, MRV, LCV, and the program entry point |
