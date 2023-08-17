from ServidorModbusTCP import *
from ClienteOpcUa import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from Constantes import *
import subprocess

class Ping:
    def __init__(self, host = 'localhost'):
        self.host = host
        self.ping()
    def ping(self):
        try:
            output = subprocess.check_output(['ping', '-n', '1', self.host])  # Executa o comando ping
            return True
        except subprocess.CalledProcessError:
            return False

class DataButton:
    def __init__(self,Btn,value):
        self.Button = Btn
        self.ValueVar = value
    def setBtn(self,btn):
        self.Button = btn
    def setValueVar(self,Vle):
        self.ValueVar = Vle
    def getBtn(self):
        return self.Button
    def getValueVar(self):
        return self.ValueVar

class Modbus2OpcUa(Servidor_ModbusTCP, ClientOpcUA):
    def __init__(self,host,port,url):
        Servidor_ModbusTCP.__init__(self,host,port)
        ClientOpcUA.__init__(self,url)
        self.run_client()   
        self.run()
    def Disconnect(self):
        self.stop()
        self.disconnect_client()
    def __del__(self):
        # Chamar os destrutores das classes pai
        Servidor_ModbusTCP.__del__(self)
        ClientOpcUA.__del__(self)
class MyWindow:
    def __init__(self):
        self.fonte = ['black',"Helvetica",12]
        self.fonteTitulo = ['white',"Gill Sans MT (Corpo)", 12]
        self.cor = "#ff0000"
        self.imagens = ["Right.png","Left.png","Duplex.png"]
        # Carrega a primeira imagem 
        self.indice_imagem = 0
        self.imagem = open("Imagens/" + self.imagens[self.indice_imagem])
        self.Mod2OPC = Modbus2OpcUa('127.0.0.1',502,"opc.tcp://127.0.0.1:4840")
        self.Incompativel = False   

        self.MainWindow()   
        self.window.mainloop()

    def inicializar_atributos(self):
        del self.Mod2OPC
        self.Mod2OPC = Modbus2OpcUa(self.entry_Host.get(),int(self.entry_Prt.get()),self.entry_Url.get())

        self.Iopc = None
        self.IModC = None
        self.IModR = None
        self.Start = False
        self.IopcAnterior = None
        self.IModCAnterior = None
        self.IModRAnterior= None
        self.BtnListO = []
        self.BtnListMC = []
        self.BtnListMR = []
        self.RefOpcMCoil = []# Matriz referencia dos índices row=0 => opc E row=1 => Modbus
        self.RefOpcMReg = []# Matriz referencia dos índices row=0 => opc E row=1 => Modbus
        self.sentido = 0
        self.connect = 0
        self.FreezeButton = FREEZEBUTTONS_OFF
        self.auxbtn = False

    def set_param_config(self,host,port,url):
        self.Mod2OPC.set_Host(host)
        self.Mod2OPC.set_Port(port)
        self.Mod2OPC.set_Url(url)

    def MainWindow(self):
        self.window=Tk()
        self.window.title('Configuração')
        self.window.geometry("422x340")
        self.Blue = '#9BAFB5'

        # criando um Frame com a cor predominante como fundo
        frame = Frame(self.window, bg=self.Blue)
        frame.pack(fill=BOTH, expand=1)

        #Label MODBUS TCP
        self.lbl_Mod=Label(frame, text="MODBUS TCP", fg='black', font=("Gill Sans MT (Títulos)", 12,'bold'), relief="solid", borderwidth=5)
        self.lbl_Mod['background'] = '#FFFFFF'
        self.lbl_Mod.config(width=40)  # Define a largura da Label como 20
        self.lbl_Mod.grid(row = 0, column = 0,sticky = N,padx=5, pady=5)

        #Label HOST
        self.lbl_Host=Label(frame, text="HOST", fg='#FFFFFF', font=("Gill Sans MT (Corpo)", 12))
        self.lbl_Host['background'] = self.Blue
        self.lbl_Host.grid(row = 1, column = 0,sticky = N,padx=5, pady=0)

        #Entry HOST
        self.entry_Host=Entry(frame, text="HOST", bd=5)
        self.entry_Host.insert(0, "127.0.0.1")
        self.entry_Host.grid(row = 2, column = 0,sticky = N,padx=5, pady=0)
        self.entry_Host['background'] = '#D9D9D9'
        self.entry_Host.config(width=40)

        #Label PORT
        self.lbl_Prt=Label(frame, text="PORT", fg='#FFFFFF', font=("Gill Sans MT (Corpo)", 12))
        self.lbl_Prt['background'] = self.Blue
        self.lbl_Prt.grid(row = 3, column = 0,sticky = N,padx=5, pady=0)

        #Entry PORT
        self.entry_Prt=Entry(frame, text="PORT", bd=5)
        self.entry_Prt.insert(0, "502")
        self.entry_Prt.grid(row = 4, column = 0,sticky = N,padx=5, pady=0)
        self.entry_Prt['background'] = '#D9D9D9'
        self.entry_Prt.config(width=40)

        #Label OPC UA
        self.lbl_OPC=Label(frame, text="OPC UA", fg='black', font=("Gill Sans MT (Títulos)", 12,'bold'), relief="solid", borderwidth=5)
        self.lbl_OPC['background'] = '#FFFFFF'
        self.lbl_OPC.grid(row = 5, column = 0,sticky = N,padx=5, pady=(35,0))
        self.lbl_OPC.config(width=40)  # Define a largura da Label

        #Label URL
        self.lbl_Url=Label(frame, text="URL", fg='#FFFFFF', font=("Gill Sans MT (Corpo)", 12))
        self.lbl_Url['background'] = self.Blue
        self.lbl_Url.grid(row = 6, column = 0,sticky = N,padx=5, pady=0)

        #Entry URL
        self.entry_Url=Entry(frame, width=24, text="URL", bd=5)
        self.entry_Url.insert(0, "opc.tcp://127.0.0.1:4840")
        self.entry_Url.grid(row = 7, column = 0,sticky = N,padx=5, pady=0)
        self.entry_Url['background'] = '#D9D9D9'
        self.entry_Url.config(width=40)  # Define a largura da Label

        #Botão Configurar
        self.btn=Button(frame, text="CONFIGURAR", command=self.Configurar,fg= '#9BAFB5', font=("Gill Sans MT (Títulos)", 12))
        self.btn.grid(row = 8, column = 0,sticky = N,padx=0, pady=35)
        self.btn['background'] = '#404040'
        self.btn.config(width=45)

    def DestroyNewWindow(self):
        #Destroi A janela 
        self.newWindow.destroy()
    def TestPing(self,hosT):
        P = Ping(hosT)
        print(hosT+" respondeu ao ping") if P.ping() else print(hosT+" NÃO respondeu ao ping")   
    def Configurar(self):
        self.window.iconify()
        self.newWindow = Toplevel(self.window)
        self.newWindow.title("Mapeamento") 
        print("self.Mod2OPC.ErrorModbus()",self.Mod2OPC.ErrorModbus()) 
        print("self.Mod2OPC.ErrorOPC()",self.Mod2OPC.ErrorOPC())
        self.inicializar_atributos()
        
        if(self.Mod2OPC.ErrorModbus() or self.Mod2OPC.ErrorOPC()):
            #UMA JANELA FALANDO QUE ACONTECEU ERRO DE CONEXÃO PEDINDO PRA ENTRAR COM OS VALORES NOVAMENTE
            self.newWindow.geometry("180x80")
            self.newWindow['background']= self.Blue 
            self.LbErro=Label(self.newWindow, text="ERRO DE CONEXÃO!", 
                            fg='#FFFFFF', 
                            font=("Gill Sans MT (Corpo)", 12)
                            )
            self.LbErro.grid(row = 0, column = 0,columnspan=2,sticky = N,padx=5, pady=5)
            self.LbErro['background']= self.Blue    
            self.btn = Button(self.newWindow, 
                            text="VOLTAR",fg= '#9BAFB5', 
                                        font=("Gill Sans MT (Títulos)", 10),
                            command=self.DestroyNewWindow) 
            self.btn.grid(row = 1, column = 0,columnspan=2,sticky = N,padx=5, pady=5)
            self.btn ['background'] = '#404040'
        else: 
                       

            self.newWindow.geometry("818x525")
            self.newWindow['background']= self.Blue 

            self.ListaOPC = self.Mod2OPC.ListDataOPCUA()
            self.ListaModbusCoils,self.ListaModbusRegistradores = self.Mod2OPC.ListsModbus()
            #-----------------------------------------------------------------------------------------------
            #Label OPC UA
            self.lbl_OPC=Label(self.newWindow, text="OPC UA", fg='black', font=("Gill Sans MT (Títulos)", 12,'bold'), relief="solid", borderwidth=5)
            self.lbl_OPC['background'] = '#FFFFFF'
            self.lbl_OPC.grid(row = 0, column = 0,columnspan=3,sticky = N,padx=0, pady=5)
            self.lbl_OPC.config(width=22)  # Define a largura da Label 

            #Label MODBUS TCP
            self.lbl_Mod=Label(self.newWindow, text="MODBUS TCP", fg='black', font=("Gill Sans MT (Títulos)", 12,'bold'), relief="solid", borderwidth=5)
            self.lbl_Mod['background'] = '#FFFFFF'
            self.lbl_Mod.config(width=47)  # Define a largura da Label
            self.lbl_Mod.grid(row = 0, column = 4,columnspan=6,sticky = N,padx=0, pady=5)


            self.Desc=Label(self.newWindow, text="COILS", fg='#FFFFFF', font=("Gill Sans MT (Corpo)", 12))
            self.Desc.grid(row = 1, column = 5,columnspan=2,sticky = N,padx=5, pady=5)
            self.Desc['background']= self.Blue   

            self.Desc=Label(self.newWindow, text=" REGISTERS", fg='#FFFFFF', font=("Gill Sans MT (Corpo)", 12))
            self.Desc.grid(row = 1, column = 8,columnspan=2,sticky = N,padx=5, pady=5)
            self.Desc['background']= self.Blue   

            #Adciona Botão que indica o sentido do fluxo de dados
            self.AddButtonImage()

            #Criando/dispondo Labels e Botões
            self.LabelsNewWindow()
            self.Botoes(FREEZEBUTTONS_OFF)
            #Fica esperando as váriveis serem linkadas
            self.btn_StartStop = Button(self.newWindow, 
                                        text="START" if not self.Start else "Stop",
                                        command=self.StartAction,fg= '#9BAFB5', 
                                        font=("Gill Sans MT (Títulos)", 12)
                                        )
            self.btn_StartStop.grid(row=1, column=3,sticky = W,padx=2, pady=1)
            self.btn_StartStop.config(width=8)
            self.btn_StartStop['background'] = '#404040'

            self.newWindow.after(500,self.Referenciar_Indicarsentido)
            
            self.newWindow.mainloop()

    def StartAction(self):
        self.Start = not self.Start
        self.btn_StartStop.config(text="Start" if not self.Start else "Stop")
        if(self.Start == False):
            print("QUANDO START FALSE ")
            self.Botoes(FREEZEBUTTONS_OFF)

    def Referenciar_Indicarsentido(self):
        if(self.Start):
            #Configurar botões 
            self.ConfigBTN(FREEZEBUTTONS_ON)
            self.newWindow.after(500,self.Mapping)
        else:
            #Linkar variaveis 
            self.ReferenciasVariaveis()
            #Configurar botões 
            self.ConfigBTN(FREEZEBUTTONS_OFF)
            self.newWindow.after(500,self.Referenciar_Indicarsentido)
            
    def ConfigBTN(self,FreezeButton):
        if(FreezeButton):
            self.Botoes(FREEZEBUTTONS_ON)
            self.botaoIMG.configure(state="disabled")
        else:
            self.Sense(self.indice_imagem)
            self.botaoIMG.configure(state="normal")  
    

    def Mapping(self):
        if(self.Start):
            self.newWindow.after(500,self.Mapping)
        else:
            self.newWindow.after(500,self.Referenciar_Indicarsentido)
        PingICMPv6 =  Ping('localhost')
        PingInicial = Ping('192.168.1.10')
        if(self.indice_imagem == OPCtoMODBUS):#OPCtoMODBUS    
            self.OPCtoMod()  
        elif(self.indice_imagem == MODBUStoOPC):#MODBUStoOPC 
            self.ModtoOPC()
        elif(self.indice_imagem == TWOSENSES):  
            self.ModtoOPC()
            self.OPCtoMod()
        PingFinal = Ping('192.168.1.10')

        self.LabelsNewWindow()# Atualizar valores na tela
    def OPCtoMod(self):
        for Indice in self.RefOpcMCoil: # Indice[0] indices lista OPC # Indice[1] indices lista Modbus
            print("RefOpcMCoil",self.RefOpcMCoil)
            self.Mod2OPC.AtualizarDadosOPC()
            #Valores sendo transferidos da lista OPC para lista Modbus             
            valorMapeado = self.ListaOPC[Indice[OPC]].getValue()
            self.ListaModbusCoils[Indice[MODBUS]].setValue(valorMapeado)

            #Valor é enviado por meio do servidor MODBUS
            self.Mod2OPC.WriteCoil(Indice[MODBUS],valorMapeado)

        for Indice in self.RefOpcMReg: # Indice[0] indices lista OPC # Indice[1] indices lista Modbus
            self.Mod2OPC.AtualizarDadosOPC()
            #Valores sendo transferidos da lista OPC para Modbus                
            valorMapeado = self.ListaOPC[Indice[OPC]].getValue()
            self.ListaModbusRegistradores[Indice[MODBUS]].setValue(valorMapeado)
            #Valor é enviado por meio do servidor MODBUS
            self.Mod2OPC.WriteHoldingRegister(Indice[MODBUS],valorMapeado)
        self.Mod2OPC.AtualizarDadosModbus()
    def ModtoOPC(self):
        print("RefOpcMCoil",self.RefOpcMCoil)
        for Indice in self.RefOpcMCoil: # Indice[0] indices lista OPC # Indice[1] indices lista Modbus
            self.Mod2OPC.AtualizarDadosModbus()
            #Valores sendo transferidos da lista Modbus para OPC                
            valorMapeado = self.ListaModbusCoils[Indice[MODBUS]].getValue()
            self.ListaOPC[Indice[OPC]].setValue(valorMapeado) 
     
            #Valor é enviado por meio do client OPC UA
            #nodeid = Nome do nó, Valor que será mapeado, Booleano que indica se é Bool ou Int
            self.Mod2OPC.set_Client(self.ListaOPC[Indice[OPC]],valorMapeado,ISBOOL)

        for Indice in self.RefOpcMReg: # Indice[0] indices lista OPC # Indice[1] indices lista Modbus
            self.Mod2OPC.AtualizarDadosModbus()
            #Valores sendo transferidos da lista Modbus para OPC                
            valorMapeado = self.ListaModbusRegistradores[Indice[MODBUS]].getValue()
            self.ListaOPC[Indice[OPC]].setValue(valorMapeado) 

            #Valor é enviado por meio do client OPC UA
            self.Mod2OPC.set_Client(self.ListaOPC[Indice[OPC]],valorMapeado,ISINT)
        self.Mod2OPC.AtualizarDadosOPC()

    def AddButtonImage(self):
        imagem = Image.open("Imagens/" + self.imagens[self.indice_imagem])
        imagem = imagem.resize((76, 18))
        self.imagem_tk = ImageTk.PhotoImage(imagem)
        self.botaoIMG = Button(self.newWindow, image=self.imagem_tk, command=self.trocar_imagem)
        self.botaoIMG.grid(row = 2, column = 3,sticky = W,padx=2, pady=1)

    def trocar_imagem(self):
        # Atualiza o índice da imagem e carrega a nova imagem
        self.indice_imagem = (self.indice_imagem + 1) % len(self.imagens)
        nova_imagem = Image.open("Imagens/" + self.imagens[self.indice_imagem])
        nova_imagem = nova_imagem.resize((30, 20))
        nova_imagem_tk = ImageTk.PhotoImage(nova_imagem)

        # Atualiza a imagem do botão
        self.botaoIMG.configure(image=nova_imagem_tk)
        self.botaoIMG.image = nova_imagem_tk  # Atualiza imagem

    def Sense(self,Sense):
        if(Sense == OPCtoMODBUS):
            self.sentido = OPCtoMODBUS
        elif(Sense == MODBUStoOPC):
            self.sentido = MODBUStoOPC          
        else:
            self.sentido = TWOSENSES
    def IndiceMesmaSublista(self,Reflist,IndcOPC,IndcMod):
        #Nenhum botão foi selecionado
        ThereIsInList = 0 
        for sublista in Reflist:
            #Se o indice esta na sublista
            if IndcOPC in sublista:
                ThereIsInList = ThereIsInList + 1
            #Se o indice esta na sublista
            if IndcMod in sublista:
                ThereIsInList = ThereIsInList + 1
            #Se os dois indices estão na mesma sublista
            if IndcOPC in sublista and IndcMod in sublista:
                ThereIsInList = ThereIsInList + 1
        #Se ThereIsInList = 1, só um botão foi selecionado
        #Se ThereIsInList = 2, os dois botões foram selecionados mas não necessáriamente na mesma sublista
        #Se ThereIsInList = 3 = os dois botões foram selecionados na mesma sublista
        ##### Se ThereIsInList = 0 Retorna False
        ##### Se ThereIsInList = 3 Retorna True
        ##### Se ThereIsInList = 1 ou 2 Retorna -1
        return True if ThereIsInList == 3 else (False if ThereIsInList == 0 else -1)

    def RemoveListRef(self,List,varOPC,varMod):
        # Removendo o número da coluna OPC
        for sublista in List:
            if varOPC in sublista:
                sublista.remove(varOPC)
        # Removendo o número da coluna Modbus
        for sublista in List:
            if varMod in sublista:
                sublista.remove(varMod)
        # Retirando as lista vazia decorrentes da desseleção dos botões
        self.RefOpcMCoil = list(filter(bool,self.RefOpcMCoil))
        self.RefOpcMReg = list(filter(bool,self.RefOpcMReg))

    def ButtonSelect(self,atual,anterior,list_num):
        #Se for a primeira vez que o botão foi selecionado
        if anterior == None:
            if list_num == LIST_OPCUA:
                self.BtnListO[atual].getBtn().configure(bg=RED_COLOR_LIGHT)
                if self.Incompativel:
                    self.BtnListO[atual].getBtn().configure(bg=RED_COLOR)
            elif list_num == LIST_MODBUSCOIL:
                self.BtnListMC[atual].getBtn().configure(bg=RED_COLOR_LIGHT)
                if self.Incompativel:
                    self.BtnListMC[atual].getBtn().configure(bg=RED_COLOR)
            elif list_num == LIST_MODBUSREGISTER:
                self.BtnListMR[atual].getBtn().configure(bg=RED_COLOR_LIGHT)
                if self.Incompativel:
                    self.BtnListMR[atual].getBtn().configure(bg=RED_COLOR)
        else:
            if list_num == LIST_OPCUA:
                self.BtnListO[anterior].getBtn().configure(bg=RED_COLOR)
                self.BtnListO[atual].getBtn().configure(bg=RED_COLOR_LIGHT)
            elif list_num == LIST_MODBUSCOIL:
                self.BtnListMC[anterior].getBtn().configure(bg=RED_COLOR)
                self.BtnListMC[atual].getBtn().configure(bg=RED_COLOR_LIGHT)
            elif list_num == LIST_MODBUSREGISTER:
                self.BtnListMR[anterior].getBtn().configure(bg=RED_COLOR)
                self.BtnListMR[atual].getBtn().configure(bg=RED_COLOR_LIGHT)
    def exibir_erro(self):
        messagebox.showerror("Erro", "Tipos de dados incompatíveis!")
        self.Incompativel = True   
    def ReferenciasVariaveis(self):
        #Se um Botão opc e modbus Coil forem selecionados
        if(self.Iopc != None and self.IModC != None):
            #Se a váriavel OPC for um boleano será mapeada como Coil
            if(self.ListaOPC[self.Iopc].getType() == "Boolano"):
                #AddRefBool()
                # Se os dois indices selecionados estiverem na mesma sublista
                if(self.IndiceMesmaSublista(self.RefOpcMCoil,self.Iopc,self.IModC) == True):
                    #Trocar cor botões
                    self.BotaoConfig(self.BtnListO[self.Iopc],OFF_BUTTON)     
                    self.BotaoConfig(self.BtnListMC[self.IModC],OFF_BUTTON)   
                    #Remove da lista
                    self.RemoveListRef(self.RefOpcMCoil,self.Iopc,self.IModC)
                    #Retira conexão
                    self.ListaOPC[self.Iopc].setConnection(DISCONNECT)
                    self.ListaModbusCoils[self.IModC].setConnection(DISCONNECT)
                elif (self.IndiceMesmaSublista(self.RefOpcMCoil,self.Iopc,self.IModC) == False):
                    #Trocar cor botões
                    self.BotaoConfig(self.BtnListO[self.Iopc],ON_BUTTON)     
                    self.BotaoConfig(self.BtnListMC[self.IModC],ON_BUTTON)   
                    #Colocar na lista os indices das listas OPC e Modbus Coil
                    self.RefOpcMCoil.append([self.Iopc,self.IModC])
                    #Identidicando quais são os indices que foram conectados
                    self.ListaOPC[self.Iopc].setConnection(self.connect)
                    self.ListaModbusCoils[self.IModC].setConnection(self.connect)
                self.Iopc = None 
                self.IModC = None 
                self.IopcAnterior = None
                self.IModCAnterior = None
            else:
                self.exibir_erro()
                self.ButtonSelect(self.Iopc,None,LIST_OPCUA)
                self.ButtonSelect(self.IModC,None,LIST_MODBUSCOIL)
                self.Iopc = None 
                self.IModC = None 
        if(self.Iopc != None and self.IModR != None):
            #Se a váriavel OPC for um inteiro será mapeada como Register
            if(self.ListaOPC[self.Iopc].getType() == "Inteiro"):
                #AddRefInt()
                # Se os dois indices selecionados estiverem na mesma sublista
                if(self.IndiceMesmaSublista(self.RefOpcMReg,self.Iopc,self.IModR) == True):
                    #Trocar cor botões
                    self.BotaoConfig(self.BtnListO[self.Iopc],OFF_BUTTON)
                    self.BotaoConfig(self.BtnListMR[self.IModR],OFF_BUTTON)    
                    #Remove da lista
                    self.RemoveListRef(self.RefOpcMReg,self.Iopc,self.IModR)
                    #Retira conexão
                    self.ListaOPC[self.Iopc].setConnection(DISCONNECT)
                    self.ListaModbusRegistradores[self.IModR].setConnection(DISCONNECT)
                elif (self.IndiceMesmaSublista(self.RefOpcMReg,self.Iopc,self.IModR) == False):
                    #Trocar cor botões
                    self.BotaoConfig(self.BtnListO[self.Iopc],ON_BUTTON)     
                    self.BotaoConfig(self.BtnListMR[self.IModR],ON_BUTTON)   
                    #Colocar na lista os indices das listas OPC e Modbus Coil
                    self.RefOpcMReg.append([self.Iopc,self.IModR])
                    #Identidicando quais são os indices que foram conectados
                    self.ListaOPC[self.Iopc].setConnection(self.connect)
                    self.ListaModbusRegistradores[self.IModR].setConnection(self.connect)
                self.Iopc = None 
                self.IModR = None   
                self.IopcAnterior = None
                self.IModRAnterior = None
            else:
                self.exibir_erro() 
                self.ButtonSelect(self.Iopc,None,LIST_OPCUA)
                self.ButtonSelect(self.IModR,None,LIST_MODBUSREGISTER)
                self.Iopc = None 
                self.IModR = None  
    def AddLabel(self,List,i,j):# Adiciona Label somente na JANELA newWindow
        if(self.Start == False):
            if(List == self.ListaOPC):
                for indice, conteudo in enumerate(List):
                    label = Label(self.newWindow, text=conteudo.getName(), fg=(self.fonte[0]), font=(self.fonte[1], self.fonte[2]))
                    label.grid(row=indice+i, column=j,sticky = W,padx=(5,2), pady=1)
                    label.config(width=10)    
            else:
                for indice, conteudo in enumerate(List):
                    label = Label(self.newWindow, text= str(conteudo.getAddress()), fg=(self.fonte[0]), font=(self.fonte[1], self.fonte[2]))
                    label.grid(row=indice+i, column=j,sticky = W,padx=2, pady=1)
                    label.config(width=10)    

        for indice, conteudo in enumerate(List):
            label = Label(self.newWindow, 
                          text=str(conteudo.getValue()).replace("[", "").replace("]", ""), 
                          fg=(self.fonte[0]), 
                          font=(self.fonte[1],
                                self.fonte[2])
                                )
            label.grid(row=indice+i, column=j+1,sticky = W,padx=2, pady=1)
            label.config(width=10) 
    def LabelsNewWindow(self):           
        # Cria os labels com os valores da lista ListDataOPCUA
        self.AddLabel(self.ListaOPC,1+1,0)
        label = Label(self.newWindow, text="Node", fg=(self.fonteTitulo[0]), font=(self.fonteTitulo[1], self.fonteTitulo[2]))
        label.grid(row=1, column=0,sticky = W,padx=2, pady=1)
        label.config(width=10)  
        label['background'] = self.Blue
        label = Label(self.newWindow, text="Value", fg=(self.fonteTitulo[0]), font=(self.fonteTitulo[1], self.fonteTitulo[2]))
        label.grid(row=1, column=1,sticky = W,padx=2, pady=1)
        label.config(width=10)  
        label['background'] = self.Blue
        # Cria os labels com os valores da lista ListaModbusCoils
        self.AddLabel(self.ListaModbusCoils,1+2,5)
        label = Label(self.newWindow, text="Adress", fg=(self.fonteTitulo[0]), font=(self.fonteTitulo[1], self.fonteTitulo[2]))
        label.grid(row=1+1, column=5,sticky = W,padx=2, pady=1)
        label.config(width=10)  
        label['background'] = self.Blue
        label = Label(self.newWindow, text="Value", fg=(self.fonteTitulo[0]), font=(self.fonteTitulo[1], self.fonteTitulo[2]))
        label.grid(row=1+1, column=6,sticky = W,padx=2, pady=1)
        label.config(width=10)  
        label['background'] = self.Blue

        # Cria os labels com os valores da lista ListaModbusRegistradores
        self.AddLabel(self.ListaModbusRegistradores,1+2,8)
        label = Label(self.newWindow, text="Adress", fg=(self.fonteTitulo[0]), font=(self.fonteTitulo[1], self.fonteTitulo[2]))
        label.grid(row=1+1, column=8,sticky = W,padx=2, pady=1)
        label.config(width=10)  
        label['background'] = self.Blue
        label = Label(self.newWindow, text="Value", fg=(self.fonteTitulo[0]), font=(self.fonteTitulo[1], self.fonteTitulo[2]))
        label.grid(row=1+1, column=9,sticky = W,padx=2, pady=1)
        label.config(width=10)  
        label['background'] = self.Blue
    def BotaoConfig(self,button,OnOffBtn):
        self.auxbtn = not self.auxbtn 
        if self.auxbtn:
            self.connect = self.connect + 1
        Btn = button.getBtn()
        button.setValueVar(self.connect)
        Value = str(self.connect)
        if(OnOffBtn):
            Btn.configure(text="Var " + Value)# if Value !=-1 else "         ")
            Btn.configure(bg=GREEN_COLOR)
        else:
            Btn.configure(text="         ")
            Btn.configure(bg=RED_COLOR)

    def Botoes(self,FreezeButton):
        # Cria os botões seleção váriaveis OPC
        for i, conteudo in enumerate(self.ListaOPC):
            button = Button(self.newWindow, 
                            text="Var " + str(conteudo.getConnection()) if conteudo.getConnection() !=-1 else "         ",
                            bg= RED_COLOR if conteudo.getConnection() ==-1 else GREEN_COLOR,
                            command=lambda i=i: self.change_index(i, LIST_OPCUA)) 
            if(FreezeButton):
                button.configure(state="disabled")
            else:
                button.configure(state="normal")
            self.BtnListO.append(DataButton(button,str(conteudo.getConnection())))
            button.grid(row=i+2, column=2,sticky = W,padx=2, pady=1)
        # Cria os botões seleção váriaveis Modbus Coils
        for i, conteudo in enumerate(self.ListaModbusCoils):
            button = Button(self.newWindow, 
                            text="Var " + str(conteudo.getConnection()) if conteudo.getConnection() !=-1 else "         ",
                            bg= RED_COLOR if conteudo.getConnection() ==-1 else GREEN_COLOR,
                            command=lambda i=i: self.change_index(i,LIST_MODBUSCOIL))
            if(FreezeButton):
                button.configure(state="disabled")
            else:
                button.configure(state="normal")
            self.BtnListMC.append(DataButton(button,str(conteudo.getConnection())))
            button.grid(row=i+1+2, column=4,sticky = W,padx=2, pady=1)       
        # Cria os botões seleção váriaveis Modbus Registers
        for i, conteudo in enumerate(self.ListaModbusRegistradores):
            button = Button(self.newWindow, 
                            text="Var " + str(conteudo.getConnection()) if conteudo.getConnection() !=-1 else "         ",
                            bg= RED_COLOR if conteudo.getConnection() ==-1 else GREEN_COLOR,
                            command=lambda i=i: self.change_index(i,LIST_MODBUSREGISTER))
            if(FreezeButton):
                button.configure(state="disabled")
            else:
                button.configure(state="normal")
            self.BtnListMR.append(DataButton(button,str(conteudo.getConnection())))
            button.grid(row=i+1+2, column=7,sticky = W,padx=2, pady=1)

    # Método para identificar qual botão foi apertado
    def change_index(self, i, list_num):
        if list_num == LIST_OPCUA:
            self.Iopc = i
            print("Iopc",i)
            self.ButtonSelect(self.Iopc,self.IopcAnterior,list_num)
            self.IopcAnterior = i
        elif list_num == LIST_MODBUSCOIL:
            self.IModC = i
            print("IModC",i)
            self.ButtonSelect(self.IModC,self.IModCAnterior,list_num)
            self.IModCAnterior = i
        elif list_num == LIST_MODBUSREGISTER:
            self.IModR = i
            print("IModR:",i)
            self.ButtonSelect(self.IModR,self.IModRAnterior,list_num)
            self.IModRAnterior = i


if __name__ == '__main__':
    MyWindow()

   
    