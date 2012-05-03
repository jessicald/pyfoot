from random import choice
import urllib

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]
html_types = ['text/html','application/xhtml+xml']

def choose_agent():
    return choice(user_agents)

def ajax_url(url):
    """AJAX HTML Snapshot URL parsing"""
    """ https://developers.google.com/webmasters/ajax-crawling/docs/specification """
    hashbang_index = url.find('#!')
    if hashbang_index != -1:
        base = url[:hashbang_index]
        if '?' in base:
            join = '&'
        else:
            join = '?'
        url = base + join + '_escaped_fragment_=' + urllib.quote(url[hashbang_index+2:], '=')
    return url
