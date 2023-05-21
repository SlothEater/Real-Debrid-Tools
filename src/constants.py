VLC_PATH = r"PATH_TO_VLC"

API_KEY = 'REAL-DEBRID-API-KEY'
HEADERS = {'Authorization': 'Bearer ' + API_KEY}
TIMEOUT = 5  # Time interval for checking download status

BASE_URL = 'https://api.real-debrid.com/rest/1.0/'

AVAILABLE_HOSTS_URL = BASE_URL + 'torrents/availableHosts'
ADD_MAGNET_URL = BASE_URL + 'torrents/addMagnet'
TORRENT_INFO_URL = BASE_URL + 'torrents/info/'
SELECT_FILES_URL = BASE_URL + 'torrents/selectFiles/'
UNRESTRICT_LINK_URL = BASE_URL + 'unrestrict/link'
