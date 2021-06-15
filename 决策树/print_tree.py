def format_result(tree, count, result, list_last):
    count += 1
    try:
        if result[count] != []:
            pass
    except:
        result[count] = []

    try:
        if list_last[count] != []:
            pass
    except:
        list_last[count] = []

    # print("count:", count)
    key = list(tree.keys())
    for k in key:
        # print(k)
        if count != 1:
            last = result[count - 1][-1]
            # print('last:', result[count - 1][-1])
            list_last[count].append(last)
        result[count].append(k)
        value = tree[k]
        try:
            a = tree[k].keys()
        except:
            count += 1
            try:
                if result[count] != []:
                    pass
            except:
                result[count] = []
            result[count].append(tree[k])
            # print(tree[k])

            last = result[count - 1][-1]
            try:
                if list_last[count] != []:
                    pass
            except:
                list_last[count] = []
            list_last[count].append(last)
            # print('last:', result[count][-1])
            # print("count:", count)
            # print('end')
            continue
        format_result(value, count, result, list_last)
    return result, list_last

def printf_tree(result):
    for i in range(len(result.keys())-2):
        t = ''.join(result[i + 1])
        s = ''
        for j in range(len(t) - 1):
            s += t[j]
            if ord('0') <= ord(t[0]) <= ord('9'):
                if int(t[j + 1]) <= int(t[j]) or t[j] == '0':
                    s += '|'
            elif ord('a') <= ord(t[0]) <= ord('z'):
                s += '|'
        s += t[-1]
        print(s)
    for i in range(len(result.keys())-2, len(result.keys())):
        t = ''.join(result[i + 1])
        s = ''
        for j in range(len(t) - 1):
            s += t[j]
            s += '|'
        s += t[-1]
        print(s)

if __name__ == '__main__':
    tree = {'d': {'1': {'b': {'1': {'a': {'1': {'c': '2'}, '2': {'c': {'1': {'e': '1'}, '2': {'e': '1'}, '3': {'e': '0'}}}, '3': {'c': {'1': {'e': '1'}, '2': {'e': '1'}, '3': {'e': '0'}}}}}, '2': {'a': {'1': {'a': '0'}, '2': {'c': '2'}, '3': {'f': {'1': {'c': '2'}, '2': {'c': '2'}, '3': {'c': '0'}}}}}, '3': {'a': '2'}}}, '2': {'f': {'1': {'a': {'1': {'b': '2'}, '2': {'b': {'1': {'c': '1'}, '2': {'c': '2'}, '3': {'c': '0'}}}, '3': {'b': '2'}}}, '2': {'a': '3'}, '3': {'a': '0'}}}, '3': {'a': '1'}}}

    count = 0
    result = {}
    list_last = {}
    result, list_last = format_result(tree, count, result, list_last)
    print(result)
    # print(list_last)
    printf_tree(result)



