import requests as re
from bs4 import BeautifulSoup as bs
import ast
import subprocess

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"}

dat = {'username': 'useradmin', 'psd': 'useradmin', 'loginSelinit': '1'}
dat1 = {"macFilterEnble": "on", "action": "sw", "bcdata": "le",
        "submit-url": "http://192.168.1.1/secu_macfilter_src.asp"}
dat2 = {"macFilterEnble": "on", "macFilterBlack": "on",
        "macFilterWhite": "off", "action": "modesw", "bcdata": "le",
        "submit-url": "http://192.168.1.1/secu_macfilter_src.asp"}

def login():
    global sc
    s.get('http://192.168.1.1/', headers=headers)
    sc = s.post('http://192.168.1.1/boaform/admin/formLogin',
                data=dat, headers=headers)


def logout():
    global sc
    s.post('http://192.168.1.1/boaform/admin/formLogout',
           headers=headers, cookies=sc.cookies)
    s.get('http://192.168.1.1/', headers=headers)
    re.Session().close()
    print('\nLogged Out')


def scan():
    return(subprocess.Popen(["sudo", "arp-scan", "--interface=wlp1s0", "--localnet"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split("\n")[2:-4])


def parse():
    global scl
    global er
    r = s.get('http://192.168.1.1/secu_macfilter_src.asp', headers=headers)
    soup = bs(r.content, 'html5lib')
    flst = soup.find("script", attrs={"type": "text/javascript"})
    er = flst.text.split(';')
    prls = list()
    scl = [i.split('\t') for i in scan()]
    sc1 = [x.split(',')[4][2:-4].replace('-', ':') for x in er if 'push' in x]
    return(scl, sc1)


def macblstat():
    flst1, whst, blst = 'OFF', 'OFF', 'OFF'
    if er[2][13:].split('=')[1].strip() == 'true':
        flst1 = 'ON'
    if er[3].split('=')[1].strip() == 'true':
        blst = 'ON'
    if er[4].split('=')[1].strip() == 'true':
        whst = 'ON'
    print(
        f'\nMac Filter [{flst1}]\nBlack List [{blst}]\nWhite List [{whst}]\n')


def macban():
    scl, sc1 = parse()
    macblstat()
    for x in scl:
        if x[1] in sc1:
            ix = '+'
        else:
            ix = ' '
        print(f"[{ix}]  {x[1]}  {x[2]}")
    s.post('http://192.168.1.1/boaform/admin/formRteMacFilter',
           data=dat1, headers=headers)
    s.post('http://192.168.1.1/boaform/admin/formRteMacFilter',
           data=dat2, headers=headers)
    ch = int(input('\nIndex to block [Note: index starts from 0]: '))
    dat3st = '{"desc": "'+scl[ch][2]+'", "mac": "'+scl[ch][1] + \
        '", "action": "ad", "submit-url": "/secu_macfilter_src.asp"}'
    dat3 = ast.literal_eval(dat3st)
    s.post('http://192.168.1.1/boaform/admin/formRteMacFilter',
           data=dat3, headers=headers)
    print(f"\nAdded {scl[ch][1]} to the mac blocklist.")


'''def macuban():
    macblstat()
    scl, _ = parse()
    s.post('http://192.168.1.1/boaform/admin/formRteMacFilter',
           data=dat1, headers=headers)
    ch = int(input('Index to unban: '))
    dat4st = '{"action": "rm","bcdata": "ld4:name1:04:desc31:(Unknown:+locally+administered)3:mac17:'++'ee","submit-url": "http://192.168.1.1/secu_macfilter_src.asp"}'''


try:
    with re.Session() as s:
        print('\nLogging In...')
        login()
        print('Logged In\n\nScanning Network for MAC addresses...\n')
        macban()
        logout()
except Exception as e:
    print(e,'\nLogging Out...')
    logout()
except KeyboardInterrupt:
    print('\nLogging Out...')
    logout()
