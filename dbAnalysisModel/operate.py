import pandas
from pandas import Series, DataFrame

class transformToPandas(object):
	def __init__(self, data, fields):
		self.data = DataFrame(data, columns=fields)

class Process(transformToPandas):
	def __init__(self, data, fields):
		super(Process, self).__init__(data, fields)

	def groupData(self, groupColumns, asIndex, resultColumns):
		data = self.data.groupby(groupColumns, as_index=asIndex)resultColumns
		return data

