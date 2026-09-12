# 🏗️ Civil QuantEstimate

**Civil QuantEstimate** is a Streamlit-based web application designed to help civil engineering students, professionals, and construction users estimate quantities of common construction materials.

The application provides quick calculations for **brickwork, plaster, concrete, and steel**, along with material ratios, wastage considerations, and an AI-powered civil engineering assistant.

## 🚀 Features

* 🧱 **Brickwork Quantity Estimation**

  * Calculate required bricks and mortar.
  * Consider wall dimensions and mortar requirements.

* 🧱 **Plaster Quantity Estimation**

  * Estimate plaster material requirements.
  * Support for different mortar ratios.

* 🏗️ **Concrete Quantity Estimation**

  * Calculate concrete quantities.
  * Support for commonly used concrete mix ratios.

* 🔩 **Steel Quantity Estimation**

  * Calculate approximate steel requirements.
  * Support for different reinforcement bar sizes.

* 📊 **Material & Wastage Calculations**

  * Built-in material ratios.
  * Configurable/default wastage percentages.

* 🤖 **Civil Engineering AI Assistant**

  * Provides civil engineering-related assistance.
  * Helps users understand construction calculations and concepts.
  * Powered by the Groq API.

* 🎨 **Modern User Interface**

  * Responsive Streamlit interface.
  * Sidebar navigation.
  * Light and dark theme support.
  * Designed for desktop and mobile use.

* 📱 **Responsive Design**

  * Interface optimized for different screen sizes.
  * Mobile-friendly navigation and layouts.

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **Groq API**
* **HTML/CSS**
* **GitHub**
* **Streamlit Community Cloud**

## 📂 Project Structure

```text
civil-quantestimate/
│
├── app.py
├── style.css
├── requirements.txt
├── README.md
│
└── utils/
    ├── __init__.py
    ├── calculations.py
    ├── data.py
    └── groq_helper.py
```

### File Description

| File                    | Purpose                                              |
| ----------------------- | ---------------------------------------------------- |
| `app.py`                | Main Streamlit application and user interface        |
| `style.css`             | Custom styling and responsive UI                     |
| `requirements.txt`      | Python dependencies                                  |
| `utils/calculations.py` | Construction quantity calculation functions          |
| `utils/data.py`         | Material ratios, wastage defaults, and bar-size data |
| `utils/groq_helper.py`  | Groq AI assistant integration                        |
| `README.md`             | Project documentation                                |

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/civil-quantestimate.git
cd civil-quantestimate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Groq API key

Create a Streamlit secrets configuration and add:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

**Never upload your API key directly to GitHub.**

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🌐 Deployment

The application can be deployed using **Streamlit Community Cloud**.

Basic deployment process:

1. Upload the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select `app.py` as the main file.
5. Add the `GROQ_API_KEY` through Streamlit Secrets.
6. Deploy the application.

## 🧮 Supported Calculations

Civil QuantEstimate currently focuses on:

* Brickwork
* Plaster
* Concrete
* Steel
* Material quantities
* Mortar and concrete mix ratios
* Construction material wastage

The calculation modules are separated from the user interface to keep the project organized and easier to maintain.

## 🤖 AI Assistant

The application includes an AI assistant specifically designed around the **civil engineering and construction domain**.

It can assist with topics such as:

* Construction materials
* Quantity estimation
* Concrete
* Brickwork
* Plaster
* Steel reinforcement
* Construction calculations
* Basic civil engineering concepts

The assistant is powered by the **Groq API**.

## 🔐 Security

API credentials should be stored using **Streamlit Secrets** rather than being hard-coded into the application.

Do not commit files containing:

```text
GROQ_API_KEY
```

or any other private API credentials to GitHub.

## 📱 User Interface

Civil QuantEstimate provides a simple workflow:

```text
Dashboard
   │
   ├── Brickwork
   ├── Plaster
   ├── Concrete
   ├── Steel
   │
   └── AI Assistant
```

Users can select the required calculation, enter the relevant dimensions and parameters, and receive estimated material quantities.

## 🎯 Project Objective

The primary objective of Civil QuantEstimate is to make common construction quantity calculations **faster, simpler, and more accessible** through an easy-to-use web application.

It is particularly useful for students learning civil engineering concepts and users who need quick preliminary quantity estimates.

## 🔮 Future Improvements

Possible future improvements include:

* 📄 PDF estimation reports
* 📊 Advanced cost estimation
* 💰 Material price management
* 📈 Project cost summaries
* 🏢 Multiple project management
* 📐 Additional civil engineering calculations
* 💾 Saving and exporting estimates
* 🌐 Multi-language support
* 📱 Further mobile UI improvements



⭐ If you find this project useful, consider giving the repository a star!
