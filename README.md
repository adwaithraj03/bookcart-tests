# Bookcart — User Registration & Login Test Suite

**Assignment - 1**  
Prepare positive and negative test cases for the user registration and login modules of the Bookcart web application.

🔗 **App URL:** https://bookcart.azurewebsites.net/register

---

## 📁 Project Structure

```
bookcart_tests/
├── conftest.py          # pytest fixtures, screenshot hook, HTML report config
├── test_positive.py     # 10 positive test cases (registration + login)
├── test_negative.py     # 5 negative test cases (registration + login)
├── requirements.txt     # Python dependencies
└── screenshots/         # Auto-created — test screenshots saved here
```

---

## ✅ Test Cases

### Positive (10)
| ID | Description |
|----|-------------|
| TC_REG_P01 | Register with valid user details |
| TC_REG_P02 | Register with valid email format as username |
| TC_REG_P03 | Register with strong password |
| TC_REG_P04 | Register with unique username |
| TC_REG_P05 | Register with all required fields filled |
| TC_LOG_P01 | Login with valid email and password |
| TC_LOG_P02 | Login after successful registration |
| TC_LOG_P03 | Login with correct registered account |
| TC_LOG_P04 | Login and navigate to home page |
| TC_LOG_P05 | Login multiple times with valid credentials |

### Negative (5)
| ID | Description |
|----|-------------|
| TC_REG_N01 | Register with empty fields |
| TC_REG_N02 | Register with invalid email format |
| TC_REG_N03 | Register with already existing username |
| TC_LOG_N01 | Login with incorrect password |
| TC_LOG_N02 | Login with unregistered username |

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/bookcart-tests.git
cd bookcart-tests
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run all tests
```bash
pytest --html=report.html --self-contained-html -v
```

### 4. Run only positive tests
```bash
pytest test_positive.py --html=report_positive.html -v
```

### 5. Run only negative tests
```bash
pytest test_negative.py --html=report_negative.html -v
```

---

## 📋 Requirements

- Python 3.8+
- Google Chrome browser
- ChromeDriver (auto-managed via `webdriver-manager`)

---

## 📸 Screenshots

Screenshots are automatically captured for every test and embedded in the HTML report. They are also saved to the `screenshots/` folder.
