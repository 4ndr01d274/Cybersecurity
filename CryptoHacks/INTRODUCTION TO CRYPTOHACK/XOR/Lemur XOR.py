from PIL import Image
from pwn import *

lemur = Image.open("lemur.png")
flag = Image.open("flag.png")

leak_bytes = xor(lemur.tobytes(), flag.tobytes())
leak = Image.frombytes(flag.mode, flag.size, leak_bytes)

leak.save('leak.png')