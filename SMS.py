from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import socket
import requests
import json

def ValidateRno(rno):
	def CheckRno(r):
		flag = 0
		if r == "":
			showerror("Failure", "Roll number should not be empty")
			flag = 1
		elif r.isalpha():
			showerror("Failure", "Roll number must be in integer form")
			flag = 1
		elif (int(r) < 0):
			showerror("Failure", "Roll number must be positive")
			flag = 1
		return flag
	try:
		r = rno.get()
		flag = CheckRno(r)
		if r == "" or flag == 1:
			return
		else:
			return int(r)
	except Exception as er:
			if (str(er)=="UNIQUE constraint failed: student.rno"):
				showerror("Failure", "Entered roll no already exists")
			elif (str(er)=="invalid literal for int() with base 10: ''"):
				showerror("Failure", "Roll number should not be empty")
			else:
				showerror("Failure", er)

def ValidateName(name):
	def CheckName(n):
		flag = 0
		if n == "":
			showerror("Failure", "Name should not be empty")
			flag = 1
		elif not n.isalpha():
			showerror("Failure", "Name input is invalid")
			flag = 1
		elif len(n) < 2:
			showerror("Failure", "Name should be at least 2 characters.")
			flag = 1
		return flag	
	try:
		n = name.get()
		flag = CheckName(n)
		if n == None or flag == 1:
			return 0
		else:
			return n
	except Exception as en:
		showerror("Failure", "Issue:" + en)

def ValidateMarks(marks):
	try:
		m = marks.get()
		flag = 0
		if m == "":
			showerror("Failure", "Marks should not be empty")
			flag = 1
		elif (int(m)<0) or (int(m)>100):
			showerror("Failure", "Marks must be in range of 0-100")
			flag = 1
		if m == "" or flag == 1:
			return
		else:
			return int(m)
	except Exception as em:
		if (str(em)=="invalid literal for int() with base 10: ''"):
			showerror("Failure", "Marks should not be empty")

def sortrno(e):
	return e[0]

def AddWindow():
	adst.deiconify()
	root.withdraw()

def BackAdd():
	entrno.delete(0, END)
	entrno.insert(0, "")
	entname.delete(0, END)
	entname.insert(0, "")
	entmarks.delete(0, END)
	entmarks.insert(0, "")
	root.deiconify()
	adst.withdraw()

