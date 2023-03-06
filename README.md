# Compare Darshan vs. eBPF prototype monitoring for POSIX write() call

## For Darshan, just profile the Python code as usual with an LD_PRELOAD

## for eBPF

1. In 1 terminal session do: `sudo python3 simple.py` and keyboard interrupt when
you are done profiling.
2. In another terminal session run the code you want to profile: `python3 test.py`
3. Since eBPF will monitor `write()` across the kernel, we confirm the appropriate
number of writes in the log manually for now, i.e. using the PID of the application
we want to instrument, `grep -E "71757" log.txt | wc -l`
