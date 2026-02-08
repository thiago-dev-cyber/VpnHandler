import os
import logging

logger = logging.getLogger(__file__)


def join_path(base_dir: str, file_name:str) -> str:
	"""Monta o caminho completo combinando um diretório base e um nome."""
	return os.path.join(base_dir, file_name)


def delete_file(file_path: str) -> bool:
	"""Exclui o arquivo indicado por file_path."""
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"Não foi possivel encontrar o arquivo {file_path}.")

	try:
		os.remove(file_path)
		return True

	except OSError as err:
		logger.error(f"Erro ao tentar excluir {file_path}.")
		return False


def ŕead_txt(file_path: str) -> str:
	"""Lê um arquivo .txt e retorna seu conteúdo."""
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"Não foi possivel encontrar o caminho informado {file_path}")

	try:

		with open(file_path, 'r') as file:
			return file.read()


	except OSError as err:
		logger.error(f"Erro ao ler o arquivo: {err}")


def write_txt(file_path: str, file_name, data: str) -> bool:
	"""Escreve dados em um arquivo no formato txt"""
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"Não foi possivel encontrar o caminho informado: {file_path}")

	full_path_file = os.path.join(file_path, file_name)

	try:
		with open(full_path_file, 'w') as file:
			file.write(data)

		return True

	except Exception as err:
		logger.error(f"Não foi possivel salvar em disco o arquivo {full_path_file}\nErro: {err}")
		return False