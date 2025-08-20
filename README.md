# Librarian - Kütüphane Yönetim Sistemi

Basit ve etkili bir kütüphane yönetim sistemi. Kitap ekleme, arama, silme ve Open Library API entegrasyonu ile gelişmiş kitap bilgisi alma özelliklerini içerir.

## Özellikler

- **Terminal Tabanlı CLI**: Interaktif komut satırı arayüzü
- **FastAPI REST API**: Modern web API sunucusu
- **Open Library Entegrasyonu**: ISBN ile otomatik kitap bilgisi alma
- **JSON Veri Depolama**: Yerel dosya tabanlı veri saklama
- **Kapsamlı Test Paketi**: Tüm bileşenler için otomatik testler

## Kurulum

### 1. Repoyu Klonlayın
```bash
git clone https://github.com/myaseminsungur/librarian.git
cd librarian
```

### 2. Sanal Ortam Oluşturun (Önerilen)
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# veya
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Kurun
```bash
pip install -r requirements.txt
```

## Kullanım

### Aşama 1-2: Terminal Uygulaması

CLI (Command Line Interface) uygulamasını başlatmak için:

```bash
python main.py
```

**Mevcut özellikler:**
- Kitap ekleme
- Kitap arama (başlık, yazar, ISBN)
- Kitap silme
- Tüm kitapları listeleme
- Kütüphane verilerini kaydetme/yükleme

### Aşama 3: API Sunucusu

FastAPI web sunucusunu başlatmak için:

```bash
uvicorn api:app --reload
```

API sunucusu `http://localhost:8000` adresinde çalışacaktır.

**API Dokümantasyonu:** `http://localhost:8000/docs`

## API Dokümantasyonu

### Endpoints

#### GET /books
Kütüphanedeki tüm kitapları listeler.

**Response:**
```json
[
  {
    "title": "Kitap Adı",
    "author": "Yazar Adı", 
    "isbn": "9781234567890"
  }
]
```

#### POST /books
ISBN numarası ile Open Library'den kitap bilgisi çekerek kütüphaneye ekler.

**Request Body:**
```json
{
  "isbn": "9782848300443"
}
```

**Response:**
```json
{
  "title": "Kitap Adı",
  "author": "Yazar Adı",
  "isbn": "9782848300443"
}
```

#### DELETE /books/{isbn}
Belirtilen ISBN'ye sahip kitabı kütüphaneden siler.

**Response:**
```json
{
  "message": "Book with ISBN 9782848300443 has been removed"
}
```

#### GET /books/search
Kütüphanedeki kitapları arar.

**Query Parameters:**
- `query`: Arama terimi
- `search_by`: Arama türü (`title`, `author`, `isbn`) - varsayılan: `title`

**Example:** `GET /books/search?query=python&search_by=title`

**Response:**
```json
[
  {
    "title": "Python Programming",
    "author": "John Doe",
    "isbn": "9781234567890"
  }
]
```

#### GET /books/search/online
Open Library API'sinde kitap arar.

**Query Parameters:**
- `query`: Arama terimi

**Example:** `GET /books/search/online?query=python`

**Response:**
```json
[
  {
    "title": "Python Crash Course",
    "author": "Eric Matthes",
    "isbn": "9781593279288"
  }
]
```

## Test Senaryoları

### Tüm Testleri Çalıştırma
```bash
python -m pytest tests/ -v
```

### Belirli Test Kategorileri

#### API Testleri
```bash
python -m pytest tests/test_api.py -v
```

#### Library Core Testleri
```bash
python -m pytest tests/test_library.py -v
```

#### CLI Testleri
```bash
python -m pytest tests/test_library_cli.py -v
```

#### Book Model Testleri
```bash
python -m pytest tests/test_book.py -v
```

### Test Kapsamı

**Toplam: 63 Test**
- **API Tests (14)**: FastAPI endpoint'leri
- **Library Tests (14)**: Kütüphane core işlevleri
- **CLI Tests (20)**: Komut satırı arayüzü
- **Book Tests (5)**: Kitap modeli
- **Basic Tests (10)**: Temel sistem testleri

### Manuel Test Örnekleri

#### API Test Örnekleri (curl ile)

**Kitap ekleme:**
```bash
curl -X POST "http://localhost:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"isbn": "9782848300443"}'
```

**Tüm kitapları listeleme:**
```bash
curl "http://localhost:8000/books"
```

**Kitap arama:**
```bash
curl "http://localhost:8000/books/search?query=python&search_by=title"
```

**Online arama:**
```bash
curl "http://localhost:8000/books/search/online?query=python"
```

**Kitap silme:**
```bash
curl -X DELETE "http://localhost:8000/books/9782848300443"
```

## Proje Yapısı

```
librarian/
├── api.py                 # FastAPI uygulaması
├── book.py               # Book model sınıfı
├── library.py            # Library core sınıfı
├── library_cli.py        # CLI interface
├── main.py              # CLI uygulaması giriş noktası
├── open_library.py      # Open Library API client
├── library.json         # Veri dosyası
├── requirements.txt     # Python bağımlılıkları
├── README.md           # Bu dosya
└── tests/              # Test dosyaları
    ├── test_api.py
    ├── test_library.py
    ├── test_library_cli.py
    ├── test_book.py
    └── test_basic.py
```

## Teknolojiler

- **Python 3.11+**
- **FastAPI**: Modern web API framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Pytest**: Test framework
- **HTTPX**: HTTP client (testing)
- **Open Library API**: Kitap bilgileri

## Geliştirme Aşamaları

- ✅ **Aşama 1**: Temel CLI uygulaması
- ✅ **Aşama 2**: Open Library API entegrasyonu
- ✅ **Aşama 3**: FastAPI REST API