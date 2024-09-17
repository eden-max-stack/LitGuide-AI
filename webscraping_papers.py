import requests
from bs4 import BeautifulSoup

def getScholarData(keywords):
    try:

        # Join keywords with "+" for Google Scholar search syntax
        search_query = "+" .join(keywords)

        # Base URL for Google Scholar search
        base_url = "https://scholar.google.com/scholar?q="

        # Combine base URL and search query
        url = base_url + search_query
        print(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361681261652"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        scholar_results = []
        for el in soup.select(".gs_r"):
            try:
                dict = {
                "title": el.select(".gs_rt")[0].text,
                "title_link": el.select(".gs_rt a")[0]["href"],   
                "id": el.select(".gs_rt a")[0]["id"],
                "cited_by_count": el.select(".gs_nph+ a")[0].text}  

                scholar_results.append(dict)
            
            except Exception as err:
                print(err)
                exit

            papers = []
            links = []

        for i in range(len(scholar_results)):
            #print(i)
            scholar_results[i] = {key: str(value) for key, value in scholar_results[i].items() if str(value) != "" and value is not None}
            result = scholar_results[i]
            papers.append(result["title"])
            links.append(result["title_link"])

        return papers, links
        

    except Exception as err:
        print("Error: " + str(err))


def getAuthorProfileData():
    try:
        url = "https://scholar.google.com/citations?hl=en&user=cOsxSDEAAAAJ"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        author_results = {}
        articles = []
        author_results['name'] = soup.select_one("#gsc_prf_in").text
        author_results['position'] = soup.select_one("#gsc_prf_inw+ .gsc_prf_il").text
        author_results['email'] = soup.select_one("#gsc_prf_ivh").text
        author_results['departments'] = soup.select_one("#gsc_prf_int").text
        for el in soup.select("#gsc_a_b .gsc_a_t"):
            article = {
                'title': el.select_one(".gsc_a_at").text,
                'link': "https://scholar.google.com" + el.select_one(".gsc_a_at")['href'],
                'authors': el.select_one(".gsc_a_at+ .gs_gray").text,
                'publication': el.select_one(".gs_gray+ .gs_gray").text
            }
            articles.append(article)
        for i in range(len(articles)):
            articles[i] = {k: v for k, v in articles[i].items() if v and v != ""}
        cited_by = {}
        cited_by['table'] = []
        cited_by['table'].append({})
        cited_by['table'][0]['citations'] = {}
        cited_by['table'][0]['citations']['all'] = soup.select_one("tr:nth-child(1) .gsc_rsb_sc1+ .gsc_rsb_std").text
        cited_by['table'][0]['citations']['since_2017'] = soup.select_one("tr:nth-child(1) .gsc_rsb_std+ .gsc_rsb_std").text
        cited_by['table'].append({})
        cited_by['table'][1]['h_index'] = {}
        cited_by['table'][1]['h_index']['all'] = soup.select_one("tr:nth-child(2) .gsc_rsb_sc1+ .gsc_rsb_std").text
        cited_by['table'][1]['h_index']['since_2017'] = soup.select_one("tr:nth-child(2) .gsc_rsb_std+ .gsc_rsb_std").text
        cited_by['table'].append({})
        cited_by['table'][2]['i_index'] = {}
        cited_by['table'][2]['i_index']['all'] = soup.select_one("tr~ tr+ tr .gsc_rsb_sc1+ .gsc_rsb_std").text
        cited_by['table'][2]['i_index']['since_2017'] = soup.select_one("tr~ tr+ tr .gsc_rsb_std+ .gsc_rsb_std").text
        print(author_results)
        print(articles)
        print(cited_by['table'])
    except Exception as e:
        print(e)

