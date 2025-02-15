import numpy as np
from scipy.stats import entropy
import multiprocessing as mp
from functools import partial

    
def generatePattern(word: str, target: str):
    """
    🟩🟨🟥
    """
    #targetList = [*target]
    #print(targetList)
    pattern = ['🟥']*5
    wordset = set(word)
    targetset = set(target)
    targetList = [*target]
    common = wordset.intersection(target)
    #print(common)
    green = set()
    rest = set([0, 1, 2, 3, 4])
    for i, letter in enumerate(word):
        if letter in common:
           pattern[i] = '🟨'
           common.remove(letter)
     
    for i in range(5):
        if word[i] == target[i]:
            pattern[i] = '🟩'
    #print(common)      
    
               #common.remove(letter)
    #for i in rest:
        #if word[i] in common:
            #if word[i] not in green:
                #pattern[i] = '🟨'
                #targetList.remove(word[i])
                #common.remove(word[i])
    #print(word, target, common,pattern)
    return ' '.join(pattern)




def calculateEntropy(word: str, candidates: list, wordFreqDict = None):
    denominator = len(candidates)
    count = {}
    #Bprint(word, candidates)
    if wordFreqDict:
        freqs = np.zeros(denominator)
        for i, candidate in enumerate(candidates):
            freqs[i] = wordFreqDict[candidate]
        freqs = freqs/np.sum(freqs)
        freqs = freqs*denominator
        for i, candidate in enumerate(candidates):
            pattern = generatePattern(word, candidate)
            count[pattern] = count.get(pattern, 0.0) + freqs[i]
    else:
        for candidate in candidates:
            pattern = generatePattern(word, candidate)
            count[pattern] = count.get(pattern, 0) + 1
    pk = [value/denominator for value in count.values()]
    try:
        return entropy(pk)
    except:
        return 0.0
    

    
def selectNewCandidates(word, pattern, candidates):
    '''
    pattern_list = pattern.split()
    #print(pattern_list)
    #candidates_new = [candidate for candidate in candidates]
    mask = [1]*len(candidates)
    for location, key in enumerate(pattern_list):
        #print(location, key)
        if key == '🟩':
            for idx, candidate in enumerate(candidates):
                if candidate[location] != word[location]:
                    #print(candidate, word[location])
                    mask[idx] = 0
        if key == '🟨':
            for idx, candidate in enumerate(candidates):
                if word[location] not in candidate or word[location] == candidate[location]:
                    mask[idx] = 0     
        if key == '🟥':
            for idx, candidate in enumerate(candidates):
                if word[location] in candidate:
                    if word[location] == candidate[location]:    
                        #print(candidate, candidate[location] , word, word[location], location)
                        mask[idx] = 0
    candidates_new = [candidate for idx, candidate in enumerate(candidates) if mask[idx]]
    '''
                
    
    
    candidates_new = []
    for candidate in candidates:
        pattern_test = generatePattern(word, candidate)
        #print(candidate, pattern_test)
        if pattern_test == pattern:
            candidates_new.append(candidate)
    
    return candidates_new

def selectWord(candidates: list, wordFreqDict = None, alpha=10000):
    if len(candidates) == 0:
        return 'ERROR, try: tares', -1
    entropies = np.zeros(len(candidates))
    from tqdm import tqdm
    for i, word in enumerate(candidates):
        entropy = calculateEntropy(word, candidates, wordFreqDict)
        if wordFreqDict:
            entropies[i] = entropy + min(alpha*wordFreqDict.get(word, 0), 0.5)
        else:
            entropies[i] = entropy
        print(f'{word}: {entropy}')
    return candidates[np.argmax(entropies)], np.max(entropies)

def calculateEntropyWrapper(word, candidates, wordFreqDict):
    """Helper function for parallel execution"""
    e = calculateEntropy(word, candidates, wordFreqDict)
    if wordFreqDict:
        adjusted = e + min(10000 * wordFreqDict.get(word, 0), 0.5)
    else:
        adjusted = e
    return (word, e, adjusted)

def selectWord_parallel(candidates: list, wordFreqDict = None, alpha=10000, processes=None):
    if len(candidates) == 0:
        return 'ERROR, try: tares', -1
    
    # (2) PARALLEL PROCESSING LOGIC
    if processes is None:
        processes = mp.cpu_count()  # Use all available cores
    
    with mp.Pool(processes=processes) as pool:
        # Create partial function with fixed arguments
        worker = partial(calculateEntropyWrapper,
                        candidates=candidates,
                        wordFreqDict=wordFreqDict)
        
        # Process words in parallel
        from tqdm import tqdm
        results = tqdm(pool.imap(worker, candidates))
        
        # (3) PROCESS RESULTS WITH PROGRESS TRACKING
        max_score = -float('inf')
        best_word = ''
        entropy_values = []
        
        for i, (word, entropy, adjusted) in enumerate(results):
            #print(f'{word}: {entropy:.2f}')  # Maintain original output format
            entropy_values.append(entropy)
            
            if adjusted > max_score:
                max_score = adjusted
                best_word = word

    return best_word, max_score

