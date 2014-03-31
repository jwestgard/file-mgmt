#! usr/bin/python
    
def alignlists(list1, list2):
    col1 = iter(sorted(list1))
    col2 = iter(sorted(list2))
    
    x = next(col1)
    y = next(col2)
    
    while col1 and col2:
        if x == None and y == None:
            break
        if x == None:
            while y:
                print("\t" + str(y))
                y = next(col2, None)
        elif y == None:
            while x:
                print(str(x) + "\t")
                x = next(col1, None)
        elif x == y:
            print(str(x) + "\t" + str(y))
            x = next(col1, None)
            y = next(col2, None)
        elif x > y:
            print("\t" + str(y))
            y = next(col2, None)
        elif x < y:
            print(str(x) + "\t")
            x = next(col1, None)
                
alignlists([1,2,8,9,100,74,3,5,10,11,14], [1,3,87,43,1039,982,1092,98,23,4,6,7,11,15])