result,a=[],[]
for i in range(1,100):
    result.append(i)
    try :
        assert all([i % 7 ==0 for i in result])
        assert any([i % 5 != 0 for i in result])
        a.append(result[0])
    except Exception as e :
        result=[]
result=a
assert len(result) ==12
print(result)