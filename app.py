# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:55:53 2016

@author: manager
"""

from flask import Flask, render_template, json, request, redirect, make_response, url_for, send_from_directory, jsonify, flash
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session
from flask.ext.cache import Cache
from werkzeug.utils import secure_filename
import os




app = Flask(__name__, static_folder='static', static_url_path='/static')
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','vcf'])
app.secret_key = 'super secret key'



mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kelemvor'
app.config['MYSQL_DATABASE_DB'] = 'GenomicData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mysql.init_app(app)



extra_files="/home/manager/database/static/my_data.txt"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
@app.route("/")

def main():
    w=open("/home/manager/database/static/my_data.txt","w")
    w.close()
    return render_template('index.html')

@app.route('/searchGene')
def searchGene():
    return render_template("searchGene.html")

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    try:
        search = request.args.get('q') 
        con = mysql.connect()
        cursor = con.cursor()
        sql = "SELECT SYMBOL FROM GenomicData.VARIANTS \
        WHERE SYMBOL LIKE '%s'" % (search+"%")
        cursor.execute(sql)
        data = cursor.fetchall()
        gene_list = [item[0] for item in set(data)]
        return jsonify(matching_results=gene_list)
    except:
        pass
    finally:
        cursor.close()
        con.close()
        

        
@app.route('/validateGene',methods=['POST'])
def validateGene():
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
            return redirect(url_for('showGene', gene=gene))
        else:
            return render_template('error.html',error = 'Wrong Gene')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
		cursor.close()
		con.close()

@app.route('/showGene/<gene>')
def showGene(gene):		
	response = make_response(render_template('VariantView.html',gene=gene))
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'no-cache, no-store'
	return response
	

@app.route('/searchPosition')
def searchPosition():
    return render_template("searchPosition.html")

@app.route('/autocompletepos', methods=['GET'])
def autocompletepos():
    try:
        search = request.args.get('q') 
        con = mysql.connect()
        cursor = con.cursor()
        sql = "SELECT POS FROM GenomicData.VARIANTS \
        WHERE POS LIKE '%s'" % (search+"%")
        cursor.execute(sql)
        data = cursor.fetchall()
        gene_list = [str(item[0]) for item in set(data)]
        return jsonify(matching_results=gene_list)
    except:
        pass
    finally:
        cursor.close()
        con.close() 
        
@app.route('/validatePosition',methods=['POST'])
def validatePosition():
    try:
        position = request.form['position']
        con = mysql.connect()
        cursor = con.cursor()
        sql = "SELECT * FROM GenomicData.VARIANTS \
       WHERE POS = '%s'" % (position)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) > 0:
            variants=[dict(chrom=row[0],position=row[1],maf=str(row[5]),rs=row[4],gene=row[-3],change=row[-1]) for row in data]
            return render_template('posDisplayer.html', variants=variants)
        else:
            return render_template('error.html',error = 'Wrong Position')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()
        
@app.route('/searchTableGene')
def searchTableGene():
    return render_template("searchTableGene.html")
    
@app.route('/validateTableGene',methods=['POST'])
def validateTableGene():
    try:
        position = request.form['gene']
        con = mysql.connect()
        cursor = con.cursor()
        sql = "SELECT * FROM GenomicData.VARIANTS \
       WHERE SYMBOL = '%s'" % (position)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) > 0:
            variants=[dict(chrom=row[0],position=row[1],maf=str(row[5]),rs=row[4],gene=row[-3],change=row[-1]) for row in data]
            return render_template('geneDisplayer.html', variants=variants)
        else:
            return render_template('error.html',error = 'Wrong Position')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()
        
@app.route('/downloadTable',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_n = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file_n.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_n and allowed_file(file_n.filename):
            content=file_n.readlines()
            positions=[]
            for line in content:
                if line.startswith("#"):
                    pass
                elif file_n.filename.split(".")[-1]=="vcf":
                    data=line.split("\t")
                    positions.append(int(data[1]))
                else:
                    positions.append(int(line.strip("\r\n").strip("\n")))
            if len(positions)>0:
                selected_variants=[]
                con = mysql.connect()
                cursor = con.cursor()
                for item in positions:
                    sql = "SELECT * FROM GenomicData.VARIANTS \
                        WHERE POS = '%i'" % (item)
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    if len(data) > 0:
                        selected_variants.extend(data)
                variants=[dict(chrom=row[0],position=row[1],maf=str(row[5]),rs=row[4],gene=row[-3],change=row[-1]) for row in selected_variants]
                if len(selected_variants)<20:
                    return render_template('geneDisplayer.html', variants=variants)
                else:
                    name=file_n.filename.split(".")[0]+".txt"
                    w=open("upload/"+name,"w")
                    for variant in selected_variants:
                        w.write(("\t").join(map(str,variant))+"\n")
                    w.close()
                    return redirect(url_for("download",filename=name))
            else:
                return render_template('error.html',error = 'Wrong Position')
    return render_template("downloadTable.html")

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)       
        
if __name__ == "__main__":
    app.debug = True
    app.run(extra_files=extra_files,use_reloader=True)
