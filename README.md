# Personal Finance Tracker  

A lightweight **Streamlit** web app for tracking personal finances, built primarily for **NAB (National Australia Bank)** CSV exports.  
Upload your NAB account statement, categorise transactions using **custom rules**, and get **interactive summaries** and **charts** of your spending.

> ⚠️ **Note:**  
This tool was built for **personal use** and currently works best with **NAB bank CSV formats**.  
If you're using another bank, you may need to adjust your CSV headers to match the expected NAB structure.

---

## ✨ Features

- **CSV Upload** → Handles NAB-style CSV statements  
- **Custom Categories** → Create your own categories and persist them in `custom_categories.json`  
- **Interactive Data Editor** → Easily edit categories directly in the browser  
- **Spending Insights** → Get totals + pie chart breakdown by custom categories  
- **Persistent Rules** → Your custom categories automatically save for future sessions  

---

## NAB Expected CSV Format

The app was built around **NAB's CSV export format** from online banking.  
Your CSV should look like this:

| **Column**            | **Example Value**   | **Notes**                                |
|-----------------------|----------------------|-----------------------------------------|
| Date                 | `05 Jan 25`         | Must be `%d %b %y` format              |
| Merchant Name        | `Coles`             | Used for custom category matching      |
| Transaction Details  | `POS 1234 Coles`    | Free-text description                 |
| Category            | `Groceries`         | NAB’s auto-assigned category          |
| Amount             | `-45.50`           | Negative = expense, Positive = income |
| Balance           | `1032.75`         | Balance after the transaction        |

> 💡 If your NAB CSV uses slightly different headers, **rename the columns** to match this format before uploading.

---


## Tech Stack

- **Frontend / UI** → [Streamlit](https://streamlit.io/)
- **Data Processing** → [pandas](https://pandas.pydata.org/)
- **Charts** → [Plotly Express](https://plotly.com/python/plotly-express/)

---
