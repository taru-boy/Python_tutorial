def fizz_buzz(number_list: list):
    for i in number_list:
        if i % 15 == 0:
            print(f"{i}は１５で割り切れる。")
        elif i % 3 == 0:
            print(f"{i}は3で割り切れる。")
        elif i % 5 == 0:
            print(f"{i}は５で割り切れる。")
        else:
            print(f"{i}は3でも5でも割り切れない。")


my_list = [1, 30, 45, 99, 340]
fizz_buzz(my_list)
