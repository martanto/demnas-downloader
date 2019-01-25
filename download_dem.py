import json
import requests
import os.path
import argparse
from requests import get
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# DEMNAS Donwloader for http://tides.big.go.id/DEMNAS
class DemDownloader():

    # Constructor
    def __init__(self, pulau='sulawesi', data=None, session=None, cookies=None, login_url=None):
        self._pulau = pulau.lower()
        with open(os.getcwd()+'/json/'+self._pulau+'.json') as f:
            self._data = json.load(f)
        self._session = requests.Session()
        self._login_url = 'http://tides.big.go.id/DEMNAS/login.php'
        self._download_url = 'http://tides.big.go.id/DEMNAS/download.php?download_file=DEMNAS_'

    # Login into DEMNAS
    def login(self, username, password):
        data_login = {'user_email' : username, 
                    'user_password' : password, 
                    'login' : 'Login'}
        self._session.post(self._login_url,data=data_login)
        self._cookies = self._session.cookies
        return self

    # Starting download
    def download(self):
        for features in self._data['features']:
            nomor_peta = features['properties']['NOMOR_PETA']
            download_url = self._download_url+nomor_peta+'_v1.0.tif'
            folder = os.getcwd()+'/downloaded/'+self._pulau
            filename = 'DEMNAS_'+nomor_peta+'_v1.0.tif'
            print(download_url)
            if not os.path.exists(folder):
                os.makedirs(folder)
            if not os.path.exists(folder+'/'+filename):
                with open(folder+'/'+filename, "wb") as file:
                    retry = Retry(connect=3, backoff_factor=1)
                    adapter = HTTPAdapter(max_retries=retry)
                    self._session.mount('http://', adapter)
                    response = self._session.get(download_url, cookies={"PHPSESSID": self._cookies["PHPSESSID"]})
                    file.write(response.content)
                    if (os.path.getsize(folder+'/'+filename) < 5000):
                        return 'Gagal Download. Cek login email dan password'
        return '============ TOTAL ('+str(len(self._data['features']))+') Finish! ============'

def main():
    parser = argparse.ArgumentParser(description='DEM Downloader v1.0')
    parser.add_argument('-pulau', help='Pilihan : sumatera,jawa,kalimantan,maluku,nusa_tenggara,papua,sulawesi')
    parser.add_argument('-email', help='Masukkan alamat email yang terdaftar di DEMNAS')
    parser.add_argument('-password', help='Masukkan password')
    args = parser.parse_args()
    pulau = args.pulau
    username = args.email
    password = args.password
    dem = DemDownloader(pulau=pulau).login(username,password).download()
    print(dem)

if __name__ == '__main__':
    main()