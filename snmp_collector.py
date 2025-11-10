from pysnmp.hlapi import *
from prometheus_client import start_http_server, Gauge
import time

# Métricas Prometheus
cpu_usage = Gauge('device_cpu_usage', 'Uso de CPU do dispositivo (%)')
uptime = Gauge('device_uptime_seconds', 'Uptime do dispositivo (segundos)')
traffic_in = Gauge('interface_traffic_in_bytes', 'Tráfego de entrada (bytes)')
traffic_out = Gauge('interface_traffic_out_bytes', 'Tráfego de saída (bytes)')

# Configuração SNMP
DEVICE_IP = "192.168.1.1"
COMMUNITY = "public"

def get_snmp_data(oid):
    for (errorIndication, errorStatus, errorIndex, varBinds) in getCmd(
        SnmpEngine(),
        CommunityData(COMMUNITY, mpModel=0),
        UdpTransportTarget((DEVICE_IP, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    ):
        if errorIndication:
            print(errorIndication)
            return None
        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            ))
            return None
        else:
            for varBind in varBinds:
                return float(varBind[1])

def collect_metrics():
    cpu_oid = '1.3.6.1.4.1.9.2.1.57.0'  # Cisco CPU example
    uptime_oid = '1.3.6.1.2.1.1.3.0'
    in_oid = '1.3.6.1.2.1.2.2.1.10.1'
    out_oid = '1.3.6.1.2.1.2.2.1.16.1'

    cpu_usage.set(get_snmp_data(cpu_oid) or 0)
    uptime.set(get_snmp_data(uptime_oid) or 0)
    traffic_in.set(get_snmp_data(in_oid) or 0)
    traffic_out.set(get_snmp_data(out_oid) or 0)

if __name__ == '__main__':
    start_http_server(8000)
    print("Coletor SNMP em execução na porta 8000...")
    while True:
        collect_metrics()
        time.sleep(15)
