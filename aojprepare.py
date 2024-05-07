"""
AOJの問題を解くためのテンプレートを作成するスクリプト
引数には問題のIDとタイトル(省略可)を指定する
"""

import re
import os
import sys
import requests
import datetime
from bs4 import BeautifulSoup

from src.scripts import prepare_template

# テンプレートの言語。src/code_templates/aojフォルダ内のファイル名と一致させる。
template_type = "rs"
# ファイルなどを生成するディレクトリ
target_dir = ""

class AOJ(prepare_template.CompProgTemplate):
    def __init__(self):
        self.key_dict = {
            "本文": "html",
            "回答者数": "solvedUser",
            "正解率": "successRate",
            "得点": "score",
            "提供元": "source",
            "問題ID": "problem_id",
            "実行時間制限": "time_limit",
            "メモリ制限": "memory_limit",
            "作成日時": "created_at",
            "タイトル": "title",
        }
        self.code_template_location = 'src/code_templates/aoj'

    def get_folder_name(self, description):
        """フォルダ名の生成"""
        return f'{datetime.datetime.now().strftime("%m%d")}/{description["problem_id"]}_{description["title"]}'

    def get_file_name(self, description):
        """ファイル名の生成"""
        return self.get_folder_name(description).split("/")[-1]

    def get_data(self, id, title):
        """
        AOJのAPIを使って問題の情報を取得。titleが指定されていない場合は問題文から取得。
        """
        description_url = f'https://judgeapi.u-aizu.ac.jp/resources/descriptions/en/{id}'
        testcase_url = f'https://judgedat.u-aizu.ac.jp/testcases/samples/{id}'
        description = requests.get(description_url).json()
        description["title"] = title if title else self.get_title(description["html"])
        testcase = requests.get(testcase_url).json()
        return description, testcase

    def get_title(self, html):
        """問題文からタイトルを取得"""
        soup = BeautifulSoup(html, 'html.parser')
        first_line = soup.get_text(separator='\n').strip().split('\n')[0]
        return re.sub(r'[\\/:\*\?"<>\| ]', '', first_line)

if __name__ == '__main__':
    contest = AOJ()
    id = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else None
    description, testcase = contest.get_data(id, title)
    folder_name = os.path.join(target_dir, contest.get_folder_name(description))
    file_name = contest.get_file_name(description)
    contest.create_files(description, testcase, folder_name, file_name, template_type)