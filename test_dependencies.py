# -*- coding: utf-8 -*-
"""
Script de teste para verificar dependências
"""

def test_imports():
    """Testa se todas as dependências estão instaladas"""
    
    try:
        import pandas as pd
        print("? Pandas importado com sucesso")
        
        # Testar criação de DataFrame
        df = pd.DataFrame({'teste': [1, 2, 3]})
        print(f"? DataFrame criado: {len(df)} linhas")
        
    except ImportError as e:
        print(f"? Erro ao importar pandas: {e}")
        return False
    
    try:
        from pymongo import MongoClient
        print("? PyMongo importado com sucesso")
        
    except ImportError as e:
        print(f"? Erro ao importar pymongo: {e}")
        return False
        
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)
        print(f"{Fore.GREEN}? Colorama importado com sucesso{Style.RESET_ALL}")
        
    except ImportError as e:
        print(f"? Erro ao importar colorama: {e}")
        return False
    
    print("\n?? Todas as dependências estão funcionando!")
    return True

def create_sample_dataframes():
    """Cria os DataFrames de exemplo do desafio"""
    import pandas as pd
    
    print("\n?? Criando DataFrames do desafio...")
    
    # DataFrame Carros
    carros_data = {
        'carro': ['Onix', 'Polo', 'Sandero', 'Fiesta', 'City'],
        'cor': ['Prata', 'Branco', 'Prata', 'Vermelho', 'Preto'],
        'montadora': ['Chevrolet', 'Volkswagen', 'Renault', 'Ford', 'Honda']
    }
    
    df_carros = pd.DataFrame(carros_data)
    print("\n?? DataFrame Carros:")
    print(df_carros.to_string(index=False))
    
    # DataFrame Montadoras
    montadoras_data = {
        'montadora': ['Chevrolet', 'Volkswagen', 'Renault', 'Ford', 'Honda'],
        'pais': ['EUA', 'Alemanha', 'França', 'EUA', 'Japão']
    }
    
    df_montadoras = pd.DataFrame(montadoras_data)
    print("\n?? DataFrame Montadoras:")
    print(df_montadoras.to_string(index=False))
    
    return df_carros, df_montadoras

if __name__ == "__main__":
    print("?? TESTE DE DEPENDÊNCIAS - DESAFIO DATAOPS")
    print("=" * 50)
    
    if test_imports():
        df_carros, df_montadoras = create_sample_dataframes()
        
        print("\n? Teste concluído com sucesso!")
        print("\n?? Próximos passos:")
        print("1. Instalar MongoDB localmente")
        print("2. Executar: python scripts/main_local.py")
        print("3. Ou configurar conexão remota em configs/remote_config.py")
        print("4. E executar: python scripts/main_remote.py")
        
    else:
        print("\n? Alguns problemas foram encontrados.")
        print("Execute: pip install -r requirements.txt")
