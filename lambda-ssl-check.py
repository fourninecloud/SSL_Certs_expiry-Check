
import socket
import ssl, boto3
import re,sys,os,datetime

def ssl_expiry_date(domainname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=domainname,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)
    conn.connect((domainname, 443))
    ssl_info = conn.getpeercert()
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt).date()

def ssl_valid_time_remaining(domainname):
    """Number of days left."""
    expires = ssl_expiry_date(domainname)
    return expires - datetime.datetime.utcnow().date()

def sns_Alert(dName, eDays, sslStatus):
    sslStat = dName + ' SSL certificate will be expired in ' + eDays +' days!! '
    snsSub = dName + ' SSL Certificate Expiry ' + sslStatus + ' alert'
    print sslStat
    print snsSub
    response = client.publish(
    TargetArn="arn:aws:sns:ap-southeast-1:41367:ssl-expiry-alerts",
    Message= sslStat,
    Subject= snsSub
    )
    
    
#####Main Section
client = boto3.client('sns')
def lambda_handler(event, context):
    f = ['www.google.com']
    for dName in f:
        print(dName)
        expDate = ssl_valid_time_remaining(dName.strip())
        (a, b) = str(expDate).split(',')
        (c, d) = a.split(' ')
    # Critical alerts 
        if int(c) < 15:
            sns_Alert(dName, str(c), 'Critical')
      # Frist critical alert on 20 th day      
        elif int(c) == 20:
            sns_Alert(dName, str(c), 'Critical')
    #third warning alert on 30th day      
        elif int(c) == 30:
            sns_Alert(dName, str(c), 'Warning')
    #second warning alert on 40th day
        elif int(c) == 40:
            sns_Alert(dName, str(c), 'Warning')
    #First warning alert on 50th day      
        elif int(c) == 50:
            sns_Alert(dName, str(c), 'Warning')
        else:
            print('Everything Fine..')
