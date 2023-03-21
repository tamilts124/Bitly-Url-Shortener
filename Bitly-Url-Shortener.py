import requests, optparse, json
from time import sleep

parser =optparse.OptionParser()

def help():
    parser.add_option('-l', '--longurl', dest='longurl', type='string', help='What the Url to Be Short? [Required]')
    parser.add_option('-a', '--account', dest='account', type='string', help='Email id (or) Username For The Account [Optional]')
    parser.add_option('-p', '--password', dest='password', type='string', help='Account Password [Optional]')

def find_all():
    if option.longurl and option.account and option.password: return 1
    elif option.longurl and option.account or option.password: return False
    elif option.longurl: return 2
    else: return False

def request_resourse(url, data={}, headers={}, method='GET', cookies={}, allow_redirects=True):
    if method.upper()=='POST': response =requests.post(url, data=data, headers=headers, cookies=cookies, allow_redirects=allow_redirects)
    else: response =requests.get(url, data=data, headers=headers, cookies=cookies, allow_redirects=allow_redirects)
    return response

def free_url_shortener(longurl):
    cookies =request_resourse('https://bitly.com').cookies
    _xsrf =cookies['_xsrf']
    while True:
        sleep(2) # wait for the server update the cookies to database
        result =request_resourse('https://bitly.com/data/anon_shorten', {'url':longurl}, {'X-Xsrftoken':_xsrf, 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}, 'POST', cookies)
        try:result =result.json()
        except Exception:continue
        else:break
    if result['status_txt']=="OK":print(f" Link: {result['data']['link']}")
    elif result['status_txt']=="RATE_LIMIT_EXCEEDED":print("> MAXIMUN LIMIT REACHED.., TRY AGAIN LATER (or) USE USER ACCOUNT!")
    elif result['status_txt']=="INVALID_ARG_URL":print("> INVALID URL, PROPARE URL NEED FOR SHORT!")
    else: print(f"> {result['status_txt']}!")

def user_url_shortener(longurl, user, password):
    _xsrf =request_resourse('https://bitly.com/').cookies['_xsrf']
    user_account =request_resourse('https://bitly.com/a/sign_in', {'rd':r'/', 'username':user, 'password':password, '_xsrf':_xsrf, 'verificaton':True}, {'X-Xsrftoken':_xsrf, 'Content-Type':'application/x-www-form-urlencoded'}, 'POST', {'_xsrf':_xsrf}, False)
    user =user_account.cookies.get('user', False)
    if not user: print('> USER ACCOUNT NOT FOUND!');return
    result =request_resourse('https://app.bitly.com/bbt2/', {}, {}, 'GET', {'_xsrf':_xsrf, 'user':user});result =result.text
    group_guid =result.split('groups: ["')[1].split('"')[0]
    json_data =json.dumps({'long_url':longurl, 'group_guid':group_guid})
    result =request_resourse('https://app.bitly.com/proxy/v4/shorten', json_data, {'X-Xsrftoken':_xsrf, 'X-Bitly-Client':'bbt2', 'Referer': 'https://app.bitly.com', 'Content-Type':'application/json'}, 'POST', {'_xsrf':_xsrf, 'user':user})
    result =result.json()
    if result.get('link', False):print(f"    Link: {result['link']}")
    elif result.get('status_text', False):
        if result['status_text']=="INVALID_ARG_LONG_URL":print("> INVALID URL, PROPARE URL NEED FOR SHORT!")
        elif result['status_text']=="RATE_LIMIT_EXCEEDED":print("> MAXIMUN LIMIT REACHED.., TRY AGAIN LATER (or) USE USER ACCOUNT!")
        else: print(f"> {result['status_text']}!")
    else: print('> SHORT URL CAN\'T RECEIVE!')

def Main():
    global option
    option =parser.parse_args()[0]
    find =find_all()
    if not find:parser.print_help();return
    print()
    if find==1:user_url_shortener(option.longurl, option.account, option.password)
    elif find==2:free_url_shortener(option.longurl)

if __name__ == '__main__':
    help();Main()