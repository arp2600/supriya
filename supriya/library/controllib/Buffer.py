# -*- encoding: utf-8 -*-
from supriya.library.controllib.ServerObjectProxy import ServerObjectProxy


class Buffer(ServerObjectProxy):
    r'''A buffer.

    ::

        >>> from supriya import controllib
        >>> stereo_buffer = controllib.Buffer(
        ...     frame_count=1024,
        ...     channel_count=2,
        ...     )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_number',
        '_channel_count',
        '_frame_count',
        )

    ### INITIALIZER ###

    def __init__(self, frame_count=512, channel_count=1):
        ServerObjectProxy.__init__(self)
        assert 0 < frame_count
        assert 0 < channel_count
        self._frame_count = int(frame_count)
        self._channel_count = int(channel_count)

    ### PUBLIC METHODS ###

    def allocate(self, server_session=None):
        ServerObjectProxy.allocate(self)

    def free(self):
        ServerObjectProxy.free(self)

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def frame_count(self):
        return self._frame_count
