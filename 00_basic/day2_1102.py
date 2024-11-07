import math

# "ctrl+shift+I"でpythonコードをフォーマットできる。
# Black Formatterを使用することにした

list = [1, 2, 3, 4, 5]
list_n = []

for i in list:
    i = i**3
    # listのiを回しているが、listが増え続けるため無限ループ。
    # list.append(i)
    list_n.append(i)


i = 0
while i < 3:
    i += 1  # i=i+1
    # print(f"あと{3-i}回で終わります")

# listの内包表記
# [iを含む式 for i in イテラブルアイテム]
my_list = [i * 3 + 5 for i in range(10)]

# join関数
# 文字列を結合することができる。区切り文字の指定も可能。
# join()の中はlistで渡す。
tag_id = "_".join(["タグ名", "説明"])


# while, break
i = 0
while True:
    i += 1
    if i == 5:
        break

# 三項演算子
# 条件が真ならば5, 偽ならば10。値の代入に便利。
x = 1
point = 5 if x == 1 else 10

# 例外処理　try except文
# try　本来の処理
# except　エラー処理

try:
    theta = float(input())
    theta = theta * math.pi
    print(math.sin(theta))
except Exception as e:
    print(e)
