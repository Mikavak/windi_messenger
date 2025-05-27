# def explain_args_and_kwargs():
#     # *args - позиционные аргументы
#     # **kwargs - именованные аргументы
#     def example(*args, **kwargs):
#         for i in kwargs:
#             print(i, kwargs[i])
#
#     # Примеры вызова
#     example(1, 2, 3, a=4, b=5)
#
# explain_args_and_kwargs()


a = 1
b = 2
c=3
a, b, c = c, b, a
print(a, b, c)

a = b, c

print(a)