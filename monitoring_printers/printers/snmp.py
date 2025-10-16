import asyncio
import logging

from django.conf import settings
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi.v3arch import ContextData, UdpTransportTarget, CommunityData
from pysnmp.hlapi.v3arch.asyncio import get_cmd
from pysnmp.proto.error import StatusInformation
from pysnmp.smi.rfc1902 import ObjectType, ObjectIdentity


class SNMP:
    def __init__(self):
        self.log = logging.getLogger('SNMP Python')
        self.log.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        self.loop = asyncio.new_event_loop()

        self.engine = SnmpEngine()
        self.public = CommunityData('public', mpModel=0)
        self.context = ContextData()

        self.tasks = []

    def get_value_by_oid(self, ip, oid: str, port=161):
        self.log.info(f'getting value by oid: {oid} from {ip}:{port}')
        task = self.loop.create_task(self.__get_by_oid(ip, oid, port))
        self.loop.run_until_complete(asyncio.wait([task]))
        return task.result()

    def get_bulk_value_by_oid(self, requests_data: list):
        self.log.info(f'getting bulk value by oid count: {len(requests_data)}')
        if len(requests_data) == 0:
            return []
        self.tasks = [self.loop.create_task(self.__get_by_oid(*request)) for request in requests_data]
        self.loop.run_until_complete(asyncio.wait(self.tasks))
        return [task.result() for task in self.tasks]

    def close(self):
        self.log.info('SNMP Python is shutting down')
        pending_tasks = [
            task for task in self.tasks if not task.done()]
        self.loop.run_until_complete(asyncio.gather(*pending_tasks))
        self.loop.close()

    async def __get_by_oid(self, ip, oid, port=161):
        self.log.info(f'get_by_oid({ip}, {oid})')

        response = {
            'ip': ip,
            'port': port,
            'oid': oid,
            'value': None,
            'error': '',
        }

        var_binds = ObjectType(ObjectIdentity(oid))
        try:
            error_indication, error_status, error_index, result_table = await get_cmd(
                self.engine,
                self.public,
                await UdpTransportTarget.create((ip, port),
                                                timeout=settings.SNMP_TIMEOUT,
                                                retries=settings.SNMP_RETRIES),
                self.context,
                var_binds,
            )
        except StatusInformation as ex:
            self.log.error(f'cannot fetch {oid} from {ip}: {ex}')
            response['error'] = str(ex)
            return response

        if error_indication:
            self.log.error(f'{oid} from {ip} indication: {error_indication}, '
                           f'status: {error_status}, index: {error_index}')
            response['error'] = str(error_indication)
            return response

        if not result_table:
            self.log.warning(f'no result table for {oid}')
            response['error'] = f"no result table for {oid}"
            return response

        name, val = result_table[0]
        self.log.info(f'name: {name}, value: {val}')
        response['value'] = str(val)
        return response
