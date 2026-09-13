# Painel de planejamento de voo

O planejamento de missão de voo fotogramétrico pelo painel acoplável (*dock widget*) do QGC4QGIS segue um fluxo estruturado em **cinco passos**.

## Fluxo de trabalho em cinco passos

```text
[Passo 1: Polígono] ➔ [Passo 2: Câmera] ➔ [Passo 3: Altura/GSD] ➔ [Passo 4: Grade] ➔ [Passo 5: Exportação]
```

1. **Seleção do Polígono de Cobertura**:
   - Selecione a camada vetorial de polígonos que define a área de interesse (AOI).
   - Escolha a feição específica na camada ou utilize todas as feições para delimitar o perímetro do levantamento.

2. **Configuração da Câmera**:
   - Escolha um modelo de câmera pré-configurado da biblioteca de câmeras integradas (ex.: Sony ILCE-7R, câmeras DJI, etc.).
   - Alternativamente, selecione *Custom Camera* (Câmera Manual) para especificar as propriedades físicas do sensor: largura do sensor (mm), altura do sensor (mm), largura da imagem (px), altura da imagem (px) e distância focal (mm).

3. **Definição da Altura de Voo ou GSD**:
   - Escolha o parâmetro principal de controle: **Altura de Voo (m)** ou **GSD (cm/px)**.
   - Ao alterar um dos valores, o complemento calcula automaticamente o valor correspondente mantendo a relação óptica da câmera.

4. **Ajuste da Grade e Sobreposições**:
   - Defina a **Sobreposição Lateral (%)** (*side overlap*) e a **Sobreposição Frontal (%)** (*front overlap*).
   - Ajuste o **Ângulo da Grade (graus)** para orientar os transectos de voo no sentido desejado (ex.: alinhado ao vento ou à maior dimensão do terreno).
   - Configure a **Distância de Turnaround (m)** para prolongar as faixas além do polígono, permitindo estabilizar o voo antes das fotos.
   - Defina o **Ponto de Entrada** (*Top-Left*, *Top-Right*, *Bottom-Left*, *Bottom-Right*) e habilite a **Grade Cruzada (Refly 90°)** se desejar um voo ortogonal duplo.

5. **Pré-visualização e Exportação (.plan)**:
   - Visualize a grade de transectos, os centros das fotos e os polígonos de pegada (*footprints*) diretamente no mapa do QGIS em tempo real.
   - Verifique as estatísticas calculadas: área total (ha), extensão de voo (km), número estimado de fotos e tempo de voo.
   - Clique em **Exportar Plano QGC (.plan)** para salvar o arquivo pronto para ser importado no QGroundControl ou carregado no drone.

## Tabela de parâmetros

A tabela a seguir descreve todos os parâmetros disponíveis no painel acoplável e nas ferramentas de processamento do complemento (`gerar_grade_voo`, `gerar_centros_foto` e `exportar_plano_qgc`):

