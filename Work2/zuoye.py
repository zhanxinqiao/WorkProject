result=[]
for i in range(1,100):
    if i%7==0 and i%5!=0 :
        result.append(i)
print(result)
assert len(result) ==12
assert all([i % 7 ==0 for i in result])
assert any([i % 5 !=0 for i in result])

