from graphviz import Digraph
from scapy.all import rdpcap, IP, TCP, UDP, DNS, DNSQR, DNSRR

def main():
    packets = rdpcap("capture-2025-11-08.pcap")
    g = Digraph()

    ports_per_ip = {}
    edges = set()
    dns_flows = set()

    for p in packets:
        if IP in p:
            src_ip = p[IP].src
            dst_ip = p[IP].dst

            # if TCP in p:
            #     sport = str(p[TCP].sport)
            #     dport = str(p[TCP].dport)

            #     ports_per_ip.setdefault(src_ip, set()).add(sport)
            #     ports_per_ip.setdefault(dst_ip, set()).add(dport)

            #     edges.add((src_ip, sport, dst_ip, dport))
            if UDP in p:
                sport = str(p[UDP].sport)
                dport = str(p[UDP].dport)

                ports_per_ip.setdefault(src_ip, set()).add(sport)
                ports_per_ip.setdefault(dst_ip, set()).add(dport)

                edges.add((src_ip, sport, dst_ip, dport))

                if p.haslayer(DNS):
                    dns_flows.add((src_ip, sport, dst_ip, dport))

    for ip, port_set in ports_per_ip.items():
        port_fields = "|".join(f"<{p}> {p}" for p in sorted(port_set))
        label = f"{{{ip}|{port_fields}}}"
        g.node(ip, label=label, shape="record")

    for src_ip, sport, dst_ip, dport in edges:
        if (src_ip, sport, dst_ip, dport) in dns_flows:
            g.edge(f"{src_ip}:{sport}", f"{dst_ip}:{dport}", color="blue", label="DNS")
        else:
            g.edge(f"{src_ip}:{sport}", f"{dst_ip}:{dport}")

    g.render("graph_udp_dns_111", format="png")

if __name__ == "__main__":
    main()