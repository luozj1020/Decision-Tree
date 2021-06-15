import random
import json

def create_data():
    test_data = []
    for j in range(10):
        temp = []
        for i in range(6):
            temp.append(random.randint(1, 3))
        test_data.append(temp)
    # print(test_data)
    return test_data

def test(tree, data):
    attribute = list(tree.keys())[0]
    # print(attribute)
    if attribute != 'r':
        # print(data[ord(attribute) - ord('a')])
        global dir
        dir = tree[attribute][str(data[ord(attribute) - ord('a')])]
        # print('dir:', dir)
        test(tree[attribute][str(data[ord(attribute) - ord('a')])], data)
    else:
        global test_result
        test_result = ''
        # print('result:', dir[attribute])
        test_result = dir[attribute]
    return test_result

if __name__ == '__main__':
    with open('tree.json', 'r') as f:
        tree = json.loads(f.read())
        print(tree)
    test_data = create_data()
    result = {}

    for i in range(len(test_data)):
        print(test_data[i])
        r = test(tree, test_data[i])
        result[i+1] = r
    print(result)


