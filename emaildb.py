import MySQLdb

db = MySQLdb.connect("localhost","root","kelemvor","GenomicData" )
cur = db.cursor()


cur.execute("DROP TABLE IF EXISTS GenomicData.VARIANTS")

sql = """CREATE TABLE GenomicData.VARIANTS (
         CHROM  CHAR(20),
         POS INT,
         REF TEXT(1000),  
         ALT TEXT(1000),
         RS CHAR(20),
         MAF FLOAT,
         HGVSC TEXT(1000) ,
         COSM CHAR(20),
         TYPE CHAR(100),
         SYMBOL CHAR(40),
         REFSEQ TEXT(1000),
         CHANGES TEXT(1000))"""
         
cur.execute(sql)


fh = open("my_data.txt")
content=fh.readlines()
fh.close()
for line in content[1:]:
    data=line.strip("\r\n").split("\t")
    info=data
    info[1]=int(data[1])
    info[5]=float(data[5])
    sql = "INSERT INTO GenomicData.VARIANTS( \
       CHROM, POS, REF, ALT, RS, MAF, HGVSC, COSM, TYPE, SYMBOL, REFSEQ, CHANGES) \
       VALUES ('%s', '%i', '%s', '%s', '%s', '%f', '%s','%s','%s','%s', '%s', '%s' )" % \
       tuple(info)
    cur.execute(sql)
   # Commit your changes in the database

db.commit()
    
# https://www.sqlite.org/lang_select.html

cur.close()

