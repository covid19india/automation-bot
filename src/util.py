def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i : i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


ocr_dict = {
    "AP": "Andhra Pradesh",
    "BR": "Bihar",
    "CT": "Chhattisgarh",
    "HP": "Himachal Pradesh",
    "JK": "Jammu and Kashmir",
    "JH": "Jharkhand",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "UP": "Uttar Pradesh",
    "UT": "Uttarakhand",
    "TN": "Tamil Nadu",
}


pdf_dict = {
    "HR": "Haryana",
    "KA": "Karnataka",
    "PB": "Punjab",
    "TN": "Tamil Nadu",
    "WB": "West Bengal",
    "AP": "Andhra Pradesh",
}

dash_dict = {
    "AS": "Assam",
    "AP": "Andhra Pradesh",
    "GJ": "Gujarat",
    "KL": "Kerala",
    "LA": "Ladakh",
    "MH": "Maharashtra",
    "ML": "Meghalaya",
    "OR": "Odisha",
    "PY": "Puducherry",
    "TR": "Tripura",
}

