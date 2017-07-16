from abjad.tools import sequencetools
from supriya.tools.ugentools.PseudoUGen import PseudoUGen


class Mix(PseudoUGen):
    """
    A down-to-mono signal mixer.

    ..  container:: example

        ::

            >>> with synthdeftools.SynthDefBuilder() as builder:
            ...     oscillators = [ugentools.DC.ar(1) for _ in range(5)]
            ...     mix = ugentools.Mix.new(oscillators)
            ...
            >>> synthdef = builder.build(name='mix1')
            >>> graph(synthdef)  # doctest: +SKIP

        ::

            >>> print(synthdef)
            synthdef:
                name: mix1
                ugens:
                -   DC.ar/0:
                        source: 1.0
                -   DC.ar/1:
                        source: 1.0
                -   DC.ar/2:
                        source: 1.0
                -   DC.ar/3:
                        source: 1.0
                -   Sum4.ar:
                        input_four: DC.ar/3[0]
                        input_one: DC.ar/0[0]
                        input_three: DC.ar/2[0]
                        input_two: DC.ar/1[0]
                -   DC.ar/4:
                        source: 1.0
                -   BinaryOpUGen(ADDITION).ar:
                        left: Sum4.ar[0]
                        right: DC.ar/4[0]

    ..  container:: example

        ::

            >>> with synthdeftools.SynthDefBuilder() as builder:
            ...     oscillators = [ugentools.DC.ar(1) for _ in range(15)]
            ...     mix = ugentools.Mix.new(oscillators)
            ...
            >>> synthdef = builder.build('mix2')
            >>> graph(synthdef)  # doctest: +SKIP

        ::

            >>> print(synthdef)
            synthdef:
                name: mix2
                ugens:
                -   DC.ar/0:
                        source: 1.0
                -   DC.ar/1:
                        source: 1.0
                -   DC.ar/2:
                        source: 1.0
                -   DC.ar/3:
                        source: 1.0
                -   Sum4.ar/0:
                        input_four: DC.ar/3[0]
                        input_one: DC.ar/0[0]
                        input_three: DC.ar/2[0]
                        input_two: DC.ar/1[0]
                -   DC.ar/4:
                        source: 1.0
                -   DC.ar/5:
                        source: 1.0
                -   DC.ar/6:
                        source: 1.0
                -   DC.ar/7:
                        source: 1.0
                -   Sum4.ar/1:
                        input_four: DC.ar/7[0]
                        input_one: DC.ar/4[0]
                        input_three: DC.ar/6[0]
                        input_two: DC.ar/5[0]
                -   DC.ar/8:
                        source: 1.0
                -   DC.ar/9:
                        source: 1.0
                -   DC.ar/10:
                        source: 1.0
                -   DC.ar/11:
                        source: 1.0
                -   Sum4.ar/2:
                        input_four: DC.ar/11[0]
                        input_one: DC.ar/8[0]
                        input_three: DC.ar/10[0]
                        input_two: DC.ar/9[0]
                -   DC.ar/12:
                        source: 1.0
                -   DC.ar/13:
                        source: 1.0
                -   DC.ar/14:
                        source: 1.0
                -   Sum3.ar:
                        input_one: DC.ar/12[0]
                        input_three: DC.ar/14[0]
                        input_two: DC.ar/13[0]
                -   Sum4.ar/3:
                        input_four: Sum3.ar[0]
                        input_one: Sum4.ar/0[0]
                        input_three: Sum4.ar/2[0]
                        input_two: Sum4.ar/1[0]

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def new(cls, sources):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        flattened_sources = []
        for source in sources:
            if isinstance(source, synthdeftools.UGenArray):
                flattened_sources.extend(source)
            else:
                flattened_sources.append(source)
        sources = synthdeftools.UGenArray(flattened_sources)
        summed_sources = []
        parts = sequencetools.partition_sequence_by_counts(
            sources,
            [4],
            cyclic=True,
            overhang=True,
            )
        for part in parts:
            if len(part) == 4:
                summed_sources.append(ugentools.Sum4(*part))
            elif len(part) == 3:
                summed_sources.append(ugentools.Sum3(*part))
            elif len(part) == 2:
                summed_sources.append(part[0] + part[1])
            else:
                summed_sources.append(part[0])
        if len(summed_sources) == 1:
            return summed_sources[0]
        return Mix.new(summed_sources)

    @classmethod
    def multichannel(cls, sources, channel_count):
        """
        Segment by channel count and mix down in parallel.

        ..  container:: example

            Combine panner outputs, first with first, second with second, etc.

            ::

                >>> source = ugentools.SinOsc.ar(frequency=[440, 660, 880])
                >>> panner = ugentools.PanAz.ar(
                ...     channel_count=4,
                ...     source=source,
                ...     position=ugentools.LFNoise2.kr(),
                ...     )
                >>> mix = ugentools.Mix.multichannel(panner, channel_count=4)
                >>> out = ugentools.Out.ar(bus=0, source=mix)
                >>> graph(out)  # doctest: +SKIP

            ::

                >>> print(out)
                synthdef:
                    name: fd9cb7fa733e52136a3108b9c3fe23ea
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   LFNoise2.kr:
                            frequency: 500.0
                    -   PanAz.ar/0:
                            amplitude: 1.0
                            channel_count: 4.0
                            orientation: 0.5
                            position: LFNoise2.kr[0]
                            source: SinOsc.ar/0[0]
                            width: 2.0
                    -   SinOsc.ar/1:
                            frequency: 660.0
                            phase: 0.0
                    -   PanAz.ar/1:
                            amplitude: 1.0
                            channel_count: 4.0
                            orientation: 0.5
                            position: LFNoise2.kr[0]
                            source: SinOsc.ar/1[0]
                            width: 2.0
                    -   SinOsc.ar/2:
                            frequency: 880.0
                            phase: 0.0
                    -   PanAz.ar/2:
                            amplitude: 1.0
                            channel_count: 4.0
                            orientation: 0.5
                            position: LFNoise2.kr[0]
                            source: SinOsc.ar/2[0]
                            width: 2.0
                    -   Sum3.ar/0:
                            input_one: PanAz.ar/0[0]
                            input_three: PanAz.ar/2[0]
                            input_two: PanAz.ar/1[0]
                    -   Sum3.ar/1:
                            input_one: PanAz.ar/0[1]
                            input_three: PanAz.ar/2[1]
                            input_two: PanAz.ar/1[1]
                    -   Sum3.ar/2:
                            input_one: PanAz.ar/0[2]
                            input_three: PanAz.ar/2[2]
                            input_two: PanAz.ar/1[2]
                    -   Sum3.ar/3:
                            input_one: PanAz.ar/0[3]
                            input_three: PanAz.ar/2[3]
                            input_two: PanAz.ar/1[3]
                    -   Out.ar:
                            bus: 0.0
                            source[0]: Sum3.ar/0[0]
                            source[1]: Sum3.ar/1[0]
                            source[2]: Sum3.ar/2[0]
                            source[3]: Sum3.ar/3[0]

            Compare with a non-multichannel mixdown:

                >>> mix = ugentools.Mix.new(panner)
                >>> out = ugentools.Out.ar(bus=0, source=mix)
                >>> graph(out)  # doctest: +SKIP

            ::

                >>> print(out)
                synthdef:
                    name: ac5c82bf384ab89565e859c4f948dce5
                    ugens:
                    -   SinOsc.ar/0:
                            frequency: 440.0
                            phase: 0.0
                    -   LFNoise2.kr:
                            frequency: 500.0
                    -   PanAz.ar/0:
                            amplitude: 1.0
                            channel_count: 4.0
                            orientation: 0.5
                            position: LFNoise2.kr[0]
                            source: SinOsc.ar/0[0]
                            width: 2.0
                    -   Sum4.ar/0:
                            input_four: PanAz.ar/0[3]
                            input_one: PanAz.ar/0[0]
                            input_three: PanAz.ar/0[2]
                            input_two: PanAz.ar/0[1]
                    -   SinOsc.ar/1:
                            frequency: 660.0
                            phase: 0.0
                    -   PanAz.ar/1:
                            amplitude: 1.0
                            channel_count: 4.0
                            orientation: 0.5
                            position: LFNoise2.kr[0]
                            source: SinOsc.ar/1[0]
                            width: 2.0
                    -   Sum4.ar/1:
                            input_four: PanAz.ar/1[3]
                            input_one: PanAz.ar/1[0]
                            input_three: PanAz.ar/1[2]
                            input_two: PanAz.ar/1[1]
                    -   SinOsc.ar/2:
                            frequency: 880.0
                            phase: 0.0
                    -   PanAz.ar/2:
                            amplitude: 1.0
                            channel_count: 4.0
                            orientation: 0.5
                            position: LFNoise2.kr[0]
                            source: SinOsc.ar/2[0]
                            width: 2.0
                    -   Sum4.ar/2:
                            input_four: PanAz.ar/2[3]
                            input_one: PanAz.ar/2[0]
                            input_three: PanAz.ar/2[2]
                            input_two: PanAz.ar/2[1]
                    -   Sum3.ar:
                            input_one: Sum4.ar/0[0]
                            input_three: Sum4.ar/2[0]
                            input_two: Sum4.ar/1[0]
                    -   Out.ar:
                            bus: 0.0
                            source[0]: Sum3.ar[0]

        """
        from supriya.tools import synthdeftools
        mixes, parts = [], []
        for i in range(0, len(sources), channel_count):
            parts.append(sources[i:i + channel_count])
        for columns in zip(*parts):
            mixes.append(cls.new(columns))
        return synthdeftools.UGenArray(mixes)
