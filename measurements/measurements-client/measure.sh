#!/bin/bash

# Number of measurements
count=10

# Regular host
host="34.229.200.55"

# Onion service
onion="fdy6szsebmu56buihzafvcquorjxvu73625ckrqz6sfyv5jrrgnnzlid.onion"

single_onion="nk42uw3h2xq7igdy6l6eeescpnd3og2nl55aryvhpypmrcjxq6w7lfyd.onion"

# Tor proxy settings
tor_proxy="127.0.0.1:9150"

echo "Measuring latency for regular host: $host"
regular_total_ns=0
for i in $(seq 1 $count); do
    start=$(date +%s%N | sed 's/N$//')  # Remove trailing N if present
    ping -c 1 $host > /dev/null 2>&1
    end=$(date +%s%N | sed 's/N$//')
    latency_ns=$((end - start))
    echo "Latency $i: $latency_ns ns"
    regular_total_ns=$((regular_total_ns + latency_ns))
done
regular_avg_ns=$((regular_total_ns / count))
echo "Average latency for $host: $regular_avg_ns ns"

echo "Measuring latency for onion service: $onion"
onion_total_ns=0
for i in $(seq 1 $count); do
    start=$(date +%s%N | sed 's/N$//')
    curl --socks5-hostname $tor_proxy -o /dev/null -s "$onion"
    end=$(date +%s%N | sed 's/N$//')
    latency_ns=$((end - start))
    echo "Latency $i: $latency_ns ns"
    onion_total_ns=$((onion_total_ns + latency_ns))
done
onion_avg_ns=$((onion_total_ns / count))
echo "Average latency for $onion: $onion_avg_ns ns"

echo "Measuring latency for single onion service: $single_onion"
single_onion_total_ns=0
for i in $(seq 1 $count); do
    start=$(date +%s%N | sed 's/N$//')
    curl --socks5-hostname $tor_proxy -o /dev/null -s "$single_onion"
    end=$(date +%s%N | sed 's/N$//')
    latency_ns=$((end - start))
    echo "Latency $i: $latency_ns ns"
    single_onion_total_ns=$((single_onion_total_ns + latency_ns))
done
single_onion_avg_ns=$((single_onion_total_ns / count))
echo "Average latency for $single_onion: $single_onion_avg_ns ns"

echo "Latency difference (regular to onion): $((onion_avg_ns - regular_avg_ns)) ns"
