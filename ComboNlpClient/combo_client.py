import json
import requests
import sys


class ComboSentenceSplitter:
    def __init__(self):
        self.api_urls = [
            ("OpenNlp", 'http://localhost:8081/sentsplit'),  # supervised
            ("NltkNlp", 'http://localhost:8082/sentsplit'),  # unsupervised
            ("CoreNlp", 'http://localhost:8083/sentsplit')   # rule-based
        ]

    def total_occurrences(self, haystack, needle, start=0):
        """
        find total occurrences of the needle in the haystack
        """
        k = 0
        start = haystack.find(needle, start)
        while start >=0:
            k += 1
            start = haystack.find(needle, start+len(needle))
        return k

    def find_kth_occurrence(self, haystack, needle, k, start=0):
        """
        find the k-th occurrence of the needle in the haystack
        """
        start = haystack.find(needle, start)
        while start >= 0 and k > 1:
            start = haystack.find(needle, start+len(needle))
            k -= 1
        return start

    def call_api(self, api_url, text):
        """
        call sent-split api to split the given text into sentences.
        """
        resp = requests.post(api_url, data = text)
        sentences = resp.json()

        split_positions = []
        start_idx = 0
        for sent in sentences:
            last_char = sent[-1]
            k = self.total_occurrences(sent, last_char)
            idx = self.find_kth_occurrence(text, last_char, k, start=start_idx)
            split_positions.append(idx)
            start_idx = idx + 1

        result = {}
        result["Sentences"] = sentences
        result["SplitPositions"] = split_positions

        return result

    def combo_split(self, text):
        """
        combine results of sentence splitters by majority vote.
        """
        # get results of different splitters
        api_results = []
        for api_name, api_url in self.api_urls:
            api_result = self.call_api(api_url, text)
            api_results.append((api_name, api_result))

        # count split positions
        split_position_dict = {}
        for api_name, api_res in api_results:
            for split_pos in api_res["SplitPositions"]:
                if split_pos in split_position_dict.keys():
                    split_position_dict[split_pos].append(api_name)
                else:
                    split_position_dict[split_pos] = [api_name] 
        
        # find majority splits
        split_positions = []
        for split_pos, api_names in split_position_dict.items():
            #print(split_pos, api_names)
            if (len(api_names) >= 2):
                split_positions.append((split_pos, api_names))

        sentences = []
        last_split_pos = -1
        for split_pos, api_names in split_positions:
            sentence = text[last_split_pos+1: split_pos+1]
            sentences.append((sentence.strip(), api_names))
            last_split_pos = split_pos

        result = {}
        result["ApiResults"] = api_results
        result["ComboResults"] = sentences
        return result


def main(argv):
    text = '  First Dr. Whitespace   in text is collapsed (all whitespace is replaced by single spaces).   If the result fits in the width, \nit is returned.   Otherwise, enough words are dropped \tfrom the end so that the remaining words plus the placeholder fit within width:  '

    # leading/trailing spaces will be ignored by sentence splitter anyway!
    trimmed_text = text.strip()

    splitter = ComboSentenceSplitter()
    x = splitter.combo_split(trimmed_text)

    print(x)

if __name__ == '__main__':
    main(sys.argv) 
