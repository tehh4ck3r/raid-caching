import sys

# Used for converting data from the gawk output to a better format for our cache simulators.

def main(argv):
	if len(sys.argv) != 3:
		sys.exit("Usage: %s inputfilename outputfilename" % argv[0])

	filename = sys.argv[2]
	outfilename = sys.argv[3]

	with open(filename) as file:
		lines = file.readlines()

	with open(outfilename, 'w') as file:
		for x in lines:
			file.write(str(lines.index(x)))
			file.write('\n')

if __name__ == "__main__":
	main(sys.argv)