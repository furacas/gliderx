import yaml
import requests


def download_config(subscription_url):
    headers = {
        "User-Agent": "ClashX/1.0"
    }
    response = requests.get(subscription_url, headers=headers)
    response.raise_for_status()
    return response.text


def convert_clash_to_glider_config(clash_config_content):
    clash_config = yaml.safe_load(clash_config_content)
    glider_config = []

    for proxy in clash_config.get('proxies', []):
        glider_line = ""
        if proxy['type'] == 'trojan':

            # trojan as forwarder
            # forward=trojan://PASSWORD@1.1.1.1:8080[?serverName=SERVERNAME][&skipVerify=true]

            # trojanc as forwarder
            # forward=trojanc://PASSWORD@1.1.1.1:8080

            password = proxy.get('password', '')
            port = proxy.get('port', '')
            server = proxy.get('server', '')
            glider_line = f"forward=trojan://{password}:{port}@{server}?"

            skip_verify = proxy.get('skip-cert-verify','')
            if skip_verify:
                glider_line += f"&skipVerify=true"

        if proxy['type'] == 'ssr':
            # ssr as forwarder
            # forward=ssr://method:password@server:port?protocol=xxx&protocol_param=yyy&obfs=zzz&obfs_param=aaa

            method = proxy.get('cipher', '')
            password = proxy.get('password', '')
            server = proxy.get('server', '')
            port = proxy.get('port', '')
            protocol = proxy.get('protocol', '')
            protocol_param = proxy.get('protocol-param', '')
            obfs = proxy.get('obfs', '')
            obfs_param = proxy.get('obfs-param', '')

            glider_line = f"forward=ssr://{method}:{password}@{server}:{port}?"
            if protocol:
                glider_line += f"protocol={protocol}&"
            if protocol_param:
                glider_line += f"protocol_param={protocol_param}&"
            if obfs:
                glider_line += f"obfs={obfs}&"
            if obfs_param:
                glider_line += f"obfs_param={obfs_param}"

            if glider_line.endswith('&'):
                glider_line = glider_line[:-1]

        if glider_line:
            glider_config.append(glider_line)


    return glider_config


def write_glider_config(glider_config, output_path, template_path='glider.conf.template'):
    template_content = ''
    try:
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        print(f"Warning: Template file {template_path} not found. Skipping template.")

    with open(output_path, 'w') as output_file:
        if template_content:
            output_file.write(template_content)
            output_file.write("\n")

        for line in glider_config:
            output_file.write(line + "\n")


def read_config(config_file_path):
    with open(config_file_path, 'r') as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    config_file_path = "gliderx-config.yaml"
    output_path = "glider.conf"

    config = read_config(config_file_path)

    all_glider_config = []

    for subscription in config.get('subscriptions', []):
        config_content = download_config(subscription['url'])

        if subscription['type'] == 'clash':
            glider_config = convert_clash_to_glider_config(config_content)
            all_glider_config.extend(glider_config)
        # 在此处为其他订阅类型添加逻辑

    write_glider_config(all_glider_config, output_path)
    print(f"Glider configuration generated and saved to:", output_path)