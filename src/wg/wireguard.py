import file_help
import logging 

import subprocess

logger = logging.getLogger(__file__)


class Wireguard:

	CONFIG_PATH = "/etc/wireguard"

	@classmethod
	def generate_config_file(cls, template_file_path: str, config: dict, private_key: str) -> str:
		template = file_help.ŕead_txt(template_file_path)

		server_pubkey = config.get("pubkey", "")
		server_ip = config.get("ipv4_addr_in", "")
		server_port = "51820"


		template = template.replace("PRIVATE_KEY", private_key)
		template = template.replace("PUBLIC_KEY", server_pubkey)
		template = template.replace("SERVER_IP", server_ip)
		template = template.replace("SERVER_PORT", server_port)

	
	@classmethod
	def save_config_file(cls, file_name: str, config) -> bool:
		full_path = file_help.join_path(CONFIG_PATH, file_name)

		if file_help.write_txt(full_path, config):
			logger.info("Arquivo de configuração salvo com sucesso!")


	@staticmethod
	def stop_connection():
		interfaces_actives = subprocess.run(["wg", "show", "interfaces"], text=True, capture_output=True).stdout
		subprocess.run(["wg-quick", "down", interfaces_actives.strip()])

	