from data.main import session, Port, Address

class Data:

    def __init__(self, populate_ports = False):
        self.session = session
        self.populate_ports = populate_ports

        if self.populate_ports == True:
            self.populate_port_table()
            self.populate_ports = False
        
    def write_to_database(self, open_ports, ipv6_address):
        """Writes an open ipv6 address and all its ports to db"""
        
        #Making sure we are not working with an already exsiting ip
        if self.session.query(Address).filter(Address.address==ipv6_address).first() != None:
            return

        new_ipv6 = Address(address=ipv6_address)

        for open_port in open_ports:
            assinged_port = self.session.query(Port).filter(Port.port==open_port).first()
            new_ipv6.ports.append(assinged_port)
        
        print(ipv6_address, open_ports)
        self.session.commit()

    def get_addresses(self):
        all_addresses = self.session.query(Address).all()
        return all_addresses[1:]

    def get_ipv6_with_open_port(self, open_ports):
        """
        Return all addresses that have ports open in open_ports
        If open_ports = [22, 80], it will return all addresses with
        22, 80 open and more. Not less.
        """
        addresses = session.query(Address).all()
        ret_lis = []

        for address in addresses:
            port_hits = 0
            
            for port in address.ports:
                if port.port in open_ports:
                    port_hits += 1

            if port_hits == len(open_ports):
                ret_lis.append(address)

        return ret_lis

    def populate_port_table(self):
        """
        Populates all ports if port table is empty not
        being used at all right now
        """
        port_list = []
        for i in range(1,65536):
            new_port = Port(port=i)
            port_list.append(new_port)
        self.session.add_all(port_list)
        self.session.commit()

            