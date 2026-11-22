// Colores del proyecto
#let azul = rgb("#0B2545")
#let turquesa = rgb("#13A89E")
#let ambar = rgb("#F2A541")
#let claro = rgb("#EEF3F8")

// Portada con banda de color
#let portada(titulo, pregunta, autores, curso) = block(
  width: 100%, radius: 10pt, inset: (x: 16pt, y: 14pt), below: 10pt,
  fill: gradient.linear(azul, rgb("#0F5E73"), turquesa, angle: 0deg),
)[
  #text(fill: rgb("#8FF3DF"), size: 8pt, weight: "bold", tracking: 1.5pt)[DOCUMENTO TÉCNICO · USD/COP]
  #v(2pt)
  #text(fill: white, size: 17pt, weight: "bold")[#titulo]
  #v(1pt)
  #text(fill: rgb("#D6ECFF"), size: 10.5pt, style: "italic")[#pregunta]
  #v(4pt)
  #text(fill: white, size: 8.5pt)[#autores] \
  #text(fill: rgb("#BFD7EA"), size: 8pt)[#curso]
]

// Tarjeta de cifra clave
#let tarjeta(titulo, valor, detalle) = block(
  width: 100%, radius: 8pt, inset: 8pt, fill: claro, stroke: (left: 3pt + turquesa),
)[
  #text(size: 7.5pt, fill: rgb("#5B6B7F"))[#titulo] \
  #text(size: 13pt, weight: "bold", fill: azul)[#valor] \
  #text(size: 7pt, fill: rgb("#5B6B7F"))[#detalle]
]

// Títulos de sección
#show heading: it => block(above: 11pt, below: 6pt)[
  #text(size: 12pt, weight: "bold", fill: azul)[#it]
  #v(-7pt)
  #line(length: 100%, stroke: 0.8pt + turquesa)
]

// Tablas y párrafos
#set par(justify: true, leading: 0.58em, spacing: 0.75em)
#show table: set text(size: 7.8pt)
#show table.cell.where(y: 0): set text(weight: "bold", fill: white)
#set table(
  fill: (x, y) => if y == 0 { azul } else if calc.even(y) { claro } else { white },
  stroke: none, inset: 4pt,
)
#show figure: set block(above: 6pt, below: 6pt)
#show figure.caption: set text(size: 7.8pt, fill: rgb("#5B6B7F"))
