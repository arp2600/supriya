from supriya.tools.ugentools.PseudoUGen import PseudoUGen


class CompanderD(PseudoUGen):
    """
    A convenience constructor for Compander.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Dynamics UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        threshold=0.5,
        clamp_time=0.01,
        relax_time=0.1,
        slope_above=1.,
        slope_below=1.,
        ):
        """
        Constructs an audio-rate dynamics processor.

        ..  container:: example

            ::

                >>> source = ugentools.In.ar(bus=0)
                >>> compander_d = ugentools.CompanderD.ar(
                ...     source=source,
                ...     )
                >>> graph(compander_d)  # doctest: +SKIP

            ::

                >>> print(compander_d)
                synthdef:
                    name: d4e7b88df56af5070a88f09b0f8c633e
                    ugens:
                    -   In.ar:
                            bus: 0.0
                    -   DelayN.ar:
                            delay_time: 0.01
                            maximum_delay_time: 0.01
                            source: In.ar[0]
                    -   Compander.ar:
                            clamp_time: 0.01
                            control: DelayN.ar[0]
                            relax_time: 0.1
                            slope_above: 1.0
                            slope_below: 1.0
                            source: In.ar[0]
                            threshold: 0.5

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        control = ugentools.DelayN.ar(
            source=source,
            maximum_delay_time=clamp_time,
            delay_time=clamp_time,
            )
        ugen = ugentools.Compander._new_expanded(
            clamp_time=clamp_time,
            calculation_rate=calculation_rate,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            control=control,
            threshold=threshold,
            )
        return ugen
