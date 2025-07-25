// Agregação MongoDB - Desafio DataOps
// Esta agregação relaciona carros com montadoras e agrupa por país

// Pipeline de agregação que:
// 1. Faz lookup entre carros e montadoras
// 2. Agrupa os carros por país da montadora
// 3. Ordena os resultados por país

db.carros.aggregate([
  // Estágio 1: Lookup - relaciona carros com montadoras
  {
    $lookup: {
      from: "montadoras",              // Collection de destino
      localField: "montadora",         // Campo na collection carros
      foreignField: "montadora",       // Campo na collection montadoras
      as: "montadora_info"            // Nome do array resultado
    }
  },
  
  // Estágio 2: Unwind - transforma array em documentos individuais
  {
    $unwind: "$montadora_info"
  },
  
  // Estágio 3: Group - agrupa carros por país da montadora
  {
    $group: {
      _id: "$montadora_info.pais",    // Agrupa por país
      carros: {                       // Cria array com informações dos carros
        $push: {
          carro: "$carro",
          cor: "$cor",
          montadora: "$montadora"
        }
      }
    }
  },
  
  // Estágio 4: Sort - ordena resultados por país
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
    "_id": "França",
    "carros": [
      {
        "carro": "Sandero",
        "cor": "Prata",
        "montadora": "Renault"
      }
    ]
  },
  {
    "_id": "Japão",
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

// Versão alternativa da agregação com mais detalhes
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

// Para salvar o resultado da agregação em uma nova collection:
// db.carros.aggregate([...pipeline...]).forEach(doc => db.resultado_agregacao.insertOne(doc));
