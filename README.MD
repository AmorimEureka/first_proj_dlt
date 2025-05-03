

Projeto Teste de Viabilidade de Implantação DLT como Stack de EL
=============



<br>
<br>

<details open>
    <summary>
        <strong>Criar Path Repositório</strong>
    </summary>

<br>

- Criar diretório para o repositório:

``` sh
mkdir first_proj
```

<br>

- Acessar repositório:

``` sh
cd first_proj
```

</details>

---

<br>
<br>

<details open>
    <summary>
        <strong>Criando Ambiente Virtual</strong>
    </summary>

<br>

- Iniciando Ambiente Virtual


``` python
python -m venv .venv
```

<br>

- Ativando Ambiente Virtual


``` python
source ./.venv/bin/activate
```

<br>

- Desativando Ambiente Virtual


``` python
deactivate
```

</details>

---

<br>
<br>

<details open>
    <summary>
        <strong>Definindo Versão Python - pyenv</strong>
    </summary>

<br>

- Instalação e Configuração `pyenv`

<br>

- Definindo Versão Python Global

<br>

- Definindo Versão Python do Repo Local

</details>

---

<br>
<br>


<details open>
    <summary>
        <strong>Iniciando Versionamento - Git</strong>
    </summary>

<br>

- Configurando Conexão ssh


<br>

- Iniciando Repositório

``` sh
git init
```


<br>

- Clonando Repositório Remoto


```sh
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```

<br>

- Criando `.gitignore`

``` sh
cat >> requirements.txt
.venv
ctrl+c
```


<br>


- Primeiro Commit

``` sh
git commit -m"Primeito Commit"
```

<br>

- Criando *requirements.txt*


``` python
pip freeze >> requirements.txt
```


</details>

---

<br>
<br>