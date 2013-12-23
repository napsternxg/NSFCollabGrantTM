import pandas as pd

collab_data = pd.read_csv("collab_awards.csv", sep='\t',
	na_values = {'AbstractNarration': ''})

def getNSFDivisions():
	div_list = collab_data.drop_duplicates('NSFDivision')['NSFDivision']
	return div_list

def getAbstractForDiv(div):
	return collab_data[collab_data['NSFDivision'] == div]['AbstractNarration'].dropna()
	

if __name__ == "__main__":
	print getAbstractForDiv(getNSFDivisions()[0])
