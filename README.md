# api-modelo
Api em Flask *Python 3.8* com intenção de ser escalável, estrutura pensada para seguir um padrão *Domain Drive Design*.

### Execução Docker:
O repositório possui um ambiente Docker pronto para levantar o ambiente necessário, localmente. 

Para levantar o ambiente é necessário:
- Adicionar um arquivo *.env* baseado no arquivo *.env_example*.

#### run:
`$ docker-compose up`

---

### Execução Local:
Aconselhamos que seja utilizado o Docker para testes, mas se desejar executar a api em seu ambiente local, você poderá efetuar os seguintes passos:
- Crie o seu próprio *virutalenv* baseado no python 3.8
- Instale as dependências contidas no arquivo *requirements.txt*
- Registre as variáveis do arquivo *.env_example* junto ao seu *virtualenv*

#### run:
`$(venv) flask run`

---

## #TODO:
- [ ] Adicionar execução através de script uWSGI.
- [ ] Renomear o domínio de teste 'File' para algo mais intuitivo.
- [ ] Adicionar driver MongoDB em "app/core".
- [ ] Adicionar driver Mysql em "app/core".
- [ ] Adicionar driver PostgreSQL em "app/core".
- [ ] Adicionar suporte ao Redis em "app/core".

<br>

## Domínios e Bibliotecas:

### Domínio 'File':
O domínio 'File' *(precisamos mudar esse nome)* ,  trabalha manipulando arquivos CSV aplicando um filtro de testes baseado nas regras que poderão ser verificadas mais abaixo.

### *Bibliotecas do domínio:*
- DictReader
- jsonify
- urllib
- HTTPError
- reduce (functools)
- datetime

<br>

### *Endpoints:*

---

#### /main - [GET]:
Testar se a rota do domínio está respondendo de acordo, executando no *Controller* do domínio *File*, a função *mainPage()*.

<br>

***Resposta:***
```json
{
  "message": "Main Success",
  "status": 200
}
```

---

#### /checkCsv - [POST]:
Recebe um conteúdo do tipo *Multipart Form Data*  contendo um arquivo csv e executa uma bateria de testes, antes de consultar cada linha junto a uma API externa de blacklists *(ver regras mais abaixo).*

<br>

***Exemplo de Arquivo de Entrada:***
O arquivo *file-example.csv* contido no repositório, poderá ser utilizado para testes.

```csv
IDMENSAGEM;DDD;CELULAR;OPERADORA;HORARIO_ENVIO;MENSAGEM
bff58d7b-8b4a-456a-b852-5a3e000c0e63;2;996958849;NEXTEL;21:24:03;sapien sapien non mi integer ac neque duis bibendum
b7e2af69-ce52-4812-adf1-395c8875ad30;69;949360612;CLARO;19:05:21;justo lacinia eget tincidunt eget
e7b87f43-9aa8-8b62-9cec-f28e653ac25e;34;990171682;VIVO;18:35:20;dui luctus rutrum nulla tellus in sagittis dui
66sr7f43-43fx-414b-0poi-knjsd87j4843;34;990171682;VIVO;18:35:19;dui in sagittis dui
```

<br>

***Resposta:***
```json
[
  "66sr7f43-43fx-414b-0poi-knjsd87j4843;1",
  "d81b2696-8b62-4b8b-af82-586ce0875ebc;1",
  "qwe8byy7-3j6k-8x5k-0ut5-jk2h34mfk34h;2"
]
```

---

#### /checkCsvFast - [POST]:
Recebe um conteúdo do tipo *Multipart Form Data*  contendo um arquivo csv e executa uma bateria de testes *(ver regras mais abaixo)* junto a uma *blacklist*  baixada de uma API externa.

<br>

***Exemplo de Arquivo de Entrada:***
O arquivo *file-example.csv* contido no repositório, poderá ser utilizado para testes.

```csv
IDMENSAGEM;DDD;CELULAR;OPERADORA;HORARIO_ENVIO;MENSAGEM
bff58d7b-8b4a-456a-b852-5a3e000c0e63;2;996958849;NEXTEL;21:24:03;sapien sapien non mi integer ac neque duis bibendum
b7e2af69-ce52-4812-adf1-395c8875ad30;69;949360612;CLARO;19:05:21;justo lacinia eget tincidunt eget
e7b87f43-9aa8-8b62-9cec-f28e653ac25e;34;990171682;VIVO;18:35:20;dui luctus rutrum nulla tellus in sagittis dui
66sr7f43-43fx-414b-0poi-knjsd87j4843;34;990171682;VIVO;18:35:19;dui in sagittis dui
```

<br>

***Resposta:***
```json
[
  "66sr7f43-43fx-414b-0poi-knjsd87j4843;1",
  "d81b2696-8b62-4b8b-af82-586ce0875ebc;1",
  "qwe8byy7-3j6k-8x5k-0ut5-jk2h34mfk34h;2"
]
```

---

### *Regras:*

* mensagens com telefone inválido deverão ser bloqueadas(DDD+NUMERO);
* mensagens que estão na _blacklist_ deverão ser bloqueadas; _(ver blacklist)_
* mensagens para o estado de São Paulo deverão ser bloqueadas;
* mensagens com agendamento após as 19:59:59 deverão ser bloqueadas;
* as mensagens com mais de 140 caracteres deverão ser bloqueadas;
* caso possua mais de uma mensagem para o mesmo destino, apenas a mensagem apta com o menor horário deve ser considerada;
* o id_broker será definido conforme a operadora; _(ver broker x operadora)_

#### Broker de envio

Cada broker será responsável pelo envio de algumas operadoras, representado pela tabela abaixo:

| ID_BROKER | OPERADORAS |
|-----------|------------|
|   1       |  VIVO, TIM |
|   2       |  CLARO, OI |
|   3       |  NEXTEL    |

#### Consulta de blacklist

```
https://front-test-pg.herokuapp.com/blacklist/:phone
```
Possíveis retornos:
* Se retornar 200, está na blacklist.
* Se retornar 404 não está na blacklist.

#### Número de telefone celular válido

```
 DDD + CELULAR
```
* DDD com 2 digitos;
* DDD deve ser válido;
* número celular deve conter 9 dígitos;
* numero celular deve começar com 9;
* o segundo dígito deve ser > 6;

Exemplos:

* 41987563653 - ok
* **00**987563653 - nok
* 419**2**7563653 - nok
* 41**8**87563653 - nok

---
