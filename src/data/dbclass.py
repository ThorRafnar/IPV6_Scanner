from data.main import session, Port, Address
from sqlalchemy import create_engine
######################################
#   CREATED BY Arnjee & ThorRafnar   #
######################################

class Data:

    def __init__(self, populate_ports = False):
        self.session = session
        self.populate_ports = populate_ports
        
        if self.populate_ports == True:
            self.populate_port_table()
            self.populate_ports = False
    def get_addresses_with_ports_sql_query(self, ports):
        sql = """select * from addresses A join association_table PA on PA.address = A.address where PA.port in ports;"""
   

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
    def sublist(self, lst1, lst2):
       ls1 = [element for element in lst1 if element in lst2]
       ls2 = [element for element in lst2 if element in lst1]
       return ls1 == ls2

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
            #port_hits = 0
            
            #for port in address.ports:
            #    if port.port in open_ports:
            #        port_hits += 1

            #if port_hits == len(open_ports):
            #    ret_lis.append(address)

            if self.sublist(open_ports, address.ports):
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

            
