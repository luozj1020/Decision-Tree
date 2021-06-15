import math
from print_tree import format_result, printf_tree
from train_tree import create_data, test
import json

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

# data:训练集；attributes:属性集；target_attr:好瓜/坏瓜
# data的元素应该为字典，data=[(’瓜1‘)[“属性值”, “属性值”, ...]。。。]
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

    # 如果属性集为空 或者 属性数量小于等于1
    if not data or (len(attributes) - 1) <= 0:
        print('属性集为空 或者 属性数量小于等于1')
        if data == []:
            default = '0'
        else:
            default = majority_value(vals)
        print({nex: default})
        return {nex: default} # 返回样本数最多的类
    # 如果样本全属于同一类
    elif vals.count(vals[0]) == len(vals):
        print('样本全属于同一类')
        print({nex: vals[0]})
        return {nex: vals[0]}
    else:
        # Choose the next best attribute to best classify our data
        best = choose_attribute(data, attributes, target_attr, fitness_func)
        # Create a new decision tree/node with the best attribute and an empty dictionary object--we'll fill that up next.
        tree = {best:{}} # 生成决策树，是一个嵌套的字典
        print(tree)
        # Create a new decision tree/sub-node for each of the values in the best attribute field
        val = get_values(data, best) # 筛选出最佳属性的三种属性值的序号组

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
    attributes = [chr(ord('a')+i) for i in range(len(data[0])-1)] # 6种属性
    print(attributes)
    target_attr = '1' # 选取好瓜
    call_count = 0
    # list_d = [[1,4,6,10,13,17],[2,3,7,8,9,15],[5,11,12,14,16]]
    # print(choose_attribute(data, attributes, target_attr, fitness_func))
    tree = create_decision_tree(data, attributes, target_attr, fitness_func, call_count)
    print('tree:\n', tree)
    print('formated_tree:')
    json_tree = json.dumps(tree, sort_keys=True, indent=4, separators=(',', ': '))
    print(json_tree)
    with open('tree.json', 'w') as f:
        f.write(json_tree)
    '''
    count = 0
    result = {}
    list_last = {}
    result, list_last = format_result(tree, count, result, list_last)
    print('\nformated_result:\n', result)
    # print(list_last)
    print('formated_tree:')
    printf_tree(result)
    '''
    test_data = create_data()
    result = {}
    for i in range(len(test_data)):
        r = test(tree, test_data[i])
        result[i+1] = r
    print('\ntest_data:\n', test_data)
    print('test_result:\n', result)
