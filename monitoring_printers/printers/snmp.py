import asyncio
import logging

from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi.v3arch import ContextData, UdpTransportTarget, CommunityData
from pysnmp.hlapi.v3arch.asyncio import get_cmd
from pysnmp.proto.error import StatusInformation
from pysnmp.smi.rfc1902 import ObjectType, ObjectIdentity


class SNMP:
    def __init__(self):
        self.log = logging.getLogger('SNMP Python')
        self.loop = asyncio.get_event_loop()

        self.engine = SnmpEngine()
        self.public = CommunityData('public')
        self.context = ContextData()

    def get_value_by_oid(self, ip, oid: str, port=161):
        task = self.loop.create_task(self.__get_by_oid(ip, oid, port))
        self.loop.run_until_complete(asyncio.wait([task]))
        return task.result()

    async def __get_by_oid(self, ip, oid: str, port=161):
        self.log.debug(f'get_by_oid({ip}, {oid})')
        var_binds = ObjectType(ObjectIdentity(oid))
        try:
            error_indication, error_status, error_index, result_table = await get_cmd(
                self.engine,
                self.public,
                await UdpTransportTarget.create((ip, port)),
                self.context,
                var_binds,
            )
        except StatusInformation as ex:
            self.log.error(f'cannot fetch {oid} from {ip}: {ex}')
            return None

        if error_indication:
            self.log.error(f'Indication: {error_indication}, status: {error_status}, index: {error_index}')
            return None

        if result_table:
            name, val = result_table[0]
            self.log.debug(f'name: {name}, value: {val}')
            return val
        else:
            self.log.warning(f'no result table for {oid}')
            return None