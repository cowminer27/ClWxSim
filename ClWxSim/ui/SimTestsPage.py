import tkinter as tk
from tkinter import ttk

import numpy as np

import ClWxSim.sim.fluid_solver as solver

# Pages
from ClWxSim.ui.SimControlPage import SimControlPage

LARGE_FONT= ("Verdana", 12)

class SimTestsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        self.wld_ref = None

        # Create Parts:
            # Heading
        label = tk.Label(self, text="Debug Commands", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

            # Heading
        label = tk.Label(self, text="Add Source:", font=("Verdana", 8))
        label.pack(pady=10,padx=10)

            # Add Source Options Frame
        add_source_frame = tk.Frame(self)

                # Source Option Entries
        self.source_field_names = "Value", "Centre X", "Centre Y", "Radius"
        self.source_fields = []

        for i in range(len(self.source_field_names)):
            lab = tk.Label(add_source_frame, width=25, text=self.source_field_names[i], anchor='w')
            ent = tk.Entry(add_source_frame)
            lab.grid(column=0, row=i, sticky='w')
            ent.grid(column=1, row=i)
            self.source_fields.append(ent)

        self.source_fields[0].insert(0, "0")
        self.source_fields[1].insert(0, "0")
        self.source_fields[2].insert(0, "0")
        self.source_fields[3].insert(0, "0")

        add_source_frame.pack(padx=5, pady=10)

            # Add Source Buttons Frame
        add_source_btns_frame = tk.Frame(self)

                # Add Pressure Button
        add_p_btn = ttk.Button(add_source_btns_frame, text="Add Pressure", command=self.add_pressure)
        add_p_btn.grid(row=0, column=0)

                # Add Wind U Vector Button
        add_wu_btn = ttk.Button(add_source_btns_frame, text="Add Wind U Vector", command=self.add_wind_u)
        add_wu_btn.grid(row=0, column=1)

                # Add Wind V Vector Button
        add_wv_btn = ttk.Button(add_source_btns_frame, text="Add Wind V Vector", command=self.add_wind_v)
        add_wv_btn.grid(row=0, column=2)

        add_source_btns_frame.pack(padx=5, pady=10)

            # Heading
        label = tk.Label(self, text="Get Cell Data:", font=("Verdana", 8))
        label.pack(pady=10,padx=10)

            # Add Cell Data Entries Frame
        cell_data_entries_frame = tk.Frame(self)

                # Cell Data Entries
        self.cell_data_field_names = "Cell X", "Cell Y"
        self.cell_data_fields = []

        for i in range(len(self.cell_data_field_names)):
            lab = tk.Label(cell_data_entries_frame, width=25, text=self.cell_data_field_names[i], anchor='w')
            ent = tk.Entry(cell_data_entries_frame)
            lab.grid(column=0, row=i, sticky='w')
            ent.grid(column=1, row=i)
            self.cell_data_fields.append(ent)

        self.cell_data_fields[0].insert(0, "0")
        self.cell_data_fields[1].insert(0, "0")

        cell_data_entries_frame.pack(padx=5, pady=10)

            # Add Cell Data View Frame
        cell_data_frame = tk.Frame(self)

                # Set cell data button
        self.p_data_label = tk.Label(cell_data_frame, text="Pressure: Null")
        self.p_data_label.grid(row=0, column=0)

        self.u_data_label = tk.Label(cell_data_frame, text="Wind U: Null")
        self.u_data_label.grid(row=0, column=1)

        self.v_data_label = tk.Label(cell_data_frame, text="Wind V: Null")
        self.v_data_label.grid(row=0, column=2)

        get_data_btn = ttk.Button(cell_data_frame, text="View Cell Data", command=self.view_cell_data)
        get_data_btn.grid(row=0, column=3)

        cell_data_frame.pack(padx=5, pady=10)

    def onFirstShow(self):
        # Create world reference
        self.wld_ref = self.cont.frames[SimControlPage].wld

# Commands
    def view_cell_data(self):
        x = int(self.cell_data_fields[1].get())
        y = int(self.cell_data_fields[0].get())

        self.p_data_label.config(text=self.wld_ref.air_pressure[x, y])
        self.u_data_label.config(text=self.wld_ref.air_vel_u[x, y])
        self.v_data_label.config(text=self.wld_ref.air_vel_v[x, y])

    def add_pressure(self):
        # Get entry vals
        val = float(self.source_fields[0].get())
        cx = int(self.source_fields[1].get())
        cy = int(self.source_fields[2].get())
        r = int(self.source_fields[3].get())

        # Calculate source array
        arr = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        x = np.arange(0, self.wld_ref.grid_size)
        y = np.arange(0, self.wld_ref.grid_size)

        mask = (x[np.newaxis,:] - cx) ** 2 + (y[:,np.newaxis] - cy) ** 2 < r ** 2
        arr[mask] = val

        # Add source array to pressure
        solver.add_source(self.wld_ref.wld_grid_size, self.wld_ref.air_pressure, arr, self.wld_ref.dt)

    def add_wind_u(self):
        # Get entry vals
        val = float(self.source_fields[0].get())
        cx = int(self.source_fields[1].get())
        cy = int(self.source_fields[2].get())
        r = int(self.source_fields[3].get())

        # Calculate source array
        arr = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        x = np.arange(0, self.wld_ref.grid_size)
        y = np.arange(0, self.wld_ref.grid_size)

        mask = (x[np.newaxis,:] - cx) ** 2 + (y[:,np.newaxis] - cy) ** 2 < r ** 2
        arr[mask] = val

        # Add source array to wind u
        solver.add_source(self.wld_ref.wld_grid_size, self.wld_ref.air_vel_u, arr, self.wld_ref.dt)

    def add_wind_v(self):
        # Get entry vals
        val = float(self.source_fields[0].get())
        cx = int(self.source_fields[1].get())
        cy = int(self.source_fields[2].get())
        r = int(self.source_fields[3].get())

        # Calculate source array
        arr = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        x = np.arange(0, self.wld_ref.grid_size)
        y = np.arange(0, self.wld_ref.grid_size)

        mask = (x[np.newaxis,:] - cx) ** 2 + (y[:,np.newaxis] - cy) ** 2 < r ** 2
        arr[mask] = val

        # Add source array to wind v
        solver.add_source(self.wld_ref.wld_grid_size, self.wld_ref.air_vel_v, arr, self.wld_ref.dt)
