#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import requests, re

DOCUMENTATION = r'''
---
module: healthcheck
author: Pupkin V.
short_description: healthcheck of site
description:
  - healthcheck of site with or without TLS
version_added: 1.0.0
requirements:
  - requests
  - python >= 3.6
options:
  addr:
    description:
      - Address of site we want to check
      - This is a required parameter
    type: str
  tls:
    description:
      - Whether site using certificates or not
      - Default value is 'True'
    type: bool
'''

EXAMPLES = r'''
- name: Check availability of site
  healthcheck:
    addr: mysite.example
  connection: local

- name: Check availability of site without certs
  healthcheck:
    addr: mysite.example
    tls: false
  connection: local
'''

RETURN = r'''
msg:
  description: Errors if occured
  returned: always
  type: str
  sample: ""
site_status:
  description: State status
  returned: always
  type: str
  sample: Available
rc:
  description: Return code
  returned: always
  type: int
  sample: 200
'''

def url_check(url):
  try:
      echo = requests.get(url, verify=False, timeout=60)
  except Exception as e:
      result = {
        'failed': True, 
        'rc': '1', 
        'site_status': 'Error', 
        'msg': str(e)
      }
  else:
      site_status = "Service is available" if echo.status_code == 200 else "Service is not available"
      result = {
        'failed': False, 
        'rc': '0', 
        'msg': str(site_status),
        'site_status': str(echo.status_code), 
        'site_msg': str(echo.reason),
      }
  finally:
      return result


def main():
    # Аргументы для модуля
    arguments = dict(
        addr=dict(required=True, type='str'),
        tls=dict(type='bool', default="True")
    )
    # Создаем объект - модуль
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=False
    )
    # Получаем аргументы
    addr = module.params["addr"]
    tls = module.params["tls"]


    if addr.startswith('http://') or addr.startswith('https://'):
        result = url_check(addr)
    else:
        result = {
            'failed': True, 
            'rc': '2', 
            'site_status': 'Error', 
            'msg': 'URL incorrect. Make sure you have http(s):// at the begining'
        }
    # Если задача зафейлилась
    if result['failed']:
        module.fail_json(changed=False,
                         rc=result['rc'],
                         site_status=result['site_status'],
                         msg=result['msg'])
                         
    # Если задача успешно завершилась
    else:
        module.exit_json(changed=False,
                         rc=result['rc'],
                         site_status=result['site_status'],
                         msg=result['msg'],
                         site_msg=result['site_msg'])

if __name__ == "__main__":
    main()