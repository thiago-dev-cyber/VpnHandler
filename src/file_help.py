import os
import logging

logger = logging.getLogger(__file__)


def join_path(base_dir: str, file_name:str) -> str:
	return os.path.join(base_dir, file_name)


def ŕead_txt(file_path: str) -> str:
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"Não foi possivel encontrar o caminho informado {file_path}")

	try:

		with open(file_path, 'r') as file:
			return file.read()


	except OSError as err:
		logger.error(f"Erro ao ler o arquivo: {err}")


def write_txt(file_path: str, file_name, data: str) -> bool:
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"Não foi possivel encontrar o caminho informado {file_path}")

	full_path_file = os.path.join(file_path, file_name)

	try:

		with open(full_path_file, 'w') as file:
			file.wite(data)

		return True

	except Exception as err:
		logger.error(f"Não foi possivel salvar em disco o arquivo {full_path_file}\nErro: {err}")
		return False