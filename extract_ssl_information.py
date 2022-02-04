import socket
import ssl


def get_dict_of_tuples(given_tuple, main_key=None):
    """
    get dictionary from tuple
    """
    split_string = str(given_tuple).split("),")
    list_of_items = []
    for ss in split_string:
        ss_and_comma = ss.replace("(", "").replace(")", "").replace("\'", "")
        list_of_items.append(ss_and_comma) if "," in ss_and_comma else None
    dict_of_tuple = {}
    for loi in list_of_items:
        split_loi = loi.split(", ", 1)
        if len(split_loi) == 2:
            x, y = split_loi
            dict_of_tuple[main_key + x.strip().capitalize()] = y.strip()
        else:
            dict_of_tuple[main_key] = split_loi[0]
    return dict_of_tuple


def get_ssl_information(hostname):
    """
    get ssl information from hostname
    """
    ssl_information = {}
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        s.connect((hostname, 443))
        cert = s.getpeercert()
        for key, value in cert.items():
            if type(value) is tuple:
                for gdt_key, gdt_value in get_dict_of_tuples(value, main_key=key).items():
                    ssl_information[gdt_key] = gdt_value
            else:
                ssl_information[key] = value
    return ssl_information


print(get_ssl_information("goal.com"))

