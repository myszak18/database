# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:55:53 2016

@author: manager
"""

from flask import Flask, render_template, json, request, redirect
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kelemvor'
app.config['MYSQL_DATABASE_DB'] = 'GenomicData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)




@app.route("/")

def main():
	w=open("/home/manager/database/static/my_data.txt","w")
	w.close()
	return render_template('index.html')
        
@app.route('/searchGene')

def searchGene():
	w=open("/home/manager/database/static/my_data.txt","w")
	w.close()
	return render_template('searchGene.html')
    
@app.route('/validateGene',methods=['POST'])
def validateLogin():
    try:
        gene = request.form['gene']
        con = mysql.connect()
        cursor = con.cursor()
        sql = "SELECT * FROM GenomicData.VARIANTS \
       WHERE SYMBOL = '%s'" % (gene)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) > 0:
            w=open("/home/manager/database/static/my_data.txt","w")
            w.write("#\n")
            for item in data:
                new_data=map(str,item)
                w.write(("\t").join(new_data)+"\n")
            w.close()
            return redirect('/userGene')
        else:
            return render_template('error.html',error = 'Wrong Gene')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
		cursor.close()
		con.close()
		
@app.route('/userGene')
def userHome():
    return render_template('VariantView.html')
        
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')
    
@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')
    
@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addWish',(_title,_description,_user))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()
    
@app.route('/getWish')
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')
 
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()
 
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)
 
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))
        
        
if __name__ == "__main__":
    app.run()
