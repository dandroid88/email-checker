##Explanation
*  My company uses an old version of exchange that doesnt play nicely with various native email clients available for ubuntu 12.04
*  Without a full blown VM, I can only check mail via Outlook Web Access (OWA)
*  Because OWA only works correctly in IE, it falls back to OWA Light
*  :(
*  I just want to know when I have unread messages
*  This was quick and dirty, no apologies :)

##Requirements
*  Redis installed locally - yes I know extreme. I don't care, I already had it installed. Fork this or submit a pull request if you want something more sane.
*  phantomjs
*  Python libs - redis, pynotify, selenium, hashlib

##Install
*  Put this project somewhere (I put it in ~/email-checker)
*  Modify the GLOBALS
*  pip install the aforementioned python libs
*  Add a cron job
```bash
crontab -e
* * * * * export DISPLAY=:0 && python /home/dan/email-checker/check-email.py
```
