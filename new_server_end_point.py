def get_nordvpn_servers():
    serverlist =  BeautifulSoup(requests.get("https://api.nordvpn.com/v1/servers").content,"html.parser")
    site_json=json.loads(serverlist.text)
    filtered_servers = {'windows_names': [], 'linux_names': []}
    
    for specific_dict in site_json:
        try:
            groups = specific_dict.get('groups', [])  # Verifica se 'groups' está presente
            for group in groups:
                if group['title'] == 'Standard VPN servers':
                    filtered_servers['windows_names'].append(specific_dict['name'])
                    filtered_servers['linux_names'].append(specific_dict['domain'].split('.')[0])
                    break  # Sai do loop de grupos se encontrar a categoria desejada
        except KeyError:
            pass  # Ignora dicionários que não possuem a chave 'groups' ou 'title'

    return filtered_servers
