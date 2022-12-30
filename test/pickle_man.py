import pickle

list_1 = {"beijing":1, "xiangyang":2}

with open("./test.pkl", 'wb') as fw:
    pickle.dump(list_1, fw,)

fw.close()

with open("./test.pkl", "rb") as fr:
    old = pickle.load(fr)

list_2 = {"shanghai":3, "xiamen":4}
print(list(list_2.keys())[0])
# print(list_2["test"])
list_3 = {"beijing":3}
old.update(list_3)
print(old)
old.update(list_2)
fra = open("./test.pkl", 'wb')

pickle.dump(old, fra)

fra.close()

with open("./test.pkl","rb") as fr1:
    print(pickle.load(fr1))

