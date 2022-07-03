from config import infura_url
from web3 import HTTPProvider,Web3
from ens import ENS


def convert_ENSname_to_ResolvedAddress(infura_url, ENS_name):

    provider = HTTPProvider(infura_url)
    ns = ENS(provider)
    eth_address = ns.address(ENS_name)

    print(eth_address)
    return eth_address

def get_clean_ResolvedETHAddress(infura_url, address):
    #convert ENS name to resolved address(42-char hexadecimal)
    if (address.endswith('.eth') or 
        address.endswith('.ETH')):
        eth_address = convert_ENSname_to_ResolvedAddress(infura_url, address)
        if eth_address:
            return eth_address
        else:
            return "INVALID_or_UNREGISTERED_ENS.ETH"
    #check if it's a valid 42-char hexadecimal
    elif Web3.isAddress(address):
        return address 

    return "INVALID_hexadecimal_ADDRESS!!!!"


