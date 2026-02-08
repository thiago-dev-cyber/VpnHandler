import file_help
import logging 

import subprocess

logger = logging.getLogger(__file__)


class Wireguard:
	"""Fornece métodos para controlar e interagir com o WireGuard."""

	CONFIG_PATH = "/etc/wireguard"

	@classmethod
	def generate_config_file(cls, template_file_path: str, config: dict, private_key: str) -> str:
		"""Monta o arquivo de configuração do WireGuard."""
		template = file_help.ŕead_txt(template_file_path)
		if not template:
			logger.warning("Template retornado está vazio, verifique e tente novamente: %s", template)
			return ""

		server_pubkey = config.get("pubkey", "")
		server_ip = config.get("ipv4_addr_in", "")
		server_port = "51820"

		template = template.replace("PRIVATE_KEY", private_key)
		template = template.replace("PUBLIC_KEY", server_pubkey)
		template = template.replace("SERVER_IP", server_ip)
		template = template.replace("SERVER_PORT", server_port)

		return template


	@classmethod
	def save_config_file(cls, file_name: str, config) -> bool:
		"""Persiste o arquivo de configuração em disco."""
		if not file_help.write_txt(cls.CONFIG_PATH, file_name, config):
			logger.error("Não foi possivel salvar o arquivo de configuração em disco!")
			return False

		logger.info("Arquivo de configuração salvo com sucesso!")
		return True


	@classmethod
	def exclude_config_file(cls, file_name: str) -> bool:
		"""Exclui o arquivo de configuração do disco."""
		full_path = file_help.join_path(cls.CONFIG_PATH, file_name)

		if not file_help.delete_file(full_path):
			logger.error("Não foi possivel excluir o arquivo de configuração: %s", full_path)
			return False

		logger.info("Arquivo de configuração excluido com sucesso.")
		return True


	@staticmethod
	def stop_connection(interface: str = "", shutdown_all: bool = True):
		"""Desativa conexões WireGuard."""
		result = subprocess.run(["wg", "show", "interfaces"], text=True, capture_output=True)
		interfaces = result.stdout.strip().split()

		if not interfaces:
			logger.info("Nenhuma interface WireGuard ativa encontrada.")
			return

		if interface:
			result = subprocess.run(["wg-quick", "down", interface.strip()], text=True, capture_output=True)
			if result.check_returncode == 0:
				logger.info(f"Interface {interface} desligada com sucesso.")
				return

			else:
				logger.warning(f"Falha ao desligar a interface {interface}: {resul.strerr}")

			return

		if shutdown_all:
			for iface in interfaces:
				resul = subprocess.run(["wg-quick", "down", iface.strip()], text=True, capture_output=True)
				if result.check_returncode == 0:
					logger.info(f"Interface {iface} desligada com sucesso.")

				else: 
					logger.warning(f"Falha ao desligar a interface {iface}: {resul.stderr}")


	@classmethod
	def start_connection(cls, config_name: str):
		"""Inicia uma conexão WireGuard"""
		try:
			result = subprocess.run(["wg-quick", "up", config_name], text=True, capture_output=True)
			logger.info(result.stderr)

		except Exception as err:
			logger.error(f"Não foi possivel iniciar a conexão: {err}")