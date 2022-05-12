import random
import time
import csv
import socket

######################################
#   CREATED BY Arnjee & ThorRafnar   #
######################################

socket.setdefaulttimeout(0.15)  

class Generator:
    def __init__(self, filename, id, pool_size, current=0):   
        ''' Reads a file containing prefixes and lengths, or initializes with 1 prefix and its length '''     
        if filename:
            file = open(filename)
            csvreader = csv.reader(file)
            rows = []
            idx = 0
            for row in csvreader:
                prefix = self.__parse_prefix(row[0])
                length = int(row[1])
                rows.append((prefix, length))
                idx += 1
            file.close()
            print(f'Scanning with {len(rows)} prefixes')
            self.prefixes = rows
        else:
            self.prefixes = [("2001:0DB8:0000:000b", 64)] # Random default value, should never be used this way
        self.id = id
        self.pool_size = pool_size
        self.chunk_size = 65536 // pool_size
        self.lower_pref = self.chunk_size * self.id
        self.upper_pref = self.chunk_size * (self.id + 1)
        self.current_pref = 0
        self.next = 0
        self.size = len(self.prefixes)
        self.offset = 0
        self.current = 1
        self.power = 1.5
        self.target = 65536 ** 3
        self.iterations = 0
        self.iter_target = 65536
        self.step = self.target ** (1/self.power) / self.iter_target
        if self.step <= 0:
	        self.step = 1
        self.__generate_next_address()


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
        self.__generate_next_address()
        if self.next >= self.size:
            self.next = self.next % self.size
        addr = self.__merge(prefix, length, base_address)
        addr = self.__address_to_string(addr)
        #print(addr)
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
        ls = [0] * 8
        num = (self.current**self.power) + self.offset
        ls[7] = int(num % 0x10000)
        num /= 0x10000
        ls[6] = int(num % 0x10000)
        num /= 0x10000
        ls[5] = int(num % 0x10000)
        num /= 0x10000
        ls[4] = int(num % 0x10000)
        self.current += self.step
        self.iterations += 1
        prefix_ending = random.randint(self.lower_pref, self.upper_pref - 1) * 0x100
        ls[3] = prefix_ending % 0x10000
        ls[2] = (prefix_ending // 0x10000) % 0x10000
        if ((self.current**self.power) + self.offset >= self.target):
            self.current = 0
            self.offset += 1
        self.address = ls

    def __parse_prefix(self, prefix):
        return [ int(item, 16) if item != '' else 0 for item in prefix.split(':')  ]

    def __address_to_string(self, address):
        return ":".join([ f'{n:X}' for n in address ])
