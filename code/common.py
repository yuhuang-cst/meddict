# encoding: UTF-8

"""
@author: hy
"""

def dictListAdd(k, v, d):
	if k in d:
		d[k].append(v)
	else:
		d[k] = [v]


def dictSetAdd(k, v, d):
	if k in d:
		d[k].add(v)
	else:
		d[k] = {v}


if __name__ == '__main__':
	pass


