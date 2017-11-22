from bins import bins
import sys

class page:
	def __init__(self, val, ref):
		self.value = val
		self.referenced = ref

def main(argv):
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

	num_misses = 0
	max_val = max(lines) # get max value for binning

	cachelist = [] # list containing each device's cache
	clock = [] # each device has an independent clock

	max_indiv_cache_size = max_pages // num_devices # max_indiv_cache_size = max cache size per device
	
	# initialize the per-device caches with empty pages
	for x in range(num_devices):		
		# initialize a new device with empty/invalid pages
		cache = []
		for y in range(max_indiv_cache_size):
			cache.append(page(-1, False))

		cachelist.append(cache) # add the new device to the list

		clock.append(0) # set the device's cache clock to 0

	# for each line
	for x in lines:
		bin_num = bins(max_val, num_devices, x) # get the device that block x would be stored on

		found = False 

		# find out if the value is in the cache
		for y in range(max_indiv_cache_size):
			if cachelist[bin_num][y].value == x: # we found it!
				cachelist[bin_num][y].referenced = True # set its referenced flag to True
				found = True
				break

		if not found: # it was a miss
			i = clock[bin_num] # used for incrementing
			while True:
				if not cachelist[bin_num][i].referenced: # find the next unreferenced element
					clock[bin_num] = i
					break

				cachelist[bin_num][i].referenced = False # set element's referenced flag to False

				if i == clock[bin_num] - 1: # stop the loop if we made it all the way around the cache
					break

				# traverse the cache circularly
				i += 1
				i %= max_indiv_cache_size

			# we found our unreferenced element, so replace it with the new value
			cachelist[bin_num][clock[bin_num]].value = x # replace element clock hand is pointing at
			cachelist[bin_num][clock[bin_num]].referenced = True # set its reference flag to True
			
			# advance the clock by 1, circularly
			clock[bin_num] += 1
			clock[bin_num] %= max_indiv_cache_size

			num_misses += 1

	miss_rate = num_misses / len(lines)
	miss_rate *= 100
	print("Number of misses: %i" % num_misses)
	print ("Number of input lines: %i" % len(lines))
	print ("Miss rate: %s%%" % str(round(miss_rate, 2)))

if __name__ == "__main__":
	main(sys.argv)