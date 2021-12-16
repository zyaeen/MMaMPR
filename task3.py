import json
import numpy as np
from anytree import Node, RenderTree


with open('data.json', 'r') as f:
    data = json.load(f)

common_count = {key: sum(data[key].values()) for key in data.keys()}
print(common_count)


def get_prob(n):

    array = []

    for k in range(n):

        while True:
            p = np.round(np.random.uniform(0.2, 0.98, size=1), 2)[0]
            if p != 0.5:
                break
        sums = np.round(np.random.randint(2, 16, size=2), 2)
        array += [{"p": [p, int(sums[0])], "q": [np.round(1 - p, 2), int(sums[1])]}]

    return array

counter = 3
trees = [
    {
        "name": str(key),
        "choices": {
            "choose {}".format(pos[-1]): [
                {
                    "Employee id": "Employee {}".format(r1 * 100 + num * 10 + k + 1),
                    "p": obj["p"],
                    "q": obj["q"]
                }
                for k, obj in zip(range(data[key][pos]), get_prob(data[key][pos]))
            ] for pos, num in zip(data[key].keys(),range(1, counter + 1)) if data[key][pos] != 0
        }
    } for key, r1 in zip(data.keys(), range(1, len(data.keys()) + 1))
]
print(trees[0])
teams = json.dumps(trees)
with open('data_with_probs.JSON', 'w') as f:
    f.write(teams)

with open('data_with_probs.json', 'r') as f:
     data = json.load(f)

trees = []

means = {}

for structure in data:
    root = Node(structure['name'])
    choices = []

    means[structure['name']] = {}

    for choice_key in structure['choices'].keys():
        choice_cur = Node(choice_key, parent=root)
        choices += [choice_cur]
        employees = []
        for employee in structure['choices'][choice_key]:
            employee_cur = Node(employee["Employee id"], parent=choice_cur)
            employees += [employee_cur]
            p_cur = Node(employee["p"][0], parent=employee_cur)
            q_cur = Node(employee["q"][0], parent=employee_cur)
            tp_cur = Node(employee["p"][1], parent=p_cur)
            tq_cur = Node(employee["q"][1], parent=q_cur)

            means[structure['name']][employee["Employee id"]] = np.round(employee["p"][0] * employee["p"][1]
                                                                         + employee["q"][0] * employee["q"][1],
                                                                         2
                                                                         )
    # means[structure['name']]['min'] = min(means[structure['name']].values())

    means[structure['name']] = {k: v for k, v in sorted(means[structure['name']].items(), key=lambda item: item[1])}
    trees += [root]

for tree, mean_key in zip(trees, means.keys()):
    for pre, fill, node in RenderTree(tree):
        print("%s%s" % (pre, node.name))
    print(mean_key)
    for emp in means[mean_key]:
        print(emp, means[mean_key][emp])

