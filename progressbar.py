import sys
import os

def init():
	bar_width = os.get_terminal_size().columns - 7

	sys.stdout.write('[%s]' % (' ' * bar_width))
	sys.stdout.flush()
	sys.stdout.write('\r[\n')

def update(progress):
	sys.stdout.write('\033[F') # go to beginning of previous line

	bar_width = os.get_terminal_size().columns - 7

	fill_count = round(progress * bar_width)
	sys.stdout.write('[' + '-' * fill_count)

	blank_count = round((1.0 - progress) * bar_width)
	progress = int(progress * 100)
	padding = '   '[:-len(str(progress))]
	sys.stdout.write(' ' * blank_count + '] ' + padding + str(progress) + '%\n')
	sys.stdout.flush()