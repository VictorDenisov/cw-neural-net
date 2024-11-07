import torch

x = torch.rand(5, 3)

print(x)
print(torch.cuda.is_available())

y = 10

y = y + 4

print(y)
