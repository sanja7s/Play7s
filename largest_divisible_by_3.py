def answer(l):
    if l == []:
        return 0
    l.sort(reverse=True)
    k = sum(l) % 3
    
    if k == 0:
        return int(''.join(map(str,l)))
        
    
    for i in range(len(l)):
        el = l[i]
        if el % 3 == k:
            l.pop(i)
            return int(''.join(map(str,l)))
            
    for i in range(len(l)):
        r = answer(l.pop(i))
        if r:
            return int(''.join(map(str,l)))
            
    return 0

def test()
    print answer([3,1,4,1])

    print answer([3, 1, 4, 1, 5, 9])

    print answer([0])

    print answer([0,0,0,0,0,0,9,9,9,9,9,7])

    print answer([0,0,0,1,4,5,8,3,0,0,0,9,9,9,9,9,7])
