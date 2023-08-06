###################################################################
###      If you want to export the netlist to Seesaw Compiler   ###
###      format, this File should be imported instead of        ###
###      "Gates.py" or "DualRailGates.py"                       ###
###################################################################

from DualRailGates import *

###################################################################
###                   Translatable Gates                        ###
###################################################################

class And2Gate(And2Gate):
    def __init__(self, name, input1, input2, output) -> None:
        super().__init__(name, [input1, input2], output)
        self.inputs_lst = [input1, input2]
        self.outputs_lst = [output]
        self.gate_type = "AND"

class Or2Gate(Or2Gate):
    def __init__(self, name, input1, input2, output) -> None:
        super().__init__(name, [input1, input2], output)
        self.inputs_lst = [input1, input2]
        self.outputs_lst = [output]
        self.gate_type = "OR"

class And2DRGate(And2DRGate):
    def __init__(self, name, input1, input2, output) -> None:
        super().__init__(name, [input1, input2], output)
        self.inputs_lst = [input1, input2]
        self.outputs_lst = [output]
        self.gate_type = "AND"
        
class Or2DRGate(Or2DRGate):
    def __init__(self, name, input1, input2, output) -> None:
        super().__init__(name, [input1, input2], output)
        self.inputs_lst = [input1, input2]
        self.outputs_lst = [output]
        self.gate_type = "OR"
        
class Nand2DRGate(Nand2DRGate):
    def __init__(self, name, input1, input2, output) -> None:
        super().__init__(name, [input1, input2], output)
        self.inputs_lst = [input1, input2]
        self.outputs_lst = [output]
        self.gate_type = "NAND"
 
 
###################################################################
###                   Multiplying Seesaws                       ###
### For Multiplying gates with output weights of 1, we assume   ###
### they are there to split the signals so they can be input to ###
### multiple gates.                                             ###
### But since seesaw compiler adds them by itself, we want to   ###
### avoid this split, and "short" them instead.                 ###
###################################################################
 
class MultiplyingDRSeesaw(MultiplyingDRSeesaw):
    def __init__(self, name, inp, outputs_list, weight_list) -> None:
        super().__init__(name, inp, outputs_list, weight_list)
        if all(w == 1 for w in weight_list):
            self.inputs_lst = [inp]
            self.outputs_lst = outputs_list
        
class MultiplyingSeesaw(MultiplyingSeesaw):
    def __init__(self, name, inp, outputs_list, weight_list) -> None:        
        super().__init__(name, inp, outputs_list, weight_list)
        if all(w == 1 for w in weight_list):
            self.inputs_lst = [inp]
            self.outputs_lst = outputs_list


###################################################################
###                   Translation Function                      ###
###################################################################
   
def get_seesaw_compiler_netlist( system ):
    netlist = []

    bm = {}
    for g in system.gates_list:
        if hasattr(g, 'inputs_lst'):
            bm.update({b: b for b in g.inputs_lst})
            bm.update({b: b for b in g.outputs_lst})
        else:
            print("\nError: Could not translate netlist.") 
            print("No translation to Seesaw Compiler for gate type: " + str(type(g)) + "\n") 
            print("For Multiplying Seesaw check if all the weights are 1's")
            print("For other gates, please add translation class to 'ToSeesawComp.py'\n")
            return []
            
    for g in system.gates_list:
        if isinstance(g, MultiplyingDRSeesaw) or isinstance(g, MultiplyingSeesaw):
            bm.update({out: g.inputs_lst[0] for out in g.outputs_lst})

    bn = {b: i for i, b in enumerate(set(bm.values()))}

    for b, i in bn.items():
        netlist.append('INPUT(' + str(i) + ')\t# ' + b.name)  
    netlist.append('')

    for g in system.gates_list:
        if hasattr(g, 'gate_type'):
            gstr = str(bn[bm[g.outputs_lst[0]]]) + ' = ' + g.gate_type + "("           
            gstr += ",".join(str(bn[bm[inp]]) for inp in g.inputs_lst)
            gstr += ")"
            netlist.append( gstr )
            
    return netlist
            
