st = input("请输入：")  # 输入字符串
result = []  # 创建空列表
for i in range(len(st)):
    if st[i] != 'i':
        result.append(st[i])
    elif st[i] == 'i':
        if i == len(st) - 1:
            if st[i - 1] == ' ':  # 判断该字符是否为i并且是最后一位且为单字母
                result.append('I')
            else:
                result.append(st[i])
        else:
            if st[i - 1] == ' ' and st[i + 1] == ' ':  # 判断该点是否为单字母
                result.append('I')
            else:  # 不为单字母便是单词直接添加到列表result里面
                result.append(st[i])

if result[0] == 'i' and result[1] == ' ':  # 判断第一个字母是否为单字母并且为i
    result[0] = 'I'

print(''.join(result))  # 将空格作为连字符并输出
