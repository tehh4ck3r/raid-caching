from bins import bins
import sys
import collections

class page:
	def __init__(self, val, count=0):
		self.value = val
		self.counter = count

def main(argv):
	if len(sys.argv) != 4:
		sys.exit("Usage: %s cachesize filename numdevices" % argv[0])

	max_pages = int(sys.argv[1]) # max_pages = maximum number of entries in the entire cache
	in_file = sys.argv[2] # in_file = the file to use as input for requests
	num_devices = int(sys.argv[3]) # num_devices = number of devices in our RAID 0 array
	max_indiv_cache_size = max_pages // num_devices # max_indiv_cache_size = max cache size per device
	num_misses = 0 # number of misses for our cache

	# get all the lines from our input and put them in a list
	with open(in_file) as file:
		lines = file.readlines()

	lines = [x.strip() for x in lines] # get rid of newline characters
	lines = map(int, lines) # make everything into an int

	max_val = max(lines) # get max requested value so we can request the right device later on

	# initialize a list of empty lists to simulate our cache; each sublist = 1 device
	cachelist = [] 
	for x in range(num_devices):
		cache = []
		cachelist.append(cache) # add the new device to the list

	# for each line
	for x in lines:
		# bin_num = bins(max_val, num_devices, x) # get the device that block x would be stored on
		bin_num = x % num_devices # get the device that block x would be stored on
		
		# check if x is in our cache already
		for y in cachelist[bin_num]:
			if y.value == x: # we found it! 
				y.counter += 1 # so increment its counter... 
				cachelist[bin_num].insert(0, cachelist[bin_num].pop(cachelist[bin_num].index(y))) # ...and move it to the front
				break

		else: # we didn't find it
			num_misses += 1

			# if our cache is full
			if len(cachelist[bin_num]) == max_indiv_cache_size:
				# search for the least frequently used element
				least_used_count = cachelist[bin_num][0].counter 
				least_used = None

				for z in cachelist[bin_num]:
					if z.counter <= least_used_count:
						least_used_count = z.counter
						least_used = z

				cachelist[bin_num].remove(least_used) # remove the least frequently used element

			cachelist[bin_num].insert(0, page(x, 0)) # insert the new value at the front


	miss_rate = float(num_misses) / len(lines)
	miss_rate *= 100
	print("Number of misses: %i" % num_misses)
	print ("Number of input lines: %i" % len(lines))
	print ("Miss rate: %s%%" % str(round(miss_rate, 2)))

if __name__ == "__main__":
	main(sys.argv)