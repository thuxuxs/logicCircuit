class Port:
    def __init__(self,index,gate,state=-1):
        self.index=index
        self.gate=gate
        self.state=state
        self.connector=[]

    def set_state(self,state):
        self.state=state

    def set_connector(self,c):
        self.connector.append(c)

class Connector:
    def __init__(self,port_in,port_out):
        self.port_in=port_in
        self.port_out=port_out

class BasicGate:
    def __init__(self,i,o=1):
        self.in_state=[-1]*i
        self.out_state=[-1]*o
        self.in_num=i
        self.out_num=o
        self.in_port=[Port(j,self) for j in range(i)]
        self.out_port=[Port(j,self) for j in range(o)]

    def o2i(self,next_gate,next_index,out_index=0):
        c=Connector(self.out_port[out_index],next_gate.in_port[next_index])
        if next_gate.in_port[next_index].connector == []:
            next_gate.in_port[next_index].set_connector(c)
            self.out_port[out_index].set_connector(c)
        else:
            print("Gate input occupied")

    def set_input(self,index,state):
        assert state in [0,1]
        self.in_state[index]=state
        if -1 not in self.in_state:
            self.out_state=self.logic()
            for i,j in enumerate(self.out_state):
                self.out_port[i].set_state(j)
                if self.out_port[i].connector!=[]:
                    for ct in self.out_port[i].connector:
                        ct.port_out.gate.set_input(ct.port_out.index,j)

    def logic(self):
        pass

class AND(BasicGate):
    def __init__(self):
        super().__init__(i=2)

    def logic(self):
        if 0 in self.in_state:
            return [0]
        else:
            return [1]

class OR(BasicGate):
    def __init__(self):
        super().__init__(i=2)

    def logic(self):
        if 1 in self.in_state:
            return [1]
        else:
            return [0]

class NOT(BasicGate):
    def __init__(self):
        super().__init__(i=1)

    def logic(self):
        return [1-self.in_state[0]]

class NAND(BasicGate):
    def __init__(self):
        super().__init__(i=2)

    def logic(self):
        if self.in_state==[1,1]:
            return [0]
        else:
            return [1]

class NOR(BasicGate):
    def __init__(self):
        super().__init__(i=2)

    def logic(self):
        if self.in_state==[0,0]:
            return [1]
        else:
            return [0]

class XOR(BasicGate):
    def __init__(self):
        super().__init__(i=2)

    def logic(self):
        if sum(self.in_state)==1:
            return [1]
        else:
            return [0]

class INPUT(BasicGate):
    def __init__(self):
        super().__init__(i=1)

    def logic(self):
        return self.in_state

class OR_N(BasicGate):
    def __init__(self,n):
        super().__init__(i=n)

    def logic(self):
        if 1 in self.in_state:
            return [1]
        else:
            return [0]

class AND_N(BasicGate):
    def __init__(self,n):
        super().__init__(i=n)

    def logic(self):
        if 0 in self.in_state:
            return [0]
        else:
            return [1]

# %%
if __name__ == "__main__":
    input=[INPUT() for i in range(3)]
    xor1=XOR()
    xor2=XOR()
    and1=AND()
    and2=AND()
    and3=AND()
    or_3=OR_N(3)

    input[0].o2i(xor1,0)
    input[1].o2i(xor1,1)
    input[0].o2i(and1,0)
    input[1].o2i(and1,1)
    input[0].o2i(and2,0)
    input[2].o2i(and2,1)
    input[1].o2i(and3,0)
    input[2].o2i(and3,1)
    xor1.o2i(xor2,0)
    input[2].o2i(xor2,1)
    and1.o2i(or_3,0)
    and2.o2i(or_3,1)
    and3.o2i(or_3,2)

    for s in [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]:
        print(s,end=';')
        for i,j in enumerate(s):
            input[i].set_input(0,j)

        for p in [xor2,or_3]:
            print(p.out_state[0],end=' ')
        print('\n')
