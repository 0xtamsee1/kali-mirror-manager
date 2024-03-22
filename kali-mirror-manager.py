import re
import os
import sys
import subprocess
import threading

from operator import itemgetter
from shutil import copyfile

#MIRROR DICTIONARY
mirrors = {
    'https://kali.download/kali/':0,
    'https://mirror.kku.ac.th/kali/':0,
    'https://mirror.aktkn.sg/kali/':0,
    'https://mirror.freedif.org/kali/':0,
    'https://mirror.primelink.net.id/kali/':0,
    'https://xsrv.moratelindo.io/kali/':0,
    'https://mirrors.ustc.edu.cn/kali/':0,
    'https://mirrors.neusoft.edu.cn/kali/':0,
    'https://free.nchc.org.tw/kali/':0,
    'https://repo.jing.rocks/kali/':0,
    'https://mirrors.netix.net/kali/':0,
    'https://mirror1.sox.rs/kali/kali/':0,
    'https://mirror.cspacehostings.com/kali/':0,
    'https://ftp.riken.jp/Linux/kali/':0,
    'https://ftp.jaist.ac.jp/pub/Linux/kali/':0,
    'https://ftp.ne.jp/Linux/packages/kali/kali/':0,
    'https://ftp.yz.yamagata-u.ac.jp/pub/linux/kali/':0,
    'https://mirror.karneval.cz/pub/linux/kali/':0,
    'https://ftp.acc.umu.se/mirror/kali.org/kali/':0,
    'https://mirrors.dotsrc.org/kali/':0,
    'https://mirror.pyratelan.org/kali/':0,
    'https://mirror.init7.net/kali/':0,
    'https://mirror.netcologne.de/kali/':0,
    'https://mirror.johnnybegood.fr/kali/':0,
    'https://ftp.halifax.rwth-aachen.de/kali/':0,
    'https://ftp.nluug.nl/os/Linux/distr/kali/':0,
    'https://mirror.serverius.net/kali/':0,
    'https://ftp.belnet.be/pub/kali/kali/':0,
    'https://archive-4.kali.org/kali/':0,
    'https://mirror.vinehost.net/kali/':0,
    'https://mirror.leitecastro.com/kali/':0,
    'https://mirror.lagoon.nc/kali/':0,
    'https://mirror.2degrees.nz/kali/':0,
    'https://wlglam.fsmg.org.nz/kali/':0,
    'https://hlzmel.fsmg.org.nz/kali/':0,
    'https://mirror.0xem.ma/kali/':0,
    'https://mirror.accuris.ca/kali/':0,
    'https://mirrors.jevincanders.net/kali/':0,
    'https://mirrors.ocf.berkeley.edu/kali/':0,
    'https://kali.darklab.sh/kali/':0,
    'https://mirror.ufro.cl/kali/':0,
    'https://elmirror.cl/kali/':0,
    'https://mirror.cedia.org.ec/kali/':0,
    'https://ftp.cc.uoc.gr/mirrors/linux/kali/kali/':0,
    'https://kali.itsec.am/kali/':0,
    'https://kali.mirror1.gnc.am/kali/':0,
    'https://kali.mirror2.gnc.am/kali/':0,
    'https://fastmirror.pp.ua/kali/':0,
    'https://kali.cs.nycu.edu.tw/kali/':0,
    'https://kali.koyanet.lv/kali/':0,
    'https://md.mirrors.hacktegic.com/kali/':0,
    'https://mirror.truenetwork.ru/kali/':0,
    'https://quantum-mirror.hu/mirrors/pub/kali/':0,
    'https://mirror.amuksa.com/kali/':0,
    'http://kali.mirror.net.in/kali/':0,
    'http://ftp.free.fr/pub/kali/':0
}

# MENU
choices = {
    'menu' : 'Display commands and usage',
    'show' : 'Display the list of available mirrors',
    'ping' : 'Ping all mirrors to measure latency',
    'set' : 'Set a new mirror for package updates',
    'exit' : 'Terminate session'
}

# SOURCE.LIST BACKUP
def backUp():
    copyfile('/etc/apt/sources.list','/etc/apt/sources.list.bk')
    print()
    print("[+] Backing up source.list to '/etc/apt/sources.list.bk' ")

def check():
    backUp()
    content = []
    file = open("/etc/apt/sources.list", "r+")
    for line in file.readline():
        if re.search ('^deb http://http.kali.org/kali', line, re.I) or re.search('^deb-src http://http.kali.org/kali', line, re.I):
            newline = "#" + line
            file.write(newline)
            content.append(newline)
        elif re.search("^# Updated by https://github.com/0xtamsee1/kali-mirror-manager", line, re.I):
            break
        else:
            content.append(line)
    file.seek(0)
    file.truncate()
    file.seek(0)
    for line in content:
        file.write(line)
    file.close()

