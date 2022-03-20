#!/bin/bash
# WANT_JSON

addr=$(cat "$1" | grep -Po '(?<="addr": ")(.*?)(?=")')
tls=$(cat "$1" | grep -Po '(?<="tls": )(.*?)(?=,)')

# return=$(curl -sIL -k "${addr}" | grep ^HTTP | tail -1)
return=$(wget --server-response --spider --quiet "${addr}" 2>&1 | grep HTTP | tail -1 | sed -r 's/^ *| *$//g')
return_code=$(echo "${return}" | cut -d' ' -f2 )
return_status=$(echo "${return}" | cut -d' ' -f3- | tr -d '\r')

if [[ "${return_code}" == '200' ]]; then
    msg="Service is available"
else
    msg="Service is not available"
fi

echo "{\"site_status\": \"$return_code\",
\"site_msg\": \"$return_status\",
\"msg\": \"$msg\"}"