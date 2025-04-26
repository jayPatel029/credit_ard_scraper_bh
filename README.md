# Credit Card Scraper using AI (Groq API + Streamlit)

This project extracts credit card information either from **web URLs** or **PDF documents** using **LLM (Groq API)** and displays the results in a simple **Streamlit web app**.

---

## 🚀 How to Setup and Run Locally

Follow these steps to get started:

### 1. Clone the Repository

```bash
git clone git@github.com:jayPatel029/credit_card_scraper_bh.git
cd credit_card_scraper_bh
```

---

### 2. Open Terminal in Project Folder

You can open any IDE (like VSCode, PyCharm) and open a **new terminal** inside the project root.

---

### 3. Install `uv` (Fast Python Environment Manager)

Install `uv` globally (if not already installed):

```bash
pip install uv
```

`uv` is used for fast dependency installation.

---

### 4. Get your Groq API Key

- Visit [Groq Console](https://console.groq.com/home).
- Sign up (if you don’t have an account).
- Click on "**Create API Key**".
- Copy your new API key.

---

### 5. Set up Environment Variables

In your project root, create a `.env` file.

Paste the following inside `.env`:

```env
groc_api_key = "your-api-key-here"
```

Make sure to replace `"your-api-key-here"` with your actual Groq API key.

---

### 6. Install Dependencies

Now install all required Python libraries by running:

```bash
uv sync
```

> ⚡ **Note**: If `uv` does not work for you, you can still use the traditional method:
> 
> ```bash
> pip install -r requirements.txt
> ```

---

### 7. Run the Streamlit App

Start the app using:

```bash
streamlit run streamlit_app.py
```

The app will open automatically in your browser (usually at `http://localhost:8501`).

---

## 🧪 How to Test the App

You can test credit card extraction **from URLs or PDFs**:

### 👉 Testing with URLs

- In **Option 1 (URL field)**, paste one of the following sample links:

```
Link 1: https://www.paisabazaar.com/credit-card/best-credit-cards-online-shopping/
Link 2: https://cardinsider.com/best-credit-cards-in-india/
```

- Hit `Enter` after pasting the URL.
- Wait a few seconds; the JSON output will appear on the screen.

---

### 👉 Testing with PDFs

- In the **pdfs/** folder inside the project, you will find sample PDFs.
- Download a PDF from there.
- Then in **Option 2 (File Upload field)**, upload a PDF directly.

**OR**

- Copy the full path to a local PDF file and paste it into **Option 1 (URL field)**, then hit `Enter`.

---

## 📦 Output Location

- The extracted card data will appear as **JSON** on your screen.
- Also, it will be **saved automatically** inside the `/outputs/` folder as `.json` files.

> If the `outputs/` folder doesn't exist, it will be created automatically.

---

## 📂 Important Project Files

Here are the key files and folders to understand the project structure:

- **`main.py`** — Local entry point to run core functionality.
- **`streamlit_app.py`** — Main entry point for launching the Streamlit web app.
- **`scraper/`** — Contains all core logic:
  - Functions for scraping websites and PDFs.
  - Text extraction, chunking, LLM communication, and JSON saving.

> Explore these files first to quickly understand how the project works internally.

---

## ⚡ Important Notes

- **Free-tier Groq API** is being used — large files (or many cards) might take a little longer to process.
- Make sure your `.env` file is properly set up, otherwise the API won't work.
- If any module is missing, re-run `uv sync` or manually install it.

---

## 🛠️ Project Tech Stack

- **Python 3.10+**
- **Streamlit** (Frontend App)
- **Groq API** (Backend LLM - LLaMA 3 Model)
- **PyMuPDF / pdfminer / pypdf** (for PDF reading)
- **BeautifulSoup** (for Web scraping)
- **Jina Reader** (for extracting and normalizing web page content)
- **uv** (for Dependency Management)

---

# 🙏 Thank You for Visiting!

If you liked the project or found it useful, feel free to contribute or suggest improvements!

Happy Scraping! 🧹🚀
