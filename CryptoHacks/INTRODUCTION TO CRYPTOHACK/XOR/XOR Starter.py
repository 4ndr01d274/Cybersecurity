parte = "label"


flag="".join(chr(ord(x)^13)for x in parte)

print("crypto{"+flag+"}")