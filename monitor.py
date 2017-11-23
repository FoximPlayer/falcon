import falcon
import os
import socket
import psutil
import netifaces
from psutil import virtual_memory
from psutil import disk_partitions
from psutil import disk_usage
from psutil import cpu_times
from psutil import net_if_addrs
from subprocess import Popen, PIPE

for iface4 in netifaces.interfaces():
    for iftype, data in netifaces.ifaddresses(iface4).items():
        if iftype in (netifaces.AF_INET, netifaces.AF_INET):
            for info4 in data:
                ip4 = (info4['addr'])

for iface6 in netifaces.interfaces():
    for iftype, data in netifaces.ifaddresses(iface6).items():
        if iftype in (netifaces.AF_INET, netifaces.AF_INET6):
            for info6 in data:
                ip6 = (info6['addr'])





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
        'idle': cpu. idle,
        'iowait': cpu.iowait,
        'irq': cpu.irq,
        'softirq': cpu.softirq,
        'steal': cpu.steal,
        'guest': cpu.guest,
        'nice': cpu.nice,
        'number_of_cpu': psutil.cpu_count(),
        'xload': "here must be uptime"
        }
        resp.media = response


class NetResource:
    def on_get(self, req, resp):
        net = net_if_addrs()
        response = {
            'family': socket.AF_INET,
            'IPv4_address': ip4,
            'IPv6_address': ip6,
            }
        resp.media = response

api = falcon.API()
api.add_route('/mem', MemResource())
api.add_route('/disk', DiskResource())
api.add_route('/cpu', CPUResource())
api.add_route('/net', NetResource())


