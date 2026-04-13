from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()


def _handle_ConnectionUp(event):
    log.info("Switch connected!")


def _handle_PacketIn(event):
    packet = event.parsed

    # Ignore incomplete packets
    if not packet.parsed:
        return

    ip_packet = packet.find('ipv4')

    # -------------------------------
    # 🔴 BLOCK TRAFFIC FROM h1
    # -------------------------------
    if ip_packet and str(ip_packet.srcip) == "10.0.0.1":
        log.info("BLOCKED: h1 traffic dropped")
        return

    # -------------------------------
    # 🟢 TRAFFIC CLASSIFICATION
    # -------------------------------
    if packet.find('icmp'):
        log.info("ICMP → HIGH PRIORITY")

    elif packet.find('tcp'):
        log.info("TCP → MEDIUM PRIORITY")

    else:
        log.info("OTHER → LOW PRIORITY")

    # -------------------------------
    # 📡 FORWARD PACKET
    # -------------------------------
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))

    event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)