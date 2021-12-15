from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import numpy as np
import json

R = 2700

grades = ['j', 'm', 's']

qualities = {
    "sa": [0.2, 0.3, 0.2],
    "dev": [0.8, 0.9, 0.4],
    "qa": [0.1, 0.2, 0.3],
    "db": [0.2, 0.4, 0.8]
}

persons_count = {
    "sa": [3, 4, 2],
    "qa": [1, 6, 1],
    "dev": [4, 10, 8],
    "db": [1, 1, 2]
}

distribution = {
    "sa": {
        "prices": [50, 100, 150],
        "max": 450,
    },
    "dev": {
        "prices": [70, 130, 180],
        "max": 550,
    },
    "qa": {
        "prices": [30, 50, 70],
        "max": 350,
    },
    "db": {
        "prices": [65, 100, 140],
        "max": 450,
    },
}

n = 3
k = 3
m = 2

persons_dist = {
    "dev-qa": [m, k],
    "dev-sa": [1, n]
}


sa = [LpVariable(name="{}{}".format('sa'.upper(), grade), lowBound=0, cat='Integer')
    for grade, quality in zip(grades, qualities['sa'])]
dev = [LpVariable(name="{}{}".format('dev'.upper(), grade), lowBound=0, cat='Integer')
    for grade, quality in zip(grades, qualities['dev'])]
qa = [LpVariable(name="{}{}".format('qa'.upper(), grade), lowBound=0, cat='Integer')
    for grade, quality in zip(grades, qualities['qa'])]
db = [LpVariable(name="{}{}".format('db'.upper(), grade), lowBound=0, cat='Integer')
    for grade, quality in zip(grades, qualities['db'])]

groups = {
    'sa': sa,
    'dev': dev,
    'qa': qa,
    'db': db
}

obj_func = lpSum(lpSum([q * x for q, x in zip(qualities[quality],groups[group])]) for group, quality in zip(groups.keys(), qualities.keys()))

print(obj_func)

inequality = lambda position: (lpSum([price * x for price, x in zip(distribution[position]['prices'], groups[position])]) <= distribution[position]['max'], 'Ограничение цен по отделу ' + position)

limitations = [inequality(position) for position in distribution.keys()]


inequality = lambda position: [
    (lpSum(x) <= count, 'Ограничение количества сотрудников {}'.format(x))
    for x, count in zip(groups[position], persons_count[position])
]

for position in persons_count.keys():
    limitations += inequality(position)

ratio = lambda position: [
    (persons_dist[position][0] * lpSum(groups[position.split('-')[0]])
    >= persons_dist[position][1] * lpSum(groups[position.split('-')[1]]), 'Ограничение по соотношению {}'.format(position))
]

for couple in persons_dist.keys():
    limitations += ratio(couple)


inequality = lambda position: lpSum([price * x for price, x in zip(distribution[position]['prices'], groups[position])])

iq = []
for key in groups.keys():
    iq += [inequality(key)]

iq = (lpSum(iq) <= 0.8*R, 'Основное ценовое ограничние')
limitations += [iq]

for limit in limitations:
    print(limit)

model = LpProblem(name="Quality", sense=LpMaximize)

for limit in limitations:
    model += limit

model += obj_func

model.solve()

print(f"status: {model.status}, {LpStatus[model.status]}")

print(f"objective: {model.objective.value()}")

teams = {}

for var in model.variables():
    try:
        teams[var.name[:-1].lower()][var.name[-1]] = int(var.value())
    except:
        teams[var.name[:-1].lower()] = {var.name[-1]: int(var.value())}
    print(f"{var.name}: {var.value()}")

teams = json.dumps(teams)
with open('data.json', 'w') as f:
    f.write(teams)

for name, constraint in model.constraints.items():
    print(f"{name}: {constraint.value()}")

print(teams)
