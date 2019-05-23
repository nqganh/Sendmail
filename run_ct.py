import psutil
import sys
from subprocess import Popen

for process in psutil.process_iter():
    if process.cmdline() == ['/usr/bin/python', '/var/www/fusionpbx/esl_mail/send_mail.py']:
        sys.exit('Process found: exiting.')
Popen(['/usr/bin/python', '/var/www/fusionpbx/esl_mail/send_mail.py'])