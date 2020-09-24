import iptc


def add_target_rule(chain, port, source_ip="0.0.0.0/0", target_ip="0.0.0.0/0", target="ACCEPT",
                    interface="*", protocol="tcp"):
    """
    添加一条防火墙规则
    :param chain:
    :param port:
    :param source_ip:
    :param target_ip:
    :param target:
    :param interface:
    :param protocol:
    :return:
    """
    rule = iptc.Rule()
    rule.protocol = protocol
    target = iptc.Target(rule, target)
    rule.target = target
    match = iptc.Match(rule, protocol)
    rule.add_match(match)

    if chain == "INPUT":
        rule.in_interface = interface
        rule.src = source_ip
        match.dport = port
    else:
        rule.out_interface = interface
        rule.des = target_ip
        match.sport = port
    _chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain)
    return _chain.insert_rule(rule)


def get_rule_line_num_by_args(chain, port=None, source_ip=None, target_ip=None, target=None, interface=None,
                              protocol=None):
    """
    给定条件，获取符合条件的规则的行号
    :param chain:
    :param port:
    :param source_ip:
    :param target_ip:
    :param target:
    :param interface:
    :param protocol:
    :return:
    """
    rule_list = iptc.easy.dump_chain('filter', chain=chain, ipv6=False)
    if chain == "INPUT":
        port_key = "dport"
        interface_key = "in-interface"
    else:
        port_key = "sport"
        interface_key = "out-interface"

    if source_ip == "0.0.0.0/0":
        source_ip = None

    if target_ip == "0.0.0.0/0":
        target_ip = None

    for rule in rule_list:
        if rule.get('protocol') != protocol:
            continue
        elif rule.get(interface_key) != interface:
            continue
        elif rule.get(protocol) and rule[protocol].get(port_key) != port:
            continue
        elif not ((rule.get("src") and source_ip and str(source_ip) in rule.get("src")) or (
                not rule.get("src") and not source_ip)):
            continue
        elif not ((rule.get("dst") and target_ip and str(target_ip) in rule.get("dst")) or (
                not rule.get("dst") and not target_ip)):
            continue
        elif rule.get("target") != target:
            continue
        else:
            return rule_list.index(rule) + 1
    return 0
