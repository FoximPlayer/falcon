import falcon
import os
from psutil import virtual_memory
from psutil import disk_partitions
from psutil import disk_usage
from psutil import cpu_times
from psutil import net_connections



def list_media_devices():
    with open("/proc/partitions", "r") as f:
        devices = []
        
        for line in f.readlines()[2:]: # skip header lines
            words = [ word.strip() for word in line.split() ]
            minor_number = int(words[1])
            device_name = words[3]
            
            if (minor_number % 16) == 0:
                path = "/sys/class/block/" + device_name
                
                if os.path.islink(path):
                    if os.path.realpath(path).find("/usb") > 0:
                        devices.append("/dev/" + device_name)
        
        return devices


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
    def on_get(self, req, resp):
        response = []
        for mp in ['/', '/boot']:
            disk = disk_usage(mp)
            response.append({
            'mount_point': mp,
            'device': device,
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

        }
        resp.media = response

class NetResource:
    def on_get(self, req, resp):
        net = net_connections()
        response = {
            'address': "???"

        }
        resp.media = response

api = falcon.API()
api.add_route('/mem', MemResource())
api.add_route('/disk', DiskResource())
api.add_route('/cpu', CPUResource())
api.add_route('/net', NetResource())


