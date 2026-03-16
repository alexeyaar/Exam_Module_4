# def user_input():
#     n= int(input("Что то типо цифр тут нужно ввести: "))
#     if n % 2 == 0:
#         ("Вы ввели четное число")
#     elif n % 2 != 0:
#         print("Вы ввели нечетное число")
#
# user_input()
def echo():
    n = int(input("Число: "))
    text = input("Текст: ")
    i = 0
    while i < n:
        print(text)
        i+=1
echo()