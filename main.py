import cProfile
import json
from os import stat
from word.pipeline import WordGeneratorPipeline
from html.pipeline import HtmlGeneratorPipeline
from latex.pipeline import LatexGeneratorPipeline
import concurrent.futures
import time
import numpy as np
np.random.seed(0)


def generate_serial(func,config):
	return func(config)


def generate_parallel(func,args):
	path = args['path']
	if func == 'latex':
			latex_pipeline = LatexGeneratorPipeline(path)
			f = latex_pipeline.generate_data
	elif func=='html':
			html_pipeline = HtmlGeneratorPipeline(path)
			f = html_pipeline.generate_data
	else:
			word_pipeline = WordGeneratorPipeline(path)
			f = word_pipeline.generate_data
	table = args['table']
	prof = cProfile.Profile()
	prof.enable()
	r = f(args)
	prof.disable()
	prof.dump_stats("".join(['profiles/',table+'_parallel','.profile']))
	return r

def parallel_run(funcs,config):
	tables = ['latex','html','word']
	args = [{ 'table':t,**config[t],'path':config['path']} for t in tables]
	with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:        
		for dataset,stats in zip(tables,executor.map(generate_parallel,funcs,args)):
				print(f'{dataset} : Done' )
		


		# executor.shutdown(wait=True)
def serial_run(funcs,config):
	tables =  ['latex','html','word']
	for index in range(len(funcs)):
		prof = cProfile.Profile()
		prof.enable()
		generate_serial(funcs[index],config[tables[index]])
		prof.disable()
		prof.dump_stats("".join(['profiles/',tables[index]+'_serial','.profile']))
		print(f'{tables[index]} : Done' )

def time_serial_pipeline(pipeline,config,output):
	prof = cProfile.Profile()
	prof.enable()
	c,s = pipeline.generate_data_parallel(config)
	prof.disable()
	prof.dump_stats("".join(['profiles/',output,'.profile']))
	return c,s

def main(config):
	path = 'sources/*.csv'
	parallel = config['parallel']

	latex_pipeline = LatexGeneratorPipeline(path)

	latex_pipeline.generate_data(config['latex'])
	word_pipeline = WordGeneratorPipeline(path)
	html_pipeline = HtmlGeneratorPipeline(path)

	serial_funcs = [latex_pipeline.generate_data,html_pipeline.generate_data,word_pipeline.generate_data]
	parallel_funcs = ['latex','html','word']
	parallel = False
	if parallel:
		print('Parallel generation')
		config['path'] = path
		start = time.time()
		parallel_run(parallel_funcs,config)
		end = time.time()
		print(f'Time taken for parallel dataset generation {end-start}, seconds')
	else:
		print('Sequential generation')
		serial_run(serial_funcs,config)		

if __name__=='__main__':
	with open('config.json','r') as f:
		config = json.load(f)
	print(1)
	main(dict(config))
