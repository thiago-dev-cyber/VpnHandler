import requests
import time
import json
from src.filehelp import FileHelp
from pathlib import Path
from abc import ABC, abstractmethod


class VpnProvider(ABC):
	"""
	Classe Abstrata que serve como base para a criação das outras.
	"""
	# https://pt.wikipedia.org/wiki/Alian%C3%A7a_Cinco_Olhos
	five_eyes = ["EUA", "UK", "CA", "AU", "NZ"]                        #eyes_type 5
	nine_eyes = five_eyes + ["DK", "FR", "NL" ,"NO"]                   #eyes_type 9
	fourteen_eyes  = nine_eyes + ["DE", "BE", "IT", "ES", "SE"]        #eyes_type 14

	@abstractmethod
	def cache_is_valid(ttl=3600):
		pass


	@abstractmethod
	def load_cache(cache_path: str) -> bool:
		pass


	# Limpa os paises da aliança dos servidores.
	@classmethod
	def clean_data(cls, raw_data: dict, eyes_type: int) -> list:
		pass


	# Coleta informações sobres os servidores disponiveis
	@abstractmethod
	def fetch_raw(self) -> list:
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
	API_URL = "https://api.mullvad.net/www/relays/wireguard/"
	CACHE_FILE_NAME = "mullvad_servers.json"
	def __init__(self, cache_dir: str = "./cache"):		
		self.cache_dir = Path(cache_dir)
		self.cache_dir.mkdir(parents=True, exist_ok=True)
		self._servers = None
		self._cache_ttl: float = 0.0



	# Tempo de vida do cache 1h (3600 segundos)
	def cache_is_valid(self, ttl: int = 3600):
		"""
		Verifica se o cache em memoria ainda é valido.
		"""
		if not self._servers or time.time() - self._cache_ttl > ttl:
			return False

		return True


	def fetch_raw(self) -> list:
		"""
		Coleta a lista de servidores disponiveis a partir da API disponibilizada pela Mullvad.
		"""
		try:
			response = requests.get(self.API_URL, timeout=10)
			if response.status_code == 200:
				raw_data = response.json()
				print(f"Dados da API Mullvad obtidos com sucesso ({len(raw_data)} servidores)")
				return raw_data


		except requests.RequestException as err:
			print(f"Falha ao obter dados da API Mullvad: {err}")
			raise


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
			14 : cls.fourteen_eyes
		}

		countries = eyes_map.get(eyes_type)
		if countries is None:
			raise ValueError(f"Tipo de aliança inválido: {eyes_type}. Eperado: 5, 9 ou 14")

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



	def load_cache(self, eyes_type: int = 5) -> bool:
		"""
		Carrega o cache em memoria
		"""
		cache_path = self.cache_dir / self.CACHE_FILE_NAME
		if not cache_path.exists():
			print("Cache não existe")
			return False

		try:

			ćache = FileHelp.json_load(str(cache_dir), self.CACHE_FILE_NAME)
			if not isinstance(cache, dict) or "ttl_cache" not in cache:
				return False

			if time.time() - cache["ttl_cache"] > 3600:
				print("Cache expirado")
				return False

			self._servers = cache["servers"]
			self._cache_ttl = cache["ttl_cache"]

			print(f"Cache carregado (ttl restante: {time.time() - self._cache_ttl:.2f}")
			return True

		except Exception as err:
			print(f"Falha ao carregar o cache: {err}")
 


	def update_and_save_cache(self, eyes_type: int = 5):
		raw_data = self.fetch_raw()
		cleaned = self.clean_data(raw_data, eyes_type)
		transformed = self.transformdata(cleaned)

		cache_data = {
			"servers" : transformed,
			"ttl_cache": time.time(),
			"eyes_type": eyes_type
		}


		FileHelp.write_json(str(self.cache_dir), self.CACHE_FILE_NAME, cache_data)

		self._servers = transformed
		self._cache_ttl = cache_data["ttl_cache"]

		print("Cache atualizado e salvo")


	def get_servers(self, force_refresh: bool = False, eyes_type: int = 5) -> dict:
		if force_refresh or not self.cache_is_valid():
			self.update_and_save_cache(eyes_type)
		if self._servers is None:
			raise RuntimeError("Nenhum servidor carregado")

		return self._servers