def input_word_check(word):
    if len(word)!= 5:
        return False
    for letter in word:
        if letter not in 'abcdefghijklmnopqrstuvwxyz':
            return False
    return True 

def input_response_check(response):
    if len(response)!= 5:
        return False
    for letter in response:
        if letter not in '🟩🟨🟥':
            return False
    return True 

if __name__ == "__main__":
    intab = 'GYRBgyrb'
    outtab = '🟩🟨🟥🟥🟩🟨🟥🟥'
    trantab = str.maketrans(intab, outtab)
    wordList = []
    with open('words', 'r') as file:
        for word in file:
            word = word.strip()
            wordList.append(word)
    from wordfreq import word_frequency
    wordFreq = np.zeros(len(wordList))
    for i, word in enumerate(wordList):
        freq = word_frequency(word, 'en')
        wordFreq[i] = freq
    #wordFreq = wordFreq/np.sum(wordFreq)
    #wordFreq = wordFreq*len(wordList)
    wordFreqDict = dict(zip(wordList, wordFreq))
    #print(np.sum(wordFreq), len(wordList))
    
    
    
    print("Wordle Solver v0.2")
    candidates = wordList.copy()
    #word = selectWord_parallel(candidates)
    #print(word)
    #word_freq, _ = selectWord_parallel(candidates, wordFreqDict)
    #print(word_freq)
    word = 'raise'
    print(' '.join(word.upper()))
    response = input("INPUT RESPONSE:\n")
    response = response.translate(trantab).strip()
    while not input_response_check(response):
        print("Invalid input, please try again.")
        response = input("INPUT RESPONSE:\n")
        response = response.translate(trantab).strip()
    response = ' '.join(response)
    attempt = 0
    record_candidates = [candidates]
    record_word = ['rates']
    record_pattern = ['N N N N N']
    while response != '🟩 🟩 🟩 🟩 🟩':
        attempt += 1
        candidates = selectNewCandidates(word, response, candidates)
        #print(candidates)
        recommend_word, entropy = selectWord(candidates, wordFreqDict=wordFreqDict)
        #recommend_word, entro = selectWord(candidates, wordFreqDict=None)
        print('first attempt: ',' '.join(recommend_word.upper()), " score: ", entropy)
        try_times = 0
        while entropy == -1:
            try_times += 1
            initial_candidates = wordList.copy()
            print(len(initial_candidates))
            candidates_set = set(initial_candidates)
            subsets = []
            for pattern in record_pattern:
                subset = set(selectNewCandidates(word, pattern, initial_candidates))
                #print(subset)
                if len(subset) > 0:
                    subsets.append(subset)
            
            for subset in subsets:
                candidates_set = candidates_set.intersection(subset)
            candidates = list(candidates_set)
          
            recommend_word, entropy = selectWord(candidates, wordFreqDict=wordFreqDict, alpha = 10000-try_times*1500)
            print(f'attempt {try_times}: ',' '.join(recommend_word.upper()), " score: ", entropy)
            
            
        '''
        try_times = -1
        while entro == -1 and attempt >= 0:
            #print('yes')
            attempt -= 1
            candidates = record_candidates[try_times]
            pattern = record_pattern[try_times]
            
            #print(pattern)
            #print(candidates, word)
            try:
                candidates.remove(word)
            except:
                pass
            #print(pattern, word, candidates)
            word = record_word[try_times]
            #print(pattern, word, candidates)
            candidates = selectNewCandidates(word, pattern, candidates)
            recommend_word, entro = selectWord(candidates, wordFreqDict=wordFreqDict, alpha = 10000-try_times*1500)
            print('try: ', ' '.join(recommend_word.upper()), " score:", entro)
            try_times -= 1
        '''
        word = input("INPUT WORD:\n").lower()
        if word == "":
            word = recommend_word
            print("No input, use recommend word: ", ' '.join(recommend_word.upper()))
        while word != recommend_word and not input_word_check(word):
            print("Invalid input, please try again.")
            word = input("INPUT WORD:\n").lower()
            if word == "":
                word = recommend_word
                print("No input, use recommend word: ", ' '.join(recommend_word.upper()))
        response = input("INPUT RESPONSE:\n")
        response = response.translate(trantab).strip()
        while not input_response_check(response):
            print("Invalid input, please try again.")
            response = input("INPUT RESPONSE:\n")
            response = response.translate(trantab).strip()
        response = ' '.join(response)
     
        record_word.append(word)
        try:
            candidates.remove(word)
        except:
            pass
        record_pattern.append(response)
        record_candidates.append(candidates.copy())
        #print(f'record: {record_candidates}')
        #candidates = selectNewCandidates(word, response, candidates)
    