#!/bin/bash
# Script de instalação para a bomba simulada de airsoft

echo "=========================================="
echo "Instalação da Bomba Simulada para Airsoft"
echo "=========================================="
echo ""

# Verificar se está rodando no Raspberry Pi
if [ ! -d "/sys/class/gpio" ]; then
    echo "AVISO: Este script deve ser executado em um Raspberry Pi!"
    read -p "Continuar mesmo assim? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Atualizar sistema
echo "Atualizando sistema..."
sudo apt-get update

# Instalar dependências do sistema
echo "Instalando dependências do sistema..."
sudo apt-get install -y python3-pip python3-dev python3-spidev python3-pil python3-numpy

# Ativar SPI (necessário para display TFT)
echo "Ativando SPI..."
if ! grep -q "dtparam=spi=on" /boot/config.txt; then
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
    echo "SPI adicionado ao config.txt. Reinicie o sistema após a instalação."
    NEEDS_REBOOT=1
fi

# Ativar I2C (opcional, para outros componentes)
echo "Ativando I2C (opcional)..."
if ! grep -q "dtparam=i2c_arm=on" /boot/config.txt; then
    echo "dtparam=i2c_arm=on" | sudo tee -a /boot/config.txt
    echo "I2C adicionado ao config.txt."
    NEEDS_REBOOT=1
fi

# Instalar dependências Python
echo "Instalando dependências Python..."
pip3 install --user -r requirements.txt

# Tornar os scripts executáveis
chmod +x bomb.py
chmod +x test_components.py

echo ""
echo "=========================================="
echo "Instalação concluída!"
echo "=========================================="
echo ""

if [ "$NEEDS_REBOOT" = "1" ]; then
    echo "⚠️  IMPORTANTE: SPI ou I2C foram ativados."
    echo "   Você PRECISA reiniciar o sistema antes de usar:"
    echo "   sudo reboot"
    echo ""
fi

echo "Próximos passos:"
echo "1. Monte o hardware conforme HARDWARE_SETUP.md"
echo "2. Configure o código e tempo em config.py"
echo "3. Teste os componentes: sudo python3 test_components.py"
echo "4. Execute: sudo python3 bomb.py"
echo ""
