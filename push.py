"""
№1
4 - А
2 - С
7 - Е
6 + 10 = 16
Ответ: 16
№2
"""
# print("x y z w")
# for x in range(2):
#     for y in range(2):
#         for z in range(2):
#             for w in range(2):
#                 if int((x == w) or (y and not z)) == 0:
#                     print(f"{x} {y} {z} {w}")
"""
w y z x
1 0 0 0
1 0 1 0
0 0 0 1
Ответ: wyzx
№4
А - 11
Б - 0110
В - 00
Г - 010
Ответ: 10
№5
"""
#
#
# def alg(n):
#     r = str(bin(n))[2:]
#     if n % 2 == 0:
#         return r + "00"
#     return r + "10"
#
#
# for n in range(1, 1000000000):
#     if int(alg(n), 2) > 130:
#         print(n)
#         break

"""
Ответ: 33
№6
"""
# x = 120
# p = 12
# while p <= x + 15:
#     p += 10
#     x -= 5
# print(x)
"""
Ответ: 75
№7
288 * 1152 * 6 = 1990656 бит
1990656 / 8 / 1024 = 243 Кбайт
Ответ: 243 Кбайт
№8
"""
# count = 0
# for q in range(10):
#     for w in range(10):
#         for e in range(10):
#             for r in range(10):
#                 for t in range(10):
#                     for y in range(10):
#                         a = f"{q}{w}{e}{r}{t}{y}"
#                         if a[-2:] != "34":
#                             continue
#                         if (a.count("0") + a.count("2") + a.count("4") + a.count("6") + a.count("8") == 3 or
#                             a.count("1") + a.count("3") + a.count("5") + a.count("7") + a.count("9") == 2) and \
#                                 len(set(a)) == 6:
#                             count += 1
# print(count)
"""
Ответ: 1248
№9
Ответ: 10,8
№10
Ответ: 2
№11
28 => 5 бит
5 * 13 = 65 бит = 9 байт
39 байт на одного
39 * 60 = 2400
Ответ: 2340 байт
№12
"""
# a = ">" + "1" * 32 + "4" * 11 + "6" * 22
# while ">1" in a or ">4" in a or ">6" in a:
#     if ">1" in a:
#         a = a.replace(">1", "1661>", 1)
#     if ">4" in a:
#         a = a.replace(">4", "146141>", 1)
#     if ">6" in a:
#         a = a.replace(">6", "141>", 1)
# print(sum(map(int, list(a[:-1]))))
"""
Ответ: 767
№13
Ответ:13
"""
