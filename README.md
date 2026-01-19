# Bomba Simulada para Airsoft 🎯

Projeto para criar uma bomba simulada (NÃO REAL) para jogos de airsoft usando Raspberry Pi.

## ⚠️ AVISO IMPORTANTE
Este projeto é apenas para simulação e jogos de airsoft. NÃO é uma bomba real e não deve ser usado de forma a causar alarme ou confusão em locais públicos.

## Componentes Necessários

- **Raspberry Pi 2 Model B** (ou superior com GPIO)
- **Display TFT SPI 240x320** (3.2" TFT com controlador ST7789)
- **Teclado numérico matricial 4x3** (12 teclas: 1-9, 0, *, #)
- **LEDs** (vermelhos recomendados) - mínimo 2
- **Resistores 220Ω** para LEDs
- **Buzzer opcional** (para som de alerta)
- **Fios jumper**
- **Breadboard** (opcional, para testes)

## 🚀 Instalação Rápida

### Para Raspberry Pi Nova (Primeira Vez)

1. **Siga o guia completo:** Veja `SETUP_RASPBERRY.md` para configuração inicial completa

### Para Raspberry Pi Já Configurada

1. **Ativar SPI:**
```bash
sudo raspi-config
# Interface Options > SPI > Enable
sudo reboot
```

2. **Executar script de instalação:**
```bash
cd ~/AirsoftProject
chmod +x install.sh
./install.sh
```

3. **Reiniciar (se necessário):**
```bash
sudo reboot
```

O script `install.sh` irá:
- Atualizar o sistema
- Instalar todas as dependências necessárias
- Ativar SPI e I2C
- Instalar bibliotecas Python

## 📐 Montagem do Hardware

**⚠️ IMPORTANTE:** Veja `HARDWARE_SETUP.md` para diagramas detalhados e instruções completas.

### Resumo das Conexões

#### Display TFT SPI 240x320
- **VCC** → Pin 2 (5V)
- **GND** → Pin 6 (GND)
- **MOSI** → Pin 19 (GPIO 10)
- **SCLK** → Pin 23 (GPIO 11)
- **CS** → Pin 24 (GPIO 8)
- **DC** → Pin 18 (GPIO 24)
- **RST** → Pin 22 (GPIO 25)

#### LEDs
- **LED 1:** Anodo → GPIO 18 (Pin 12) via resistor 220Ω → GND
- **LED 2:** Anodo → GPIO 23 (Pin 16) via resistor 220Ω → GND

#### Teclado Matricial 4x3
- **Linhas:** GPIO 5, 6, 13, 19 (Pins 29, 31, 33, 35)
- **Colunas:** GPIO 26, 20, 21 (Pins 37, 38, 40)

#### Buzzer (Opcional)
- **Positivo** → GPIO 22 (Pin 15) via resistor 1kΩ
- **Negativo** → GND

## 🎮 Uso

1. **Configurar o código da bomba:**
   Edite `config.py` e altere `CORRECT_CODE` para o código desejado.

2. **Configurar o tempo:**
   Altere `INITIAL_TIME` no arquivo `config.py` para definir o tempo inicial em segundos.

3. **Testar componentes (recomendado):**
```bash
sudo python3 test_components.py
```

4. **Executar:**
```bash
sudo python3 bomb.py
```

**Nota:** O `sudo` pode ser necessário para acessar os GPIOs.

## ✨ Funcionalidades

- ⏱️ Timer regressivo configurável
- 🔢 Entrada de código via teclado matricial 4x3 ou USB
- 💡 LEDs piscando durante a contagem
- 📺 Display TFT mostrando tempo e status em tempo real
- 🔔 Alertas sonoros (se buzzer conectado)
- ✅ Desativação ao inserir código correto
- ❌ Explosão simulada se o tempo acabar

## 🔧 Configuração

Todas as configurações estão no arquivo `config.py`:

- `CORRECT_CODE`: Código para desativar (padrão: "1234")
- `INITIAL_TIME`: Tempo inicial em segundos (padrão: 300 = 5 minutos)
- `LED_PINS`: Pins GPIO para os LEDs
- `TFT_PINS`: Pins GPIO para o display TFT
- `KEYPAD_ROWS` e `KEYPAD_COLS`: Pins GPIO para o keypad
- `BUZZER_PIN`: Pin GPIO para o buzzer

## 📁 Estrutura do Projeto

```
AirsoftProject/
├── README.md              # Este arquivo
├── SETUP_RASPBERRY.md     # Guia de configuração inicial da Raspberry Pi
├── HARDWARE_SETUP.md      # Instruções detalhadas de montagem
├── requirements.txt       # Dependências Python
├── install.sh             # Script de instalação automática
├── bomb.py                # Programa principal
├── display.py             # Módulo do display TFT SPI
├── leds.py                # Módulo dos LEDs
├── keypad.py              # Módulo do teclado
├── config.py              # Configurações
└── test_components.py     # Script de teste de componentes
```

## 🧪 Testes

Antes de usar, teste cada componente:

```bash
sudo python3 test_components.py
```

Isso testará:
- LEDs (ligar, desligar, piscar)
- Display TFT (texto, tempo, status)
- Keypad (leitura de teclas)
- Buzzer (se conectado)

## 🐛 Troubleshooting

### Display TFT não funciona
- Verifique se SPI está ativado: `lsmod | grep spi`
- Verifique conexões SPI (MOSI, SCLK, CS, DC, RST)
- Verifique alimentação (VCC e GND)
- Execute: `sudo python3 test_components.py`

### Keypad não responde
- Verifique todas as conexões linha/coluna
- Verifique se os pins estão corretos em `config.py`
- Teste com teclado USB: altere `use_matrix=False` em `bomb.py`

### LEDs não acendem
- Verifique polaridade dos LEDs
- Verifique se os resistores estão conectados
- Teste os GPIOs individualmente

### Permissões GPIO
- Execute com `sudo`: `sudo python3 bomb.py`
- OU adicione usuário ao grupo gpio: `sudo usermod -a -G gpio pi`

## 📚 Documentação Adicional

- **`SETUP_RASPBERRY.md`**: Guia completo para configurar a Raspberry Pi do zero
- **`HARDWARE_SETUP.md`**: Diagramas e instruções detalhadas de montagem
- **`config.py`**: Todas as configurações do projeto

## 🔒 Segurança

- O código correto pode ser configurado em `config.py`
- O timer pode ser pausado durante a entrada do código
- Todos os componentes são seguros e de baixa voltagem
- ⚠️ **NUNCA** use este projeto de forma a causar alarme em locais públicos

## 📝 Notas Técnicas

- **Display:** TFT SPI 240x320 com controlador ST7789
- **Keypad:** Matricial 4x3 (12 teclas) ou USB
- **Interface:** SPI para display, GPIO para keypad e LEDs
- **Python:** Requer Python 3.6+
- **Bibliotecas:** RPi.GPIO, Pillow, spidev

## 🎯 Checklist de Instalação

- [ ] Raspberry Pi configurada com sistema operativo
- [ ] SPI ativado via `raspi-config`
- [ ] Script `install.sh` executado com sucesso
- [ ] Sistema reiniciado (se necessário)
- [ ] Hardware montado conforme `HARDWARE_SETUP.md`
- [ ] Componentes testados com `test_components.py`
- [ ] Configurações ajustadas em `config.py`
- [ ] Projeto executado com sucesso: `sudo python3 bomb.py`

## 📞 Suporte

Se encontrar problemas:
1. Verifique `HARDWARE_SETUP.md` para conexões
2. Execute `test_components.py` para testar individualmente
3. Verifique logs de erro no terminal
4. Verifique se todos os pins estão corretos em `config.py`

## 📄 Licença

Este projeto é apenas para fins educacionais e de entretenimento.

---

**Desenvolvido para jogos de airsoft - Use com responsabilidade! 🎮**
