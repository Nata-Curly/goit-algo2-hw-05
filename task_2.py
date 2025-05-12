import time
import re
from hyperloglog import HyperLogLog
import pandas as pd


def load_ip_addresses(filepath):
    """
    Loads IP addresses from the given file.

    :param filepath: path to a file containing IP addresses
    :return: a list of IP addresses found in the file
    """
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    ip_addresses = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            match = ip_pattern.search(line)
            if match:
                ip_addresses.append(match.group())
    return ip_addresses


def exact_unique_count(ip_list):
    """
    Counts the number of unique IP addresses in the given list using the set data structure.

    :param ip_list: a list of IP addresses
    :return: a tuple containing the number of unique IP addresses and the time taken to count them
    """

    start = time.time()
    unique_ips = set(ip_list)
    duration = time.time() - start
    return len(unique_ips), duration


def hyperloglog_unique_count(ip_list, p=14):
    """
    Counts the number of unique IP addresses in the given list using HyperLogLog.

    :param ip_list: a list of IP addresses
    :param p: the precision parameter for HyperLogLog (default: 14)
    :return: a tuple containing an estimated number of unique IP addresses and the time taken to count them
    """
    hll = HyperLogLog(p=p)
    start = time.time()
    for ip in ip_list:
        hll.add(ip)
    estimated = hll.count()
    duration = time.time() - start
    return estimated, duration


if __name__ == "__main__":
    filepath = "lms-stage-access.log"
    ip_list = load_ip_addresses(filepath)

    exact_count, exact_time = exact_unique_count(ip_list)
    hll_count, hll_time = hyperloglog_unique_count(ip_list)

    df = pd.DataFrame(
        {
            "Метод": ["Точний підрахунок", "HyperLogLog"],
            "Унікальні елементи": [exact_count, round(hll_count)],
            "Час виконання (сек.)": [round(exact_time, 4), round(hll_time, 4)],
        }
    )

    print("\nРезультати порівняння:")
    print(df.to_string(index=False))
