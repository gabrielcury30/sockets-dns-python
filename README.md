# Cliente DNS em Python

Um cliente DNS implementado do zero em Python utilizando sockets UDP e o módulo `struct`, sem dependências externas. Este projeto demonstra na prática como funcionam os mecanismos internos de resolução de nomes na Internet.

## 🎯 Objetivo

Implementar um cliente DNS que seja capaz de:

- Construir pacotes DNS válidos conforme a RFC 1035
- Enviar consultas para servidores DNS via UDP
- Receber e decodificar respostas DNS
- Suportar consultas dos tipos A (IPv4) e AAAA (IPv6)

## 📋 Requisitos

- **Python 3.6+**
- Nenhuma dependência externa (apenas bibliotecas padrão)

## 🚀 Como Usar

### Instalação

```bash
git clone https://github.com/gabrielcury30/sockets-dns-python.git
cd sockets-dns-python
```

### Execução

A sintaxe básica é:

```bash
python3 dns.py --type=<TIPO> --name=<DOMINIO> --server=<IP_SERVIDOR>
```

**Parâmetros:**

- `--type`: Tipo de consulta (`A` para IPv4 ou `AAAA` para IPv6)
- `--name`: Nome do domínio a consultar
- `--server`: Endereço IP do servidor DNS

### Exemplos

#### Consultar endereço IPv4 do Google

```bash
python3 dns.py --type=A --name=www.google.com --server=8.8.8.8
```

**Saída esperada:**

```
Server Response
Message ID: 25811
Response code: No error
Counts: Query 1, Answer 1, Authority 0, Additional 0
Question 1:
  Name: www.google.com
  Type: A
  Class: IN
Answer 1:
  Name: 0xc00c
  Type: A, Class: IN, TTL: 130
  RDLength: 4 bytes
  Addr: 142.250.219.4 (IPv4)
```

#### Consultar endereço IPv6 do Google

```bash
python3 dns.py --type=AAAA --name=www.google.com --server=8.8.8.8
```

#### Consultar domínio local ou privado

```bash
python3 dns.py --type=A --name=localhost --server=8.8.8.8
```

#### Usar servidor DNS alternativo

```bash
# Cloudflare DNS
python3 dns.py --type=A --name=example.com --server=1.1.1.1

# Quad9 DNS
python3 dns.py --type=A --name=example.com --server=9.9.9.9
```

## 📁 Estrutura do Projeto

```
sockets-dns-python/
├── dns.py              # Cliente DNS principal (implementado)
├── dns_tools.py        # Módulo de decodificação de respostas
├── README.md           # Este arquivo
└── .gitignore          # Configuração do Git
```

## 🔧 Componentes Principais

### dns.py

**Função `encode_qname(domain_name)`**

- Codifica um nome de domínio no formato de rótulos DNS
- Exemplo: `www.google.com` → `\x03www\x06google\x03com\x00`
- Cada rótulo é prefixado com seu comprimento em bytes

**Função `build_dns_query(qname, qtype)`**

- Constrói um pacote DNS completo seguindo RFC 1035
- **Cabeçalho (12 bytes):**
  - ID: Identificador aleatório de 16 bits
  - Flags: 0x0100 (Consulta padrão com recursão desejada)
  - Contadores: QDCOUNT=1, ANCOUNT=0, NSCOUNT=0, ARCOUNT=0
- **Seção de Pergunta:**
  - QNAME: Nome codificado
  - QTYPE: 1 para A, 28 para AAAA
  - QCLASS: 1 para IN (Internet)

**Função `main()`**

- Orquestra o fluxo completo: parse de argumentos, criação de socket, envio de consulta, recepção de resposta

### dns_tools.py

Fornece a classe `DNS` com método estático:

**`DNS.decode_dns(raw_bytes)`**

- Decodifica pacotes DNS binários
- Exibe informações de cabeçalho, perguntas e respostas
- Converte IPs binários para notação legível

## 🌐 Servidores DNS Públicos Recomendados

| Provedor   | IPv4           |
| ---------- | -------------- |
| Google     | 8.8.8.8        |
| Cloudflare | 1.1.1.1        |
| Quad9      | 9.9.9.9        |
| OpenDNS    | 208.67.222.123 |

## 📚 Entendendo o DNS

### Tipos de Registros Suportados

- **A**: Endereço IPv4 (32 bits)
- **AAAA**: Endereço IPv6 (128 bits)
- **CNAME**: Alias canônico para outro domínio
- **NS**: Servidor de nomes
- **MX**: Servidor de correio eletrônico

### Byte Order (Endianness)

O protocolo DNS utiliza **network byte order** (big-endian). Isso é garantido no código através do prefixo `!` na função `struct.pack()`:

```python
struct.pack('!HHHHHH', id, flags, qdcount, ancount, nscount, arcount)
```

### TTL (Time To Live)

Indica por quanto tempo (em segundos) a resposta pode ser cacheada antes de solicitar novamente ao servidor.

## 🔍 Investigando Respostas DNS

### Quando não há resposta para www.dominio.br mas há para dominio.br

Isso ocorre quando o domínio raiz (`dominio.br`) possui um registro A/AAAA direto, mas o subdomínio (`www.dominio.br`) está configurado como um **CNAME** (alias) para outro host. Exemplo:

```bash
# Retorna IP direto
python3 dns.py --type=A --name=ufba.br --server=8.8.8.8
# Addr: 200.128.56.88

# Retorna CNAME em vez de IP
python3 dns.py --type=A --name=www.ufba.br --server=8.8.8.8
# Type: CNAME (precisa seguir o alias para obter o IP)
```

Essa é uma prática comum em infraestruturas que utilizam CDNs ou load balancers.

## ⚙️ Tratamento de Erros

O programa trata os seguintes cenários:

- **Tipo de consulta inválido**: Valida se é "A" ou "AAAA"
- **Timeout de socket**: Timeout padrão de 5 segundos
- **Erro ao enviar**: Captura erros de comunicação de saída
- **Erro ao receber**: Captura erros de comunicação de entrada
- **Servidor inacessível**: Retorna mensagem de erro apropriada

## 📖 Referências Acadêmicas

- **RFC 1035** - Domain Names - Implementation and Specification
- **RFC 3596** - DNS Extensions to Support Protocol Version 6 (IPv6)
- Python Documentation - [socket module](https://docs.python.org/3/library/socket.html)
- Python Documentation - [struct module](https://docs.python.org/3/library/struct.html)

## 📝 Extensões Futuras

Possíveis melhorias e funcionalidades a implementar:

- [ ] Seguimento automático de CNAMEs para obter IP final
- [ ] Cache de respostas DNS
- [ ] Suporte para mais tipos de registros (MX, NS, SOA, etc.)
- [ ] Interface gráfica
- [ ] Resolução reversa (DNS reverso)
- [ ] Suporte para DNSSEC
- [ ] Busca iterativa (implementar resolvedor recursivo completo)

## 🧪 Testes e Validação

O código foi testado com sucesso contra:

- Google Public DNS (8.8.8.8)
- Cloudflare DNS (1.1.1.1)
- Servidores DNS locais
- Domínios públicos (google.com, github.com, ufba.br)

## 📄 Licença

Este projeto é fornecido como trabalho acadêmico e está disponível para fins educacionais.

## 👤 Autor

Desenvolvido como trabalho da disciplina de Redes de Computadores.

---

**Dúvidas ou sugestões?** Abra uma issue ou entre em contato!
