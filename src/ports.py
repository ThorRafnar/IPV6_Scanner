import subprocess

class Ports():
	"""
	Parses most n common ports from the output of
	the nmap command  nmap --top-ports {count} -v -oG
	where count == the number of ports.
	"""
	def __init__(self, count=20):
		self.count = count
		self.ports = []
		command = f"nmap --top-ports {count} -v -oG -".split(' ')
		result = subprocess.run(command, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout
		result = result.decode("utf-8").split("TCP")[1].split(";")[1].split(")")[0].split(",")
		for port in result:
			if '-' in port:
				p = port.split('-')
				for i in range(int(p[0]), int(p[1]) + 1):
					self.ports.append(i)
			else:
				self.ports.append(int(port))

	def get_common_ports(self):
		return self.ports

if __name__ == "__main__":
	p = Ports()
	print(p.get_common_ports())


	