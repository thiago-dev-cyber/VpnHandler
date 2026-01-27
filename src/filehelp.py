class FileHelp:
    """Classe de ajuda parar manipulação de arquivos diversos."""
    @staticmethod
    def write_json(cls, file_dir: str, file_name: str, data: dict) -> bool:
        """Salva dados em um arquivo no formato JSON"""
        pass

    
    @staticmethod
    def read_json(cls, file_dir: str, file_name) -> dict:
        """Le dados de um arquivo que esteja no formato JSON"""
        pass


    @staticmethod
    def read_txt(cls, file_dir: str, file_name) -> str:
        pass

    
    @staticmethod
    def write_txt(cls, file_dir: str, file_name, data) -> bool:
        pass

    @staticmethod
    def is_lock(cls, file_path: str) -> bool:
        """Verifica se o arquivo esta bloqueado para escrita."""
        pass

    
    @staticmethod
    def lock_file(cls, file_path: str) -> bool:
        """Bloqueia o arquivo, impossibilitando a escrita."""
        pass


    @staticmethod
    def unlock_file(cls, file_path: str) -> bool: 
        """Desbloqueia o arquivo, possibilitando a escrita"""