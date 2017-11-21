import sys
import collections

def main(argv):
	if len(sys.argv) != 3:
		sys.exit("Usage: lru.py cachesize filename numdevices")

	numPages = int(sys.argv[1])
	inFile = sys.argv[2]

	with open(inFile) as file:
		lines = file.readlines()

	lines = [x.strip() for x in lines]
	cache = collections.deque(maxlen=numPages)

	numPageFaults = 0

	for x in lines:
		if x not in cache:
			numPageFaults += 1

			if len(cache) == numPages:
				cache.pop()

			cache.appendleft(x)

		else:
			cache.remove(x)
			cache.appendleft(x)

	print("Number of page faults: %i" % numPageFaults)
	print ("Number of input lines: %i" % len(lines))

if __name__ == "__main__":
	main(sys.argv)