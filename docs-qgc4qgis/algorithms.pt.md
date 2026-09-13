# Referência dos algoritmos do Processing

O plugin QGC4QGIS integra-se diretamente à **Caixa de Ferramentas de Processamento do QGIS** (Processing Toolbox) sob o provedor `QGC4QGIS`. Isso permite automatizar o planejamento de voos fotogramétricos, geração de centros de foto, download de DEMs e exportações de missões em múltiplos formatos através do Modelador Gráfico do QGIS, scripts Python (`pyqgis`) e rotinas em lote.

---

## Visão geral do provedor

- **ID do Provedor**: `qgc4qgis`
- **Nome do Provedor**: `QGC4QGIS`
- **Grupo de Algoritmos**: `Planejamento de Voo` (`planejamento_voo`)

Abaixo está a referência completa dos 7 algoritmos registrados pelo provedor `qgc4qgis`.

---

## 1. Gerar grade de voo

- **ID completo do algoritmo**: `qgc4qgis:gerar_grade_voo`
- **Nome de exibição**: Gerar grade de voo
- **Grupo**: Planejamento de Voo (`planejamento_voo`)

### Descrição

Gera linhas de grade de voo fotogramétrico a partir de uma camada de polígonos, configurações de câmera, altitude ou GSD, sobreposições, ângulo da grade, distância de manobra e canto de entrada.

### Entradas e Saídas

