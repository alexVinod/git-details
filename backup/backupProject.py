import time, re, pymysql
from flask import Flask, render_template, url_for, flash, request, jsonify
from pymysql import cursors

app = Flask(__name__)

db = pymysql.connect(
		host='localhost',
		user='root',
		password='',
		db='poctest',
		charset='utf8'
	)

cursor1 = db.cursor(cursors.DictCursor)
cursor = db.cursor()

# Create Tables domainDetails
query = """CREATE TABLE IF NOT EXISTS dbDomainDetails (id int primary key auto_increment,
										  domainName varchar(300),
										  createdBy varchar(300),
										  createdOn varchar(300),
										  createdMailId varchar(300),
										  empId varchar(300))"""
cursor.execute(query)



# query1="select*from sample"
# cursor.execute(query1)
# for rows in cursor.fetchall():
# 	print(rows)





@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
	if request.method == 'POST':
		fname = request.form['firstName']
		lname = request.form['lastName']
		createdBy = fname+" "+lname

		createdOn = time.ctime()

		email = request.form['email']
		empId = request.form['empId']

		domain = re.search("@[\w]+", email).group().replace('@','')

		try:
			#print('-------------------------', type(domain), type(createdBy), type(createdOn), type(email), type(empId) )
			# Insert into dbDomainDetails here
			#iquery= "insert into dbDomainDetails (domainName,createdBy,createdOn,createdMailId,empId) values (?,?,?,?,?)"
			#cursor.execute(iquery,(domain, createdBy, createdOn, email, empId, ))
			cursor.execute("insert into dbDomainDetails (domainName,createdBy,createdOn,createdMailId,empId) values ('"+domain+"','"+createdBy+"','"+createdOn+"','"+email+"','"+empId+"')")

			try:
				cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(domain))
				db.commit()

				domainDB = pymysql.connect(
						host='localhost',
						user='root',
						password='',
						db=domain,
						charset='utf8'
					)

				domainCursor1 = domainDB.cursor(cursors.DictCursor)
				domainCursor = domainDB.cursor()
				# Create Tables userDetails in dynamic database here
				dquery = """CREATE TABLE IF NOT EXISTS userDetails (id int primary key auto_increment,
														  firstName varchar(300),
														  lastName varchar(300),
														  email varchar(300),														  
														  empId varchar(300))"""
				domainCursor.execute(dquery)
				domainCursor.execute("insert into userDetails (firstName,lastName,email,empId) values ('"+fname+"','"+lname+"','"+email+"','"+empId+"')")
				domainDB.commit()

				flash('User Also Added Successfully','info')
				return render_template('home.html')
			except Exception as e:
				flash(str(e),'info')
				return render_template('home.html')				

			flash('Added Successfully','info')
			return render_template('home.html')
		except Exception as e:
			flash(str(e),'info')
			return render_template('home.html')			
			
			#print(domain, createdBy, createdOn, email, empId)
			#CREATE DATABASE IF NOT EXISTS DBName;
	else:
		return render_template('home.html')


@app.route('/genApis', methods=['GET',"POST"])
def getAllAPI():
	cursor.execute("select *from dbDomainDetails")
	row_headers=[x[0] for x in cursor.description]
	dbDomains = cursor.fetchall()
	#json_data = {'DomainsDetails':[{'domains':[]}]}
	json_data = {'DomainsDetails':[]}
	c=0
	for result in dbDomains:
		jsonDomainDB = pymysql.connect(
						host='localhost',
						user='root',
						password='',
						db=result[1],
						charset='utf8')

		jsonDomainCursor1 = jsonDomainDB.cursor(cursors.DictCursor)
		jsonDomainCursor = jsonDomainDB.cursor()

		jsonDomainCursor.execute("select*from userDetails")
		jdc_datas = jsonDomainCursor.fetchall()
		for jdc in jdc_datas:
			convertDomain = re.search("@[\w]+", jdc[3]).group().replace('@','')
			if convertDomain == result[1]:
				if convertDomain not in json_data['DomainsDetails']:
					json_data['DomainsDetails'].append(dict(zip(row_headers,result)))
				#json_data['DomainsDetails']['convertDomain'] = dict(zip(row_headers,result))
				#json_data['DomainsDetails'].append()
				# if convertDomain not in json_data['DomainsDetails']:
				# 	cd=[dict(zip(row_headers,result))]
				# 	oneDomain = json_data['DomainsDetails'].append(dict(zip(row_headers,result)))
				# 	#json_data['DomainsDetails'].append({convertDomain:dict(zip(row_headers,result))})
				# 	#print(json_data['DomainsDetails'][c])
				# 	c=c+1
				#dn.append({convertDomain:dict(zip(row_headers,result))})
				#json_data['DomainsDetails'].append(dict(zip(convertDomain,result)))
				c=c+1
		#json_data['DomainsDetails'].append(dict(zip(row_headers,result)))
		#json_domain = json_data['DomainsDetails'][c]['domainName']		
		# print('------------------------',jsonDomainDB)













	# for data in json_data:
	# 	print('--------------',data['domainName'])
		#print("----------------",dict(zip(row_headers,result)))
	#print('-----------------',row_headers,dbDomains)
	#return render_template('genAPIs.html', domainsDetails=json_data)
	return jsonify(json_data)

if __name__ == '__main__':
	app.secret_key = "secret key"
	app.debug = True
	app.run(host='0.0.0.0',port=5000)











#from flask_mysqldb import MySQL
#from flaskext.mysql import MySQL


# Config MySQL here
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_PORT'] = '3306'
# app.config["MYSQL_USER"] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] ='poctest'
# app.config['MYSQL_CURSORCLASS'] ='DictCursor'

# mysql = MySQL(app)

# cur = mysql.connection.cursor()

#with app.app_context():cur = mysql.connection.cursor()

# Create Tables domainDetails
# query = """CREATE TABLE IF NOT EXISTS dbDetails (id int primary key auto_increment,										  domainName varchar(300),
# 										  createdBy varchar(300),
# 										  createdOn varchar(300),
# 										  createdMailId varchar(300),
# 										  empId varchar(300))"""

#cur.execute("select * from sample")
#cur.close()
# connect = mysql.connect('poctest')
# cursor = connect.cursor()
# cursor.execute("select * from sample")
# cursor.close()

#mysql = MySQL(app)
#mysql.init_app(app)
#cursor = mysql.connection.cursor()

#cursor = mysql.get_db().cursor()