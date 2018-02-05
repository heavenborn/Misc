import ts3
import csv


def ts3_scanner():
    """Scans the typefrag servers for the old dreamteam"""


    ips = []
    ports = 5000
    with open('urls.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            ips.append(row[1][:])
            #print(ips[0])


    for i in ips:
        with ts3.query.TS3Connection(i) as ts3conn:
            while ports < 6000:
                try:

                    ts3conn.use(port=ports)
                    print("Trying URL " + i)
                    print("Trying port number: " + str(ports))
                    ts3conn.clientlist()
                    resp = ts3conn.clientlist()
                    for client in resp.parsed:
                        if "Namek" or "Asator" in client['client_nickname']:
                            print("-----------FOUND------------ ")
                            print(i)
                            print(ports)

                        else:
                            print("Nothing here, moving on.")
                            ports += 1

                except ts3.query.TS3QueryError:
                    print("Error Moving on")
                    ports += 1
                    ts3conn.logout()
            if ports == 6000:
                ports = 5000


ts3_scanner()
