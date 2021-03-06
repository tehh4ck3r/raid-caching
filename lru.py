import sys
import collections

def main(argv):
	# check for correct number of arguments
	if len(sys.argv) != 4:
		sys.exit("Usage: %s cachesize filename numdevices" % argv[0])

	max_pages = int(sys.argv[1]) # max_pages = maximum number of entries in the entire cache
	in_file = sys.argv[2] # in_file = the file to use as input for requests
	num_devices = int(sys.argv[3]) # num_devices = number of devices in our RAID 0 array

	# get all the lines from our input and put them in a list
	with open(in_file) as file:
		lines = file.readlines()

	lines = [x.strip() for x in lines] # get rid of newline characters
	lines = map(int, lines) # make everything into an int

	# initialize an empty list of deques to simulate our cache; each deque = 1 device
	cachelist = [] 
	max_indiv_cache_size = max_pages // num_devices # max_indiv_cache_size = max cache size per device
	for x in range(num_devices):
		cachelist.append(collections.deque(maxlen=max_indiv_cache_size))

	num_misses = 0

	# for each line
	for x in lines:
		bin_num = x % num_devices # get the device that block x would be stored on

		if x not in cachelist[bin_num]: # if it's not in that device's cache, it's a miss
			num_misses += 1

			if len(cachelist[bin_num]) == max_indiv_cache_size: # if we've reached our max cache size for that device
				cachelist[bin_num].pop() # get rid of the least recently used entry

			cachelist[bin_num].appendleft(x) # put the requested value into the cache

		else: # it's not a miss, so move it to the front of the cache
			cachelist[bin_num].remove(x)
			cachelist[bin_num].appendleft(x)

	miss_rate = float(num_misses) / len(lines)
	miss_rate *= 100
	print("Number of misses: %i" % num_misses)
	print ("Number of input lines: %i" % len(lines))
	print ("Miss rate: %s%%" % str(round(miss_rate, 2)))

if __name__ == "__main__":
	main(sys.argv)