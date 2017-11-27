import falcon
import os
import socket
import psutil
import netifaces
import re
from psutil import virtual_memory
from psutil import disk_partitions
from psutil import disk_usage
from psutil import cpu_times
from psutil import net_if_addrs, net_io_counters
from subprocess import Popen, PIPE

for iface4 in netifaces.interfaces():
    for iftype, data in netifaces.ifaddresses(iface4).items():
        if iftype in (netifaces.AF_INET, netifaces.AF_INET):
            for info4 in data:
                IPv4 = (info4['addr'])
                netmaskIPv4 = (info4['netmask'])

for iface6 in netifaces.interfaces():
    for iftype, data in netifaces.ifaddresses(iface6).items():
        if iftype in (netifaces.AF_INET, netifaces.AF_INET6):
            for info6 in data:
                IPv6 = (info6['addr'])
                netmaskIPv6 = (info6['netmask'])

for ifacemac in netifaces.interfaces():
    for iftype, data in netifaces.ifaddresses(ifacemac).items():
        if iftype in (netifaces.AF_LINK, netifaces.AF_LINK):
            for infomac in data:
                mac = (infomac['addr'])


nazwy = ['interface',
         'bytes_in','packets_in','errs_in','drop_in','fifo_in','frame_in','compressed_in','multicast_in',
        'bytes_out','packets_out','errs_out','drop_out','fifo_out','frame_out','compressed_out','multicast_out']

result = {}
for linia in open('/proc/net/dev').readlines():
    linia = linia[:-1]
    m = re.match("\s*(\w+):\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",linia)
    if m:
        wynik = dict(zip(nazwy, m.groups()))
        result[wynik['interface']] = wynik

class MemResource:
    def on_get(self, req, resp):
        mem = virtual_memory()
        response = {
            'free': mem.free,
            'total': mem.total,
            'cached': mem.cached,
            'active': mem.active,
            'percent': mem.percent,
            'available': mem.available,
            'used': mem.used,
            'inactive': mem.inactive,
            'buffers': mem.buffers,
            'shared': mem.shared,

        }
        resp.media = response

class DiskResource:
    def __init__(self):
        self.devices = []
        with Popen(["mount"], stdout=PIPE) as proc:
            out = proc.stdout.read()
        lines = out.decode("utf-8").split('\n')
        for l in lines:
            if l[0:4] == '/dev':
                ch = l.split(' ')

                device = (ch[0],ch[2], ch[4],)
                self.devices.append(device)

    def on_get(self, req, resp, ):
        response = []
        for device in self.devices:
            mp = device[1]
            disk = disk_usage(mp)
            response.append({
                'mount_point': mp,
                'device': device[0],
                'fstype': device[2],
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent_used': disk.percent
            })
        resp.media = response

class CPUResource:
    def on_get(self, req, resp):
        cpu = cpu_times()
        response = {
            'user': cpu.user,
            'nice': cpu.nice,
            'system': cpu.system,
            'idle': cpu.idle,
            'iowait': cpu.iowait,
            'irq': cpu.irq,
            'softirq': cpu.softirq,
            'steal': cpu.steal,
            'guest': cpu.guest,
            'nice': cpu.nice,
            'number_of_cpu': psutil.cpu_count(),
            'load_avg': os.getloadavg(),
        }
        resp.media = response


class NetResource:
    def on_get(self, req, resp):
        net = net_if_addrs()
        net = net_io_counters(pernic=True)    
        response = {
            'family': socket.AF_INET,
            'addr_IPv6': IPv6,
            'addr_IPv4': IPv4,
            'addr_mac': mac,
            'IPv4_netmask': netmaskIPv4,
            'IPv6_netmask': netmaskIPv6,
            'byte': result
            }
        resp.media = response

class SysinfoResource:
    def on_get(self, req, resp):
        sys = psutil.users()
        response = {
            'boot_time': psutil.boot_time(),
            'user': psutil.users()[0].name,
            'terminal': psutil.users()[0].terminal,
            'host': psutil.users()[0].host,
            'started': psutil.users()[0].started,
            'pid': psutil.users()[0].pid,
            }
        resp.media = response

api = falcon.API()
api.add_route('/mem', MemResource())
api.add_route('/disk', DiskResource())
api.add_route('/cpu', CPUResource())
api.add_route('/net', NetResource())
api.add_route('/sys', SysinfoResource())
