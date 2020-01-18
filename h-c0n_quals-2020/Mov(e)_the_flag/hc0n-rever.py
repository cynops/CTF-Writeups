import string
import gdb
#H-c0n{bdd0fbdbefa8e89f421140836280a5683}
# gdb -x script.py
gdb.execute("file demov_challenge")
gdb.execute("handle SIGSEGV nostop noprint pass")
gdb.execute("handle SIGILL nostop noprint pass")

class MyBreakpoint(gdb.Breakpoint):
	def stop(self):
		return True

bp = MyBreakpoint("*0x8050f1e")

flag = ''
junk = '1'
valid_chars = string.printable
for i in range(0,40):
	for char in valid_chars:
		bp.hit_count=0

		with open("flagfile", "w") as f:
			f.write(flag + char + junk * (38 - len(flag)))
			f.write('\n')
		exec_command = 'r < flagfile > /dev/null'
		gdb.write("Trying: " + char + "\n")
		gdb.execute(exec_command)

		if bp.hit_count != 0:
			_ = [gdb.execute("c") for i in range(len(flag))]

		if (bp.hit_count == len(flag)+1) and bp.hit_count != 0:
			gdb.write("[!] Found character: " + char + "\n")
			flag  +=char
			break
		else:
			gdb.write("Hits: {}\n".format(bp.hit_count))

