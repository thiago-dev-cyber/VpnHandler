from providers import MullvadProvider
from wg import Wireguard
import os

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

VPN = MullvadProvider()
TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), "providers/template_wg.conf")

def choice_random_server(servers: list) -> dict:
	import random

	country_choice = random.choice(list(servers.keys()))
	server = random.choice(servers[country_choice])
	return server


def main(): 
	# Fetch servers
	servers = VPN.get_servers()
	server = choice_random_server(servers)

	Wireguard.stop_connection()
	#config = Wireguard.generate_config_file(TEMPLATE_FILE, server, "")
	#Wireguard.save_config_file("Mullvad", config)
	
main()