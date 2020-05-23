#!/usr/bin/env python3

import csv, datetime, calendar, os, smtplib, getpass

from datetime import timedelta

def monthyear(month,year):
	daymonth = str(datetime.date(year, month, 1)).split("-")
	daymonth.pop(2)
	daymonth.reverse()
	return "-".join(daymonth)
def nextmonthyear(month,year):
	delta=timedelta(days=32)
	daymonth = str(datetime.date(year, month, 1)+delta).split("-")
	daymonth.pop(2)
	daymonth.reverse()
	return "-".join(daymonth)

def days_in_month(month,year):
	num_days = calendar.monthrange(year, month)[1]
	return list([datetime.date(year, month, day) for day in range(1, num_days+1)])

def makenice(table):
	table=list(table)
	table_new=[]
	if len(table[0])<3:
		for row in table:
			table_new.append([row[0],row[1],""])
	else:
		table_new=table
	table_newer=[]
	for row in table_new:
		row_new=[row[0], row[1] ,row[2].split()]
		row_newer=[]
		for i in row_new[2]:
			if len(i)>2:
				j=i.split("-")
				i_new=list(range(int(j[0]),int(j[1])+1))
				row_newer.extend(i_new)
			else:
				row_newer.append(int(i))
		row_new.pop(2)
		row_new.append(row_newer)
		table_newer.append(row_new)
	return table_newer

def isavailable(table, i, k):
	unavailable = table[i][2]
	for j in unavailable:
		if j==k:
			return 0
	return 1
	
file=input("Enter Unavailability List: ")# We are assumsing that this list is ordered by how long ago it was that a worker has done kitchen duty (descending). If you have used this program last month fill out "unavailability_mm-yyyy.csv" and input it.
with open('unavailability/'+file,'rt')as f:
  table = csv.reader(f)
  table= makenice(table)
  #table=[]
  #for row in data:
  #	table.append(row)
  n=len(table)
  workers=[]
  m=int(input("Enter month: "))
  y=int(input("Enter year: "))
  days=days_in_month(m,y)
  d=len(days)
  kitchen_schedule=[]
  bottle_schedule=[]
  for k in range(1, d+1):
  	indi=0
  	if days[k-1].weekday()==5:
  		for i in range(0,n):
  			if isavailable(table, i, k) and indi==0:
  				w=table[i]
  				table.pop(i)
  				table.append(w)
  				indi=indi+1
  				kitchen_schedule.append([w[0], w[1] , str(days[k-1])])
  			if isavailable(table, i, k) and indi ==1:
  				w=table[i]
  				table.pop(i)
  				table.append(w)
  				indi=indi+1
  				bottle_schedule.append([w[0], w[1] ,str(days[k-1])])
  			if isavailable(table, i, k) and indi ==2 and bottle_schedule[-1][0]!=table[i][0]:
  				w=table[i]
  				table.pop(i)
  				table.append(w)
  				indi=indi+1
  				bottle_schedule.append([w[0],w[1], str(days[k-1])])
  		if indi<3:
  			bottle_schedule.append(["nobody", "0", str(days[k-1])])
  		if indi<2:
  			bottle_schedule.append(["nobody", "0", str(days[k-1])])
  		if indi== 0:
  			kitchen_schedule.append(["nobody", "0", str(days[k-1])])
  	else:
	  	for i in range(0,n):
	  		if isavailable(table, i, k) and indi==0:
	  			w=table[i]
	  			table.pop(i)
	  			table.append(w)
	  			indi=1
	  			kitchen_schedule.append([w[0], w[1], str(days[k-1])])
	  	if indi==0:
	  		kitchen_schedule.append(["nobody","0" ,str(days[k-1])])
  with open('kitchen_schedule/kitchen_schedule_'+monthyear(m,y)+'.csv', 'w') as csvfile: #The schedule will be saved in the directory: schedule
  	schedulewriter=csv.writer(csvfile, dialect='excel')
  	schedulewriter.writerow(["Kitchen schedule for "+str(m)+"-"+str(y)])
  	schedulewriter.writerow(["Name", "Room", "Day"])
  	schedulewriter.writerows(kitchen_schedule)
  with open('bottle_schedule/bottle_schedule_'+monthyear(m,y)+'.csv', 'w') as csvfile: #The schedule will be saved in the directory: schedule
  	schedulewriter=csv.writer(csvfile, dialect='excel')
  	schedulewriter.writerow(["Bottle schedule for "+str(m)+"-"+str(y)])
  	schedulewriter.writerow(["Name", "Room", "Day"])
  	schedulewriter.writerows(bottle_schedule)  
  	new_list=[[row[0]] for row in table]
  with open('unavailability/unavailability_'+nextmonthyear(m,y)+'.csv', 'w') as csvfile:#The list of workers sorted by how long ago it was that they have done kitchen duty will be saved in the directory: unavailability. Fill this out with the days in which the person is unavailable.
  	listwriter=csv.writer(csvfile, dialect='excel')
  	listwriter.writerows(new_list)
kschedule=open('kitchen_schedule/kitchen_schedule_'+monthyear(m,y)+'.csv')
print(kschedule.read())
bschedule=open('bottle_schedule/bottle_schedule_'+monthyear(m,y)+'.csv')
print(bschedule.read())
send=input("Send emails?[y/n] ")
if send=='y' or send=='yes':
  emails=input("Enter email list: ")
  emailsreader = csv.reader(open(emails))
  email_dict={}
  for row in emailsreader:
    name= row[0]
    if name in email_dict:
      pass
    email_dict[name]=row[1]
  print(email_dict)
  import smtplib
  # set up the SMTP server
  gmail_user = input("Enter your gmail address: ")
  gmail_password = getpass.getpass("Input password: ")
  
  for row in kitchen_schedule:
    name=row[0].split()[0]
    sent_from = gmail_user
    to = email_dict[row[0]]
    subject = 'Kitchen Duty'
    body = 'Hi '+name+',\n your kitchen duty is on the '+row[2]+'\n Save the date!\n\n Your friendly student council.'
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, to, subject, body)
    s = smtplib.SMTP(host='smtp.gmail.com.', port=587)
    s.ehlo()
    s.starttls()
    s.login(gmail_user,gmail_password)
    s.sendmail(sent_from, to, email_text)
    s.close()
    print('Email sent to '+row[0])
  for row in bottle_schedule:
    name=row[0].split()
    name=name[0]
    sent_from = gmail_user
    to = email_dict[row[0]]
    subject = 'Bottle Duty'
    body = 'Hi '+name+',\n your bottle duty is on the '+row[2]+'\n Save the date!\n\n Your friendly student council.'
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, to, subject, body)
    s = smtplib.SMTP(host='smtp.gmail.com.', port=587)
    s.ehlo()
    s.starttls()
    s.login(gmail_user,gmail_password)
    s.sendmail(sent_from, to, email_text)
    s.close()
    print('Email sent to '+row[0])



