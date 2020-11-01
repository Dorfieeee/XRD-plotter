import os
import re
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FixedLocator)
import numpy as np

def main() -> None:
	noise = read_noise()

	products = read_products()
	
	draw_graph(noise, products)


def draw_graph(noise, products):
	nrows = len(noise) + len(products)
	# Init graph figure
	figure, axes = plt.subplots(nrows=nrows, ncols=1, figsize=[8, 12], dpi=300)
	figure.suptitle('XRD NAME', fontsize=20)
	#figure.tight_layout()
	plt.figtext(0.05, 0.65, "Intensity (a.u.)", fontsize=16,
		rotation='vertical', horizontalalignment='left')
	plt.figtext(0.5, 0.05, "2theta (degree)", fontsize=16,
        horizontalalignment='center',
        verticalalignment='center')
	# Remove Y gaps in between subplots
	plt.subplots_adjust(hspace=0)
	# Plot counter
	pc = 0

	# draw noise plots
	for data in noise:
		x = data[0]
		y = data[1]
		axes[pc].plot(x, y, color='black', label=f"Label-{pc}")
		axes[pc].legend()
		# Set range of X and Y axis
		axes[pc].set_xlim(xmin=10, xmax=60)
		axes[pc].set_ylim(ymin=0, ymax=400)
		# # Set tick labels to nothing
		axes[pc].tick_params(labelbottom=False, labelleft=False)
		# Set minor and major X axis ticks
		axes[pc].xaxis.set_minor_locator(MultipleLocator(2.5))
		axes[pc].xaxis.set_major_locator(MultipleLocator(5))
		# Set minor and major Y axis ticks
		axes[pc].yaxis.set_minor_locator(MultipleLocator(50))
		axes[pc].yaxis.set_major_locator(MultipleLocator(100))
		# Change direction of all ticks
		axes[pc].tick_params(which='both', direction='in', bottom=True, right=True, left=True, top=(pc == 0))

		pc += 1

	# draw product plots
	for data in products:
		axes[pc].bar(data[0], data[1], width=0.2, label=f"Label-{pc}")
		axes[pc].legend()
		axes[pc].sharex(axes[1])
		axes[pc].set_ylim(ymin=0, ymax=1100)
		# Set minor and major Y axis ticks
		axes[pc].yaxis.set_minor_locator(MultipleLocator(150))
		axes[pc].yaxis.set_major_locator(MultipleLocator(300))

		axes[pc].tick_params(which='both', direction='in', bottom=True, right=True, left=True, top=False, labelsize=12)

		axes[pc].tick_params(labelbottom=(pc == nrows - 1), labelleft=False)
		pc += 1

	plt.savefig(os.getcwd() + "/output/xrd_graph")


def read_noise():
	noise = []
	noise_files = [filename for filename in os.listdir("./source/") if filename.endswith('.txt')]
	for i, file in enumerate(noise_files):
		with open("./source/" + file, 'r', newline='') as f:
			reader = f.readlines()

		x = []
		y = []
		is_data = False

		for row in reader:
			if is_data:
				pair = [x[0] for x in re.finditer(r"(\d*\.?\d+)", row.strip())]

				if pair:
					try:
						x.append(float(pair[0]))
						y.append(float(pair[1]))
					except:
						raise SystemExit(f"One or both values in {pair} could not be converted to number.")

			if "[Data]" in row:
				is_data = True

		noise.append([x, y])

	return noise


def read_products():
	products = []
	product_files = [filename for filename in os.listdir("./source/") if '$A' in filename]
	for i, file in enumerate(product_files):
		with open("./source/" + file, 'r', newline='') as f:
			reader = f.readlines()

		data = {}

		for row in reader:
			pair = [x[0] for x in re.finditer(r"(\d*\.?\d+)", row.strip())]

			if pair:
				try:
					x = float(pair[0])
					y = float(pair[1])
				except:
					raise SystemExit(f"One or both values in {pair} could not be converted to number.")
					
				if not x in data:
					data[x] = y
		
		x = list(data.keys())
		y = list(data.values())

		products.append([x, y])
		
	return products


if __name__ == "__main__":
	main()