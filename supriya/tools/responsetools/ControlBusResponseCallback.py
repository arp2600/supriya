# -*- encoding: utf-8 -*-
from supriya.tools.osctools.OscCallback import OscCallback


class ControlBusResponseCallback(OscCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import servertools
        OscCallback.__init__(
            self,
            address_pattern='/c_(set|setn)',
            procedure=self.__call__,
            )
        assert isinstance(server, servertools.Server)
        self._server = server

    ### SPECIAL METHODS ###

    def __call__(self, message):
        from supriya.tools import responsetools
        response = responsetools.ResponseManager.handle_message(message)
        if not isinstance(response, tuple):
            response = (response,)
        for x in response:
            bus_id = x.bus_id
            bus_proxy = self._server._get_control_bus_proxy(bus_id)
            bus_proxy.handle_response(x)
