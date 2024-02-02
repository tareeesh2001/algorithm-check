import torch
import gc

print("Torch version:",torch.__version__)

print("Is CUDA enabled?",torch.cuda.is_available())

print(torch.cuda.empty_cache())
gc.collect()