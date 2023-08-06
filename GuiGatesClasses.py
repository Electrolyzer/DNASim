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
            "NotSB": NotSB,
            "DelaySB": DelaySB,
            "ReporterSB": ReporterSB
           }


#######################################################
###            Dialog Box For User Input            ###
#######################################################
class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title="", prompts=[], defaults=[]):
        super().__init__(parent)
        self.title(title)
        self.prompts = prompts
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
        # Store the entries as a dictionary in the result attribute
        self.result = {}
        for prompt, entry in zip (self.prompts, self.entries):
            self.result.update({prompt: entry.get()})
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
        self.labels = []
        self.labelIds =[]
        
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

    def on_drag_motion(self, delta_x, delta_y):
        for labelId in self.labelIds:
            self.master.move(labelId, delta_x, delta_y)

    def destroy_all_labels(self):
        for label in self.labels:
            label.destroy()

class GateTwoInOneOut(GateLabel):
    def __init__(self, master, impath, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "out"])
        master.wait_window(dialog)
        if not dialog.result:
            # If there is no result (user closed window) then cancel operation
            return 
                   
        # init image widget label
        super().__init__(master, impath=impath, kwargs=kwargs)
        self.make_labels(master, **dialog.result)
    
    def make_labels(self, master, name, in1, in2, out, **kwargs):
        # Create the text labels
        self.name_label = tk.Label(master, text=name)
        self.in1_label = tk.Label(master, text=in1)
        self.in2_label = tk.Label(master, text=in2)
        self.out_label = tk.Label(master, text=out)
        self.interface_buckets = [(self.in1_label["text"], "ON"), (self.in2_label["text"], "ON"), (self.out_label["text"], "EMPTY")]
        self.labels += [self.name_label, self.in1_label, self.in2_label, self.out_label]
        
    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw") 
        
        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((70, 5), window=self.name_label, anchor="nw") 
        self.in1_id = self.master.create_window((5, 35), window=self.in1_label, anchor="nw") 
        self.in2_id = self.master.create_window((5, 70), window=self.in2_label, anchor="nw") 
        self.out_id = self.master.create_window((160, 52), window=self.out_label, anchor="nw")
        self.labelIds += [self.id, self.name_id, self.in1_id, self.in2_id, self.out_id]

    def get_ports_string(self):
        return "input1="+self.in1_label["text"]+", input2="+self.in2_label["text"]+", output="+self.out_label["text"]


class GateOneInOneOut(GateLabel):
    def __init__(self, master, impath, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "input", "out", "delay"],
                                                            defaults=["name", "input", "out", "1"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super().__init__(master, impath=impath, kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, input, out, delay, **kwargs):
        # Create the text labels
        self.name_label = tk.Label(master, text=name)
        self.in_label = tk.Label(master, text=input)
        self.out_label = tk.Label(master, text=out)
        self.delay_label = tk.Label(master, text=str(delay))
        self.interface_buckets = [(self.in_label["text"], "OFF"), (self.out_label["text"], "EMPTY")]
        self.labels += [self.name_label, self.in_label, self.out_label, self.delay_label]

    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw")

        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((70, 5), window=self.name_label, anchor="nw")
        self.in_id = self.master.create_window((-5, 35), window=self.in_label, anchor="nw")
        self.out_id = self.master.create_window((150, 35), window=self.out_label, anchor="nw")
        self.delay_id = self.master.create_window((70, 45), window=self.delay_label, anchor="nw")

        self.labelIds += [self.id, self.name_id, self.in_id, self.out_id, self.delay_id]

    def get_ports_string(self):
        return "inp=" + self.in_label["text"] + ", output=" + self.out_label["text"] + ", delay=" + str(self.delay_label["text"])


#######################################################
###                 SB Basic Gates                  ###
#######################################################

class And2SB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//And2.JPG"), kwargs=kwargs)
        
    def get_type_string(self):
        return "And2Gate"

class NotSB(GateOneInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Not.PNG"), kwargs=kwargs)

    def get_type_string(self):
        return "NotGate"

class DelaySB(GateLabel):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "out", "delay"],
                                                            defaults=["name", "out", "1"])
        master.wait_window(dialog)
        if not dialog.result:
            return

            # init image widget label
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Delay.PNG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, out, delay):
        # Create the text labels
        self.name_label = tk.Label(master, text=name)
        self.out_label = tk.Label(master, text=out)
        self.delay_label = tk.Label(master, text=str(delay))
        self.interface_buckets = [(self.out_label["text"], "EMPTY")]

        self.labels += [self.name_label, self.out_label, self.delay_label]

    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw")

        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((55, 5), window=self.name_label, anchor="nw")
        self.out_id = self.master.create_window((120, 35), window=self.out_label, anchor="nw")
        self.delay_id = self.master.create_window((40, 45), window=self.delay_label, anchor="nw")

        self.labelIds += [self.id, self.name_id, self.out_id, self.delay_id]

    def get_ports_string(self):
        return "output=" + self.out_label["text"] + ", delay=" + str(self.delay_label["text"])

    def get_type_string(self):
        return "DelayGate"

