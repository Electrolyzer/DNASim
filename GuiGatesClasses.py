import os

import tkinter as tk
from PIL import ImageTk, Image

#######################################################
###         GUI Gates Defined In This File          ###
###                                                 ###
### Naming Format:                                  ###
###     Standard Gates end with "SB"                ###
###     Dual Rail Gates end with "DB"               ###
#######################################################

def get_gates_map():
    return {
            "And2SB": And2SB,
            "And2DB": And2DB,
            "Or2SB": Or2SB,
            "Or2DB": Or2DB,
            "Nand2DB": Nand2DB,
            "Amp2SeesawSB": Amp2SeesawSB,
            "Amp3SeesawSB": Amp3SeesawSB,
            "Integ2SeesawSB": Integ2SeesawSB,
            "Integ3SeesawSB": Integ3SeesawSB,
            "ThSeesawSB": ThSeesawSB,
            "Mult2SeesawSB": Mult2SeesawSB,
            "Mult2SeesawDB": Mult2SeesawDB,
            "Mult3SeesawSB": Mult3SeesawSB,
            "Mult3SeesawDB": Mult3SeesawDB,
            "Threshold2DB": Threshold2DB,
            "Threshold3DB": Threshold3DB,
            "Threshold4DB": Threshold4DB,
            "NotSB": NotSB
           }


#######################################################
###            Dialog Box For User Input            ###
#######################################################
class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title="", prompts=[], defaults=[]):
        super().__init__(parent)
        self.title(title)
        self.minsize(200, 0)
        self.entries = []

        if not defaults:
            defaults = prompts

        # Set up the prompts
        for prompt, dflt in zip(prompts, defaults):
            tk.Label(self, text=prompt).pack()
            self.entries.append(tk.Entry(self))
            self.entries[-1].insert(tk.END, dflt)
            self.entries[-1].pack()        

        # Set up the OK and Cancel buttons
        button_frame = tk.Frame(self)
        button_frame.pack()
        ok_button = tk.Button(button_frame, text="OK", command=self.ok)
        ok_button.pack(side=tk.LEFT)
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side=tk.LEFT)

        self.result = None

    def ok(self):
        # Store the entries as a tuple in the result attribute
        self.result = []
        for entry in self.entries:
            self.result.append(entry.get())
        self.destroy()

    def cancel(self):
        self.destroy()


#######################################################
###      General Gate Classes For Gates Panel       ###
#######################################################

