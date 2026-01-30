from providers import MullvadProvider
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

API = MullvadProvider()

servers = API._fetch_servers()
API._filter_active_servers(servers)
#print(servers)
API._exclude_alliance_countries(servers)