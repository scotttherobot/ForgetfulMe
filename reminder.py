import sqlite3
import sys

datab = sqlite3.connect("reminderdata.db")
cursor = datab.cursor()

def parse(message):
	if 'add' in message[0:3]:
		print add(message[4:])
	if 'find' in message[0:4]:
		print find(message[5:])
	if 'done' in message[0:4]:
		print done(message[5:])
	if 'show' in message[0:4]:
		print show()
	if 'clear' in message[0:5]:
		print clear()
	if 'help' in message[0:4]:
		print usage()
	if 'quit' in message[0:4]:
		sys.exit(1)

def add(message):
	cursor.execute("INSERT INTO reminders(reminder) VALUES (?)", [message])
	datab.commit()
	return 'Okay, a reminder was created.'

def find(keyword):
	cursor.execute("SELECT * FROM reminders WHERE reminder LIKE '%"+keyword+"%'")
	reminder = cursor.fetchall()
	response = ''
	for item in reminder:
		row = "%d : %s" % (item[0], item[1])
		response += row + "\n"
	if response is '':
		response = 'There are no reminders matching the keyword '+keyword+'.'
	return response.rstrip('\n')

def done(id):
	cursor.execute("DELETE FROM reminders WHERE id = ?", [id])
	datab.commit()
	return 'Okay, the reminder with id ' + id + ' was removed.'
	
def clear():
	cursor.execute("DELETE FROM reminders")
	datab.commit()
	return 'All reminders were deleted.'
	
def show():
	cursor.execute("SELECT * FROM reminders")
	reminder = cursor.fetchall()
	response = ''
	for item in reminder:
		row = "%d : %s" % (item[0], item[1])
		response += row + "\n"
	if response is '':
		response = 'There are no reminders.'
	return response.rstrip('\n')
	
def createdb():
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reminders'")
	done = cursor.fetchone()
	# print done
	if not done:
		print 'Creating a new database.'
		cursor.execute("""CREATE TABLE reminders
					  (id INTEGER PRIMARY KEY,
					  reminder TEXT)""")
	datab.commit()

def usage():
	return 'Welcome do the reminders database.\nusage > add [reminder]\n      > show\n      > find [keyword]\n      > done [id]\n      > clear\n      > help\n      > quit'

def main():
	print usage()	
	createdb()
	while 1:
		input = raw_input("> ")
		parse(input)
	
if __name__ == "__main__":
	main()