import numpy as np
import pandas as pd
import re
import typer
import os

def read_file(path):
    df = pd.read_csv(path)
    df = df.drop_duplicates(['title'],keep='first') #중복 처리를 해준다.
    return df

def remove_pattern(df, patterns, column_name):
    valid_index = [True] * df.shape[0]
    res = [True] * df.shape[0]
    for patt in patterns:
        patt_find = df[column_name].str.findall(patt, flags = re.IGNORECASE)
        valid_index = np.where(patt_find.apply(len) == 0, True, False)
        res = res & valid_index
    return res

def get_valid_df(df):
    column_name = 'title'
    url_patt = "(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}"
    word_patt  = r'\bfree\b|\binstall\b|\bdownload\b|\bapp\b|\bwallet\b|\bhardware\b|\blink\b|\bcard\b|\bpayapl\b|\bmine\b|\bplatform\b|\bbrowser\b|\bsite\b'
    patterns = [url_patt,word_patt]
    valid_index = remove_pattern(df, patterns, column_name)
    return df.loc[valid_index]

def main(subreddit:str):
    path = './dataset'
    if not os.path.exists(f'{path}/{subreddit}'):
        os.mkdir(f'{path}/{subreddit}')
    for f in os.listdir(path):
        try:
            df = read_file(f"{path}/{f}")
            df.drop('selftext',axis=1,inplace=True)
            typer.echo(f"{f}: start processing")
            total_cnt = df.shape[0]
            df = get_valid_df(df)
            df['vader'] = get_vader_df(df)['compound']
            removed_cnt = total_cnt - df.shape[0]
            df = df[['id','author','vader','title','created_utc','num_comments','score']]
            df.to_csv(f'{path}/{subreddit}/{f}')
            typer.echo(f"{f}: end processing (total: {total_cnt} removed: {removed_cnt})")
        except Exception as e:
            print(f'{e} got some problem')
            continue
if __name__ == '__main__':
    typer.run(main)
