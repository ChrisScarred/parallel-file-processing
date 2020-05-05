from multiprocessing import Pool, cpu_count
import os
from fsplit.filesplit import FileSplit
FILES = []

def main():
	res = multiFunction()
	print(res)

# divides files into multiple chunks and runs desired function in parallel on chunks
def multiFunction():
	# number of chunks and processes equal to cpu count
	processes = int(os.getenv('CPU_COUNT', cpu_count()))

	chunk = chunks('text.txt',processes)

	results = []

	with Pool(processes=processes) as pool:
		result = pool.map(doSth, chunk)
		results.append(result)

	return results

# placeholder for the function to be parallelised
def doSth(filename):
	f = open(filename, "r")
	words = f.read()
	words = words.split(None, 1)
	if len(words)>0:
		return words[0]
	else:
		return 'empty'

# splitting files via FileSplit, more info of pypi
def chunks(path, chunksize):
	def func(f, s, c):
		global FILES
		FILES.append(f)

	fs = FileSplit(file=path, splitsize=(os.path.getsize(path)/chunksize))
	fs.split(callback=func)
	return FILES

if __name__ == "__main__":
    main()