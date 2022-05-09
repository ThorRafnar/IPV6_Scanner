from data.dbclass import Data

def addr_to_string(address):
	"""RIP debugger"""
	address = [ "{:0>4}".format(hextet) for hextet in address.split(':') ]
	return ':'.join(address)

def print_addresses(addresses):
	print("{:.<42}{:.<6}".format("ADDRESS", "PORTS"))
	for ipv6 in addresses:
		# Good luck figuring this one out :^)
		print("{: <42}".format(addr_to_string(ipv6.address.decode('utf-8'))), end='')
		first = True
		for port in ipv6.ports:
			if first:
				print(f"{port.port}", end='')
				first = False
			else:
				print(f", {port.port}", end='')
		print()

def print_addresses_with_port(addresses, ports):
	print("Addresses with ports", ports, "open")
	print_addresses(addresses)

def get_ports():
	ports = []
	print("Enter ports, press enter to when done")
	p = input("Input: ")
	while p != '':
		ports.append(int(p))
		print("Ports:", ports)
		p = input("Input: ")
	return ports

if __name__ == '__main__':
	d = Data()
	print("1. Print All Addresses")
	print("2. Print Addresses with specific port/s")
	inp = input("Input: ")
	while inp != 'q':
		if inp == '1':
			addresses = d.get_addresses()
			print_addresses(addresses)
		elif inp == '2':
			ports = get_ports()
			addresses = d.get_ipv6_with_open_port(ports)
			print_addresses_with_port(addresses, ports)
		else:
			print("Invalid input!")
		inp = input("Input: ")
