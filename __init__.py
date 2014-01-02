#This file is part of network module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.pool import Pool
from .network import *


def register():
    Pool.register(
        Network,
        NetworkHardwareType,
        NetworkHardware,
        NetworkSoftwareType,
        NetworkSoftware,
        NetworkSoftwareLogin,
        NetworkProtocolType,
        NetworkProtocol,
        module='network', type_='model')