| Parâmetro (Interface) | Identificador | Direção | Descrição |
| :--- | :--- | :--- | :--- |
| Camada de polígonos | `INPUT` | Entrada | Camada vetorial de polígonos que define a área do levantamento. |
| Câmera | `CAMERA` | Entrada | Perfil de câmera selecionado no banco de dados (ou especificação manual). |
| Altitude de voo (m) | `ALTITUDE` | Entrada | Altitude de voo em metros acima do solo/decolagem (padrão: 100.0 m). |
| GSD (cm/px) - se > 0, se sobrepõe/calcula a altitude | `GSD` | Entrada | Resolução no solo em cm/px. Se > 0, calcula e substitui a altitude automaticamente. |
| Sobreposição lateral (%) | `OVERLAP_SIDE` | Entrada | Porcentagem de sobreposição lateral entre faixas de voo (0–99%, padrão: 70.0%). |
| Sobreposição frontal (%) | `OVERLAP_FRONTAL` | Entrada | Porcentagem de sobreposição frontal ao longo das faixas (0–99%, padrão: 70.0%). |
| Ângulo da grade (graus) | `ANGLE` | Entrada | Ângulo de orientação das faixas de voo em graus (-180° a 180°, padrão: 0.0°). |
| Distância de manobra (m) | `TURNAROUND` | Entrada | Extensão adicional das linhas fora do polígono em metros para manobra da aeronave. |
| Ponto de entrada | `ENTRY_LOCATION` | Entrada | Canto inicial da grade (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Grade cruzada (Re-voo 90°) | `REFLY` | Entrada | Ativa uma segunda passagem de grade perpendicular (90°) para voo de grade dupla. |
| Câmera manual: Largura do sensor (mm) | `SENSOR_WIDTH` | Entrada | Largura do sensor em mm (opcional, usado se `CAMERA` for câmera manual). |
| Câmera manual: Altura do sensor (mm) | `SENSOR_HEIGHT` | Entrada | Altura do sensor em mm (opcional, usado se `CAMERA` for câmera manual). |
| Câmera manual: Largura da imagem (px) | `IMAGE_WIDTH` | Entrada | Largura da imagem em pixels (opcional, usado se `CAMERA` for câmera manual). |
| Câmera manual: Altura da imagem (px) | `IMAGE_HEIGHT` | Entrada | Altura da imagem em pixels (opcional, usado se `CAMERA` for câmera manual). |
| Câmera manual: Distância focal (mm) | `FOCAL_LENGTH` | Entrada | Distância focal da lente em mm (opcional, usado se `CAMERA` for câmera manual). |
| Grade de voo (Linhas) | `OUTPUT` | Saída | Camada vetorial de linhas resultante contendo as faixas de voo geradas. |

---

## 2. Gerar centros de foto e pegadas

- **ID completo do algoritmo**: `qgc4qgis:gerar_centros_foto`
- **Nome de exibição**: Gerar centros de foto e pegadas
- **Grupo**: Planejamento de Voo (`planejamento_voo`)

### Descrição

Gera camadas de pontos com as posições dos centros de disparo das fotos e polígonos de pegada no solo (*footprints*), orientados pelo azimute das faixas de voo. Aceita camadas de polígonos ou faixas de voo em linha.

### Entradas e Saídas

| Parâmetro (Interface) | Identificador | Direção | Descrição |
| :--- | :--- | :--- | :--- |
| Camada de entrada (Polígonos ou Linhas) | `INPUT` | Entrada | Camada vetorial de polígonos da área ou linhas de grade de voo. |
| Câmera | `CAMERA` | Entrada | Perfil de câmera selecionado no banco de dados (ou especificação manual). |
| Altitude de voo (m) | `ALTITUDE` | Entrada | Altitude de voo em metros (padrão: 100.0 m). |
| GSD (cm/px) - se > 0, se sobrepõe/calcula a altitude | `GSD` | Entrada | Resolução no solo em cm/px (calcula/substitui altitude se > 0). |
| Sobreposição lateral (%) | `OVERLAP_SIDE` | Entrada | Porcentagem de sobreposição lateral entre faixas (padrão: 70.0%). |
| Sobreposição frontal (%) | `OVERLAP_FRONTAL` | Entrada | Porcentagem de sobreposição frontal ao longo das faixas (padrão: 70.0%). |
| Ângulo da grade (graus) | `ANGLE` | Entrada | Ângulo de orientação das faixas em graus (padrão: 0.0°). |
| Distância de manobra (m) | `TURNAROUND` | Entrada | Extensão das linhas para manobra em metros. |
| Ponto de entrada | `ENTRY_LOCATION` | Entrada | Canto inicial da grade (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Grade cruzada (Re-voo 90°) | `REFLY` | Entrada | Ativa passagem adicional de grade perpendicular (90°). |
| Câmera manual: Largura do sensor (mm) | `SENSOR_WIDTH` | Entrada | Largura do sensor manual em mm (opcional). |
| Câmera manual: Altura do sensor (mm) | `SENSOR_HEIGHT` | Entrada | Altura do sensor manual em mm (opcional). |
| Câmera manual: Largura da imagem (px) | `IMAGE_WIDTH` | Entrada | Largura da imagem manual em pixels (opcional). |
| Câmera manual: Altura da imagem (px) | `IMAGE_HEIGHT` | Entrada | Altura da imagem manual em pixels (opcional). |
| Câmera manual: Distância focal (mm) | `FOCAL_LENGTH` | Entrada | Distância focal manual em mm (opcional). |
| Centros de foto (Pontos) | `OUTPUT_CENTERS` | Saída | Camada vetorial de pontos resultante com a posição de disparo das fotos. |
| Pegadas das fotos (Polígonos) | `OUTPUT_FOOTPRINTS` | Saída | Camada vetorial de polígonos resultante com a pegada de cobertura no solo. |

---

## 3. Exportar plano QGC (.plan)

- **ID completo do algoritmo**: `qgc4qgis:exportar_plano_qgc`
- **Nome de exibição**: Exportar plano QGC (.plan)
- **Grupo**: Planejamento de Voo (`planejamento_voo`)

### Descrição

Exporta um plano de missão completo no formato nativo do QGroundControl (`.plan`) a partir de polígonos de cobertura ou linhas de voo, com suporte a modelos de elevação raster (DEM) para acompanhamento de terreno.

### Entradas e Saídas

| Parâmetro (Interface) | Identificador | Direção | Descrição |
| :--- | :--- | :--- | :--- |
| Camada de entrada (Polígonos ou Linhas) | `INPUT` | Entrada | Camada vetorial de polígonos da área ou linhas de grade. |
| Câmera | `CAMERA` | Entrada | Perfil de câmera selecionado no banco ou especificação manual. |
| Altitude de voo (m) | `ALTITUDE` | Entrada | Altitude de voo em metros (padrão: 100.0 m). |
| GSD (cm/px) - se > 0, se sobrepõe/calcula a altitude | `GSD` | Entrada | GSD desejado em cm/px (calcula/substitui altitude se > 0). |
| Sobreposição lateral (%) | `OVERLAP_SIDE` | Entrada | Porcentagem de sobreposição lateral entre faixas (padrão: 70.0%). |
| Sobreposição frontal (%) | `OVERLAP_FRONTAL` | Entrada | Porcentagem de sobreposição frontal ao longo das faixas (padrão: 70.0%). |
| Ângulo da grade (graus) | `ANGLE` | Entrada | Ângulo de orientação da grade em graus (padrão: 0.0°). |
| Distância de manobra (m) | `TURNAROUND` | Entrada | Extensão adicional de manobra em metros. |
| Ponto de entrada | `ENTRY_LOCATION` | Entrada | Canto inicial da grade (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Grade cruzada (Re-voo 90°) | `REFLY` | Entrada | Opção para voo de grade dupla cruzada em 90°. |
| Câmera manual: Largura do sensor (mm) | `SENSOR_WIDTH` | Entrada | Largura do sensor manual em mm (opcional). |
| Câmera manual: Altura do sensor (mm) | `SENSOR_HEIGHT` | Entrada | Altura do sensor manual em mm (opcional). |
| Câmera manual: Largura da imagem (px) | `IMAGE_WIDTH` | Entrada | Largura da imagem manual em pixels (opcional). |
| Câmera manual: Altura da imagem (px) | `IMAGE_HEIGHT` | Entrada | Altura da imagem manual em pixels (opcional). |
| Câmera manual: Distância focal (mm) | `FOCAL_LENGTH` | Entrada | Distância focal manual em mm (opcional). |
| Velocidade de cruzeiro (m/s) | `CRUISE_SPEED` | Entrada | Velocidade de voo de cruzeiro em m/s (padrão: 15.0 m/s). |
| Velocidade em pairado (m/s) | `HOVER_SPEED` | Entrada | Velocidade em pairado em m/s (padrão: 5.0 m/s). |
| Tipo de Firmware | `FIRMWARE_TYPE` | Entrada | Firmware do piloto automático alvo (`PX4 (12)` ou `ArduPilot (3)`). |
| Tipo de Veículo | `VEHICLE_TYPE` | Entrada | Tipo de veículo alvo (`Multirotor (2)`, `Fixed Wing (1)`, `VTOL (19)`). |
| Camada de elevação (DEM) — se informada, exporta em modo sobre terreno | `ELEVATION_LAYER` | Entrada | Camada raster DEM opcional para exportação com acompanhamento de terreno. |
| Tolerância do terreno (m) | `TOLERANCE` | Entrada | Tolerância de variação de altitude do terreno em metros (padrão: 10.0 m). |
| Arquivo de saída (.plan) | `OUTPUT` | Saída | Caminho do arquivo de destino para o plano `.plan` gerado. |

---

## 4. Exportar missão Litchi (.csv)

- **ID completo do algoritmo**: `qgc4qgis:exportar_litchi_csv`
- **Nome de exibição**: Exportar missão Litchi (.csv)
- **Grupo**: Planejamento de Voo (`planejamento_voo`)

### Descrição

Exporta uma missão de voo no formato Litchi CSV (`.csv`) a partir de polígonos de cobertura ou linhas de voo. Suporta cálculo de altitude relativa ao terreno quando um DEM é fornecido.

### Entradas e Saídas

| Parâmetro (Interface) | Identificador | Direção | Descrição |
| :--- | :--- | :--- | :--- |
| Camada de entrada (Polígonos ou Linhas) | `INPUT` | Entrada | Camada vetorial de polígonos da área ou linhas de grade. |
| Câmera | `CAMERA` | Entrada | Perfil de câmera selecionado ou manual. |
| Altitude de voo (m) | `ALTITUDE` | Entrada | Altitude nominal de voo em metros (padrão: 100.0 m). |
| GSD (cm/px) - se > 0, se sobrepõe/calcula a altitude | `GSD` | Entrada | GSD desejado em cm/px (calcula/substitui altitude se > 0). |
| Sobreposição lateral (%) | `OVERLAP_SIDE` | Entrada | Porcentagem de sobreposição lateral (padrão: 70.0%). |
| Sobreposição frontal (%) | `OVERLAP_FRONTAL` | Entrada | Porcentagem de sobreposição frontal (padrão: 70.0%). |
| Ângulo da grade (graus) | `ANGLE` | Entrada | Ângulo da grade em graus (padrão: 0.0°). |
| Distância de manobra (m) | `TURNAROUND` | Entrada | Extensão adicional de manobra em metros. |
| Ponto de entrada | `ENTRY_LOCATION` | Entrada | Canto inicial da grade (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Grade cruzada (Re-voo 90°) | `REFLY` | Entrada | Opção para voo de grade dupla cruzada em 90°. |
| Câmera manual: Largura do sensor (mm) | `SENSOR_WIDTH` | Entrada | Largura do sensor manual em mm (opcional). |
| Câmera manual: Altura do sensor (mm) | `SENSOR_HEIGHT` | Entrada | Altura do sensor manual em mm (opcional). |
| Câmera manual: Largura da imagem (px) | `IMAGE_WIDTH` | Entrada | Largura da imagem manual em pixels (opcional). |
| Câmera manual: Altura da imagem (px) | `IMAGE_HEIGHT` | Entrada | Altura da imagem manual em pixels (opcional). |
| Câmera manual: Distância focal (mm) | `FOCAL_LENGTH` | Entrada | Distância focal manual em mm (opcional). |
| Modo de disparo | `TRIGGER_MODE` | Entrada | Mecanismo de disparo das fotos (`Por distância`, `Por tempo`, `Por foto`). |
| Velocidade (m/s) | `SPEED` | Entrada | Velocidade do voo nos waypoints em m/s (padrão: 5.0 m/s). |
| Ângulo do gimbal (graus) | `GIMBAL_PITCH` | Entrada | Ângulo de inclinação do gimbal em graus (-90° a 20°, padrão: -90.0°). |
| Espera no waypoint (s) | `WAYPOINT_WAIT` | Entrada | Tempo de pausa em segundos em cada waypoint (padrão: 0.0 s). |
| Camada de elevação (DEM) — se informada, exporta em modo sobre terreno | `ELEVATION_LAYER` | Entrada | Camada raster DEM opcional para cálculo de altitude relativa ao terreno. |
| Tolerância do terreno (m) | `TOLERANCE` | Entrada | Tolerância de elevação na amostragem do terreno (padrão: 10.0 m). |
| Ponto de decolagem (opcional — padrão: primeiro waypoint) | `PONTO_DECOLAGEM` | Entrada | Coordenadas do ponto de decolagem de referência para cálculo de altura relativa (opcional). |
| Arquivo de saída (.csv) | `OUTPUT` | Saída | Caminho do arquivo CSV de destino para a missão Litchi. |

---

## 5. Exportar missão Litchi Mission Hub (.kml)

- **ID completo do algoritmo**: `qgc4qgis:exportar_litchi_kml`
- **Nome de exibição**: Exportar missão Litchi Mission Hub (.kml)
- **Grupo**: Planejamento de Voo (`planejamento_voo`)

### Descrição

Exporta uma missão de voo no formato Litchi Mission Hub KML (`.kml`) a partir de polígonos de cobertura ou linhas de voo para importação na plataforma flylitchi.com/hub.

### Entradas e Saídas

| Parâmetro (Interface) | Identificador | Direção | Descrição |
| :--- | :--- | :--- | :--- |
| Camada de entrada (Polígonos ou Linhas) | `INPUT` | Entrada | Camada vetorial de polígonos da área ou linhas de grade. |
| Câmera | `CAMERA` | Entrada | Perfil de câmera selecionado ou manual. |
| Altitude de voo (m) | `ALTITUDE` | Entrada | Altitude nominal de voo em metros (padrão: 100.0 m). |
| GSD (cm/px) - se > 0, se sobrepõe/calcula a altitude | `GSD` | Entrada | GSD desejado em cm/px (calcula/substitui altitude se > 0). |
| Sobreposição lateral (%) | `OVERLAP_SIDE` | Entrada | Porcentagem de sobreposição lateral (padrão: 70.0%). |
| Sobreposição frontal (%) | `OVERLAP_FRONTAL` | Entrada | Porcentagem de sobreposição frontal (padrão: 70.0%). |
| Ângulo da grade (graus) | `ANGLE` | Entrada | Ângulo da grade em graus (padrão: 0.0°). |
| Distância de manobra (m) | `TURNAROUND` | Entrada | Extensão adicional de manobra em metros. |
| Ponto de entrada | `ENTRY_LOCATION` | Entrada | Canto inicial da grade (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Grade cruzada (Re-voo 90°) | `REFLY` | Entrada | Opção para voo de grade dupla cruzada em 90°. |
| Câmera manual: Largura do sensor (mm) | `SENSOR_WIDTH` | Entrada | Largura do sensor manual em mm (opcional). |
| Câmera manual: Altura do sensor (mm) | `SENSOR_HEIGHT` | Entrada | Altura do sensor manual em mm (opcional). |
| Câmera manual: Largura da imagem (px) | `IMAGE_WIDTH` | Entrada | Largura da imagem manual em pixels (opcional). |
| Câmera manual: Altura da imagem (px) | `IMAGE_HEIGHT` | Entrada | Altura da imagem manual em pixels (opcional). |
| Câmera manual: Distância focal (mm) | `FOCAL_LENGTH` | Entrada | Distância focal manual em mm (opcional). |
| Modo de disparo | `TRIGGER_MODE` | Entrada | Mecanismo de disparo das fotos (`Por distância`, `Por tempo`, `Por foto`, padrão: `Por foto`). |
| Velocidade (m/s) | `SPEED` | Entrada | Velocidade do voo nos waypoints em m/s (padrão: 5.0 m/s). |
| Camada de elevação (DEM) — se informada, exporta em modo sobre terreno | `ELEVATION_LAYER` | Entrada | Camada raster DEM opcional para cálculo de altitude relativa ao terreno. |
| Tolerância do terreno (m) | `TOLERANCE` | Entrada | Tolerância de elevação na amostragem do terreno (padrão: 10.0 m). |
| Ponto de decolagem (opcional — padrão: primeiro waypoint) | `PONTO_DECOLAGEM` | Entrada | Coordenadas do ponto de decolagem de referência para cálculo de altura relativa (opcional). |
| Arquivo de saída (.kml) | `OUTPUT` | Saída | Caminho do arquivo KML de destino para o Litchi Mission Hub. |

---

## 6. Exportar missão DJI Fly (.kmz)

- **ID completo do algoritmo**: `qgc4qgis:exportar_dji_kmz`
- **Nome de exibição**: Exportar missão DJI Fly (.kmz)
- **Grupo**: Planejamento de Voo (`planejamento_voo`)

### Descrição

Exporta uma missão de voo no formato DJI WPML (`.kmz`) contendo `template.kml` e `waylines.wpml` para execução no aplicativo DJI Fly e controles remotos compatíveis.

### Entradas e Saídas

| Parâmetro (Interface) | Identificador | Direção | Descrição |
| :--- | :--- | :--- | :--- |
| Camada de entrada (Polígonos ou Linhas) | `INPUT` | Entrada | Camada vetorial de polígonos da área ou linhas de grade. |
| Câmera | `CAMERA` | Entrada | Perfil de câmera selecionado ou manual. |
| Altitude de voo (m) | `ALTITUDE` | Entrada | Altitude nominal de voo em metros (padrão: 100.0 m). |
| GSD (cm/px) - se > 0, se sobrepõe/calcula a altitude | `GSD` | Entrada | GSD desejado em cm/px (calcula/substitui altitude se > 0). |
| Sobreposição lateral (%) | `OVERLAP_SIDE` | Entrada | Porcentagem de sobreposição lateral (padrão: 70.0%). |
| Sobreposição frontal (%) | `OVERLAP_FRONTAL` | Entrada | Porcentagem de sobreposição frontal (padrão: 70.0%). |
| Ângulo da grade (graus) | `ANGLE` | Entrada | Ângulo da grade em graus (padrão: 0.0°). |
| Distância de manobra (m) | `TURNAROUND` | Entrada | Extensão adicional de manobra em metros. |
| Ponto de entrada | `ENTRY_LOCATION` | Entrada | Canto inicial da grade (`Top-Left`, `Top-Right`, `Bottom-Left`, `Bottom-Right`). |
| Grade cruzada (Re-voo 90°) | `REFLY` | Entrada | Opção para voo de grade dupla cruzada em 90°. |
| Câmera manual: Largura do sensor (mm) | `SENSOR_WIDTH` | Entrada | Largura do sensor manual em mm (opcional). |
| Câmera manual: Altura do sensor (mm) | `SENSOR_HEIGHT` | Entrada | Altura do sensor manual em mm (opcional). |
| Câmera manual: Largura da imagem (px) | `IMAGE_WIDTH` | Entrada | Largura da imagem manual em pixels (opcional). |
| Câmera manual: Altura da imagem (px) | `IMAGE_HEIGHT` | Entrada | Altura da imagem manual em pixels (opcional). |
| Câmera manual: Distância focal (mm) | `FOCAL_LENGTH` | Entrada | Distância focal manual em mm (opcional). |
| Modo de disparo | `TRIGGER_MODE` | Entrada | Mecanismo de disparo das fotos (`Por distância`, `Por tempo`, `Por foto`, padrão: `Por foto`). |
| Velocidade (m/s) | `SPEED` | Entrada | Velocidade do voo nos waypoints em m/s (padrão: 5.0 m/s). |
| Ângulo do gimbal (graus) | `GIMBAL_PITCH` | Entrada | Ângulo de inclinação do gimbal em graus (-90° a 20°, padrão: -90.0°). |
| Espera no waypoint (s) | `WAYPOINT_WAIT` | Entrada | Tempo de pausa em segundos em cada waypoint (padrão: 0.0 s). |
| Ação ao finalizar | `FINISH_ACTION` | Entrada | Ação do drone ao concluir a missão (`Retornar para casa (goHome)`, `Sem ação (noAction)`, `Pouso automático (autoLand)`, `Ir para 1º waypoint (gotoFirstWaypoint)`). |
| Ação se sinal RC for perdido | `RC_LOST_ACTION` | Entrada | Ação de segurança se perder sinal do controle (`Retornar (goBack)`, `Pousar (landing)`, `Pairar (hover)`). |
| Velocidade de transição (m/s) | `TRANSITIONAL_SPEED` | Entrada | Velocidade de deslocamento entre Home e início da missão em m/s (padrão: 5.0 m/s). |
| Estrutura do arquivo KMZ (ZIP) | `ZIP_LAYOUT` | Entrada | Estrutura interna do arquivo ZIP (`Subpasta wpmz/ (padrão DJI)` ou `Na raiz do arquivo`). |
| Camada de elevação (DEM) — se informada, exporta em modo sobre terreno | `ELEVATION_LAYER` | Entrada | Camada raster DEM opcional para conversão de altitude relativa ao terreno. |
| Tolerância do terreno (m) | `TOLERANCE` | Entrada | Tolerância de elevação na amostragem do terreno (padrão: 10.0 m). |
| Ponto de decolagem (opcional — padrão: primeiro waypoint) | `PONTO_DECOLAGEM` | Entrada | Coordenadas do ponto de decolagem de referência para cálculo de altura relativa (opcional). |
| Arquivo de saída (.kmz) | `OUTPUT` | Saída | Caminho do arquivo pacote KMZ (WPML) de destino. |

---

## 7. Baixar DEM Copernicus para área

- **ID completo do algoritmo**: `qgc4qgis:baixar_dem_copernicus`
- **Nome de exibição**: Baixar DEM Copernicus para área
- **Grupo**: Planejamento de Voo (`planejamento_voo`)

### Descrição

Baixa o modelo digital de elevação (DEM) Copernicus GLO-30 (~30m de resolução espacial global) para a extensão da camada vetorial de entrada, com uma margem de segurança configurável em metros.

### Entradas e Saídas

| Parâmetro (Interface) | Identificador | Direção | Descrição |
| :--- | :--- | :--- | :--- |
| Camada de polígonos | `INPUT` | Entrada | Camada vetorial de polígonos que define a região geográfica de interesse. |
| Margem de segurança (m) | `MARGEM` | Entrada | Raio de margem extra em metros expandido ao redor da caixa delimitadora (padrão: 250.0 m). |
| DEM de saída | `OUTPUT` | Saída | Caminho do arquivo GeoTIFF de destino para o raster DEM baixado. |
