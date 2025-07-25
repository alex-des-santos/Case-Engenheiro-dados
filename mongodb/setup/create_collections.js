// Script para criar collections no MongoDB
// Execute este script no MongoDB shell ou MongoDB Compass

// Selecionar o banco de dados
use dataops_challenge;

// Criar collection de carros
db.createCollection("carros", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["carro", "cor", "montadora"],
      properties: {
        carro: {
          bsonType: "string",
          description: "Nome do carro - obrigat�rio"
        },
        cor: {
          bsonType: "string",
          description: "Cor do carro - obrigat�rio"
        },
        montadora: {
          bsonType: "string",
          description: "Nome da montadora - obrigat�rio"
        }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "warn"
});

print("Collection 'carros' criada com sucesso!");

// Criar collection de montadoras
db.createCollection("montadoras", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["montadora", "pais"],
      properties: {
        montadora: {
          bsonType: "string",
          description: "Nome da montadora - obrigat�rio"
        },
        pais: {
          bsonType: "string",
          description: "Pa�s de origem - obrigat�rio"
        }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "warn"
});

print("Collection 'montadoras' criada com sucesso!");

// Exibir collections criadas
print("Collections dispon�veis:");
db.getCollectionNames().forEach(function(collection) {
  print("- " + collection);
});

// Inserir dados de exemplo (opcional)
print("\nInserindo dados de exemplo...");

// Dados dos carros
db.carros.insertMany([
  { carro: "Onix", cor: "Prata", montadora: "Chevrolet" },
  { carro: "Polo", cor: "Branco", montadora: "Volkswagen" },
  { carro: "Sandero", cor: "Prata", montadora: "Renault" },
  { carro: "Fiesta", cor: "Vermelho", montadora: "Ford" },
  { carro: "City", cor: "Preto", montadora: "Honda" }
]);

print("Dados de carros inseridos: " + db.carros.countDocuments());

// Dados das montadoras
db.montadoras.insertMany([
  { montadora: "Chevrolet", pais: "EUA" },
  { montadora: "Volkswagen", pais: "Alemanha" },
  { montadora: "Renault", pais: "Fran�a" },
  { montadora: "Ford", pais: "EUA" },
  { montadora: "Honda", pais: "Jap�o" }
]);

print("Dados de montadoras inseridos: " + db.montadoras.countDocuments());

print("\nSetup completo!");
print("Para visualizar os dados:");
print("  db.carros.find().pretty()");
print("  db.montadoras.find().pretty()");
