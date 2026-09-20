# 3d-printing

Scripts em Python para editar malhas STL (alongar peças, gerar placas 3MF prontas para o Bambu Studio).

Os modelos em si **não estão neste repositório**: são de terceiros (MakerWorld) e a licença deles não permite redistribuição.
Baixe os originais e coloque em `input/`:

- [Ratcheted Toothpaste Tube Squeezer](https://makerworld.com/en/models/30246-ratcheted-toothpaste-tube-squeezer) (remix de Roland Deschain) em `input/squeezer-catupiry/`
- [Stand for Toothpaste V5.0 (Kids' version)](https://makerworld.com/en/models/831100-stand-for-toothpaste-v5-0-kids-version) (3DKUB) em `input/stand-bepantol/`

## Uso

```bash
uv sync
uv run python src/inspect_stl.py                   # bounding box e estanqueidade de cada STL em input/
uv run python src/sections.py peca.stl             # área da seção ao longo de Y: acha faixas seguras pra alongar
uv run python src/stretch.py in.stl out.stl y 35 107   # alonga 107 mm no eixo Y cortando em y=35
uv run python src/orient.py peca.stl               # pontua as 6 orientações de impressão
PYTHONPATH=src uv run python src/make_plates.py    # gera os .3mf em output/
```

`stretch.py` só funciona onde a seção transversal é constante no ponto de corte (verifique com `sections.py`).
Os caminhos e medidas de `make_plates.py` são específicos dos dois modelos acima.
