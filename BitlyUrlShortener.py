import cloudscraper, optparse, json, sys

parser =optparse.OptionParser()
scraper =cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})

def help():
    parser.add_option('-l', '--longurl', dest='longurl', type='string', help='What the Url to Be Short? [Required]')
    parser.add_option('-a', '--account', dest='account', type='string', help='Email id (or) Username For The Account [Optional]')
    parser.add_option('-p', '--password', dest='password', type='string', help='Account Password [Optional]')

def find_all():
    if option.longurl and option.account and option.password:return 1
    elif option.longurl and option.account or option.password:return False
    elif option.longurl:return 2
    else:return False

def request_resourse(url, data={}, headers={}, method='GET', cookies={}, allow_redirects=True):
    try:
        if method.upper()=='POST':response =scraper.post(url, data=data, headers=headers, cookies=cookies, allow_redirects=allow_redirects)
        else:response =scraper.get(url, data=data, headers=headers, cookies=cookies, allow_redirects=allow_redirects)
        return response
    except Exception as e:print(e);sys.exit(1)

def free_url_shortener(longurl):
    _xsrf =request_resourse('https://bitly.com/').cookies['_xsrf']
    while True:
        result =request_resourse('https://bitly.com/data/anon_shorten', {'url':longurl}, {'X-Xsrftoken':_xsrf, 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}, 'POST', {'_xsrf':_xsrf})
        try:result =result.json()
        except Exception:continue
        else:break
    if result['status_txt']=="OK":print(f"    Link: {result['data']['link']}");Thank()
    elif result['status_txt']=="RATE_LIMIT_EXCEEDED":print("    MAXIMUN LIMIT REACHED.., TRY AGAIN LATER (or) USE USER ACCOUNT!");Thank()
    elif result['status_txt']=="INVALID_ARG_URL":print("    INVALID URL, PROPARE URL NEED FOR SHORT!");Thank()
    else: print(f"    {result['status_txt']}!");Thank()

def user_url_shortener(longurl, user, password):
    _xsrf =request_resourse('https://bitly.com/').cookies['_xsrf']
    user_account =request_resourse('https://bitly.com/a/sign_in', {'rd':r'/', 'username':user, 'password':password, '_xsrf':_xsrf, 'verificaton':True}, {'X-Xsrftoken':_xsrf, 'Content-Type':'application/x-www-form-urlencoded'}, 'POST', {'_xsrf':_xsrf}, False)
    user =user_account.cookies.get('user', False)
    if not user:print('    USER ACCOUNT NOT FOUND!');return
    result =request_resourse('https://app.bitly.com/bbt2/', {}, {}, 'GET', {'_xsrf':_xsrf, 'user':user});result =result.text
    group_guid =result.split('groups: ["')[1].split('"')[0]
    json_data =json.dumps({'long_url':longurl, 'group_guid':group_guid})
    result =request_resourse('https://app.bitly.com/proxy/v4/shorten', json_data, {'X-Xsrftoken':_xsrf, 'X-Bitly-Client':'bbt2', 'Referer': 'https://app.bitly.com', 'Content-Type':'application/json'}, 'POST', {'_xsrf':_xsrf, 'user':user})
    result =result.json()
    if result.get('link', False):print(f"    Link: {result['link']}");Thank()
    elif result.get('status_text', False):
        if result['status_text']=="INVALID_ARG_LONG_URL":print("    INVALID URL, PROPARE URL NEED FOR SHORT!");Thank()
        elif result['status_text']=="RATE_LIMIT_EXCEEDED":print("    MAXIMUN LIMIT REACHED.., TRY AGAIN LATER (or) USE USER ACCOUNT!");Thank()
        else: print(f"    {result['status_text']}!");Thank()
    else: print('    SHORT URL CAN\'T RECEIVE!');Thank()

def Thank():
    print();print()
    print('    /////////////////////////////////////////////////////')
    print('    /////// For More Follow In Github @tamilts124 ///////')
    print('    /////////////////////////////////////////////////////')

def Main():
    global option
    try:
        option =parser.parse_args()[0]
        find =find_all()
        if not find:parser.print_help();return
        print()
        if find==1:user_url_shortener(option.longurl, option.account, option.password)
        elif find==2:free_url_shortener(option.longurl)
    except KeyboardInterrupt:Thank()
    print()

if __name__ == '__main__':
    help();Main()
