#!/usr/bin/env python3
"""
Script para corrigir campos null nos modelos AdoptedLevel e Statement
"""

import os
import sys
import django

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zeppelin.settings')
django.setup()

from apps.questionnaire.models import AdoptedLevel, Statement

def fix_adopted_levels():
    """Corrige AdoptedLevels com campos null"""
    print("Corrigindo AdoptedLevels...")
    
    # Mapeamento de nomes para descrições
    name_to_description = {
        'Not Adopted': 'Prática não adotada pela organização',
        'Não Adotado': 'Prática não adotada pela organização',
        'Partially Adopted': 'Prática parcialmente adotada pela organização',
        'Parcialmente Adotado': 'Prática parcialmente adotada pela organização',
        'Fully Adopted': 'Prática totalmente adotada pela organização',
        'Totalmente Adotado': 'Prática totalmente adotada pela organização',
    }
    
    updated_count = 0
    for level in AdoptedLevel.objects.all():
        updated = False
        
        # Corrige description null ou vazio
        if not level.description:
            level.description = name_to_description.get(
                level.name, 
                f'Nível de adoção: {level.name}'
            )
            updated = True
        
        # Corrige name null ou vazio
        if not level.name:
            level.name = f'Nível {level.percentage}%'
            updated = True
            
        if updated:
            level.save()
            updated_count += 1
            print(f"  - Corrigido: {level.name}")
    
    print(f"Total de AdoptedLevels corrigidos: {updated_count}")

def fix_statements():
    """Corrige Statements com campos null"""
    print("\nCorrigindo Statements...")
    
    updated_count = 0
    for statement in Statement.objects.all():
        updated = False
        
        # Corrige text null ou vazio
        if not statement.text:
            statement.text = f'Declaração para {statement.code or "questão"}'
            updated = True
        
        # Corrige code null ou vazio
        if not statement.code:
            statement.code = f'STMT_{statement.id}'
            updated = True
            
        if updated:
            statement.save()
            updated_count += 1
            print(f"  - Corrigido: {statement.code}")
    
    print(f"Total de Statements corrigidos: {updated_count}")

if __name__ == "__main__":
    print("Iniciando correção de campos null...")
    fix_adopted_levels()
    fix_statements()
    print("\nCorreção concluída!")