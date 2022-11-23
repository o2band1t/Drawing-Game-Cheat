#uses python3.9.7

import tkinter as tk
from tkinter import filedialog
import cv2 as cv
import numpy as np
from PIL import Image, ImageTk
from pynput import mouse
from time import sleep


def file_popup() -> str:
	fname = filedialog.askopenfilename(initialdir='imgs')
	return fname


def draw(img: np.ndarray, delay: int, tval:int, res_dims=None) -> None:
	if res_dims is None:
		r_img = img
	else:
		r_img = cv.resize(img, res_dims, interpolation=cv.INTER_AREA)
	
	gray = cv.cvtColor(r_img, cv.COLOR_BGR2GRAY)
	_, bnzd =  cv.threshold(gray, tval, 255, cv.THRESH_BINARY_INV)
	
	coords = []
	for y_idx, row in enumerate(bnzd):
		coords += \
		[(x_idx, y_idx) for x_idx, px in enumerate(row) if px > 0]
	
	cursor = mouse.Controller()
	lmb = mouse.Button.left
	sleep(delay)
	topleft = cursor.position
	for c in coords:
		cursor.position = (c[0]+topleft[0], c[1]+topleft[1])
		cursor.click(lmb, 1)


if __name__ == '__main__':

	app = tk.Tk()
	app.geometry('425x450')
	app.title('B&W Drawing Cheat v1.0')

	
	app.selected_img_path = tk.StringVar()
	app.thresh_val = tk.IntVar()
	app.active_arrays = []
	app.active_previews = []
	app.active_preview_arrays = []
	
	
	app.thresh_val.set(120)
	app.active_arrays.append(cv.imread('imgs/blank.jpeg'))
	app.active_preview_arrays.append(
		cv.threshold(
			cv.imread('imgs/blank.jpeg'),
			120,
			255,
			cv.THRESH_BINARY
		)[1]
	)
	app.active_previews.append(
		ImageTk.PhotoImage(
			Image.fromarray(
				cv.resize(
					app.active_preview_arrays[0],
					(200, 200)
				)
			)
		)
	)
	
	
	tk.Label(
		app, 
		text='Enter path of image to use:',
		font=('Arial', 12, 'bold')
	).place(x=30, y=18)
	
	
	e_path = tk.Entry(app, width=25, font=('Arial', 14))
	e_path.place(x=30, y=45)
	
	
	b_path = tk.Button(
		app,
		text='...',
		command=lambda: [
			e_path.delete(0, tk.END),
			app.selected_img_path.set(file_popup()), 
			e_path.insert(0, app.selected_img_path.get())
			]
	)
	b_path.place(x=350, y=45)


	s_thresh = tk.Scale(app, from_=0, to=255, orient=tk.HORIZONTAL)
	s_thresh.place(x=280, y=150)
	s_thresh.set(120) #default thresh val 120


	b_load = tk.Button(
		app,
		text='Load Image',
		padx=50,
		pady=10,
		command=lambda: [
			app.active_arrays.pop(0) 
			if len(app.active_arrays) > 0 
			else None,
			
			app.active_arrays.append(
				cv.imread(e_path.get())
			) 
			if len(e_path.get()) > 0 
			else None,
			
			app.active_preview_arrays.pop(0)
			if len(app.active_preview_arrays) > 0
			else None,

			app.active_preview_arrays.append(
				cv.threshold(
					cv.cvtColor(
						cv.imread(e_path.get()),
						cv.COLOR_BGR2GRAY
					),
					120,
					255,
					cv.THRESH_BINARY
				)[1]
			)
			if len(e_path.get()) > 0 
			else None,
			
			app.active_previews.pop(0) 
			if len(app.active_previews) > 0 
			else None,
			
			app.active_previews.append(
				ImageTk.PhotoImage(
					Image.fromarray(
						cv.resize(
							app.active_preview_arrays[0],
							(200, 200)
						)
					)
				)
			) 
			if len(e_path.get()) > 0 
			else None,
			
			l_preview.config(
				image=app.active_previews[0]
			) 
			if len(app.active_previews) > 0 
			else None,

			s_thresh.set(120)
		]
	)
	b_load.place(x=30, y=75)

	
	tk.Label(
		app, 
		text='Selected image:',
		font=('Arial', 12, 'bold')
	).place(x=30, y=125)

	
	tk.Label(
		app, 
		text='Threshold:',
		font=('Arial', 12, 'bold')
	).place(x=280, y=125)


	l_preview = tk.Label(
			app,
			image=app.active_previews[0]
		)
	l_preview.place(x=30, y=150)

	
	b_thresh = tk.Button(
		app, 
		text='Binarize', 
		padx=21, 
		pady=15,
		command=lambda: [
			app.active_preview_arrays.append(
				cv.threshold(
					cv.cvtColor(
						app.active_arrays[0],
						cv.COLOR_BGR2GRAY
					),
					s_thresh.get(),
					255,
					cv.THRESH_BINARY
				)[1]
			)
			if len(app.active_arrays[0]) > 0
			else None,
			
			app.active_preview_arrays.pop(0)
			if len(app.active_preview_arrays[0]) > 1
			else None,

			app.active_previews.append(
				ImageTk.PhotoImage(
					Image.fromarray(
						cv.resize(
							app.active_preview_arrays[0],
							(200, 200)
						)
					)
				)
			)
			if len(app.active_preview_arrays) > 0
			else None,

			app.active_previews.pop(0)
			if len(app.active_previews) > 1
			else None,

			l_preview.config(image=app.active_previews[0]),

			app.thresh_val.set(int(s_thresh.get()))
		]
	)
	b_thresh.place(x=280, y=190)
	
	
	tk.Label(
		app, 
		text='Resize (px):',
		font=('Arial', 12, 'bold')
	).place(x=280, y=255)


	e_resize = tk.Entry(app, width=10, font=('Arial', '14'))
	e_resize.place(x=280, y=282)
	e_resize.insert(0, '200 200') #default 200x200 px


	tk.Label(
		app, 
		text='Delay (s):',
		font=('Arial', 12, 'bold')
	).place(x=280, y=325)


	e_delay = tk.Entry(app, width=10, font=('Arial', '14'))
	e_delay.place(x=280, y=352)
	e_delay.insert(0, '4') #default 200x200 px

	b_draw = tk.Button(
		app,
		text='Draw',
		font=('Arial', '14', 'bold'),
		padx=74,
		pady=20,
		command=lambda: [
			s_thresh.set(app.thresh_val.get()),
			print(f'{app.active_preview_arrays[0].shape}'), #############
			draw(
				app.active_arrays[0],
				int(e_delay.get()),
				int(app.thresh_val.get()),
				tuple(map(int, e_resize.get().split()))
			)
		]
	).place(x=30, y=360)


	app.mainloop()
