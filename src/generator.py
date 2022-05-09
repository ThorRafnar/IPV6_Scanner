import random
import time
import csv

class Generator:
	def __init__(self, filename=None, prefix=None, prefixLength=None):   
		''' Reads a file containing prefixes and lengths, or initializes with 1 prefix and its length '''     
		if filename:
			file = open(filename)
			csvreader = csv.reader(file)
			rows = []
			for row in csvreader:
				prefix = self.__parse_prefix(row[0])
				length = int(row[1])
				rows.append((prefix, length))
			file.close()
			self.prefixes = rows
		elif prefix and prefixLength:
			self.prefixes = [(prefix, prefixLength)]
		else:
			self.prefixes = [("2001:0DB8:0000:000b", 64)] # Random default value, should never be used this way
		self.next = 0
		self.__generate_next_address()
		self.size = len(self.prefixes)


	def get_list(self, count):
		''' Returns a list of generated addresses of length count '''
		ret = []
		for i in range(count):
			ret.append(self.get_address())
		return ret


	def get_address(self):
		''' Returns a generated address merged with a prefix from the list '''
		pair = self.prefixes[self.next]
		prefix = pair[0]
		length = pair[1]
		base_address = self.address
		self.next += 1
		if self.next >= self.size:
			self.__generate_next_address()
			self.next = self.next % self.size
		addr = self.__merge(prefix, length, base_address)
		addr = self.__address_to_string(addr)
		return addr
          
		  
	def __merge(self, prefix, prefix_length, address):
		''' Merges a prefix with an address'''
		ret = []
		i = 0
		while prefix_length > 0:
			if prefix_length >= 16:
				ret.append(prefix[i])
				prefix_length -= 16
			else:
				mask = 0xFFFF & (0xFFFF << 16 - prefix_length)
				merged_hextet = (prefix[i] & mask) | (address[i] & ~mask)
				ret.append(merged_hextet)
				prefix_length  = 0
			i += 1
		while i < 8:
			ret.append(address[i])
			i += 1
		return ret

	def __generate_next_address(self):
		''' Generates a list of length 8 containing numbers between 0 and 0xFFFF '''
		max = 0xFFFF
		ls = []
		while (len(ls) < 8):
			n = random.randint(0, max) & max
			ls.append(n)
		self.address = ls

	def __parse_prefix(self, prefix):
		return [ int(item, 16) if item != '' else 0 for item in prefix.split(':')  ]

	def __address_to_string(self, address):
		return ":".join([ f'{n:X}' for n in address ])
