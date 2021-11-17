"""
Goal : Automated email to me and others.

Ex: Consider a website in which there is latest news updates everyday, and it's important 
for us to read that newsletter, but we find it diffcult to open the website everyday and read it.
instead if the newsletter can be imported into our mail directly then we can access only our mail
to read the entire newsletter. 

It can be done through web scraping. 

1. First we have to make a HTTP request to that particular url.

2. We have to prase that website through html praser.

3. Then scrape certain information on that website. 

4. Here the scraping task is done, next is to send the output to our mail.

5. It can be done by providing SERVER, PORT, FROM, TO, PASS; server would be the email service which 
   we are using ; port number is constant ; from is the email of sender ; to is the email of reciever in 
   this case we are only sending to us ; pass is the password for sending email. 

6. Then we have to make our message and initialize the server. 

"""



import requests # for http requests

from bs4 import BeautifulSoup # for web scraping

# for sending the mail
# standard mail transfer protocol lib
import smtplib 

# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# system date and time manipulation
import datetime

now = datetime.datetime.now() # today's date and time 

# email content placeholder

content = ''


#extracting Hacker News Stories


def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')  # this is message header. 
    
    response = requests.get(url)  # HTTP request is sent to url. 

    content = response.content
    
    soup = BeautifulSoup(content,'html.parser') # a soup is created by prasing HTML 

    # Here i is for indexes and tag is for the information. 
    # We are only finding and scraping td class:title and valign:""

    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')
        #print(tag.prettify) #find_all('span',attrs={'class':'sitestr'}))
    return(cnt)
    
cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content +=('<br><br>End of Message')


#lets send the email

print('Composing Email...')

# update your email details
# make sure to update the Google Low App Access settings before

SERVER = 'smtp.gmail.com' # "your smtp server"
PORT = 587 # your port number
FROM =  '' # "your from email id"
TO = '' # "your to email ids"  # can be a list
PASS = '*****' # "your email id's password"

# fp = open(file_name, 'rb')
# Create a text/plain message
# msg = MIMEText('')
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
# fp.close()

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()






