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
    # print(data[ord(attribute)-ord('a')])
    try:
        # print(tree[attribute][str(data[ord(attribute)-ord('a')])])
        test(tree[attribute][str(data[ord(attribute)-ord('a')])], data)
    except:
        global s
        s = ''
        target = tree[attribute]
        if int(target) == data[ord(attribute)-ord('a')]:
            # print('好瓜')
            s = '好瓜'
        else:
            # print('坏瓜')
            s = '坏瓜'
    return s

if __name__ == '__main__':
    with open('tree.json', 'r') as f:
        tree = json.loads(f.read())
        print(tree)
    test_data = create_data()
    result = {}
    for i in range(len(test_data)):
        r = test(tree, test_data[i])
        result[i+1] = r
    print(test_data)
    print(result)