class ReporterSB(GateLabel):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "input", "fluor"])
        master.wait_window(dialog)
        if not dialog.result:
            return

            # init image widget label
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Reporter.jpg"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, input, fluor):
        # Create the text labels
        self.name_label = tk.Label(master, text=name)
        self.in_label = tk.Label(master, text=input)
        self.fluor_label = tk.Label(master, text=fluor)
        self.interface_buckets = [(self.in_label["text"], "ON"), (self.fluor_label["text"], "EMPTY")]

        self.labels += [self.name_label, self.in_label, self.fluor_label]

    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw")

        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((65, 5), window=self.name_label, anchor="nw")
        self.in_id = self.master.create_window((5, 35), window=self.in_label, anchor="nw")
        self.fluor_id = self.master.create_window((135, 35), window=self.fluor_label, anchor="nw")

        self.labelIds += [self.id, self.name_id, self.in_id, self.fluor_id]

    def get_ports_string(self):
        return "inp=" + self.in_label["text"] + ", fluor=" + self.fluor_label["text"]
    def get_type_string(self):
        return "ReporterSeesaw"

#######################################################
###                 DB Basic Gates                  ###
#######################################################

class And2DB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//And2.JPG"), kwargs=kwargs)

    def get_type_string(self):
        return "And2DRGate"

class Or2SB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Or2.JPG"), kwargs=kwargs)

    def get_type_string(self):
        return "Or2Gate"

class Or2DB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Or2.JPG"), kwargs=kwargs)

    def get_type_string(self):
        return "Or2DRGate"

class Nand2DB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Nand2.JPG"), kwargs=kwargs)

    def get_type_string(self):
        return "Nand2DRGate"


#######################################################
###               DB Threshold Gates                ###
#######################################################

class Threshold2DB(GateTwoInOneOut):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "w1", "w2", "out", "threshold"],\
                                                            defaults=["Th1", "in1", "in2", "1", "1", "out", "1.7"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super(GateTwoInOneOut, self).__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//And2.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, in1, in2, w1, w2, out, threshold):
        # Create the text labels
        super().make_labels(master, name, in1, in2, out)
        self.w1_label = tk.Label(master, text=w1)
        self.w2_label = tk.Label(master, text=w2)
        self.th_label = tk.Label(master, text=threshold)

        self.labels += [self.w1_label, self.w2_label, self.th_label]

    def add_to_panel(self):
        super().add_to_panel()
        self.w1_id = self.master.create_window((65, 35), window=self.w1_label, anchor="nw")
        self.w2_id = self.master.create_window((65, 70), window=self.w2_label, anchor="nw")
        self.th_id = self.master.create_window((100, 52), window=self.th_label, anchor="nw")

        self.labelIds += [self.w1_id, self.w2_id, self.th_id]

    def get_ports_string(self):
        return "inputs_list=["+self.in1_label["text"]+","+self.in2_label["text"]+"], weight_list=["+\
               self.w1_label["text"]+","+self.w2_label["text"]+"], output="+self.out_label["text"]+\
               ", threshold="+self.th_label["text"]

    def get_type_string(self):
        return "ThresholdDRGate1Out"

class Threshold3DB(Threshold2DB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "in3", "w1", "w2", "w3", "out", "threshold"],\
                                                            defaults=["Th1", "in1", "in2", "in3", "1", "1", "1", "out", "2.7"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super(GateTwoInOneOut, self).__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Threshold3.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, in1, in2, in3, w1, w2, w3, out, threshold):
        # Create the text labels
        super().make_labels(master, name, in1, in2, w1, w2, out, threshold)
        self.in3_label = tk.Label(master, text=in3)
        self.w3_label = tk.Label(master, text=w3)
        self.interface_buckets.append((self.in3_label["text"], "ON"))

        self.labels += [self.in3_label, self.w3_label]

    def add_to_panel(self):
        super().add_to_panel()
        self.master.move(self.out_id, 0, 15)
        self.master.move(self.th_id, 0, 15)
        self.in3_id = self.master.create_window((5, 105), window=self.in3_label, anchor="nw")
        self.w3_id = self.master.create_window((65, 105), window=self.w3_label, anchor="nw")

        self.labelIds += [self.in3_id, self.w3_id]

    def get_ports_string(self):
        return "inputs_list=["+self.in1_label["text"]+","+self.in2_label["text"]+","+self.in3_label["text"]+"], weight_list=["+\
               self.w1_label["text"]+","+self.w2_label["text"]+","+self.w3_label["text"]+"], output="+self.out_label["text"]+\
               ", threshold="+self.th_label["text"]

class Threshold4DB(Threshold3DB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "in3", "in4", "w1", "w2", "w3", "w4", "out", "threshold"],\
                                                            defaults=["Th1", "in1", "in2", "in3", "in4", "1", "1", "1", "1", "out", "2.7"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super(GateTwoInOneOut, self).__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Threshold4.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, in1, in2, in3, in4, w1, w2, w3, w4, out, threshold):
        # Create the text labels
        super().make_labels(master, name, in1, in2, in3, w1, w2, w3, out, threshold)
        self.in4_label = tk.Label(master, text=in4)
        self.w4_label = tk.Label(master, text=w4)

        self.labels += [self.in4_label, self.w4_label]

    def add_to_panel(self):
        super().add_to_panel()
        self.master.move(self.out_id, 0, 17)
        self.master.move(self.th_id, 0, 17)
        self.in4_id = self.master.create_window((5, 140), window=self.in4_label, anchor="nw")
        self.w4_id = self.master.create_window((65, 140), window=self.w4_label, anchor="nw")

        self.labelIds += [self.in4_id, self.w4_id]

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
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "input", "out1", "out2", "w1", "w2"],\
                                                            defaults=["Mult2", "in1", "out1", "out2", "1", "1"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Mult2Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, input, out1, out2, w1, w2):
        # Create the text labels
        self.name_label = tk.Label(master, text=name)
        self.in_label = tk.Label(master, text=input)
        self.out1_label = tk.Label(master, text=out1)
        self.out2_label = tk.Label(master, text=out2)
        self.w1_label = tk.Label(master, text=w1)
        self.w2_label = tk.Label(master, text=w2)
        self.interface_buckets = [(self.in_label["text"], "ON"), (self.out1_label["text"], "EMPTY"), (self.out2_label["text"], "EMPTY")]

        self.labels = [self.name_label, self.in_label, self.out1_label, self.out2_label, self.w1_label, self.w2_label]

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

        self.labelIds = [self.id, self.name_id, self.in_id, self.out1_id, self.out2_id, self.w1_id, self.w2_id]
    def get_type_string(self):
        return "MultiplyingDRSeesaw"

    def get_ports_string(self):
        return "inp="+self.in_label["text"]+", outputs_list=["+self.out1_label["text"]+","+\
               self.out2_label["text"]+"], weight_list=["+self.w1_label["text"]+","+self.w2_label["text"]+"]"

