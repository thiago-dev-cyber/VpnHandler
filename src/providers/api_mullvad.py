import requests
import logging

logger = logging.getLogger(__name__)

class ApiMullvad:
	"""Cliente responsável por realizar requisições à API da Mullvad."""
	API_URL = "https://api.mullvad.net/www/relays/wireguard"

	@classmethod
	def get_servers(cls) -> dict:
		"""Consulta a API_URL e retorna um Json com os servidores informados pela API."""
		try:

			response = requests.get(url = cls.API_URL, timeout = 10)
			
			logger.info("Buscando por Servidores Wireguard da Mullvad.")
			logger.info("A Api da Mullvad respondeu com: %i", response.status_code)

			response.raise_for_status()
			return response.json()

		except requests.RequestException as err:
			raise ConnectionError(
				f"Não foi possível acessar a API da MULLVAD"
				) from err


if __name__ == "__main__":
	# Testando o funcionamento da API.
	ApiMullvad.get_servers()