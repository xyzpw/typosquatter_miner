#!/usr/bin/env python3
import requests, itertools, argparse

parser = argparse.ArgumentParser()

parser.add_argument("--silent", action="store_true", help="Don't print scanned domains")

args = parser.parse_args()

active_domains = []

typo_urls = []
scanned_count = 0
class Main:
    def gen_typos(uri):
        for s in itertools.permutations(uri):
            current_typo = ''.join(s)
            current_uri = f"https://{current_typo}{tld}"
            typo_urls.append(current_uri)
        typo_urls.remove(f"https://{uri}{tld}")

    def get_domain(domain):
        global timeout
        packet = requests.get(domain, headers={"user-agent": "typosquatting_miner"}, timeout=timeout)
        return packet

url = input("https://")
tld = url[url.find("."):]
url = url[:url.find(".")]
timeout = int(input("Timeout (ms): ")); timeout /= 1e+3
Main.gen_typos(url)

if args.silent:
    print(f"\nScanning for {len(typo_urls):,} domains\n")
    for domain in typo_urls:
        try:
            packet = Main.get_domain(domain)
            scanned_count += 1
            if packet.status_code != 404:
                print(f"\033[2KScanned {len(active_domains)} / {scanned_count}", end='\r')
                active_domains.append(domain)
            else:
                print(f"\033[2KScanned {len(active_domains)} / {scanned_count}", end='\r')
        except KeyboardInterrupt:
            print("\nTerminating script...\n")
            exit(', '.join(active_domains))
        except requests.exceptions.ConnectionError:
            scanned_count += 1
            print(f"\033[2KScanned {len(active_domains)} / {scanned_count}", end='\r')
        except:
            pass
    exit(', '.join(active_domains))
else:
    print(f"\nScanning for {len(typo_urls):,} domains\n")
    for domain in typo_urls:
        try:
            packet = Main.get_domain(domain)
            if packet.status_code != 404:
                print(f"{domain} => {packet.url} {packet}")
                active_domains.append(domain)
            else:
                print(f"{domain} - Not found!")
        except KeyboardInterrupt:
            print("\nTerminating script...\n")
            exit(', '.join(active_domains))
        except requests.exceptions.ConnectionError:
            print(f"{domain} - Not found!")
        except Exception as e:
            pass
    print()
    exit(', '.join(active_domains))