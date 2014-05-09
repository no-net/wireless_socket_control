from gnuradio import gr
from gnuradio import uhd
from gnuradio import blocks
from gnuradio import filter as gr_filter
from gnuradio.eng_option import eng_option


class top_block(gr.top_block):

    def __init__(self, dev_type="UHD", dev_addr="", dip_conf="10101", socket="A", func="on", gain=33):
        gr.top_block.__init__(self)

        ##################################################
        # Parameters
        ##################################################
        self.dev_type = dev_type
        self.dev_addr = dev_addr
        self.dip_conf = dip_conf
        self.func = func
        self.socket = socket
        self.gain = gain

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5e5
        ##################################################
        # Blocks
        ##################################################
        #self.init_device()
        self.device = None

        self.build_signal()

        self.gr_vector_source_x_0 = blocks.vector_source_c(self.signal, False, 1)

        self.gr_repeat_0 = blocks.repeat(gr.sizeof_gr_complex * 1, 125)
        self.gr_freq_xlating_fir_filter_xxx_0 = gr_filter.freq_xlating_fir_filter_ccf(1, (1, ), -180e3, samp_rate)

        ##################################################
        # Connections
        ##################################################
        #self.connect((self.gr_freq_xlating_fir_filter_xxx_0, 0), (self.device, 0))
        self.connect((self.gr_vector_source_x_0, 0), (self.gr_repeat_0, 0))
        self.connect((self.gr_repeat_0, 0), (self.gr_freq_xlating_fir_filter_xxx_0, 0))

    def build_signal(self):
        self.signal = []

        socket_to_dip = {"A": '10000',
                         "B": '01000',
                         "C": '00100',
                         "D": '00010',
                         "E": '00001'}

        self.binseq = self.dip_conf + socket_to_dip[self.socket]
        print self.binseq

        for bin in self.binseq:
            print bin
            for dip in bin:
                if dip == '1':
                    self.signal.extend([1, 0, 0, 0, 1, 0, 0, 0])
                elif dip == '0':
                    self.signal.extend([1, 0, 0, 0, 1, 1, 1, 0])

        if self.func == 'on':
            self.signal.extend([1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0])
        else:
            self.signal.extend([1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0])

        self.signal.extend([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.signal.extend(8 * self.signal)
        self.signal.extend(500 * [0, 0])
        #self.signal.extend(3 * self.signal)

    def pre_reconfiguration(self):
        self.lock()
        if self.device is not None:
            self.disconnect((self.gr_freq_xlating_fir_filter_xxx_0, 0), (self.device, 0))
        self.disconnect((self.gr_vector_source_x_0, 0), (self.gr_repeat_0, 0))
        self.disconnect((self.gr_repeat_0, 0), (self.gr_freq_xlating_fir_filter_xxx_0, 0))

    def after_reconfiguration(self):
        self.connect((self.gr_freq_xlating_fir_filter_xxx_0, 0), (self.device, 0))
        self.connect((self.gr_vector_source_x_0, 0), (self.gr_repeat_0, 0))
        self.connect((self.gr_repeat_0, 0), (self.gr_freq_xlating_fir_filter_xxx_0, 0))
        self.unlock()

    def set_dip_conf(self, dip_conf):
        self.pre_reconfiguration()
        self.dip_conf = dip_conf
        self.build_signal()
        self.gr_vector_source_x_0 = None
        self.gr_vector_source_x_0 = blocks.vector_source_c(self.signal, False, 1)
        self.after_reconfiguration()

    def set_func(self, func):
        self.pre_reconfiguration()
        self.func = func
        self.build_signal()
        self.gr_vector_source_x_0 = None
        self.gr_vector_source_x_0 = blocks.vector_source_c(self.signal, False, 1)
        self.after_reconfiguration()

    def set_socket(self, socket):
        self.pre_reconfiguration()
        self.socket = socket
        self.build_signal()
        self.gr_vector_source_x_0 = None
        self.gr_vector_source_x_0 = blocks.vector_source_c(self.signal, False, 1)
        self.after_reconfiguration()

    def set_gain(self, gain):
        print "set gain to", gain
        self.pre_reconfiguration()
        self.gain = gain
        if self.dev_type == "UHD":
            self.device.set_gain(self.gain, 0)
        else:
            print "Setting the gain value is not supported for HackRF!"
        self.after_reconfiguration()

    def init_device(self):
        if self.dev_type == "UHD":
            print self.dev_addr
            self.device = uhd.usrp_sink(
                device_addr=self.dev_addr,
                stream_args=uhd.stream_args(
                    cpu_format="fc32",
                    channels=range(1),
                ),
            )
            self.device.set_samp_rate(self.samp_rate)
            self.device.set_center_freq(433.97e6, 0)
            self.device.set_gain(self.gain, 0)
            self.device.set_antenna('TX/RX', 0)
        else:
            #TODO: Initialize HackRF
            print "HackRF not yet supported!"

    def set_device(self, dev_type, dev_addr):
        self.pre_reconfiguration()
        self.dev_type = dev_type
        self.dev_addr = dev_addr
        self.init_device()
        self.after_reconfiguration()
