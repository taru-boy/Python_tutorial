#strip関数は両端の空白や改行を削除する
#rstrip関数は右端、lstrip関数は左端を削除
string = " 明日の天気は晴れ\n明後日の天気は雨\n"
print(string.strip())

#replace関数で置換できる
catstring = "吾輩はねこニャン、ねこ好きに悪いやつはいないニャン"
print(catstring.replace("ねこ", "いぬ").replace("ニャン", "ワン"))

#listとtupleの違い
#listは代入できる。tupleは代入できない。
my_list =[1,2,3,4,5]
my_list[1]=100
print(my_list)

my_tuple =(1,2,3,4,5)
#my_tuple[1]=100
print(my_tuple)