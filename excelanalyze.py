import pandas as pd
from difflib import SequenceMatcher
from tkinter import Tk, filedialog

# Load Excel file
def load_excel(file_path):
    return pd.read_excel(file_path)

# Calculate string similarity
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Search for the best match in the Excel file
def search_excel(query, dataframe):
    dataframe["Similarity"] = dataframe.apply(lambda row: similarity(query, str(row)), axis=1)
    best_match_index = dataframe["Similarity"].idxmax()
    return dataframe.loc[best_match_index]

# Tkinter file dialog for selecting Excel file
def choose_file():
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx;*.xls"), ("All Files", "*.*")]
    )

    return file_path

# Search interface with Tkinter GUI
def search_interface_gui():
    print("Welcome to the Excel Search Interface!")

    while True:
        input("Press Enter to pick the Excel file...")
        excel_file_path = choose_file()

        if not excel_file_path:
            print("No file selected. Exiting.")
            break

        print(f"Loading Excel file: {excel_file_path}")
        excel_data = load_excel(excel_file_path)
        print("Excel file loaded successfully.")

        while True:
            user_query = input("Enter your search query (type 'exit' to pick a new file): ")
            if user_query.lower() in ["exit", "quit"]:
                break

            best_match = search_excel(user_query, excel_data)
            response = best_match["Response"]
            similarity_score = best_match["Similarity"]

            print(f"\nBest Match (Similarity: {similarity_score:.2%}):")
            print(response)

if __name__ == "__main__":
    search_interface_gui()
