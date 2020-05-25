from setuptools import setup,find_packages

setup(
	name='area1_DL_code',
	version='0.1',
	scripts=['predictor.py'],
	packages=find_packages(),
	install_requires=[
	'keras',
	'h5py',
	'sklearn'])
