import sys
import os
import random
import io
import contextlib

from Simulator import *
from ToSeesawComp import *
from GuiGatesClasses import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk


#######################################################
###            Dialog Box For User Input            ###
#######################################################
class BucketDialog(tk.Toplevel):
    def __init__(self, parent, suggested_name = "in1"):
        super().__init__(parent)
        self.title("New Bucket")
        self.minsize(200, 0)
        
        self.result = None
        
        tk.Label(self, text="Name").pack()
        self.entry = tk.Entry(self, width=18)
        self.entry.insert(tk.END, suggested_name)
        self.entry.pack()        
        
        # create label and combobox
        label = ttk.Label(self, text="Value:")
        label.pack()
        self.combobox = ttk.Combobox(self, values=["ON", "OFF", "EMPTY"], state="readonly", 
                                     width=15, height=5, justify='center')
        self.combobox.set("ON")
        self.combobox.pack(pady=10)
        
        # create ok and cancel buttons
        ok_button = ttk.Button(self, text="OK", command=self.ok)
        ok_button.pack(side="left", padx=10, pady=10)
        cancel_button = ttk.Button(self, text="Cancel", command=self.cancel)
        cancel_button.pack(side="right", padx=10, pady=10)
        
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))

    def ok(self):
        self.result = ( self.entry.get(), self.combobox.get() )
        self.destroy()

    def cancel(self):
        self.destroy()

               
