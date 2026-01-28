import os
import json

class FileHelp:
    """Classe de ajuda parar manipulação de arquivos diversos."""
    @staticmethod
    def write_json(file_dir: str, file_name: str, data: dict) -> bool:
        """Salva dados em um arquivo no formato JSON"""
        if not os.path.exists(file_dir):
            print(f"Não foi possivel encontrar o diretorio informado: {file_dir}")

            return False

        try:

            full_file_path = os.path.join(file_dir, file_name)

            with open(full_file_path, 'w') as file:
                json.dump(data, file, indent=4)

            return True

        except PermissionError:

            print(
                f"Não foi possivel escrever no arquivo {file_dir}/{file_name}"
                "\nVerifique se você possui permissão e tente novamente."
                )
            return False

        except OsError as err:
            print(f"Erro de sistema: {err}")

            return False
    
    
    @staticmethod
    def read_json(file_dir: str, file_name) -> dict:
        """Le dados de um arquivo que esteja no formato JSON"""
        if not os.path.exists(file_dir):
            print(f"Não foi possivel encontrar o diretorio informado {file_dir}")
            return False

        try:

            full_file_path = os.path.join(file_dir, file_name)

            with open(full_file_path, 'r') as file:
                return json.load(file)

        except PermissionError:

            print(
                f"Não foi possivel escrever no arquivo {file_dir}/{file_name}"
                "\nVerifique se você possui permissão e tente novamente."
                )

        except OsError as err:
            print(f"Erro de sistema: {err}")

        except json.JSONDecodeError:
            print(f"O conteudo do arquivo {full_file_path} não é um documento JSON valido")

        except json.UnicodeDecodeError:
            print(
                f"O conteudo do arquivo {full_file_path} não está em um formato unicode valido"
                "formatos aceitos UTF-8, UTF-16 ou UTF-32."
                )


    @staticmethod
    def read_txt(file_dir: str, file_name) -> str:
        pass

    
    @staticmethod
    def write_txt(file_dir: str, file_name, data) -> bool:
        pass

    @staticmethod
    def is_lock(file_path: str) -> bool:
        """Verifica se o arquivo esta bloqueado para escrita."""
        pass

    
    @staticmethod
    def lock_file(file_path: str) -> bool:
        """Bloqueia o arquivo, impossibilitando a escrita."""
        pass


    @staticmethod
    def unlock_file(file_path: str) -> bool: 
        """Desbloqueia o arquivo, possibilitando a escrita"""