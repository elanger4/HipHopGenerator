"""
Barebones implimenation of recurrent neural network for langauge modeling

For more details on these implementations, please see the following:

http://www.fit.vutbr.cz/research/groups/speech/servite/2010/rnnlm_mikolov.pdf

http://karpathy.github.io/2015/05/21/rnn-effectiveness/

https://xa.yimg.com/kq/groups/14962965/957022186/name/reading_list_Generating+Text+with+Recurrent+Neural+Networks.pdf
"""

import numpy as np
from collections import OrderedDict

class RNN(object):

	def __init__(self, data_file, lr=1e-2, hidden_layers=100, unroll_len=25);
	"""
	Constructor for RNN class.
	TODO: pass other parameters for net
	TODO: Return object for assignment
	
	params:
	data_file 	  = path to datafile to train on
	lr		  	  = learning rate for net.
					Default value = 1e-2
	unroll_len 	  = Unroll RNN with unroll_len steps.
					Default value = 25
	hidden_layers = Number of hidden layers
					Default value = 100

	returns:
	None

	"""
		self.data = open(data_file, 'r').read() # Currently only supports plain
												#text seperated by \n

		self.char_set    = np.array(set(data)) # Creates set of all chars in data
		self.total_chars = len(data)		   # Number of chars in data
		self.card_chars  = len(self.char_set)  # Number of unique chars in data
		
		self.char_to_ix = OrderedDict([char:i for i, char in np.nditer(self.char_set)])
		self.ix_to_char = OrderedDict([i:char for i, char in np.nditer(self.char_set)])
		return None

	def loss(self, inputs, targets, hprev):
		"""
		Function to calculate loss at current layer
		TODO: Write it

		params:
		inputs  - np.array of ints
		output - np.array of ints
		"""


