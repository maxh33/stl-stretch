# stl-stretch

[![GitHub stars](https://img.shields.io/github/stars/maxh33/stl-stretch?style=social)](https://github.com/maxh33/stl-stretch)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 🇺🇸 [English version](README.md) &nbsp;|&nbsp; [github.com/maxh33/stl-stretch](https://github.com/maxh33/stl-stretch)

Alonga uma peça STL ou 3MF para impressão 3D **sem deformar furos, roscas ou chanfros**.
Não precisa do arquivo CAD: corta a malha onde a seção transversal é constante, afasta uma metade e preenche o vão.

Você baixou um modelo, ele está 10 cm curto demais e você só tem o STL. Escalar a malha estica tudo junto: furos redondos
viram ovais, flanges engrossam. O `stl-stretch` só acrescenta material onde a peça é um prisma reto, então o resto
continua exatamente como foi projetado.

![original vs escala simples vs stl-stretch](docs/before-after.png)

---

## Por que este projeto existe

Sou estudante de Ciência da Computação e desenvolvedor, não sou da área de impressão 3D. Eu precisava de um espremedor de
tubo para uma bisnaga de catupiry de 16 cm de largura, e o modelo que encontrei era uns 10 cm mais curto. O profissional
de impressão 3D com quem trabalho não customiza nem edita arquivos, então eu disse que alongar uma peça não era tão
complexo, pesquisei como se faz e passei as instruções. Ele não quis se aprofundar em customização de arquivos para
clientes que têm essa demanda.

Então, num fim de tarde, por curiosidade, eu mesmo fiz: busquei as dependências, descobri como alongar uma malha sem
estragar os furos e os dentes do ratchet e ajustei a peça conforme a minha necessidade. Depois mandei os arquivos já
prontos e customizados, e ao profissional só faltava apertar o botão de imprimir. Este repositório é aquele fim de
tarde, organizado para que a próxima pessoa com o mesmo problema não precise gastar o dela.

Construí com o [Claude Code](https://claude.com/claude-code) como par de programação: ele escreveu boa parte do código
enquanto eu definia o objetivo, escolhia os trade-offs e revisava cada resultado. Por isso nada aqui é aceito na
confiança: cada alongamento é conferido contra o comprimento e o volume esperados, e há um teste.

---

## Como funciona

```
peça.stl
    ↓
find_cut — amostra a área da seção ao longo do eixo e escolhe o meio da maior faixa constante
    ↓
stretch — corta a malha nesse plano, desloca uma metade em --delta e extruda a seção para preencher o vão
    ↓
uma malha única, soldada e estanque — verificada: comprimento = original + delta, volume = original + área da seção x delta
    ↓
mais-longa.stl (ou 3MF, OBJ, ...)
```

Construído sobre [trimesh](https://trimesh.org) e manifold3d. Lê e grava STL, 3MF, OBJ e o que mais o trimesh suportar.

---

## Início rápido

```bash
uv sync
uv run python src/stretch.py peca.stl mais-longa.stl --axis y --delta 107          # corte automático
uv run python src/stretch.py peca.stl mais-longa.stl --axis y --delta 107 --cut 35 # corte manual
uv run python examples/demo.py      # regenera a imagem acima a partir de uma peça gerada
uv run python tests/test_stretch.py
```

Arquivo com vários corpos? `--body N` alonga só o corpo N. Não sabe onde é seguro cortar? `src/sections.py peca.stl`
imprime a área da seção ao longo de Y, e dá para ver as faixas constantes.

## Outras ferramentas pequenas (linha de comando, todas em `src/`)

| Script | O que faz |
|---|---|
| `inspect_stl.py` | Bounding box, estanqueidade e número de corpos de cada STL em `input/` |
| `sections.py` | Área da seção ao longo de um eixo (acha as faixas onde alongar é seguro) |
| `orient.py` | Pontua as 6 orientações de impressão alinhadas aos eixos por área em balanço vs contato com a mesa |
| `preview.py`, `section_plot.py` | Renders PNG sem interface e gráficos de seção, úteis para conferir o resultado sem abrir o fatiador |
| `examples/make_plates.py` | Arruma as peças orientadas numa mesa de 256 mm e gera um 3MF por projeto, pronto para o Bambu Studio |

---

## Uso real

Usei para alongar um espremedor de tubo com ratchet para caber uma bisnaga de 16 cm de largura (vão de 63 mm para
170 mm) e para alargar um suporte infantil de pasta de dente para um tubo de 62 mm. Os dois modelos são de outros
autores no MakerWorld e **não** estão neste repositório; confira a licença deles antes de redistribuir qualquer coisa
derivada:

- [Ratcheted Toothpaste Tube Squeezer](https://makerworld.com/en/models/30246-ratcheted-toothpaste-tube-squeezer) (remix de Roland Deschain)
- [Stand for Toothpaste V5.0 (Kids' version)](https://makerworld.com/en/models/831100-stand-for-toothpaste-v5-0-kids-version) (3DKUB)

`examples/make_plates.py` é o meu script pessoal para esses dois; caminhos e medidas são específicos deles.

## Limites

- A peça precisa ser um prisma reto no plano de corte, em um eixo por vez. Formas orgânicas não têm esse plano e o
  `find_cut` avisa.
- Área de seção igual não prova que o contorno seja igual, então olhe um render antes de imprimir uma peça incomum.
- Só edita a geometria. Configuração do fatiador, suportes e material ficam por sua conta.

## Contribuindo

Ideias que tornariam isto mais útil, sem promessa: alongar em vários planos numa só execução, detectar o eixo
automaticamente, um comando `stl-stretch` de verdade em vez de `python src/stretch.py` e generalizar o `make_plates.py`.
Issues e pull requests são bem-vindos, principalmente com peças em que o `find_cut` escolhe um plano ruim.

---

Código aberto, licença MIT (veja [LICENSE](LICENSE)). Se isto te poupou um fim de tarde, uma ⭐ ajuda outras pessoas a encontrar.
