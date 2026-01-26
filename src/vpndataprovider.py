import requests
import time
import json
from abc import ABC, abstractmethod


class VpnProvider(ABC):
	"""
	Classe Abstrata que serve como base para a criação das outras.
	"""
	# https://pt.wikipedia.org/wiki/Alian%C3%A7a_Cinco_Olhos
	five_eyes = ["EUA", "UK", "CA", "AU", "NZ"]                        #eyes_type 5
	nine_eyes = five_eyes + ["DK", "FR", "NL" ,"NO"]                   #eyes_type 9
	fourheen_eyes  = nine_eyes + ["DE", "BE", "IT", "ES", "SE"]        #eyes_type 14

	@abstractmethod
	def cache_is_valid(ttl=3600):
		pass


	# Limpa os paises da aliança dos servidores.
	@classmethod
	def clean_data(cls, raw_data: dict, eyes_type: int) -> list:
		pass


	# Coleta informações sobres os servidores disponiveis
	@abstractmethod
	def feth_raw(self) -> list:
		pass

	# Modifica dos dados coletados com o objetivo de facilitar a manipulação.
	@abstractmethod
	def transformdata(self, raw_data: dict) -> list:
		pass



class MullvadProvider(VpnProvider):
	"""
	Obtem e Filtra dados sobre os servidores que o provedor Mullvad disponibiliza para se conectar.

	Metodos:
		fetch_raw: Responsavel por se conectar a API e coletar os dados.

		cache_is_valid: Verifica se o cache dos servidores excedeu o tempo de vida maximo TTL.

		clean_data: Remove os paises dos 4, 9 e 14 olhos da lista de servidores.

		transformdata: Modifica a lista de servidores a fim de deixa-la util.

	"""
	def __init__(self):
		self.api_url = "https://api.mullvad.net/www/relays/wireguard/"
		self._servers = {}


	# Tempo de vida do cache 1h (3600 segundos)
	def cache_is_valid(ttl: int = 3600):
		"""
		Verifica se o cache salvo ainda está valido.

		Argumentos:

			ttl (int): Tempo de vida em segundos a ser verificado.
			Valor padrão 1 hora (3600)
		"""
		current_time = time.time()
		if current_time - self._servers['ttl_cache'] > ttl:
			return False


	def feth_raw(self) -> list:
		"""
		Coleta a lista de servidores disponiveis a partir da API disponibilizada pela Mullvad.

		Retorno:

			Lista de servidores disponiveis fornecida pela Mullvad.
		"""
		try:
			response = requests.get(self.api_url)
			if response.status_code == 200:
				raw_data = json.loads(response.text)
				print("Informações dos servidores obtida com Sucesso.")
				return raw_data

		except requests.ConnectionError as err:
			print(f"Não foi possivel se conectar a {self.api_url}\nERRO: {err}")


	@classmethod
	def clean_data(cls, raw_data: list, eyes_type: int) -> list:
		"""
		Retira da lista servidores que fazem parte dos 5, 9 e 14 olhos

		Argumentos:
			
			raw_data: Lista contendo os servidores

			eyes_type: Tipo de tratado usado como base. Valor esperado: 5, 9 ou 14

				five_eyes = ["EUA", "UK", "CA", "AU", "NZ"]                        eyes_type 5
				nine_eyes = five_eyes + ["DK", "FR", "NL" ,"NO"]                   eyes_type 9
				fourheen_eyes  = nine_eyes + ["DE", "BE", "IT", "ES", "SE"]        eyes_type 14


		Retorno: Uma lista sem os paises selecionados.
		"""
		eyes_map = {
			5  : cls.five_eyes,
			9  : cls.nine_eyes,
			14 : cls.fourheen_eyes
		}

		countries = eyes_map.get(eyes_type)
		if countries is None:
			raise ValueError(f"Tipo de aliança inválido: {eyes_type}. Eperado: 1, 2 ou 3")

		clean_servers = [
			server for server in raw_data 
			if server.get("country_code", "").upper() not in countries
		]

		return	clean_servers


	def transformdata(self, raw_data: list) -> list:
		"""
		Agrupa os servidores pelo codigo do pais (BR, EUA...), facilitando o controle.

		Argumentos:

			raw_data: Lista com os servidores a serem agrupados.

		Retorno:

			lista com os servidores agrupados.
		"""
		servers  = {}
		for server in raw_data:
			country = server['country_code'].upper()

			if country in servers.keys():
				servers[country].append(server)

			else:
				servers[country] = [server]

		return servers
