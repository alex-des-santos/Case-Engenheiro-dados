#!/usr/bin/env python3
# Simple test script for dependencies

def main():
    print("Testing Python dependencies...")
    
    try:
        import pandas as pd
        print("SUCCESS: Pandas imported")
        
        # Test DataFrame creation
        carros_data = {
            'carro': ['Onix', 'Polo', 'Sandero', 'Fiesta', 'City'],
            'cor': ['Prata', 'Branco', 'Prata', 'Vermelho', 'Preto'],
            'montadora': ['Chevrolet', 'Volkswagen', 'Renault', 'Ford', 'Honda']
        }
        
        df_carros = pd.DataFrame(carros_data)
        print("SUCCESS: Cars DataFrame created")
        print(df_carros)
        
        # Test second DataFrame
        montadoras_data = {
            'montadora': ['Chevrolet', 'Volkswagen', 'Renault', 'Ford', 'Honda'],
            'pais': ['EUA', 'Alemanha', 'Franca', 'EUA', 'Japao']
        }
        
        df_montadoras = pd.DataFrame(montadoras_data)
        print("SUCCESS: Manufacturers DataFrame created")
        print(df_montadoras)
        
    except ImportError as e:
        print(f"ERROR: Cannot import pandas - {e}")
        return False
    
    try:
        from pymongo import MongoClient
        print("SUCCESS: PyMongo imported")
        
    except ImportError as e:
        print(f"ERROR: Cannot import pymongo - {e}")
        return False
        
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)
        print("SUCCESS: Colorama imported")
        
    except ImportError as e:
        print(f"ERROR: Cannot import colorama - {e}")
        return False
    
    print("\nAll dependencies are working!")
    print("\nNext steps:")
    print("1. Install MongoDB locally")
    print("2. Run: python scripts/main_local.py")
    print("3. Or configure remote connection and run: python scripts/main_remote.py")
    
    return True

if __name__ == "__main__":
    main()
