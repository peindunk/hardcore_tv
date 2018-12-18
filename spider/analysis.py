with open('fenlei.txt') as f:
    data = f.read()
    li = data.split('#')
    s = set(li)
    L = []
    print('总共有%d种分类'%len(s))
    for item in s:
        num = li.count(item)
        count = (item,num)
        L.append(count)
    L = sorted(L,key=lambda x:x[1],reverse=True)
    for item in [x for x in L if x[1]>50]:
        print('%s出现了:%d次'%item)
