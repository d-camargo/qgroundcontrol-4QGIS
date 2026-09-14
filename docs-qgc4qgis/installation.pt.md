# Instalação

## Requisitos

- **QGIS**: versão 3.34 a 4.x (`qgisMinimumVersion=3.34`, `qgisMaximumVersion=4.99`).
- **Qt**: suporte a Qt5 e Qt6 (`supportsQt6=True`).
- **Python**: 3.9 ou superior, já incluído nas distribuições standard do QGIS.

## Métodos de instalação

### Método A: Repositório de plugins do QGIS (recomendado)

1. No QGIS, acesse o menu **Complementos** (*Plugins*) → **Gerenciar e
   Instalar Complementos...** (*Manage and Install Plugins...*).
2. Abra a aba **Todos** (*All*) e busque por **QGC4QGIS**.
3. Clique em **Instalar complemento** (*Install Plugin*).

O plugin está publicado em <https://plugins.qgis.org/plugins/qgc4qgis/> com o
selo **QGIS 4 Ready**.

### Método B: ZIP da release do GitHub

1. Baixe `qgc4qgis.<versão>.zip` em
   <https://github.com/d-camargo/qgroundcontrol-4QGIS/releases/latest>.
2. No QGIS, acesse o menu **Complementos** (*Plugins*) → **Gerenciar e
   Instalar Complementos...** (*Manage and Install Plugins...*).
3. Selecione a aba **Instalar a partir do ZIP** (*Install from ZIP*).
4. Selecione o arquivo `.zip` baixado e clique em **Instalar complemento**.

### Método C: symlink (desenvolvimento)

Copie ou crie um link simbólico da pasta `qgc4qgis` no diretório de plugins
do seu perfil do QGIS:

- **Linux**:

  ```bash
  mkdir -p ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins
  ln -s /caminho/para/qgroundcontrol-4qgis/qgc4qgis ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/qgc4qgis
  ```

- **Windows**:

  ```text
  %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\qgc4qgis
  ```

- **macOS**:

  ```bash
  ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/qgc4qgis
  ```

Compactar a pasta `qgc4qgis` em um arquivo `.zip` serve para testar um ZIP
antes da release, pela aba **Instalar a partir do ZIP**.

## Ativação

Após copiar ou instalar o arquivo, abra o QGIS, acesse o menu
**Complementos** → **Gerenciar e Instalar Complementos...**, localize
**QGC4QGIS** na lista e marque a caixa de seleção para ativá-lo.

## Compatibilidade com NumPy

!!! note "Nenhum caminho do plugin carrega NumPy"
    O download do DEM não requer NumPy: ele opera diretamente via Python e
    bindings nativos da GDAL. Desde a versão 0.6.1, o plugin não importa os
    bindings GDAL ao ser carregado (import tardio, apenas no momento de
    gravar o DEM). A partir da versão 0.6.2, o plugin também não habilita as
    exceções da GDAL pela via que importa `osgeo.gdal_array` (binário
    linkado ao NumPy). Desta forma, nenhum caminho do plugin (carregamento
    ou download do DEM) carrega NumPy, garantindo a operação sem conflitos
    em ambientes com NumPy 2.x (como o QGIS 4), mesmo quando os bindings
    GDAL do ambiente foram compilados com NumPy 1.x.

!!! warning "Diagnóstico: mensagem NumPy 1.x"
    - **Aviso "A module that was compiled using NumPy 1.x…" no log durante
      o download do DEM**: se o traceback aparecer no log do QGIS como
      `WARNING` enquanto o DEM baixa e carrega normalmente, trata-se de
      uma extensão C compilada contra NumPy 1.x sendo importada por outro
      componente do ambiente e imprimindo o aviso — a operação não falha.
    - **Diálogo "A module that was compiled using NumPy 1.x…" ao
      instalar**: se o diálogo aparecer ao instalar o complemento, a
      origem é outro componente do Python do QGIS — típico do QGIS em
      Flatpak com `numpy` 2.x instalado via `pip` em
      `/var/data/python/...`, que sombreia o `numpy` do runtime e quebra
      extensões compiladas contra o `numpy` antigo.
      - **Correção de ambiente**: remover esse `numpy` instalado via `pip`
        em `/var/data/python/...` no Flatpak (o runtime volta a usar o
        `numpy` casado com seus binários), em vez de fazer downgrade do
        NumPy.
