# PyScrambleAPI

PyScrambleAPI is a Flask API that unscrambles sets of characters into actual words.
It leverages its own PyScramble module, which ranks potential matches based on their likelihood of being correct.

---

## Contents

1. [Features](#features)  
2. [Requirements](#requirements)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [API endpoints](#api-endpoints)  
6. [License](#license)

---

## Features

- **Simple endpoints**: Quickly unscramble letters by sending a POST or GET request with the letters you have.
- **Ranked results**: Returns a sorted list of possible words, ranked in order of likelihood by the PyScramble module.
- **Modular**: Built with Flask, making it easy to extend or integrate into larger systems.

---

## Requirements

Make sure you have the following installed:
- **Python 3.9.6+**
- **pip** (or another Python package manager)
- **Flask**
- **logging** 
- (Optional) A virtual environment tool (e.g. venv)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/arthurauffray/PyScramble.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd PyScramble
   ```
3. **Install the dependencies**:
   ```bash
   pip install logging flask
   ```
   *If desired, create and activate a virtual environment first.*

---

## Usage

1. **Start the Flask server**:
   ```bash
   python app.py
   ```
   By default, the server runs on `http://127.0.0.1:8080`.

2. **Send requests** to the API endpoints (see below). You can use tools like [curl](https://curl.se/) or [Postman](https://www.postman.com/) to test.

---

## API endpoints

Below is a list of the API's endpoints.

### `POST /unscramble`

**Description**: Accepts a JSON payload containing scrambled letters. Returns a list of possible words ordered by their rank.

**Request body**:
```json
{
  "letters": "hist"
}
```

**Example**:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"letters":"hist"}' \
     http://127.0.0.1:8080/unscramble
```

**Response**:
```json
{
  "status": "ok", 
  "message": [
    "hist", 
    "hits", 
    "isth", 
    "shit", 
    "sith", 
    "this", 
    "tshi"
  ]
}
```

---


### `GET /unscramble`

**Description**: Accepts a query parameter containing scrambled letters. Returns a list of possible words ordered by their rank.

**Request URL**:
```json
"http://127.0.0.1:8080/unscramble?letters=hist
```

**Example**:
```bash
curl -G \
     -d "letters=hist" \
     http://127.0.0.1:8080/unscramble
```

**Response**:
```json
{
  "status": "ok", 
  "message": [
    "hist", 
    "hits", 
    "isth", 
    "shit", 
    "sith", 
    "this", 
    "tshi"
  ]
}
```

---

### `GET /ping`

**Description**: Returns a status message to check for uptime.

**Response**:
```json
{
   "status": "ok",
   "message": "Pong!",
}
```

### `GET /`

**Description**: Returns a simple status to have a home page.

**Response**:
```json
{
   "status": "ok"
}
```

## License

This project is available under the MIT License. Feel free to fork, extend, and submit pull requests.

---

If you have any questions or run into issues, please open an issue in this repository.