# PING MIRRORS
def pingDisplay():
    print("+---------------------------------------------------------------+-------------------------------------------------------+")
    print(("|    MIRRORS" + '\t' + "    |    LATENCY                                            |").expandtabs(60))
    print("+---------------------------------------------------------------+-------------------------------------------------------+")
    for k, v in sorted(mirrors.items(), key=itemgetter(1)):
        if v == 'R':
            print(("|    "+ k + '\t' + "    |    " + v + "\t|").expandtabs(60))
        else:
            print(("|    "+ k + '\t' + "    |    " + str(v) + " ms\t|" ).expandtabs(60))
    print ("+---------------------------------------------------------------+-------------------------------------------------------+")
    print()
    print("[+] Request Timed Out ? Try ping again")

def ping():
    print("[+] Indexing mirrors with latency")
    threads = []
    for i, repo in enumerate(mirrors):
        t = threading.Thread(target=ping_thread, args=(i, repo))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    pingDisplay()

def ping_thread(i, repo):
    try:
        temp = []
        avg = 0
        pattern = re.search(r'(//)((?:\\.|[^/\\])*)/', repo, re.I)
        url = pattern.group(2)
        result = subprocess.check_output(['ping', '-c', '3', url])
        result = result.decode('utf-8')
        temp.extend([line.rpartition('=')[-1] for line in result.splitlines()[1:-4]])
        for j in range(len(temp)):
            avg += float(temp[j][:-3])
        avg = avg / len(temp)
        mirrors[repo] = '{0:.1f}'.format(avg)
        sys.stdout.write("[+] Thread executing : {0}\r".format(i+1))
        sys.stdout.flush()
    except subprocess.CalledProcessError:
        mirrors[repo] = "Request Timed Out"
        sys.stdout.write("[+] Thread executing : {0}\r".format(i+1))
        sys.stdout.flush()

# SHOW MIRRORS
def mirrorsDisplay():
    i = 1
    print()
    print ("     +------------------------------------------------------+")
    print ("     |                       MIRRORS                        |")
    print ("     +------------------------------------------------------+")
    for repo in mirrors:
        print(("     | " + repo + "\t" + "|").expandtabs(30))
        i += 1
    print ("     +------------------------------------------------------+")

# SET MIRROR
def set(repo):
    print("[+] Updating sources.list with new mirror")
    temp = "sudo sh -c \'echo \"\n# Updated by https://github.com/0xtamsee1/kali-mirror-manager\" >> /etc/apt/sources.list\'"
    subprocess.Popen(temp, shell=True, stdout=subprocess.PIPE).stdout.read()
    line = "deb " + repo + " kali-rolling main contrib non-free"
    temp = "sudo sh -c \'echo %s >> /etc/apt/sources.list\'"
    subprocess.Popen(temp % line, shell=True, stdout=subprocess.PIPE).stdout.read()
    line = "deb-src " + repo + " kali-rolling main contrib non-free"
    temp = "sudo sh -c \'echo %s >> /etc/apt/sources.list\'"
    subprocess.Popen(temp % line, shell=True, stdout=subprocess.PIPE).stdout.read()
    print("[+] run 'apt-get update' or 'apt update' with updated source.list")

#MENU
def menu():
    print("    Python command-line tool designed to manage mirrors for a Kali Linux distribution.")
    print()
    print(("    COMMANDS" + '\t' + "DESCRIPTION").expandtabs(30))
    print()
    for key, value in choices.items():
        if key == 'set':
            print(("    " + key + ' <mirror>' '\t' + value).expandtabs(30))
        else:
            print(("    " + key + '\t' + value).expandtabs(30))
    print()
    print("    USAGE : set <mirror>")
    print("    EXAMPLE : set http://http.kali.org/kali")
    print()

#MAIN
command = []
if os.getuid()!=0:
    print("[-] Permission denied")
    sys.exit()
else:
    pass

#BANNER
print("""
    +-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+
    |K|A|L|I| |M|I|R|R|O|R| |M|A|N|A|G|E|R|
    +-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+
    https://github.com/0xtamsee1/kali-mirror-manager
""")

#COMMANDS
menu()
while True:
    command = list(map(str, input('cmd> ').split()))
    if command[0] not in choices:
        print("[-] Invalid command")
    elif command[0] == "menu":
        menu()
    elif command[0] == "show":
        mirrorsDisplay()
    elif command[0] == "ping":
        ping()
    elif command[0] == "set":
        if len(command) == 1:
            print("[-] ")
            continue
        else:
            check()
            set(command[1])
    elif command[0] == "exit":
        break
sys.exit()
