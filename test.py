import os

for i in range(1_000_000):
    print("boo!", flush=True)

print("PID:", os.getpid())
