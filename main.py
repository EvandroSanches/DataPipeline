import requests
import os
import json



def auth():
    os.environ['BEARER_TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAKwaagEAAAAA8r0SvQwAz3tV2PFm08Lk2MsQPa0%3DpsOsirCBtaVaqk16uqRE4NhKsD2qzo9kBYNMrYUYJlmqNWoSJI'
    return os.environ.get('BEARER_TOKEN')


def create_url():
    query = "AluraOnline"
    tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,text"
    user_fields = "expansions=author_id&user.fields=id,name,username,created_at"
    filters = "start_time=2022-04-28T00:00:00.00Z&end_time=2022-04-30T00:00:00.00Z"
    url = (f"https://api.twitter.com/2/tweets/search/recent?query={query}&{tweet_fields}"
           f"&{user_fields}&{filters}")
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def paginate(url, headers, next_token=""):
    if next_token:
        full_url = f"{url}&next_token={next_token}"
    else:
        full_url = url
    data = connect_to_endpoint(full_url,headers)
    yield data
    if "next_token" in data.get("meta",{}):
        yield from paginate(url, headers, data['meta']['next_token'])


def main():
    bearer_token = auth()
    print(bearer_token)
    url = create_url()
    headers = create_headers(bearer_token)
    for json_response in paginate(url, headers):
        print(json.dumps(json_response, indent=4, sort_keys=True))



if __name__ == "__main__":
    main()