import glob
import pandas as pd 
import numpy as np
from numpy.lib.recfunctions import stack_arrays
from root_numpy import root2rec

def root2panda(files_path, tree_name):
	'''
	Args:
	-----
		files_path: a string like './data/*.root', for example
		tree_name: a string like 'Collection_Tree' corresponding to the name of the folder inside the root 
		           file that we want to open
	Returns:
	--------	
		output_panda: a panda dataframe like allbkg_df in which all the info from the root file will be stored
	
	Note:
	-----
	    if you are working with .root files that contain different branches, you might have to mask your data
	    in that case, return pd.DataFrame(ss.data)
	'''
	
	files = glob.glob(files_path)

	# -- check whether a name was passed for the tree_name --> for root files with only one tree and no folders, 
	# -- you do not need to specify any name (I believe)
	if (tree_name == ''):
		ss = stack_arrays([root2rec(fpath) for fpath in files])
	else:
		ss = stack_arrays([root2rec(fpath, tree_name) for fpath in files])

	return pd.DataFrame(ss)

def flatten(column):
    '''
	Args:
	-----
		column: a column of a pandas df whose entries are lists (or regular entries -- in which case nothing is done)
		        e.g.: my_df['some_variable'] 

	Returns:
	--------	
		flattened out version of the column. 

		For example, it will turn:
		[1791, 2719, 1891]
		[1717, 1, 0, 171, 9181, 537, 12]
		[82, 11]
		...
		into:
		1791, 2719, 1891, 1717, 1, 0, 171, 9181, 537, 12, 82, 11, ...
	'''
    try:
        return np.array([v for e in column for v in e])
    except (TypeError, ValueError):
        return column