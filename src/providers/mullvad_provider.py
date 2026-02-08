import logging
from .api_mullvad import ApiMullvad

logger = logging.getLogger(__name__)


class MullvadProvider:
    _PROVIDER_NAME = "Mullvad"

    # https://pt.wikipedia.org/wiki/Alian%C3%A7a_Cinco_Olhos
    FIVE_EYES = ["EUA", "UK", "CA", "AU", "NZ"]
    NINE_EYES = FIVE_EYES + ["DK", "FR", "NL", "NO"]
    FOURTEEN_EYES = NINE_EYES + ["DE", "BE", "IT", "ES", "SE"]

    ALLIANCE_COUNTRIES = {
        5: FIVE_EYES,
        9: NINE_EYES,
        14: FOURTEEN_EYES
    }

    def __init__(self):
        self._api_client = ApiMullvad

    def _fetch_servers(self) -> list:
        """Consulta a API e retorna a lista de servidores disponíveis."""
        try:
            raw_servers = self._api_client.get_servers()
            logging.info("Servidores retornados: %s", len(raw_servers))
            return raw_servers

        except Exception as err:
            logging.error(f"Falha ao buscar servidores {err}")
            return []

    def _filter_active_servers(self, raw_servers: list) -> list:
        """Filtra raw_servers e retorna apenas os servidores ativos"""
        actives = [server for server in raw_servers if server.get("active")]
        total = len(raw_servers)
        qtd_actives = len(actives)
        qtd_offlines = total - qtd_actives

        if total > 0:
            logger.debug(
                "Servidores offline: %i (%.2f%%) | ativos: %i (%.2f%%)",
                qtd_offlines,
                (qtd_offlines / total) * 100,
                qtd_actives,
                (qtd_actives / total) * 100,
            )

        return actives

    def _agroup_servers_by_country_code(self, raw_servers: list) -> dict:
        """Agrupa os servidores por país"""
        servers = {}
        for server in raw_servers:
            country = server["country_code"].upper()

            if country in servers.keys():
                servers[country].append(server)
            else:
                servers[country] = [server]

        return servers

    def _exclude_alliance_countries(self, raw_servers: list, alliance: int = 5):
        """Filtra os servidores que não fazem parte da aliança dos 5, 9 ou 14 olhos."""
        if alliance not in self.ALLIANCE_COUNTRIES:
            logger.error("Aliança selecionada invalida.")
            raise ValueError("Aliança inválida. Use 5, 9 ou 14.")

        servers = raw_servers
        blocked = self.ALLIANCE_COUNTRIES[alliance]

        clean_servers = [
            server for server in servers
            if not server.get("country_code").upper() in blocked
        ]

        return clean_servers

    def get_servers(self) -> dict:
        """Retorna um dicionário dos servidores ativos, excluindo os países da aliança e agrupados por país."""
        logger.info("Iniciando a coleta e limpeza dos dados!")
        raw_servers = self._fetch_servers()
        actives = self._filter_active_servers(raw_servers)
        no_aliance_countries = self._exclude_alliance_countries(actives)
        servers = self._agroup_servers_by_country_code(no_aliance_countries)

        return servers

    def choice_random_server(self, servers: dict) -> dict:
        """Seleciona aleatoriamente um servidor a partir do dicionário de servidores."""
        from random import choice

        country_choice = choice(list(servers.keys()))
        server = choice(servers[country_choice])

        return server
