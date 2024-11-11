# -*- coding: UTF-8 -*-
import psutil
import time


def get_network_usage(pid):
    process = psutil.Process(pid)
    net_io = process.io_counters()
    return net_io.read_bytes, net_io.write_bytes


def monitor_network_usage(pid, threshold):
    while True:
        sent, received = get_network_usage(pid)
        print(f"Bytes Sent: {sent}, Bytes Received: {received}")
        if sent > threshold or received > threshold:
            print(f"Warning: Network usage exceeded threshold! Sent: {sent}, Received: {received}")
        time.sleep(1)  # 每隔5秒检查一次


pid = 10200  # 替换为目标进程的 PID
threshold = 1024 * 40  # 1024 * 1024 * 1024  # 1GB 阈值
monitor_network_usage(pid, threshold)

