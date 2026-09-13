# Dados de terreno e elevação

O QGC4QGIS disponibiliza a obtenção automática de dados de elevação do terreno (DEM/DTM) diretamente de serviços web. Isso permite planejar missões com acompanhamento de relevo (*Terrain Following*) sem a necessidade de carregar previamente arquivos raster locais.

---

## Fonte dos dados e consistência com o QGroundControl

- **Fonte de dados**: Copernicus DEM GLO-30 (resolução espacial global de ~30 metros / 1 segundo de arco).
- **Endpoint do serviço**: Serviço web REST da Auterion (`terrain-ce.suite.auterion.com/api/v1/carpet`).
- **Consistência com o QGroundControl**: O Copernicus DEM via Auterion é exatamente a mesma fonte de elevação e API utilizada nativamente pelo QGroundControl (conforme definido em `ElevationMapProvider.h`). As altitudes de terreno amostradas nos arquivos `.plan` exportados correspondem às que o QGC consulta e recalcula internamente.

---

## Como utilizar dados de elevação no QGIS

Você pode baixar dados de elevação para a área da sua missão através de duas interfaces no QGIS:

### 1. Painel Acoplável (Dock Widget)

1. Abra o painel **QGC4QGIS**.
2. Na seção **Terreno**, clique em **Baixar DEM da área…**.
3. O plugin calcula a caixa delimitadora da área da missão (incluindo a margem de segurança), baixa o GeoTIFF do Copernicus DEM e o adiciona automaticamente como camada raster no projeto QGIS.

### 2. Caixa de Ferramentas de Processamento (Processing Toolbox)

- Utilize o algoritmo `qgc4qgis:baixar_dem_copernicus` (`Baixar DEM Copernicus`).
- Parâmetros:
  - **Área de cobertura / Extensão**: Polígono de camada vetorial ou caixa delimitadora geográfica personalizada.
  - **Margem (metros)**: Raio de margem extra ao redor da área.
  - **GeoTIFF de Saída**: Caminho de arquivo onde o raster baixado será salvo.

---

## Parâmetro de margem de segurança

O parâmetro **Margem** expande a caixa delimitadora solicitada ao redor da área da missão.

### Por que a margem é importante

- **Áreas de turnaround**: Curvas de manobra e zonas de aceleração/desaceleração (*turnarounds*) estendem-se além do perímetro principal do polígono.
- **Decolagem e aproximação**: Garante a cobertura de elevação para o ponto de decolagem e a trajetória de aproximação inicial até o primeiro waypoint.

---

## Limitações e restrições da API

- **Resolução espacial**: Resolução nominal de ~30 metros (1 segundo de arco).
- **Conexão com a internet**: Requer acesso ativo à rede durante o download dos ladrilhos (*tiles*).
- **Teto de ladrilhos por requisição**: O servidor limita requisições individuais ao máximo de **256 ladrilhos (*tiles*)**, correspondendo a uma caixa delimitadora de aproximadamente **$18 \times 18\text{ km}$**. Requisições que excedem este tamanho são recusadas pelo servidor.

---

## Atribuição obrigatória de direitos autorais

!!! important "Atribuição Obrigatória"
    Conforme os termos de uso do provedor, a utilização dos dados do Copernicus
    DEM GLO-30 exige a exibição da seguinte atribuição de direitos autorais:
    **© Airbus Defence and Space GmbH**

---

## Referencial de altitude (Geoide EGM2008)

!!! note "Convenção de Altitude Ortométrica"
    As alturas fornecidas pelo Copernicus DEM são **ortométricas** (referenciadas ao modelo geoidal **EGM2008** — altitude acima do nível médio do mar). Isso segue exatamente a mesma convenção adotada pelo QGroundControl. **Não confunda altitudes ortométricas com alturas elipsoidais** obtidas diretamente de receptores GNSS/GPS sem a aplicação do modelo geoidal.

---

## Compatibilidade com NumPy

O download de dados DEM **não requer NumPy**, operando diretamente via Python e bindings nativos da GDAL.

- **Import tardio da GDAL (lazy import)**: Os bindings da GDAL são importados apenas no momento da gravação do arquivo raster.
- **Sem dependência de `osgeo.gdal_array`**: O plugin evita importar `osgeo.gdal_array` (que possui link com extensões binárias do NumPy).
- **Compatível com QGIS 4 & NumPy 2.x**: Nenhum caminho do plugin carrega NumPy durante o carregamento ou download do DEM. Isso previne falhas de interface binária em ambientes com NumPy 2.x (como o QGIS 4), mesmo quando os bindings GDAL do sistema foram compilados contra o NumPy 1.x.

---

## Problemas conhecidos e solução de problemas

### 1. Aviso "A module that was compiled using NumPy 1.x…" no log

Se o aviso *"A module that was compiled using NumPy 1.x..."* aparecer no painel **Mensagens de Log** do QGIS enquanto o DEM baixa e carrega normalmente, isso indica que outro componente do ambiente importou uma extensão legada do NumPy 1.x. O download do DEM é concluído com sucesso.

### 2. Diálogo "A module that was compiled using NumPy 1.x…" na instalação

Se um diálogo com esse aviso aparecer ao instalar o complemento (comum em instalações QGIS via Flatpak):

- **Causa raiz**: Um pacote `numpy` 2.x secundário instalado via `pip` em `/var/data/python/...` sombreia os binários do runtime.
- **Solução**: Remova o pacote instalado via `pip` em `/var/data/python/...` no Flatpak para que o QGIS volte a usar os binários pareados do runtime. Não faça downgrade do NumPy do sistema.
