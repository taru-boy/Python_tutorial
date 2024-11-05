error_list = [2, 3, 5, 7, 9]
check_list = [4, 6, 10, 11]

# for文の中でif条件に該当するときはbreak
# breakに該当しなかったらelse以下の処理が実行される。
for i in check_list:
    if i in error_list:
        print(f"{i}がerror_listに含まれていたのでfor文を抜ける")
        break
else:
    print("finish")
