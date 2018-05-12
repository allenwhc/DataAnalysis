import pymysql
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import codecs
from damageVerify import *
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

url = "localhost"	#database ip
usr = "root"	#database username
pwd = "Whc910131"	#database password

db = pymysql.connect(url,usr,pwd,"local_data",charset='utf8')	#establish database connection
cursor = db.cursor()	#define cursor
raw_data = []
#raw_data.append(['id','damage_parts_id','damage_no','part_name','part_oe','part_num','reference_type','part_type','part_brand','car_brand','car_series','car_model','damage_price','verify_price','supp_offer_price','supplier_id','supp_name','jap_offer_price','deal_price','regist_time','receive_time','offer_time','deal_time','province','city','insert_time','update_time'])
sql = "select \
			id, \
			damage_parts_id,\
			damage_no,\
			part_name,\
			part_oe,\
			part_num,\
			reference_type,\
			part_type,\
			part_brand,\
			car_brand,\
			car_series,\
			car_model,\
			damage_price,\
			round(damage_price*part_num,2) as ttl_damage_price,\
			verify_price,\
			round(verify_price*part_num,2) as ttl_verify_price,\
			supp_offer_price,\
			round(supp_offer_price*part_num,2),\
			supplier_id,\
			supp_name,\
			jap_offer_price,\
			jap_offer_price * part_num as ttl_jap_offer_price,\
			deal_price,\
			deal_price * part_num,\
			regist_time,\
			receive_time,\
			offer_time,\
			deal_time,\
			province,\
			city,\
			insert_time,\
			update_time\
 		from base_inquiry_parts_info limit 10000;"

cursor.execute(sql)
results = cursor.fetchall()
for row in results:
	_len = len(row)
	_r = []
	for j in range(_len):
		_r.append(row[j].encode('utf8').decode('utf8') if type(row[j]) == str else row[j])
	raw_data.append(_r)

obj = normStd(raw_data)
#print ('按定损单维度统计归一化标准差：',obj.getNormStdDamageno())
normStdProvince = obj.getNormStdProvince()
print (normStdProvince.dtypes)
normStdProvince.plot(kind='line')
plt.show()
#print ('按月份归一化标准差：',obj.getNormStdTime())