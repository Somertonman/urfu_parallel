# urfu_parallel

Pretrained model on English language using a masked language modeling (MLM) objective. It was introduced in this paper and first released in this repository. This model is uncased: it does not make a difference between english and English.

based on https://huggingface.co/bert-base-uncased

## About the model

Masked language modeling (MLM): taking a sentence, the model randomly masks 15% of the words in the input then run the entire masked sentence through the model and has to predict the masked words. This is different from traditional recurrent neural networks (RNNs) that usually see the words one after the other, or from autoregressive models like GPT which internally masks the future tokens. It allows the model to learn a bidirectional representation of the sentence.



## Web interface

<img width="600" alt="image" src="https://user-images.githubusercontent.com/8521878/202905546-4fa14081-d0e1-45c4-a1e2-c3baaaf78ece.png">


### Successful result
<img width="600" alt="image" src="https://user-images.githubusercontent.com/8521878/202905576-c74b022b-ab2e-48ef-95fb-d98d9182dedd.png">

### Errors
<img width="600" alt="image" src="https://user-images.githubusercontent.com/8521878/202905606-5d041a93-733c-483d-8b46-0d4986beecfe.png">

### Screencast

[![IMAGE ALT TEXT HERE](https://user-images.githubusercontent.com/8521878/203010134-2d29c220-c79c-4927-b2a9-bbcea8596fe9.png)](https://www.youtube.com/watch?v=Nd18P_x4cCQ)


## API description


### JSON arguments

Parameter|Description|Default|Range|Mandatory|
|-|-|-|-|-|
sentence| String with "*" masked symbol| - | text| yes|
min_score| Minimal score of returned tokens| 0 | [0,1) | no |
n_of_results| Number of returned tokens| 5 | [0,5] |no |
words_only| Returns detailed metadata| False| True/False| no


### Example

#### Default vals

```
import requests
BASE_URL = "http://20.123.12.234:8000/get_suggestions"
query = "I * URFU."
response = requests.post(BASE_URL, json={'sentence':query}).json()
```
response for the given example:

```
{'data': [{'score': 0.3510996401309967,
   'sequence': 'i am urfu.',
   'token': 2572,
   'token_str': 'am'},
  {'score': 0.04048578813672066,
   'sequence': 'i need urfu.',
   'token': 2342,
   'token_str': 'need'},
  {'score': 0.037849340587854385,
   'sequence': 'i want urfu.',
   'token': 2215,
   'token_str': 'want'},
  {'score': 0.036747705191373825,
   'sequence': 'i love urfu.',
   'token': 2293,
   'token_str': 'love'},
  {'score': 0.03464050963521004,
   'sequence': 'i was urfu.',
   'token': 2001,
   'token_str': 'was'}],
 'status': 'ok'}
  ```

#### Optional vals

```
import requests
BASE_URL = "http://20.123.12.234:8000/get_suggestions"
query = "I * URFU."
response = requests.post(BASE_URL, json={'sentence':query}, 'words_only':False, "min_score": 0.2).json()
```
response
```
{'data': [{'score': 0.4385973811149597,
   'sequence': 'i have to go.',
   'token': 2031,
   'token_str': 'have'},
  {'score': 0.311788409948349,
   'sequence': 'i had to go.',
   'token': 2018,
   'token_str': 'had'}],
 'status': 'ok'}
```

#### Malformed request

```
import requests
BASE_URL = "http://20.123.12.234:8000/get_suggestions"
query = "I * URFU."
response = requests.post(BASE_URL, json={'sentence':query}, 'words_only':False, "min_score": 10).json()
```
response
```
{'details': 'min_score should be a real number in [0,1)', 'status': 'error'}
```



### Response

Service responds with a a JSON list of dictionaries sorted by *score*

keys|score|sequence|token|token_str|
|-|-|-|-|-|
description|score of the given word|sentence string with given word|unique token ID|token word|
example|0.3510996401309967|i am urfu.|2572|am|

