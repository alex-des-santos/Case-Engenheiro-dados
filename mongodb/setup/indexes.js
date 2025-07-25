// Script para criar �ndices no MongoDB
// Execute este script ap�s criar as collections

// Selecionar o banco de dados
use dataops_challenge;

print("Criando �ndices para melhor performance...");

// �ndices para collection carros
db.carros.createIndex({ "montadora": 1 }, { 
  name: "idx_carros_montadora",
  background: true 
});
print("�ndice criado: carros.montadora");

db.carros.createIndex({ "carro": 1 }, { 
  name: "idx_carros_nome",
  background: true 
});
print("�ndice criado: carros.carro");

db.carros.createIndex({ "cor": 1 }, { 
  name: "idx_carros_cor",
  background: true 
});
print("�ndice criado: carros.cor");

// �ndices para collection montadoras
db.montadoras.createIndex({ "montadora": 1 }, { 
  name: "idx_montadoras_nome",
  unique: true,
  background: true 
});
print("�ndice criado: montadoras.montadora (�nico)");

db.montadoras.createIndex({ "pais": 1 }, { 
  name: "idx_montadoras_pais",
  background: true 
});
print("�ndice criado: montadoras.pais");

// �ndice composto para agrega��es
db.carros.createIndex({ "montadora": 1, "carro": 1 }, { 
  name: "idx_carros_montadora_nome",
  background: true 
});
print("�ndice composto criado: carros.montadora + carros.carro");

print("\nListando todos os �ndices:");

print("\n�ndices da collection 'carros':");
db.carros.getIndexes().forEach(function(index) {
  print("  - " + index.name + ": " + JSON.stringify(index.key));
});

print("\n�ndices da collection 'montadoras':");
db.montadoras.getIndexes().forEach(function(index) {
  print("  - " + index.name + ": " + JSON.stringify(index.key));
});

// Estat�sticas dos �ndices
print("\nEstat�sticas dos �ndices:");
print("Carros - Total de �ndices: " + db.carros.getIndexes().length);
print("Montadoras - Total de �ndices: " + db.montadoras.getIndexes().length);

print("\n�ndices criados com sucesso!");
