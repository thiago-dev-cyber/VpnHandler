import requests
import time
from abc import ABC, abstractmethod


class VpnProvider(ABC):
	"""
	Classe Abstrata que serve como base para a criação das outras.
	"""
	# https://pt.wikipedia.org/wiki/Alian%C3%A7a_Cinco_Olhos
	five_eyes = ["EUA", "UK", "CA", "AU", "NZ"]                        #Type 1
	nine_eyes = five_eyes + ["DK", "FR", "NL" ,"NO"]                   #Type 2
	fourheen_eyes  = nine_eyes + ["DE", "BE", "IT", "ES", "SE"]       #Type 3

	@staticmethod
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


	@abstractmethod
	def transformdata(self, raw_data: dict) -> list:
		pass



class MullvadProvider(VpnProvider):
	"""
	Obtem e Filtra dados sobre os servidores que o provedor Mullvad disponibiliza para se conectar.

	Methodos:
		fetch_raw: Responsavel por se conectar a API e coletar os dados.
	"""
	def __init__(self):
		self.api_url = "https://api.mullvad.net/www/relays/wireguard/"


	def feth_raw(self):
		try:
			response = requests.get(self.api_url)
			if response.status_code == 200:
				raw_data = response.json()
				print("Informações dos servidores obtida com Sucesso.")
				return raw_data

		except requests.ConnectionError as err:
			print(f"Não foi possivel se conectar a {self.api_url}\nERRO: {err}")


	@classmethod
	def clean_data(cls, raw_data: dict, eyes_type: int):
		eyes_map = {
			1 : cls.five_eyes,
			2 : cls.nine_eyes,
			3 : cls.fourheen_eyes
		}

		countries = eyes_map.get(eyes_type)
		if countries is None:
			raise ValueError(f"Tipo de aliança inválido: {eyes_type}. Eperado: 1, 2 ou 3")

		clean_servers = [
			server for server in raw_data 
			if server.get("country_code", "").upper() not in countries
		]

		return	clean_servers


	def transformdata(self, raw_data: dict) -> list:
		pass