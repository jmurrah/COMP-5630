#!/usr/bin/env python3
import json
import os

def quick_fix_notebook(notebook_path):
    """
    Fix a Jupyter notebook by adding missing 'state' keys to metadata.widgets
    WITHOUT re-executing any cells.
    
    Args:
        notebook_path: Path to the notebook file
    """
    print(f"Fixing notebook: {notebook_path}")
    
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Check if the notebook has metadata
    if 'metadata' not in notebook:
        notebook['metadata'] = {}
    
    # Check if the notebook has widgets metadata
    if 'widgets' not in notebook['metadata']:
        print("No widgets metadata found. No changes needed.")
        return
    
    # Keep track of changes
    widgets_fixed = 0
    
    # For each widget, ensure it has a 'state' key
    for widget_key in notebook['metadata']['widgets']:
        if 'state' not in notebook['metadata']['widgets'][widget_key]:
            # Add an empty state object if missing
            notebook['metadata']['widgets'][widget_key]['state'] = {}
            widgets_fixed += 1
    
    if widgets_fixed > 0:
        print(f"Added 'state' key to {widgets_fixed} widgets")
        
        # Create a backup of the original file
        backup_path = notebook_path + '.backup'
        if not os.path.exists(backup_path):
            os.rename(notebook_path, backup_path)
            print(f"Original notebook backed up to {backup_path}")
        
        # Write the fixed notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1)
        
        print(f"Fixed notebook saved to {notebook_path}")
    else:
        print("All widgets already have 'state' keys. No changes needed.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python quick_fix_notebook.py <path_to_notebook.ipynb>")
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    if not os.path.exists(notebook_path):
        print(f"Error: File {notebook_path} not found")
        sys.exit(1)
    
    quick_fix_notebook(notebook_path)
    print("\nDone! Try opening the notebook again.")