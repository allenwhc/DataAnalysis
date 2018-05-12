import pandas as pd
from pandas import Series, DataFrame
class normStd():
	def __init__(self, data):
		self.data = DataFrame(data, columns=['id','damage_parts_id','damage_no','part_name','part_oe','part_num','reference_type','part_type','part_brand','car_brand','car_series','car_model','unit_damage_price','total_damage_price','unit_verify_price','total_verify_price','unit_supp_offer_price','total_supp_offer_price','supplier_id','supp_name','unit_jap_offer_price','total_jap_offer_price','unit_deal_price','total_deal_price','regist_time','receive_time','offer_time','deal_time','province','city','insert_time','update_time'])
		self.dataByDamageno = self.data.groupby(['damage_no'])['total_damage_price','total_verify_price'].sum() 		

	def getNormStdDamageno(self):
		absDamVeriDiff = self.dataByDamageno.total_damage_price - self.dataByDamageno.total_verify_price	#calculate absolute diff
		maxDamVeriDiff = absDamVeriDiff.max()
		minDamVeriDiff = absDamVeriDiff.min()
		normDamVeriDiff = (absDamVeriDiff - minDamVeriDiff) / (maxDamVeriDiff - minDamVeriDiff)
		return normDamVeriDiff.std()

	def getNormStdProvince(self):
		damPriceProvince = self.data.groupby(['damage_no','province'], as_index = False)['total_damage_price'].sum()
		veriPriceProvince = self.data.groupby(['damage_no','province'], as_index = False)['total_verify_price'].sum()
		absDiffProvince = DataFrame([damPriceProvince.province.astype(str), damPriceProvince.total_damage_price - veriPriceProvince.total_verify_price]).transpose()
		minMaxDiff = [absDiffProvince.groupby('province',as_index=False)['Unnamed 0'].min(), absDiffProvince.groupby('province',as_index=False)['Unnamed 0'].max()]
		combineDiff = pd.merge(absDiffProvince, minMaxDiff[0], on='province')
		combineDiff = pd.merge(combineDiff, minMaxDiff[1], on='province')
		combineDiff['diff'] = combineDiff['Unnamed 0_x'].astype(int) - combineDiff['Unnamed 0_y']
		combineDiff['maxDiff'] = combineDiff['Unnamed 0'] - combineDiff['Unnamed 0_y']
		combineDiff['normDiff'] = combineDiff['diff']/combineDiff['maxDiff']
		print (combineDiff)
		return combineDiff.groupby('province')['normDiff'].std().to_frame(name='normStd')
	
	def getNormStdTime(self):
		timePrice = DataFrame(self.data, columns=['damage_no','receive_time','total_damage_price','total_verify_price'])
		timePrice['yearMonth'] = [str(i.year) + str(i.month) for i in timePrice['receive_time']]
		damageVerifyPrice = timePrice.groupby(['damage_no','yearMonth'], as_index=False)['total_damage_price','total_verify_price'].sum()
		damageVerifyPrice['priceDiff'] = damageVerifyPrice['total_damage_price'] - damageVerifyPrice['total_verify_price']
		minMaxPriceDiff = [damageVerifyPrice.groupby('yearMonth',as_index=False)['priceDiff'].min().add_prefix('min_'), damageVerifyPrice.groupby('yearMonth',as_index=False)['priceDiff'].max().add_prefix('max_')]
		damageVerifyPrice = damageVerifyPrice.merge(minMaxPriceDiff[0],left_on = 'yearMonth',right_on='min_yearMonth').merge(minMaxPriceDiff[1], left_on = 'yearMonth', right_on='max_yearMonth')
		damageVerifyPrice['normPriceDiff'] = (damageVerifyPrice['priceDiff'] - damageVerifyPrice['min_priceDiff']) / (damageVerifyPrice['max_priceDiff'] - damageVerifyPrice['min_priceDiff'])
		return damageVerifyPrice.groupby('yearMonth')['normPriceDiff'].std()