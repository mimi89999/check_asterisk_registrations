#!/usr/bin/env python3

import argparse
import json
import requests

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3


def check_pjsip_registrations(server, username, password, number):
    ari_response = requests.get('{}/ari/endpoints/PJSIP/{}'.format(server, number), auth=(username, password))
    if ari_response.status_code == 200:
        resource_state = json.loads(ari_response.content)['state']

        if resource_state == 'online':
            return STATE_OK, 'OK: SIP number {} is online'.format(number)
        elif resource_state == 'offline':
            return STATE_CRITICAL, 'CRIT: SIP number {} is offline'.format(number)
    else:
        return STATE_UNKNOWN, 'UNKNOWN: {}'.format(ari_response.content.decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check if a SIP number is registered using Asterisk REST API.')
    parser.add_argument('number', type=int, help='SIP number to check')
    parser.add_argument('-u', '--username', required=True, help='ARI username')
    parser.add_argument('-p', '--password', required=True, help='ARI password')
    parser.add_argument('--url', default='http://127.0.0.1:5038', help='ARI base URL')

    args = parser.parse_args()
    state, message = check_pjsip_registrations(args.url, args.username, args.password, args.number)

    print(message)
    exit(state)
