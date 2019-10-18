import ast
teststr = "['aaa','bbb','ccc']"
testarray = ast.literal_eval(teststr)
print(len(testarray))
