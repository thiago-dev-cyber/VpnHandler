import requests
import logging

logger = logging.getLogger(__name__)

class ApiMullvad:

	API_URL = "https://api.mullvad.net/www/relays/wireguard"

	@classmethod
	def get_servers(cls) -> dict:
		try:

			response = requests.get(url = cls.API_URL, timeout = 10)
			
			# Registrando informações para debug.
			logger.info("Buscando por Servidores Wireguard da Mullvad.")
			logger.info("A Api da Mullvad respondeu com: %i", response.status_code)

			response.raise_for_status()
			return response.json()

		except requests.RequestException as err:
			raise ConnectionError(
				f"Não foi possível acessar a API da MULLVAD"
				) from err


if __name__ == "__main__":

	ApiMullvad.get_servers()