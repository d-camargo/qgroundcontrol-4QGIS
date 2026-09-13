# Histórico de alterações

## 0.7.1

Compatibilidade total com Qt6 e QGIS 4.x — todos os enums Qt/QGIS com escopo explícito, corrigindo os 106 apontamentos da checagem Qt6 do plugins.qgis.org na 0.7.0; tipos de campo construídos por versão do Qt (QVariant.Type no Qt5, QMetaType.Type no Qt6); asserts de produção substituídos por guardas de entrada; guarda estática de regressão para enums Qt6.

## 0.7.0

Strings fonte em inglês com tradução para português do Brasil (i18n/qgc4qgis_pt_BR.qm) — a interface permanece em português para locales pt-BR. A entrada de câmera customizada agora é "Custom camera (manual)": uma configuração de câmera salva com o nome antigo reverte para a primeira câmera da lista.

## 0.6.3

Falhas de exportação, geração de grade de mapeamento e download de DEM agora são registradas no log do QGIS em vez de serem silenciadas; geração de XML (.kml/.kmz) sem o parser XML da biblioteca padrão. Nenhuma alteração nos arquivos exportados.

## 0.6.2

A gravação de DEM não carrega mais os bindings GDAL NumPy (osgeo.gdal_array) — elimina o aviso "module compiled using NumPy 1.x" no log durante o download de DEM.

## 0.6.1

O carregamento do complemento não importa mais os bindings da GDAL (importação tardia no momento da gravação do DEM) — a instalação fica imune a ambientes com NumPy 2.x onde o gdal_array foi compilado contra o NumPy 1.x; diagnóstico do diálogo de instalação do NumPy adicionado ao README.

## 0.6.0

Compatibilidade declarada com QGIS 4.x (qgisMaximumVersion=4.99); download de DEM não depende mais do NumPy — corrige o erro "module compiled using NumPy 1.x" em ambientes QGIS 4 com NumPy 2.x.

## 0.5.0

Download automático do Copernicus DEM (a mesma fonte de elevação usada pelo QGroundControl) para a área de interesse, já carregado e selecionado no projeto.

## 0.4.0

Exportação .kml para o Litchi Mission Hub clássico (flylitchi.com/hub), compatível com a opção "Add take photo action"; o exportador .csv agora avisa quando o modo de disparo não gera uma ação de foto por waypoint.

## 0.3.0

Exportação WPML (.kmz) em modo terreno, convertida para altitude relativa ao ponto de decolagem; template.kml completo com Folder de waypoints e ponto de decolagem; o mesmo .kmz é importado pelo Litchi Hub 2.

## 0.2.1

O painel de planejamento agora rola verticalmente — todo o conteúdo fica acessível em telas menores.

## 0.2.0

Versão atualizada para 0.2.0 e metadados completos adicionados para o repositório oficial do QGIS.
