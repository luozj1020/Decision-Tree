import math
import json
from train_tree1 import create_data, test

def majority_value(vals):
    count_num = []
    for i in range(3):
        count_num.append(vals.count(str(i+1)))
    c = max(count_num)
    return str(count_num.index(c) + 1)

def fitness_func(data, target_attr, list_D):
    list_0 = []
    for i in range(len(data)):
        if data[i][-1] == '0':
            list_0.append(data[i])
    list_1 = []
    for i in range(len(data)):
        if data[i][-1] == '1':
            list_1.append(data[i])
    p0 = len(list_0)/len(data)
    p1 = len(list_1)/len(data)
    if p0 != 0 and p1 != 1 and p0 != 1 and p1 != 0:
        ent_d = -(p0 * math.log(p0, 2) + p1 * math.log(p1, 2))
    else:
        ent_d = 0

    result = []
    for i in range(len(list_D)):
        list_t = []
        for j in range(len(list_D[i])):
            if data[list_D[i][j]-1][-1] == target_attr:
                list_t.append(list_D[i][j])
        # print('list_t:' + str(list_t))

        p = len(list_t)/len(list_D[i])
        if p == 0:
            result.append(-((1-p) * math.log((1-p), 2)))
        elif p == 1:
            result.append(-(p * math.log(p, 2)))
        else:
            result.append(-(p * math.log(p, 2) + (1-p) * math.log((1-p), 2)))
    # print('result:' + str(result))
    gain = ent_d
    for i in range(len(list_D)):
        gain -= len(list_D[i])/len(data) * result[i]
    # print('gain:' + str(gain))
    return gain

def choose_attribute(data, attributes, target_attr, fitness_func):
    list_gain = []
    # print(data)
    for k in attributes:
        list_1, list_2, list_3 = [], [], []
        for j in range(len(data)):
            if data[j][ord(k)-ord('a')] == '1':
                list_1.append(j+1)
            elif data[j][ord(k)-ord('a')] == '2':
                list_2.append(j+1)
            else:
                list_3.append(j+1)
        list_d = [list_1, list_2, list_3]
        try:
            while [] in list_d:
                list_d.remove([])
        except:
            pass
        # print('list_d:' + str(list_d))
        list_gain.append(fitness_func(data, target_attr, list_d))
    # print('list_gain:' + str(list_gain))
    max_gain = max(list_gain)
    # print('max_gain:' + str(max_gain))
    return attributes[list_gain.index(max_gain)]

def get_values(data, best):
    list_1, list_2, list_3 = [], [], []
    for j in range(len(data)):
        if data[j][ord(best) - ord('a')] == '1':
            list_1.append(j+1)
        elif data[j][ord(best) - ord('a')] == '2':
            list_2.append(j+1)
        else:
            list_3.append(j+1)
    list_best = [list_1, list_2, list_3]
    # print('get_values list_best:' + str(list_best))
    return list_best

def get_examples(data, val):
    examples = []
    for num in val:
        examples.append(data[num-1])
    # print('examples:' + str(examples))
    return examples

# data:????????????attributes:????????????target_attr:??????/??????
# data???????????????????????????data=[(??????1???)[???????????????, ???????????????, ...]?????????]
def create_decision_tree(data, attributes, target_attr, fitness_func, call_count):
    call_count += 1
    print("call_count:", call_count)
    data = data[:]
    print('data:' + str(data))
    if call_count == 1:
        vals = [record[-1] for record in data]
    else:
        try:
            global nex
            nex = choose_attribute(data, attributes, target_attr, fitness_func)
            print('nex:' + nex)
            vals = [record[ord(nex) - ord('a')] for record in data]
            print('vals:' + str(vals))
        except ZeroDivisionError:
            pass

    # ????????????????????? ?????? ????????????????????????1
    if not data or (len(attributes) - 1) <= 0:
        print('??????????????? ?????? ????????????????????????1')
        if data == []:
            dir = {}
            for i in range(3):
                dir[str(i+1)] = {'r': '0'}
            default = dir
        else:
            dir = {majority_value(vals): {'r': '1'}}
            for i in range(3):
                if int(majority_value(vals)) != i + 1:
                    dir[str(i + 1)] = {'r': '0'}
            default = {nex: dir}
        print('default:', {nex: default})
        return {nex: default} # ???????????????????????????
    # ??????????????????????????????
    elif vals.count(vals[0]) == len(vals):
        print('????????????????????????')
        dir = {vals[0]: {'r': '1'}}
        for i in range(3):
            if int(vals[0]) != i+1:
                dir[str(i+1)] = {'r': '0'}
        print({nex: dir})
        return {nex: dir}
    else:
        # Choose the next best attribute to best classify our data
        best = choose_attribute(data, attributes, target_attr, fitness_func)
        # Create a new decision tree/node with the best attribute and an empty dictionary object--we'll fill that up next.
        tree = {best:{}} # ??????????????????????????????????????????
        print(tree)
        # Create a new decision tree/sub-node for each of the values in the best attribute field
        val = get_values(data, best) # ???????????????????????????????????????????????????

        for i in range(len(val)):
            print('val:' + str(val))
            # Create a subtree for the current value under the "best" field
            print('val_i:' + str(val[i]))
            tree[best][str(i+1)] = create_decision_tree(get_examples(data, val[i]),
                [attr for attr in attributes if attr != best],
                target_attr, fitness_func, call_count)
            # Add the new subtree to the empty dictionary object in our new tree/node we just created.
    return tree

if __name__ == '__main__':
    with open("wm3.csv", 'r') as f:
        data = [d.split(',')[1:] for d in [s.replace('\n', '') for s in f.readlines()]]
    print(data)
    attributes = [chr(ord('a')+i) for i in range(len(data[0])-1)] # 6?????????
    print(attributes)
    target_attr = '1' # ????????????
    call_count = 0
    # list_d = [[1,4,6,10,13,17],[2,3,7,8,9,15],[5,11,12,14,16]]
    # print(choose_attribute(data, attributes, target_attr, fitness_func))
    tree = create_decision_tree(data, attributes, target_attr, fitness_func, call_count)
    print('tree:\n', tree)
    print('formated_tree:')
    json_tree = json.dumps(tree, sort_keys=True, indent=4, separators=(',', ': '))
    print(json_tree)
    with open('tree1.json', 'w') as f:
        f.write(json_tree)
    test_data = create_data()
    result = {}
    print('\ntest_data:\n', test_data)
    for i in range(len(test_data)):
        r = test(tree, test_data[i])
        result[i+1] = r
    print('test_result:\n', result)
