# coding:utf-8
import re
import urllib3
from urllib.parse import unquote
from pathlib import Path


def downloadFileFromUrl(driver, url, destPath):
    http = urllib3.PoolManager()

    cookieString = driver.getCookieString()

    headers = {
        'Cookie': cookieString,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
    }

    r = http.request('GET',
            url,

            # make the response active like object
            preload_content = False,

            headers = headers)

    # get the filename from header
    d = r.headers['Content-Disposition']

    # handle utf8 character
    fname = unquote(re.findall(r"attachment; filename\*=utf-8\'\'(.+)",d)[0])

    Path(destPath).mkdir(parents=True, exist_ok=True)
    p = Path(destPath, fname)
    with open(p, "wb") as f:
        while True:
            chunk = r.read(500000)
            if not chunk:
                break
            f.write(chunk)
    r.release_conn()

