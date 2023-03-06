import os

with open("test_out.txt", "w") as outfile:
    for i in range(1_000):
        outfile.write("a")
        outfile.flush()
        os.fsync(outfile)

print("PID:", os.getpid())
