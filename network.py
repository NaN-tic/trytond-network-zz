#This file is part of network module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelSQL, ModelView, fields


__all__ = [
    'Network',
    'NetworkHardwareType',
    'NetworkHardware',
    'NetworkSoftwareType',
    'NetworkSoftware',
    'NetworkSoftwareLogin',
    'NetworkProtocolType',
    'NetworkProtocol',
]


class Network(ModelSQL, ModelView):
    "Network"
    __name__ = 'network.network'

    name = fields.Char('Network name', required=True)
    party = fields.Many2One('party.party', 'Party', required=True)
    hardwares = fields.One2Many('network.hardware', 'network', 'Hardwares')
    domain = fields.Char('Domain')
    ip_address = fields.Char('IP Address')
    note = fields.Text('Notes')

    @classmethod
    def __setup__(cls):
        super(Network, cls).__setup__()
        cls._constraints += [
            ('check_domain_or_ip_address', 'domain_or_ip_address_needed'),
        ]
        cls._error_messages.update({
            'domain_or_ip_address_needed':
                    'You must set at least the domain or IP address.',
        })

    def check_domain_or_ip_address(self):
        if not self.domain and not self.ip_address:
            return False
        return True


class NetworkHardwareType(ModelSQL, ModelView):
    "Network"
    __name__ = 'network.hardware.type'

    name = fields.Char('Type of hardware', required=True, translate=True)

    @staticmethod
    def default_networkable():
        return False


class NetworkHardware(ModelSQL, ModelView):
    'Network Hardware'
    __name__ = 'network.hardware'

    name = fields.Char('Device Name', required=True)
    network = fields.Many2One('network.network', 'Network', required=True)
    type = fields.Many2One('network.hardware.type', 'Hardware type',
            required=True)
    note = fields.Text('Notes')
    softwares = fields.One2Many('network.software', 'hardware', 'Softwares')
    party = fields.Function(fields.Many2One('party.party', 'Party'),
            'get_party', searcher='search_party')

    def get_party(self, name):
        return self.network.party.id

    @classmethod
    def search_party(cls, name, clause):
        return [('network.%s' % name,) + tuple(clause[1:])]


class NetworkSoftwareType(ModelSQL, ModelView):
    'Network Software Type'
    __name__ = 'network.software.type'

    name = fields.Char('Software Type Name', required=True)


class NetworkSoftware(ModelSQL, ModelView):
    'Network Software'
    __name__ = 'network.software'

    name = fields.Char('Software name', required=True)
    hardware = fields.Many2One('network.hardware', 'Hardware', required=True)
    type = fields.Many2One('network.software.type', 'Software Type')
    note = fields.Text('Notes')
    network = fields.Function(fields.Many2One('network.network', 'Network'),
            'get_network', searcher='search_network'
        )
    party = fields.Function(fields.Many2One('party.party', 'Party'),
            'get_party', searcher='search_party'
        )
    logins = fields.One2Many('network.software.login', 'software',
        'Login Users')
    protocols = fields.One2Many('network.protocol', 'software',
        'Connection Protocols')

    def get_network(self, name):
        return self.hardware.network.id

    @classmethod
    def search_network(cls, name, clause):
        return [('hardware.%s' % name,) + tuple(clause[1:])]

    def get_party(self, name):
        return self.hardware.network.party.id

    @classmethod
    def search_party(cls, name, clause):
        return [('hardware.network.%s' % name,) + tuple(clause[1:])]


class NetworkSoftwareLogin(ModelSQL, ModelView):
    'Network Software Login'
    __name__ = 'network.software.login'
    _rec_name = 'login'

    login = fields.Char('User', required=True)
    password = fields.Char('Password', required=True)
    software = fields.Many2One('network.software', 'Software', required=True)
    note = fields.Text('Notes')
    hardware = fields.Function(fields.Many2One('network.hardware', 'Hardware'),
            'get_hardware',
        )
    superuser = fields.Boolean('Super User')

    def get_hardware(self, login):
        return self.software.hardware.id


class NetworkProtocolType(ModelSQL, ModelView):
    'Network Protocol Type'
    __name__ = 'network.protocol.type'

    name = fields.Char('Protocol Name', required=True)

    @classmethod
    def __setup__(cls):
        super(NetworkProtocolType, cls).__setup__()
        cls._order.insert(0, ('name', 'ASC'))


class NetworkProtocol(ModelSQL, ModelView):
    'Network Protocol'
    __name__ = 'network.protocol'

    name = fields.Many2One('network.protocol.type', 'Protocol', required=True)
    note = fields.Text('Notes')
    port = fields.Integer('Port', required=True)
    software = fields.Many2One('network.software', 'Software', required=True)
