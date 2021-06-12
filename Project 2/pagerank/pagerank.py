import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_of_links_from_page = len(corpus[page])
    num_of_pages = len(corpus)

    result_dict = {}

    if num_of_links_from_page == 0:
        for key in corpus:
            result_dict[key] = 1 / num_of_pages
        return result_dict

    unlinked_page_probability = (1 - damping_factor) * (1 / num_of_pages)
    linked_page_probability = (damping_factor * (1 / num_of_links_from_page)) + unlinked_page_probability

    for temp_page in corpus:
        if temp_page in corpus[page]:
            result_dict[temp_page] = linked_page_probability
        else:
            result_dict[temp_page] = unlinked_page_probability
    
    return result_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = corpus.keys()
    result_dict = {}
    init_page = random.choice(list(pages))
    result_dict[init_page] = 1 / n

    cur_page = init_page
    for i in range(n - 1):
        trans = transition_model(corpus, cur_page, damping_factor)
        cur_page = random.choices(list(trans.keys()), list(trans.values()))[0]
        result_dict[cur_page] = result_dict.get(cur_page, 0) + (1 / n)
    
    return result_dict



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_of_pages = len(corpus)
    pre_result_dict = {}
    margin = 0.001

    for page in corpus:
        pre_result_dict[page] = 1 / num_of_pages
    
    cur_result_dict = pre_result_dict.copy()

    while True:
        num_converged = 0
        for dest_page in corpus:
            updated_value = 0

            for src_page in corpus:
                if dest_page in corpus[src_page]:
                    updated_value += (pre_result_dict[src_page] / len(corpus[src_page]))
                elif len(corpus[src_page]) == 0:
                    updated_value += (pre_result_dict[src_page] / num_of_pages)

            updated_value *= damping_factor
            updated_value += (1 - damping_factor) / num_of_pages
            cur_result_dict[dest_page] = updated_value

            if abs(updated_value - pre_result_dict[dest_page]) < margin:
                num_converged += 1
            
        if num_converged == num_of_pages:
            break
        pre_result_dict = cur_result_dict.copy()
    
    return pre_result_dict



if __name__ == "__main__":
    main()
