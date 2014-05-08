from optparse import OptionParser

from gnuradio.eng_option import eng_option

from wirock_topblock import top_block


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-t", "--dev-type", dest="devtype", type="string", default="UHD",
        help="Set device type (UHD/HackRF) [default=%default]")
    parser.add_option("-u", "--usrp-addr", dest="usrp_addr", type="string", default="",
        help="Set USRP address (empty for 1st) [default=%default]")
    parser.add_option("-d", "--dip-conf", dest="dip_conf", type="string", default="10101",
        help="Set DIP config (10100) [default=%default]")
    parser.add_option("-a", "--addr", dest="addr", type="string", default="A",
        help="Set switch address (A/B/C/D) [default=%default]")
    parser.add_option("-f", "--func", dest="func", type="string", default="on",
        help="Set function (on/off) [default=%default]")
    parser.add_option("-g", "--gain", dest="gain", type="int", default=20,
        help="Set gain [default=%default]")
    (options, args) = parser.parse_args()
    tb = top_block(dev_type=options.devtype, dev_addr=options.usrp_addr, dip_conf=options.dip_conf, socket=options.addr, func=options.func)
    tb.run()
