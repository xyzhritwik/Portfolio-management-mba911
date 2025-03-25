import pandas as pd
import pdfplumber

def parse_reports(file_paths):
    holdings = []

    for path in file_paths:
        if path.endswith(".xlsx"):
            df = pd.read_excel(path, sheet_name=None)
            for name, sheet in df.items():
                if "PnL" in name or "Holdings" in name:
                    holdings.append(sheet)
        elif path.endswith(".pdf"):
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    lines = text.split("\n")
                    for line in lines:
                        if any(word in line for word in ["LTD", "LIMITED"]):
                            parts = line.split()
                            if len(parts) >= 4:
                                holdings.append({
                                    "Stock": parts[0],
                                    "Dividend": parts[-1].replace("Rs.", "")
                                })

    return pd.concat([pd.DataFrame(h) if isinstance(h, dict) else h for h in holdings], ignore_index=True)