| Parâmetro | Identificador | Tipo / Unidade | Valor Padrão | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Camada de Entrada** | `INPUT` | Vetorial (Polígono / Linha) | *Obrigatório* | Camada vetorial contendo a geometria da área de cobertura ou linhas de transectos. |
| **Câmera** | `CAMERA` | Enum / Texto | `0` (Primeira da lista) | Câmera selecionada da biblioteca predefinida ou modelo manual (*Custom Camera*). |
| **Altura de Voo** | `ALTITUDE` | Numérico (`Double`) / metros (m) | `100.0` | Altura relativa de voo em relação ao ponto de decolagem. |
| **GSD** | `GSD` | Numérico (`Double`) / cm/px | `0.0` | Resolução no solo. Se > 0, calcula e substitui a altura de voo. |
| **Sobreposição Lateral** | `OVERLAP_SIDE` | Numérico (`Double`) / porcentagem (%) | `70.0` | Porcentagem de sobreposição entre faixas de voo adjacentes. |
| **Sobreposição Frontal** | `OVERLAP_FRONTAL` | Numérico (`Double`) / porcentagem (%) | `70.0` | Porcentagem de sobreposição entre imagens consecutivas na mesma faixa. |
| **Ângulo da Grade** | `ANGLE` | Numérico (`Double`) / graus (°) | `0.0` | Orientação dos transectos de voo em relação ao Norte (-180° a 180°). |
| **Turnaround** | `TURNAROUND` | Numérico (`Double`) / metros (m) | `0.0` | Extensão das linhas fora do polígono para manobra de curva e aceleração da aeronave. |
| **Ponto de Entrada** | `ENTRY_LOCATION` | Enum (`0`: Top-Left, `1`: Top-Right, `2`: Bottom-Left, `3`: Bottom-Right) | `0` | Canto de início da execução da grade de voo. |
| **Grade Cruzada** | `REFLY` | Booleano (`True`/`False`) | `False` | Se ativo, gera uma segunda grade de transectos perpendicular (90°) à primeira. |
| **Largura do Sensor** | `SENSOR_WIDTH` | Numérico (`Double`) / mm | `35.9` | Largura física do sensor fotográfico (usado em Câmera Manual). |
| **Altura do Sensor** | `SENSOR_HEIGHT` | Numérico (`Double`) / mm | `24.0` | Altura física do sensor fotográfico (usado em Câmera Manual). |
| **Largura da Imagem** | `IMAGE_WIDTH` | Numérico (`Integer`) / pixels | `7952` | Resolução horizontal da imagem capturada (usado em Câmera Manual). |
| **Altura da Imagem** | `IMAGE_HEIGHT` | Numérico (`Integer`) / pixels | `5304` | Resolução vertical da imagem capturada (usado em Câmera Manual). |
| **Distância Focal** | `FOCAL_LENGTH` | Numérico (`Double`) / mm | `35.0` | Distância focal real da lente da câmera (usado em Câmera Manual). |
| **Velocidade de Cruzeiro** | `CRUISE_SPEED` | Numérico (`Double`) / m/s | `15.0` | Velocidade horizontal nominal da aeronave em voo (utilizada na exportação do `.plan`). |
| **Velocidade Pairado** | `HOVER_SPEED` | Numérico (`Double`) / m/s | `5.0` | Velocidade horizontal de desaceleração/pairado em multicópteros. |
| **Firmware** | `FIRMWARE_TYPE` | Enum (`12`: PX4, `3`: ArduPilot) | `12` (PX4) | Protocolo e formato do piloto automático para exportação da missão. |
| **Tipo de Veículo** | `VEHICLE_TYPE` | Enum (`2`: Multicóptero, `1`: Asa Fixa, `19`: VTOL) | `2` (Multicóptero) | Categoria do veículo aéreo não tripulado. |

## Limitações conhecidas

Para manter total compatibilidade com o algoritmo original do QGroundControl, o QGC4QGIS herda duas limitações arquiteturais da biblioteca `SurveyComplexItem` do QGC:

### Polígono côncavo sem decomposição

- **Descrição**: O gerador de transectos de voo do QGC trata o polígono de cobertura como um único anel externo contínuo (*outer ring*). Ao processar áreas com geometrias côncavas (como formatos em "L", "C" ou "U") ou polígonos contendo furos (*donuts*), a grade é gerada varrendo a extensão total do envelope (*bounding envelope*).
- **Consequência**: O algoritmo não realiza a decomposição automática da geometria em subpolígonos convexos isolados. Como resultado, alguns transectos podem cruzar regiões fora do polígono entre duas reentrâncias côncavas.

### GSD calculado apenas pela largura do sensor

- **Descrição**: A equação de conversão entre Altura de Voo (m) e GSD (cm/px) no QGroundControl calcula a resolução no solo exclusivamente com base na dimensão horizontal do sensor (`sensorWidth`) e na largura da imagem em pixels (`imageWidth`):

$$\text{GSD} = \frac{\text{Altura de Voo (m)} \times \text{Largura do Sensor (mm)}}{\text{Distância Focal (mm)} \times \text{Largura da Imagem (px)}} \times 100$$

$$\text{Altura de Voo (m)} = \frac{\text{GSD (cm/px)} \times \text{Distância Focal (mm)} \times \text{Largura da Imagem (px)}}{\text{Largura do Sensor (mm)} \times 100}$$

- **Consequência**: A dimensão vertical do sensor (`sensorHeight`) e a altura da imagem em pixels (`imageHeight`) não afetam o cálculo escalar do GSD nem a altura de voo gerada, sendo utilizadas apenas para determinar a extensão das pegadas (*footprints*) e a distância de disparo frontal de fotos.