#######################################################
###             Main Application Class              ###
#######################################################
class Application(tk.Tk):   
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("HDS GUI")
        self.add_gates_map()

        # Set up the notebook and tabs
        self.notebook = tk.ttk.Notebook(self)
        self.tabSchematic = tk.ttk.Frame(self.notebook)
        self.tabNetlist = tk.ttk.Frame(self.notebook)
        self.tabSimulate = tk.ttk.Frame(self.notebook)
        self.tabBuckets = tk.ttk.Frame(self.notebook)
        self.tabSeesawComp = tk.ttk.Frame(self.notebook)
        self.notebook.add(self.tabSchematic, text="Schematic  ")
        self.notebook.add(self.tabNetlist, text="Netlist  ")
        self.notebook.add(self.tabSimulate, text="Simulation  ")
        self.notebook.add(self.tabBuckets, text="Buckets  ")
        self.notebook.add(self.tabSeesawComp, text="Seesaw Compiler")
        self.notebook.pack(expand=True, fill=tk.BOTH)
        
        self.setup_schematic_tab()
        self.setup_netlist_tab()
        self.setup_simulate_tab()
        self.setup_buckets_tab()
        self.setup_seesaw_compiler_tab()
        
    def add_gates_map(self):    
        # Get gates defined for simulator with proper print and image
        self.constructors = get_gates_map()
    
        self.sb_gates =[]
        self.db_gates = []
        for key in self.constructors:
            if key.endswith("SB"):
                self.sb_gates.append(key[:-2])
            elif key.endswith("DB"):
                self.db_gates.append(key[:-2])
            else:
                print("ERROR: gate constructor key is in unknown format")
    

    #######################################################
    ###                 Schematic Tab                   ###
    #######################################################
    def setup_schematic_tab(self):
        self.tabSchematic.frame = tk.Frame(self.tabSchematic)
        self.tabSchematic.frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # create the radio buttons
        self.tabSchematic.selected_option = tk.StringVar(value="SB")
        sb = ttk.Radiobutton(self.tabSchematic.frame, text="Simple Buckets", variable=self.tabSchematic.selected_option, value="SB",
                                                      command=self.on_radio_button_changed)
        sb.pack(side=tk.TOP)
        db = ttk.Radiobutton(self.tabSchematic.frame, text="Dual Buckets", variable=self.tabSchematic.selected_option, value="DB",
                                                      command=self.on_radio_button_changed)
        db.pack(side=tk.TOP,pady=(0,20))
       
        # Create a label widget and set its text to the name of the listbox
        self.tabSchematic.frame.listbox_label = tk.Label(self.tabSchematic.frame, text="Available Gates:")
        self.tabSchematic.frame.listbox_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create a listbox widget and add it to the first tab
        self.tabSchematic.frame.listbox = tk.Listbox(self.tabSchematic.frame, selectmode="SINGLE")
        self.tabSchematic.frame.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Create a panel widget and add it to the first tab
        self.tabSchematic.panel = tk.Canvas(self.tabSchematic, width=800, height=800, bg="white")
        self.tabSchematic.panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        
        # Add items to the listbox
        self.on_radio_button_changed()
        
        # Create an "Add Gate" button and add it to the first tab
        self.tabSchematic.frame.add_gate_button = tk.Button(self.tabSchematic.frame, text="Add Gate", command=self.add_gate_item)
        self.tabSchematic.frame.add_gate_button.pack(side=tk.TOP)
        
        # Create a label widget and set its text to the name of the Table
        self.tabSchematic.frame.table_label = tk.Label(self.tabSchematic.frame, text="Buckets:")
        self.tabSchematic.frame.table_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=(50,0))
  
        # create a buckets table in the first tab
        self.tabSchematic.frame.table = ttk.Treeview(self.tabSchematic.frame, columns=('Name', 'Value'), show='headings')
        self.tabSchematic.frame.table.column('Name', minwidth=0, width=60, stretch=tk.NO)
        self.tabSchematic.frame.table.heading('Name', text='Name')        
        self.tabSchematic.frame.table.column('Value', minwidth=0, width=50, stretch=tk.NO)
        self.tabSchematic.frame.table.heading('Value', text='Value')
        self.tabSchematic.frame.table.pack(side=tk.TOP)
        
        # Create an "Add Gate" button and add it to the first tab
        self.tabSchematic.frame.add_bucket_button = tk.Button(self.tabSchematic.frame, text="Add Bucket", command=self.add_bucket_item)
        self.tabSchematic.frame.add_bucket_button.pack(side=tk.TOP)
        
        # Create button and add it to the first tab
        self.tabSchematic.frame.del_bucket_button = tk.Button(self.tabSchematic.frame, text="Delete Bucket", command=self.delete_bucket_item)
        self.tabSchematic.frame.del_bucket_button.pack(side=tk.TOP)
              
    def add_bucket_item(self):
        dialog = BucketDialog(self.tabSchematic)
        self.tabSchematic.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name, val] = dialog.result
            self.tabSchematic.frame.table.insert('', 'end', values=(name, val))
            
    def delete_bucket_item(self):
        selected_items = self.tabSchematic.frame.table.selection() 
        for item in selected_items:
            self.tabSchematic.frame.table.delete(item) 
                    
    # Define a function to handle adding an item to the gates panel canvas
    def add_gate_item(self):
        if not self.tabSchematic.frame.listbox.curselection():
            return
            
        # Get the selected item from the listbox
        selected_index = self.tabSchematic.frame.listbox.curselection()[0]
        selected_item = self.tabSchematic.frame.listbox.get(selected_index)

        constructor = self.constructors[selected_item+self.tabSchematic.selected_option.get()]
        label = constructor(master=self.tabSchematic.panel)
            
        if not 'label' in locals() or not hasattr(label, 'master'):
            return
        
        # Add the label widget to the canvas
        label.add_to_panel()
        
        #Place in random position so gates will no overlap
        label.on_drag_motion(random.randint(1, 100) , random.randint(1, 200))  
              
        # Bind the label widget to the dragging events
        label.bind("<ButtonPress-1>", self.on_drag_start)
        label.bind("<B1-Motion>", self.on_drag_motion)
        label.bind("<Button-3>", self.on_label_right_click)

    # Define a function to handle starting a drag operation on a label
    def on_drag_start(self,event):
        # Save the current position of the label
        widget = event.widget
        widget.drag_start_x = event.x
        widget.drag_start_y = event.y
        
    def on_label_right_click(self,event):
        self.right_clicked_widget = event.widget
        
        # create the label popup menu
        label_popup_menu = tk.Menu(self.tabSchematic.panel, tearoff=0)
        label_popup_menu.add_command(label="Delete", command=self.delete_label)
        label_popup_menu.add_command(label="Add interface buckets", command=self.add_interface_buckets)

        # display the right-click menu
        label_popup_menu.post(event.x_root, event.y_root)
        
    def delete_label(self):
        self.right_clicked_widget.destroy_all_labels()
        self.right_clicked_widget.destroy()
        self.right_clicked_widget = None
        
    def add_interface_buckets(self):
        blist = self.right_clicked_widget.add_interface_buckets()
        if blist:
            for b in blist:
                self.tabSchematic.frame.table.insert('', 'end', values=(b[0], b[1]))
        self.right_clicked_widget = None
        
    # Define a function to handle dragging a label
    def on_drag_motion(self,event):
        # Calculate the distance the label has been dragged
        widget = event.widget
        delta_x = int(event.x - widget.drag_start_x)
        delta_y = int(event.y - widget.drag_start_y)
        
        # Move the label to the new position
        widget.on_drag_motion(delta_x, delta_y)
        
    def on_radio_button_changed(self):
        self.tabSchematic.frame.listbox.delete(0, 'end')
        for child in self.tabSchematic.panel.winfo_children():
            child.destroy()
        if self.tabSchematic.selected_option.get() == "SB":
            for item in self.sb_gates:
                self.tabSchematic.frame.listbox.insert(tk.END, item)
        elif self.tabSchematic.selected_option.get() == "DB":
            for item in self.db_gates:
                self.tabSchematic.frame.listbox.insert(tk.END, item)
        
    #######################################################
    ###                  Netlist Tab                    ###
    #######################################################
    def setup_netlist_tab(self):
        self.tabNetlist.frame = tk.Frame(self.tabNetlist)
        self.tabNetlist.frame.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create t_step label and entry widgets 
        label_t_step = tk.Label(self.tabNetlist.frame, text="t_step:")
        label_t_step.grid(row=0, column=0)

        self.tabNetlist.frame.entry_t_step = tk.Entry(self.tabNetlist.frame)
        self.tabNetlist.frame.entry_t_step.insert(tk.END, "1")
        self.tabNetlist.frame.entry_t_step.grid(row=0, column=1)
        
        # Create t_step label and entry widgets 
        label_t_max = tk.Label(self.tabNetlist.frame, text="t_max:")
        label_t_max.grid(row=1, column=0)

        self.tabNetlist.frame.entry_t_max = tk.Entry(self.tabNetlist.frame)
        self.tabNetlist.frame.entry_t_max.insert(tk.END, "25000")
        self.tabNetlist.frame.entry_t_max.grid(row=1, column=1)
        
        # Create K_fast label and entry widgets 
        label_K_fast = tk.Label(self.tabNetlist.frame, text="K_fast:")
        label_K_fast.grid(row=0, column=2)

        self.tabNetlist.frame.entry_K_fast = tk.Entry(self.tabNetlist.frame)
        self.tabNetlist.frame.entry_K_fast.insert(tk.END, "0.000315")
        self.tabNetlist.frame.entry_K_fast.grid(row=0, column=3)
        
        # Create K_slow label and entry widgets 
        label_K_slow = tk.Label(self.tabNetlist.frame, text="K_slow:")
        label_K_slow.grid(row=1, column=2)

        self.tabNetlist.frame.entry_K_slow = tk.Entry(self.tabNetlist.frame)
        self.tabNetlist.frame.entry_K_slow.insert(tk.END, "0.000015*0.95")
        self.tabNetlist.frame.entry_K_slow.grid(row=1, column=3)
        
        # Create csv_fname label and entry widgets 
        label_csv_fname = tk.Label(self.tabNetlist.frame, text="csv_fname:")
        label_csv_fname.grid(row=2, column=0)

        self.tabNetlist.frame.entry_csv_fname = tk.Entry(self.tabNetlist.frame, width=50)
        self.tabNetlist.frame.entry_csv_fname.insert(tk.END, "sim_res.csv")
        self.tabNetlist.frame.entry_csv_fname.grid(row=2, column=1, columnspan=3)
   
        # Create an "Generate Code" button and add it to the tab
        self.tabNetlist.generate_button = tk.Button(self.tabNetlist, text="Generate Code", width=30, command=self.add_generate_code,\
                                                    bg="white", highlightthickness=3, highlightbackground="gray", font=("Helvetica", 12))
        self.tabNetlist.generate_button.pack(side=tk.TOP, pady=(0,10))
        
        # Create code label 
        label_code = tk.Label(self.tabNetlist, text="Simulator Code:")
        label_code.pack(side=tk.TOP)

        # Create a Text widget and pack it into the Netlist tab
        self.tabNetlist.text_widget = tk.Text(self.tabNetlist, height=30, width=110, wrap="none")
        self.tabNetlist.text_widget.pack(side=tk.TOP)
        
        xscrollbar = tk.Scrollbar(self.tabNetlist, orient=tk.HORIZONTAL)
        xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        xscrollbar.config(command=self.tabNetlist.text_widget.xview)
        self.tabNetlist.text_widget.config(xscrollcommand=xscrollbar.set)
        
        # Create an "Simulate" button and add it to the tab
        self.tabNetlist.simulate_button = tk.Button(self.tabNetlist, text="Simulate", width=30, command=self.simulate_netlist,\
                                                    bg="white", highlightthickness=3, highlightbackground="gray", font=("Helvetica", 12))
        self.tabNetlist.simulate_button.pack(side=tk.TOP, pady=30)
        
        # Create frame for saved script name 
        self.tabNetlist.sc_frame = tk.Frame(self.tabNetlist)
        self.tabNetlist.sc_frame.pack(side=tk.TOP, padx=10, pady=(10,0))
        
        # Create script_fname label and entry widgets 
        self.tabNetlist.sc_frame.label_script_fname = tk.Label(self.tabNetlist.sc_frame, text="script_fname:")
        self.tabNetlist.sc_frame.label_script_fname.grid(row=0, column=0)

        self.tabNetlist.sc_frame.entry_script_fname = tk.Entry(self.tabNetlist.sc_frame, width=50)
        self.tabNetlist.sc_frame.entry_script_fname.insert(tk.END, "run_me.py")
        self.tabNetlist.sc_frame.entry_script_fname.grid(row=0, column=1, columnspan=3)
        
        # Create an "GSave Script" button and add it to the tab
        self.tabNetlist.simulate_button = tk.Button(self.tabNetlist, text="Save Script", width=20, command=self.save_script)
        self.tabNetlist.simulate_button.pack(side=tk.TOP)
        
    def add_generate_code(self):
        self.tabNetlist.text_widget.delete('1.0', 'end')
        self.tabBuckets.frame.text_widget.delete('1.0', 'end')
        self.tabSeesawComp.frame.text_widget.delete('1.0', 'end')
    
        # Add always present code to text widget
        self.tabNetlist.text_widget.insert(tk.END, "import sys \n\n")
        self.tabNetlist.text_widget.insert(tk.END, "from Simulator import * \n")
        if self.tabSchematic.selected_option.get() == "DB":
            self.tabNetlist.text_widget.insert(tk.END, "from DualRailGates import * \n")
        else:
            self.tabNetlist.text_widget.insert(tk.END, "from Gates import * \n")
        self.tabNetlist.text_widget.insert(tk.END, "\n")    
        self.tabNetlist.text_widget.insert(tk.END, "def simulate_netlist():\n")
        self.tabNetlist.text_widget.insert(tk.END, "\ts = System()\n")
        
        # Set Simulator options
        self.tabNetlist.text_widget.insert(tk.END, "\ts.t_step = "+self.tabNetlist.frame.entry_t_step.get()+"\n")  
        self.tabNetlist.text_widget.insert(tk.END, "\ts.t_max = "+self.tabNetlist.frame.entry_t_max.get()+"\n")  
        self.tabNetlist.text_widget.insert(tk.END, "\ts.K_fast = "+self.tabNetlist.frame.entry_K_fast.get()+"\n")
        self.tabNetlist.text_widget.insert(tk.END, "\ts.K_slow = "+self.tabNetlist.frame.entry_K_slow.get()+"\n")
        self.tabNetlist.text_widget.insert(tk.END, "\ts.csv_fname = \""+self.tabNetlist.frame.entry_csv_fname.get()+"\"\n")
        self.tabNetlist.text_widget.insert(tk.END, "\n")    
        
        # Iterate over buckets table items
        bnames = []
        for child in self.tabSchematic.frame.table.get_children():
            name = self.tabSchematic.frame.table.item(child)["values"][0]
            val = self.tabSchematic.frame.table.item(child)["values"][1]
            if name in bnames:
                self.tabNetlist.text_widget.delete('1.0', 'end')
                self.tabNetlist.text_widget.insert(tk.END, "Error generating netlist. The following bucket appears twice: " + name)
                return
            bnames.append(name)
            if self.tabSchematic.selected_option.get() == "SB":
                self.tabNetlist.text_widget.insert(tk.END, "\t" + name +" = DnaBucket(\""+name+"\", Amounts."+val+")\n")
            elif self.tabSchematic.selected_option.get() == "DB":
                self.tabNetlist.text_widget.insert(tk.END, "\t" + name +" = DualBucket(\""+name+"\", Amounts."+val+")\n")
        self.tabNetlist.text_widget.insert(tk.END, "\n")
                
        # Iterate over the gates in the panel
        gnames = []
        labels = [widget for widget in self.tabSchematic.panel.winfo_children() if isinstance(widget, GateLabel)]
        for label in labels:
            name = label.get_name_string()
            if name in gnames:
                self.tabNetlist.text_widget.delete('1.0', 'end')
                self.tabNetlist.text_widget.insert(tk.END, "Error generating netlist. The following gate appears twice: " + name)
                return
            gnames.append(name)
            self.tabNetlist.text_widget.insert(tk.END, "\t" + name + " = " + label.get_type_string() + \
                                                       "(name=\"" + name + "\", " + label.get_ports_string()+ ")\n")
        self.tabNetlist.text_widget.insert(tk.END, "\n")
        
        # Add gates to simulator
        for name in gnames:
            self.tabNetlist.text_widget.insert(tk.END, "\ts.gates_list.append(" + name + ")\n")
        self.tabNetlist.text_widget.insert(tk.END, "\n")
        
        # Add simulate
        self.tabNetlist.text_widget.insert(tk.END, "\ts.simulate()\n\n")
        
        # Add main
        self.tabNetlist.text_widget.insert(tk.END, "def main() -> int:\n")
        self.tabNetlist.text_widget.insert(tk.END, "\tsimulate_netlist()\n")
        self.tabNetlist.text_widget.insert(tk.END, "\tplot_graphs(\""+self.tabNetlist.frame.entry_csv_fname.get()+"\")\n")       
        self.tabNetlist.text_widget.insert(tk.END, "\treturn 0\n\n")
        self.tabNetlist.text_widget.insert(tk.END, "if __name__ == '__main__':\n")
        self.tabNetlist.text_widget.insert(tk.END, "\tsys.exit(main())\n")
        
    def save_script(self):
        with open(self.tabNetlist.sc_frame.entry_script_fname.get(), "w") as file:
            file.write(self.tabNetlist.text_widget.get("1.0", "end"))

    def simulate_netlist(self):
        self.tabSimulate.ax.clear()
        self.tabSimulate.canvas.draw()  
        code = self.tabNetlist.text_widget.get("1.0", "end-8l")
        if len(code) < 1 or "simulate_netlist()" not in code:
            popup_window = tk.Toplevel()
            popup_window.title("Could not Simulate")
            popup_window.geometry("300x50")
            label = tk.Label(popup_window, text="The simulation could not be run due to bad netlist")
            label.pack(pady=10)
            return
        code += "\nsimulate_netlist()\n"
        exec(code)
        self.tabSimulate.entry_csv_fname.delete(0, 'end')
        self.tabSimulate.entry_csv_fname.insert(tk.END, self.tabNetlist.frame.entry_csv_fname.get())
        self.load_csv()

    #######################################################
    ###                 Simulation Tab                  ###
    #######################################################
    def setup_simulate_tab(self):
    
        # Create csv_fname label and entry widgets 
        label_csv_fname = tk.Label(self.tabSimulate, text="csv_fname:")
        label_csv_fname.pack(side=tk.TOP, fill=tk.BOTH)

        self.tabSimulate.entry_csv_fname = tk.Entry(self.tabSimulate, width=50)
        self.tabSimulate.entry_csv_fname.insert(tk.END, "sim_res.csv")
        self.tabSimulate.entry_csv_fname.pack(side=tk.TOP, fill=tk.BOTH)
    
        # Create a Frame for all signals in the csv file
        self.tabSimulate.frame = tk.Frame(self.tabSimulate)
        self.tabSimulate.frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        
        # Create an "Load csv" button and add it to the tab
        self.tabSimulate.frame.load_button = tk.Button(self.tabSimulate.frame, width=15, text="Load csv", command=self.load_csv)
        self.tabSimulate.frame.load_button.pack(side=tk.TOP)
        
        # Create a label widget and set its text to the name of the listbox
        self.tabSimulate.frame.listbox_label = tk.Label(self.tabSimulate.frame, width=35, text="Signals in csv:")
        self.tabSimulate.frame.listbox_label.pack(side=tk.TOP, fill=tk.BOTH)

        # Create a listbox widget and add it to the third tab
        self.tabSimulate.frame.listbox = tk.Listbox(self.tabSimulate.frame)              
        xscrollbar = tk.Scrollbar(self.tabSimulate.frame, orient=tk.HORIZONTAL)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tabSimulate.frame.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        xscrollbar.config(command=self.tabSimulate.frame.listbox.xview)
        self.tabSimulate.frame.listbox.config(xscrollcommand=xscrollbar.set)
        
        # Create button and add it to the tab
        self.tabSimulate.frame.add_bucket_button = tk.Button(self.tabSimulate.frame, text="Add", command=self.add_to_plotted)
        self.tabSimulate.frame.add_bucket_button.pack(side=tk.TOP)
        
        # Create a Frame for the plotted signals
        self.tabSimulate.plt_frame = tk.Frame(self.tabSimulate)
        self.tabSimulate.plt_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Create a label widget and set its text to the name of the listbox
        self.tabSimulate.plt_frame.listbox_label = tk.Label(self.tabSimulate.plt_frame, text="Signals to plot:")
        self.tabSimulate.plt_frame.listbox_label.pack(side=tk.TOP, fill=tk.BOTH)
        
        # Create a listbox widget and add it to the third tab
        self.tabSimulate.plt_frame.plt_listbox = tk.Listbox(self.tabSimulate.plt_frame, selectmode="SINGLE")
        self.tabSimulate.plt_frame.plt_listbox.pack(side=tk.TOP)
        
        # Create button and add it to the tab
        self.tabSimulate.plt_frame.add_bucket_button = tk.Button(self.tabSimulate.plt_frame, text="Delete", command=self.delete_from_plotted)
        self.tabSimulate.plt_frame.add_bucket_button.pack(side=tk.LEFT)
        
        # Create button and add it to the tab
        self.tabSimulate.plt_frame.plot_gui = tk.Button(self.tabSimulate.plt_frame, text="Plot in GUI", command=self.plot_in_gui)
        self.tabSimulate.plt_frame.plot_gui.pack(side=tk.TOP)
        
        # Create button and add it to the tab
        self.tabSimulate.plt_frame.plot_ext = tk.Button(self.tabSimulate.plt_frame, text="Plot External", command=self.plot_external)
        self.tabSimulate.plt_frame.plot_ext.pack(side=tk.TOP)
        
        # Create a Figure object to draw on
        self.tabSimulate.fig = Figure(figsize=(5, 5), dpi=100)
        
        # Create a subplot and plot some data
        self.tabSimulate.ax = self.tabSimulate.fig.add_subplot(111)
        
        # Create a Tkinter canvas to hold the plot
        self.tabSimulate.canvas = FigureCanvasTkAgg(self.tabSimulate.fig, master=self.tabSimulate)
        self.tabSimulate.canvas.draw()

        # Add the canvas to the app
        self.tabSimulate.canvas.get_tk_widget().pack(side=tk.RIGHT)
        
    def load_csv(self):
        df = pd.read_csv(self.tabSimulate.entry_csv_fname.get())
        buckets = list(df.columns)[1:]
        self.tabSimulate.frame.listbox.delete(0, 'end')
        for bucket in buckets:
            self.tabSimulate.frame.listbox.insert(tk.END, bucket)
            
    def add_to_plotted(self):
        # Get the selected items from the listbox
        selected_indexes = self.tabSimulate.frame.listbox.curselection()
        for selected_index in selected_indexes:
            selected_item = self.tabSimulate.frame.listbox.get(selected_index)
            if selected_item not in self.tabSimulate.plt_frame.plt_listbox.get(0, tk.END):
                self.tabSimulate.plt_frame.plt_listbox.insert(tk.END, selected_item)
            
    def delete_from_plotted(self):
        selection = self.tabSimulate.plt_frame.plt_listbox.curselection()
        if selection:
            self.tabSimulate.plt_frame.plt_listbox.delete(selection)
            
    def plot_in_gui(self): 
        self.tabSimulate.ax.clear()
        
        # Load data
        df = pd.read_csv(self.tabSimulate.entry_csv_fname.get())
        times = list(df['time'])

        styles = ('-', '--', '-.', ':', \
                  (0, (5, 5)), (0, (5, 10)), (0, (1, 10)), (0, (1, 1)), (5, (10, 3)), \
                  (0, (5, 1)), (0, (3, 10, 1, 10)), (0, (3, 5, 1, 5)), (0, (3, 1, 1, 1)), \
                  (0, (3, 5, 1, 5, 1, 5)), (0, (3, 10, 1, 10, 1, 10)), (0, (3, 1, 1, 1, 1, 1)) )
        linestyle = itertools.cycle((styles))
    
        for b in self.tabSimulate.plt_frame.plt_listbox.get(0, tk.END):
            amounts = df[b]
            self.tabSimulate.ax.plot(times, amounts, label=b, linestyle=next(linestyle))
            
        self.tabSimulate.ax.set_xlabel('Time [sec]')
        self.tabSimulate.ax.set_ylabel('DNA amount [nM]')
        self.tabSimulate.ax.legend()
        self.tabSimulate.ax.grid()    
        self.tabSimulate.canvas.draw()      

    def plot_external(self):
        plot_graphs(csv_fname=self.tabSimulate.entry_csv_fname.get(), buckets=self.tabSimulate.plt_frame.plt_listbox.get(0, tk.END))       
        
    #######################################################
    ###                  Buckets Tab                    ###
    #######################################################
    def setup_buckets_tab(self):
        # Create an "Show Netlist Buckets" button and add it to the tab
        self.tabBuckets.buckets_button = tk.Button(self.tabBuckets, text="Show Netlist Buckets", width=30, command=self.show_buckets,\
                                                   bg="white", highlightthickness=3, highlightbackground="gray", font=("Helvetica", 10))
        self.tabBuckets.buckets_button.pack(side=tk.TOP, pady=(10,10))
        
        # Create code label 
        label_code = tk.Label(self.tabBuckets, text="Buckets structure, and values at simulation start:")
        label_code.pack(side=tk.TOP)

        # Create a Frame for text widget
        self.tabBuckets.frame = tk.Frame(self.tabBuckets)
        self.tabBuckets.frame.pack(side=tk.TOP)

        # Create a Scrollbar for text widget
        yscrollbar = tk.Scrollbar(self.tabBuckets.frame, orient=tk.VERTICAL)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Text widget and pack it into the Buckets tab
        self.tabBuckets.frame.text_widget = tk.Text(self.tabBuckets.frame, height=40, width=110, wrap="none")
        self.tabBuckets.frame.text_widget.pack(side=tk.TOP)
        
        # Link the scrollbar to the text widget        
        yscrollbar.config(command=self.tabBuckets.frame.text_widget.xview)
        self.tabBuckets.frame.text_widget.config(yscrollcommand=yscrollbar.set)
        
    def show_buckets(self):
        self.tabBuckets.frame.text_widget.delete('1.0', 'end')
        
        code = self.tabNetlist.text_widget.get("1.0", "end-8l")
        if len(code) < 1 or "simulate_netlist()" not in code:
            self.tabBuckets.frame.text_widget.insert(tk.END, "Cannot show buckets for empty\\bad netlist")
            return
            
        new_sim_str = "\ts.csv_fname = \"temp_print_res.csv\"\n"
        new_sim_str += "\ts.t_max = 0\n"
        new_sim_str += "\ts.print_steps = True\n"
        new_sim_str += "\ts.simulate()"
        code = code.replace("\ts.simulate()", new_sim_str)
        code += "\nsimulate_netlist()\n"
        
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            exec(code)
            output = buf.getvalue()
        
        lines = output.splitlines()
        for line in lines[2:]:
            self.tabBuckets.frame.text_widget.insert(tk.END, line+"\n")  
            
        if len(self.tabBuckets.frame.text_widget.get("1.0", "end-1c")) == 0:
            self.tabBuckets.frame.text_widget.insert(tk.END, "No gates in the netlist")
  

    #######################################################
    ###              Seesaw Compiler Tab                ###
    #######################################################
    def setup_seesaw_compiler_tab(self):
        # Create an "Show Netlist Buckets" button and add it to the tab
        self.tabSeesawComp.translate_button = tk.Button(self.tabSeesawComp, text="Translate Netlist", width=30, command=self.translate,\
                                                   bg="white", highlightthickness=3, highlightbackground="gray", font=("Helvetica", 10))
        self.tabSeesawComp.translate_button.pack(side=tk.TOP, pady=(10,10))
        
        # Create code label 
        label_code = tk.Label(self.tabSeesawComp, text="Seesaw Compiler Code:")
        label_code.pack(side=tk.TOP)

        # Create a Frame for text widget
        self.tabSeesawComp.frame = tk.Frame(self.tabSeesawComp)
        self.tabSeesawComp.frame.pack(side=tk.TOP)
       
        # Create a Scrollbar for text widget
        yscrollbar = tk.Scrollbar(self.tabSeesawComp.frame, orient=tk.VERTICAL)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Text widget and pack it into the Buckets tab
        self.tabSeesawComp.frame.text_widget = tk.Text(self.tabSeesawComp.frame, height=30, width=110, wrap="none")
        self.tabSeesawComp.frame.text_widget.pack(side=tk.TOP)
        
        # Link the scrollbar to the text widget        
        yscrollbar.config(command=self.tabSeesawComp.frame.text_widget.xview)
        self.tabSeesawComp.frame.text_widget.config(yscrollcommand=yscrollbar.set)
        
    def translate(self):
        self.tabSeesawComp.frame.text_widget.delete('1.0', 'end')
        
        code = self.tabNetlist.text_widget.get("1.0", "end-8l")
        if len(code) < 1 or "simulate_netlist()" not in code:
            self.tabSeesawComp.frame.text_widget.insert(tk.END, "Cannot translate empty\\bad netlist")
            return
        
        code = code.replace("from Gates import *", "from ToSeesawComp import *")
        code = code.replace("from DualRailGates import *", "from ToSeesawComp import *")
        
        new_sim_str = "\tnetlist = get_seesaw_compiler_netlist( s )\n"
        new_sim_str += "\tfor l in netlist:\n\t\tprint(l)"
        code = code.replace("\ts.simulate()", new_sim_str)
        code += "\nsimulate_netlist()\n"
        
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            exec(code)
            output = buf.getvalue()
        
        self.tabSeesawComp.frame.text_widget.insert(tk.END,output)  
            
        if len(self.tabSeesawComp.frame.text_widget.get("1.0", "end-1c")) < 2:
            self.tabSeesawComp.frame.text_widget.insert(tk.END, "No gates in the netlist")
        
  
#######################################################
###                 Instantiation                   ###
#######################################################

def main() -> int:
    app = Application()
    app.mainloop()
    return 0

if __name__ == '__main__':
    sys.exit(main())


