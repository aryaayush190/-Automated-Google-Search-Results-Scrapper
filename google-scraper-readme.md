# Google Search Results Scraper

## Overview
A Python-based tool for scraping Google search results. This scraper extracts titles, links, and snippets from Google search results pages, with features for customization and different output formats.

## Features
- Extracts search result titles, URLs, and snippets
- Configurable number of results
- Multiple output formats (CSV, JSON)
- Language and country customization
- Built-in rate limiting
- Robust error handling
- Detailed logging
- User agent rotation to avoid blocking

## Requirements
```
python >= 3.7
requests
beautifulsoup4
pandas
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/google-scraper.git
cd google-scraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage
### Command Line Interface
Basic usage:
```bash
python scraper.py "your search query"
```

With options:
```bash
python scraper.py "your search query" --results 20 --format json --lang en --country us
```

### Arguments
- `query`: Search query (required)
- `--results`: Number of results to fetch (default: 10)
- `--format`: Output format (csv or json, default: csv)
- `--lang`: Language code (default: en)
- `--country`: Country code (default: us)

### As a Python Module
```python
from scraper import GoogleScraper

scraper = GoogleScraper()
results = scraper.search("python programming", num_results=20)
scraper.save_results(results, output_format='json')
```

## Output Format
### CSV Example
```csv
position,title,link,snippet
1,"Title 1","https://example1.com","Snippet 1"
2,"Title 2","https://example2.com","Snippet 2"
```

### JSON Example
```json
[
  {
    "position": 1,
    "title": "Title 1",
    "link": "https://example1.com",
    "snippet": "Snippet 1"
  }
]
```

## Best Practices
1. Respect Google's robots.txt
2. Use reasonable delays between requests
3. Don't make too many requests in a short time
4. Consider using a proxy for large-scale scraping
5. Check Google's Terms of Service before use

## Error Handling
- Failed requests are logged to `scraper.log`
- The script implements exponential backoff
- Malformed results are skipped and logged

## Limitations
- May be blocked by Google if used too frequently
- Cannot bypass Google's anti-bot measures
- Limited to organic search results

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License

## Disclaimer
This tool is for educational purposes only. Be sure to comply with Google's Terms of Service and robots.txt when using it.

## Author
Your Name
- GitHub: [@yourusername]
- Email: your.email@example.com
