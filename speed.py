import speedtest as st
from datetime import datetime


def get_new_speeds():
    speed_test = st.Speedtest()
    speed_test.get_best_server()

    ping = speed_test.results.ping
    download = speed_test.download()
    upload = speed_test.upload()

    download_mbs = round(download / (10**6), 2)
    upload_mbs = round(upload / (10**6), 2)

    return (ping, download_mbs, upload_mbs)


ping, download_mbs, upload_mbs = get_new_speeds()
result_string = "Ping = {:.2f} ms, Download speed = {:.2f} Mbps, Upload speed = {:.2f} Mbps.".format(
    ping, download_mbs, upload_mbs
)
print(result_string)