class Mult3SeesawDB(Mult2SeesawDB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "input", "out1", "out2", "out3", "w1", "w2", "w3"],\
                                                            defaults=["Mult3", "in1", "out1", "out2", "out3", "1", "1", "1"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super(Mult2SeesawDB, self).__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Mult3Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, input, out1, out2, out3, w1, w2, w3, **kwargs):
        # Create the text labels
        super().make_labels(master, name, input, out1, out2, w1, w2)
        self.out3_label = tk.Label(master, text=out3)
        self.w3_label = tk.Label(master, text=w3)
        self.interface_buckets.append((self.out3_label["text"], "EMPTY"))

        self.labels += [self.out3_label,self.w3_label]

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

        self.labelIds = [self.id, self.name_id, self.in_id, self.out1_id, self.out2_id, self.out3_id, self.w1_id, self.w2_id, self.w3_id]

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
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "input", "threshold", "out1", "out2", "w1", "w2"],\
                                                            defaults=["Amp2", "in1", "0.5", "out1", "out2", "1", "1"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super(Mult2SeesawDB, self).__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Mult2Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, input, threshold, out1, out2, w1, w2):
        # Create the text labels
        super().make_labels(master, name, input, out1, out2, w1, w2)
        self.th_label = tk.Label(master, text=threshold)

        self.labels += [self.th_label]

    def add_to_panel(self):
        super().add_to_panel()
        self.th_id = self.master.create_window((75, 57), window=self.th_label, anchor="nw")
        self.labelIds += [self.th_id]

    def get_type_string(self):
        return "AmplifyingSeesaw"

    def get_ports_string(self):
        return "inp="+self.in_label["text"]+", outputs_list=["+self.out1_label["text"]+","+self.out2_label["text"]+\
               "], weight_list=["+self.w1_label["text"]+","+self.w2_label["text"]+"], threshold_amount="+self.th_label["text"]

