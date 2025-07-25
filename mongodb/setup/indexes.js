// Script para criar índices no MongoDB
// Execute este script após criar as collections

// Selecionar o banco de dados
use dataops_challenge;

print("Criando índices para melhor performance...");

// Índices para collection carros
db.carros.createIndex({ "montadora": 1 }, { 
  name: "idx_carros_montadora",
  background: true 
});
print("Índice criado: carros.montadora");

db.carros.createIndex({ "carro": 1 }, { 
  name: "idx_carros_nome",
  background: true 
});
print("Índice criado: carros.carro");

db.carros.createIndex({ "cor": 1 }, { 
  name: "idx_carros_cor",
  background: true 
});
print("Índice criado: carros.cor");

// Índices para collection montadoras
db.montadoras.createIndex({ "montadora": 1 }, { 
  name: "idx_montadoras_nome",
  unique: true,
  background: true 
});
print("Índice criado: montadoras.montadora (único)");

db.montadoras.createIndex({ "pais": 1 }, { 
  name: "idx_montadoras_pais",
  background: true 
});
print("Índice criado: montadoras.pais");

// Índice composto para agregações
db.carros.createIndex({ "montadora": 1, "carro": 1 }, { 
  name: "idx_carros_montadora_nome",
  background: true 
});
print("Índice composto criado: carros.montadora + carros.carro");

print("\nListando todos os índices:");

print("\nÍndices da collection 'carros':");
db.carros.getIndexes().forEach(function(index) {
  print("  - " + index.name + ": " + JSON.stringify(index.key));
});

print("\nÍndices da collection 'montadoras':");
db.montadoras.getIndexes().forEach(function(index) {
  print("  - " + index.name + ": " + JSON.stringify(index.key));
});

// Estatísticas dos índices
print("\nEstatísticas dos índices:");
print("Carros - Total de índices: " + db.carros.getIndexes().length);
print("Montadoras - Total de índices: " + db.montadoras.getIndexes().length);

print("\nÍndices criados com sucesso!");
