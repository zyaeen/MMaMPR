from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import numpy as np


def solve_task(matrix, max_solve=False):

    play_matrix = matrix

    if max_solve:
        play_matrix = play_matrix.T

    elements_count = play_matrix.shape[0]

    model = LpProblem(name="Game", sense=LpMaximize)

    x = [LpVariable(name="y{}".format(i + 1), lowBound=0) for i in range(elements_count)]
    print('Переменные:', x)

    obj_func = -lpSum(x)
    if max_solve:
        obj_func = -obj_func

    print('Функция: ',obj_func)

    for ineq in play_matrix:
        print('Ограничение')
        print(lpSum([x[i]* ineq[i] for i in range(elements_count)]))
        if max_solve:
            model += (lpSum([x[i]* ineq[i] for i in range(elements_count)]) <= 1)
        else:
            model += (lpSum([x[i] * ineq[i] for i in range(elements_count)]) >= 1)

    model += obj_func

    model.solve()
    F = -model.objective.value()
    if max_solve:
        F = -F

    return {
        "y": np.array([var.value() for var in model.variables()]),
        "F":  F,
        "v": 1 / F
    }


matrix = np.array([
    [300, 900, 700],
    [600, 400, 500],
    [800, 200, 400]
])


solution_one = solve_task(matrix=matrix)
solution_two = solve_task(matrix=matrix, max_solve=True)

S_one = solution_one['y'] * solution_one['v']
S_two = solution_two['y'] * solution_two['v']

print(solution_one['v'], solution_two['v'])
print(S_one, S_two)