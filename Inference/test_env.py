import torch
print(torch.cuda.is_available())
print(torch.backends.cudnn.is_acceptable(torch.cuda.FloatTensor(1)))
print(torch.backends.cudnn.version())
print(torch.version.cuda)
