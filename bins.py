from __future__ import division
import math

# given a maximum value, a number of bins, and an input value, returns the bin to which the input value belongs (from range 0 -> num_bins-1)
def bins(max_value, num_bins, x):
	bin_size = math.ceil(max_value / num_bins)
	increment = 0

	for z in range(num_bins):
		if (0 < x <= increment+bin_size):
			return z
		else:
			increment += bin_size