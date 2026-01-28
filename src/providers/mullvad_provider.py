import time
import os
from pathlib import Path
from random import choice

import requests

from . import VpnProvider
from src.helpers import FileHelp
from src.helpers import WireguardHelp

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
	CONFIG_FILE_NAME = "mullvad.conf"

	def __init__(self, cache_dir: str = "./cache"):		
		self.cache_dir = Path(cache_dir)
		self.cache_dir.mkdir(parents=True, exist_ok=True)

		self._servers = None
		self._cache_ttl: float = 0.0
		self._current_server = {}

	# Tempo de vida do cache 1h (3600 segundos)
	def cache_is_valid(self, ttl: int = 3600) -> bool:
		"""Verifica se o cache em memoria ainda é valido."""
		if not self._servers or time.time() - self._cache_ttl > ttl:
			return False

		return True


	# TODO: Mudar para a função propria do Python "urllib" evitando dependencias de terceiros.
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
		"""Carrega o cache em memoria"""
		cache_path = self.cache_dir / self.CACHE_FILE_NAME
		if not cache_path.exists():
			print("Cache não existe")
			return False

		try:

			cache = FileHelp.read_json(str(self.cache_dir), self.CACHE_FILE_NAME)
			if not isinstance(cache, dict) or "ttl_cache" not in cache:
				return False

			if time.time() - cache["ttl_cache"] > 3600:
				print("Cache expirado")
				return False

			self._servers = cache["servers"]
			self._cache_ttl = cache["ttl_cache"]

			print(f"Cache carregado (ttl restante: {time.time() - self._cache_ttl:.2f})")
			return True

		except Exception as err:
			print(f"Falha ao carregar o cache: {err}")
			raise err


	def update_and_save_cache(self, eyes_type: int = 5):
		"""Atualiza o cache e persiste ele no disco."""
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
		"""Retorna os servidores disponiveis para se conectar"""
		if not force_refresh and self.load_cache(eyes_type):
			return self._servers

		self.update_and_save_cache(eyes_type)

		return self._servers


	def make_config_file(self, country_code: str = "", random_country: bool = True):
		if not self._servers or not self.cache_is_valid():
			self.update_and_save_cache()

		if not country_code and random_country:
			country = choice(list(self._servers.keys()))
			server = choice(self._servers[country])

			
			# TODO: Pegar o caminho de forma dinamica
			raw_conf = FileHelp.read_txt("", "template_wireguard.conf")

			raw_conf = raw_conf.replace("ENDPOINT", server["ipv4_addr_in"])
			raw_conf = raw_conf.replace("PORT", "51820")
			raw_conf = raw_conf.replace("ALLOWEDIPS", "0.0.0.0/0")
			raw_conf = raw_conf.replace("PUBLICKEYSERVER", server["pubkey"])
			raw_conf = raw_conf.replace("PRIVATE_KEY", "VOCE ACHOU MESMO QUE EU IA DEIXAR ELA DANDO SOPA AQUI ?")


			# TODO: Escrever essa config em /etc/wireguard/mullvad.conf
			FileHelp.write_txt(WireguardHelp.CONFIG_PATH, self.CONFIG_FILE_NAME, raw_conf)

				