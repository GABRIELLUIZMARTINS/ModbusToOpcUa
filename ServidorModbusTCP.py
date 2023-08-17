from pyModbusTCP.server import ModbusServer, DataBank
from Constantes import *

class DataModbus:
    def __init__(self,address,value):
        self.Address = address
        self.Value = value
        self.Connection = DISCONNECT
    def setAddress(self,adr):
        self.Address = adr
    def setValue(self,Vle):
        self.Value = Vle
    def getAddress(self):
        return self.Address
    def getValue(self):
        return self.Value
    def getConnection(self): 
        return self.Connection
    def setConnection(self,c):
        self.Connection = c

class Servidor_ModbusTCP:
    #Contrutor
    def __init__(self, _host, _port):
        self.databank = DataBank
        self.Server = ModbusServer(host=_host,port=_port,no_block=True)
        self.i=0
        self.ListIntModbus = []
        self.ListBoolModbus = []
        self.Host = _host
        self.Port = _port
    def __del__(self):
        self.stop()
    def set_Host(self,H):
        self.Host = H
        self.Server.host = self.Host
    def set_Port(self,P):
        self.Port = P
        self.Server.port = self.Port
    def get_Host(self):
        return self.Host
    def get_Port(self):
        return self.Port
    #Execução Servidor
    def run(self):
        try:
            self.Server.start()
            print("Modbus Server conectado.") 
            self.SetErrorModbus(False)
        except Exception:
            self.SetErrorModbus(True)
            print("!!!Erro ao iniciar o Modbus Server!!!")
    def ListsModbus(self):# Retorna uma Lista de Coils(bool) e Lista de registradores(inteiros)
            #Elipse permite 20 tag
            NumTags = 20
            #10 Holding Register
            NumAdressInt = list(range(int(NumTags/2)))
            #10 Coils
            NumAdressBool = list(range(int(NumTags/2)))

            #======== Lista de registradores ========
            for i,adrI in enumerate(NumAdressInt):
                self.ListIntModbus.append(DataModbus(adrI,0))
                #print(f"Registers: {adrI} ")
           
            #============ Lista de Coils ============
            for i,adrB in enumerate(NumAdressBool):
                self.ListBoolModbus.append(DataModbus(adrB,bool(0)))
                #print(f"Coils: {adrB} ")
            
            #self.ShowValues(5)
            return self.ListBoolModbus,self.ListIntModbus
    
    def AtualizarDadosModbus(self):
        #Colocar na lista  os itens em objetoModbus
        for i,conteudo in enumerate(self.ListBoolModbus):
            Vle = self.ReadCoil(i)
            self.ListBoolModbus[i].setValue(Vle)

        for i,conteudo in enumerate(self.ListIntModbus):
            Vle = self.ReadHoldingRegister(i)
            self.ListIntModbus[i].setValue(Vle)

    def SetErrorModbus(self,Erro):
        self.ErroModbus = Erro
    def ErrorModbus(self):
        return self.ErroModbus
    def stop(self):
        self.Server.stop()
    def WriteHoldingRegister(self,AddressInt,Value):
        self.Server.data_bank.set_holding_registers(AddressInt,[int(Value)])
    def ReadHoldingRegister(self,AddressInt):
        return self.Server.data_bank.get_holding_registers(AddressInt)
    def ReadCoil(self,AddressBool):
        return self.Server.data_bank.get_coils(AddressBool)
    def WriteCoil(self,AddressBool,Value):
        self.Server.data_bank.set_coils(AddressBool,[bool(Value)])
    def ShowValues(self):
        for i in self.ListIntModbus:
            print("Registers [", i.getAddress(),"] value:",self.ReadHoldingRegister(i.getAddress()))
        print("\n")
        for c in self.ListBoolModbus:
            print("Coils [", c.getAddress(),"] value:",self.ReadCoil(c.getAddress()))
        print("\n")
