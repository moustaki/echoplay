import numpy
import jack
import ao

class Player:
    def __init__(self, output='jack', numChannels = 2):
        self.numChannels = numChannels
        self.output = output
        if output == 'jack':
            # use pyjack
            import jack
            try:
                jack.get_client_name()
            except jack.NotConnectedError:
                jack.attach('remix')
                # not registering an input port makes the output sync
                # consistently break after processing 2 buffers
                # - bug in pyjack?
                jack.register_port("in_1", jack.IsInput)
                for i in range(0, self.numChannels):
                    jack.register_port("out_" + str(i+1), jack.IsOutput)
                jack.activate()
                for i in range(0, self.numChannels):
                    jack.connect("remix:out_" + str(i+1), "alsa_pcm:playback_" + str(i+1))
            self.n = jack.get_buffer_size()
            self.jackSampleRate = float(jack.get_sample_rate())
            # loosing a buffer, here, see below
            self._reset_jack()
    def play(self, audiodata):
        if self.output == 'jack':
            if self.jackSampleRate != audiodata.sampleRate:
                raise Exception('Sample rate of audio different from sample rate of Jack audio server')
            n = self.n
            input = numpy.zeros((1, n), 'f').astype('f')
            i = 0
            # converting from int16 to jack float
            output = audiodata.data.astype('f').T / 32768.0
            while i < output.shape[1] - n:
                try:
                    jack.process(output[:,i:i+n], input)
                    i += n
                except jack.InputSyncError:
                    pass
                except jack.OutputSyncError:
                    print "output lost sync while playing at " + str(i/float(audiodata.sampleRate)) + " seconds"
                    pass
            self._reset_jack()
        else:
            # use pyao
            dev = ao.AudioDevice(self.output, channels = self.numChannels, rate = audiodata.sampleRate)
            dev.play(audiodata.data, len(audiodata.data))

    def _reset_jack(self):
        # weird noise if we don't process an empty buffer
        # must look into pyjack to see what's going on
        input = numpy.zeros((1, self.n), 'f').astype('f')
        output = numpy.zeros((self.numChannels, self.n), 'f').astype('f')
        jack.process(output, input)
