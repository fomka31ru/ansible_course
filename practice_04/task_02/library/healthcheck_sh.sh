#!/bin/bash
# WANT_JSON

addr=$(cat "$1" | grep -Po '(?<="addr": ")(.*?)(?=")')
tls=$(cat "$1" | grep -Po '(?<="tls": )(.*?)(?=,)')

# return=$(curl -sIL -k "${addr}" | grep ^HTTP | tail -1)
return=$(wget --server-response --no-check-certificate --spider --quiet "${addr}" 2>&1 | grep HTTP | tail -1 | sed -r 's/^ *| *$//g')
return_code=$(echo "${return}" | cut -d' ' -f2 )
return_status=$(echo "${return}" | cut -d' ' -f3- | tr -d '\r')

if [[ "${return_code}" == '200' ]]; then
    msg="Service is available";
    rc="0"
else
    msg="Service is not available";
    rc="1"
fi

echo "{\"site_status\": \"$return_code\",
\"site_msg\": \"$return_status\",
\"msg\": \"$msg\",
\"rc\": \"$rc\"}"