class Amp3SeesawSB(Mult3SeesawDB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "input", "threshold", "out1", "out2", "out3", "w1", "w2", "w3"],\
                                                            defaults=["Amp3", "in1", "0.5", "out1", "out2", "out3", "1", "1", "1"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super(Mult2SeesawDB, self).__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Mult3Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, input, threshold, out1, out2, out3, w1, w2, w3):
        # Create the text labels
        super().make_labels(master, name, input, out1, out2, out3, w1, w2, w3)
        self.th_label = tk.Label(master, text=threshold)

        self.labels == [self.th_label]

    def add_to_panel(self):
        super().add_to_panel()
        self.th_id = self.master.create_window((85, 70), window=self.th_label, anchor="nw")

        self.labelIds += [self.th_id]

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
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "out", "weight"],\
                                                            defaults=["Integ2", "in1", "in2", "out", "1"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Integ2Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, in1, in2, out, weight):
        # Create the text labels
        self.name_label = tk.Label(master, text=name)
        self.in1_label = tk.Label(master, text=in1)
        self.in2_label = tk.Label(master, text=in2)
        self.out_label = tk.Label(master, text=out)
        self.w_label = tk.Label(master, text=weight)
        self.interface_buckets = [(self.in1_label["text"], "ON"), (self.in2_label["text"], "ON"), (self.out_label["text"], "EMPTY")]

        self.labels += [self.name_label, self.in1_label, self.in2_label, self.out_label, self.w_label]


    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw")

        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((75, 5), window=self.name_label, anchor="nw")
        self.in1_id = self.master.create_window((5, 15), window=self.in1_label, anchor="nw")
        self.in2_id = self.master.create_window((5, 100), window=self.in2_label, anchor="nw")
        self.out_id = self.master.create_window((165, 55), window=self.out_label, anchor="nw")
        self.w_id = self.master.create_window((105, 55), window=self.w_label, anchor="nw")

        self.labelIds += [self.id, self.name_id, self.in1_id, self.in2_id, self.out_id, self.w_id]

    def get_type_string(self):
        return "IntegratingSeesaw"

    def get_ports_string(self):
        return "inputs_list=["+self.in1_label["text"]+","+self.in2_label["text"]+"], output="+\
               self.out_label["text"]+", weight="+self.w_label["text"]

class Integ3SeesawSB(Integ2SeesawSB):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "in1", "in2", "in3", "out", "weight"],\
                                                            defaults=["Integ3", "in1", "in2", "in3", "out", "1"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super(Integ2SeesawSB, self).__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//Integ3Seesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, in1, in2, in3, out, weight):
        # Create the text labels
        super().make_labels(master, name, in1, in2, out, weight)
        self.in3_label = tk.Label(master, text=in3)
        self.interface_buckets.append((self.in3_label["text"], "ON"))

        self.labels += [self.in3_label]

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

        self.labelIds += [self.id, self.name_id, self.in1_id, self.in2_id, self.in3_id, self.out_id, self.w_id]

    def get_ports_string(self):
        return "inputs_list=["+self.in1_label["text"]+","+self.in2_label["text"]+","+self.in3_label["text"]+"], output="+\
               self.out_label["text"]+", weight="+self.w_label["text"]


#######################################################
###           SB Thresholding Seesaw Gate           ###
#######################################################

class ThSeesawSB(GateLabel):
    def __init__(self, master, **kwargs):
        # Get buckets dialog
        dialog = CustomDialog(master, title="Gate Buckets", prompts=["name", "input", "threshold", "out"],\
                                                            defaults=["Th1seesaw", "in1", "0.7", "out"])
        master.wait_window(dialog)
        if not dialog.result:
            return

        # init image widget label
        super().__init__(master, impath=os.path.join(os.path.abspath(__file__),"..//graphics//ThSeesaw.JPG"), kwargs=kwargs)
        self.make_labels(master, **dialog.result)

    def make_labels(self, master, name, input, threshold, out):
        # Create the text labels
        self.name_label = tk.Label(master, text=name)
        self.in_label = tk.Label(master, text=input)
        self.th_label = tk.Label(master, text=threshold)
        self.out_label = tk.Label(master, text=out)
        self.interface_buckets = [(self.in_label["text"], "ON"), (self.out_label["text"], "EMPTY")]

        self.labels += [self.name_label, self.in_label, self.th_label, self.out_label]
        
    def add_to_panel(self):
        # Add the image label widget to the canvas
        self.id = self.master.create_window((30, 25), window=self, anchor="nw") 
        
        # Add the text label widgets to the canvas
        self.name_id = self.master.create_window((78, 5), window=self.name_label, anchor="nw") 
        self.in_id = self.master.create_window((5, 55), window=self.in_label, anchor="nw") 
        self.th_id = self.master.create_window((120, 55), window=self.th_label, anchor="nw") 
        self.out_id = self.master.create_window((185, 55), window=self.out_label, anchor="nw")

        self.labelIds += [self.id, self.name_id, self.in_id, self.th_id, self.out_id]
        
    def get_type_string(self):
        return "ThresholdingSeesaw"
        
    def get_ports_string(self):
        return "inp="+self.in_label["text"]+", threshold_amount="+self.th_label["text"]+", output="+self.out_label["text"]

