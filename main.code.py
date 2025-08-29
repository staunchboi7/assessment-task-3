import pandas as pd
import matplotlib.pyplot as plt
import os

LINE_ROUTES = {
    # Suburban
    'T1': 'Berowra/Hornsby to Richmond',
    'T2': 'Parramatta to City',
    'T3': 'Liverpool/City to Lidcombe',
    'T4': 'Cronulla to Bondi Junction',
    'T5': 'Richmond to City',
    'T7': 'Olympic Park to City',
    'T8': 'Macarthur to City',
    'T9': 'Hornsby/Northern Line to North Shore',
    
    # Intercity
    'Blue Mountains': 'Central to Lithgow/Katoomba',
    'Central Coast & Newcastle': 'Central to Newcastle',
    'South Coast': 'Central to Kiama',
    'Southern Highlands': 'Central to Goulburn/Moss Vale',
    'Hunter': 'Newcastle to Dungog'
}

def load_data_manually(filename):
    """Read the CSV file manually to avoid pandas parsing issues"""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            

            for line in lines:
                line = line.strip()
                if line and not line.startswith('Line,Period,Date,Punctuality'): 
                    if ',' in line:
                        parts = line.split(',')
                        if len(parts) >= 4:
                            data.append(parts[:4])
        return data
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

def main():
    print("Sydney Trains Punctuality Data Viewer")
    print("=" * 40)
    
    # 1. Ask user which network they want to see
    print("\nWhich network would you like to explore?")
    print("1. Suburban")
    print("2. Intercity")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == '1':
        filename = 'Suburban.csv'
        network_name = 'Suburban'
    elif choice == '2':
        filename = 'Intercity.csv'
        network_name = 'Intercity'
    else:
        print("Invalid choice. Please run again and choose 1 or 2.")
        return
    
    # 2. Look for file in folder
    if not os.path.exists(filename):
        print(f"Error: {filename} not found in current directory.")
        print(f"Current directory: {os.getcwd()}")
        return
    
    # 3. Load data
    print(f"\nLoading {network_name} data...")
    raw_data = load_data_manually(filename)
    
    if not raw_data:
        print("No data found or error reading file.")
        return
    
    # 4. Use panda to convert raw data
    df = pd.DataFrame(raw_data, columns=['Line', 'Period', 'Date', 'Punctuality'])
    
    # 5. Show available lines
    available_lines = df['Line'].unique()
    print(f"\nAvailable lines in {network_name} network:")
    for i, line in enumerate(available_lines, 1):
        print(f"{i}. {line}")
    
    # 6. Get user line choice and show where that line goes
    try:
        line_choice = int(input(f"\nSelect a line (1-{len(available_lines)}): ")) - 1
        selected_line = available_lines[line_choice]
        
        print(f"\nSelected: {selected_line}")
        if selected_line in LINE_ROUTES:
            print(f"Route: {LINE_ROUTES[selected_line]}")
        print("-" * 50)
        
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
    
    # 7. Period choice
    print("\nWhat type of data would you like to see?")
    print("1. Monthly data")
    print("2. Yearly data")
    print("3. Both")
    
    period_choice = input("Enter your choice (1-3): ").strip()
    
    # 8. Filter (needed help for this part)
    filtered_data = df[df['Line'] == selected_line]
    
    if period_choice == '1':
        filtered_data = filtered_data[filtered_data['Period'] == 'Month']
        period_name = 'Monthly'
    elif period_choice == '2':
        filtered_data = filtered_data[filtered_data['Period'] == 'Year']
        period_name = 'Yearly'
    else:
        period_name = 'Both Monthly and Yearly'
    
    # 9. Show data
    if filtered_data.empty:
        print(f"\nNo data found for {selected_line} ({period_name})")
    else:
        print(f"\n{network_name} Network: {selected_line} Line ({period_name})")
        print("-" * 50)
        
        for _, row in filtered_data.iterrows():
            print(f"{row['Period']:6} {row['Date']:15} {row['Punctuality']:>6}")
        
        # 10. Ask about graph
        show_graph = input("\nWould you like to see a graph? (y/n): ").lower()
        
        if show_graph in ['y', 'yes']:
            # Make graph
            graph_data = filtered_data.copy()
            graph_data['Punctuality_Number'] = graph_data['Punctuality'].str.replace('%', '').astype(float)
            
            # Create plot
            plt.figure(figsize=(12, 6))
            plt.plot(graph_data['Date'], graph_data['Punctuality_Number'], 
                     marker='o', linestyle='-', linewidth=2, markersize=6)
            
            plt.title(f'{selected_line} Line Punctuality ({period_name})')
            plt.xlabel('Time Period')
            plt.ylabel('Punctuality (%)')
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            plt.show()
            print("Graph displayed! Close the window to continue.")

if __name__ == "__main__":
    main()