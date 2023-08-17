from opcua import Client,ua 
from Constantes import *

class DataOPC:
    def __init__(self, type,name,value,nameNode):
        self.Name = name
        self.Type = self.typeValeu(type.NodeIdType)
        self.Value = bool(value) if self.typeValeu(type.NodeIdType) == "Boolano" else value
        self.NameNode = nameNode
        self.Connection = DISCONNECT
    def typeValeu(self,tp):
        if(tp == 0):
            return "Boolano"
        else:
            return "Inteiro"
    def getNameNode(self):
        return self.NameNode   
    def getType(self):
        return self.Type   
    def getName(self):
        return self.Name 
    def getValue(self): 
        return self.Value
    def setValue(self,v):
        self.Value = v
    def getConnection(self): 
        return self.Connection
    def setConnection(self,c):
        self.Connection = c

class ClientOpcUA:
    #Contrutor
    def __init__(self, url):
        self.Url = url
        self.client = Client(url)
        self.ListDataOPC = []
    def __del__(self):
        self.disconnect_client()
    def set_Url(self,U):
        self.Url = U
    def get_Url(self):
        return self.Url

    #Execução Client
    def run_client(self):
        try:
            self.client.connect()
            print("Client OPC UA conectado.") 
            #self.ListDataOPCUA()
            self.SetErrorOPC(False)
        except Exception:
            self.SetErrorOPC(True)
            print("!!!Erro na conexão Client OPC UA!!!")
    def ListDataOPCUA(self):
        Programs = self.FindNodePrograms(self.client.get_root_node())
        PLC_PRG = Programs.get_children()
        #Possui só um PLC_PRG então é PLC_PRG[0]
        self.variablesPRG = PLC_PRG[0].get_children() 
        for i in self.variablesPRG:
                    if(i.get_node_class() == 2):
                        #Colocar na lista  os itens em objetoOPC
                        self.ListDataOPC.append(DataOPC(i.get_data_type(),
                                                   i.get_display_name().Text,
                                                   i.get_value(),
                                                   i)
                                                   )
                    else:
                        AUXNode = i.get_children()
                        for j in AUXNode:
                            if(j.get_node_class() == 2):
                                self.ListDataOPC.append(DataOPC(j.get_data_type(),
                                                                str(i.get_display_name().Text) + '.' +j.get_display_name().Text,
                                                                j.get_value(),
                                                                j)
                                                           )
        return self.ListDataOPC
    def AtualizarDadosOPC(self):
        indice = 0
        for i in self.variablesPRG:
            # Se i = 2 variavel, se i = 1 Nó
            if(i.get_node_class() == 2):
                #Colocar na lista  os itens em objetoOPC
                self.ListDataOPC[indice].setValue(i.get_value())
                indice = indice + 1
            else:
                AUXNode = i.get_children()
                for  j in AUXNode:
                    if(j.get_node_class() == 2):
                        self.ListDataOPC[indice].setValue(j.get_value())
                        indice = indice + 1

    def SetErrorOPC(self,Erro):
        self.ErroOPC = Erro
    def ErrorOPC(self):
        return self.ErroOPC
    def FindNodePrograms(self,node):
        # Verifica se o nó atual é o nó "Programs"
        if node.get_browse_name().Name == "Programs":
            return node
        # Obtém os filhos do nó atual
        children = node.get_children()
        # Percorre recursivamente os filhos em busca do nó "Programs"
        for child in children:
            result = self.FindNodePrograms(child)
            if result is not None:
                return result
        return None
    def set_Client(self,DataOpcUa,DataModbus,IsBool):
        nodeid = DataOpcUa.getNameNode()
        Node = self.client.get_node(nodeid)
        if(IsBool): 
            Node.set_value(ua.Variant(bool(DataModbus[0]), ua.VariantType.Boolean))
        else:
            Node.set_value(ua.Variant(int(DataModbus[0]), ua.VariantType.Int64))
    def disconnect_client(self):
        return self.client.disconnect()