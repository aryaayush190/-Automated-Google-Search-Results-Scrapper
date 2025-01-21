import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
from datetime import datetime
import argparse
from urllib.parse import quote_plus
import logging

class GoogleScraper:
    def __init__(self):
        self.base_url = "https://www.google.com/search"
        # Rotate different user agents to avoid blocking
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        self.setup_logging()

    def setup_logging(self):
        """Configure logging settings"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )

    def get_random_headers(self):
        """Generate random headers for requests"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def search(self, query, num_results=10, lang='en', country='us'):
        """
        Perform Google search and extract results
        
        Args:
            query (str): Search query
            num_results (int): Number of results to fetch
            lang (str): Language code
            country (str): Country code
        
        Returns:
            list: List of dictionaries containing search results
        """
        results = []
        start_index = 0
        
        while len(results) < num_results:
            try:
                # Construct search URL
                params = {
                    'q': query,
                    'start': start_index,
                    'hl': lang,
                    'gl': country,
                    'num': min(10, num_results - len(results))
                }
                
                # Add random delay between requests
                time.sleep(random.uniform(1.0, 3.0))
                
                # Make request
                response = requests.get(
                    self.base_url,
                    params=params,
                    headers=self.get_random_headers(),
                    timeout=30
                )
                response.raise_for_status()
                
                # Parse results
                soup = BeautifulSoup(response.text, 'html.parser')
                search_results = soup.find_all('div', class_='g')
                
                if not search_results:
                    logging.warning(f"No results found for page starting at index {start_index}")
                    break
                
                # Extract information from each result
                for result in search_results:
                    try:
                        title_element = result.find('h3')
                        link_element = result.find('a')
                        snippet_element = result.find('div', class_='VwiC3b')
                        
                        if title_element and link_element and snippet_element:
                            results.append({
                                'title': title_element.text.strip(),
                                'link': link_element['href'],
                                'snippet': snippet_element.text.strip(),
                                'position': len(results) + 1
                            })
                            
                            if len(results) >= num_results:
                                break
                                
                    except Exception as e:
                        logging.error(f"Error parsing individual result: {str(e)}")
                        continue
                
                start_index += 10
                
            except requests.RequestException as e:
                logging.error(f"Request failed: {str(e)}")
                break
                
            except Exception as e:
                logging.error(f"Unexpected error: {str(e)}")
                break
        
        return results[:num_results]

    def save_results(self, results, output_format='csv'):
        """
        Save results to file
        
        Args:
            results (list): Search results
            output_format (str): Format to save results (csv or json)
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_format.lower() == 'csv':
            df = pd.DataFrame(results)
            filename = f'search_results_{timestamp}.csv'
            df.to_csv(filename, index=False)
            logging.info(f"Results saved to {filename}")
            
        elif output_format.lower() == 'json':
            filename = f'search_results_{timestamp}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logging.info(f"Results saved to {filename}")
            
        else:
            logging.error("Invalid output format specified")

def main():
    parser = argparse.ArgumentParser(description='Google Search Results Scraper')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--results', type=int, default=10, help='Number of results to fetch')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='Output format')
    parser.add_argument('--lang', default='en', help='Language code')
    parser.add_argument('--country', default='us', help='Country code')
    
    args = parser.parse_args()
    
    scraper = GoogleScraper()
    logging.info(f"Starting search for query: {args.query}")
    
    results = scraper.search(
        args.query,
        num_results=args.results,
        lang=args.lang,
        country=args.country
    )
    
    scraper.save_results(results, args.format)
    logging.info(f"Scraping completed. Found {len(results)} results")

if __name__ == "__main__":
    main()
