// Agrega��o MongoDB - Desafio DataOps
// Esta agrega��o relaciona carros com montadoras e agrupa por pa�s

// Pipeline de agrega��o que:
// 1. Faz lookup entre carros e montadoras
// 2. Agrupa os carros por pa�s da montadora
// 3. Ordena os resultados por pa�s

db.carros.aggregate([
  // Est�gio 1: Lookup - relaciona carros com montadoras
  {
    $lookup: {
      from: "montadoras",              // Collection de destino
      localField: "montadora",         // Campo na collection carros
      foreignField: "montadora",       // Campo na collection montadoras
      as: "montadora_info"            // Nome do array resultado
    }
  },
  
  // Est�gio 2: Unwind - transforma array em documentos individuais
  {
    $unwind: "$montadora_info"
  },
  
  // Est�gio 3: Group - agrupa carros por pa�s da montadora
  {
    $group: {
      _id: "$montadora_info.pais",    // Agrupa por pa�s
      carros: {                       // Cria array com informa��es dos carros
        $push: {
          carro: "$carro",
          cor: "$cor",
          montadora: "$montadora"
        }
      }
    }
  },
  
  // Est�gio 4: Sort - ordena resultados por pa�s
  {
    $sort: { _id: 1 }
  }
]);

// Exemplo de resultado esperado:
/*
[
  {
    "_id": "Alemanha",
    "carros": [
      {
        "carro": "Polo",
        "cor": "Branco",
        "montadora": "Volkswagen"
      }
    ]
  },
  {
    "_id": "EUA",
    "carros": [
      {
        "carro": "Onix",
        "cor": "Prata",
        "montadora": "Chevrolet"
      },
      {
        "carro": "Fiesta",
        "cor": "Vermelho",
        "montadora": "Ford"
      }
    ]
  },
  {
    "_id": "Fran�a",
    "carros": [
      {
        "carro": "Sandero",
        "cor": "Prata",
        "montadora": "Renault"
      }
    ]
  },
  {
    "_id": "Jap�o",
    "carros": [
      {
        "carro": "City",
        "cor": "Preto",
        "montadora": "Honda"
      }
    ]
  }
]
*/

// Vers�o alternativa da agrega��o com mais detalhes
db.carros.aggregate([
  {
    $lookup: {
      from: "montadoras",
      localField: "montadora",
      foreignField: "montadora",
      as: "montadora_info"
    }
  },
  {
    $unwind: "$montadora_info"
  },
  {
    $project: {
      _id: 0,
      carro: 1,
      cor: 1,
      montadora: 1,
      pais: "$montadora_info.pais"
    }
  },
  {
    $group: {
      _id: "$pais",
      total_carros: { $sum: 1 },
      carros: {
        $push: {
          carro: "$carro",
          cor: "$cor",
          montadora: "$montadora"
        }
      }
    }
  },
  {
    $sort: { _id: 1 }
  }
]);

// Para salvar o resultado da agrega��o em uma nova collection:
// db.carros.aggregate([...pipeline...]).forEach(doc => db.resultado_agregacao.insertOne(doc));
