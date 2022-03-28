from datetime import datetime
from os.path import splitext




def timestapppp(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])