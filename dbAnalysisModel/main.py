from connectDB import *
from operate import *
import tkinter

#MySQL connection parameters
url = "localhost"
user = "root"
password = "Whc910131"
db = "local_data"

#SQL
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
			round(supp_offer_price*part_num,2) as ttl_supp_offer_price,\
			supplier_id,\
			supp_name,\
			jap_offer_price,\
			jap_offer_price * part_num as ttl_jap_offer_price,\
			deal_price,\
			deal_price * part_num as ttl_deal_price,\
			regist_time,\
			receive_time,\
			offer_time,\
			deal_time,\
			province,\
			province_name,\
			city,\
			insert_time,\
			update_time\
 		from base_inquiry_parts_info limit 10000;"

#create operate object
dbObj = Operate(url, user, password, db, sql)
data = dbObj.getData()	#Get data from db
fields = dbObj.getFields()	#Get fields from result
print (fields)

#create operate object
opObj = Process(data,fields)
print (opObj.groupData(['damage_no','province_name'],False,['total_damage_price','total_verify_price']))
