import socket
import nmap
from wolfpack.beta.settings import PORT as alpha_port


def get_network_ip():
    '''Get local IP address'''

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    return s.getsockname()[0]


def get_alpha_addr():
    '''Find & get IP address of alpha in the local network'''

    alpha_ip = ''
    nm = nmap.PortScanner()

    # it will probably take a while
    nm.scan('%s/24' % get_network_ip(), str(alpha_port))
    for host in nm.all_hosts():
        if nm[host].state() == 'up' and nm[host]['tcp'][alpha_port]['state'] == 'open':
            alpha_ip = host
            break

    if not alpha_ip:
        raise Exception, 'Alpha not found'

    return (alpha_ip, alpha_port)
