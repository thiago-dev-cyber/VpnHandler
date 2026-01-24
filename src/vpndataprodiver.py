import requests
import time
from abc import ABC, abstractmethod


class VpnProvider(ABC):
	"""
	Classe Abstrata que serve como base para a criação das outras.
	"""
	# https://pt.wikipedia.org/wiki/Alian%C3%A7a_Cinco_Olhos
	five_eyes = ["EUA", "UK", "CA", "AU", "NZ"]
	nine_eyes = five_eyes + ["DK", "FR", "NL" ,"NO"]
	fourtheen_eyes  = nine_eyes + ["DE", "BE", "IT", "ES", "SE"]

	@staticmethod
	def cache_is_valid(ttl=3600):
		pass

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


	def transformdata(self, raw_data: dict) -> list:
		pass