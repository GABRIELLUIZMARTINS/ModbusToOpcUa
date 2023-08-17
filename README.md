# ModbusToOpcUa
**Software de integração OPC UA e Modbus TCP**

Este software foi desenvolvido para permitir a integração entre os protocolos de comunicação OPC UA e Modbus TCP. 

**Instalação e Configuração**
- Faça a configuração do ambiente Codesys:
    - Faça a configuração dos Símbolos(Symbol Configuration).
    - Permita que o CLP virtual faça login anônimo.

- Instale e configure o driver de comunicação Modbus TCP no Elipse E3:
    - Siga as instruções detalhadas no documento Exemplos/Configuração Codesys e Elipse.pdf para instalar e configurar o driver de comunicação Modbus TCP no Elipse E3.

- Download das bibliotecas necessárias:
    - Todas as bibliotecas e dependências utilizadas pelo software estão listadas no arquivo requirements.txt. Faça o download e instalação das bibliotecas listadas neste arquivo antes de executar o software.

**Funcionamento**
- Inicializando o programa:
    - Ao iniciar o programa, ele inicializará o CLP virtual do Codesys e fará a conexão com o dispositivo Modbus TCP.

- Configuração dos parâmetros:
    - Antes de iniciar a integração, é necessário configurar os parâmetros dos respectivos protocolos, como endereços IP, portas e host.
    - Uma vez que todos os parâmetros estejam configurados corretamente, selecione o botão "Configurar".

- Mapeamento das variáveis:
    - Com os parâmetros de comunicação configurados, você poderá conectar as variáveis OPC UA com as variáveis Modbus TCP e selecionar o sentido do mapeamento.
    - Certifique-se de realizar o mapeamento corretamente para garantir uma comunicação precisa entre os dois protocolos.

- Iniciando o mapeamento:
    - Com todas as configurações e mapeamentos realizados, selecione o botão "Start" para iniciar o processo de integração entre os protocolos OPC UA e Modbus TCP.

**Observações importantes:**
- No diretório principal do projeto, você encontrará o arquivo Modbus2opcua.py, que é o script principal.
- Certifique-se de que todas as dependências listadas no arquivo requirements.txt foram instaladas corretamente antes de executar o software.
- Verifique se as configurações do ambiente Codesys e do Elipse E3 foram realizadas conforme as instruções fornecidas.

