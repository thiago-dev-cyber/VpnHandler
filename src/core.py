import os
import json
import logging

from providers import MullvadProvider
from wg import Wireguard

#from rich import print



logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

VPN = MullvadProvider()

ROOT = os.path.dirname(__file__)
TEMPLATE_FILE = os.path.join(ROOT, "providers/template_wg.conf")

with open(os.path.join(ROOT, "config.json"), "r") as file:
	PRIV_KEY = json.load(file).get("PRIV_KEY", "")


def main(): 
	# Fetch servers
	available_servers = VPN.get_servers()
	server = VPN.choice_random_server(available_servers)

	print(server)
	Wireguard.stop_connection()
	config = Wireguard.generate_config_file(TEMPLATE_FILE, server, PRIV_KEY)
	Wireguard.save_config_file("wg-mullvad.conf", config)

	Wireguard.start_connection("wg-mullvad")


	
main()