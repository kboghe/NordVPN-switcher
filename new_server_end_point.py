def get_nordvpn_servers():
    serverlist =  BeautifulSoup(requests.get("https://nordvpn.com/api/server").content,"html.parser")
    site_json=json.loads(serverlist.text)

    filtered_servers = {key: [] for key in ['windows_names','linux_names']}
    for specific_dict in site_json:
        try:
            if specific_dict['categories'][0]['name'] == 'Standard VPN servers':
                filtered_servers['windows_names'].append(specific_dict['name'])
                filtered_servers['linux_names'].append(specific_dict['domain'].split('.')[0])
        except IndexError:
            pass
    return filtered_servers
