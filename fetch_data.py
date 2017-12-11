import datadotworld as dw
import os

os.environ['DW_AUTH_TOKEN'] = (
    'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJwcm9kLXVzZXItY2xpZW50OnRyaWxvZ3l'
    'lZCIsImlzcyI6ImFnZW50OnRyaWxvZ3llZDo6ZTVkMTBkNDgtODRmYy00ZTVjLTk'
    'zNTUtMGIwOGMzYjIxNGNlIiwiaWF0IjoxNTAzMTAxNDIzLCJyb2xlIjpbInVzZXJ'
    'fYXBpX3dyaXRlIiwidXNlcl9hcGlfcmVhZCJdLCJnZW5lcmFsLXB1cnBvc2UiOnR'
    'ydWV9.HpopfqxXh0VqNgb1b8tpP6G1bkr-WblRNeS3UlhF-05sSTxx1CHJgRuAjd'
    'nP8MoBIsHsysJANP27ioXqCKChgw'
)

url = 'trilogyed/dataviz-unit-11-hwk'
download_dir = 'Resources'

if os.path.isdir(download_dir):
    print("Resources Directory Already Exists!")
    print("Please Remove the existing Resources folder and re-run this script")
    exit()

client = dw.api_client()

print("Downloading Data...")
client.download_datapackage(url, download_dir)
print("Download Complete!")
