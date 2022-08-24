import requests, os, netifaces, socket, sys
from concurrent.futures import ThreadPoolExecutor


if hasattr(sys, 'getwindowsversion'):
    clearScreen = lambda: os.system('cls')
else:
    clearScreen = lambda: os.system('clear')
################################################################################

def setWindow(title, cols, lines):
    os.system('title '+title+' && mode con: cols='+str(cols))
################################################################################

def PrintSeparator():
    print('='*70)
################################################################################

def GetDefaultGateway():

    gateways = netifaces.gateways()
    if 'default' in gateways and netifaces.AF_INET in gateways['default']:
        return gateways['default'][netifaces.AF_INET][0]
################################################################################

def TestPortNumber(host, port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        try:
            sock.connect((host, port))
            return True
        except:
            return False
################################################################################

def SearchLocalAddress():

    retIP = []
    ip_gateway = GetDefaultGateway()

    #print("Gateway default ip:\t" + ip_gateway)

    ip_splt = ip_gateway.split('.')
    ip_splt = ip_splt[0] + '.' + ip_splt[1] + '.' + ip_splt[2] + '.'

    print(f'Ricerca nel range:\t' + ip_splt + '0/255\n' )

    hosts = []
    for i in range(0, 255):
        hosts.append(ip_splt + str(i))

    ports = [80]*len(hosts)

    with ThreadPoolExecutor(len(hosts)) as executor:
        results = executor.map(TestPortNumber, hosts, ports)

        for ip,is_open in zip(hosts,results):
            if is_open:
                retIP.append(ip)
                print("> Online: " + ip + '\t'+ HttpGetRequest(ip))

    PrintSeparator()
    return retIP
################################################################################

def HttpGetRequest(host):

    url = "http://" + host
    r = requests.get(url)
    stato = ""

    if r.status_code == 200:
        stato = "<==[ Accessibile da browser"
    elif r.status_code == 401:
        stato = "<==[ Autenticazione richiesta"
    else:
        stato = ""

    return stato
################################################################################

def PortScan(host, ports):

    retPorts = []
    serviceName = ""
    print(f'Scansione porte {host}...\n')

    with ThreadPoolExecutor(len(ports)) as executor:
        results = executor.map(TestPortNumber, [host]*len(ports), ports)

        for port,is_open in zip(ports,results):
            if is_open:
                try:
                    serviceName = socket.getservbyport(port, 'tcp');
                except:
                    serviceName = ""

                if serviceName == "rtsp":
                    data=[]
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sk:
                        sk.settimeout(3)
                        try:
                            sk.connect((host, port))
                            sk.sendall(b".")
                            buff = sk.recv(1024)

                            if len(buff) > 10:
                                data = str(buff)
                                data = data.split('\\r\\n')

                                if len(data) >= 3:
                                    serviceName = "RTSP <==[ "+ data[2]
                        except socket.error as err:
                                pass


                    #serviceName = serviceName + " <==[ IP CAMERA"

                retPorts.append(port)
                if port == 80:
                    st = HttpGetRequest(host)
                    print(f'> Porta: 80 ' + '\t' + serviceName + ' ' + st )
                else:
                    print(f'> Porta: {port} ' + '\t' + serviceName)
    PrintSeparator()
    return retPorts
################################################################################
setWindow("", 70, 40)
clearScreen()
print('█'*70)

print("""████████████ < SRL > (Scansione Rete Locale) Ver. 1.0.1b █████████████
██████████████████████████████████████████████████████████████████████
INFORMAZIONI:

    1) Ricava la terna della rete locale in base..
        all'ip del gateway sulla scheda di rete (di default).

    2) Scansiona l'intera terna (0/255) cercando ip con la..
        porta 80 aperta.

    3) Su ogni ip che trova dai passaggi precedenti effettua..
        un port scan sul range 0/9999.
""")

print('█'*70)

addrs = SearchLocalAddress()
ports = range(9999)
found = []

for addr in addrs:
    ret = PortScan(addr, ports)
    found.append([addr, ret])