def ViewWindow():
	stdata.delete(1.0, END)
	vist.deiconify()
	root.withdraw()
	con = None
	try:
		con = connect("test.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		data.sort(key = sortrno)		
		info = "ROLL NO\t\tNAME\t\tMARKS\n"
		for d in data:
			info = info + str(d[0]) + "\t\t" + str(d[1]) + "\t\t" + str(d[2]) + "\n"
		stdata.insert(INSERT, info)
	except Exception as e:
		showerror("Failure", "Insert issue: " + str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()

def BackView():
	root.deiconify()
	vist.withdraw()

def AddRecord():
	con = None
	try:
		con = connect("test.db")
		rno = ValidateRno(entrno)
		name = ValidateName(entname)
		if name == 0:
			return
		marks = ValidateMarks(entmarks)
		args = (rno, name, marks)
		cursor = con.cursor()
		sql = "insert into student values('%d', '%s', '%d') "
		cursor.execute(sql % args)
		con.commit()
		showinfo("Success ", "Record added")
	except Exception as e:
			if (str(e)=="UNIQUE constraint failed: student.rno"):
				showerror("Failure", "Entered roll no already exists")
	finally:
		if con is not None:
			con.close()

def UpdateRecord():
		con = None
		try:
			ch = s.get()
			con = connect("test.db")
			cursor = con.cursor()
			if (ch == 1):
				urno = ValidateRno(enturno)
				newname = ValidateName(entuname)
				if newname == 0:
					return
				sql = """Update student set name = ? where rno = ? """
				args = (newname, urno)
			elif (ch == 2):
				urno = ValidateRno(enturno)
				newmarks = ValidateMarks(entumarks)
				sql = """Update student set marks = ? where rno = ? """
				args = (newmarks, urno)
			elif (ch == 3):
				urno = ValidateRno(enturno)
				newname = ValidateName(entuname)
				if newname == 0:
					return
				newmarks = ValidateMarks(entumarks)
				sql = """Update student set name = ?, marks = ? where rno = ? """
				args = (newname, newmarks, urno)
			cursor.execute(sql, args)
			con.commit()
			data = cursor.fetchone()
			if cursor.rowcount >= 1:
				showinfo("Success ", "Record updated")
			else:
				showinfo("Error", "Roll Number does not exist")
		except Exception as e:
			showerror("Failure", "Update issue: " + str(e))
			con.rollback()
		finally:
			if con is not None:
				con.close()

def BackUpdate2():
	root.deiconify()
	update.withdraw()

def UpdateWindow():
	update.deiconify()
	root.withdraw()

def DeleteRecord():
	con = None
	try:
		con = connect("test.db")
		cursor = con.cursor()
		drno = ValidateRno(entdrno)
		sql = """delete from student where rno = ? """
		cursor.execute(sql, (drno, ))
		data = cursor.fetchone()
		if cursor.rowcount >= 1:
			con.commit()
			showinfo("Success ", "Record deleted")
		elif drno != None:
			showinfo("Error", "Roll Number does not exist")
	except ValueError:
		showerror("Failure", "Required input must be a positive integer")
		con.rollback()
	finally:
		if con is not None:
			con.close()

def DeleteWindow():
	delete.deiconify()
	root.withdraw()

def BackDelete():
	entdrno.delete(0, END)
	entdrno.insert(0, "")
	root.deiconify()
	delete.withdraw()

def ChartsWindow():
	con = connect('test.db', isolation_level=None, detect_types=PARSE_COLNAMES)
	data1 = pd.read_sql_query("SELECT * FROM student", con)
	data1.to_csv('student_info.csv', index=False)

	data2 = pd.read_csv("student_info.csv")

	trno = data2['rno'].tolist()
	tname = data2['name'].tolist()
	tmarks = data2['marks'].tolist()

	x = np.arange(len(trno))
	c =  {'xkcd:sky blue', 'c', 'xkcd:hot pink', 'xkcd:greenish yellow', 'xkcd:dark aqua'}
	plt.bar(x, tmarks, width = 0.8, color = c, align = 'center', label = 'Marks')
	plt.xticks(x, tname)
	plt.ylabel("Marks")
	plt.title("Batch Information!")
	plt.show()

def LocTemp():
	try:
		socket.create_connection(("www.google.com",80))
		res = requests.get("https://ipinfo.io/")
		data = res.json()
		city = data['city']
		a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
		a2 = "&q=" + city 
		a3 = "&appid=c6e315d09197cec231495138183954bd"
		api_address =  a1 + a2  + a3 		
		res = requests.get(api_address)
		data = res.json()
		main = data['main']
		temp1 = main['temp']
		s = ("LOCATION: " + city + "   TEMP: " + str(temp1))
		return (s)
	except OSError as e:
		showerror("Failure", "Issue: " + str(e))

def Qotd():
	try:
		url = "https://quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com/quote"

		headers = {'x-rapidapi-host': "quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com",'x-rapidapi-key': "d99a4542eamsh38f3ce5bd0b4e95p1092e7jsn154b7b1c4a5b"}

		response = requests.request("GET", url, headers=headers) 
		quotes = response.text
		d = json.loads(quotes)
		a = d['text'] + " - " + d['author']
		return(a.strip('â€œ'))
	
	except Exception as e:
		showerror("Error", str(e))        

def BackUpdate1():
	ch = s.get()
	enturno.delete(0, END)
	enturno.insert(0, "")
	lblurno.pack_forget()
	enturno.pack_forget()
	btnusave.pack_forget()
	btnuback.pack_forget()
	if ch == 1:
		entuname.delete(0, END)
		entuname.insert(0, "")
		lbluname.pack_forget()
		entuname.pack_forget()
	elif ch == 2:
		entumarks.delete(0, END)
		entumarks.insert(0, "")
		lblumarks.pack_forget()
		entumarks.pack_forget()
	elif ch == 3:
		entuname.delete(0, END)
		entuname.insert(0, "")
		entumarks.delete(0, END)
		entumarks.insert(0, "")
		lbluname.pack_forget()
		entuname.pack_forget()
		lblumarks.pack_forget()
		entumarks.pack_forget()
	update.deiconify()
	updaten.withdraw()


# Design of root window --> SMS (Student Management System)

root = Tk()
root.title("S. M. S.")
root.geometry("800x550+400+200")
root['background']='MediumOrchid1'
btnAdd = Button(root, text = "Add", font = ("arial", 18, "bold"), width = 10, command = AddWindow)
btnView = Button(root, text = "View", font = ("arial", 18, "bold"), width = 10, command = ViewWindow)
btnUpdate = Button(root, text = "Update", font = ("arial", 18, "bold"), width = 10, command = UpdateWindow)
btnDel = Button(root, text = "Delete", font = ("arial", 18, "bold"), width = 10, command = DeleteWindow)
btnCh = Button(root, text = "Charts", font = ("arial", 18, "bold"), width = 10, command = ChartsWindow)

lnt = LabelFrame(root, font = ("Comic Sans MS", 14), padx = 5, pady = 5, bg = 'MediumOrchid1', relief = 'solid')
lbllnt = Label(lnt, text = LocTemp(), bg  = 'MediumOrchid1', font = ("Comic Sans MS", 14))
qotd = LabelFrame(root, text="QOTD",font = ("Comic Sans MS", 14, 'bold'), padx=5, pady=5, bg = 'MediumOrchid1', relief = 'solid')
lblqotd = Label(qotd, text = Qotd(), bg = 'MediumOrchid1', font = ("Comic Sans MS", 14), wraplength = 750)


btnAdd.pack(pady = 7)
btnView.pack(pady = 7)
btnUpdate.pack(pady = 7)
btnDel.pack(pady = 7)
btnCh.pack(pady = 7)
lnt.pack(padx=10, pady=10)
lbllnt.pack(pady = 7)
qotd.pack(padx=10, pady=10)
lblqotd.pack()

# Design of adst window --> Add Student

adst = Toplevel(root)
adst.title("Add Student")
adst.geometry("500x400+400+200")
adst['bg'] = 'OliveDrab1'
adst.withdraw()

lblrno = Label(adst, text = "Enter Roll Number", font = ("arial", 18, "bold"), bg = 'OliveDrab1')
entrno = Entry(adst, bd = 5, font = ("arial", 18, "bold"))
lblname = Label(adst, text = "Enter Name", font = ("arial", 18, "bold"), bg = 'OliveDrab1')
entname = Entry(adst, bd = 5, font = ("arial", 18, "bold"))
lblmarks = Label(adst, text = "Enter Marks", font = ("arial", 18, "bold"), bg = 'OliveDrab1')
entmarks = Entry(adst, bd = 5, font = ("arial", 18, "bold"))
btnsave = Button(adst, text = "Save", font = ("arial", 18, "bold"), command = AddRecord)
btnback = Button(adst, text = "Back", font = ("arial", 18, "bold"), command = BackAdd)

lblrno.pack(pady = 5)
entrno.pack(pady = 5)
lblname.pack(pady = 5)
entname.pack(pady = 5)
lblmarks.pack(pady = 5)
entmarks.pack(pady = 5)
btnsave.pack(pady = 5)
btnback.pack(pady = 5)


# Design of visit window --> View Student
vist = Toplevel(root)
vist.title("View Student")
vist.geometry("500x500+400+200")
vist.configure(bg='VioletRed1')
vist.withdraw()

stdata = ScrolledText(vist, width = 50, height = 20, font = ("Times New Roman", 12))
btnvback = Button(vist, text = "Back", font = ("arial", 18, "bold"), command = BackView)

stdata.pack(pady = 10)
btnvback.pack(pady = 10)

# Design of update window --> Update Student Info

update = Toplevel(root)
update.title("Update Student Info")
update.geometry("500x400+400+200")
update.configure(bg='cornflower blue')
update.withdraw()
updaten = Toplevel(update)
updaten.title("Update Student Info")
updaten.geometry("500x400+400+200")
updaten.configure(bg = 'yellow')
updaten.withdraw()

lblchoice = Label(update, text = "Select your choice", font = ("arial", 18, "bold"), bg='cornflower blue')

lblurno = Label(updaten, text = "Enter Roll Number", font = ("arial", 18, "bold"), bg='yellow')
enturno = Entry(updaten, bd = 5, font = ("arial", 18, "bold"))
lbluname = Label(updaten, text = "Enter New Name", font = ("arial", 18, "bold"), bg='yellow')
entuname = Entry(updaten, bd = 5, font = ("arial", 18, "bold"))
lblumarks = Label(updaten, text = "Enter New Marks", font = ("arial", 18, "bold"), bg='yellow')
entumarks = Entry(updaten, bd = 5, font = ("arial", 18, "bold"))

def choice():
	updaten.deiconify()
	update.withdraw()
	ch = s.get()
	if ch == 1:
		lblurno.pack(pady = 5)
		enturno.pack(pady = 5)
		lbluname.pack(pady = 5)
		entuname.pack(pady = 5)
		btnusave.pack(pady = 5)
		btnuback.pack(pady = 5)
	elif ch == 2:
		lblurno.pack(pady = 5)
		enturno.pack(pady = 5)
		lblumarks.pack(pady = 5)
		entumarks.pack(pady = 5)
		btnusave.pack(pady = 5)
		btnuback.pack(pady = 5)
	elif ch == 3:
		lblurno.pack(pady = 5)
		enturno.pack(pady = 5)
		lbluname.pack(pady = 5)
		entuname.pack(pady = 5)
		lblumarks.pack(pady = 5)
		entumarks.pack(pady = 5)
		btnusave.pack(pady = 5)
		btnuback.pack(pady = 5)
	

s = IntVar()
s.set(1)
radiob = LabelFrame(update, text="SELECT YOUR CHOICE",font = ("arial", 14, 'bold'), labelanchor = 'n', padx=5, pady=5, bg = 'cornflower blue', relief = 'solid')
rbUpName = Radiobutton(radiob, text = "Update Name", font = ("arial", 14, "bold"), bg = 'cornflower blue', variable = s, value = 1)
rbUpRno = Radiobutton(radiob, text = "Update Marks", font = ("arial", 14, "bold"), bg = 'cornflower blue', variable = s, value = 2)
rbUpBoth = Radiobutton(radiob, text = "Update Both: Name & Roll no", font = ("arial", 14, "bold"), bg = 'cornflower blue', variable = s, value = 3)
btnSubmit = Button(update, text = "Submit", font = ("arial", 18, "bold"), command = choice)
btnUpback = Button(update, text = "Back", font = ("arial", 18, "bold"), command = BackUpdate2)

btnusave = Button(updaten, text = "Save", font = ("arial", 18, "bold"), command = UpdateRecord)
btnuback = Button(updaten, text = "Back", font = ("arial", 18, "bold"), command = BackUpdate1)

radiob.pack(padx=10, pady=10)
rbUpName.pack(pady = 6)
rbUpRno.pack(pady = 2)
rbUpBoth.pack(pady = 2)

btnSubmit.pack(pady = 6)
btnUpback.pack(pady = 3)

# Design of delete window --> Delete Student Info

delete = Toplevel(root)
delete.title("Delete Student Info")
delete.geometry("500x400+400+200")
delete.configure(bg='indian red')
delete.withdraw()

lbldrno = Label(delete, text = "Enter Roll Number", font = ("arial", 18, "bold"), bg='indian red')
entdrno = Entry(delete, bd = 5, font = ("arial", 18, "bold"))
btndsave = Button(delete, text = "Save", font = ("arial", 18, "bold"), command = DeleteRecord)
btndback = Button(delete, text = "Back", font = ("arial", 18, "bold"), command = BackDelete)

lbldrno.pack(pady = 5)
entdrno.pack(pady = 5)
btndsave.pack(pady = 5)
btndback.pack(pady = 5)

root.mainloop()
