#!/usr/bin/env bash

for file in */*/log.jtl; do
    start=$(head -n 2 "${file}" | tail -n 1 |  sed -En 's#([0-9]{10}).*#\1000#p')
    end=$(
        tail -n 1 "${file}"| sed -En 's#([0-9]{10}).*#\1000#p'
    )
    echo "${file} : http://localhost:3000/d/azDLI144k/jvm-micrometer?orgId=1&from=${start}&to=${end}"
done