class GateLabel(tk.Label):
    def __init__(self, master, impath, **kwargs):
        # Load and resize the image
        img = Image.open(impath)
        width, height = img.size
        img = img.resize((width//4,height//4))
        self.image = ImageTk.PhotoImage(img)
        
        # init image widget label
        super().__init__(master, image=self.image)
        
    def get_name_string(self):
        return self.name_label["text"]
        
    def add_interface_buckets(self):
        if hasattr(self, 'interface_buckets'):
            return self.interface_buckets
        else:
            popup_window = tk.Toplevel()
            popup_window.title("Not Defined")
            popup_window.geometry("300x50")
            label = tk.Label(popup_window, text="interface_buckets list not defined for this gate type")
            label.pack(pady=10)
        

class GateTwoInOneOut(GateLabel):
    def __init__(self, master, impath, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "out"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in1_text, in2_text, out_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super().__init__(master, impath=impath, kwargs=kwargs)
        self.make_labels(master, name_text, in1_text, in2_text, out_text)
    
    def make_labels(self, master, name_text, in1_text, in2_text, out_text):
        # Create the text labels
        self.name_label = tk.Label(master, text=name_text)
        self.in1_label = tk.Label(master, text=in1_text)
        self.in2_label = tk.Label(master, text=in2_text)
        self.out_label = tk.Label(master, text=out_text)  
        self.interface_buckets = [(self.in1_label["text"], "ON"), (self.in2_label["text"], "ON"), (self.out_label["text"], "EMPTY")]
        
    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw") 
        
        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((70, 5), window=self.name_label, anchor="nw") 
        self.in1_id = self.master.create_window((5, 35), window=self.in1_label, anchor="nw") 
        self.in2_id = self.master.create_window((5, 70), window=self.in2_label, anchor="nw") 
        self.out_id = self.master.create_window((160, 52), window=self.out_label, anchor="nw") 
        
    def on_drag_motion(self, delta_x, delta_y):
        self.master.move(self.id, delta_x, delta_y)
        self.master.move(self.name_id, delta_x, delta_y)
        self.master.move(self.in1_id, delta_x, delta_y)
        self.master.move(self.in2_id, delta_x, delta_y)
        self.master.move(self.out_id, delta_x, delta_y)
        
    def destroy_all_labels(self):
        self.name_label.destroy()
        self.in1_label.destroy()
        self.in2_label.destroy()
        self.out_label.destroy()    
        
    def get_ports_string(self):
        return "input1="+self.in1_label["text"]+", input2="+self.in2_label["text"]+", output="+self.out_label["text"]


class GateOneInOneOut(GateLabel):
    def __init__(self, master, impath, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "inp", "out", "delay"],
                                                            defaults=["name", "inp", "out", "1"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in_text, out_text, delay] = dialog.result
        else:
            return

            # init image widget label
        super().__init__(master, impath=impath, kwargs=kwargs)
        self.make_labels(master, name_text, in_text, out_text, delay)

    def make_labels(self, master, name_text, in_text, out_text, delay):
        # Create the text labels
        self.name_label = tk.Label(master, text=name_text)
        self.in_label = tk.Label(master, text=in_text)
        self.out_label = tk.Label(master, text=out_text)
        self.delay_label = tk.Label(master, text=str(delay))
        self.interface_buckets = [(self.in_label["text"], "ON"), (self.out_label["text"], "EMPTY")]

    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw")

        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((70, 5), window=self.name_label, anchor="nw")
        self.in_id = self.master.create_window((5, 35), window=self.in_label, anchor="nw")
        self.out_id = self.master.create_window((150, 35), window=self.out_label, anchor="nw")
        self.delay_id = self.master.create_window((70, 45), window=self.delay_label, anchor="nw")

    def on_drag_motion(self, delta_x, delta_y):
        self.master.move(self.id, delta_x, delta_y)
        self.master.move(self.name_id, delta_x, delta_y)
        self.master.move(self.in_id, delta_x, delta_y)
        self.master.move(self.out_id, delta_x, delta_y)
        self.master.move(self.delay_id, delta_x, delta_y)


    def destroy_all_labels(self):
        self.name_label.destroy()
        self.in_label.destroy()
        self.out_label.destroy()
        self.delay_label.destroy()

    def get_ports_string(self):
        return "inp=" + self.in_label["text"] + ", output=" + self.out_label["text"] + ", delay=" + str(self.delay_label["text"])


#######################################################
###                 SB Basic Gates                  ###
#######################################################

class And2SB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","And2.JPG"), kwargs=kwargs)
        
    def get_type_string(self):
        return "And2Gate"

class NotSB(GateOneInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Not.PNG"), kwargs=kwargs)

    def get_type_string(self):
        return "NotGate"

#######################################################
###                 DB Basic Gates                  ###
#######################################################

class And2DB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","And2.JPG"), kwargs=kwargs)
        
    def get_type_string(self):
        return "And2DRGate"
 
class Or2SB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Or2.JPG"), kwargs=kwargs)
        
    def get_type_string(self):
        return "Or2Gate"
        
class Or2DB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Or2.JPG"), kwargs=kwargs)
     
    def get_type_string(self):
        return "Or2DRGate"
        
class Nand2DB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Nand2.JPG"), kwargs=kwargs)
        
    def get_type_string(self):
        return "Nand2DRGate"


#######################################################
###               DB Threshold Gates                ###
#######################################################
        
class Threshold2DB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "w1", "w2", "out", "th"],\
                                                            defaults=["Th1", "in1", "in2", "1", "1", "out", "1.7"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in1_text, in2_text, w1_text, w2_text, out_text, th_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super(GateTwoInOneOut, self).__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","And2.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in1_text, in2_text, w1_text, w2_text, out_text, th_text)
                 
    def make_labels(self, master, name_text, in1_text, in2_text, w1_text, w2_text, out_text, th_text):
        # Create the text labels
        super().make_labels(master, name_text, in1_text, in2_text, out_text)
        self.w1_label = tk.Label(master, text=w1_text)
        self.w2_label = tk.Label(master, text=w2_text)
        self.th_label = tk.Label(master, text=th_text)   
    
    def add_to_panel(self):
        super().add_to_panel()
        self.w1_id = self.master.create_window((65, 35), window=self.w1_label, anchor="nw") 
        self.w2_id = self.master.create_window((65, 70), window=self.w2_label, anchor="nw") 
        self.th_id = self.master.create_window((100, 52), window=self.th_label, anchor="nw")    
    
    def on_drag_motion(self, delta_x, delta_y):
        super().on_drag_motion(delta_x, delta_y)
        self.master.move(self.w1_id, delta_x, delta_y)
        self.master.move(self.w2_id, delta_x, delta_y)
        self.master.move(self.th_id, delta_x, delta_y)
        
    def destroy_all_labels(self):
        super().destroy_all_labels()
        self.w1_label.destroy()
        self.w2_label.destroy()
        self.th_label.destroy()
        
    def get_ports_string(self):
        return "inputs_list=["+self.in1_label["text"]+","+self.in2_label["text"]+"], weight_list=["+\
               self.w1_label["text"]+","+self.w2_label["text"]+"], output="+self.out_label["text"]+\
               ", threshold="+self.th_label["text"]
        
    def get_type_string(self):
        return "ThresholdDRGate1Out"

class Threshold3DB(Threshold2DB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "in3", "w1", "w2", "w3", "out", "th"],\
                                                            defaults=["Th1", "in1", "in2", "in3", "1", "1", "1", "out", "2.7"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in1_text, in2_text, in3_text, w1_text, w2_text, w3_text, out_text, th_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super(GateTwoInOneOut, self).__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Threshold3.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in1_text, in2_text, in3_text, w1_text, w2_text, w3_text, out_text, th_text)
        
    def make_labels(self, master, name_text, in1_text, in2_text, in3_text, w1_text, w2_text, w3_text, out_text, th_text):
        # Create the text labels
        super().make_labels(master, name_text, in1_text, in2_text, w1_text, w2_text, out_text, th_text)
        self.in3_label = tk.Label(master, text=in3_text)
        self.w3_label = tk.Label(master, text=w3_text)  
        self.interface_buckets.append((self.in3_label["text"], "ON"))
        
    def add_to_panel(self):
        super().add_to_panel()
        self.master.move(self.out_id, 0, 15)
        self.master.move(self.th_id, 0, 15)
        self.in3_id = self.master.create_window((5, 105), window=self.in3_label, anchor="nw") 
        self.w3_id = self.master.create_window((65, 105), window=self.w3_label, anchor="nw") 
        
    def on_drag_motion(self, delta_x, delta_y):
        super().on_drag_motion(delta_x, delta_y)
        self.master.move(self.in3_id, delta_x, delta_y)
        self.master.move(self.w3_id, delta_x, delta_y)
        
    def destroy_all_labels(self):
        super().destroy_all_labels()
        self.in3_label.destroy()
        self.w3_label.destroy()
        
    def get_ports_string(self):
        return "inputs_list=["+self.in1_label["text"]+","+self.in2_label["text"]+","+self.in3_label["text"]+"], weight_list=["+\
               self.w1_label["text"]+","+self.w2_label["text"]+","+self.w3_label["text"]+"], output="+self.out_label["text"]+\
               ", threshold="+self.th_label["text"]
 
class Threshold4DB(Threshold3DB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "in3", "in4", "w1", "w2", "w3", "w4", "out", "th"],\
                                                            defaults=["Th1", "in1", "in2", "in3", "in4", "1", "1", "1", "1", "out", "2.7"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in1_text, in2_text, in3_text, in4_text, w1_text, w2_text, w3_text, w4_text, out_text, th_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super(GateTwoInOneOut, self).__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Threshold4.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in1_text, in2_text, in3_text, in4_text, w1_text, w2_text, w3_text, w4_text, out_text, th_text)
        
    def make_labels(self, master, name_text, in1_text, in2_text, in3_text, in4_text, w1_text, w2_text, w3_text, w4_text, out_text, th_text):
        # Create the text labels
        super().make_labels(master, name_text, in1_text, in2_text, in3_text, w1_text, w2_text, w3_text, out_text, th_text)
        self.in4_label = tk.Label(master, text=in4_text)
        self.w4_label = tk.Label(master, text=w4_text)  
        
    def add_to_panel(self):
        super().add_to_panel()
        self.master.move(self.out_id, 0, 17)
        self.master.move(self.th_id, 0, 17)
        self.in4_id = self.master.create_window((5, 140), window=self.in4_label, anchor="nw") 
        self.w4_id = self.master.create_window((65, 140), window=self.w4_label, anchor="nw") 
 
    def on_drag_motion(self, delta_x, delta_y):
        super().on_drag_motion(delta_x, delta_y)
        self.master.move(self.in4_id, delta_x, delta_y)
        self.master.move(self.w4_id, delta_x, delta_y)
        self.interface_buckets.append((self.in4_label["text"], "ON"))
        
    def destroy_all_labels(self):
        super().destroy_all_labels()
        self.in4_label.destroy()
        self.w4_label.destroy()
        
    def get_ports_string(self):
        return "inputs_list=["+self.in1_label["text"]+","+self.in2_label["text"]+","+self.in3_label["text"]+","+self.in4_label["text"]+"], weight_list=["+\
               self.w1_label["text"]+","+self.w2_label["text"]+","+self.w3_label["text"]+","+self.w4_label["text"]+"], output="+self.out_label["text"]+\
               ", threshold="+self.th_label["text"]
   

#######################################################
###           DB Multiplying Seesaw Gates           ###
#######################################################
   
class Mult2SeesawDB(GateLabel):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["Name", "input", "out1", "out2", "w1", "w2"],\
                                                            defaults=["Mult2", "in1", "out1", "out2", "1", "1"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in_text, out1_text, out2_text, w1_text, w2_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super().__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Mult2Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in_text, out1_text, out2_text, w1_text, w2_text)

    def make_labels(self, master, name_text, in_text, out1_text, out2_text, w1_text, w2_text):
        # Create the text labels
        self.name_label = tk.Label(master, text=name_text)
        self.in_label = tk.Label(master, text=in_text)
        self.out1_label = tk.Label(master, text=out1_text)
        self.out2_label = tk.Label(master, text=out2_text)   
        self.w1_label = tk.Label(master, text=w1_text)
        self.w2_label = tk.Label(master, text=w2_text)
        self.all_labels = [self.name_label, self.in_label, self.out1_label, self.out2_label, self.w1_label, self.w2_label]
        self.interface_buckets = [(self.in_label["text"], "ON"), (self.out1_label["text"], "EMPTY"), (self.out2_label["text"], "EMPTY")]
        
    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw") 
        
        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((70, 5), window=self.name_label, anchor="nw") 
        self.in_id = self.master.create_window((5, 57), window=self.in_label, anchor="nw") 
        self.out1_id = self.master.create_window((165, 18), window=self.out1_label, anchor="nw") 
        self.out2_id = self.master.create_window((165, 95), window=self.out2_label, anchor="nw") 
        self.w1_id = self.master.create_window((120, 42), window=self.w1_label, anchor="nw") 
        self.w2_id = self.master.create_window((120, 70), window=self.w2_label, anchor="nw") 
        self.all_ids = [self.id, self.name_id, self.in_id, self.out1_id, self.out2_id, self.w1_id, self.w2_id]
        
    def on_drag_motion(self, delta_x, delta_y):
        for lid in self.all_ids:
            self.master.move(lid, delta_x, delta_y)
        
    def destroy_all_labels(self):
        for label in self.all_labels:
            label.destroy()
        
    def get_type_string(self):
        return "MultiplyingDRSeesaw"
        
    def get_ports_string(self):
        return "inp="+self.in_label["text"]+", outputs_list=["+self.out1_label["text"]+","+\
               self.out2_label["text"]+"], weight_list=["+self.w1_label["text"]+","+self.w2_label["text"]+"]"
               
class Mult3SeesawDB(Mult2SeesawDB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["Name", "input", "out1", "out2", "out3", "w1", "w2", "w3"],\
                                                            defaults=["Mult3", "in1", "out1", "out2", "out3", "1", "1", "1"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in_text, out1_text, out2_text, out3_text, w1_text, w2_text, w3_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super(Mult2SeesawDB, self).__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Mult3Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in_text, out1_text, out2_text, out3_text, w1_text, w2_text, w3_text)

    def make_labels(self, master, name_text, in_text, out1_text, out2_text, out3_text, w1_text, w2_text, w3_text):
        # Create the text labels
        super().make_labels(master, name_text, in_text, out1_text, out2_text, w1_text, w2_text)
        self.out3_label = tk.Label(master, text=out3_text)   
        self.w3_label = tk.Label(master, text=w3_text)
        self.all_labels.extend([self.out3_label,self.w3_label])
        self.interface_buckets.append((self.out3_label["text"], "EMPTY"))
                
    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw") 
        
        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((110, 5), window=self.name_label, anchor="nw") 
        self.in_id = self.master.create_window((5, 70), window=self.in_label, anchor="nw") 
        self.out1_id = self.master.create_window((200, 18), window=self.out1_label, anchor="nw") 
        self.out2_id = self.master.create_window((200, 70), window=self.out2_label, anchor="nw") 
        self.out3_id = self.master.create_window((200, 125), window=self.out3_label, anchor="nw") 
        self.w1_id = self.master.create_window((140, 45), window=self.w1_label, anchor="nw") 
        self.w2_id = self.master.create_window((152, 70), window=self.w2_label, anchor="nw") 
        self.w3_id = self.master.create_window((140, 100), window=self.w3_label, anchor="nw") 
        self.all_ids = [self.id, self.name_id, self.in_id, self.out1_id, self.out2_id, self.out3_id, self.w1_id, self.w2_id, self.w3_id]
               
    def get_type_string(self):
        return "MultiplyingDRSeesaw"
        
    def get_ports_string(self):
        return "inp="+self.in_label["text"]+", outputs_list=["+self.out1_label["text"]+","+self.out2_label["text"]+","+\
               self.out3_label["text"]+"], weight_list=["+self.w1_label["text"]+","+self.w2_label["text"]+","+self.w3_label["text"]+"]"
        
        
#######################################################
###           SB Multiplying Seesaw Gates           ###
#######################################################      

class Mult2SeesawSB(Mult2SeesawDB):
    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs=kwargs)
        
    def get_type_string(self):
        return "MultiplyingSeesaw"
        
class Mult3SeesawSB(Mult3SeesawDB):
    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs=kwargs)
        
    def get_type_string(self):
        return "MultiplyingSeesaw"


#######################################################
###           SB Amplifying Seesaw Gates            ###
#######################################################

class Amp2SeesawSB(Mult2SeesawDB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["Name", "input", "threshold", "out1", "out2", "w1", "w2"],\
                                                            defaults=["Amp2", "in1", "0.5", "out1", "out2", "1", "1"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in_text, th_text, out1_text, out2_text, w1_text, w2_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super(Mult2SeesawDB, self).__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Mult2Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in_text, th_text, out1_text, out2_text, w1_text, w2_text)
        
    def make_labels(self, master, name_text, in_text, th_text, out1_text, out2_text, w1_text, w2_text):
        # Create the text labels
        super().make_labels(master, name_text, in_text, out1_text, out2_text, w1_text, w2_text)
        self.th_label = tk.Label(master, text=th_text)
        self.all_labels.append(self.th_label)

    def add_to_panel(self):
        super().add_to_panel()
        self.th_id = self.master.create_window((75, 57), window=self.th_label, anchor="nw") 
        self.all_ids.append(self.th_id)

    def get_type_string(self):
        return "AmplifyingSeesaw"
        
    def get_ports_string(self):
        return "inp="+self.in_label["text"]+", outputs_list=["+self.out1_label["text"]+","+self.out2_label["text"]+\
               "], weight_list=["+self.w1_label["text"]+","+self.w2_label["text"]+"], threshold_amount="+self.th_label["text"]
               
class Amp3SeesawSB(Mult3SeesawDB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["Name", "input", "threshold", "out1", "out2", "out3", "w1", "w2", "w3"],\
                                                            defaults=["Amp3", "in1", "0.5", "out1", "out2", "out3", "1", "1", "1"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in_text, th_text, out1_text, out2_text, out3_text, w1_text, w2_text, w3_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super(Mult2SeesawDB, self).__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Mult3Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in_text, th_text, out1_text, out2_text, out3_text, w1_text, w2_text, w3_text)
        
    def make_labels(self, master, name_text, in_text, th_text, out1_text, out2_text, out3_text, w1_text, w2_text, w3_text):
        # Create the text labels
        super().make_labels(master, name_text, in_text, out1_text, out2_text, out3_text, w1_text, w2_text, w3_text)
        self.th_label = tk.Label(master, text=th_text)
        self.all_labels.append(self.th_label)

    def add_to_panel(self):
        super().add_to_panel()
        self.th_id = self.master.create_window((85, 70), window=self.th_label, anchor="nw") 
        self.all_ids.append(self.th_id)

    def get_type_string(self):
        return "AmplifyingSeesaw"
        
    def get_ports_string(self):
        return "inp="+self.in_label["text"]+", outputs_list=["+self.out1_label["text"]+","+self.out2_label["text"]+","+self.out3_label["text"]+\
               "], weight_list=["+self.w1_label["text"]+","+self.w2_label["text"]+","+self.w3_label["text"]+"], threshold_amount="+self.th_label["text"]
        
        
#######################################################
###           SB Integrating Seesaw Gates           ###
#######################################################

class Integ2SeesawSB(GateLabel):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["Name", "in1", "in2", "out", "weight"],\
                                                            defaults=["Integ2", "in1", "in2", "out", "1"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in1_text, in2_text, out_text, w_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super().__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Integ2Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in1_text, in2_text, out_text, w_text)

    def make_labels(self, master, name_text, in1_text, in2_text, out_text, w_text):
        # Create the text labels
        self.name_label = tk.Label(master, text=name_text)
        self.in1_label = tk.Label(master, text=in1_text)
        self.in2_label = tk.Label(master, text=in2_text)
        self.out_label = tk.Label(master, text=out_text)   
        self.w_label = tk.Label(master, text=w_text)
        self.all_labels = [self.name_label, self.in1_label, self.in2_label, self.out_label, self.w_label]
        self.interface_buckets = [(self.in1_label["text"], "ON"), (self.in2_label["text"], "ON"), (self.out_label["text"], "EMPTY")]
        
    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw") 
        
        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((75, 5), window=self.name_label, anchor="nw") 
        self.in1_id = self.master.create_window((5, 15), window=self.in1_label, anchor="nw") 
        self.in2_id = self.master.create_window((5, 100), window=self.in2_label, anchor="nw") 
        self.out_id = self.master.create_window((165, 55), window=self.out_label, anchor="nw") 
        self.w_id = self.master.create_window((105, 55), window=self.w_label, anchor="nw")  
        self.all_ids = [self.id, self.name_id, self.in1_id, self.in2_id, self.out_id, self.w_id]
        
    def on_drag_motion(self, delta_x, delta_y):
        for lid in self.all_ids:
            self.master.move(lid, delta_x, delta_y)
        
    def destroy_all_labels(self):
        for label in self.all_labels:
            label.destroy()
        
    def get_type_string(self):
        return "IntegratingSeesaw"
        
    def get_ports_string(self):
        return "inputs_list=["+self.in1_label["text"]+","+self.in2_label["text"]+"], output="+\
               self.out_label["text"]+", weight="+self.w_label["text"]
        
class Integ3SeesawSB(Integ2SeesawSB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["Name", "in1", "in2", "in3", "out", "weight"],\
                                                            defaults=["Integ3", "in1", "in2", "in3", "out", "1"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in1_text, in2_text, in3_text, out_text, w_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super(Integ2SeesawSB, self).__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","Integ3Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in1_text, in2_text, in3_text, out_text, w_text)

    def make_labels(self, master, name_text, in1_text, in2_text, in3_text, out_text, w_text):
        # Create the text labels
        super().make_labels(master, name_text, in1_text, in2_text, out_text, w_text)
        self.in3_label = tk.Label(master, text=in3_text)
        self.all_labels.append(self.in3_label)
        self.interface_buckets.append((self.in3_label["text"], "ON"))
        
    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw") 
        
        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((90, 5), window=self.name_label, anchor="nw") 
        self.in1_id = self.master.create_window((5, 15), window=self.in1_label, anchor="nw") 
        self.in2_id = self.master.create_window((5, 70), window=self.in2_label, anchor="nw") 
        self.in3_id = self.master.create_window((5, 120), window=self.in3_label, anchor="nw") 
        self.out_id = self.master.create_window((190, 70), window=self.out_label, anchor="nw") 
        self.w_id = self.master.create_window((130, 70), window=self.w_label, anchor="nw")  
        self.all_ids = [self.id, self.name_id, self.in1_id, self.in2_id, self.in3_id, self.out_id, self.w_id]
        
    def get_ports_string(self):
        return "inputs_list=["+self.in1_label["text"]+","+self.in2_label["text"]+","+self.in3_label["text"]+"], output="+\
               self.out_label["text"]+", weight="+self.w_label["text"]


#######################################################
###           SB Thresholding Seesaw Gate           ###
#######################################################

class ThSeesawSB(GateLabel):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["Name", "input", "threshold", "out"],\
                                                            defaults=["Th1seesaw", "in1", "0.7", "out"])
        master.wait_window(dialog)
        if dialog.result:
            # The user clicked OK
            [name_text, in_text, th_text, out_text] = dialog.result
        else:
            return 
                   
        # init image widget label
        super().__init__(master, impath=os.path.join("C:\\Users\\user\\Desktop\\DNASim\\graphics","ThSeesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, name_text, in_text, th_text, out_text)

    def make_labels(self, master, name_text, in_text, th_text, out_text):
        # Create the text labels
        self.name_label = tk.Label(master, text=name_text)
        self.in_label = tk.Label(master, text=in_text)
        self.th_label = tk.Label(master, text=th_text)   
        self.out_label = tk.Label(master, text=out_text)
        self.interface_buckets = [(self.in_label["text"], "ON"), (self.out_label["text"], "EMPTY")]
        
    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw") 
        
        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((78, 5), window=self.name_label, anchor="nw") 
        self.in_id = self.master.create_window((5, 55), window=self.in_label, anchor="nw") 
        self.th_id = self.master.create_window((120, 55), window=self.th_label, anchor="nw") 
        self.out_id = self.master.create_window((185, 55), window=self.out_label, anchor="nw") 
                
    def on_drag_motion(self, delta_x, delta_y):
        self.master.move(self.id, delta_x, delta_y)
        self.master.move(self.name_id, delta_x, delta_y)
        self.master.move(self.in_id, delta_x, delta_y)
        self.master.move(self.th_id, delta_x, delta_y)
        self.master.move(self.out_id, delta_x, delta_y)
        
    def destroy_all_labels(self):
        self.name_label.destroy()
        self.in_label.destroy()
        self.th_label.destroy()
        self.out_label.destroy()
        
    def get_type_string(self):
        return "ThresholdingSeesaw"
        
    def get_ports_string(self):
        return "inp="+self.in_label["text"]+", threshold_amount="+self.th_label["text"]+", output="+self.out_label["text"]


