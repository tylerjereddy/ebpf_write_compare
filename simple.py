import os
import pwd

from bcc import BPF

prog = """
int hello(void *ctx) {
    bpf_trace_printk("called write!\\n");
    return 0;
}
"""

b = BPF(text=prog)

# track POSIX write() calls via libc:
b.attach_uprobe(name="c",
                sym="write",
                fn_name="hello")

# eBPF will track ALL write() calls, not just
# of any given program we run in another session,
# so for now we'll awkwardly try to scope our counts
# to our specific username (tyler)

def owner(pid):
    # see: https://stackoverflow.com/a/5327812/2942522
    '''Return username of UID of process pid'''
    for ln in open(f"/proc/{pid}/status"):
        if ln.startswith('Uid:'):
            uid = int(ln.split()[1])
            return pwd.getpwuid(uid).pw_name

total_posix_writes = 0

with open("log.txt", "w") as outfile:
    while 1:
        try:
            (task, pid, cpu, flags, ts, msg) = b.trace_fields()
            if pid == os.getpid():
                # we don't want to profile this profiling
                # application itself
                continue
            username = owner(pid)
            # TODO: needing to "manually" filter by username is a bit
            # awkward, and even this isn't enough to narrow things down--
            # I still need to parse the log.txt for the exact PID of the
            # program I ran/that I wanted to profile...
            if username == "tyler":
                total_posix_writes += 1
                outfile.write(f"task: {task}, flags: {flags}, pid: {pid}, username: {username}\n")
        except ValueError:
            continue
        except (FileNotFoundError, ProcessLookupError):
            continue
        except KeyboardInterrupt:
            break

print(f"total_posix_writes for user tyler: {total_posix_writes}")
