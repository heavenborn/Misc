import ts3
import time
import _thread
from requests import get


def online_users():
        """Shows who is online, and thier mic status"""
        resp = ts3conn.clientlist(voice=True)

        for client in resp.parsed:
            if client['client_input_muted'] == '1':
                print(client['client_nickname'] + ' is muted')
            elif client['client_input_muted'] == '0':
                print(client['client_nickname'] + ' is not muted')
        for client in resp.parsed:
            print(client)

def weather():
    """gets current weather for the user that requested it"""

    if event[0]['msg'] == '!weather':

        user = ts3conn.clientinfo(clid=event[0]['invokerid'])

        #for us in user:
        ip = user[0]['connection_client_ip']
        latlong = get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')

        weather = get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=7965aa8bea9cc9d62311210c63f92592'.format(latlong[0], latlong[1])).json()
        #print(weather)
        #print(weather['weather'][0]['main'])
        #print(weather['main']['temp'] * (9/5) - 459.67)
        cond = weather['weather'][0]['main']
        temp = weather['main']['temp'] * (9/5) - 459.67  # Converts kelvin to freedom units
        cond = str(cond)
        temp = str(temp)
        msg = 'Conditions: ' + cond + ', Temperature: ' + temp
        print(msg)
        ts3conn.clientpoke(msg=str(msg), clid=event[0]['invokerid'])

with ts3.query.TS3Connection("jewishwarriorsinc.typefrag.com") as ts3conn:
    ts3conn.login(
        client_login_name=" ",
        client_login_password=" "
    )
    ts3conn.use(port=5670)
    ts3conn.servernotifyregister(event='textserver')


    while True:
        ts3conn.send_keepalive()
        #event = ts3conn.wait_for_event()
        try:
            # This method blocks, but we must sent the keepalive message at
            # least once in 10 minutes. So we set the timeout parameter to
            # 9 minutes.

            event = ts3conn.wait_for_event(timeout=3600)

        except ts3.query.TS3TimeoutError:

            pass
        else:
            weather()

