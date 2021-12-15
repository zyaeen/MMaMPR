import json
import numpy as np

# 1 дерево с разными исходными данными

data = None

with open('data.json', 'r') as f:
    data = json.load(f)

print(data)

counter = 3
trees = [
    {
        'name': key,
        'choices': {
            'choose {}'.format(pos[-1]): np.round(np.random.uniform(0.2,
                                                                    0.98, size=data[key][pos]
                                                                    ),
                                                  2
                                                  ) for pos, num in zip(data[key].keys(),
                                                                        range(1, counter + 1)
                                                                        ) if data[key][pos] != 0
        }
    } for key in data.keys()
]

for key in trees:
    print(key)